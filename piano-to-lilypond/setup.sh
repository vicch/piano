#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$ROOT"

if ! command -v ffmpeg >/dev/null 2>&1; then
  echo "Error: ffmpeg is required but not found on PATH." >&2
  echo "Install with: brew install ffmpeg  (macOS)  or  apt install ffmpeg  (Debian/Ubuntu)" >&2
  exit 1
fi

if ! command -v uv >/dev/null 2>&1; then
  echo "uv not found; installing via official installer..."
  curl -LsSf https://astral.sh/uv/install.sh | sh
  export PATH="$HOME/.local/bin:$PATH"
  if ! command -v uv >/dev/null 2>&1; then
    echo "Error: uv installation failed. Install manually: https://docs.astral.sh/uv/" >&2
    exit 1
  fi
fi

# Core deps only (piano backend). basic-pitch optional extra pulls tensorflow-macos
# which does not support Python 3.12 on Apple Silicon — install separately if needed.
uv sync --extra dev

if [[ ! -f .env ]]; then
  cp .env.example .env
  echo "Created .env from .env.example — set GOOGLE_API_KEY before running step 4."
fi

echo ""
echo "Setup complete."
echo "  1. Edit .env and set GOOGLE_API_KEY"
echo "  2. Run: uv run piano-to-lilypond \"https://youtube.com/watch?v=...\" --title \"Song Title\""
