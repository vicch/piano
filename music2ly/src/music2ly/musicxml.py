from __future__ import annotations

import copy
import json
import re
import xml.etree.ElementTree as ET
from pathlib import Path

from music21 import stream

from music2ly.models import ChunkInfo


# MusicXML elements/attrs that are pure engraving cruft for our LLM translation.
# Dropping them shrinks chunk size 40-60% with zero information loss for LilyPond
# output (the LLM doesn't need page layout, stem direction, or voicing hints).
_SLIM_DROP_TAGS = {
    "identification",
    "defaults",
    "print",
    "credit",
    "work",
    "movement-title",
    "part-abbreviation",
    "score-instrument",
    "midi-instrument",
    "notations",
    "stem",
    "beam",
    "sound",
}
_SLIM_DROP_ATTRS = {
    "default-x",
    "default-y",
    "dynamics",
    "width",
    "id",
    "color",
    "font-family",
    "font-size",
    "placement",
    "relative-x",
    "relative-y",
    "print-object",
}


def slim_musicxml(xml_text: str) -> str:
    """Strip engraving/layout cruft from MusicXML so the LLM sees just the music."""
    xml_text = re.sub(r"<!DOCTYPE[^>]*>", "", xml_text)
    root = ET.fromstring(xml_text)
    _slim_element(root)
    return ET.tostring(root, encoding="unicode")


def _slim_element(elem: ET.Element) -> None:
    for child in list(elem):
        if child.tag in _SLIM_DROP_TAGS:
            elem.remove(child)
    for attr in list(elem.attrib):
        if attr in _SLIM_DROP_ATTRS:
            del elem.attrib[attr]
    for child in elem:
        _slim_element(child)
    if elem.text and not elem.text.strip():
        elem.text = None
    if elem.tail and not elem.tail.strip():
        elem.tail = None


def _estimate_seconds_per_measure(part: stream.Part) -> float:
    tempo = 120.0
    for mark in part.recurse().getElementsByClass("MetronomeMark"):
        if mark.number:
            tempo = float(mark.number)
            break

    ts = part.getTimeSignatures()[0] if part.getTimeSignatures() else None
    beats = float(ts.numerator) if ts else 4.0
    beat_type = float(ts.denominator) if ts else 4.0
    quarter_beats = beats * (4.0 / beat_type)
    return (60.0 / tempo) * quarter_beats


def _attributes_for_staff(attributes: ET.Element, staff: str) -> ET.Element:
    """Copy an <attributes> block keeping shared keys plus only this staff's clef.

    A grand-staff <attributes> carries one <clef number="N"> per staff. When we
    fan the part out into one part per staff, each staff must keep only its own
    clef (with the now-redundant ``number`` attribute dropped) and shed the
    <staves> count, while retaining shared <divisions>/<key>/<time>.
    """
    out = ET.Element("attributes")
    for child in attributes:
        if child.tag == "staves":
            continue
        if child.tag == "clef":
            if child.get("number") not in (None, staff):
                continue
            clef_copy = copy.deepcopy(child)
            clef_copy.attrib.pop("number", None)
            out.append(clef_copy)
            continue
        out.append(copy.deepcopy(child))
    return out


def split_grand_staff_xml(xml_text: str) -> str | None:
    """Split a single multi-staff <part> into one <part> per staff.

    OMR engines (e.g. homr) emit a piano grand staff as a single <part> whose
    hands share <voice>1</voice> and are told apart only by <staff>1/2</staff>,
    interleaved with per-note <backup>. music21 merges equal-numbered voices and
    discards the <staff> tag, collapsing both hands into one overlapping stream.
    Rewriting to one <part> per staff (the staff tag is the only reliable hand
    signal) makes music21 yield separate treble/bass Parts.

    Returns rewritten MusicXML, or None when the split does not apply: anything
    other than exactly one part, or a part with fewer than two staves, is left
    untouched for music21's normal path.
    """
    xml_text = re.sub(r"<!DOCTYPE[^>]*>", "", xml_text)
    root = ET.fromstring(xml_text)
    parts = root.findall("part")
    if len(parts) != 1:
        return None
    src_part = parts[0]

    staff_nums = sorted(
        {s.text for s in src_part.iter("staff") if s.text},
        key=int,
    )
    if len(staff_nums) < 2:
        return None

    new_parts = {
        staff: ET.Element("part", {"id": f"P{i + 1}"})
        for i, staff in enumerate(staff_nums)
    }

    for measure in src_part.findall("measure"):
        new_measures = {
            staff: ET.SubElement(new_parts[staff], "measure", dict(measure.attrib))
            for staff in staff_nums
        }
        # Each staff is its own sequential timeline once split, so <backup>/
        # <forward> (which only exist to interleave staves) are dropped. A note
        # without its own <staff> (e.g. a chord member) inherits the previous
        # note's staff.
        last_staff = staff_nums[0]
        for child in list(measure):
            if child.tag in ("backup", "forward"):
                continue
            if child.tag == "attributes":
                for staff in staff_nums:
                    new_measures[staff].append(_attributes_for_staff(child, staff))
                continue
            if child.tag == "note":
                staff_el = child.find("staff")
                if staff_el is not None and staff_el.text:
                    last_staff = staff_el.text
                note_copy = copy.deepcopy(child)
                inner_staff = note_copy.find("staff")
                if inner_staff is not None:
                    note_copy.remove(inner_staff)
                new_measures[last_staff].append(note_copy)
                continue
            # Barlines, directions, etc. apply to the system: copy to every staff.
            for staff in staff_nums:
                new_measures[staff].append(copy.deepcopy(child))

    part_list = root.find("part-list")
    insert_at = list(root).index(part_list) if part_list is not None else len(list(root))
    if part_list is not None:
        root.remove(part_list)
    root.remove(src_part)

    new_part_list = ET.Element("part-list")
    for i in range(len(staff_nums)):
        score_part = ET.SubElement(new_part_list, "score-part", {"id": f"P{i + 1}"})
        ET.SubElement(score_part, "part-name").text = "Piano"
    root.insert(insert_at, new_part_list)
    for part in new_parts.values():
        root.append(part)

    return ET.tostring(root, encoding="unicode")


def load_grand_staff(musicxml_path: Path) -> tuple[stream.Part, stream.Part, int]:
    """Parse a MusicXML file into (treble, bass, measure_count).

    Source-agnostic: works for MuseScore output (video2ly) and OMR output
    (image2ly). A piano grand staff that music21 already splits into two Parts is
    used as-is; a single multi-staff part (common from OMR) is first fanned out
    by staff via ``split_grand_staff_xml``. Falls back to duplicating the sole
    part only when there is genuinely one single-staff part.
    """
    from music21 import converter

    raw = Path(musicxml_path).read_text(encoding="utf-8")
    rewritten = split_grand_staff_xml(raw)
    if rewritten is not None:
        score = converter.parse(rewritten, format="musicxml")
    else:
        score = converter.parse(str(musicxml_path))
    parts = list(score.parts)
    if not parts:
        raise ValueError(f"MusicXML has no parts: {musicxml_path}")

    if len(parts) >= 2:
        treble, bass = parts[0], parts[1]
    else:
        treble = bass = parts[0]

    measure_count = max(
        len(list(treble.getElementsByClass("Measure"))),
        len(list(bass.getElementsByClass("Measure"))),
    )
    return treble, bass, measure_count


def chunk_musicxml(
    treble: stream.Part,
    bass: stream.Part,
    chunks_dir: Path,
    *,
    chunk_seconds: float = 90.0,
    make_notation: bool = True,
) -> list[ChunkInfo]:
    """Split treble/bass parts into per-chunk MusicXML files.

    ``make_notation`` controls music21's re-notation on export. Keep it True for
    MIDI-derived parts (video2ly) that need rest/tie/beam derivation. Set it
    False for OMR output (image2ly): those measures are already segmented, and
    re-deriving ties trips music21 on irregular OMR measures.
    """
    chunks_dir.mkdir(parents=True, exist_ok=True)

    treble_measures = list(treble.getElementsByClass("Measure"))
    bass_measures = list(bass.getElementsByClass("Measure"))
    measure_count = max(len(treble_measures), len(bass_measures))

    if measure_count == 0:
        raise ValueError("No measures found after processing MIDI")

    seconds_per_measure = _estimate_seconds_per_measure(treble)
    measures_per_chunk = max(8, min(32, int(chunk_seconds / seconds_per_measure)))
    if measures_per_chunk < 1:
        measures_per_chunk = 8

    chunk_infos: list[ChunkInfo] = []
    chunk_index = 0
    measure_start = 1

    while measure_start <= measure_count:
        measure_end = min(measure_start + measures_per_chunk - 1, measure_count)
        chunk_index += 1

        # deepcopy the slices: measures() returns elements that retain site
        # references to the source part, which music21's export deepcopy can
        # trip over (KeyError in sortTuple) for some OMR-produced scores.
        treble_slice = copy.deepcopy(treble.measures(measure_start, measure_end))
        bass_slice = copy.deepcopy(bass.measures(measure_start, measure_end))

        chunk_score = stream.Score()
        chunk_score.insert(0, treble_slice)
        chunk_score.insert(0, bass_slice)

        musicxml_file = chunks_dir / f"chunk_{chunk_index:03d}.musicxml"
        chunk_score.write("musicxml", fp=str(musicxml_file), makeNotation=make_notation)

        duration_est = (measure_end - measure_start + 1) * seconds_per_measure
        info = ChunkInfo(
            index=chunk_index,
            total=0,
            measure_start=measure_start,
            measure_end=measure_end,
            duration_est=duration_est,
            musicxml_path=musicxml_file,
        )
        chunk_infos.append(info)
        measure_start = measure_end + 1

    total = len(chunk_infos)
    for info in chunk_infos:
        info.total = total
        sidecar = info.musicxml_path.with_suffix(".json")
        sidecar.write_text(
            json.dumps(
                {
                    "index": info.index,
                    "total": info.total,
                    "measure_start": info.measure_start,
                    "measure_end": info.measure_end,
                    "duration_est": info.duration_est,
                },
                indent=2,
            )
            + "\n",
            encoding="utf-8",
        )

    return chunk_infos


def extract_variable_body(lilypond_text: str, variable_name: str) -> str | None:
    pattern = rf"{re.escape(variable_name)}\s*=\s*\{{"
    match = re.search(pattern, lilypond_text)
    if not match:
        return None

    start = match.end()
    depth = 1
    idx = start
    while idx < len(lilypond_text) and depth > 0:
        char = lilypond_text[idx]
        if char == "{":
            depth += 1
        elif char == "}":
            depth -= 1
        idx += 1

    if depth != 0:
        return None

    return lilypond_text[start : idx - 1].strip()
