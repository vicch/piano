from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path

from dotenv import load_dotenv

DEFAULT_CHUNK_SECONDS = 20
DEFAULT_QUANTIZE_SUBDIV = 4  # subdivisions per beat for tempo-snap (4 = 1/16)

# Transcription sensitivity presets. Each level bundles knobs that together
# control how aggressively the model captures notes from the audio:
#   - onset_threshold:  note-onset confidence (library default 0.3)
#   - frame_threshold:  per-frame note-active probability (library default 0.1)
#   - min_velocity:     drop quantized notes below this MIDI velocity
#   - min_note_ms:      drop quantized notes shorter than this many ms
#   - desustain_window: clip an over-sustained note's offset to the onset of
#                       the next note within N semitones (hand-reach). 0=off.
#                       Reduces accumulating-chord artifact (C → CE → CEG) at
#                       the cost of detail. Tune manually per preset to enable.
# Lower sensitivity = stricter thresholds = fewer (more confident) notes,
# better for YouTube clips with sound effects, voiceovers, or reverb.
SENSITIVITY_PRESETS: dict[str, dict[str, float | int]] = {
    "low": {
        "onset_threshold": 0.6,
        "frame_threshold": 0.4,
        "min_velocity": 30,
        "min_note_ms": 60,
        "desustain_window": 0,
    },
    "medium": {
        "onset_threshold": 0.5,
        "frame_threshold": 0.3,
        "min_velocity": 20,
        "min_note_ms": 40,
        "desustain_window": 0,
    },
    "high": {
        "onset_threshold": 0.35,
        "frame_threshold": 0.15,
        "min_velocity": 5,
        "min_note_ms": 20,
        "desustain_window": 0,
    },
}
DEFAULT_SENSITIVITY = "medium"


@dataclass
class Config:
    quantize_subdiv: int = DEFAULT_QUANTIZE_SUBDIV
    chunk_seconds: float = DEFAULT_CHUNK_SECONDS
    transcription_backend: str = "piano"
    sensitivity: str = DEFAULT_SENSITIVITY
    mscore_bin: str | None = None

    @property
    def onset_threshold(self) -> float:
        return float(SENSITIVITY_PRESETS[self.sensitivity]["onset_threshold"])

    @property
    def frame_threshold(self) -> float:
        return float(SENSITIVITY_PRESETS[self.sensitivity]["frame_threshold"])

    @property
    def min_velocity(self) -> int:
        return int(SENSITIVITY_PRESETS[self.sensitivity]["min_velocity"])

    @property
    def min_note_ms(self) -> int:
        return int(SENSITIVITY_PRESETS[self.sensitivity]["min_note_ms"])

    @property
    def desustain_window(self) -> int:
        return int(SENSITIVITY_PRESETS[self.sensitivity]["desustain_window"])

    @classmethod
    def load(
        cls,
        *,
        env_file: Path | None = None,
        quantize_subdiv: int = DEFAULT_QUANTIZE_SUBDIV,
        chunk_seconds: float = DEFAULT_CHUNK_SECONDS,
        transcription_backend: str = "piano",
        sensitivity: str | None = None,
        mscore_bin: str | None = None,
        **_ignored_kwargs,
    ) -> Config:
        if env_file and env_file.exists():
            load_dotenv(env_file)
        else:
            load_dotenv()

        mscore = mscore_bin or os.environ.get("MSCORE_BIN", "").strip() or None

        sens = (sensitivity or os.environ.get("SENSITIVITY") or DEFAULT_SENSITIVITY).strip()
        if sens not in SENSITIVITY_PRESETS:
            raise ValueError(
                f"Unknown sensitivity {sens!r}. "
                f"Choose one of: {', '.join(SENSITIVITY_PRESETS)}."
            )

        return cls(
            quantize_subdiv=quantize_subdiv,
            chunk_seconds=chunk_seconds,
            transcription_backend=transcription_backend,
            sensitivity=sens,
            mscore_bin=mscore,
        )


def project_root() -> Path:
    """App root when developing from the repo (music2ly/)."""
    return Path(__file__).resolve().parents[2]
