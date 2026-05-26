from music21 import chord, note, stream

from piano_to_lilypond.musicxml import split_hands


def test_split_hands_middle_c():
    part = stream.Part()
    part.insert(0, note.Note("C3", quarterLength=1))
    part.insert(0, note.Note("C4", quarterLength=1))
    part.insert(0, chord.Chord(["E3", "G3", "C4", "E4"], quarterLength=1))

    treble, bass = split_hands(part, middle_c=60)

    treble_pitches = {p.nameWithOctave for el in treble.flatten().notes for p in el.pitches}
    bass_pitches = {p.nameWithOctave for el in bass.flatten().notes for p in el.pitches}

    assert "C4" in treble_pitches
    assert "E4" in treble_pitches
    assert "C3" in bass_pitches
    assert "E3" in bass_pitches
    assert "G3" in bass_pitches
