from pathlib import Path
import pytest

from music2ly.converter import ScoreConverter
from music2ly.lilypond import (
    ChunkBody,
    merge_lilypond_chunks,
    translate_all_chunks,
    translate_chunk,
)
from music2ly.models import ChunkInfo
from music2ly.musicxml import extract_variable_body

SAMPLE_CHUNK = """
trebleMusic = { c'4 d'4 e'4 f'4 \\break g'4 a'4 b'4 c''4 }
bassMusic = { c,4 d,4 e,4 f,4 \\break g,4 a,4 b,4 c4 }
"""


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
        source="Sheet image: test.png",
        metadata={"tempo": 96, "key": "c \\major", "time": "4/4"},
        include_path="../template/base.ly",
    )
    assert '\\version "2.24.3"' in merged
    assert "PianoStaff" in merged
    assert "#(define source     \"Sheet image: test.png\")" in merged
    assert "instrumentName" not in merged
    assert "\\vspace" not in merged
    assert merged.index("\\chords {") < merged.index("\\new Staff {")
    assert "\\clef treble" in merged
    assert "\\clef bass" in merged
    assert "Test Song" in merged
    assert "../template/base.ly" in merged
    # final barline applied once per hand (treble + bass)
    assert merged.count('\\bar "|."') == 2
    assert "c'4 d'4 e'4 f'4" in merged


def test_translate_chunk_and_all_chunks_deterministic(tmp_path):
    # Create sample MusicXML
    xml_path1 = tmp_path / "chunk_001.musicxml"
    xml_path2 = tmp_path / "chunk_002.musicxml"

    xml_content_1 = """<?xml version="1.0" encoding="UTF-8"?>
    <score-partwise>
      <part-list>
        <score-part id="P1"><part-name>Treble</part-name></score-part>
        <score-part id="P2"><part-name>Bass</part-name></score-part>
      </part-list>
      <part id="P1">
        <measure number="1">
          <attributes>
            <divisions>16</divisions>
            <key><fifths>0</fifths></key>
            <time><beats>4</beats><beat-type>4</beat-type></time>
            <clef><sign>G</sign><line>2</line></clef>
          </attributes>
          <note>
            <pitch><step>C</step><octave>4</octave></pitch>
            <duration>16</duration>
            <type>quarter</type>
          </note>
          <note>
            <pitch><step>D</step><octave>4</octave></pitch>
            <duration>16</duration>
            <type>quarter</type>
          </note>
          <note>
            <pitch><step>E</step><octave>4</octave></pitch>
            <duration>16</duration>
            <type>quarter</type>
          </note>
          <note>
            <pitch><step>F</step><octave>4</octave></pitch>
            <duration>16</duration>
            <type>quarter</type>
          </note>
        </measure>
      </part>
      <part id="P2">
        <measure number="1">
          <attributes>
            <divisions>16</divisions>
            <key><fifths>0</fifths></key>
            <time><beats>4</beats><beat-type>4</beat-type></time>
            <clef><sign>F</sign><line>4</line></clef>
          </attributes>
          <note>
            <pitch><step>C</step><octave>3</octave></pitch>
            <duration>64</duration>
            <type>whole</type>
          </note>
        </measure>
      </part>
    </score-partwise>
    """

    xml_content_2 = """<?xml version="1.0" encoding="UTF-8"?>
    <score-partwise>
      <part-list>
        <score-part id="P1"><part-name>Treble</part-name></score-part>
        <score-part id="P2"><part-name>Bass</part-name></score-part>
      </part-list>
      <part id="P1">
        <measure number="2">
          <note>
            <pitch><step>G</step><octave>4</octave></pitch>
            <duration>64</duration>
            <type>whole</type>
          </note>
        </measure>
      </part>
      <part id="P2">
        <measure number="2">
          <note>
            <pitch><step>G</step><octave>2</octave></pitch>
            <duration>64</duration>
            <type>whole</type>
          </note>
        </measure>
      </part>
    </score-partwise>
    """

    xml_path1.write_text(xml_content_1, encoding="utf-8")
    xml_path2.write_text(xml_content_2, encoding="utf-8")

    chunk1 = ChunkInfo(
        index=1,
        total=2,
        measure_start=1,
        measure_end=1,
        duration_est=4.0,
        musicxml_path=xml_path1,
    )
    chunk2 = ChunkInfo(
        index=2,
        total=2,
        measure_start=2,
        measure_end=2,
        duration_est=4.0,
        musicxml_path=xml_path2,
    )

    body1 = translate_chunk(chunk1)
    assert "c'4 d'4 e'4 f'4" in body1.treble
    assert "c1" in body1.bass

    body2 = translate_chunk(chunk2)
    assert "g'1" in body2.treble
    assert "g,1" in body2.bass

    out_file = tmp_path / "OutputSong.ly"
    chunks_dir = tmp_path / "lilypond_chunks"
    result_path = translate_all_chunks(
        [chunk1, chunk2],
        lilypond_chunks_dir=chunks_dir,
        output_path=out_file,
        title="OutputSong",
        source="https://www.youtube.com/watch?v=TEST1234",
    )

    assert result_path.exists()
    content = result_path.read_text(encoding="utf-8")
    assert '#(define title      "OutputSong")' in content
    assert '#(define source     "YouTube TEST1234")' in content
    assert "c'4 d'4 e'4 f'4" in content
    assert "g'1" in content
    assert (chunks_dir / "chunk_001.ly").exists()
    assert (chunks_dir / "chunk_002.ly").exists()
