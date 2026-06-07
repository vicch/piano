"""Optical Music Recognition: sheet-music image -> MusicXML.

Wraps an external OMR engine as a subprocess so neither engine becomes a hard
Python dependency of the shared core:

  - homr  (default): transformer OMR, run via ``uvx homr`` (AGPL, external CLI).
  - oemer (fallback): ``pip install`` via the ``image`` extra; MIT licensed.

Both write a MusicXML file; we normalize the output location to ``out_musicxml``.
"""

from __future__ import annotations

import shutil
import subprocess
from pathlib import Path

OMR_BACKENDS = ("homr", "oemer")
_XML_GLOBS = ("*.musicxml", "*.xml", "*.mxl")


class OMRError(RuntimeError):
    pass


def _resolve_command(backend: str) -> list[str]:
    """Return the base argv for an OMR backend, or raise with install guidance."""
    if backend == "homr":
        if shutil.which("homr"):
            return ["homr"]
        if shutil.which("uvx"):
            return ["uvx", "homr"]
        raise OMRError(
            "homr backend needs `homr` or `uvx` on PATH. Install uv "
            "(https://docs.astral.sh/uv/) so `uvx homr` works, or pick --omr-backend oemer."
        )
    if backend == "oemer":
        if shutil.which("oemer"):
            return ["oemer"]
        raise OMRError(
            "oemer backend not found. Install with: uv sync --extra image"
        )
    raise OMRError(f"Unknown OMR backend: {backend!r}. Choose one of: {', '.join(OMR_BACKENDS)}.")


def _existing_xml(directory: Path) -> set[Path]:
    found: set[Path] = set()
    for pattern in _XML_GLOBS:
        found.update(directory.glob(pattern))
    return found


def recognize(
    image_path: Path,
    out_musicxml: Path,
    *,
    backend: str = "homr",
    timeout: float = 1800.0,
) -> Path:
    """Run OMR on ``image_path`` and write the result to ``out_musicxml``.

    OMR engines emit the MusicXML next to the image (homr) or into an output dir
    (oemer); we run with the image's directory as the workspace, detect the
    newly created MusicXML, and move it to ``out_musicxml``.
    """
    if not image_path.exists():
        raise FileNotFoundError(f"Image not found: {image_path}")

    base = _resolve_command(backend)
    work_dir = image_path.parent
    out_musicxml.parent.mkdir(parents=True, exist_ok=True)

    before = _existing_xml(work_dir)

    if backend == "oemer":
        argv = [*base, str(image_path), "-o", str(work_dir)]
    else:  # homr writes alongside the input
        argv = [*base, str(image_path)]

    proc = subprocess.run(
        argv,
        capture_output=True,
        text=True,
        timeout=timeout,
        cwd=str(work_dir),
    )
    if proc.returncode != 0:
        raise OMRError(
            f"{backend} failed (exit {proc.returncode}).\n"
            f"stderr:\n{proc.stderr[-2000:]}"
        )

    produced = sorted(_existing_xml(work_dir) - before, key=lambda p: p.stat().st_mtime)
    if not produced:
        raise OMRError(
            f"{backend} produced no MusicXML in {work_dir}. "
            f"stdout tail:\n{proc.stdout[-1000:]}"
        )

    result = produced[-1]
    if result.resolve() != out_musicxml.resolve():
        shutil.move(str(result), str(out_musicxml))
    return out_musicxml
