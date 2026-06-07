"""Tempo-aware MIDI quantization.

Piano transcription models (e.g. piano-transcription-inference) emit MIDI
with note onsets at their raw real-time positions under a placeholder tempo
(usually 120 BPM). For any performance that isn't exactly 120 BPM (i.e.
all of them), notes never land on a beat grid, which makes every downstream
notation tool produce micro-fragmented tied output.

This module recovers a beat grid from the original audio with librosa,
snaps every MIDI note onset/offset onto that grid (default: 1/16 notes),
and rewrites the MIDI under a single canonical tempo so ticks fall exactly
on subdivision boundaries.
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path

import librosa
import mido
import numpy as np

TICKS_PER_BEAT = 480


@dataclass
class QuantizeResult:
    bpm: float
    beats_detected: int
    grid_points: int
    notes: int
    notes_merged: int
    notes_dropped: int


def _detect_beat_grid(audio_path: Path) -> tuple[float, np.ndarray]:
    y, sr = librosa.load(str(audio_path), sr=22050, mono=True)
    tempo, beat_frames = librosa.beat.beat_track(y=y, sr=sr, units="frames")
    beat_times = librosa.frames_to_time(beat_frames, sr=sr)
    bpm = float(tempo if np.isscalar(tempo) else tempo[0])
    return bpm, beat_times


def _build_subdiv_grid(beat_times: np.ndarray, subdiv: int) -> np.ndarray:
    if len(beat_times) < 2:
        raise ValueError("Need at least 2 detected beats to build a grid")

    grid: list[float] = []
    for a, b in zip(beat_times[:-1], beat_times[1:]):
        step = (b - a) / subdiv
        for i in range(subdiv):
            grid.append(a + i * step)
    grid.append(float(beat_times[-1]))

    median_beat = float(np.median(np.diff(beat_times)))
    extension_step = median_beat / subdiv
    last = grid[-1]
    for _ in range(subdiv * 8):
        last += extension_step
        grid.append(last)

    return np.asarray(grid)


def _snap_index(t: float, grid: np.ndarray) -> int:
    if t <= grid[0]:
        return 0
    if t >= grid[-1]:
        return len(grid) - 1
    idx = int(np.searchsorted(grid, t))
    before = grid[idx - 1]
    after = grid[idx]
    return idx - 1 if (t - before) <= (after - t) else idx


def _extract_notes(mid: mido.MidiFile) -> list[dict]:
    """Return notes with absolute on/off times in seconds under the source tempo map."""
    tempo_us = 500_000
    for tr in mid.tracks:
        for msg in tr:
            if msg.type == "set_tempo":
                tempo_us = msg.tempo
                break
        else:
            continue
        break
    sec_per_tick = (tempo_us / 1_000_000.0) / mid.ticks_per_beat

    notes: list[dict] = []
    for track in mid.tracks:
        abs_ticks = 0
        active: dict[int, list[tuple[int, int]]] = {}
        for msg in track:
            abs_ticks += msg.time
            if msg.type == "note_on" and msg.velocity > 0:
                active.setdefault(msg.note, []).append((abs_ticks, msg.velocity))
            elif msg.type == "note_off" or (msg.type == "note_on" and msg.velocity == 0):
                stack = active.get(msg.note)
                if stack:
                    start_tick, vel = stack.pop(0)
                    notes.append(
                        {
                            "pitch": msg.note,
                            "velocity": vel,
                            "start_sec": start_tick * sec_per_tick,
                            "end_sec": abs_ticks * sec_per_tick,
                        }
                    )
    return notes


def _merge_same_pitch_overlaps(
    quantized: list[tuple[int, int, int, int]],
) -> tuple[list[tuple[int, int, int, int]], int]:
    """Collapse same-pitch notes that overlap or touch into a single sustained note.

    Transcription models often re-trigger held piano notes (especially under sustain
    pedal), and quantization can leave the new onset landing on or before the prior
    offset. Without merging, MuseScore is forced to render them as separate voices.
    """
    by_pitch: dict[int, list[list[int]]] = {}
    for on, off, pitch, vel in quantized:
        by_pitch.setdefault(pitch, []).append([on, off, vel])

    merged: list[tuple[int, int, int, int]] = []
    merge_count = 0
    for pitch, runs in by_pitch.items():
        runs.sort()
        cur_on, cur_off, cur_vel = runs[0]
        for on, off, vel in runs[1:]:
            if on <= cur_off:
                cur_off = max(cur_off, off)
                cur_vel = max(cur_vel, vel)
                merge_count += 1
            else:
                merged.append((cur_on, cur_off, pitch, cur_vel))
                cur_on, cur_off, cur_vel = on, off, vel
        merged.append((cur_on, cur_off, pitch, cur_vel))

    return merged, merge_count


def _build_quantized_midi(
    notes: list[dict], bpm: float, grid: np.ndarray, subdiv: int
) -> tuple[mido.MidiFile, int]:
    ticks_per_subdiv = TICKS_PER_BEAT // subdiv

    quantized: list[tuple[int, int, int, int]] = []
    for n in notes:
        on_idx = _snap_index(n["start_sec"], grid)
        off_idx = _snap_index(n["end_sec"], grid)
        if off_idx <= on_idx:
            off_idx = on_idx + 1
        quantized.append(
            (on_idx * ticks_per_subdiv, off_idx * ticks_per_subdiv, n["pitch"], n["velocity"])
        )

    quantized, merge_count = _merge_same_pitch_overlaps(quantized)

    events: list[tuple[int, str, int, int]] = []
    for on_tick, off_tick, pitch, vel in quantized:
        events.append((on_tick, "on", pitch, vel))
        events.append((off_tick, "off", pitch, 0))

    events.sort(key=lambda e: (e[0], 0 if e[1] == "off" else 1))

    out = mido.MidiFile(ticks_per_beat=TICKS_PER_BEAT)
    meta = mido.MidiTrack()
    meta.append(mido.MetaMessage("set_tempo", tempo=int(round(60_000_000 / bpm)), time=0))
    meta.append(mido.MetaMessage("time_signature", numerator=4, denominator=4, time=0))
    out.tracks.append(meta)

    notes_track = mido.MidiTrack()
    last_tick = 0
    for tick, kind, pitch, vel in events:
        delta = tick - last_tick
        last_tick = tick
        if kind == "on":
            notes_track.append(mido.Message("note_on", note=pitch, velocity=vel, time=delta))
        else:
            notes_track.append(mido.Message("note_off", note=pitch, velocity=0, time=delta))
    out.tracks.append(notes_track)
    return out, merge_count


def _filter_notes(
    notes: list[dict], *, min_velocity: int, min_note_sec: float
) -> tuple[list[dict], int]:
    kept: list[dict] = []
    dropped = 0
    for n in notes:
        if n["velocity"] < min_velocity:
            dropped += 1
            continue
        if (n["end_sec"] - n["start_sec"]) < min_note_sec:
            dropped += 1
            continue
        kept.append(n)
    return kept, dropped


def quantize_midi(
    audio_path: Path,
    midi_in: Path,
    midi_out: Path,
    meta_path: Path | None = None,
    *,
    subdiv: int = 4,
    min_velocity: int = 0,
    min_note_ms: int = 0,
) -> QuantizeResult:
    bpm, beats = _detect_beat_grid(audio_path)
    grid = _build_subdiv_grid(beats, subdiv)

    mid = mido.MidiFile(str(midi_in))
    notes = _extract_notes(mid)

    notes, drop_count = _filter_notes(
        notes,
        min_velocity=min_velocity,
        min_note_sec=min_note_ms / 1000.0,
    )

    out_mid, merge_count = _build_quantized_midi(notes, bpm, grid, subdiv)
    midi_out.parent.mkdir(parents=True, exist_ok=True)
    out_mid.save(str(midi_out))

    result = QuantizeResult(
        bpm=bpm,
        beats_detected=int(len(beats)),
        grid_points=int(len(grid)),
        notes=len(notes) - merge_count,
        notes_merged=merge_count,
        notes_dropped=drop_count,
    )
    if meta_path is not None:
        meta_path.write_text(
            json.dumps(
                {
                    "bpm": result.bpm,
                    "beats_detected": result.beats_detected,
                    "grid_points": result.grid_points,
                    "notes": result.notes,
                    "notes_merged": result.notes_merged,
                    "notes_dropped": result.notes_dropped,
                    "min_velocity": min_velocity,
                    "min_note_ms": min_note_ms,
                    "subdiv": subdiv,
                    "ticks_per_beat": TICKS_PER_BEAT,
                },
                indent=2,
            )
            + "\n",
            encoding="utf-8",
        )
    return result
