from __future__ import annotations

import argparse
import sys

from scanprep.models import ScanPaths


def _denoise_mode(raw: str) -> bool | None:
    """Map --denoise {auto,on,off}: None means decide from measured noise."""
    if raw == "auto":
        return None
    if raw == "on":
        return True
    if raw == "off":
        return False
    raise argparse.ArgumentTypeError("denoise must be one of: auto, on, off")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description=(
            "Pre-process raw scanned sheet-music images (scans, photocopies, "
            "photos) into clean, OMR-ready pages for image2ly. Processes in "
            "place: raws are moved as-is into an 'original/' subdirectory and "
            "cleaned pages are written as '<stem>.png', so image2ly picks up "
            "exactly the cleaned pages. Kernel sizes and corrections adapt to "
            "each page automatically."
        ),
    )
    parser.add_argument(
        "target",
        help=(
            "Directory of scan images, path to a scan image, or a song title "
            "(resolved under ./output/<title>/ like image2ly)"
        ),
    )
    parser.add_argument(
        "--title",
        "-t",
        default=None,
        help="Song title (default: directory or file name); outputs go to that directory",
    )
    parser.add_argument(
        "--no-deskew",
        action="store_true",
        help="Skip skew detection and rotation",
    )
    parser.add_argument(
        "--max-skew",
        type=float,
        default=3.0,
        help="Trust skew estimates up to this many degrees (default: 3)",
    )
    parser.add_argument(
        "--background-method",
        choices=("morph", "gaussian"),
        default="morph",
        help="Paper-background estimator (default: morph, which sees past solid "
        "title blocks; gaussian is smoother but can wash out large dark marks)",
    )
    parser.add_argument(
        "--background-scale",
        type=float,
        default=4.0,
        help="Background/kernel size in staff-spacing units (default: 4)",
    )
    parser.add_argument(
        "--paper-target",
        type=int,
        default=245,
        help="Target paper brightness after correction, 0-255 (default: 245)",
    )
    parser.add_argument(
        "--no-contrast",
        action="store_true",
        help="Skip the ink-darkening contrast remap",
    )
    parser.add_argument(
        "--no-whiten",
        action="store_true",
        help="Skip white saturation (paper grain survives as gray tones)",
    )
    parser.add_argument(
        "--no-sharpen",
        action="store_true",
        help="Skip the unsharp-mask crispness pass",
    )
    parser.add_argument(
        "--no-despeckle",
        action="store_true",
        help="Skip grain-blob removal from the restored page",
    )
    parser.add_argument(
        "--binary",
        action="store_true",
        help="Write a strict pure black-and-white page instead of the default "
        "restored grayscale (which keeps smooth anti-aliased edges like a "
        "professionally scanned document)",
    )
    parser.add_argument(
        "--sauvola-k",
        type=float,
        default=None,
        help="Pin Sauvola threshold sensitivity k "
        "(default: auto, 0.15 or 0.22 for noisy pages)",
    )
    parser.add_argument(
        "--sauvola-window-scale",
        type=float,
        default=5.0,
        help="Sauvola window in staff-spacing units (default: 5)",
    )
    parser.add_argument(
        "--denoise",
        type=_denoise_mode,
        default=None,
        help="Speck denoising: auto (decide from measured noise), on, off (default: auto)",
    )
    parser.add_argument(
        "--no-preview",
        action="store_true",
        help="Do not write the side-by-side preview contact sheet",
    )
    parser.add_argument(
        "--resume",
        action="store_true",
        help="Skip pages already cleaned in place (raw backed up + page exists)",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    try:
        # Imported lazily so a missing 'scan' extra produces a friendly hint
        # instead of a raw traceback at CLI startup.
        from scanprep.pipeline import PrepOptions, run_pipeline

        paths, _title = ScanPaths.from_target(args.target, title=args.title)
        options = PrepOptions(
            deskew=not args.no_deskew,
            max_skew=args.max_skew,
            background_method=args.background_method,
            background_scale=args.background_scale,
            paper_target=args.paper_target,
            contrast=not args.no_contrast,
            whiten=not args.no_whiten,
            sharpen=not args.no_sharpen,
            despeckle=not args.no_despeckle,
            binary_output=args.binary,
            sauvola_k=args.sauvola_k,
            sauvola_window_scale=args.sauvola_window_scale,
            denoise=args.denoise,
            preview=not args.no_preview,
            resume=args.resume,
        )
        run_pipeline(paths, options)
    except ImportError as exc:
        print(
            f"Error: scanprep dependencies missing ({exc}). "
            "Install with: uv sync --extra scan",
            file=sys.stderr,
        )
        return 1
    except (FileNotFoundError, ValueError, RuntimeError) as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
