from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


@dataclass
class ChunkInfo:
    index: int
    total: int
    measure_start: int
    measure_end: int
    duration_est: float
    musicxml_path: Path


@dataclass
class PipelinePaths:
    work_dir: Path
    audio_path: Path
    midi_path: Path
    musicxml_path: Path
    chunks_dir: Path
    lilypond_chunks_dir: Path
    output_path: Path
    transcription_meta_path: Path

    @classmethod
    def from_work_dir(cls, work_dir: Path, output_path: Path) -> PipelinePaths:
        work_dir.mkdir(parents=True, exist_ok=True)
        chunks_dir = work_dir / "chunks"
        lilypond_chunks_dir = work_dir / "lilypond_chunks"
        return cls(
            work_dir=work_dir,
            audio_path=work_dir / "audio.wav",
            midi_path=work_dir / "transcription.mid",
            musicxml_path=work_dir / "structured.musicxml",
            chunks_dir=chunks_dir,
            lilypond_chunks_dir=lilypond_chunks_dir,
            output_path=output_path,
            transcription_meta_path=work_dir / "transcription.meta.json",
        )
