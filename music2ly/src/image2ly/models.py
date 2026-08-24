from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path

from music2ly.models import slugify_title

IMAGE_EXTENSIONS = {".png", ".jpg", ".jpeg", ".webp", ".bmp", ".tiff", ".tif"}


def natural_sort_key(p: Path | str) -> list[int | str]:
    """Natural sort key for ordering file names containing numbers (e.g. page 1, 2, 10)."""
    s = p.name if isinstance(p, Path) else str(p)
    return [int(text) if text.isdigit() else text.lower() for text in re.split(r"(\d+)", s)]


def find_image_files(directory: Path) -> list[Path]:
    """Find all image files directly in a directory in natural sort order."""
    if not directory.exists() or not directory.is_dir():
        return []
    images = [
        f for f in directory.iterdir()
        if f.is_file() and f.suffix.lower() in IMAGE_EXTENSIONS
    ]
    return sorted(images, key=natural_sort_key)


@dataclass
class ImagePaths:
    """Artifact layout for the image2ly pipeline under a target directory (e.g. output/<title>/)."""

    work_dir: Path
    source_images: list[Path]
    musicxml_path: Path
    chunks_dir: Path
    lilypond_chunks_dir: Path
    output_path: Path

    @property
    def source_image(self) -> Path:
        """Single image alias for backward compatibility."""
        if self.source_images:
            return self.source_images[0]
        return self.work_dir / "source.png"

    @property
    def page_musicxml_paths(self) -> list[Path]:
        """Paths to per-page recognized MusicXML files."""
        if len(self.source_images) <= 1:
            return [self.musicxml_path]
        return [
            self.work_dir / f"recognized_{i + 1:03d}.musicxml"
            for i in range(len(self.source_images))
        ]

    @classmethod
    def resolve_target(
        cls,
        target: str | Path,
        *,
        title: str | None = None,
        output_root: Path = Path("output"),
    ) -> tuple[Path, str, list[Path]]:
        """Resolve a target directory or file, song title, and source images."""
        target_path = Path(target)

        # 1. Target is an existing directory
        if target_path.is_dir():
            work_dir = target_path.resolve()
            song_title = title or target_path.name
            images = find_image_files(work_dir)
            return work_dir, song_title, images

        # 2. Target is an existing single image file
        if target_path.is_file() and target_path.suffix.lower() in IMAGE_EXTENSIONS:
            song_title = title or target_path.stem
            basename = slugify_title(song_title)
            # If the file is already in output_root/<basename>, use that as work_dir
            if target_path.parent.name == basename or target_path.parent == (output_root / basename).resolve():
                work_dir = target_path.parent.resolve()
                images = find_image_files(work_dir) or [target_path.resolve()]
            else:
                work_dir = (output_root / basename).resolve()
                work_dir.mkdir(parents=True, exist_ok=True)
                images = [target_path.resolve()]
            return work_dir, song_title, images

        # 3. Target is a name/title or sub-dir relative to output_root
        song_title = title or str(target)
        basename = slugify_title(song_title)
        sub_dir = (output_root / basename).resolve()
        if not sub_dir.exists() and (output_root / str(target)).resolve().exists():
            sub_dir = (output_root / str(target)).resolve()

        sub_dir.mkdir(parents=True, exist_ok=True)
        images = find_image_files(sub_dir)
        return sub_dir, song_title, images

    @classmethod
    def from_target(
        cls,
        target: str | Path,
        *,
        title: str | None = None,
        output_root: Path = Path("output"),
    ) -> tuple["ImagePaths", str]:
        work_dir, song_title, images = cls.resolve_target(
            target, title=title, output_root=output_root
        )
        basename = slugify_title(song_title)
        paths = cls(
            work_dir=work_dir,
            source_images=images,
            musicxml_path=work_dir / "recognized.musicxml",
            chunks_dir=work_dir / "chunks",
            lilypond_chunks_dir=work_dir / "lilypond_chunks",
            output_path=work_dir / f"{basename}.ly",
        )
        return paths, song_title

    @classmethod
    def from_title(
        cls,
        title: str,
        image_path: Path | None = None,
        *,
        output_root: Path = Path("output"),
    ) -> "ImagePaths":
        target = image_path if image_path is not None else title
        paths, _ = cls.from_target(target, title=title, output_root=output_root)
        return paths

    @classmethod
    def from_dir(
        cls,
        directory: Path,
        *,
        title: str | None = None,
    ) -> "ImagePaths":
        paths, _ = cls.from_target(directory, title=title)
        return paths
