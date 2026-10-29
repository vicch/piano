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


ORIGINAL_DIR = "original"  # subdirectory holding preserved raw scans, as-is


@dataclass
class PageSource:
    """One sheet page discovered in a work directory.

    The raw scan lives either as a plain file in the work directory
    (first run: it is moved as-is into the "original/" subdirectory) or
    already inside "original/" (re-runs: ``backup_path`` is None and
    ``raw_path`` points there). Legacy "<stem> (original)<ext>" backups
    from older scanprep runs are still recognized as raws and migrate
    into "original/" under their original name. The processed page is
    always written as "<stem>.png" at the top level.
    """

    stem: str
    raw_path: Path
    backup_path: Path | None  # move target for first-run raws; None if already preserved
    processed_path: Path
    strays: list[Path] = field(default_factory=list)  # duplicate files left untouched (warned)

    @property
    def settled(self) -> bool:
        """True when the raw is already preserved and processing is idempotent."""
        return self.backup_path is None


def _split_backup_stem(path: Path) -> str | None:
    """Backup stem "1 (original)" -> "1"; None for normal files."""
    if not is_original_backup(path):
        return None
    return path.stem[: -len(ORIGINAL_SUFFIX)].rstrip()


def discover_page_sources(work_dir: Path) -> list[PageSource]:
    """Pair raw scans with their processed outputs in a work directory.

    Preserved raws live in the "original/" subdirectory under their
    original filenames. Plain top-level images are fresh raws (to be
    moved into "original/"); legacy top-level "<stem> (original)<ext>"
    backups from older runs are raws too (they migrate into "original/"
    under their original name). A re-dropped raw whose name matches a
    preserved raw replaces it (the move overwrites the old raw).
    "<stem>.png" at the top level is the processed page. Duplicate
    top-level files sharing a stem are reported as strays.
    """
    original_dir = work_dir / ORIGINAL_DIR
    preserved: dict[str, list[Path]] = {}
    for f in find_image_files(original_dir):
        preserved.setdefault(f.stem, []).append(f)

    files = find_image_files(work_dir, include_originals=True)
    legacy: dict[str, list[Path]] = {}
    tops: dict[str, list[Path]] = {}
    for f in files:
        backup_stem = _split_backup_stem(f)
        if backup_stem is not None:
            legacy.setdefault(backup_stem, []).append(f)
        else:
            tops.setdefault(f.stem, []).append(f)

    stems = sorted(set(preserved) | set(legacy) | set(tops), key=natural_sort_key)
    sources: list[PageSource] = []
    for stem in stems:
        processed_path = work_dir / f"{stem}.png"
        preserved_raws = sorted(preserved.get(stem, []), key=natural_sort_key)
        legacy_raws = sorted(legacy.get(stem, []), key=natural_sort_key)
        top_candidates = sorted(tops.get(stem, []), key=natural_sort_key)

        if preserved_raws:
            # A re-dropped raw carrying the same name as the preserved one
            # replaces it (the move into original/ overwrites the old raw).
            # A file named like the processed page is that page, never a
            # re-dropped raw, so idempotent re-runs don't clobber raws.
            redrop = next(
                (t for t in top_candidates if t.name == preserved_raws[0].name and t != processed_path),
                None,
            )
            if redrop is not None:
                sources.append(
                    PageSource(
                        stem=stem,
                        raw_path=redrop,
                        backup_path=original_dir / redrop.name,
                        processed_path=processed_path,
                        strays=[t for t in top_candidates if t not in (redrop, processed_path)]
                        + legacy_raws,
                    )
                )
            else:
                # Re-run: the preserved raw is canonical. Anything else at
                # the top level is a leftover that image2ly would sweep up.
                sources.append(
                    PageSource(
                        stem=stem,
                        raw_path=preserved_raws[0],
                        backup_path=None,
                        processed_path=processed_path,
                        strays=[t for t in top_candidates if t != processed_path] + legacy_raws,
                    )
                )
        elif legacy_raws:
            # Legacy "<stem> (original)<ext>" backup migrates into original/
            # under its original name.
            sources.append(
                PageSource(
                    stem=stem,
                    raw_path=legacy_raws[0],
                    backup_path=original_dir / f"{stem}{legacy_raws[0].suffix}",
                    processed_path=processed_path,
                    strays=[t for t in top_candidates if t != processed_path] + legacy_raws[1:],
                )
            )
        else:
            # Fresh raws: prefer a file already named like the processed page
            # (moving it away never silently overwrites user data); the
            # rest become strays.
            primary = next((t for t in top_candidates if t == processed_path), top_candidates[0])
            sources.append(
                PageSource(
                    stem=stem,
                    raw_path=primary,
                    backup_path=original_dir / primary.name,
                    processed_path=processed_path,
                    strays=[t for t in top_candidates if t != primary],
                )
            )
    return sources


@dataclass
class ScanPaths:
    """Artifact layout for the scanprep pipeline inside a song directory.

    Processing is in place, mirroring image2ly's flow: raw scans are
    moved as-is into the "original/" subdirectory (overwriting any
    same-named file there), cleaned pages are written as "<stem>.png"
    with the original stem, so ``image2ly <dir>`` picks up exactly the
    cleaned pages in natural page order:

        <work_dir>/
        ├── 1.png                  # cleaned page (restored, smooth anti-aliased)
        ├── original/1.jpg          # preserved raw scan, original filename
        └── scanprep/
            ├── preview.png         # raw | clean contact sheet
            └── scanprep.json       # parameters + per-page metrics report
    """

    work_dir: Path
    original_dir: Path
    scanprep_dir: Path
    preview_path: Path
    report_path: Path

    @classmethod
    def for_work_dir(cls, work_dir: Path) -> ScanPaths:
        scanprep_dir = work_dir / "scanprep"
        return cls(
            work_dir=work_dir,
            original_dir=work_dir / ORIGINAL_DIR,
            scanprep_dir=scanprep_dir,
            preview_path=scanprep_dir / "preview.png",
            report_path=scanprep_dir / "scanprep.json",
        )

    @staticmethod
    def _stem_settled(work_dir: Path, stem: str) -> bool:
        """True when a stem already has a processed page or a preserved raw."""
        if not work_dir.is_dir():
            return False
        processed = work_dir / f"{stem}.png"
        if processed.is_file():
            return True
        original_dir = work_dir / ORIGINAL_DIR
        if original_dir.is_dir():
            for f in original_dir.iterdir():
                if f.is_file() and f.stem == stem and f.suffix.lower() in IMAGE_EXTENSIONS:
                    return True
        for f in work_dir.iterdir():
            if not f.is_file():
                continue
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
    contrast_applied: bool = False
    noise_pct: float = 0.0
    denoised: bool = False
    sharpened: bool = False
    sauvola_window_px: int = 0
    sauvola_k: float = 0.0
    specks_removed: int = 0
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
            "contrast_applied": self.contrast_applied,
            "noise_pct": round(self.noise_pct, 2),
            "denoised": self.denoised,
            "sharpened": self.sharpened,
            "sauvola_window_px": self.sauvola_window_px,
            "sauvola_k": round(self.sauvola_k, 3),
            "specks_removed": self.specks_removed,
            "paper_before": self.paper_before,
            "paper_after": self.paper_after,
            "ink_ratio": round(self.ink_ratio, 4),
            "dark_border": self.dark_border,
            "warnings": self.warnings,
            "outputs": self.outputs,
        }
