from pathlib import Path
import pytest

from image2ly.models import (
    ImagePaths,
    find_image_files,
    natural_sort_key,
)
from music2ly.models import PipelinePaths, slugify_title


def test_slugify_title():
    assert slugify_title("My Song") == "My Song"
    assert slugify_title("It's A Small World") == "It's A Small World"
    assert slugify_title("  Passacaglia  ") == "Passacaglia"
    assert slugify_title("看见") == "看见"
    assert slugify_title('A/B: "C"?') == "AB C"


def test_slugify_title_empty():
    with pytest.raises(ValueError):
        slugify_title("   ")


def test_paths_from_title(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    paths = PipelinePaths.from_title("Test Piece")
    project = (tmp_path / "output" / "Test Piece").resolve()
    assert paths.work_dir.resolve() == project
    assert paths.output_path.resolve() == (project / "Test Piece.ly").resolve()
    assert paths.chunks_dir.resolve() == (project / "chunks").resolve()


def test_natural_sort_key():
    files = [
        Path("page10.png"),
        Path("page2.png"),
        Path("page1.png"),
        Path("page20.png"),
    ]
    sorted_files = sorted(files, key=natural_sort_key)
    assert [f.name for f in sorted_files] == [
        "page1.png",
        "page2.png",
        "page10.png",
        "page20.png",
    ]


def test_find_image_files(tmp_path):
    d = tmp_path / "sheet_images"
    d.mkdir()
    (d / "p2.png").write_text("")
    (d / "p1.jpg").write_text("")
    (d / "p10.png").write_text("")
    (d / "ignore.txt").write_text("")
    (d / "ignore.musicxml").write_text("")

    found = find_image_files(d)
    assert [f.name for f in found] == ["p1.jpg", "p2.png", "p10.png"]


def test_find_image_files_skips_original_backups(tmp_path):
    """scanprep renames raws to "<stem> (original)<ext>"; image2ly must
    only ever see the cleaned pages."""
    d = tmp_path / "song"
    d.mkdir()
    (d / "1.png").write_text("")
    (d / "1 (original).jpg").write_text("")
    (d / "2 (original).png").write_text("")

    assert [f.name for f in find_image_files(d)] == ["1.png"]

    from music2ly.models import find_image_files as find_all

    assert [f.name for f in find_all(d, include_originals=True)] == [
        "1 (original).jpg",
        "1.png",
        "2 (original).png",
    ]


def test_image_paths_from_target_dir_name(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    # Target is "Foo Bar", default output root is "output"
    target_dir = tmp_path / "output" / "Foo Bar"
    target_dir.mkdir(parents=True)
    (target_dir / "1.png").write_text("")
    (target_dir / "2.png").write_text("")

    paths, title = ImagePaths.from_target("Foo Bar")
    assert title == "Foo Bar"
    assert paths.work_dir == target_dir.resolve()
    assert [f.name for f in paths.source_images] == ["1.png", "2.png"]
    assert paths.output_path == target_dir.resolve() / "Foo Bar.ly"
    assert [p.name for p in paths.page_musicxml_paths] == [
        "recognized_001.musicxml",
        "recognized_002.musicxml",
    ]


def test_image_paths_from_existing_custom_dir(tmp_path):
    custom_dir = tmp_path / "custom_song"
    custom_dir.mkdir()
    (custom_dir / "score 1.png").write_text("")
    (custom_dir / "score 2.png").write_text("")

    paths, title = ImagePaths.from_target(custom_dir)
    assert title == "custom_song"
    assert paths.work_dir == custom_dir.resolve()
    assert [f.name for f in paths.source_images] == ["score 1.png", "score 2.png"]
    assert paths.output_path == custom_dir.resolve() / "custom_song.ly"


def test_image_paths_with_title_override(tmp_path):
    d = tmp_path / "my_dir"
    d.mkdir()
    paths, title = ImagePaths.from_target(d, title="Custom Title")
    assert title == "Custom Title"
    assert paths.output_path == d.resolve() / "Custom Title.ly"


def test_image_paths_with_sequence_in_title(tmp_path):
    d = tmp_path / "Für Elise (EveryonePiano 47)"
    d.mkdir()
    paths, title = ImagePaths.from_target(d)
    assert title == "Für Elise"
    assert paths.output_path == d.resolve() / "Für Elise (EveryonePiano 47).ly"


def test_image_paths_with_sequence_in_images(tmp_path):
    d = tmp_path / "Für Elise"
    d.mkdir()
    (d / "Für Elise (EveryonePiano 47) 1.png").write_text("")
    (d / "Für Elise (EveryonePiano 47) 2.png").write_text("")
    paths, title = ImagePaths.from_target(d)
    assert title == "Für Elise"
    assert paths.output_path == d.resolve() / "Für Elise (EveryonePiano 47).ly"
