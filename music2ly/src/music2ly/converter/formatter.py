from __future__ import annotations

from typing import Sequence

from music2ly.converter.models import (
    ChordIR,
    ClefChangeIR,
    KeySignatureIR,
    MeasureIR,
    NoteIR,
    ScoreIR,
    StaffIR,
    TimeSignatureIR,
)
from music2ly.converter.rules import (
    ChordRule,
    ClefRule,
    KeyRule,
    NoteRule,
    TimeRule,
)


class LilyPondFormatter:
    """Formats ScoreIR into idiomatic, compile-ready LilyPond syntax."""

    @classmethod
    def format_score(
        cls,
        score: ScoreIR,
        *,
        sequence: str = "",
        include_path: str = "../template/base.ly",
    ) -> str:
        treble_content = ""
        bass_content = ""

        if len(score.staves) >= 1:
            treble_content = cls.format_staff(
                score.staves[0],
                time_sig=score.time_signature,
                key_sig=score.key_signature,
                add_break=True,
            )
        if len(score.staves) >= 2:
            bass_content = cls.format_staff(
                score.staves[1],
                time_sig=score.time_signature,
                key_sig=score.key_signature,
            )

        # Apply final barlines
        treble_formatted = treble_content.rstrip() + ' \\bar "|."'
        bass_formatted = bass_content.rstrip() + ' \\bar "|."'

        key_str = KeyRule.to_lilypond(score.key_signature)
        time_str = TimeRule.to_lilypond(score.time_signature)

        return (
            '\\version "2.24.3"\n'
            "\n"
            f'#(define title      "{score.title}")\n'
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
            f"      \\tempo 4 = {score.tempo}\n"
            "      \\clef treble\n"
            f"      \\key {key_str}\n"
            f"      \\time {time_str}\n"
            "      \n"
            f"{cls._indent(treble_formatted)}\n"
            "    }\n"
            "    \\new Staff {\n"
            "      \\clef bass\n"
            f"      \\key {key_str}\n"
            f"      \\time {time_str}\n"
            "      \n"
            f"{cls._indent(bass_formatted)}\n"
            "    }\n"
            "    \\chords {\n"
            "    }\n"
            "  >>\n"
            "  \\layout {}\n"
            "  \\midi {}\n"
            "}\n"
        )

    @classmethod
    def format_staff(
        cls,
        staff: StaffIR,
        time_sig: TimeSignatureIR | None = None,
        key_sig: KeySignatureIR | None = None,
        line_break_interval: int | None = 4,
        add_break: bool = False,
    ) -> str:
        measure_strs: list[str] = []
        current_clef = staff.initial_clef
        current_time = time_sig
        current_key = key_sig

        for idx, m in enumerate(staff.measures):
            time_change = None
            key_change = None

            if m.time_signature is not None:
                if current_time is None or (
                    m.time_signature.beats != current_time.beats
                    or m.time_signature.beat_type != current_time.beat_type
                ):
                    current_time = m.time_signature
                    if idx > 0:
                        time_change = m.time_signature

            if m.key_signature is not None:
                if current_key is None or (
                    m.key_signature.fifths != current_key.fifths
                    or m.key_signature.mode != current_key.mode
                ):
                    current_key = m.key_signature
                    if idx > 0:
                        key_change = m.key_signature

            m_str, current_clef = cls.format_measure(
                m,
                time_sig=current_time,
                current_clef=current_clef,
                time_change=time_change,
                key_change=key_change,
            )
            measure_strs.append(m_str)

        if line_break_interval is not None and line_break_interval > 0:
            lines = []
            for i in range(0, len(measure_strs), line_break_interval):
                group = measure_strs[i:i + line_break_interval]
                suffix = " \\break" if add_break else ""
                lines.append(" | ".join(group) + " |" + suffix)
            return "\n".join(lines)
        return " | ".join(measure_strs)

    @classmethod
    def format_measure(
        cls,
        measure: MeasureIR,
        time_sig: TimeSignatureIR | None = None,
        current_clef: str = "treble",
        time_change: TimeSignatureIR | None = None,
        key_change: KeySignatureIR | None = None,
    ) -> tuple[str, str]:
        prefix_tokens: list[str] = []
        if key_change is not None:
            prefix_tokens.append(f"\\key {KeyRule.to_lilypond(key_change)}")
        if time_change is not None:
            prefix_tokens.append(f"\\time {TimeRule.to_lilypond(time_change)}")
        prefix = (" ".join(prefix_tokens) + " ") if prefix_tokens else ""

        if not measure.elements_by_voice:
            # Empty measure -> full rest (always lowercase 'r')
            if time_sig:
                if time_sig.beats == 3 and time_sig.beat_type == 4:
                    return f"{prefix}r2.", current_clef
                if time_sig.beats == 4 and time_sig.beat_type == 4:
                    return f"{prefix}r1", current_clef
                return f"{prefix}r1*{time_sig.beats}/{time_sig.beat_type}", current_clef
            return f"{prefix}r1", current_clef

        active_voices = sorted(
            [v for v, elems in measure.elements_by_voice.items() if elems]
        )

        if not active_voices:
            return f"{prefix}r1", current_clef

        if len(active_voices) == 1:
            elems = measure.elements_by_voice[active_voices[0]]
            m_str, new_clef = cls._format_element_list(
                elems, time_sig, measure.divisions, current_clef
            )
            return f"{prefix}{m_str}", new_clef

        # Multi-voice measure: << { v1 } \\ { v2 } >>
        voice_blocks: list[str] = []
        new_clef = current_clef
        for v in active_voices:
            elems = measure.elements_by_voice[v]
            v_str, v_clef = cls._format_element_list(
                elems, time_sig, measure.divisions, current_clef
            )
            voice_blocks.append(f"{{ {v_str} }}")
            new_clef = v_clef

        return f"{prefix}<< {' \\\\ '.join(voice_blocks)} >>", new_clef

    @classmethod
    def _format_element_list(
        cls,
        elements: Sequence[NoteIR | ChordIR | ClefChangeIR],
        time_sig: TimeSignatureIR | None,
        divisions: int,
        current_clef: str = "treble",
    ) -> tuple[str, str]:
        tokens: list[str] = []
        in_tuplet: list[str] = []
        tuplet_info = None
        active_clef = current_clef

        for el in elements:
            if isinstance(el, ClefChangeIR):
                clef_name = "bass" if el.sign.upper() == "F" else "treble"
                if clef_name != active_clef:
                    clef_token = ClefRule.to_lilypond(el)
                    tokens.append(clef_token)
                    active_clef = clef_name
                continue

            # Format NoteIR or ChordIR
            if isinstance(el, NoteIR):
                token = NoteRule.to_lilypond(el, time_sig, divisions)
                tuplet = el.tuplet
            elif isinstance(el, ChordIR):
                token = ChordRule.to_lilypond(el, divisions)
                tuplet = el.tuplet
            else:
                continue

            if tuplet is not None:
                if tuplet_info is None:
                    tuplet_info = tuplet
                in_tuplet.append(token)
            else:
                if in_tuplet:
                    # Flush tuplet
                    tuplet_str = (
                        f"\\tuplet {tuplet_info.actual_notes}/{tuplet_info.normal_notes} "
                        f"{{ {' '.join(in_tuplet)} }}"
                    )
                    tokens.append(tuplet_str)
                    in_tuplet = []
                    tuplet_info = None
                tokens.append(token)

        if in_tuplet and tuplet_info is not None:
            tuplet_str = (
                f"\\tuplet {tuplet_info.actual_notes}/{tuplet_info.normal_notes} "
                f"{{ {' '.join(in_tuplet)} }}"
            )
            tokens.append(tuplet_str)

        return " ".join(tokens), active_clef

    @classmethod
    def _indent(cls, body: str, spaces: int = 6) -> str:
        pad = " " * spaces
        return "\n".join(pad + line if line.strip() else line for line in body.splitlines())
