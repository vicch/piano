# Piano-to-LilyPond Pipeline

Local Python CLI that downloads a YouTube piano performance, transcribes it to MIDI, structures it as MusicXML, and uses Gemini to generate LilyPond sheet music.

## Pipeline

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
cd piano-to-lilypond
chmod +x setup.sh
./setup.sh
```

Edit `.env` and set `GOOGLE_API_KEY`.

## Usage

Full pipeline:

```bash
uv run piano-to-lilypond "https://www.youtube.com/watch?v=VIDEO_ID" \
  --output out/score.ly \
  --work-dir work/run1
```

Run individual steps:

```bash
uv run piano-to-lilypond "URL" --steps extract
uv run piano-to-lilypond "URL" --steps transcribe --work-dir work/run1
uv run piano-to-lilypond "URL" --steps musicxml --work-dir work/run1
uv run piano-to-lilypond "URL" --steps lilypond --work-dir work/run1 --output out/score.ly
```

Resume after interruption (skip existing artifacts):

```bash
uv run piano-to-lilypond "URL" --work-dir work/run1 --output out/score.ly --resume
```

Options:

- `--quantize {8,16}` — grid for timing cleanup (default: 16)
- `--chunk-seconds 90` — MusicXML chunk size for LLM context
- `--transcription-backend {piano,basic-pitch}` — default `piano` (includes sustain pedal)
- `--gemini-model MODEL` — override `GEMINI_MODEL` in `.env`

Compile output (requires LilyPond installed):

```bash
lilypond out/score.ly
```

## First run: model download

The `piano` backend downloads a **~165 MB** checkpoint once to:

`~/piano_transcription_inference_data/note_F1=0.9677_pedal_F1=0.9186.pth`

The pipeline uses Python’s built-in downloader (no `wget` required on macOS).

## Smoke test

Use a short solo piano clip (under 2 minutes):

```bash
uv run piano-to-lilypond "https://www.youtube.com/watch?v=SHORT_PIANO_CLIP" \
  --output out/test.ly \
  --work-dir work/smoke
lilypond out/test.ly   # optional
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
uv run piano-to-lilypond "URL" --transcription-backend basic-pitch
```

The default `piano` backend (PyTorch) works on Python 3.12 and includes sustain-pedal transcription.
