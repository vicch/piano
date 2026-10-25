from __future__ import annotations

import os
import re
from dataclasses import dataclass
from pathlib import Path
from urllib.parse import parse_qs, urlparse

from music2ly.config import Config, project_root
from music2ly.converter import (
    LilyPondFormatter,
    MusicXMLParser,
    ScoreConverter,
    convert_musicxml_to_lilypond,
)
from music2ly.models import ChunkInfo


@dataclass
class ChunkBody:
    treble: str
    bass: str


def _extract_parentheses_content(name: str) -> str:
    match = re.search(r"\(([^)]+)\)", name)
    if match:
        return match.group(1).strip()
    return ""


def _derive_sequence(source: str | Path | list[Path]) -> str:
    if isinstance(source, (list, tuple)):
        for item in source:
            seq = _extract_parentheses_content(Path(item).name)
            if seq:
                return seq
        return ""

    src_str = str(source)
    if src_str.startswith("http://") or src_str.startswith("https://"):
        parsed = urlparse(src_str)
        host = (parsed.hostname or "").lower()
        if host in ("youtu.be",):
            video_id = parsed.path.lstrip("/")
        elif "youtube" in host:
            q = parse_qs(parsed.query)
            video_id = (q.get("v") or [""])[0] or parsed.path.rsplit("/", 1)[-1]
        else:
            return ""
        return f"YouTube {video_id}" if video_id else ""

    p = Path(source)
    seq = _extract_parentheses_content(p.name)
    if seq:
        return seq
    if p.is_dir():
        for f in p.iterdir():
            seq = _extract_parentheses_content(f.name)
            if seq:
                return seq
    return ""


def _relative_template_include(output_path: Path) -> str:
    """Compute the relative include path from output file to template/base.ly."""
    template_path = project_root().parent / "template" / "base.ly"
    if not template_path.exists():
        return "../template/base.ly"
    try:
        return os.path.relpath(template_path, output_path.parent).replace("\\", "/")
    except ValueError:
        # Cross-drive on Windows
        return "../template/base.ly"


def _indent(body: str, spaces: int = 6) -> str:
    pad = " " * spaces
    return "\n".join(pad + line if line.strip() else line for line in body.splitlines())


def translate_chunk(
    chunk: ChunkInfo,
    config: Config | None = None,
    output_path: Path | None = None,
    default_time_signature=None,
    default_key_signature=None,
) -> ChunkBody:
    """Deterministically translates a single chunk MusicXML into treble & bass bodies."""
    xml_text = chunk.musicxml_path.read_text(encoding="utf-8")
    score_ir = MusicXMLParser.parse_xml(
        xml_text,
        default_time_signature=default_time_signature,
        default_key_signature=default_key_signature,
    )

    treble_str = ""
    bass_str = ""
    if len(score_ir.staves) >= 1:
        treble_str = LilyPondFormatter.format_staff(
            score_ir.staves[0],
            time_sig=score_ir.time_signature,
            key_sig=score_ir.key_signature,
            add_break=True,
        )
    if len(score_ir.staves) >= 2:
        bass_str = LilyPondFormatter.format_staff(
            score_ir.staves[1],
            time_sig=score_ir.time_signature,
            key_sig=score_ir.key_signature,
        )

    if output_path is not None:
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(
            f"% chunk {chunk.index}/{chunk.total} "
            f"(measures {chunk.measure_start}-{chunk.measure_end})\n"
            f"```lilypond-treble\n{treble_str}\n```\n\n"
            f"```lilypond-bass\n{bass_str}\n```\n",
            encoding="utf-8",
        )

    return ChunkBody(treble=treble_str, bass=bass_str)


def merge_lilypond_chunks(
    chunks: list[ChunkBody],
    *,
    title: str,
    sequence: str,
    metadata: dict,
    include_path: str,
) -> str:
    treble_parts = [c.treble.strip() for c in chunks if c.treble.strip()]
    bass_parts = [c.bass.strip() for c in chunks if c.bass.strip()]

    treble_combined = "\n".join(treble_parts) + ' \\bar "|."'
    bass_combined = "\n".join(bass_parts) + ' \\bar "|."'

    tempo = metadata.get("tempo", 96)
    key = metadata.get("key", "c \\major")
    time_sig = metadata.get("time", "4/4")

    return (
        '\\version "2.24.3"\n'
        "\n"
        f'#(define title      "{title}")\n'
        '#(define title-font "")\n'
        f'#(define sequence   "{sequence}")\n'
        "#(define total-page 1)\n"
        "\n"
        f'\\include "{include_path}"\n'
        "\n"
        "\\markup \\vspace #1.5\n"
        "\n"
        "\\score {\n"
        '  \\new PianoStaff \\with {\n'
        '    instrumentName = "Piano"\n'
        "  } <<\n"
        "    \\new Staff {\n"
        f"      \\tempo 4 = {tempo}\n"
        "      \\clef treble\n"
        f"      \\key {key}\n"
        f"      \\time {time_sig}\n"
        "      \n"
        f"{_indent(treble_combined)}\n"
        "    }\n"
        "    \\new Staff {\n"
        "      \\clef bass\n"
        f"      \\key {key}\n"
        f"      \\time {time_sig}\n"
        "      \n"
        f"{_indent(bass_combined)}\n"
        "    }\n"
        "    \\chords {\n"
        "    }\n"
        "  >>\n"
        "  \\layout {}\n"
        "  \\midi {}\n"
        "}\n"
    )


def translate_all_chunks(
    chunks: list[ChunkInfo],
    config: Config | None = None,
    lilypond_chunks_dir: Path | None = None,
    output_path: Path | None = None,
    *,
    title: str = "",
    source: str = "",
    sequence: str | None = None,
) -> Path:
    """Deterministically translates chunks to LilyPond fragments and merges them."""
    score_first = MusicXMLParser.parse_file(chunks[0].musicxml_path)
    from music2ly.converter.rules import KeyRule, TimeRule

    metadata = {
        "tempo": score_first.tempo,
        "key": KeyRule.to_lilypond(score_first.key_signature),
        "time": TimeRule.to_lilypond(score_first.time_signature),
    }

    bodies: list[ChunkBody] = []
    for chunk in chunks:
        chunk_out = (
            (lilypond_chunks_dir / f"chunk_{chunk.index:03d}.ly")
            if lilypond_chunks_dir
            else None
        )
        body = translate_chunk(
            chunk,
            config,
            chunk_out,
            default_time_signature=score_first.time_signature,
            default_key_signature=score_first.key_signature,
        )
        bodies.append(body)

    resolved_seq = sequence if sequence is not None else _derive_sequence(source)
    resolved_out = output_path or (chunks[0].musicxml_path.parent / f"{title}.ly")
    include_path = _relative_template_include(resolved_out)

    merged = merge_lilypond_chunks(
        bodies,
        title=title,
        sequence=resolved_seq,
        metadata=metadata,
        include_path=include_path,
    )
    resolved_out.parent.mkdir(parents=True, exist_ok=True)
    resolved_out.write_text(merged, encoding="utf-8")
    return resolved_out
