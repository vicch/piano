from pathlib import Path
import pytest

from music2ly.converter import (
    ChordIR,
    ChordRule,
    ClefChangeIR,
    ClefRule,
    DurationIR,
    DurationRule,
    KeyRule,
    KeySignatureIR,
    MeasureIR,
    MusicXMLParser,
    NoteIR,
    NoteRule,
    PitchIR,
    PitchRule,
    RestRule,
    ScoreConverter,
    ScoreIR,
    StaffIR,
    TimeRule,
    TimeSignatureIR,
    TupletIR,
    convert_musicxml_to_lilypond,
)


def test_pitch_rule_octaves():
    assert PitchRule.to_lilypond(PitchIR("C", 0, 4)) == "c'"
    assert PitchRule.to_lilypond(PitchIR("C", 0, 3)) == "c"
    assert PitchRule.to_lilypond(PitchIR("C", 0, 2)) == "c,"
    assert PitchRule.to_lilypond(PitchIR("C", 0, 1)) == "c,,"
    assert PitchRule.to_lilypond(PitchIR("C", 0, 5)) == "c''"
    assert PitchRule.to_lilypond(PitchIR("C", 0, 6)) == "c'''"


def test_pitch_rule_accidentals():
    # Sharps
    assert PitchRule.to_lilypond(PitchIR("D", 1, 5)) == "ds''"
    assert PitchRule.to_lilypond(PitchIR("F", 1, 4)) == "fs'"
    assert PitchRule.to_lilypond(PitchIR("C", 2, 4)) == "css'"

    # Flats
    assert PitchRule.to_lilypond(PitchIR("B", -1, 3)) == "bf"
    assert PitchRule.to_lilypond(PitchIR("E", -1, 4)) == "ef'"
    assert PitchRule.to_lilypond(PitchIR("A", -1, 2)) == "af,"
    assert PitchRule.to_lilypond(PitchIR("B", -2, 3)) == "bff"


def test_duration_rule():
    assert DurationRule.to_lilypond(DurationIR("quarter")) == "4"
    assert DurationRule.to_lilypond(DurationIR("eighth", dots=1)) == "8."
    assert DurationRule.to_lilypond(DurationIR("half", dots=2)) == "2.."
    assert DurationRule.to_lilypond(DurationIR("whole")) == "1"
    assert DurationRule.to_lilypond(DurationIR("16th")) == "16"
    assert DurationRule.to_lilypond(DurationIR("32nd")) == "32"

    # Fallback division estimation
    assert DurationRule.to_lilypond(DurationIR(None, duration_divisions=16), divisions=16) == "4"
    assert DurationRule.to_lilypond(DurationIR(None, duration_divisions=8), divisions=16) == "8"
    assert DurationRule.to_lilypond(DurationIR(None, duration_divisions=24), divisions=16) == "4."
    assert DurationRule.to_lilypond(DurationIR(None, duration_divisions=32), divisions=16) == "2"


def test_rest_rule():
    # Regular rests
    note_r4 = NoteIR(is_rest=True, duration=DurationIR("quarter"))
    assert RestRule.to_lilypond(note_r4) == "r4"

    note_r8 = NoteIR(is_rest=True, duration=DurationIR("eighth", dots=1))
    assert RestRule.to_lilypond(note_r8) == "r8."

    # Full measure rests (always lowercase 'r')
    full_rest = NoteIR(is_rest=True, is_full_measure_rest=True)
    assert RestRule.to_lilypond(full_rest, TimeSignatureIR(4, 4)) == "r1"
    assert RestRule.to_lilypond(full_rest, TimeSignatureIR(3, 4)) == "r2."
    assert RestRule.to_lilypond(full_rest, TimeSignatureIR(2, 4)) == "r2"
    assert RestRule.to_lilypond(full_rest, TimeSignatureIR(6, 8)) == "r2."


def test_derive_sequence():
    from music2ly.lilypond import _derive_sequence

    # From image filenames with parentheses
    assert _derive_sequence("Für Elise (EveryonePiano 47) 1.png") == "EveryonePiano 47"
    assert _derive_sequence("送别 (EveryonePiano 519).png") == "EveryonePiano 519"
    assert _derive_sequence("看见 (YouTube 7I34903vez8).ly") == "YouTube 7I34903vez8"
    assert _derive_sequence("Greensleeves (MuseScore 35704259-6340178).png") == "MuseScore 35704259-6340178"

    # From list of Paths
    imgs = [
        Path("output/Für Elise/Für Elise (EveryonePiano 47) 1.png"),
        Path("output/Für Elise/Für Elise (EveryonePiano 47) 2.png"),
    ]
    assert _derive_sequence(imgs) == "EveryonePiano 47"

    # From YouTube URL
    assert _derive_sequence("https://www.youtube.com/watch?v=7I34903vez8") == "YouTube 7I34903vez8"
    assert _derive_sequence("https://youtu.be/7I34903vez8") == "YouTube 7I34903vez8"

    # Default to empty string when not found
    assert _derive_sequence("Moonlight Sonata.png") == ""
    assert _derive_sequence("output/Moonlight/1.png") == ""
    assert _derive_sequence("") == ""


def test_chord_rule():
    chord = ChordIR(
        notes=[
            NoteIR(pitch=PitchIR("C", 0, 4)),
            NoteIR(pitch=PitchIR("E", 0, 4)),
            NoteIR(pitch=PitchIR("G", 0, 4)),
        ],
        duration=DurationIR("quarter"),
    )
    assert ChordRule.to_lilypond(chord) == "<c' e' g'>4"

    # Notes given highest-to-lowest are reordered lowest-to-highest
    chord_desc = ChordIR(
        notes=[
            NoteIR(pitch=PitchIR("G", 0, 4)),
            NoteIR(pitch=PitchIR("E", 0, 4)),
            NoteIR(pitch=PitchIR("C", 0, 4)),
        ],
        duration=DurationIR("quarter"),
    )
    assert ChordRule.to_lilypond(chord_desc) == "<c' e' g'>4"

    # Chord with tie and arpeggio
    chord_tie_arp = ChordIR(
        notes=[
            NoteIR(pitch=PitchIR("E", 0, 4)),
            NoteIR(pitch=PitchIR("G", 0, 4)),
            NoteIR(pitch=PitchIR("C", 0, 5)),
        ],
        duration=DurationIR("half"),
        tie_start=True,
        arpeggio=True,
    )
    assert ChordRule.to_lilypond(chord_tie_arp) == "<e' g' c''>2\\arpeggio ~"


def test_clef_rule():
    assert ClefRule.to_lilypond(ClefChangeIR("G", 2)) == "\\clef treble"
    assert ClefRule.to_lilypond(ClefChangeIR("F", 4)) == "\\clef bass"
    assert ClefRule.to_lilypond(ClefChangeIR("G", 2, octave_change=-1)) == '\\clef "treble_8"'
    assert ClefRule.to_lilypond(ClefChangeIR("C", 3)) == "\\clef alto"


def test_key_and_time_rule():
    assert KeyRule.to_lilypond(KeySignatureIR(0, "major")) == "c \\major"
    assert KeyRule.to_lilypond(KeySignatureIR(1, "major")) == "g \\major"
    assert KeyRule.to_lilypond(KeySignatureIR(-1, "major")) == "f \\major"
    assert KeyRule.to_lilypond(KeySignatureIR(0, "minor")) == "a \\minor"
    assert KeyRule.to_lilypond(KeySignatureIR(2, "major")) == "d \\major"

    assert TimeRule.to_lilypond(TimeSignatureIR(3, 4)) == "3/4"
    assert TimeRule.to_lilypond(TimeSignatureIR(4, 4)) == "4/4"
    assert TimeRule.to_lilypond(TimeSignatureIR(6, 8)) == "6/8"


def test_tuplet_formatting():
    score_xml = """<?xml version="1.0" encoding="UTF-8"?>
    <score-partwise>
      <part-list>
        <score-part id="P1"><part-name>Piano</part-name></score-part>
      </part-list>
      <part id="P1">
        <measure number="1">
          <attributes>
            <divisions>24</divisions>
            <time><beats>4</beats><beat-type>4</beat-type></time>
            <clef><sign>G</sign><line>2</line></clef>
          </attributes>
          <note>
            <pitch><step>C</step><octave>4</octave></pitch>
            <duration>16</duration>
            <type>eighth</type>
            <time-modification><actual-notes>3</actual-notes><normal-notes>2</normal-notes></time-modification>
          </note>
          <note>
            <pitch><step>D</step><octave>4</octave></pitch>
            <duration>16</duration>
            <type>eighth</type>
            <time-modification><actual-notes>3</actual-notes><normal-notes>2</normal-notes></time-modification>
          </note>
          <note>
            <pitch><step>E</step><octave>4</octave></pitch>
            <duration>16</duration>
            <type>eighth</type>
            <time-modification><actual-notes>3</actual-notes><normal-notes>2</normal-notes></time-modification>
          </note>
          <note>
            <pitch><step>F</step><octave>4</octave></pitch>
            <duration>24</duration>
            <type>quarter</type>
          </note>
        </measure>
      </part>
    </score-partwise>
    """
    ly = ScoreConverter.convert_xml(score_xml, title="Tuplet Test")
    assert "\\tuplet 3/2 { c'8 d'8 e'8 }" in ly
    assert "f'4" in ly


def test_polyphonic_voices_formatting():
    score_xml = """<?xml version="1.0" encoding="UTF-8"?>
    <score-partwise>
      <part-list>
        <score-part id="P1"><part-name>Piano</part-name></score-part>
      </part-list>
      <part id="P1">
        <measure number="1">
          <attributes>
            <divisions>16</divisions>
            <time><beats>4</beats><beat-type>4</beat-type></time>
            <clef><sign>G</sign><line>2</line></clef>
          </attributes>
          <note>
            <pitch><step>E</step><octave>5</octave></pitch>
            <duration>32</duration>
            <voice>1</voice>
            <type>half</type>
          </note>
          <note>
            <pitch><step>D</step><octave>5</octave></pitch>
            <duration>32</duration>
            <voice>1</voice>
            <type>half</type>
          </note>
          <note>
            <pitch><step>C</step><octave>4</octave></pitch>
            <duration>64</duration>
            <voice>2</voice>
            <type>whole</type>
          </note>
        </measure>
      </part>
    </score-partwise>
    """
    ly = ScoreConverter.convert_xml(score_xml, title="Polyphony Test")
    assert "<< { e''2 d''2 } \\\\ { c'1 } >>" in ly


def test_score_converter_end_to_end():
    score_xml = """<?xml version="1.0" encoding="UTF-8"?>
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
            <time><beats>3</beats><beat-type>4</beat-type></time>
            <clef><sign>G</sign><line>2</line></clef>
          </attributes>
          <note>
            <pitch><step>E</step><alter>0</alter><octave>5</octave></pitch>
            <duration>8</duration>
            <type>eighth</type>
          </note>
          <note>
            <pitch><step>D</step><alter>1</alter><octave>5</octave></pitch>
            <duration>8</duration>
            <type>eighth</type>
          </note>
          <note>
            <pitch><step>E</step><alter>0</alter><octave>5</octave></pitch>
            <duration>8</duration>
            <type>eighth</type>
          </note>
          <note>
            <pitch><step>D</step><alter>1</alter><octave>5</octave></pitch>
            <duration>8</duration>
            <type>eighth</type>
          </note>
          <note>
            <pitch><step>E</step><alter>0</alter><octave>5</octave></pitch>
            <duration>8</duration>
            <type>eighth</type>
          </note>
          <note>
            <pitch><step>B</step><alter>0</alter><octave>4</octave></pitch>
            <duration>8</duration>
            <type>eighth</type>
          </note>
        </measure>
        <measure number="2">
          <note>
            <pitch><step>D</step><alter>0</alter><octave>5</octave></pitch>
            <duration>8</duration>
            <type>eighth</type>
          </note>
          <note>
            <pitch><step>C</step><alter>0</alter><octave>5</octave></pitch>
            <duration>8</duration>
            <type>eighth</type>
          </note>
          <note>
            <pitch><step>A</step><alter>0</alter><octave>4</octave></pitch>
            <duration>32</duration>
            <type>half</type>
          </note>
        </measure>
      </part>
      <part id="P2">
        <measure number="1">
          <attributes>
            <divisions>16</divisions>
            <key><fifths>0</fifths></key>
            <time><beats>3</beats><beat-type>4</beat-type></time>
            <clef><sign>F</sign><line>4</line></clef>
          </attributes>
          <note>
            <rest measure="yes"/>
            <duration>48</duration>
            <type>whole</type>
          </note>
        </measure>
        <measure number="2">
          <note>
            <rest/>
            <duration>16</duration>
            <type>quarter</type>
          </note>
          <note>
            <pitch><step>A</step><octave>2</octave></pitch>
            <duration>8</duration>
            <type>eighth</type>
          </note>
          <note>
            <pitch><step>E</step><octave>3</octave></pitch>
            <duration>8</duration>
            <type>eighth</type>
          </note>
          <note>
            <pitch><step>A</step><octave>3</octave></pitch>
            <duration>8</duration>
            <type>eighth</type>
          </note>
          <note>
            <pitch><step>C</step><octave>4</octave></pitch>
            <duration>8</duration>
            <type>eighth</type>
          </note>
        </measure>
      </part>
    </score-partwise>
    """
    ly = convert_musicxml_to_lilypond(score_xml, title="Für Elise Test")
    assert '\\version "2.24.3"' in ly
    assert '#(define title      "Für Elise Test")' in ly
    assert '#(define source     "")' in ly
    assert "instrumentName" not in ly
    assert "\\vspace" not in ly
    assert ly.index("\\chords {") < ly.index("\\new Staff {")
    assert "\\key c \\major" in ly
    assert "\\time 3/4" in ly
    assert "e''8 ds''8 e''8 ds''8 e''8 b'8 | d''8 c''8 a'2" in ly
    assert "r2. | r4 a,8 e8 a8 c'8" in ly
    assert "\\break" not in ly
    assert ly.count('\\bar "|."') == 2
