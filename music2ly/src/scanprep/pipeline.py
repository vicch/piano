"""scanprep pipeline: in-place raw scans -> cleaned pages + QC report.

For every image directly in the target directory, the raw scan is moved
as-is into the "original/" subdirectory (overwriting any same-named file
there) and the cleaned page is written as "<stem>.png" with the original
stem, so image2ly picks up exactly the cleaned pages (its file finder
only lists top-level images). The pipeline adapts per page: it measures
the input first (skew, staff spacing, background unevenness, noise) and
then decides which corrections to apply. Effective decisions are
recorded in scanprep.json so results are auditable and reproducible.
"""

from __future__ import annotations

import json
import os
import sys
from dataclasses import dataclass, replace
from pathlib import Path

import numpy as np

from music2ly.models import IMAGE_EXTENSIONS

from scanprep import __version__
from scanprep import enhance
from scanprep.models import PageReport, PageSource, ScanPaths, discover_page_sources

PAPER_UNEVENNESS_WARN = 8.0   # paper-after std above this: residual shading
INK_RATIO_MIN = 0.003         # binarization sanity bounds (fraction of page)
INK_RATIO_MAX = 0.25


@dataclass
class PrepOptions:
    """Effective processing knobs. None means "decide from measurement"."""

    deskew: bool = True
    max_skew: float = 3.0
    background_method: str = "morph"  # "morph" | "gaussian"
    background_scale: float = 4.0
    paper_target: int = enhance.PAPER_TARGET
    contrast: bool = True
    whiten: bool = True
    sharpen: bool = True
    despeckle: bool = True
    binary_output: bool = False       # strict 1-bit page; default keeps anti-aliased edges
    sauvola_window_scale: float = 5.0
    sauvola_k: float | None = None       # None: derive from measured noise
    denoise: bool | None = None           # None: derive from measured noise
    preview: bool = True
    resume: bool = False

    def to_dict(self) -> dict:
        return {
            "deskew": self.deskew,
            "max_skew": self.max_skew,
            "background_method": self.background_method,
            "background_scale": self.background_scale,
            "paper_target": self.paper_target,
            "contrast": self.contrast,
            "whiten": self.whiten,
            "sharpen": self.sharpen,
            "despeckle": self.despeckle,
            "binary_output": self.binary_output,
            "sauvola_window_scale": self.sauvola_window_scale,
            "sauvola_k": self.sauvola_k,
            "denoise": self.denoise,
            "preview": self.preview,
            "resume": self.resume,
        }


@dataclass
class PageResult:
    clean: np.ndarray
    report: PageReport


def process_page(
    src: Path,
    index: int,
    stem: str,
    options: PrepOptions,
) -> PageResult:
    """Run all adaptive enhancement stages for one raw page image."""
    original = enhance.load_grayscale(src)
    report = PageReport(index=index, stem=stem, source=str(src))
    report.height, report.width = original.shape

    gray = original

    # 1. Deskew from long-line evidence only; never rotate blindly.
    if options.deskew:
        angle, lines = enhance.estimate_skew(gray, max_angle=options.max_skew)
        report.skew_angle_deg, report.skew_lines = angle, lines
        if lines < enhance.SKEW_MIN_LINES:
            report.warnings.append(
                f"fewer than {enhance.SKEW_MIN_LINES} long horizontal lines found; "
                "skew estimate not trusted, deskew skipped"
            )
        elif abs(angle) >= enhance.MIN_DESKEW_ANGLE:
            gray = enhance.deskew(gray, angle)
            report.deskewed = True

    # 2. Staff metrics drive every later kernel size.
    staff_space, _peaks = enhance.estimate_staff_space(gray)
    report.staff_space_px = staff_space
    if staff_space < enhance.MIN_STAFF_SPACE:
        report.warnings.append(
            f"staff spacing ~{staff_space}px is very small; "
            "low-resolution scan, consider rescanning at higher DPI"
        )

    # 3. Illumination: divide out the paper background only when it is
    #    measurably uneven; flat pages go straight to levels.
    background = enhance.estimate_background(
        gray, staff_space, method=options.background_method, scale=options.background_scale
    )
    report.background_method = options.background_method
    report.background_size_px = (
        options.background_scale * staff_space
        if options.background_method == "gaussian"
        else float(max(int(2 * options.background_scale * staff_space) | 1, 9))
    )
    report.background_range = enhance.background_range(background)
    if enhance.needs_illumination(background):
        gray = enhance.correct_illumination(
            gray, background, paper_target=options.paper_target
        )
        report.illumination_corrected = True

    # 4. Levels normalize the paper to white across heterogeneous inputs,
    #    scaling ink by the same gain so faint notation is never clipped.
    gray = enhance.apply_levels(gray)

    # 5. Contrast: aggressively pull ink toward black and paper toward white
    #    (strengths are constants in enhance.py, tweakable to taste).
    if options.contrast:
        gray = enhance.apply_contrast(
            gray,
            ink_target=enhance.CONTRAST_INK_TARGET,
            gamma=enhance.CONTRAST_GAMMA,
        )
        report.contrast_applied = True

    # 6. Denoise only when the page is measurably noisy.
    noise = enhance.measure_noise(gray)
    report.noise_pct = noise
    denoise_on = options.denoise if options.denoise is not None else (
        noise >= enhance.DENOISE_NOISE_THRESHOLD
    )
    if denoise_on:
        gray = enhance.denoise(gray)
    report.denoised = bool(denoise_on)

    # 7. Smooth: melt pixel jaggies and JPEG blockiness so edges look
    #    scanned, not crystallized; the subtle sharpen below adds back
    #    just enough definition.
    gray = enhance.smooth_edges(gray)

    # 8. Crispness: unsharp mask scaled to staff spacing, after denoise so
    #    specks are removed before edges are boosted.
    if options.sharpen:
        gray = enhance.sharpen(
            gray,
            staff_space,
            amount=enhance.SHARPEN_AMOUNT,
            sigma_scale=enhance.SHARPEN_SIGMA_SCALE,
        )
        report.sharpened = True

    # 9. Whiten: saturate near-paper tones to pure white (the document-
    #    scanner look). Run after sharpening so grain raised toward white
    #    by the unsharp mask is erased too.
    if options.whiten:
        gray = enhance.saturate_white(gray, margin=enhance.PAPER_WHITE_MARGIN)

    # 10. Sauvola threshold: the ink decision. It drives QC (ink ratio)
    #     and the despeckle mask. The saved page keeps the restored
    #     grayscale with its anti-aliased edges - the natural scanned-PDF
    #     look; a hard 1-bit threshold is what makes edges crystallized,
    #     so strict black-and-white is opt-in (options.binary_output).
    window = max(15, int(options.sauvola_window_scale * staff_space))
    k = options.sauvola_k if options.sauvola_k is not None else enhance.sauvola_k_for(noise)
    report.sauvola_window_px = window
    report.sauvola_k = k
    binary = enhance.sauvola_binary(gray, window, k)
    ink_ratio = float((binary == 0).mean())
    if not (INK_RATIO_MIN <= ink_ratio <= INK_RATIO_MAX):
        report.warnings.append(
            f"ink coverage {100 * ink_ratio:.1f}% outside sane bounds "
            f"({100 * INK_RATIO_MIN:.1f}-{100 * INK_RATIO_MAX:.0f}%); "
            "thresholding may be unreliable, try a different --sauvola-k"
        )
    report.ink_ratio = ink_ratio

    # 11. Final page: restored grayscale (default) or strict 1-bit; grain
    #     blobs found in the threshold mask are erased from either.
    clean = binary.copy() if options.binary_output else gray.copy()
    if options.despeckle:
        mask, removed = enhance.speck_mask(
            binary, staff_space, area_scale=enhance.DESPECKLE_AREA_SCALE
        )
        if removed:
            clean[mask] = 255
        report.specks_removed = removed

    # 12. Diagnostics (paper flatness is measured on the enhanced grayscale,
    #     where it is still meaningful).
    report.paper_before = enhance.paper_stats(original)
    report.paper_after = enhance.paper_stats(gray)
    if report.paper_after.get("std", 0.0) > PAPER_UNEVENNESS_WARN:
        report.warnings.append(
            f"paper unevenness after correction (std={report.paper_after['std']}); "
            "try a larger --background-scale"
        )
    report.dark_border = enhance.detect_dark_border(original)
    if report.dark_border:
        report.warnings.append(
            "dark border frame detected (photocopy edge); consider cropping the scan"
        )

    return PageResult(clean=clean, report=report)


def _backup_raw(source: PageSource) -> None:
    """Move a first-run raw into original/ under its original name,
    overwriting any same-named file already preserved there."""
    backup = source.backup_path
    assert backup is not None
    backup.parent.mkdir(parents=True, exist_ok=True)
    os.replace(source.raw_path, backup)
    source.raw_path = backup
    source.backup_path = None


def _outputs(paths: ScanPaths, source: PageSource) -> dict[str, str]:
    """Report paths relative to the work dir (POSIX style)."""
    return {
        "processed": source.processed_path.relative_to(paths.work_dir).as_posix(),
        "original": source.raw_path.relative_to(paths.work_dir).as_posix(),
    }


def _build_preview(paths: ScanPaths, sources: list[PageSource]) -> None:
    if not sources:
        return
    width = 700 if len(sources) <= 4 else 420
    rows = []
    for source in sources:
        if not source.processed_path.exists():
            continue
        rows.append(
            [
                enhance.load_grayscale(source.raw_path),
                enhance.load_grayscale(source.processed_path),
            ]
        )
    if not rows:
        return
    enhance.save_image(enhance.make_preview(rows, width=width), paths.preview_path)


def run_pipeline(
    paths: ScanPaths,
    options: PrepOptions | None = None,
) -> ScanPaths:
    """Clean every raw page in the work directory, in place."""
    options = options or PrepOptions()
    sources = discover_page_sources(paths.work_dir)
    if not sources:
        raise FileNotFoundError(
            f"No sheet music images found in {paths.work_dir}. "
            f"Supported formats: {', '.join(sorted(IMAGE_EXTENSIONS))}"
        )

    total = len(sources)
    reports: list[PageReport] = []
    processed = 0

    for idx, source in enumerate(sources, start=1):
        for stray in source.strays:
            print(
                f"Page {idx}/{total} ({source.stem}): stray file {stray.name} left "
                "untouched; remove it so image2ly does not pick it up",
                file=sys.stderr,
            )

        if options.resume and source.settled and source.processed_path.exists():
            print(
                f"Skipping page {idx}/{total} (exists): {source.processed_path.name}",
                file=sys.stderr,
            )
            reports.append(
                PageReport(
                    index=idx,
                    stem=source.stem,
                    source=str(source.raw_path),
                    skipped=True,
                    outputs=_outputs(paths, source),
                )
            )
            continue

        print(
            f"Page {idx}/{total}: processing {source.raw_path.name}...",
            file=sys.stderr,
        )
        if not source.settled:
            _backup_raw(source)
            print(
                f"  raw kept as {source.raw_path.relative_to(paths.work_dir).as_posix()}",
                file=sys.stderr,
            )

        result = process_page(source.raw_path, idx, source.stem, options)
        enhance.save_image(result.clean, source.processed_path)
        result.report.outputs = _outputs(paths, source)
        reports.append(result.report)
        processed += 1

        for warning in result.report.warnings:
            print(f"  ! {warning}", file=sys.stderr)
        print(f"  -> {result.report.outputs['processed']}", file=sys.stderr)

    if options.preview:
        _build_preview(paths, sources)
        if paths.preview_path.exists():
            print(f"  -> {paths.preview_path.relative_to(paths.work_dir).as_posix()}", file=sys.stderr)

    _write_report(paths, options, reports)
    print(
        f"Done: {processed} page(s) cleaned in {paths.work_dir} "
        f"({total - processed} skipped)",
        file=sys.stderr,
    )
    return paths


def _write_report(paths: ScanPaths, options: PrepOptions, reports: list[PageReport]) -> None:
    payload = {
        "tool": "scanprep",
        "version": __version__,
        "parameters": options.to_dict(),
        "pages": [r.to_dict() for r in reports],
    }
    paths.scanprep_dir.mkdir(parents=True, exist_ok=True)
    paths.report_path.write_text(
        json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8"
    )


def run(target: str | Path, *, title: str | None = None, **option_overrides) -> ScanPaths:
    """Resolve a target and run the pipeline in one call."""
    paths, _ = ScanPaths.from_target(target, title=title)
    unknown = set(option_overrides) - set(PrepOptions.__dataclass_fields__)
    if unknown:
        raise ValueError(f"Unknown options: {sorted(unknown)}")
    options = replace(PrepOptions(), **option_overrides)
    return run_pipeline(paths, options)
