from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path

from dotenv import load_dotenv

MIDDLE_C_MIDI = 60
DEFAULT_CHUNK_SECONDS = 90
DEFAULT_QUANTIZE_DIVISOR = 16


@dataclass
class Config:
    google_api_key: str
    gemini_model: str
    quantize_divisor: int
    chunk_seconds: float
    transcription_backend: str
    middle_c_midi: int = MIDDLE_C_MIDI

    @classmethod
    def load(
        cls,
        *,
        env_file: Path | None = None,
        quantize_divisor: int = DEFAULT_QUANTIZE_DIVISOR,
        chunk_seconds: float = DEFAULT_CHUNK_SECONDS,
        transcription_backend: str = "piano",
        gemini_model: str | None = None,
    ) -> Config:
        if env_file and env_file.exists():
            load_dotenv(env_file)
        else:
            load_dotenv()

        api_key = os.environ.get("GOOGLE_API_KEY", "").strip()
        model = gemini_model or os.environ.get("GEMINI_MODEL", "gemini-2.0-flash").strip()

        return cls(
            google_api_key=api_key,
            gemini_model=model,
            quantize_divisor=quantize_divisor,
            chunk_seconds=chunk_seconds,
            transcription_backend=transcription_backend,
        )


def project_root() -> Path:
    """App root when developing from the repo (piano-to-lilypond/)."""
    return Path(__file__).resolve().parents[2]


def system_prompt_path() -> Path:
    return Path(__file__).resolve().parent / "prompts" / "lilypond_system.txt"
