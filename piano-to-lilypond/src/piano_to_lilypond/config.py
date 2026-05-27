from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path

from dotenv import load_dotenv

DEFAULT_CHUNK_SECONDS = 20
DEFAULT_QUANTIZE_SUBDIV = 4  # subdivisions per beat for tempo-snap (4 = 1/16)

# Transcription sensitivity presets. Each level bundles four knobs that
# together control how aggressively the model captures notes from the audio:
#   - onset_threshold:  note-onset confidence (library default 0.3)
#   - frame_threshold:  per-frame note-active probability (library default 0.1)
#   - min_velocity:     drop quantized notes below this MIDI velocity
#   - min_note_ms:      drop quantized notes shorter than this many ms
# Lower sensitivity = stricter thresholds = fewer (more confident) notes,
# better for YouTube clips with sound effects, voiceovers, or reverb.
SENSITIVITY_PRESETS: dict[str, dict[str, float | int]] = {
    "low": {
        "onset_threshold": 0.6,
        "frame_threshold": 0.4,
        "min_velocity": 30,
        "min_note_ms": 60,
    },
    "medium": {
        "onset_threshold": 0.5,
        "frame_threshold": 0.3,
        "min_velocity": 20,
        "min_note_ms": 40,
    },
    "high": {
        "onset_threshold": 0.35,
        "frame_threshold": 0.15,
        "min_velocity": 5,
        "min_note_ms": 20,
    },
}
DEFAULT_SENSITIVITY = "medium"
DEFAULT_LMSTUDIO_BASE_URL = "http://127.0.0.1:1234/v1"
DEFAULT_LMSTUDIO_MODEL = "google/gemma-4-31b"
DEFAULT_LLM_BACKEND = "lmstudio"


@dataclass
class Config:
    google_api_key: str
    gemini_model: str
    quantize_subdiv: int
    chunk_seconds: float
    transcription_backend: str
    sensitivity: str = DEFAULT_SENSITIVITY
    llm_backend: str = DEFAULT_LLM_BACKEND
    lmstudio_base_url: str = DEFAULT_LMSTUDIO_BASE_URL
    lmstudio_model: str = DEFAULT_LMSTUDIO_MODEL
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

    @classmethod
    def load(
        cls,
        *,
        env_file: Path | None = None,
        quantize_subdiv: int = DEFAULT_QUANTIZE_SUBDIV,
        chunk_seconds: float = DEFAULT_CHUNK_SECONDS,
        transcription_backend: str = "piano",
        gemini_model: str | None = None,
        llm_backend: str | None = None,
        lmstudio_base_url: str | None = None,
        lmstudio_model: str | None = None,
        sensitivity: str | None = None,
    ) -> Config:
        if env_file and env_file.exists():
            load_dotenv(env_file)
        else:
            load_dotenv()

        api_key = os.environ.get("GOOGLE_API_KEY", "").strip()
        model = gemini_model or os.environ.get("GEMINI_MODEL", "gemini-2.0-flash").strip()
        mscore = os.environ.get("MSCORE_BIN", "").strip() or None

        backend = (llm_backend or os.environ.get("LLM_BACKEND") or DEFAULT_LLM_BACKEND).strip()
        base_url = (
            lmstudio_base_url
            or os.environ.get("LMSTUDIO_BASE_URL")
            or DEFAULT_LMSTUDIO_BASE_URL
        ).rstrip("/")
        lm_model = (
            lmstudio_model
            or os.environ.get("LMSTUDIO_MODEL")
            or DEFAULT_LMSTUDIO_MODEL
        ).strip()

        sens = (sensitivity or os.environ.get("SENSITIVITY") or DEFAULT_SENSITIVITY).strip()
        if sens not in SENSITIVITY_PRESETS:
            raise ValueError(
                f"Unknown sensitivity {sens!r}. "
                f"Choose one of: {', '.join(SENSITIVITY_PRESETS)}."
            )

        return cls(
            google_api_key=api_key,
            gemini_model=model,
            quantize_subdiv=quantize_subdiv,
            chunk_seconds=chunk_seconds,
            transcription_backend=transcription_backend,
            sensitivity=sens,
            llm_backend=backend,
            lmstudio_base_url=base_url,
            lmstudio_model=lm_model,
            mscore_bin=mscore,
        )


def project_root() -> Path:
    """App root when developing from the repo (piano-to-lilypond/)."""
    return Path(__file__).resolve().parents[2]


def system_prompt_path() -> Path:
    return Path(__file__).resolve().parent / "prompts" / "lilypond_system.txt"
