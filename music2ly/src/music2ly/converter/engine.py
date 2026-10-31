from __future__ import annotations

import os
from pathlib import Path
from typing import Sequence

from music2ly.converter.formatter import LilyPondFormatter
from music2ly.converter.models import ScoreIR, StaffIR
from music2ly.converter.parser import MusicXMLParser
from music2ly.models import ChunkInfo


class ScoreConverter:
    """Orchestrates deterministic MusicXML to LilyPond conversion."""

    @classmethod
    def convert_xml(
        cls,
        xml_text: str,
        *,
        title: str = "",
        source: str = "",
        include_path: str = "../template/base.ly",
    ) -> str:
        score = MusicXMLParser.parse_xml(xml_text, title=title)
        return LilyPondFormatter.format_score(
            score,
            source=source,
            include_path=include_path,
        )

    @classmethod
    def convert_file(
        cls,
        file_path: str | Path,
        *,
        title: str = "",
        source: str = "",
        include_path: str = "../template/base.ly",
    ) -> str:
        path = Path(file_path)
        content = path.read_text(encoding="utf-8")
        resolved_title = title or path.stem
        return cls.convert_xml(
            content,
            title=resolved_title,
            source=source,
            include_path=include_path,
        )

    @classmethod
    def convert_score_to_file(
        cls,
        source_xml_path: Path,
        output_path: Path,
        *,
        title: str = "",
        source: str = "",
        include_path: str | None = None,
    ) -> Path:
        resolved_title = title or output_path.stem
        rel_include = include_path or cls.relative_template_include(output_path)
        ly_code = cls.convert_file(
            source_xml_path,
            title=resolved_title,
            source=source,
            include_path=rel_include,
        )
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(ly_code, encoding="utf-8")
        return output_path

    @classmethod
    def relative_template_include(cls, output_path: Path) -> str:
        """Compute the relative include path from output file to template/base.ly."""
        # Check standard relative location: project_root / template / base.ly
        from music2ly.config import project_root

        template_path = project_root().parent / "template" / "base.ly"
        if not template_path.exists():
            return "../template/base.ly"
        try:
            return os.path.relpath(template_path, output_path.parent).replace("\\", "/")
        except ValueError:
            return "../template/base.ly"


def convert_musicxml_to_lilypond(
    musicxml_source: str | Path,
    output_path: Path | None = None,
    *,
    title: str = "",
    source: str = "",
    include_path: str | None = None,
) -> str:
    """Convenience functional API for deterministic MusicXML -> LilyPond conversion."""
    if output_path is not None:
        ScoreConverter.convert_score_to_file(
            Path(musicxml_source),
            output_path,
            title=title,
            source=source,
            include_path=include_path,
        )
        return output_path.read_text(encoding="utf-8")

    if isinstance(musicxml_source, Path) or (
        isinstance(musicxml_source, str) and not musicxml_source.strip().startswith("<")
    ):
        return ScoreConverter.convert_file(
            musicxml_source,
            title=title,
            source=source,
            include_path=include_path or "../template/base.ly",
        )

    return ScoreConverter.convert_xml(
        str(musicxml_source),
        title=title,
        source=source,
        include_path=include_path or "../template/base.ly",
    )
