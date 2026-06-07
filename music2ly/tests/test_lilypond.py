import pytest

from music2ly.lilypond import ChunkBody, merge_lilypond_chunks, parse_chunk_response
from music2ly.musicxml import extract_variable_body


SAMPLE_CHUNK = """
trebleMusic = { c'4 d'4 e'4 f'4 \\break g'4 a'4 b'4 c''4 }
bassMusic = { c,4 d,4 e,4 f,4 \\break g,4 a,4 b,4 c4 }
"""


def test_parse_chunk_response_extracts_both_hands():
    response = (
        "Sure, here it is:\n"
        "```lilypond-treble\nc'4 d'4 e'4 f'4\n```\n"
        "```lilypond-bass\nc,4 d,4 e,4 f,4\n```\n"
    )
    treble, bass = parse_chunk_response(response)
    assert treble == "c'4 d'4 e'4 f'4"
    assert bass == "c,4 d,4 e,4 f,4"


def test_parse_chunk_response_missing_raises():
    with pytest.raises(ValueError):
        parse_chunk_response("no fenced lilypond blocks here")


def test_extract_variable_body():
    body = extract_variable_body(SAMPLE_CHUNK, "trebleMusic")
    assert body is not None
    assert "c'4" in body
    assert "bassMusic" not in body


def test_merge_lilypond_chunks_builds_score():
    chunks = [
        ChunkBody(treble="c'4 d'4 e'4 f'4", bass="c,4 d,4 e,4 f,4"),
        ChunkBody(treble="g'4 a'4 b'4 c''4", bass="g,4 a,4 b,4 c4"),
    ]
    merged = merge_lilypond_chunks(
        chunks,
        title="Test Song",
        sequence="Sheet image: test.png",
        metadata={"tempo": 96, "key": "c \\major", "time": "4/4"},
        include_path="../template/base.ly",
    )
    assert '\\version "2.24.3"' in merged
    assert "PianoStaff" in merged
    assert "\\clef treble" in merged
    assert "\\clef bass" in merged
    assert "Test Song" in merged
    assert "../template/base.ly" in merged
    # final barline applied once per hand (treble + bass)
    assert merged.count('\\bar "|."') == 2
    assert "c'4 d'4 e'4 f'4" in merged
