from __future__ import annotations

import shutil
import sys
from pathlib import Path
from urllib.request import urlretrieve


class DependencyError(RuntimeError):
    pass


def check_ffmpeg() -> str:
    ffmpeg = shutil.which("ffmpeg")
    if ffmpeg is None:
        raise DependencyError(
            "ffmpeg is required but not found on PATH.\n"
            "Install with: brew install ffmpeg  (macOS)  or  apt install ffmpeg  (Debian/Ubuntu)"
        )
    return ffmpeg


def resolve_torch_device() -> str:
    try:
        import torch
    except ImportError as exc:
        raise DependencyError(
            "PyTorch is required for transcription. Install with: uv sync"
        ) from exc

    if torch.cuda.is_available():
        name = torch.cuda.get_device_name(0)
        print(f"Using GPU: {name}", file=sys.stderr)
        return "cuda"

    # Apple Silicon acceleration (Metal Performance Shaders)
    mps_backend = getattr(torch.backends, "mps", None)
    if mps_backend is not None and mps_backend.is_available():
        print("Using Apple GPU (MPS) for transcription.", file=sys.stderr)
        return "mps"

    print("CUDA/MPS not available; using CPU for transcription.", file=sys.stderr)
    return "cpu"


PIANO_CHECKPOINT_URL = (
    "https://zenodo.org/record/4034264/files/"
    "CRNN_note_F1%3D0.9677_pedal_F1%3D0.9186.pth?download=1"
)
PIANO_CHECKPOINT_MIN_BYTES = int(1.6e8)


def default_piano_checkpoint_path() -> Path:
    return (
        Path.home()
        / "piano_transcription_inference_data"
        / "note_F1=0.9677_pedal_F1=0.9186.pth"
    )


def _download_progress(block_num: int, block_size: int, total_size: int) -> None:
    if total_size <= 0:
        return
    downloaded = block_num * block_size
    percent = min(100, downloaded * 100 // total_size)
    print(f"\rDownloading model checkpoint… {percent}%", end="", file=sys.stderr, flush=True)


def ensure_piano_checkpoint(checkpoint_path: Path | None = None) -> Path:
    """Download the piano-transcription-inference weights (macOS has no wget by default)."""
    path = checkpoint_path or default_piano_checkpoint_path()
    if path.exists() and path.stat().st_size >= PIANO_CHECKPOINT_MIN_BYTES:
        return path

    path.parent.mkdir(parents=True, exist_ok=True)
    print(f"Checkpoint path: {path}", file=sys.stderr)
    print("Total size: ~165 MB (one-time download)", file=sys.stderr)

    tmp_path = path.with_suffix(path.suffix + ".part")
    try:
        urlretrieve(PIANO_CHECKPOINT_URL, tmp_path, reporthook=_download_progress)
        print(file=sys.stderr)
        tmp_path.replace(path)
    except Exception:
        if tmp_path.exists():
            tmp_path.unlink()
        raise

    if not path.exists() or path.stat().st_size < PIANO_CHECKPOINT_MIN_BYTES:
        raise DependencyError(
            f"Checkpoint download failed or file too small: {path}\n"
            f"Try manually: curl -L -o '{path}' '{PIANO_CHECKPOINT_URL}'"
        )

    return path
