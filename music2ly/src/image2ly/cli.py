from __future__ import annotations

import argparse
import sys


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Convert an image of sheet music to LilyPond (not yet implemented).",
    )
    parser.add_argument("image", help="Path to a sheet-music image")
    parser.add_argument(
        "--title",
        "-t",
        required=True,
        help="Song title; artifacts and score go under output/<title>/",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    build_parser().parse_args(argv)
    print(
        "image2ly is not implemented yet. Planned pipeline: "
        "image -> OMR -> MusicXML -> LLM translate (music2ly.lilypond) -> LilyPond.",
        file=sys.stderr,
    )
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
