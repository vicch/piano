from __future__ import annotations

import argparse
import sys
from pathlib import Path

from piano_to_lilypond.config import Config
from piano_to_lilypond.models import PipelinePaths
from piano_to_lilypond.pipeline import ALL_STEPS, run_pipeline


def parse_steps(raw: str) -> set[str]:
    if raw == "all":
        return {"all"}
    steps = {s.strip() for s in raw.split(",") if s.strip()}
    unknown = steps - set(ALL_STEPS)
    if unknown:
        raise argparse.ArgumentTypeError(f"Unknown steps: {unknown}. Valid: {', '.join(ALL_STEPS)}, all")
    return steps


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Convert a YouTube piano performance to LilyPond sheet music.",
    )
    parser.add_argument("url", help="YouTube video URL")
    parser.add_argument(
        "--title",
        "-t",
        required=True,
        help="Song title; artifacts and score go under output/<title>/",
    )
    parser.add_argument(
        "--quantize",
        type=int,
        choices=[8, 16],
        default=16,
        help="Quantization grid: 1/8 or 1/16 notes (default: 16)",
    )
    parser.add_argument(
        "--chunk-seconds",
        type=float,
        default=90.0,
        help="Target seconds per MusicXML chunk for LLM (default: 90)",
    )
    parser.add_argument(
        "--transcription-backend",
        choices=["piano", "basic-pitch"],
        default="piano",
        help="Audio-to-MIDI backend (default: piano)",
    )
    parser.add_argument(
        "--steps",
        type=parse_steps,
        default={"all"},
        help=f"Comma-separated steps to run, or 'all' (default). Steps: {', '.join(ALL_STEPS)}",
    )
    parser.add_argument(
        "--resume",
        action="store_true",
        help="Skip steps whose output artifacts already exist",
    )
    parser.add_argument(
        "--env-file",
        type=Path,
        default=None,
        help="Path to .env file (default: .env in current directory)",
    )
    parser.add_argument(
        "--gemini-model",
        default=None,
        help="Override GEMINI_MODEL from environment",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    config = Config.load(
        env_file=args.env_file,
        quantize_divisor=args.quantize,
        chunk_seconds=args.chunk_seconds,
        transcription_backend=args.transcription_backend,
        gemini_model=args.gemini_model,
    )

    paths = PipelinePaths.from_title(args.title)
    paths = PipelinePaths.from_project_dir(
        paths.work_dir.resolve(),
        paths.output_path.resolve(),
    )

    try:
        run_pipeline(
            args.url,
            paths,
            config,
            steps=args.steps,
            resume=args.resume,
        )
    except (FileNotFoundError, ValueError, RuntimeError) as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
