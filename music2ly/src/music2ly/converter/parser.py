from __future__ import annotations

import re
import xml.etree.ElementTree as ET
from pathlib import Path

from music2ly.converter.models import (
    ChordIR,
    ClefChangeIR,
    DurationIR,
    KeySignatureIR,
    MeasureIR,
    NoteIR,
    PitchIR,
    ScoreIR,
    StaffIR,
    TimeSignatureIR,
    TupletIR,
)
from music2ly.musicxml import split_grand_staff_xml


class MusicXMLParser:
    """Parses MusicXML XML data into a strongly-typed ScoreIR."""

    @classmethod
    def parse_file(
        cls,
        file_path: str | Path,
        title: str = "",
        default_time_signature: TimeSignatureIR | None = None,
        default_key_signature: KeySignatureIR | None = None,
    ) -> ScoreIR:
        path = Path(file_path)
        content = path.read_text(encoding="utf-8")
        return cls.parse_xml(
            content,
            title=title or path.stem,
            default_time_signature=default_time_signature,
            default_key_signature=default_key_signature,
        )

    @classmethod
    def parse_xml(
        cls,
        xml_text: str,
        title: str = "",
        default_time_signature: TimeSignatureIR | None = None,
        default_key_signature: KeySignatureIR | None = None,
    ) -> ScoreIR:
        xml_clean = re.sub(r"<!DOCTYPE[^>]*>", "", xml_text)

        # If it's a 1-part grand staff (common in OMR), split into 2 parts first
        split_result = split_grand_staff_xml(xml_clean)
        if split_result is not None:
            xml_clean = split_result

        root = ET.fromstring(xml_clean)

        score_title = title
        work_title_elem = root.find(".//work/work-title")
        if work_title_elem is not None and work_title_elem.text and not score_title:
            score_title = work_title_elem.text.strip()

        score = ScoreIR(title=score_title)
        if default_time_signature is not None:
            score.time_signature = default_time_signature
        if default_key_signature is not None:
            score.key_signature = default_key_signature

        cls._extract_score_metadata(root, score)

        parts = root.findall("part")
        if not parts:
            return score

        for idx, part_elem in enumerate(parts):
            staff_ir = cls._parse_part(part_elem, staff_num=idx + 1)
            score.staves.append(staff_ir)

        return score

    @classmethod
    def _extract_score_metadata(cls, root: ET.Element, score: ScoreIR) -> None:
        # 1. Tempo
        sound_tempo = root.find(".//sound[@tempo]")
        if sound_tempo is not None and sound_tempo.get("tempo"):
            try:
                score.tempo = int(round(float(sound_tempo.get("tempo", 96))))
            except ValueError:
                pass
        else:
            metro_pm = root.find(".//metronome/per-minute")
            if metro_pm is not None and metro_pm.text:
                try:
                    score.tempo = int(round(float(metro_pm.text.strip())))
                except ValueError:
                    pass

        # Only extract initial score key/time from the first measure of the first part
        first_measure = root.find(".//part/measure")
        if first_measure is not None:
            fifths_elem = first_measure.find(".//attributes/key/fifths")
            if fifths_elem is not None and fifths_elem.text:
                try:
                    fifths = int(fifths_elem.text.strip())
                    mode_elem = first_measure.find(".//attributes/key/mode")
                    mode = mode_elem.text.strip() if mode_elem is not None and mode_elem.text else "major"
                    score.key_signature = KeySignatureIR(fifths=fifths, mode=mode)
                except ValueError:
                    pass

            beats_elem = first_measure.find(".//attributes/time/beats")
            beat_type_elem = first_measure.find(".//attributes/time/beat-type")
            if (
                beats_elem is not None
                and beats_elem.text
                and beat_type_elem is not None
                and beat_type_elem.text
            ):
                try:
                    score.time_signature = TimeSignatureIR(
                        beats=int(beats_elem.text.strip()),
                        beat_type=int(beat_type_elem.text.strip()),
                    )
                except ValueError:
                    pass

    @classmethod
    def _parse_part(cls, part_elem: ET.Element, staff_num: int) -> StaffIR:
        part_id = part_elem.get("id", f"P{staff_num}")
        staff_ir = StaffIR(
            part_id=part_id,
            staff_number=staff_num,
            initial_clef="bass" if staff_num == 2 else "treble",
        )

        current_divisions = 16
        for measure_elem in part_elem.findall("measure"):
            m_num_str = measure_elem.get("number", "1")
            try:
                m_num = int(m_num_str)
            except ValueError:
                m_num = 1

            measure_ir = MeasureIR(number=m_num, divisions=current_divisions)

            # Check attributes in this measure
            attr_elem = measure_elem.find("attributes")
            if attr_elem is not None:
                div_el = attr_elem.find("divisions")
                if div_el is not None and div_el.text:
                    try:
                        current_divisions = int(div_el.text.strip())
                        measure_ir.divisions = current_divisions
                    except ValueError:
                        pass

                clef_el = attr_elem.find("clef")
                if clef_el is not None:
                    sign_el = clef_el.find("sign")
                    line_el = clef_el.find("line")
                    oct_el = clef_el.find("clef-octave-change")
                    sign = sign_el.text.strip() if sign_el is not None and sign_el.text else "G"
                    line = int(line_el.text.strip()) if line_el is not None and line_el.text else 2
                    oct_chg = int(oct_el.text.strip()) if oct_el is not None and oct_el.text else 0
                    measure_ir.clef_change = ClefChangeIR(
                        sign=sign, line=line, octave_change=oct_chg
                    )
                    if not staff_ir.measures:
                        # First measure determines initial clef
                        staff_ir.initial_clef = "bass" if sign.upper() == "F" else "treble"

                time_el = attr_elem.find("time")
                if time_el is not None:
                    b_el = time_el.find("beats")
                    bt_el = time_el.find("beat-type")
                    if b_el is not None and b_el.text and bt_el is not None and bt_el.text:
                        try:
                            measure_ir.time_signature = TimeSignatureIR(
                                beats=int(b_el.text.strip()),
                                beat_type=int(bt_el.text.strip()),
                            )
                        except ValueError:
                            pass

                key_el = attr_elem.find("key")
                if key_el is not None:
                    f_el = key_el.find("fifths")
                    m_el = key_el.find("mode")
                    if f_el is not None and f_el.text:
                        try:
                            measure_ir.key_signature = KeySignatureIR(
                                fifths=int(f_el.text.strip()),
                                mode=m_el.text.strip() if m_el is not None and m_el.text else "major",
                            )
                        except ValueError:
                            pass

            # Parse notes and elements in measure
            cls._parse_measure_notes(measure_elem, measure_ir, current_divisions)
            staff_ir.measures.append(measure_ir)

        return staff_ir

    @classmethod
    def _parse_measure_notes(
        cls,
        measure_elem: ET.Element,
        measure_ir: MeasureIR,
        divisions: int,
    ) -> None:
        voices: dict[int, list[NoteIR | ChordIR | ClefChangeIR]] = {}

        for child in measure_elem:
            if child.tag == "note":
                note_ir = cls._parse_note(child, divisions)
                v = note_ir.voice
                if v not in voices:
                    voices[v] = []

                if note_ir.is_chord_member:
                    # Chord member: merge with previous element in this voice if possible
                    if voices[v]:
                        prev = voices[v][-1]
                        if isinstance(prev, ChordIR):
                            prev.notes.append(note_ir)
                            if note_ir.tie_start:
                                prev.tie_start = True
                        elif isinstance(prev, NoteIR):
                            chord = ChordIR(
                                notes=[prev, note_ir],
                                duration=prev.duration,
                                tie_start=prev.tie_start or note_ir.tie_start,
                                tie_stop=prev.tie_stop or note_ir.tie_stop,
                                tuplet=prev.tuplet,
                                arpeggio=prev.arpeggio or note_ir.arpeggio,
                                fermata=prev.fermata or note_ir.fermata,
                                staccato=prev.staccato or note_ir.staccato,
                                accent=prev.accent or note_ir.accent,
                                tenuto=prev.tenuto or note_ir.tenuto,
                                voice=v,
                                staff=note_ir.staff,
                            )
                            voices[v][-1] = chord
                        else:
                            voices[v].append(note_ir)
                    else:
                        voices[v].append(note_ir)
                else:
                    voices[v].append(note_ir)

            elif child.tag == "attributes":
                # Mid-measure clef change
                clef_el = child.find("clef")
                if clef_el is not None:
                    sign_el = clef_el.find("sign")
                    line_el = clef_el.find("line")
                    oct_el = clef_el.find("clef-octave-change")
                    sign = sign_el.text.strip() if sign_el is not None and sign_el.text else "G"
                    line = int(line_el.text.strip()) if line_el is not None and line_el.text else 2
                    oct_chg = int(oct_el.text.strip()) if oct_el is not None and oct_el.text else 0
                    clef_obj = ClefChangeIR(sign=sign, line=line, octave_change=oct_chg)
                    # Add clef change to voice 1
                    if 1 not in voices:
                        voices[1] = []
                    voices[1].append(clef_obj)

        measure_ir.elements_by_voice = voices

    @classmethod
    def _parse_note(cls, note_elem: ET.Element, divisions: int) -> NoteIR:
        note_ir = NoteIR()

        # Rest
        rest_el = note_elem.find("rest")
        if rest_el is not None:
            note_ir.is_rest = True
            # Only treat as full_measure_rest if no sub-measure type is given (or type is whole)
            type_el = note_elem.find("type")
            t_name = type_el.text.strip().lower() if type_el is not None and type_el.text else None
            if rest_el.get("measure") == "yes":
                if t_name in (None, "whole"):
                    note_ir.is_full_measure_rest = True
                else:
                    note_ir.is_full_measure_rest = False


        # Pitch
        pitch_el = note_elem.find("pitch")
        if pitch_el is not None:
            step_el = pitch_el.find("step")
            alter_el = pitch_el.find("alter")
            oct_el = pitch_el.find("octave")

            step = step_el.text.strip() if step_el is not None and step_el.text else "C"
            alter = float(alter_el.text.strip()) if alter_el is not None and alter_el.text else 0.0
            octave = int(oct_el.text.strip()) if oct_el is not None and oct_el.text else 4

            note_ir.pitch = PitchIR(step=step, alter=alter, octave=octave)

        # Duration
        dur_el = note_elem.find("duration")
        dur_div = int(dur_el.text.strip()) if dur_el is not None and dur_el.text else 0

        type_el = note_elem.find("type")
        type_name = type_el.text.strip() if type_el is not None and type_el.text else None
        dots = len(note_elem.findall("dot"))

        note_ir.duration = DurationIR(
            type_name=type_name,
            dots=dots,
            duration_divisions=dur_div,
        )

        # Chord flag
        if note_elem.find("chord") is not None:
            note_ir.is_chord_member = True

        # Voice & Staff
        voice_el = note_elem.find("voice")
        if voice_el is not None and voice_el.text:
            try:
                note_ir.voice = int(voice_el.text.strip())
            except ValueError:
                note_ir.voice = 1

        staff_el = note_elem.find("staff")
        if staff_el is not None and staff_el.text:
            try:
                note_ir.staff = int(staff_el.text.strip())
            except ValueError:
                note_ir.staff = 1

        # Ties
        for tie_el in note_elem.findall("tie"):
            t_type = tie_el.get("type")
            if t_type == "start":
                note_ir.tie_start = True
            elif t_type == "stop":
                note_ir.tie_stop = True
        for tied_el in note_elem.findall("tied"):
            t_type = tied_el.get("type")
            if t_type == "start":
                note_ir.tie_start = True
            elif t_type == "stop":
                note_ir.tie_stop = True

        # Tuplet / Time-modification
        tm_el = note_elem.find("time-modification")
        if tm_el is not None:
            act_el = tm_el.find("actual-notes")
            norm_el = tm_el.find("normal-notes")
            act = int(act_el.text.strip()) if act_el is not None and act_el.text else 3
            norm = int(norm_el.text.strip()) if norm_el is not None and norm_el.text else 2
            note_ir.tuplet = TupletIR(actual_notes=act, normal_notes=norm)

        # Notations & Articulations
        notations_el = note_elem.find("notations")
        if notations_el is not None:
            if notations_el.find("arpeggiate") is not None or notations_el.find("arpeggio") is not None:
                note_ir.arpeggio = True
            if notations_el.find("fermata") is not None:
                note_ir.fermata = True
            if notations_el.find(".//staccato") is not None:
                note_ir.staccato = True
            if notations_el.find(".//accent") is not None:
                note_ir.accent = True
            if notations_el.find(".//tenuto") is not None:
                note_ir.tenuto = True
            finger_el = notations_el.find(".//fingering")
            if finger_el is not None and finger_el.text:
                note_ir.finger = finger_el.text.strip()

        return note_ir
