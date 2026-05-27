from __future__ import annotations

import json
from pathlib import Path
from typing import Protocol

from piano_to_lilypond.deps import ensure_piano_checkpoint, resolve_torch_device


class TranscriptionBackend(Protocol):
    name: str

    def transcribe(self, audio_path: Path, midi_path: Path) -> dict:
        ...


class PianoTranscriptionBackend:
    name = "piano"

    def __init__(
        self,
        device: str | None = None,
        *,
        onset_threshold: float | None = None,
        frame_threshold: float | None = None,
    ) -> None:
        self.device = device or resolve_torch_device()
        self.onset_threshold = onset_threshold
        self.frame_threshold = frame_threshold

    def _make_transcriptor(self, checkpoint_path: str):
        from piano_transcription_inference import PianoTranscription

        t = PianoTranscription(device=self.device, checkpoint_path=checkpoint_path)
        if self.onset_threshold is not None:
            t.onset_threshold = float(self.onset_threshold)
        if self.frame_threshold is not None:
            t.frame_threshold = float(self.frame_threshold)
        return t

    def transcribe(self, audio_path: Path, midi_path: Path) -> dict:
        import librosa
        from piano_transcription_inference import sample_rate

        audio, _ = librosa.load(str(audio_path), sr=sample_rate, mono=True)
        checkpoint_path = str(ensure_piano_checkpoint())
        try:
            transcriptor = self._make_transcriptor(checkpoint_path)
            result = transcriptor.transcribe(audio, str(midi_path))
        except RuntimeError as exc:
            # Some PyTorch ops can be unsupported on MPS depending on version/model.
            # Fall back to CPU to keep the pipeline working.
            if self.device == "mps" and (
                "mps" in str(exc).lower() or "not implemented" in str(exc).lower()
            ):
                self.device = "cpu"
                transcriptor = self._make_transcriptor(checkpoint_path)
                result = transcriptor.transcribe(audio, str(midi_path))
            else:
                raise

        pedal_count = 0
        if result and "est_pedal_events" in result:
            pedal_count = len(result["est_pedal_events"])

        return {
            "backend": self.name,
            "device": self.device,
            "duration_seconds": float(len(audio) / sample_rate),
            "pedal_events": pedal_count,
        }


class BasicPitchBackend:
    name = "basic-pitch"

    def transcribe(self, audio_path: Path, midi_path: Path) -> dict:
        try:
            from basic_pitch.inference import predict
        except ImportError as exc:
            raise ImportError(
                "basic-pitch is not installed. Install with: uv sync --extra transcribe-basic"
            ) from exc

        _, midi_data, _ = predict(str(audio_path))
        midi_path.parent.mkdir(parents=True, exist_ok=True)
        midi_data.write(str(midi_path))

        import librosa

        audio, sr = librosa.load(str(audio_path), sr=None, mono=True)

        return {
            "backend": self.name,
            "device": "cpu",
            "duration_seconds": float(len(audio) / sr),
            "pedal_events": 0,
            "note": "basic-pitch does not transcribe sustain pedal events",
        }


def get_backend(
    name: str,
    device: str | None = None,
    *,
    onset_threshold: float | None = None,
    frame_threshold: float | None = None,
) -> TranscriptionBackend:
    if name == "piano":
        return PianoTranscriptionBackend(
            device=device,
            onset_threshold=onset_threshold,
            frame_threshold=frame_threshold,
        )
    if name == "basic-pitch":
        return BasicPitchBackend()
    raise ValueError(f"Unknown transcription backend: {name!r}. Use 'piano' or 'basic-pitch'.")


def transcribe_audio(
    audio_path: Path,
    midi_path: Path,
    meta_path: Path,
    backend_name: str = "piano",
    *,
    onset_threshold: float | None = None,
    frame_threshold: float | None = None,
) -> dict:
    backend = get_backend(
        backend_name,
        onset_threshold=onset_threshold,
        frame_threshold=frame_threshold,
    )
    meta = backend.transcribe(audio_path, midi_path)
    if onset_threshold is not None:
        meta["onset_threshold"] = onset_threshold
    if frame_threshold is not None:
        meta["frame_threshold"] = frame_threshold
    meta_path.parent.mkdir(parents=True, exist_ok=True)
    meta_path.write_text(json.dumps(meta, indent=2) + "\n", encoding="utf-8")
    return meta
