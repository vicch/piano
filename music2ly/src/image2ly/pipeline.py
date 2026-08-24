from __future__ import annotations

import json
import shutil
import sys
from pathlib import Path

from music21 import stream

from music2ly.config import Config
from music2ly.lilypond import translate_all_chunks
from music2ly.models import ChunkInfo
from music2ly.musicxml import chunk_musicxml, load_grand_staff, load_multi_grand_staff

from image2ly.models import IMAGE_EXTENSIONS, ImagePaths, find_image_files
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
    image_or_paths: Path | ImagePaths,
    paths_or_config: ImagePaths | Config | None = None,
    config_or_none: Config | None = None,
    *,
    title: str = "",
    steps: set[str] | None = None,
    resume: bool = False,
    omr_backend: str = "homr",
) -> ImagePaths:
    """Run the image2ly pipeline.

    Supports both:
      - run_pipeline(paths, config, title=title, ...)
      - run_pipeline(image_input, paths, config, title=title, ...)
    """
    if steps is None:
        steps = {"all"}

    if isinstance(image_or_paths, ImagePaths):
        paths = image_or_paths
        config = (
            paths_or_config
            if isinstance(paths_or_config, Config)
            else (config_or_none or Config.load())
        )
        song_title = title or paths.work_dir.name
    elif isinstance(paths_or_config, ImagePaths):
        paths = paths_or_config
        config = config_or_none if isinstance(config_or_none, Config) else Config.load()
        song_title = title or paths.work_dir.name
    else:
        paths, resolved_title = ImagePaths.from_target(image_or_paths, title=title or None)
        config = (
            paths_or_config
            if isinstance(paths_or_config, Config)
            else (config_or_none or Config.load())
        )
        song_title = resolved_title

    if _should_run("recognize", steps):
        # Refresh images from work_dir if empty
        if not paths.source_images:
            paths.source_images = find_image_files(paths.work_dir)

        if not paths.source_images and not (resume and _artifact_exists(paths.musicxml_path)):
            raise FileNotFoundError(
                f"No sheet music images found in {paths.work_dir}. "
                f"Supported formats: {', '.join(sorted(IMAGE_EXTENSIONS))}"
            )

        # Ensure any source image outside work_dir is copied into work_dir
        for idx, img in enumerate(paths.source_images):
            if not img.exists():
                raise FileNotFoundError(f"Image not found: {img}")
            if img.parent.resolve() != paths.work_dir.resolve():
                dest = paths.work_dir / img.name
                if not dest.exists():
                    shutil.copy2(img, dest)
                paths.source_images[idx] = dest

        # Recognize each page image
        total_pages = len(paths.source_images)
        for idx, (img_path, out_xml) in enumerate(
            zip(paths.source_images, paths.page_musicxml_paths)
        ):
            if resume and _artifact_exists(out_xml):
                print(
                    f"Skipping recognize for page {idx + 1}/{total_pages} (exists): {out_xml.name}",
                    file=sys.stderr,
                )
            else:
                page_label = f"page {idx + 1}/{total_pages} " if total_pages > 1 else ""
                print(
                    f"Step 1: Recognizing sheet image {page_label}({img_path.name}) with {omr_backend}...",
                    file=sys.stderr,
                )
                recognize(img_path, out_xml, backend=omr_backend)
                print(f"  → {out_xml.name}", file=sys.stderr)

        # Merge page MusicXMLs into unified recognized.musicxml
        if len(paths.page_musicxml_paths) > 1:
            if not (resume and _artifact_exists(paths.musicxml_path)):
                print(
                    f"  Merging {len(paths.page_musicxml_paths)} page MusicXML files into {paths.musicxml_path.name}...",
                    file=sys.stderr,
                )
                treble, bass, measure_count = load_multi_grand_staff(paths.page_musicxml_paths)
                merged_score = stream.Score()
                merged_score.insert(0, treble)
                merged_score.insert(0, bass)
                merged_score.write("musicxml", fp=str(paths.musicxml_path), makeNotation=False)
                print(
                    f"  → Merged {total_pages} pages into {paths.musicxml_path.name} ({measure_count} measures)",
                    file=sys.stderr,
                )
        elif len(paths.page_musicxml_paths) == 1:
            single_xml = paths.page_musicxml_paths[0]
            if single_xml.resolve() != paths.musicxml_path.resolve() and _artifact_exists(single_xml):
                shutil.copy2(single_xml, paths.musicxml_path)

    chunks: list[ChunkInfo] = []
    if _should_run("musicxml", steps):
        has_xml = _artifact_exists(paths.musicxml_path) or (
            paths.page_musicxml_paths
            and all(_artifact_exists(p) for p in paths.page_musicxml_paths)
        )
        if not has_xml:
            raise FileNotFoundError(
                f"MusicXML not found: {paths.musicxml_path}. Run recognize first."
            )

        if resume and paths.chunks_dir.exists():
            chunks = _load_chunks(paths.chunks_dir)
            if chunks:
                print(f"Skipping musicxml (exists): {len(chunks)} chunk(s)", file=sys.stderr)

        if not chunks:
            print("Step 2: Parsing MusicXML and chunking...", file=sys.stderr)
            if (
                len(paths.page_musicxml_paths) > 1
                and all(_artifact_exists(p) for p in paths.page_musicxml_paths)
            ):
                treble, bass, measure_count = load_multi_grand_staff(paths.page_musicxml_paths)
            else:
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
            if len(paths.source_images) == 1:
                sequence = f"Sheet image: {paths.source_images[0].name}"
            elif len(paths.source_images) > 1:
                sequence = f"Sheet images: {len(paths.source_images)} pages"
            else:
                sequence = f"Sheet: {song_title}"

            translate_all_chunks(
                chunks,
                config,
                paths.lilypond_chunks_dir,
                paths.output_path,
                title=song_title,
                source=str(paths.work_dir),
                sequence=sequence,
            )
            print(f"  → {paths.output_path}", file=sys.stderr)

    return paths
