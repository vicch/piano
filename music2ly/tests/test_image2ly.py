from pathlib import Path
import music21
import pytest

from image2ly.cli import build_parser, main
from image2ly.models import ImagePaths
from image2ly.pipeline import run_pipeline
from music2ly.config import Config
from music2ly.musicxml import load_multi_grand_staff


def _create_sample_musicxml(path: Path, note_t: str, note_b: str, measure_count: int = 4):
    path.parent.mkdir(parents=True, exist_ok=True)
    score = music21.stream.Score()
    p1 = music21.stream.Part(id="P1")
    p2 = music21.stream.Part(id="P2")
    for i in range(1, measure_count + 1):
        m1 = music21.stream.Measure(number=i)
        m2 = music21.stream.Measure(number=i)
        if i == 1:
            m1.append(music21.clef.TrebleClef())
            m1.append(music21.meter.TimeSignature("4/4"))
            m2.append(music21.clef.BassClef())
            m2.append(music21.meter.TimeSignature("4/4"))
        m1.append(music21.note.Note(note_t, type="whole"))
        m2.append(music21.note.Note(note_b, type="whole"))
        p1.append(m1)
        p2.append(m2)
    score.append(p1)
    score.append(p2)
    score.write("musicxml", fp=str(path))


def test_load_multi_grand_staff(tmp_path):
    p1 = tmp_path / "page1.musicxml"
    p2 = tmp_path / "page2.musicxml"
    _create_sample_musicxml(p1, "C4", "C3", measure_count=4)
    _create_sample_musicxml(p2, "D4", "D3", measure_count=6)

    treble, bass, measure_count = load_multi_grand_staff([p1, p2])
    assert measure_count == 10
    treble_measures = list(treble.getElementsByClass("Measure"))
    bass_measures = list(bass.getElementsByClass("Measure"))
    assert len(treble_measures) == 10
    assert len(bass_measures) == 10
    assert [m.number for m in treble_measures] == list(range(1, 11))
    assert [m.number for m in bass_measures] == list(range(1, 11))
    assert treble_measures[0].notes[0].nameWithOctave == "C4"
    assert treble_measures[3].notes[0].nameWithOctave == "C4"
    assert treble_measures[4].notes[0].nameWithOctave == "D4"
    assert treble_measures[9].notes[0].nameWithOctave == "D4"


def test_cli_parser_defaults():
    parser = build_parser()
    args = parser.parse_args(["Foo Bar"])
    assert args.target == "Foo Bar"
    assert args.title is None
    assert args.omr_backend == "homr"
    assert args.chunk_seconds == 20.0
    assert args.steps == {"all"}


def test_cli_parser_custom_options():
    parser = build_parser()
    args = parser.parse_args([
        "path/to/dir",
        "--title", "Custom Title",
        "--omr-backend", "oemer",
        "--chunk-seconds", "15",
        "--steps", "recognize,musicxml",
        "--resume",
    ])
    assert args.target == "path/to/dir"
    assert args.title == "Custom Title"
    assert args.omr_backend == "oemer"
    assert args.chunk_seconds == 15.0
    assert args.steps == {"recognize", "musicxml"}
    assert args.resume is True


def test_run_pipeline_multi_image_end_to_end(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    work_dir = tmp_path / "output" / "Moonlight"
    work_dir.mkdir(parents=True)
    img1 = work_dir / "1.png"
    img2 = work_dir / "2.png"
    img1.write_text("fake image 1")
    img2.write_text("fake image 2")

    def mock_recognize(image_path, out_musicxml, backend="homr", timeout=1800.0):
        if "1.png" in str(image_path):
            _create_sample_musicxml(out_musicxml, "E4", "E3", measure_count=4)
        else:
            _create_sample_musicxml(out_musicxml, "F4", "F3", measure_count=4)
        return out_musicxml

    monkeypatch.setattr("image2ly.pipeline.recognize", mock_recognize)

    def mock_translate_all_chunks(chunks, config, lilypond_chunks_dir, output_path, **kwargs):
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(f'% Title: {kwargs.get("title")}\n\\score {{ }}\n', encoding="utf-8")
        return output_path

    monkeypatch.setattr("image2ly.pipeline.translate_all_chunks", mock_translate_all_chunks)

    paths, title = ImagePaths.from_target("Moonlight")
    config = Config.load(
        openrouter_api_key="mock",
        chunk_seconds=20.0,
    )

    result_paths = run_pipeline(paths, config, title=title)

    assert (work_dir / "recognized_001.musicxml").exists()
    assert (work_dir / "recognized_002.musicxml").exists()
    assert (work_dir / "recognized.musicxml").exists()
    assert (work_dir / "chunks" / "chunk_001.musicxml").exists()
    assert (work_dir / "Moonlight.ly").exists()
    assert "% Title: Moonlight" in (work_dir / "Moonlight.ly").read_text(encoding="utf-8")


def test_run_pipeline_resume_skips_existing(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    work_dir = tmp_path / "output" / "ResumeTest"
    work_dir.mkdir(parents=True)
    img1 = work_dir / "1.png"
    img2 = work_dir / "2.png"
    img1.write_text("fake image 1")
    img2.write_text("fake image 2")

    # Pre-create recognized_001.musicxml
    _create_sample_musicxml(work_dir / "recognized_001.musicxml", "C4", "C3", measure_count=4)

    recognized_calls = []

    def mock_recognize(image_path, out_musicxml, backend="homr", timeout=1800.0):
        recognized_calls.append(image_path.name)
        _create_sample_musicxml(out_musicxml, "D4", "D3", measure_count=4)
        return out_musicxml

    monkeypatch.setattr("image2ly.pipeline.recognize", mock_recognize)

    def mock_translate_all_chunks(chunks, config, lilypond_chunks_dir, output_path, **kwargs):
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text("% Done\n", encoding="utf-8")
        return output_path

    monkeypatch.setattr("image2ly.pipeline.translate_all_chunks", mock_translate_all_chunks)

    paths, title = ImagePaths.from_target("ResumeTest")
    config = Config.load(openrouter_api_key="mock", chunk_seconds=20.0)

    run_pipeline(paths, config, title=title, resume=True)

    # Page 1 was already recognized, so only page 2 should have been recognized
    assert recognized_calls == ["2.png"]
    assert (work_dir / "recognized.musicxml").exists()
    assert (work_dir / "ResumeTest.ly").exists()


def test_run_pipeline_no_images_raises(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    work_dir = tmp_path / "output" / "Empty"
    work_dir.mkdir(parents=True)

    paths, title = ImagePaths.from_target("Empty")
    config = Config.load(openrouter_api_key="mock")

    with pytest.raises(FileNotFoundError, match="No sheet music images found"):
        run_pipeline(paths, config, title=title)


def test_main_cli(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    work_dir = tmp_path / "output" / "CliSong"
    work_dir.mkdir(parents=True)
    (work_dir / "page1.png").write_text("img")

    def mock_recognize(image_path, out_musicxml, backend="homr", timeout=1800.0):
        _create_sample_musicxml(out_musicxml, "C4", "C3", measure_count=4)
        return out_musicxml

    def mock_translate_all_chunks(chunks, config, lilypond_chunks_dir, output_path, **kwargs):
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text("% Done\n", encoding="utf-8")
        return output_path

    monkeypatch.setattr("image2ly.pipeline.recognize", mock_recognize)
    monkeypatch.setattr("image2ly.pipeline.translate_all_chunks", mock_translate_all_chunks)

    exit_code = main(["CliSong"])
    assert exit_code == 0
    assert (work_dir / "CliSong.ly").exists()
