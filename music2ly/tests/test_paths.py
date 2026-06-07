import pytest

from music2ly.models import PipelinePaths, slugify_title


def test_slugify_title():
    assert slugify_title("My Song") == "My-Song"
    assert slugify_title("  Passacaglia  ") == "Passacaglia"
    assert slugify_title("看见") == "看见"


def test_slugify_title_empty():
    with pytest.raises(ValueError):
        slugify_title("   ")


def test_paths_from_title(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    paths = PipelinePaths.from_title("Test Piece")
    project = (tmp_path / "output" / "Test-Piece").resolve()
    assert paths.work_dir.resolve() == project
    assert paths.output_path.resolve() == (project / "Test-Piece.ly").resolve()
    assert paths.chunks_dir.resolve() == (project / "chunks").resolve()
