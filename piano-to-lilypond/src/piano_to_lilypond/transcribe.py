from __future__ import annotations

import json
from pathlib import Path
from typing import Protocol

from piano_to_lilypond.deps import ensure_piano_checkpoint, resolve_torch_device


def desustain_midi(midi_path: Path, window_semitones: int) -> int:
    """Truncate over-sustained notes by clipping each note's offset to the
    onset of the next note within ``window_semitones`` of it.

    The transcription model encodes the sustain pedal by extending note
    durations directly, which makes held chords appear as accumulating
    polyphony in notation (C, CE, CEG). For piano notation we want each
    note to release when the player's hand moves to the next note in the
    same region. ``window_semitones`` approximates that hand reach; 0 disables.
    Returns the number of notes whose duration was shortened.
    """
    if window_semitones <= 0:
        return 0

    import mido

    mid = mido.MidiFile(str(midi_path))

    truncated = 0
    new_tracks: list[mido.MidiTrack] = []

    for track in mid.tracks:
        abs_tick = 0
        non_note: list[tuple[int, mido.Message | mido.MetaMessage]] = []
        notes: list[dict] = []
        active: dict[int, list[tuple[int, int]]] = {}
        for msg in track:
            abs_tick += msg.time
            if msg.type == "note_on" and msg.velocity > 0:
                active.setdefault(msg.note, []).append((abs_tick, msg.velocity))
            elif msg.type == "note_off" or (msg.type == "note_on" and msg.velocity == 0):
                stack = active.get(msg.note)
                if stack:
                    on_tick, vel = stack.pop(0)
                    notes.append(
                        {"pitch": msg.note, "on_tick": on_tick, "off_tick": abs_tick, "vel": vel}
                    )
            else:
                non_note.append((abs_tick, msg.copy()))

        notes.sort(key=lambda n: n["on_tick"])
        for i, n in enumerate(notes):
            for m in notes[i + 1 :]:
                if m["on_tick"] >= n["off_tick"]:
                    break
                if abs(m["pitch"] - n["pitch"]) <= window_semitones:
                    if m["on_tick"] > n["on_tick"]:
                        n["off_tick"] = m["on_tick"]
                        truncated += 1
                    break

        events: list[tuple[int, int, mido.Message | mido.MetaMessage]] = []
        for tick, msg in non_note:
            events.append((tick, 0, msg))
        for n in notes:
            events.append(
                (n["on_tick"], 2, mido.Message("note_on", note=n["pitch"], velocity=n["vel"], time=0))
            )
            events.append(
                (n["off_tick"], 1, mido.Message("note_off", note=n["pitch"], velocity=0, time=0))
            )
        events.sort(key=lambda e: (e[0], e[1]))

        new_track = mido.MidiTrack()
        prev = 0
        for tick, _, msg in events:
            msg.time = max(0, tick - prev)
            new_track.append(msg)
            prev = tick
        new_tracks.append(new_track)

    mid.tracks = new_tracks
    mid.save(str(midi_path))
    return truncated


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
    desustain_window: int = 0,
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
    if desustain_window > 0:
        truncated = desustain_midi(midi_path, desustain_window)
        meta["desustain_window"] = desustain_window
        meta["notes_truncated"] = truncated
    meta_path.parent.mkdir(parents=True, exist_ok=True)
    meta_path.write_text(json.dumps(meta, indent=2) + "\n", encoding="utf-8")
    return meta
