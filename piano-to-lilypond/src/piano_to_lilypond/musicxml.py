from __future__ import annotations

import json
import re
from copy import deepcopy
from pathlib import Path

from music21 import chord, converter, note, stream

from piano_to_lilypond.config import MIDDLE_C_MIDI
from piano_to_lilypond.models import ChunkInfo


def _flatten_to_part(score: stream.Score) -> stream.Part:
    if len(score.parts) == 1:
        return score.parts[0]

    flat = stream.Part()
    for part in score.parts:
        for element in part.flatten().notesAndRests:
            flat.insert(element.offset, deepcopy(element))
    return flat


def _split_element_by_middle_c(element, middle_c: int):
    if isinstance(element, note.Note):
        pitch = element.pitch.midi
        if pitch >= middle_c:
            return deepcopy(element), None
        return None, deepcopy(element)

    if isinstance(element, chord.Chord):
        treble_pitches = [p for p in element.pitches if p.midi >= middle_c]
        bass_pitches = [p for p in element.pitches if p.midi < middle_c]

        treble_el = None
        bass_el = None

        if treble_pitches:
            treble_el = chord.Chord(treble_pitches)
            treble_el.duration = deepcopy(element.duration)
            treble_el.offset = element.offset
        if bass_pitches:
            bass_el = chord.Chord(bass_pitches)
            bass_el.duration = deepcopy(element.duration)
            bass_el.offset = element.offset

        return treble_el, bass_el

    return None, None


def split_hands(part: stream.Part, middle_c: int = MIDDLE_C_MIDI) -> tuple[stream.Part, stream.Part]:
    treble = stream.Part(id="Treble")
    treble.partName = "Treble"
    bass = stream.Part(id="Bass")
    bass.partName = "Bass"

    for element in part.flatten().notesAndRests:
        if isinstance(element, note.Rest):
            treble.insert(element.offset, deepcopy(element))
            bass.insert(element.offset, deepcopy(element))
            continue

        treble_el, bass_el = _split_element_by_middle_c(element, middle_c)
        if treble_el is not None:
            treble.insert(treble_el.offset, treble_el)
        if bass_el is not None:
            bass.insert(bass_el.offset, bass_el)

    return treble, bass


def _estimate_seconds_per_measure(part: stream.Part) -> float:
    tempo = 120.0
    for mark in part.recurse().getElementsByClass("MetronomeMark"):
        if mark.number:
            tempo = float(mark.number)
            break

    ts = part.getTimeSignatures()[0] if part.getTimeSignatures() else None
    beats = float(ts.numerator) if ts else 4.0
    beat_type = float(ts.denominator) if ts else 4.0
    quarter_beats = beats * (4.0 / beat_type)
    return (60.0 / tempo) * quarter_beats


def process_midi_to_musicxml(
    midi_path: Path,
    musicxml_path: Path,
    *,
    quantize_divisor: int = 16,
    middle_c: int = MIDDLE_C_MIDI,
) -> tuple[stream.Score, stream.Part, stream.Part]:
    score = converter.parse(str(midi_path), quantizePost=False)
    if not isinstance(score, stream.Score):
        part = score if isinstance(score, stream.Part) else stream.Part()
        wrapped = stream.Score()
        wrapped.insert(0, part)
        score = wrapped

    mono_part = _flatten_to_part(score)
    mono_part.quantize(
        quarterLengthDivisors=(4, quantize_divisor),
        processOffsets=True,
        processDurations=True,
        recurse=True,
        inPlace=True,
    )
    mono_part.makeMeasures(inPlace=True)
    mono_part.makeNotation(inPlace=True)

    treble, bass = split_hands(mono_part, middle_c=middle_c)

    for hand_part in (treble, bass):
        hand_part.makeMeasures(inPlace=True)
        hand_part.makeNotation(inPlace=True)

    out_score = stream.Score()
    out_score.insert(0, treble)
    out_score.insert(0, bass)

    musicxml_path.parent.mkdir(parents=True, exist_ok=True)
    out_score.write("musicxml", fp=str(musicxml_path))

    return out_score, treble, bass


def chunk_musicxml(
    treble: stream.Part,
    bass: stream.Part,
    chunks_dir: Path,
    *,
    chunk_seconds: float = 90.0,
) -> list[ChunkInfo]:
    chunks_dir.mkdir(parents=True, exist_ok=True)

    treble_measures = list(treble.getElementsByClass("Measure"))
    bass_measures = list(bass.getElementsByClass("Measure"))
    measure_count = max(len(treble_measures), len(bass_measures))

    if measure_count == 0:
        raise ValueError("No measures found after processing MIDI")

    seconds_per_measure = _estimate_seconds_per_measure(treble)
    measures_per_chunk = max(8, min(32, int(chunk_seconds / seconds_per_measure)))
    if measures_per_chunk < 1:
        measures_per_chunk = 8

    chunk_infos: list[ChunkInfo] = []
    chunk_index = 0
    measure_start = 1

    while measure_start <= measure_count:
        measure_end = min(measure_start + measures_per_chunk - 1, measure_count)
        chunk_index += 1

        treble_slice = treble.measures(measure_start, measure_end)
        bass_slice = bass.measures(measure_start, measure_end)

        chunk_score = stream.Score()
        chunk_score.insert(0, treble_slice)
        chunk_score.insert(0, bass_slice)

        musicxml_file = chunks_dir / f"chunk_{chunk_index:03d}.musicxml"
        chunk_score.write("musicxml", fp=str(musicxml_file))

        duration_est = (measure_end - measure_start + 1) * seconds_per_measure
        info = ChunkInfo(
            index=chunk_index,
            total=0,
            measure_start=measure_start,
            measure_end=measure_end,
            duration_est=duration_est,
            musicxml_path=musicxml_file,
        )
        chunk_infos.append(info)
        measure_start = measure_end + 1

    total = len(chunk_infos)
    for info in chunk_infos:
        info.total = total
        sidecar = info.musicxml_path.with_suffix(".json")
        sidecar.write_text(
            json.dumps(
                {
                    "index": info.index,
                    "total": info.total,
                    "measure_start": info.measure_start,
                    "measure_end": info.measure_end,
                    "duration_est": info.duration_est,
                },
                indent=2,
            )
            + "\n",
            encoding="utf-8",
        )

    return chunk_infos


def extract_variable_body(lilypond_text: str, variable_name: str) -> str | None:
    pattern = rf"{re.escape(variable_name)}\s*=\s*\{{"
    match = re.search(pattern, lilypond_text)
    if not match:
        return None

    start = match.end()
    depth = 1
    idx = start
    while idx < len(lilypond_text) and depth > 0:
        char = lilypond_text[idx]
        if char == "{":
            depth += 1
        elif char == "}":
            depth -= 1
        idx += 1

    if depth != 0:
        return None

    return lilypond_text[start : idx - 1].strip()
