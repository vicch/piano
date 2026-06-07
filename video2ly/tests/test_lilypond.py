import pytest

from video2ly.lilypond import merge_lilypond_chunks, parse_lilypond_block
from video2ly.musicxml import extract_variable_body


SAMPLE_CHUNK = """
trebleMusic = { c'4 d'4 e'4 f'4 \\break g'4 a'4 b'4 c''4 }
bassMusic = { c,4 d,4 e,4 f,4 \\break g,4 a,4 b,4 c4 }
"""


def test_parse_lilypond_block_fenced():
    response = "Here is the output:\n```lilypond\n\\version \"2.24.0\"\nc'4\n```"
    assert "\\version" in parse_lilypond_block(response)


def test_parse_lilypond_block_raw():
    assert parse_lilypond_block("\\version \"2.24.0\"\nc'4") == '\\version "2.24.0"\nc\'4'


def test_parse_lilypond_block_missing_raises():
    with pytest.raises(ValueError):
        parse_lilypond_block("no lilypond here")


def test_extract_variable_body():
    body = extract_variable_body(SAMPLE_CHUNK, "trebleMusic")
    assert body is not None
    assert "c'4" in body
    assert "bassMusic" not in body


def test_merge_lilypond_chunks():
    merged = merge_lilypond_chunks([SAMPLE_CHUNK, SAMPLE_CHUNK])
    assert '\\version "2.24.0"' in merged
    assert "treblePart" in merged
    assert "bassPart" in merged
    assert merged.count("c'4") >= 2
