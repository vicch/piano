from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path


@dataclass
class ChunkInfo:
    index: int
    total: int
    measure_start: int
    measure_end: int
    duration_est: float
    musicxml_path: Path


def slugify_title(title: str) -> str:
    """Filesystem-safe directory and .ly basename from a human title."""
    name = title.strip()
    if not name:
        raise ValueError("Title must not be empty")
    name = re.sub(r"[/\\:\0]", "-", name)
    name = re.sub(r'[<>:"|?*]', "", name)
    name = re.sub(r"\s+", "-", name)
    name = name.strip("-._")
    if not name:
        raise ValueError("Title must contain at least one usable character")
    return name


@dataclass
class PipelinePaths:
    work_dir: Path
    audio_path: Path
    midi_path: Path
    musicxml_path: Path
    chunks_dir: Path
    lilypond_chunks_dir: Path
    output_path: Path
    transcription_meta_path: Path

    @classmethod
    def from_title(
        cls,
        title: str,
        *,
        output_root: Path = Path("output"),
    ) -> PipelinePaths:
        basename = slugify_title(title)
        project_dir = output_root / basename
        return cls.from_project_dir(project_dir, project_dir / f"{basename}.ly")

    @classmethod
    def from_project_dir(cls, project_dir: Path, output_path: Path) -> PipelinePaths:
        project_dir.mkdir(parents=True, exist_ok=True)
        chunks_dir = project_dir / "chunks"
        lilypond_chunks_dir = project_dir / "lilypond_chunks"
        return cls(
            work_dir=project_dir,
            audio_path=project_dir / "audio.wav",
            midi_path=project_dir / "transcription.mid",
            musicxml_path=project_dir / "structured.musicxml",
            chunks_dir=chunks_dir,
            lilypond_chunks_dir=lilypond_chunks_dir,
            output_path=output_path,
            transcription_meta_path=project_dir / "transcription.meta.json",
        )

    @classmethod
    def from_work_dir(cls, work_dir: Path, output_path: Path) -> PipelinePaths:
        """Backward-compatible alias for tests and custom layouts."""
        return cls.from_project_dir(work_dir, output_path)
