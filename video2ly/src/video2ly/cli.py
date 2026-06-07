from __future__ import annotations

import argparse
import sys
from pathlib import Path

from video2ly.config import Config
from video2ly.models import PipelinePaths
from video2ly.pipeline import ALL_STEPS, run_pipeline


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
        "--quantize-subdiv",
        type=int,
        choices=[2, 4, 8],
        default=4,
        help="Beat-snap grid for tempo quantize step: subdivisions per beat "
        "(2=8th, 4=16th, 8=32nd; default: 4)",
    )
    parser.add_argument(
        "--chunk-seconds",
        type=float,
        default=20.0,
        help="Target seconds per MusicXML chunk for LLM (default: 20)",
    )
    parser.add_argument(
        "--transcription-backend",
        choices=["piano", "basic-pitch"],
        default="piano",
        help="Audio-to-MIDI backend (default: piano)",
    )
    parser.add_argument(
        "--sensitivity",
        choices=["low", "medium", "high"],
        default=None,
        help="Transcription sensitivity preset (default: medium). "
        "Bundles onset/frame thresholds and post-quantize note filters. "
        "Lower = stricter, fewer ghost notes from effects/reverb. "
        "Higher = captures quieter/shorter notes.",
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
        "--llm-backend",
        choices=["lmstudio", "gemini"],
        default=None,
        help="LLM backend for LilyPond conversion. Default lmstudio "
        "(local OpenAI-compatible server); gemini is fallback.",
    )
    parser.add_argument(
        "--lmstudio-base-url",
        default=None,
        help="LM-Studio base URL (default http://127.0.0.1:1234/v1)",
    )
    parser.add_argument(
        "--lmstudio-model",
        default=None,
        help="LM-Studio model id (default google/gemma-4-31b)",
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
        quantize_subdiv=args.quantize_subdiv,
        chunk_seconds=args.chunk_seconds,
        transcription_backend=args.transcription_backend,
        gemini_model=args.gemini_model,
        llm_backend=args.llm_backend,
        lmstudio_base_url=args.lmstudio_base_url,
        lmstudio_model=args.lmstudio_model,
        sensitivity=args.sensitivity,
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
            title=args.title,
            steps=args.steps,
            resume=args.resume,
        )
    except (FileNotFoundError, ValueError, RuntimeError) as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
