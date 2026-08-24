from __future__ import annotations

import math
from typing import Sequence

from music2ly.converter.models import (
    ChordIR,
    ClefChangeIR,
    DurationIR,
    KeySignatureIR,
    NoteIR,
    PitchIR,
    TimeSignatureIR,
    TupletIR,
)


class PitchRule:
    """Translates pitch (step, alter, octave) to LilyPond English notation."""

    _ALTER_MAP = {
        -2: "ff",
        -1: "f",
        0: "",
        1: "s",
        2: "ss",
    }

    @classmethod
    def to_lilypond(cls, pitch: PitchIR | None) -> str:
        if pitch is None:
            return "c'"

        step_char = pitch.step.lower()
        alter_int = int(round(pitch.alter))
        accidental = cls._ALTER_MAP.get(alter_int, "")

        octave = pitch.octave
        if octave >= 3:
            octave_marks = "'" * (octave - 3)
        else:
            octave_marks = "," * (3 - octave)

        return f"{step_char}{accidental}{octave_marks}"


class DurationRule:
    """Translates MusicXML duration type and dots into LilyPond duration."""

    _TYPE_MAP = {
        "maxima": "\\maxima",
        "long": "\\longa",
        "breve": "\\breve",
        "whole": "1",
        "half": "2",
        "quarter": "4",
        "eighth": "8",
        "16th": "16",
        "32nd": "32",
        "64th": "64",
        "128th": "128",
        "256th": "256",
    }

    @classmethod
    def to_lilypond(cls, duration: DurationIR, divisions: int = 16) -> str:
        base = None
        if duration.type_name and duration.type_name.lower() in cls._TYPE_MAP:
            base = cls._TYPE_MAP[duration.type_name.lower()]

        if base is None:
            # Fallback: estimate from duration_divisions
            base = cls._estimate_type(duration.duration_divisions, divisions)

        dots = "." * max(0, duration.dots)
        return f"{base}{dots}"

    @classmethod
    def _estimate_type(cls, duration_divisions: int, divisions: int) -> str:
        if divisions <= 0 or duration_divisions <= 0:
            return "4"

        # quarters = duration_divisions / divisions
        # 1 quarter = 1.0 (LilyPond "4")
        # 1 whole = 4.0 (LilyPond "1")
        ratio = duration_divisions / divisions
        # Standard quarter-based durations:
        standard_ratios = [
            (4.0, "1"),
            (3.0, "2."),
            (2.0, "2"),
            (1.5, "4."),
            (1.0, "4"),
            (0.75, "8."),
            (0.5, "8"),
            (0.375, "16."),
            (0.25, "16"),
            (0.125, "32"),
            (0.0625, "64"),
        ]
        # Find closest match
        closest = min(standard_ratios, key=lambda pair: abs(pair[0] - ratio))
        return closest[1]


class RestRule:
    """Translates rest elements to LilyPond notation (always using lowercase 'r')."""

    @classmethod
    def to_lilypond(
        cls,
        note: NoteIR,
        time_sig: TimeSignatureIR | None = None,
        divisions: int = 16,
    ) -> str:
        if note.is_full_measure_rest:
            if time_sig:
                if time_sig.beats == 4 and time_sig.beat_type == 4:
                    return "r1"
                if time_sig.beats == 3 and time_sig.beat_type == 4:
                    return "r2."
                if time_sig.beats == 2 and time_sig.beat_type == 4:
                    return "r2"
                if time_sig.beats == 6 and time_sig.beat_type == 8:
                    return "r2."
                if time_sig.beats == 3 and time_sig.beat_type == 8:
                    return "r4."
                return f"r1*{time_sig.beats}/{time_sig.beat_type}"
            return "r1"

        dur = DurationRule.to_lilypond(note.duration, divisions)
        return f"r{dur}"


class NoteRule:
    """Translates single notes (including rests and articulations) to LilyPond."""

    @classmethod
    def to_lilypond(
        cls,
        note: NoteIR,
        time_sig: TimeSignatureIR | None = None,
        divisions: int = 16,
    ) -> str:
        if note.is_rest:
            return RestRule.to_lilypond(note, time_sig, divisions)

        pitch_str = PitchRule.to_lilypond(note.pitch)
        dur_str = DurationRule.to_lilypond(note.duration, divisions)

        art_parts: list[str] = []
        if note.finger:
            art_parts.append(f"^{note.finger}")
        if note.staccato:
            art_parts.append("-.")
        if note.accent:
            art_parts.append("->")
        if note.tenuto:
            art_parts.append("--")
        if note.fermata:
            art_parts.append("\\fermata")
        if note.arpeggio:
            art_parts.append("\\arpeggio")

        token = f"{pitch_str}{dur_str}{''.join(art_parts)}"
        if note.tie_start:
            token = f"{token} ~"
        return token


class ChordRule:
    """Translates simultaneous chord notes into LilyPond `<pitch ...>dur` syntax."""

    @classmethod
    def to_lilypond(
        cls,
        chord: ChordIR,
        divisions: int = 16,
    ) -> str:
        if not chord.notes:
            return "r4"

        pitch_tokens: list[str] = []
        for n in chord.notes:
            p_str = PitchRule.to_lilypond(n.pitch)
            if n.finger:
                p_str += f"^{n.finger}"
            pitch_tokens.append(p_str)

        inner = " ".join(pitch_tokens)
        dur_str = DurationRule.to_lilypond(chord.duration, divisions)

        art_parts: list[str] = []
        if chord.staccato or any(n.staccato for n in chord.notes):
            art_parts.append("-.")
        if chord.accent or any(n.accent for n in chord.notes):
            art_parts.append("->")
        if chord.tenuto or any(n.tenuto for n in chord.notes):
            art_parts.append("--")
        if chord.fermata or any(n.fermata for n in chord.notes):
            art_parts.append("\\fermata")
        if chord.arpeggio or any(n.arpeggio for n in chord.notes):
            art_parts.append("\\arpeggio")

        res = f"<{inner}>{dur_str}{''.join(art_parts)}"
        if chord.tie_start or any(n.tie_start for n in chord.notes):
            res = f"{res} ~"
        return res


class ClefRule:
    """Translates clef changes into LilyPond `\\clef ...` commands."""

    @classmethod
    def to_lilypond(cls, clef: ClefChangeIR) -> str:
        sign = clef.sign.upper()
        line = clef.line
        oct_chg = clef.octave_change

        if sign == "G" and line == 2:
            if oct_chg == -1:
                return '\\clef "treble_8"'
            if oct_chg == 1:
                return '\\clef "treble^8"'
            return "\\clef treble"
        if sign == "F" and line == 4:
            if oct_chg == -1:
                return '\\clef "bass_8"'
            if oct_chg == 1:
                return '\\clef "bass^8"'
            return "\\clef bass"
        if sign == "C" and line == 3:
            return "\\clef alto"
        if sign == "C" and line == 4:
            return "\\clef tenor"
        return "\\clef treble"


class KeyRule:
    """Translates key signatures (fifths + mode) to LilyPond `\\key ...` notation."""

    _SHARP_KEYS = ("c", "g", "d", "a", "e", "b", "fs", "cs")
    _FLAT_KEYS = ("c", "f", "bf", "ef", "af", "df", "gf", "cf")
    _SHARP_MINOR_KEYS = ("a", "e", "b", "fs", "cs", "gs", "ds", "as")
    _FLAT_MINOR_KEYS = ("a", "d", "g", "c", "f", "bf", "ef", "af")

    @classmethod
    def to_lilypond(cls, key: KeySignatureIR) -> str:
        mode = (key.mode or "major").lower()
        sharps = key.fifths

        if mode == "minor":
            if sharps >= 0:
                tonic = cls._SHARP_MINOR_KEYS[min(sharps, 7)]
            else:
                tonic = cls._FLAT_MINOR_KEYS[min(-sharps, 7)]
        else:
            if sharps >= 0:
                tonic = cls._SHARP_KEYS[min(sharps, 7)]
            else:
                tonic = cls._FLAT_KEYS[min(-sharps, 7)]

        return f"{tonic} \\{mode}"


class TimeRule:
    """Translates time signature to LilyPond `\\time ...` notation."""

    @classmethod
    def to_lilypond(cls, time_sig: TimeSignatureIR) -> str:
        return f"{time_sig.beats}/{time_sig.beat_type}"
