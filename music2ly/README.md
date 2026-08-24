# music2ly

Local Python project that turns music into LilyPond sheet music. It ships two CLIs over a shared core (`src/music2ly`, MusicXML structuring and deterministic MusicXML-to-LilyPond translation):

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
5. **Engrave (`lilypond`)** — Deterministic syntax engine translates MusicXML into clean, template-conforming LilyPond notation (`<title>.ly`)

### image2ly pipeline (3 steps)

1. **Recognize (`recognize`)** — Optical Music Recognition on all sheet images in the directory in natural page order via `homr` (default, run via `uvx homr`) or `oemer` → `recognized_001.musicxml`, `recognized_002.musicxml`, ... and merged `recognized.musicxml`
2. **Structure (`musicxml`)** — `music21` parses grand-staff MusicXML across all pages into continuous measures and splits it into chunks in `chunks/`
3. **Engrave (`lilypond`)** — Deterministic syntax engine translates MusicXML into clean, template-conforming LilyPond notation (`<title>.ly`)

## Prerequisites

| Dependency | Required for | Install |
|------------|--------------|---------|
| [uv](https://docs.astral.sh/uv/) | Python environment & package management | `curl -LsSf https://astral.sh/uv/install.sh \| sh` or `./setup.sh` |
| [ffmpeg](https://ffmpeg.org/) | Audio extraction (`video2ly`) | `brew install ffmpeg` / `apt install ffmpeg` / `winget install Gyan.FFmpeg` |
| [MuseScore](https://musescore.org/) | MIDI → MusicXML structuring (`video2ly`) | `brew install --cask musescore` / `apt install musescore3` / set `MSCORE_BIN` |
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
- `--chunk-seconds 20` — target duration in seconds per MusicXML chunk (default: 20).
- `--transcription-backend {piano,basic-pitch}` — default `piano` (PyTorch CRNN model with sustain pedal detection).
- `--env-file PATH` — path to custom `.env` file.

### image2ly

Converts sheet music images (PNG or JPG) in a directory to LilyPond via OMR and deterministic translation. Supports single or multi-page scores:

Place your page images (e.g. `1.png`, `2.png` or `page1.png`, `page2.png`) inside `output/<title>/` and pass the song title / directory name:

```bash
# Process all page images inside output/Moonlight Sonata/
uv run image2ly "Moonlight Sonata"
```

You can also pass an explicit directory or a single image file directly:

```bash
uv run image2ly path/to/sheet/images/
uv run image2ly path/to/single_page.png --title "Song Title"
```

Resume after interruption (skips already recognized pages and generated steps):

```bash
uv run image2ly "Für Elise" --resume
```

Run specific steps:

```bash
uv run image2ly "Für Elise" --steps recognize
uv run image2ly "Für Elise" --steps musicxml
uv run image2ly "Für Elise" --steps lilypond
uv run image2ly "Für Elise" --steps musicxml,lilypond
```

Options:

- `--omr-backend {homr,oemer}` — OMR engine (default: `homr` via `uvx homr`).
- `--title`, `-t` — Song title override (default: directory name).
- `--chunk-seconds 20` — Target chunk duration in seconds (default: 20).
- `--steps` — Comma-separated steps (`recognize,musicxml,lilypond` or `all`).
- `--resume` — Skip steps whose artifacts already exist.

## Output Artifacts

```
output/<title>/
├── <title>.ly                  # Final merged LilyPond score (matches template/base.ly)
├── audio.wav                   # Extracted audio (video2ly)
├── transcription.mid           # Raw transcribed MIDI with sustain pedal (video2ly)
├── transcription.quantized.mid # Beat-snapped MIDI (video2ly)
├── structured.musicxml         # Structured MusicXML from MuseScore (video2ly)
├── recognized_001.musicxml     # Page 1 OMR output (image2ly)
├── recognized_002.musicxml     # Page 2 OMR output (image2ly)
├── recognized.musicxml         # Merged grand-staff MusicXML (image2ly)
├── chunks/                     # Segmented MusicXML chunks
│   ├── chunk_001.musicxml
│   └── chunk_001.json
└── lilypond_chunks/            # Deterministically engraved LilyPond chunks
    ├── chunk_001.ly
    └── ...
```

## Testing

```bash
cd music2ly
uv run pytest
```
