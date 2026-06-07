from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from music2ly.models import slugify_title


@dataclass
class ImagePaths:
    """Artifact layout for the image2ly pipeline under output/<title>/."""

    work_dir: Path
    source_image: Path
    musicxml_path: Path
    chunks_dir: Path
    lilypond_chunks_dir: Path
    output_path: Path

    @classmethod
    def from_title(
        cls,
        title: str,
        image_path: Path,
        *,
        output_root: Path = Path("output"),
    ) -> "ImagePaths":
        basename = slugify_title(title)
        project_dir = output_root / basename
        project_dir.mkdir(parents=True, exist_ok=True)
        # Absolute so artifacts resolve correctly when subprocesses (OMR engines)
        # run with a different working directory.
        project_dir = project_dir.resolve()
        suffix = image_path.suffix.lower() or ".png"
        return cls(
            work_dir=project_dir,
            source_image=project_dir / f"source{suffix}",
            musicxml_path=project_dir / "recognized.musicxml",
            chunks_dir=project_dir / "chunks",
            lilypond_chunks_dir=project_dir / "lilypond_chunks",
            output_path=project_dir / f"{basename}.ly",
        )
