# music2ly

Local Python project that turns music into LilyPond sheet music. It ships three CLIs over a shared core (`src/music2ly`, MusicXML structuring and deterministic MusicXML-to-LilyPond translation):

- **video2ly** — YouTube piano performance to LilyPond (audio pipeline).
- **image2ly** — Sheet music image (PNG/JPG) to LilyPond via OMR (image pipeline).
- **scanprep** — Raw low-quality scans/photocopies to clean, OMR-ready pages (adaptive image pre-processing for image2ly).

Install dependencies for the tool(s) you need; heavy dependencies are isolated in extras and imported lazily:

```bash
uv sync --extra video    # video2ly stack (yt-dlp, torch, piano-transcription, librosa, mido)
uv sync --extra image    # image2ly stack (oemer); homr runs externally via `uvx homr`
uv sync --extra scan     # scanprep stack (opencv-python, numpy, pillow)
uv sync --extra all      # all three stacks
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

### scanprep pipeline (adaptive, per page, in place)

1. **Measure** — EXIF orientation, skew (long-line Hough evidence), staff-line spacing (row-ink autocorrelation), background unevenness, isolated-speck noise, dark photocopy borders
2. **Correct geometry** — deskew by the measured angle only when long-line evidence confirms it
3. **Correct tone** — divide out the paper background (morphological max-filter estimate that sees past noteheads and fat title blocks), floored so solid ink never blows out; skipped entirely on already-flat pages
4. **Normalize & restore** — paper-anchored gain to white, speck removal only when specks are measured, then the document-scanner restoration pass: ink-darkening contrast remap (gamma tilt), edge smoothing (melts jaggies/JPEG blocks), subtle unsharp-mask definition, white saturation that erases paper grain (the "clean scan" look), and grain-blob removal driven by an internal Sauvola threshold. All strengths are tweakable constants in `src/scanprep/enhance.py` (`CONTRAST_*`, `EDGE_SMOOTH_SIGMA`, `PAPER_WHITE_MARGIN`, `SHARPEN_*`, `DESPECKLE_AREA_SCALE`), which documents three ready-made combinations (fidelity / balanced / extreme) and how they trade off; disable per run with `--no-contrast` / `--no-whiten` / `--no-sharpen` / `--no-despeckle`
5. **Final page** — the cleaned page keeps the restored grayscale with its anti-aliased edges: solid dark notation on pure white paper, smooth like a professionally scanned document or PDF (hard 1-bit thresholding is what makes edges look crystallized). The internal Sauvola threshold (noise-adaptive k, window scaled to staff spacing) drives QC and despeckling; pass `--binary` for strict pure black-and-white output instead
6. **QC** — per-page metrics and every effective parameter recorded in `scanprep/scanprep.json`, side-by-side `scanprep/preview.png` contact sheet

Processing is in place, mirroring image2ly's flow: for every image in the target directory the raw scan is moved as-is into an `original/` subdirectory (overwriting any same-named file there) and the cleaned page is written as `<stem>.png`, so `image2ly <dir>` afterwards picks up exactly the cleaned pages in natural page order. Re-runs are idempotent: a raw already in `original/` is always the raw source and is never moved twice. Legacy `1 (original).jpg` backups from older scanprep runs are still recognized and migrate into `original/`.

All kernel sizes derive from the measured staff spacing, so any scan resolution, exposure, or paper tone converges on the same output quality; nothing assumes one fixed scan profile. The restored page (`<stem>.png`) — dark notation, white paper, smooth anti-aliased edges — is the archival/OMR output; staff lines are content and are never removed.

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

Only top-level images are listed (subdirectories like `original/` are never scanned); legacy files whose stem ends with `(original)` (old scanprep backups) are ignored when listing pages.

### scanprep

Cleans raw, low-quality sheet-music scans (photocopies, phone photos, gray JPEGs) into uniform, OMR-ready pages, then feeds image2ly. Put the raw scans in a directory under `output/` (or anywhere) and pass the directory name, exactly like image2ly:

```bash
# Raw scans sit in output/Innocent/ (Innocent 1.jpg, Innocent 2.jpg, ...)
uv run scanprep "Innocent"

# Afterwards run OMR on the cleaned pages — same directory, same title
uv run image2ly "Innocent"
```

Processing is in place: each raw `Innocent 1.jpg` is moved as-is into `original/Innocent 1.jpg` and the cleaned page is written as `Innocent 1.png` with the original stem, so image2ly run on the same directory picks up exactly the cleaned pages in natural page order. Re-runs re-process from the `original/` raws and never move twice; with `--resume` already-cleaned pages are skipped entirely.

A single image file works too (it is copied into `output/<title>/` like image2ly does, then cleaned in place):

```bash
uv run scanprep "path/to/Innocent 1.jpg"
```

Options (defaults adapt per page; these override the automatic decisions):

- `--title`, `-t` — Song title override (default: directory or file name).
- `--no-deskew` / `--max-skew 3.0` — Skip rotation, or trust skew estimates up to N degrees.
- `--background-method {morph,gaussian}` — Paper-background estimator (default: `morph`, robust under fat title blocks).
- `--background-scale 4` — Background window size in staff-spacing units; raise it if the report warns about residual unevenness.
- `--paper-target 245` — Target paper brightness after correction.
- `--no-contrast` / `--no-whiten` / `--no-sharpen` / `--no-despeckle` — Skip restoration stages individually (strengths are constants in `src/scanprep/enhance.py`).
- `--binary` — Strict pure black-and-white output instead of the default smooth restored grayscale.
- `--sauvola-k 0.15` — Pin Sauvola sensitivity (default: auto — 0.15, or 0.22 on speckled pages).
- `--sauvola-window-scale 5` — Sauvola window in staff-spacing units.
- `--denoise {auto,on,off}` — Isolated-speck removal (default: `auto`, applied only when specks are measured).
- `--no-preview` — Skip the side-by-side contact sheet.
- `--resume` — Skip pages already cleaned in place (raw backed up + page exists).

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
├── 1.png                       # Restored page masters, original stems (scanprep)
├── original/                   # Preserved raw scans, original filenames (scanprep)
│   └── 1.jpg
├── scanprep/                   # scanprep QC artifacts
│   ├── preview.png             # Original | clean contact sheet
│   └── scanprep.json           # Per-page metrics + effective parameters
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
