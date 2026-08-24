from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class PitchIR:
    step: str  # 'C', 'D', 'E', 'F', 'G', 'A', 'B'
    alter: float = 0.0  # -2.0, -1.0, 0.0, 1.0, 2.0
    octave: int = 4  # 4 is middle C octave


@dataclass
class DurationIR:
    type_name: str | None = None  # 'whole', 'half', 'quarter', 'eighth', '16th', etc.
    dots: int = 0
    duration_divisions: int = 0
    actual_notes: int = 1
    normal_notes: int = 1


@dataclass
class TupletIR:
    actual_notes: int = 3
    normal_notes: int = 2
    type: str | None = None  # 'start', 'stop'


@dataclass
class NoteIR:
    pitch: PitchIR | None = None
    duration: DurationIR = field(default_factory=DurationIR)
    is_rest: bool = False
    is_full_measure_rest: bool = False
    is_chord_member: bool = False
    tie_start: bool = False
    tie_stop: bool = False
    tuplet: TupletIR | None = None
    arpeggio: bool = False
    fermata: bool = False
    staccato: bool = False
    accent: bool = False
    tenuto: bool = False
    finger: str | None = None
    voice: int = 1
    staff: int = 1


@dataclass
class ChordIR:
    notes: list[NoteIR] = field(default_factory=list)
    duration: DurationIR = field(default_factory=DurationIR)
    tie_start: bool = False
    tie_stop: bool = False
    tuplet: TupletIR | None = None
    arpeggio: bool = False
    fermata: bool = False
    staccato: bool = False
    accent: bool = False
    tenuto: bool = False
    voice: int = 1
    staff: int = 1


@dataclass
class ClefChangeIR:
    sign: str  # 'G', 'F', 'C'
    line: int = 2
    octave_change: int = 0


@dataclass
class TimeSignatureIR:
    beats: int = 4
    beat_type: int = 4


@dataclass
class KeySignatureIR:
    fifths: int = 0
    mode: str = "major"


@dataclass
class MeasureIR:
    number: int
    elements_by_voice: dict[int, list[NoteIR | ChordIR | ClefChangeIR]] = field(
        default_factory=dict
    )
    time_signature: TimeSignatureIR | None = None
    key_signature: KeySignatureIR | None = None
    clef_change: ClefChangeIR | None = None
    divisions: int = 16
    is_pickup: bool = False


@dataclass
class StaffIR:
    part_id: str
    staff_number: int = 1
    initial_clef: str = "treble"
    measures: list[MeasureIR] = field(default_factory=list)


@dataclass
class ScoreIR:
    title: str = ""
    tempo: int = 96
    time_signature: TimeSignatureIR = field(
        default_factory=lambda: TimeSignatureIR(4, 4)
    )
    key_signature: KeySignatureIR = field(default_factory=lambda: KeySignatureIR(0, "major"))
    staves: list[StaffIR] = field(default_factory=list)
