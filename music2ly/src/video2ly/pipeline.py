from __future__ import annotations

import sys
from pathlib import Path

from music2ly.config import Config
from video2ly.extract import extract_audio
from music2ly.lilypond import translate_all_chunks
from music2ly.models import PipelinePaths
from music2ly.musicxml import chunk_musicxml
from video2ly.quantize import quantize_midi
from video2ly.structure import midi_to_musicxml
from video2ly.transcribe import transcribe_audio

ALL_STEPS = ("extract", "transcribe", "quantize", "musicxml", "lilypond")


def _should_run(step: str, steps: set[str]) -> bool:
    return "all" in steps or step in steps


def _artifact_exists(path: Path) -> bool:
    return path.exists() and path.stat().st_size > 0


def run_pipeline(
    youtube_url: str,
    paths: PipelinePaths,
    config: Config,
    *,
    title: str,
    steps: set[str],
    resume: bool = False,
) -> PipelinePaths:
    if _should_run("extract", steps):
        if resume and _artifact_exists(paths.audio_path):
            print(f"Skipping extract (exists): {paths.audio_path}", file=sys.stderr)
        else:
            print("Step 1: Extracting audio from YouTube...", file=sys.stderr)
            extract_audio(youtube_url, paths.audio_path)
            print(f"  → {paths.audio_path}", file=sys.stderr)

    if _should_run("transcribe", steps):
        if not _artifact_exists(paths.audio_path):
            raise FileNotFoundError(f"Audio not found: {paths.audio_path}. Run extract first.")
        if resume and _artifact_exists(paths.midi_path):
            print(f"Skipping transcribe (exists): {paths.midi_path}", file=sys.stderr)
        else:
            print("Step 2: Transcribing audio to MIDI...", file=sys.stderr)
            meta = transcribe_audio(
                paths.audio_path,
                paths.midi_path,
                paths.transcription_meta_path,
                backend_name=config.transcription_backend,
                onset_threshold=config.onset_threshold,
                frame_threshold=config.frame_threshold,
                desustain_window=config.desustain_window,
            )
            print(
                f"  → {paths.midi_path} (backend={meta['backend']}, device={meta['device']}, "
                f"sensitivity={config.sensitivity}: "
                f"onset={config.onset_threshold}, frame={config.frame_threshold}, "
                f"desustain={config.desustain_window}st, "
                f"truncated={meta.get('notes_truncated', 0)})",
                file=sys.stderr,
            )

    if _should_run("quantize", steps):
        if not _artifact_exists(paths.midi_path):
            raise FileNotFoundError(f"MIDI not found: {paths.midi_path}. Run transcribe first.")
        if not _artifact_exists(paths.audio_path):
            raise FileNotFoundError(
                f"Audio not found: {paths.audio_path}. Quantize needs the original WAV for beat tracking."
            )
        if resume and _artifact_exists(paths.quantized_midi_path):
            print(f"Skipping quantize (exists): {paths.quantized_midi_path}", file=sys.stderr)
        else:
            print("Step 3: Detecting tempo and snapping MIDI to beat grid...", file=sys.stderr)
            result = quantize_midi(
                paths.audio_path,
                paths.midi_path,
                paths.quantized_midi_path,
                paths.quantize_meta_path,
                subdiv=config.quantize_subdiv,
                min_velocity=config.min_velocity,
                min_note_ms=config.min_note_ms,
            )
            print(
                f"  → {paths.quantized_midi_path} (bpm={result.bpm:.2f}, "
                f"beats={result.beats_detected}, notes={result.notes}, "
                f"merged={result.notes_merged}, dropped={result.notes_dropped})",
                file=sys.stderr,
            )

    chunks: list = []
    if _should_run("musicxml", steps):
        midi_source = (
            paths.quantized_midi_path
            if _artifact_exists(paths.quantized_midi_path)
            else paths.midi_path
        )
        if not _artifact_exists(midi_source):
            raise FileNotFoundError(
                f"MIDI not found: {midi_source}. Run transcribe (and quantize) first."
            )
        if resume and _artifact_exists(paths.musicxml_path) and paths.chunks_dir.exists():
            existing = sorted(paths.chunks_dir.glob("chunk_*.musicxml"))
            if existing:
                print(f"Skipping musicxml (exists): {paths.musicxml_path}", file=sys.stderr)
                from music2ly.models import ChunkInfo
                import json

                for xml_path in existing:
                    sidecar = xml_path.with_suffix(".json")
                    data = json.loads(sidecar.read_text(encoding="utf-8"))
                    chunks.append(
                        ChunkInfo(
                            index=data["index"],
                            total=data["total"],
                            measure_start=data["measure_start"],
                            measure_end=data["measure_end"],
                            duration_est=data["duration_est"],
                            musicxml_path=xml_path,
                        )
                    )
        if not chunks:
            print("Step 4: Structuring MIDI → MusicXML (MuseScore)...", file=sys.stderr)
            result = midi_to_musicxml(
                midi_source,
                paths.musicxml_path,
                mscore_bin=config.mscore_bin,
            )
            chunks = chunk_musicxml(
                result.treble,
                result.bass,
                paths.chunks_dir,
                chunk_seconds=config.chunk_seconds,
            )
            print(
                f"  → {paths.musicxml_path} "
                f"({result.measure_count} measures, {len(chunks)} chunk(s))",
                file=sys.stderr,
            )

    if _should_run("lilypond", steps):
        if not chunks:
            if paths.chunks_dir.exists():
                from music2ly.models import ChunkInfo
                import json

                for xml_path in sorted(paths.chunks_dir.glob("chunk_*.musicxml")):
                    sidecar = xml_path.with_suffix(".json")
                    data = json.loads(sidecar.read_text(encoding="utf-8"))
                    chunks.append(
                        ChunkInfo(
                            index=data["index"],
                            total=data["total"],
                            measure_start=data["measure_start"],
                            measure_end=data["measure_end"],
                            duration_est=data["duration_est"],
                            musicxml_path=xml_path,
                        )
                    )
        if not chunks:
            raise FileNotFoundError("No MusicXML chunks found. Run musicxml step first.")

        if resume and _artifact_exists(paths.output_path):
            print(f"Skipping lilypond (exists): {paths.output_path}", file=sys.stderr)
        else:
            print(f"Step 5: Translating {len(chunks)} chunk(s) to LilyPond...", file=sys.stderr)
            translate_all_chunks(
                chunks,
                config,
                paths.lilypond_chunks_dir,
                paths.output_path,
                title=title,
                youtube_url=youtube_url,
            )
            print(f"  → {paths.output_path}", file=sys.stderr)

    return paths
