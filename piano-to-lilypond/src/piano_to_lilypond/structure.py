"""MIDI → MusicXML structuring via MuseScore CLI.

MuseScore's MIDI importer does what music21 cannot for piano transcriptions:
real tempo/time-signature inference, hand assignment across two staves,
polyphonic voice splitting, beat-aligned beaming, and tuplet detection.

We invoke the `mscore` binary as a subprocess and let it write MusicXML,
which we then chunk with music21 (which trivially reads MuseScore's output
back in as two parts).
"""

from __future__ import annotations

import os
import shutil
import subprocess
from dataclasses import dataclass
from pathlib import Path

from music21 import converter, stream

DEFAULT_MSCORE_PATHS = (
    "/Applications/MuseScore 4.app/Contents/MacOS/mscore",
    "/Applications/MuseScore 3.app/Contents/MacOS/mscore",
)


class MuseScoreNotFound(RuntimeError):
    pass


def resolve_mscore_binary(override: str | None = None) -> Path:
    if override:
        path = Path(override)
        if not path.exists():
            raise MuseScoreNotFound(f"MSCORE_BIN points to missing file: {override}")
        return path

    env = os.environ.get("MSCORE_BIN", "").strip()
    if env:
        path = Path(env)
        if not path.exists():
            raise MuseScoreNotFound(f"MSCORE_BIN points to missing file: {env}")
        return path

    on_path = shutil.which("mscore") or shutil.which("musescore")
    if on_path:
        return Path(on_path)

    for candidate in DEFAULT_MSCORE_PATHS:
        if Path(candidate).exists():
            return Path(candidate)

    raise MuseScoreNotFound(
        "Could not locate the mscore binary. Install MuseScore "
        "(brew install --cask musescore) or set MSCORE_BIN."
    )


@dataclass
class StructureResult:
    musicxml_path: Path
    measure_count: int
    treble: stream.Part
    bass: stream.Part


def midi_to_musicxml(
    midi_path: Path,
    musicxml_path: Path,
    *,
    mscore_bin: str | None = None,
    timeout: float = 120.0,
) -> StructureResult:
    binary = resolve_mscore_binary(mscore_bin)
    musicxml_path.parent.mkdir(parents=True, exist_ok=True)

    proc = subprocess.run(
        [str(binary), "-o", str(musicxml_path), str(midi_path)],
        capture_output=True,
        text=True,
        timeout=timeout,
    )
    if proc.returncode != 0 or not musicxml_path.exists():
        raise RuntimeError(
            f"mscore failed (exit {proc.returncode}). stderr:\n{proc.stderr[-2000:]}"
        )

    score = converter.parse(str(musicxml_path))
    parts = list(score.parts)
    if not parts:
        raise RuntimeError(f"MuseScore output has no parts: {musicxml_path}")

    # MuseScore exports a single Piano <score-part> with <staves>2</staves>;
    # music21 splits it on read into two Parts. Fall back to duplicating if
    # only a single part is present.
    if len(parts) >= 2:
        treble, bass = parts[0], parts[1]
    else:
        treble = bass = parts[0]

    measure_count = max(
        len(list(treble.getElementsByClass("Measure"))),
        len(list(bass.getElementsByClass("Measure"))),
    )

    return StructureResult(
        musicxml_path=musicxml_path,
        measure_count=measure_count,
        treble=treble,
        bass=bass,
    )
