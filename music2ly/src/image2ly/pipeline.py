from __future__ import annotations

import json
import shutil
import sys
from pathlib import Path

from music2ly.config import Config
from music2ly.lilypond import translate_all_chunks
from music2ly.models import ChunkInfo
from music2ly.musicxml import chunk_musicxml, load_grand_staff

from image2ly.models import ImagePaths
from image2ly.omr import recognize

ALL_STEPS = ("recognize", "musicxml", "lilypond")


def _should_run(step: str, steps: set[str]) -> bool:
    return "all" in steps or step in steps


def _artifact_exists(path: Path) -> bool:
    return path.exists() and path.stat().st_size > 0


def _load_chunks(chunks_dir: Path) -> list[ChunkInfo]:
    chunks: list[ChunkInfo] = []
    for xml_path in sorted(chunks_dir.glob("chunk_*.musicxml")):
        data = json.loads(xml_path.with_suffix(".json").read_text(encoding="utf-8"))
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
    return chunks


def run_pipeline(
    image_input: Path,
    paths: ImagePaths,
    config: Config,
    *,
    title: str,
    steps: set[str],
    resume: bool = False,
    omr_backend: str = "homr",
) -> ImagePaths:
    if _should_run("recognize", steps):
        if resume and _artifact_exists(paths.musicxml_path):
            print(f"Skipping recognize (exists): {paths.musicxml_path}", file=sys.stderr)
        else:
            if not image_input.exists():
                raise FileNotFoundError(f"Image not found: {image_input}")
            # Keep a stable copy of the input so later --resume steps are self-contained.
            if image_input.resolve() != paths.source_image.resolve():
                shutil.copy2(image_input, paths.source_image)
            print(f"Step 1: Recognizing sheet image ({omr_backend})...", file=sys.stderr)
            recognize(paths.source_image, paths.musicxml_path, backend=omr_backend)
            print(f"  → {paths.musicxml_path}", file=sys.stderr)

    chunks: list[ChunkInfo] = []
    if _should_run("musicxml", steps):
        if not _artifact_exists(paths.musicxml_path):
            raise FileNotFoundError(
                f"MusicXML not found: {paths.musicxml_path}. Run recognize first."
            )
        if resume and paths.chunks_dir.exists():
            chunks = _load_chunks(paths.chunks_dir)
            if chunks:
                print(f"Skipping musicxml (exists): {len(chunks)} chunk(s)", file=sys.stderr)
        if not chunks:
            print("Step 2: Parsing MusicXML and chunking...", file=sys.stderr)
            treble, bass, measure_count = load_grand_staff(paths.musicxml_path)
            chunks = chunk_musicxml(
                treble,
                bass,
                paths.chunks_dir,
                chunk_seconds=config.chunk_seconds,
                make_notation=False,
            )
            print(
                f"  → {measure_count} measures, {len(chunks)} chunk(s)",
                file=sys.stderr,
            )

    if _should_run("lilypond", steps):
        if not chunks:
            chunks = _load_chunks(paths.chunks_dir)
        if not chunks:
            raise FileNotFoundError("No MusicXML chunks found. Run musicxml step first.")
        if resume and _artifact_exists(paths.output_path):
            print(f"Skipping lilypond (exists): {paths.output_path}", file=sys.stderr)
        else:
            print(f"Step 3: Translating {len(chunks)} chunk(s) to LilyPond...", file=sys.stderr)
            translate_all_chunks(
                chunks,
                config,
                paths.lilypond_chunks_dir,
                paths.output_path,
                title=title,
                source=str(paths.source_image),
                sequence=f"Sheet image: {paths.source_image.name}",
            )
            print(f"  → {paths.output_path}", file=sys.stderr)

    return paths
