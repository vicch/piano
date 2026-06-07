# music2ly

Local Python project that turns music into LilyPond sheet music. It ships two CLIs over a shared core (`src/music2ly`, the MusicXML chunking + LLM MusicXML-to-LilyPond translation):

- **video2ly** — YouTube piano performance to LilyPond (audio path). Working.
- **image2ly** — image of sheet music to LilyPond via OMR (image path). Placeholder, not yet implemented.

Install only what a tool needs; heavy deps are isolated in extras and imported lazily:

```bash
uv sync --extra video    # video2ly stack (yt-dlp, torch, piano-transcription)
uv sync --extra image    # image2ly stack (oemer); homr runs externally via `uvx homr`
uv sync --extra all      # both
```

## video2ly pipeline

1. **Extract** — `yt-dlp` + `ffmpeg` → WAV
2. **Transcribe** — `piano-transcription-inference` (default) or `basic-pitch` → MIDI
3. **Structure** — `music21` quantize, RH/LH split at Middle C, export MusicXML chunks
4. **Engrave** — `google-genai` (Gemini) → merged `.ly` file

## Prerequisites

| Dependency | Required for | Install |
|------------|--------------|---------|
| [ffmpeg](https://ffmpeg.org/) | Audio extraction | `brew install ffmpeg` / `apt install ffmpeg` |
| [uv](https://docs.astral.sh/uv/) | Python deps | `./setup.sh` installs if missing |
| [GOOGLE_API_KEY](https://aistudio.google.com/apikey) | Step 4 (LilyPond) | Set in `.env` |
| NVIDIA CUDA (optional) | Faster transcription on Linux/Windows | PyTorch uses CUDA when available |
| Apple Silicon (M5, etc.) | Faster transcription on Mac | PyTorch uses **MPS** (Metal GPU) when available |
| [LilyPond](https://lilypond.org/) (optional) | Compile `.ly` → PDF | Not required to generate `.ly` |

## Setup

```bash
cd music2ly
chmod +x setup.sh
./setup.sh
```

Edit `.env` and set `GOOGLE_API_KEY`.

## Usage

Full pipeline (`--title` uses `output/<title>/` for all artifacts and the `.ly` file):

```bash
uv run video2ly "https://www.youtube.com/watch?v=VIDEO_ID" \
  --title "My Song Title"
```

Resume after interruption (skip existing artifacts):

```bash
uv run video2ly "https://www.youtube.com/watch?v=VIDEO_ID" \
  --title "My Song Title" \
  --resume
```

Run individual steps (same `--title` for paths):

```bash
uv run video2ly "URL" --title "My Song Title" --steps extract
uv run video2ly "URL" --title "My Song Title" --steps transcribe
uv run video2ly "URL" --title "My Song Title" --steps musicxml
uv run video2ly "URL" --title "My Song Title" --steps lilypond
```

Options:

- `--quantize {8,16}` — grid for timing cleanup (default: 16)
- `--chunk-seconds 90` — MusicXML chunk size for LLM context
- `--transcription-backend {piano,basic-pitch}` — default `piano` (includes sustain pedal)
- `--gemini-model MODEL` — override `GEMINI_MODEL` in `.env`

Compile output (requires LilyPond installed):

```bash
lilypond output/My-Song-Title/My-Song-Title.ly
```

## First run: model download

The `piano` backend downloads a **~165 MB** checkpoint once to:

`~/piano_transcription_inference_data/note_F1=0.9677_pedal_F1=0.9186.pth`

The pipeline uses Python’s built-in downloader (no `wget` required on macOS).

## Smoke test

Use a short solo piano clip (under 2 minutes):

```bash
uv run video2ly "https://www.youtube.com/watch?v=SHORT_PIANO_CLIP" \
  --title "Smoke Test"
lilypond output/Smoke-Test/Smoke-Test.ly   # optional
```

## Tests

```bash
uv run pytest
```

## Legal

Downloading YouTube content may violate YouTube's Terms of Service. Use only for personal or educational purposes on material you have rights to transcribe.

## Optional: basic-pitch backend

Lighter install without sustain-pedal detection. **Not included in `./setup.sh`** because `basic-pitch` can pull `tensorflow-macos`, which only supports Python 3.10–3.11 on macOS. If you need this backend, use a 3.11 venv or Linux:

```bash
uv sync --extra transcribe-basic   # may fail on macOS + Python 3.12
uv run video2ly "URL" --transcription-backend basic-pitch
```

The default `piano` backend (PyTorch) works on Python 3.12 and includes sustain-pedal transcription.
