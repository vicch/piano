from __future__ import annotations

import os
import re
from dataclasses import dataclass
from pathlib import Path
from urllib.parse import parse_qs, urlparse

import httpx
from google import genai
from google.genai import types
from music21 import converter

from piano_to_lilypond.config import Config, project_root, system_prompt_path
from piano_to_lilypond.models import ChunkInfo
from piano_to_lilypond.musicxml import slim_musicxml


TREBLE_FENCE_RE = re.compile(
    r"```lilypond-treble\s*\n(.*?)```",
    re.DOTALL | re.IGNORECASE,
)
BASS_FENCE_RE = re.compile(
    r"```lilypond-bass\s*\n(.*?)```",
    re.DOTALL | re.IGNORECASE,
)


def load_system_prompt() -> str:
    path = system_prompt_path()
    if not path.exists():
        raise FileNotFoundError(f"System prompt not found: {path}")
    return path.read_text(encoding="utf-8")


def parse_chunk_response(response_text: str) -> tuple[str, str]:
    treble_match = TREBLE_FENCE_RE.search(response_text)
    bass_match = BASS_FENCE_RE.search(response_text)
    if not treble_match or not bass_match:
        raise ValueError(
            "LLM response missing ```lilypond-treble``` or ```lilypond-bass``` fenced block. "
            f"Got: {response_text[:200]!r}"
        )
    return treble_match.group(1).strip(), bass_match.group(1).strip()


def build_user_prompt(chunk: ChunkInfo, musicxml_text: str) -> str:
    return (
        f"Chunk {chunk.index} of {chunk.total} "
        f"(measures {chunk.measure_start}–{chunk.measure_end}, ~{chunk.duration_est:.0f}s). "
        f"First chunk: {'yes' if chunk.index == 1 else 'no'}. "
        f"Last chunk: {'yes' if chunk.index == chunk.total else 'no'}.\n\n"
        f"MusicXML:\n```xml\n{musicxml_text}\n```"
    )


@dataclass
class ChunkBody:
    treble: str
    bass: str


def _call_lmstudio(system_prompt: str, user_prompt: str, config: Config) -> str:
    payload = {
        "model": config.lmstudio_model,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        "temperature": 0.2,
        "max_tokens": 24576,
        "stream": False,
    }
    url = f"{config.lmstudio_base_url}/chat/completions"
    with httpx.Client(timeout=httpx.Timeout(600.0, connect=10.0)) as client:
        resp = client.post(url, json=payload)
        resp.raise_for_status()
        data = resp.json()
    return data["choices"][0]["message"].get("content") or ""


def _call_gemini(system_prompt: str, user_prompt: str, config: Config) -> str:
    if not config.google_api_key:
        raise ValueError(
            "GOOGLE_API_KEY is required for the gemini backend. "
            "Set it in .env or your environment."
        )
    client = genai.Client(api_key=config.google_api_key)
    response = client.models.generate_content(
        model=config.gemini_model,
        contents=user_prompt,
        config=types.GenerateContentConfig(
            system_instruction=system_prompt,
            temperature=0.2,
            max_output_tokens=32768,
        ),
    )
    return response.text or ""


def translate_chunk(
    chunk: ChunkInfo,
    config: Config,
    system_prompt: str,
    output_path: Path,
) -> ChunkBody:
    musicxml_text = slim_musicxml(chunk.musicxml_path.read_text(encoding="utf-8"))
    user_prompt = build_user_prompt(chunk, musicxml_text)

    if config.llm_backend == "lmstudio":
        raw_text = _call_lmstudio(system_prompt, user_prompt, config)
    elif config.llm_backend == "gemini":
        raw_text = _call_gemini(system_prompt, user_prompt, config)
    else:
        raise ValueError(
            f"Unknown llm_backend: {config.llm_backend!r}. Expected 'lmstudio' or 'gemini'."
        )

    output_path.parent.mkdir(parents=True, exist_ok=True)
    raw_path = output_path.with_suffix(".raw.txt")
    raw_path.write_text(raw_text, encoding="utf-8")

    treble, bass = parse_chunk_response(raw_text)
    output_path.write_text(
        f"% chunk {chunk.index}/{chunk.total} "
        f"(measures {chunk.measure_start}-{chunk.measure_end})\n"
        f"```lilypond-treble\n{treble}\n```\n\n"
        f"```lilypond-bass\n{bass}\n```\n",
        encoding="utf-8",
    )
    return ChunkBody(treble=treble, bass=bass)


# ---------- score-header / template assembly -------------------------------


_SHARP_KEYS = ("c", "g", "d", "a", "e", "b", "fs", "cs")
_FLAT_KEYS = ("c", "f", "bf", "ef", "af", "df", "gf", "cf")


def _lilypond_key(sharps: int, mode: str = "major") -> str:
    if sharps >= 0:
        tonic = _SHARP_KEYS[min(sharps, 7)]
    else:
        tonic = _FLAT_KEYS[min(-sharps, 7)]
    if mode == "minor":
        # relative minor: 3 steps below the major tonic
        # Easier: use music21's pitch arithmetic.
        from music21 import key as m21key

        tonic = m21key.KeySignature(sharps).asKey("minor").tonic.name.lower()
        tonic = tonic.replace("-", "f").replace("#", "s")
    return f"{tonic} \\{mode}"


def _extract_score_metadata(first_chunk_path: Path) -> dict:
    score = converter.parse(str(first_chunk_path))

    tempo_bpm = 96
    for mark in score.recurse().getElementsByClass("MetronomeMark"):
        if mark.number:
            tempo_bpm = int(round(float(mark.number)))
            break

    key_str = "c \\major"
    for ks in score.recurse().getElementsByClass("KeySignature"):
        sharps = ks.sharps
        mode = getattr(ks, "mode", None) or "major"
        key_str = _lilypond_key(sharps, mode)
        break

    time_str = "4/4"
    for ts in score.recurse().getElementsByClass("TimeSignature"):
        time_str = f"{ts.numerator}/{ts.denominator}"
        break

    return {"tempo": tempo_bpm, "key": key_str, "time": time_str}


def _derive_sequence(youtube_url: str) -> str:
    parsed = urlparse(youtube_url)
    host = (parsed.hostname or "").lower()
    if host in ("youtu.be",):
        video_id = parsed.path.lstrip("/")
    elif "youtube" in host:
        q = parse_qs(parsed.query)
        video_id = (q.get("v") or [""])[0] or parsed.path.rsplit("/", 1)[-1]
    else:
        return parsed.netloc or "Unknown"
    return f"YouTube {video_id}" if video_id else "YouTube"


def _relative_template_include(output_path: Path) -> str:
    """Compute the relative include path from output file to template/base.ly."""
    template_path = project_root().parent / "template" / "base.ly"
    if not template_path.exists():
        return "../template/base.ly"
    return os.path.relpath(template_path, output_path.parent)


def _indent(body: str, spaces: int = 6) -> str:
    pad = " " * spaces
    return "\n".join(pad + line if line.strip() else line for line in body.splitlines())


def merge_lilypond_chunks(
    chunks: list[ChunkBody],
    *,
    title: str,
    sequence: str,
    metadata: dict,
    include_path: str,
) -> str:
    treble_combined = "\n      \n      ".join(c.treble.rstrip() for c in chunks)
    bass_combined = "\n      \n      ".join(c.bass.rstrip() for c in chunks)

    # Final barline on the last measure of both hands.
    treble_combined = _strip_trailing_break(treble_combined) + ' \\bar "|."'
    bass_combined = _strip_trailing_break(bass_combined) + ' \\bar "|."'

    return (
        '\\version "2.24.3"\n'
        '\n'
        f'#(define title      "{title}")\n'
        '#(define title-font "")\n'
        f'#(define sequence   "{sequence}")\n'
        '#(define total-page 1)\n'
        '\n'
        f'\\include "{include_path}"\n'
        '\n'
        '\\markup \\vspace #1.5\n'
        '\n'
        '\\score {\n'
        '  \\new PianoStaff \\with {\n'
        '    instrumentName = "Piano"\n'
        '  } <<\n'
        '    \\new Staff {\n'
        f'      \\tempo 4 = {metadata["tempo"]}\n'
        '      \\clef treble\n'
        f'      \\key {metadata["key"]}\n'
        f'      \\time {metadata["time"]}\n'
        '      \n'
        f'{_indent(treble_combined)}\n'
        '    }\n'
        '    \\new Staff {\n'
        '      \\clef bass\n'
        f'      \\key {metadata["key"]}\n'
        f'      \\time {metadata["time"]}\n'
        '      \n'
        f'{_indent(bass_combined)}\n'
        '    }\n'
        '    \\chords {\n'
        '    }\n'
        '  >>\n'
        '  \\layout {}\n'
        '  \\midi {}\n'
        '}\n'
    )


def _strip_trailing_break(body: str) -> str:
    stripped = body.rstrip()
    if stripped.endswith("\\break"):
        stripped = stripped[: -len("\\break")].rstrip()
    return stripped


def translate_all_chunks(
    chunks: list[ChunkInfo],
    config: Config,
    lilypond_chunks_dir: Path,
    output_path: Path,
    *,
    title: str,
    youtube_url: str,
) -> Path:
    if config.llm_backend == "gemini" and not config.google_api_key:
        raise ValueError(
            "GOOGLE_API_KEY is required for the gemini backend. "
            "Set it in .env or your environment."
        )

    system_prompt = load_system_prompt()
    bodies: list[ChunkBody] = []

    for chunk in chunks:
        chunk_out = lilypond_chunks_dir / f"chunk_{chunk.index:03d}.ly"
        body = translate_chunk(chunk, config, system_prompt, chunk_out)
        bodies.append(body)

    metadata = _extract_score_metadata(chunks[0].musicxml_path)
    sequence = _derive_sequence(youtube_url)
    include_path = _relative_template_include(output_path)

    merged = merge_lilypond_chunks(
        bodies,
        title=title,
        sequence=sequence,
        metadata=metadata,
        include_path=include_path,
    )
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(merged, encoding="utf-8")
    return output_path
