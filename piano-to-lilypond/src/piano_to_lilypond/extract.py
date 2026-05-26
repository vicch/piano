from __future__ import annotations

from pathlib import Path

import yt_dlp

from piano_to_lilypond.deps import check_ffmpeg


def extract_audio(youtube_url: str, output_path: Path) -> Path:
    check_ffmpeg()
    output_path.parent.mkdir(parents=True, exist_ok=True)
    stem = output_path.with_suffix("")

    ydl_opts = {
        "format": "bestaudio/best",
        "outtmpl": str(stem),
        "quiet": False,
        "no_warnings": False,
        "postprocessors": [
            {
                "key": "FFmpegExtractAudio",
                "preferredcodec": "wav",
            }
        ],
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([youtube_url])

    if not output_path.exists():
        candidates = list(output_path.parent.glob(f"{stem.name}.*"))
        wav_candidates = [p for p in candidates if p.suffix.lower() == ".wav"]
        if wav_candidates:
            wav_candidates[0].rename(output_path)
        else:
            raise FileNotFoundError(f"Expected audio at {output_path} after yt-dlp extraction")

    return output_path
