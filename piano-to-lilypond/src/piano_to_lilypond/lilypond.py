from __future__ import annotations

import re
from pathlib import Path

from google import genai
from google.genai import types

from piano_to_lilypond.config import Config, system_prompt_path
from piano_to_lilypond.models import ChunkInfo
from piano_to_lilypond.musicxml import extract_variable_body


LILYPOND_FENCE_RE = re.compile(
    r"```(?:lilypond|ly)?\s*\n(.*?)```",
    re.DOTALL | re.IGNORECASE,
)


def load_system_prompt() -> str:
    path = system_prompt_path()
    if not path.exists():
        raise FileNotFoundError(f"System prompt not found: {path}")
    return path.read_text(encoding="utf-8")


def parse_lilypond_block(response_text: str) -> str:
    match = LILYPOND_FENCE_RE.search(response_text)
    if match:
        content = match.group(1).strip()
        if content:
            return content

    stripped = response_text.strip()
    if stripped.startswith("\\"):
        return stripped

    raise ValueError("LLM response did not contain a valid LilyPond fenced block")


def build_user_prompt(chunk: ChunkInfo, musicxml_text: str) -> str:
    return (
        f"Convert the following MusicXML excerpt to LilyPond.\n"
        f"Chunk {chunk.index} of {chunk.total}.\n"
        f"Measures {chunk.measure_start}–{chunk.measure_end} "
        f"(~{chunk.duration_est:.0f}s).\n"
        f"First chunk: {'yes' if chunk.index == 1 else 'no'}.\n\n"
        f"MusicXML:\n```xml\n{musicxml_text}\n```"
    )


def translate_chunk(
    chunk: ChunkInfo,
    config: Config,
    client: genai.Client,
    system_prompt: str,
    output_path: Path,
) -> str:
    musicxml_text = chunk.musicxml_path.read_text(encoding="utf-8")
    user_prompt = build_user_prompt(chunk, musicxml_text)

    response = client.models.generate_content(
        model=config.gemini_model,
        contents=user_prompt,
        config=types.GenerateContentConfig(
            system_instruction=system_prompt,
            temperature=0.2,
        ),
    )

    lilypond_body = parse_lilypond_block(response.text or "")
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(lilypond_body + "\n", encoding="utf-8")
    return lilypond_body


def merge_lilypond_chunks(chunk_bodies: list[str]) -> str:
    treble_parts: list[str] = []
    bass_parts: list[str] = []

    for body in chunk_bodies:
        treble = extract_variable_body(body, "trebleMusic")
        bass = extract_variable_body(body, "bassMusic")

        if treble is None or bass is None:
            raise ValueError(
                "Each chunk must define trebleMusic and bassMusic variables. "
                f"Missing in chunk body starting with: {body[:80]!r}"
            )

        treble_parts.append(treble)
        bass_parts.append(bass)

    treble_combined = " ".join(treble_parts)
    bass_combined = " ".join(bass_parts)

    return (
        '\\version "2.24.0"\n'
        '\\include "english.ly"\n\n'
        f"treblePart = {{ {treble_combined} }}\n"
        f"bassPart = {{ {bass_combined} }}\n\n"
        "\\score {\n"
        "  <<\n"
        "    \\new Staff { \\clef treble \\treblePart }\n"
        "    \\new Staff { \\clef bass \\bassPart }\n"
        "  >>\n"
        "  \\layout {\n"
        "    \\context {\n"
        "      \\Score\n"
        "      \\override BarNumber.break-visibility = ##t\n"
        "    }\n"
        "  }\n"
        "}\n"
    )


def translate_all_chunks(
    chunks: list[ChunkInfo],
    config: Config,
    lilypond_chunks_dir: Path,
    output_path: Path,
) -> Path:
    if not config.google_api_key:
        raise ValueError(
            "GOOGLE_API_KEY is required for LilyPond generation. "
            "Set it in .env or your environment."
        )

    client = genai.Client(api_key=config.google_api_key)
    system_prompt = load_system_prompt()
    bodies: list[str] = []

    for chunk in chunks:
        chunk_out = lilypond_chunks_dir / f"chunk_{chunk.index:03d}.ly"
        body = translate_chunk(chunk, config, client, system_prompt, chunk_out)
        bodies.append(body)

    merged = merge_lilypond_chunks(bodies)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(merged, encoding="utf-8")
    return output_path
