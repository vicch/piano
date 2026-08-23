# music2ly

Local Python project that turns music into LilyPond sheet music. It ships two CLIs over a shared core (`src/music2ly`, MusicXML chunking and LLM MusicXML-to-LilyPond translation):

- **video2ly** — YouTube piano performance to LilyPond (audio pipeline).
- **image2ly** — Sheet music image (PNG/JPG) to LilyPond via OMR (image pipeline).

Install dependencies for the tool(s) you need; heavy dependencies are isolated in extras and imported lazily:

```bash
uv sync --extra video    # video2ly stack (yt-dlp, torch, piano-transcription, librosa, mido)
uv sync --extra image    # image2ly stack (oemer); homr runs externally via `uvx homr`
uv sync --extra all      # both video2ly and image2ly stacks
uv sync --extra dev      # development and test dependencies (pytest)
```

## Pipelines

### video2ly pipeline (5 steps)

1. **Extract (`extract`)** — `yt-dlp` + `ffmpeg` → `audio.wav`
2. **Transcribe (`transcribe`)** — `piano-transcription-inference` (default, includes sustain pedal) or `basic-pitch` → `transcription.mid`
3. **Quantize (`quantize`)** — `librosa` beat tracking snaps note onsets/offsets to beat grid and filters short/quiet ghost notes → `transcription.quantized.mid`
4. **Structure (`musicxml`)** — MuseScore CLI (`mscore`) assigns hands, voices, tuplets, and export grand-staff MusicXML (`structured.musicxml`), then `music21` splits it into manageable chunks in `chunks/`
5. **Engrave (`lilypond`)** — LLM (OpenRouter or local LM-Studio via `httpx`) translates each chunk to LilyPond notation (`lilypond_chunks/`) and merges into the final score `<title>.ly`

### image2ly pipeline (3 steps)

1. **Recognize (`recognize`)** — Optical Music Recognition via `homr` (default, run via `uvx homr`) or `oemer` → `recognized.musicxml`
2. **Structure (`musicxml`)** — `music21` parses grand-staff MusicXML and splits it into chunks in `chunks/`
3. **Engrave (`lilypond`)** — LLM translates MusicXML chunks to LilyPond (`lilypond_chunks/`) and merges into `<title>.ly`

## Prerequisites

| Dependency | Required for | Install |
|------------|--------------|---------|
| [uv](https://docs.astral.sh/uv/) | Python environment & package management | `curl -LsSf https://astral.sh/uv/install.sh \| sh` or `./setup.sh` |
| [ffmpeg](https://ffmpeg.org/) | Audio extraction (`video2ly`) | `brew install ffmpeg` / `apt install ffmpeg` / `winget install Gyan.FFmpeg` |
| [MuseScore](https://musescore.org/) | MIDI → MusicXML structuring (`video2ly`) | `brew install --cask musescore` / `apt install musescore3` / set `MSCORE_BIN` |
| [OPENROUTER_API_KEY](https://openrouter.ai/keys) | LLM LilyPond translation (step `lilypond`) | Set in `.env` (or use local LM-Studio backend) |
| [homr](https://github.com/homr-omr/homr) / `uvx` | OMR recognition (`image2ly` default) | Handled automatically via `uvx homr` when `uv` is installed |
| NVIDIA CUDA / Apple Silicon (MPS) | GPU acceleration for audio transcription | PyTorch uses CUDA or Apple Silicon Metal (MPS) when available |
| [LilyPond](https://lilypond.org/) (optional) | Compile generated `.ly` → PDF | `brew install lilypond` / `apt install lilypond` / Windows installer |

## Setup

### macOS / Linux

```bash
cd music2ly
chmod +x setup.sh
./setup.sh
```

### Manual / Windows

```bash
cd music2ly
uv sync --extra video --extra dev   # or --extra all
cp .env.example .env               # on Windows: copy .env.example .env
```

Edit `.env` and set `OPENROUTER_API_KEY`:

```env
OPENROUTER_API_KEY=your_api_key_here
OPENROUTER_MODEL=google/gemini-2.0-flash-001
```

## Usage

### video2ly

Full pipeline (creates artifacts and sheet music under `output/<title>/`):

```bash
uv run video2ly "https://www.youtube.com/watch?v=VIDEO_ID" \
  --title "My Song Title"
```

Resume after interruption (skips steps whose artifacts already exist):

```bash
uv run video2ly "https://www.youtube.com/watch?v=VIDEO_ID" \
  --title "My Song Title" \
  --resume
```

Run specific pipeline steps:

```bash
uv run video2ly "URL" --title "My Song Title" --steps extract
uv run video2ly "URL" --title "My Song Title" --steps transcribe
uv run video2ly "URL" --title "My Song Title" --steps quantize
uv run video2ly "URL" --title "My Song Title" --steps musicxml
uv run video2ly "URL" --title "My Song Title" --steps lilypond
# Or comma-separated combinations:
uv run video2ly "URL" --title "My Song Title" --steps quantize,musicxml
```

Key options:

- `--sensitivity {low,medium,high}` — transcription sensitivity preset (default: `medium`). Lower sensitivity is stricter and reduces ghost notes from audio effects/reverb; higher sensitivity captures quieter/shorter notes.
- `--quantize-subdiv {2,4,8}` — beat-snap grid subdivisions per beat (2=8th, 4=16th [default], 8=32nd).
- `--chunk-seconds 20` — target duration in seconds per MusicXML chunk for LLM translation (default: 20).
- `--transcription-backend {piano,basic-pitch}` — default `piano` (PyTorch CRNN model with sustain pedal detection).
- `--llm-backend {openrouter,lmstudio}` — default `openrouter` (or local `lmstudio`).
- `--openrouter-model MODEL` — override OpenRouter model (default: `google/gemini-2.0-flash-001`).
- `--lmstudio-model MODEL` — override LM-Studio model (default: `google/gemma-4-31b`).
- `--lmstudio-base-url URL` — override LM-Studio base URL (default: `http://127.0.0.1:1234/v1`).
- `--env-file PATH` — path to custom `.env` file.

### image2ly

Converts a sheet music image (PNG or JPG) to LilyPond via OMR and LLM translation:

```bash
# Install image extra if using oemer fallback (homr runs via uvx):
uv sync --extra image

uv run image2ly path/to/score.png --title "My Song Title"
```

Resume and step execution:

```bash
uv run image2ly path/to/score.png --title "My Song Title" --resume
uv run image2ly path/to/score.png --title "My Song Title" --steps recognize
uv run image2ly path/to/score.png --title "My Song Title" --steps musicxml
uv run image2ly path/to/score.png --title "My Song Title" --steps lilypond
```

OMR Backends (`--omr-backend`, default `homr`):

- `homr` — Transformer-based OMR executed via `uvx homr` (AGPL, requires `uv` on PATH). Best recognition accuracy for typeset piano/grand-staff scores.
- `oemer` — Installed via `uv sync --extra image` (MIT). Fallback engine.

*Note: OMR backends are designed for typeset sheet music; handwritten scores are not supported.*

## Artifact Output Structure

All artifacts for a run are organized in `output/<title>/`:

```text
output/My-Song-Title/
├── audio.wav                           # [video2ly] Extracted WAV audio
├── transcription.mid                   # [video2ly] Raw transcribed MIDI
├── transcription.meta.json             # [video2ly] Transcription metadata
├── transcription.quantized.mid         # [video2ly] Tempo-snapped quantized MIDI
├── transcription.quantized.meta.json   # [video2ly] Quantization metadata
├── source.png                          # [image2ly] Preserved source image copy
├── structured.musicxml                 # [video2ly] MuseScore structured MusicXML
├── recognized.musicxml                 # [image2ly] OMR recognized MusicXML
├── chunks/                             # MusicXML chunk slices and metadata
│   ├── chunk_001.musicxml
│   └── chunk_001.json
├── lilypond_chunks/                    # Raw and parsed LLM LilyPond translations
│   ├── chunk_001.raw.txt
│   └── chunk_001.ly
└── My-Song-Title.ly                    # Final merged LilyPond score
```

## First run: model download

When using the default `piano` transcription backend, PyTorch automatically downloads the **~165 MB** CRNN model checkpoint on first run to:

`~/piano_transcription_inference_data/note_F1=0.9677_pedal_F1=0.9186.pth`

Downloads use Python's standard library (`urllib.request`) and work cross-platform without external tools like `wget`.

## Compiling to PDF

Once the `.ly` file is generated, compile it with LilyPond (scores automatically include `template/base.ly` formatting):

```bash
lilypond output/My-Song-Title/My-Song-Title.ly
```

## Tests

Run the test suite with `pytest`:

```bash
uv run pytest
```

## Optional: basic-pitch backend

A lighter audio transcription backend without sustain pedal detection. **Not included in default setup** because `basic-pitch` can pull `tensorflow-macos` wheels that are restricted to Python 3.10–3.11 on macOS:

```bash
uv sync --extra transcribe-basic
uv run video2ly "URL" --title "Song Title" --transcription-backend basic-pitch
```

## Legal

Downloading YouTube content may violate YouTube's Terms of Service. Use only for personal or educational purposes on material you have rights to transcribe.

