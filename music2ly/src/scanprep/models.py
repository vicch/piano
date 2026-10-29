from __future__ import annotations

import shutil
from dataclasses import dataclass, field
from pathlib import Path

from music2ly.models import (
    IMAGE_EXTENSIONS,
    ORIGINAL_SUFFIX,
    find_image_files,
    is_original_backup,
    natural_sort_key,
    slugify_title,
)


@dataclass
class PageSource:
    """One sheet page discovered in a work directory.

    The raw scan lives either as a plain file (first run: it must be
    renamed to "<stem> (original)<ext>") or already as that backup
    (re-runs: ``backup_path`` is None and ``raw_path`` points at it).
    The processed page is always written as "<stem>.png" next to it.
    """

    stem: str
    raw_path: Path
    backup_path: Path | None  # rename target for first-run raws; None if already backed up
    processed_path: Path
    binary_path: Path
    strays: list[Path] = field(default_factory=list)  # duplicate files left untouched (warned)

    @property
    def settled(self) -> bool:
        """True when the raw is already backed up and processing is idempotent."""
        return self.backup_path is None


def _split_backup_stem(path: Path) -> str | None:
    """Backup stem "1 (original)" -> "1"; None for normal files."""
    if not is_original_backup(path):
        return None
    return path.stem[: -len(ORIGINAL_SUFFIX)].rstrip()


def discover_page_sources(work_dir: Path) -> list[PageSource]:
    """Pair raw scans with their processed outputs in a work directory.

    Every image directly in the directory participates: plain files are
    fresh raws (to be backed up), "(original)" files are raws of earlier
    runs, and "<stem>.png" next to a backup is a previous processed page.
    Duplicate top-level files sharing a stem are reported as strays.
    """
    files = find_image_files(work_dir, include_originals=True)
    backups: dict[str, list[Path]] = {}
    tops: dict[str, list[Path]] = {}
    for f in files:
        backup_stem = _split_backup_stem(f)
        if backup_stem is not None:
            backups.setdefault(backup_stem, []).append(f)
        else:
            tops.setdefault(f.stem, []).append(f)

    stems = sorted(set(backups) | set(tops), key=natural_sort_key)
    sources: list[PageSource] = []
    for stem in stems:
        raw_candidates = sorted(backups.get(stem, []), key=natural_sort_key)
        top_candidates = sorted(tops.get(stem, []), key=natural_sort_key)
        binary_dir = work_dir / "binary"
        processed_path = work_dir / f"{stem}.png"

        if raw_candidates:
            # Re-run: the backup is the canonical raw; the processed page is
            # expected next to it. Anything else is a leftover that image2ly
            # would sweep up.
            strays = [t for t in top_candidates if t != processed_path]
            sources.append(
                PageSource(
                    stem=stem,
                    raw_path=raw_candidates[0],
                    backup_path=None,
                    processed_path=processed_path,
                    binary_path=binary_dir / f"{stem}.png",
                    strays=strays,
                )
            )
        else:
            # Fresh raws: prefer a file already named like the processed page
            # (renaming it away never silently overwrites user data); the
            # rest become strays.
            primary = next((t for t in top_candidates if t == processed_path), top_candidates[0])
            sources.append(
                PageSource(
                    stem=stem,
                    raw_path=primary,
                    backup_path=work_dir / f"{primary.stem} {ORIGINAL_SUFFIX}{primary.suffix.lower()}",
                    processed_path=processed_path,
                    binary_path=binary_dir / f"{stem}.png",
                    strays=[t for t in top_candidates if t != primary],
                )
            )
    return sources


@dataclass
class ScanPaths:
    """Artifact layout for the scanprep pipeline inside a song directory.

    Processing is in place, mirroring image2ly's flow: raw scans are
    renamed "<stem> (original)<ext>", cleaned pages are written as
    "<stem>.png" with the original stem, so ``image2ly <dir>`` picks up
    exactly the cleaned pages in natural page order:

        <work_dir>/
        ├── 1.png                  # cleaned page (OMR-ready master)
        ├── 1 (original).jpg        # preserved raw scan
        ├── binary/1.png            # optional Sauvola binarization
        └── scanprep/
            ├── preview.png         # raw | clean | binary contact sheet
            └── scanprep.json       # parameters + per-page metrics report
    """

    work_dir: Path
    binary_dir: Path
    scanprep_dir: Path
    preview_path: Path
    report_path: Path

    @classmethod
    def for_work_dir(cls, work_dir: Path) -> ScanPaths:
        scanprep_dir = work_dir / "scanprep"
        return cls(
            work_dir=work_dir,
            binary_dir=work_dir / "binary",
            scanprep_dir=scanprep_dir,
            preview_path=scanprep_dir / "preview.png",
            report_path=scanprep_dir / "scanprep.json",
        )

    @staticmethod
    def _stem_settled(work_dir: Path, stem: str) -> bool:
        """True when a stem already has a processed page or a raw backup."""
        if not work_dir.is_dir():
            return False
        for f in work_dir.iterdir():
            if not f.is_file():
                continue
            if f.stem == stem and f.suffix.lower() == ".png":
                return True
            if f.stem == f"{stem} {ORIGINAL_SUFFIX}" and f.suffix.lower() in IMAGE_EXTENSIONS:
                return True
        return False

    @classmethod
    def from_target(
        cls,
        target: str | Path,
        *,
        title: str | None = None,
        output_root: Path = Path("output"),
    ) -> tuple[ScanPaths, str]:
        """Resolve a target directory/file/title into paths and a title.

        Mirrors image2ly target resolution:
          1. Existing directory -> process its images in place.
          2. Existing image file -> copy it into output/<title>/ (unless the
             stem is already settled there), then process in place.
          3. Bare name/title -> output/<name>/ (created if needed).
        """
        target_path = Path(target)

        # 1. Target is an existing directory: process in place
        if target_path.is_dir():
            work_dir = target_path.resolve()
            song_title = title or target_path.name

        # 2. Target is an existing single image file
        elif target_path.is_file() and target_path.suffix.lower() in IMAGE_EXTENSIONS:
            song_title = title or target_path.stem
            basename = slugify_title(song_title)
            if target_path.parent.name == basename or target_path.parent == (output_root / basename).resolve():
                work_dir = target_path.parent.resolve()
            else:
                work_dir = (output_root / basename).resolve()
                work_dir.mkdir(parents=True, exist_ok=True)
                # Copy the raw in like image2ly does, but never overwrite an
                # already-settled page (backup or processed output exists).
                dest = work_dir / target_path.name
                if not dest.exists() and not cls._stem_settled(work_dir, target_path.stem):
                    shutil.copy2(target_path, dest)

        # 3. Target is a name/title or sub-dir relative to output_root
        else:
            song_title = title or str(target)
            basename = slugify_title(song_title)
            work_dir = (output_root / basename).resolve()
            if not work_dir.exists() and (output_root / str(target)).resolve().exists():
                work_dir = (output_root / str(target)).resolve()

        paths = cls.for_work_dir(work_dir)
        return paths, song_title


@dataclass
class PageReport:
    """Per-page processing record serialized into scanprep.json."""

    index: int
    stem: str
    source: str
    width: int = 0
    height: int = 0
    skipped: bool = False
    skew_angle_deg: float = 0.0
    skew_lines: int = 0
    deskewed: bool = False
    staff_space_px: int = 0
    background_method: str = ""
    background_size_px: float = 0.0
    background_range: float = 0.0
    illumination_corrected: bool = False
    noise_pct: float = 0.0
    denoised: bool = False
    sauvola_window_px: int = 0
    sauvola_k: float = 0.0
    paper_before: dict = field(default_factory=dict)
    paper_after: dict = field(default_factory=dict)
    ink_ratio: float = 0.0
    dark_border: bool = False
    warnings: list[str] = field(default_factory=list)
    outputs: dict[str, str] = field(default_factory=dict)

    def to_dict(self) -> dict:
        return {
            "index": self.index,
            "stem": self.stem,
            "source": self.source,
            "width": self.width,
            "height": self.height,
            "skipped": self.skipped,
            "skew_angle_deg": round(self.skew_angle_deg, 3),
            "skew_lines": self.skew_lines,
            "deskewed": self.deskewed,
            "staff_space_px": self.staff_space_px,
            "background_method": self.background_method,
            "background_size_px": round(self.background_size_px, 1),
            "background_range": round(self.background_range, 1),
            "illumination_corrected": self.illumination_corrected,
            "noise_pct": round(self.noise_pct, 2),
            "denoised": self.denoised,
            "sauvola_window_px": self.sauvola_window_px,
            "sauvola_k": round(self.sauvola_k, 3),
            "paper_before": self.paper_before,
            "paper_after": self.paper_after,
            "ink_ratio": round(self.ink_ratio, 4),
            "dark_border": self.dark_border,
            "warnings": self.warnings,
            "outputs": self.outputs,
        }
