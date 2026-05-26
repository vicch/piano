from __future__ import annotations

import sys
from pathlib import Path

from piano_to_lilypond.config import Config
from piano_to_lilypond.extract import extract_audio
from piano_to_lilypond.lilypond import translate_all_chunks
from piano_to_lilypond.models import PipelinePaths
from piano_to_lilypond.musicxml import chunk_musicxml, process_midi_to_musicxml
from piano_to_lilypond.transcribe import transcribe_audio

ALL_STEPS = ("extract", "transcribe", "musicxml", "lilypond")


def _should_run(step: str, steps: set[str]) -> bool:
    return "all" in steps or step in steps


def _artifact_exists(path: Path) -> bool:
    return path.exists() and path.stat().st_size > 0


def run_pipeline(
    youtube_url: str,
    paths: PipelinePaths,
    config: Config,
    *,
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
            )
            print(
                f"  → {paths.midi_path} (backend={meta['backend']}, device={meta['device']})",
                file=sys.stderr,
            )

    chunks: list = []
    if _should_run("musicxml", steps):
        if not _artifact_exists(paths.midi_path):
            raise FileNotFoundError(f"MIDI not found: {paths.midi_path}. Run transcribe first.")
        if resume and _artifact_exists(paths.musicxml_path) and paths.chunks_dir.exists():
            existing = sorted(paths.chunks_dir.glob("chunk_*.musicxml"))
            if existing:
                print(f"Skipping musicxml (exists): {paths.musicxml_path}", file=sys.stderr)
                from piano_to_lilypond.models import ChunkInfo
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
            print("Step 3: Structuring MIDI → MusicXML...", file=sys.stderr)
            _, treble, bass = process_midi_to_musicxml(
                paths.midi_path,
                paths.musicxml_path,
                quantize_divisor=config.quantize_divisor,
                middle_c=config.middle_c_midi,
            )
            chunks = chunk_musicxml(
                treble,
                bass,
                paths.chunks_dir,
                chunk_seconds=config.chunk_seconds,
            )
            print(f"  → {paths.musicxml_path} ({len(chunks)} chunk(s))", file=sys.stderr)

    if _should_run("lilypond", steps):
        if not chunks:
            if paths.chunks_dir.exists():
                from piano_to_lilypond.models import ChunkInfo
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
            print(f"Step 4: Translating {len(chunks)} chunk(s) to LilyPond...", file=sys.stderr)
            translate_all_chunks(chunks, config, paths.lilypond_chunks_dir, paths.output_path)
            print(f"  → {paths.output_path}", file=sys.stderr)

    return paths
