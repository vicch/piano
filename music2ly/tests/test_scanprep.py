import json
from pathlib import Path

import cv2
import numpy as np
import pytest
from PIL import Image

from image2ly.models import ImagePaths
from music2ly.models import find_image_files
from scanprep import enhance
from scanprep.cli import build_parser, main
from scanprep.models import ScanPaths, discover_page_sources
from scanprep.pipeline import PrepOptions, process_page, run_pipeline


# --- synthetic scan fixtures ---------------------------------------------


def make_scan(
    shape=(600, 400),
    staff_space=12,
    paper_low=235,
    paper_high=235,
    specks=0,
    title_block=False,
    line_slope_deg=0.0,
    seed=0,
):
    """Draw a synthetic sheet-music scan.

    Paper brightness varies horizontally from paper_low (left) to
    paper_high (right) so illumination can be made flat or uneven.
    Staves are 5-line systems; noteheads and stems add real notation.
    """
    h, w = shape
    yy, xx = np.mgrid[0:h, 0:w].astype(np.float32)
    paper = paper_low + (paper_high - paper_low) * (xx / max(w - 1, 1))
    img = paper.astype(np.uint8)
    ink = 40
    slope = float(np.tan(np.radians(line_slope_deg)))

    for system in range(3):
        top = 50 + system * (staff_space * 4 + 80)
        for i in range(5):
            y0 = top + i * staff_space
            y1 = y0 + int(slope * (w - 1))
            cv2.line(img, (0, y0), (w - 1, y1), ink, 1)
        for j in range(5):
            x = 40 + j * 65
            cy = top + 2 * staff_space
            cv2.circle(img, (x, cy), max(2, staff_space // 3), ink, -1)
            stem_x = x + max(2, staff_space // 3)
            cv2.line(img, (stem_x, cy), (stem_x, cy - 3 * staff_space), ink, 1)

    if title_block:
        cv2.rectangle(img, (60, 8), (w - 60, 26), ink, -1)

    if specks:
        rng = np.random.default_rng(seed)
        ys = rng.integers(0, h, size=specks)
        xs = rng.integers(0, w, size=specks)
        img[ys, xs] = 90

    return img


def save_scan(arr, path: Path) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    Image.fromarray(arr).save(path)
    return path


# --- measurement algorithms ----------------------------------------------


def test_estimate_staff_space():
    img = make_scan(staff_space=12)
    spacing, peaks = enhance.estimate_staff_space(img)
    assert spacing == 12
    assert peaks and peaks[0] == 12


def test_estimate_staff_space_fallback_on_blank_page():
    img = np.full((400, 300), 210, dtype=np.uint8)
    spacing, peaks = enhance.estimate_staff_space(img)
    assert spacing == enhance.DEFAULT_STAFF_SPACE
    assert peaks == []


def test_estimate_skew_and_deskew():
    img = make_scan(line_slope_deg=1.5)
    angle, lines = enhance.estimate_skew(img)
    assert lines >= enhance.SKEW_MIN_LINES
    assert angle == pytest.approx(1.5, abs=0.3)
    leveled = enhance.deskew(img, angle)
    rest_angle, _ = enhance.estimate_skew(leveled)
    assert abs(rest_angle) < 0.2


def test_measure_noise_detects_specks():
    clean = make_scan(specks=0)
    noisy = make_scan(specks=600)
    assert enhance.measure_noise(clean) < enhance.DENOISE_NOISE_THRESHOLD
    assert enhance.measure_noise(noisy) > enhance.DENOISE_NOISE_THRESHOLD


def test_sauvola_k_adapts_to_noise():
    assert enhance.sauvola_k_for(0.05) == enhance.SAUVOLA_K_BASE
    assert enhance.sauvola_k_for(0.3) == enhance.SAUVOLA_K_NOISY


def test_detect_dark_border():
    clean = make_scan()
    assert enhance.detect_dark_border(clean) is False
    dark = make_scan()
    dark[:8, :] = 30
    dark[-8:, :] = 30
    assert enhance.detect_dark_border(dark) is True


# --- tone correction ------------------------------------------------------


def test_correct_illumination_flattens_paper_and_keeps_ink():
    img = make_scan(paper_low=170, paper_high=235)
    bg = enhance.estimate_background(img, staff_space=12)
    assert enhance.needs_illumination(bg) is True
    corrected = enhance.correct_illumination(img, bg)
    assert enhance.paper_stats(corrected)["std"] < enhance.paper_stats(img)["std"]
    assert corrected.min() < 100  # ink stayed ink


def test_illumination_skipped_on_flat_background():
    img = make_scan(paper_low=235, paper_high=235)
    bg = enhance.estimate_background(img, staff_space=12)
    assert enhance.needs_illumination(bg) is False


def test_background_floor_preserves_solid_title_block():
    img = make_scan(paper_low=170, paper_high=235, title_block=True)
    bg = enhance.estimate_background(img, staff_space=12)
    corrected = enhance.correct_illumination(img, bg)
    block_center = corrected[16, img.shape[1] // 2]
    assert block_center < 120  # solid black must not blow out to white


def test_illumination_floor_keeps_collapsed_background_dark():
    paper = np.full((80, 80), 214, dtype=np.uint8)
    gray = paper.copy()
    cv2.rectangle(gray, (20, 20), (60, 60), 30, -1)
    bg = paper.copy()  # estimator collapsed over the solid block
    cv2.rectangle(bg, (20, 20), (60, 60), 30, -1)
    out = enhance.correct_illumination(gray, bg)
    assert out[40, 40] < 120  # floor keeps the solid block dark
    assert out[5, 5] > 230  # paper normalized to target


def test_apply_levels_normalizes_paper_without_clipping_ink():
    img = make_scan(paper_low=180, paper_high=185)
    img[5, 5] = 150  # faint mark just below paper brightness
    out = enhance.apply_levels(img)
    assert out.max() >= 250  # paper pushed to white
    assert 200 < out[5, 5] < 240  # faint mark kept its relative contrast
    assert out.min() < 100  # ink stayed ink (scaled, not clipped to black)


def test_denoise_removes_isolated_specks():
    img = np.full((200, 200), 240, dtype=np.uint8)
    for k in range(50):
        img[20 + k * 3, 15 + (k * 7) % 170] = 90  # well-separated specks
    out = enhance.denoise(img)
    assert out.min() >= 200  # specks gone


def test_denoise_preserves_1px_staff_lines():
    """A median filter would delete 1px lines; the isolated-speck removal
    must not (staff lines have dark neighbors along their length)."""
    img = np.full((200, 200), 240, dtype=np.uint8)
    cv2.line(img, (0, 100), (199, 100), 40, 1)
    out = enhance.denoise(img)
    assert out[100, 100] < 100
    assert (out[100] < 150).mean() > 0.9


def test_denoise_preserves_note_dots():
    img = np.full((200, 200), 240, dtype=np.uint8)
    cv2.circle(img, (100, 100), 3, 40, -1)  # dot-sized musical mark
    out = enhance.denoise(img)
    assert out[100, 100] < 100


def test_sauvola_binary_separates_ink_from_paper():
    img = make_scan(paper_low=170, paper_high=235)
    bg = enhance.estimate_background(img, staff_space=12)
    clean = enhance.apply_levels(enhance.correct_illumination(img, bg))
    binary = enhance.sauvola_binary(clean, window=60, k=0.15)
    assert set(np.unique(binary)) <= {0, 255}
    assert (binary == 0).mean() > 0.005  # notation is black
    assert (binary == 255).mean() > 0.5  # paper is white


# --- adaptive end-to-end behavior -----------------------------------------


def test_process_page_adapts_decisions_per_input(tmp_path):
    flat = save_scan(make_scan(paper_low=238, paper_high=238), tmp_path / "flat.png")
    rough = save_scan(
        make_scan(paper_low=160, paper_high=240, specks=800), tmp_path / "rough.png"
    )

    flat_result = process_page(flat, 1, "flat", PrepOptions())
    rough_result = process_page(rough, 2, "rough", PrepOptions())

    # Uneven, noisy page gets corrections; clean flat page does not.
    assert rough_result.report.illumination_corrected is True
    assert rough_result.report.denoised is True
    assert rough_result.report.sauvola_k == enhance.SAUVOLA_K_NOISY
    assert flat_result.report.illumination_corrected is False
    assert flat_result.report.denoised is False
    assert flat_result.report.sauvola_k == enhance.SAUVOLA_K_BASE

    # Outputs converge on uniform quality regardless of input exposure.
    flat_paper = flat_result.report.paper_after["mean"]
    rough_paper = rough_result.report.paper_after["mean"]
    assert abs(flat_paper - rough_paper) < 15
    assert flat_result.report.paper_after["std"] < flat_result.report.paper_before["std"] or (
        flat_result.report.paper_before["std"] < 5
    )


def test_process_page_keeps_binary_ink_sane(tmp_path):
    src = save_scan(make_scan(), tmp_path / "scan.png")
    result = process_page(src, 1, "scan", PrepOptions())
    assert result.report.noise_pct < enhance.DENOISE_NOISE_THRESHOLD
    assert 0.001 < result.report.ink_ratio < 0.25
    assert result.binary is not None
    assert result.report.sauvola_k == enhance.SAUVOLA_K_BASE


# --- in-place pairing and pipeline -----------------------------------------


def test_discover_pages_first_run(tmp_path):
    work = tmp_path / "output" / "Song"
    work.mkdir(parents=True)
    save_scan(make_scan(), work / "1.jpg")
    save_scan(make_scan(), work / "2.jpg")

    sources = discover_page_sources(work)
    assert [s.stem for s in sources] == ["1", "2"]
    assert all(s.backup_path is not None for s in sources)
    assert sources[0].raw_path.name == "1.jpg"
    assert sources[0].backup_path.name == "1 (original).jpg"
    assert sources[0].processed_path.name == "1.png"
    assert sources[0].binary_path.name == "1.png"


def test_discover_pages_rerun_uses_backups(tmp_path):
    work = tmp_path / "output" / "Song"
    work.mkdir(parents=True)
    save_scan(make_scan(), work / "1 (original).jpg")
    save_scan(make_scan(), work / "1.png")

    sources = discover_page_sources(work)
    assert len(sources) == 1
    assert sources[0].raw_path.name == "1 (original).jpg"
    assert sources[0].backup_path is None  # already backed up
    assert sources[0].processed_path.name == "1.png"


def test_discover_pages_orphan_backup_still_processed(tmp_path):
    work = tmp_path / "output" / "Song"
    work.mkdir(parents=True)
    save_scan(make_scan(), work / "2 (original).jpg")

    sources = discover_page_sources(work)
    assert [s.stem for s in sources] == ["2"]
    assert sources[0].processed_path.name == "2.png"


def test_discover_pages_reports_stray_duplicate(tmp_path):
    work = tmp_path / "output" / "Song"
    work.mkdir(parents=True)
    save_scan(make_scan(), work / "1 (original).jpg")
    save_scan(make_scan(), work / "1.png")  # processed page (expected, not a stray)
    save_scan(make_scan(), work / "1.jpg")  # stray duplicate next to its backup

    sources = discover_page_sources(work)
    assert len(sources) == 1
    assert [p.name for p in sources[0].strays] == ["1.jpg"]
    assert sources[0].raw_path.name == "1 (original).jpg"


def test_discover_pages_prefers_output_named_raw(tmp_path):
    """A fresh raw already named like the processed page must be moved aside,
    never silently overwritten by the cleaned page."""
    work = tmp_path / "output" / "Song"
    work.mkdir(parents=True)
    save_scan(make_scan(), work / "1.png")  # would collide with the output
    save_scan(make_scan(), work / "1.jpg")  # second raw, becomes a stray

    sources = discover_page_sources(work)
    assert len(sources) == 1
    assert sources[0].raw_path.name == "1.png"
    assert sources[0].backup_path.name == "1 (original).png"
    assert [p.name for p in sources[0].strays] == ["1.jpg"]


def test_run_pipeline_in_place_end_to_end(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    work = tmp_path / "output" / "Adaptive Test"
    work.mkdir(parents=True)
    save_scan(make_scan(paper_low=180, paper_high=240, specks=300), work / "1.jpg")
    save_scan(make_scan(paper_low=190, paper_high=245), work / "2.jpg")

    paths, title = ScanPaths.from_target("Adaptive Test")
    assert title == "Adaptive Test"

    run_pipeline(paths, PrepOptions())

    # Originals renamed and preserved; processed pages keep the stems.
    assert (work / "1 (original).jpg").exists()
    assert (work / "2 (original).jpg").exists()
    assert not (work / "1.jpg").exists()
    assert (work / "1.png").exists()
    assert (work / "2.png").exists()
    assert (work / "binary" / "1.png").exists()
    assert (work / "scanprep" / "preview.png").exists()

    report = json.loads((work / "scanprep" / "scanprep.json").read_text(encoding="utf-8"))
    assert report["tool"] == "scanprep"
    assert len(report["pages"]) == 2
    assert report["pages"][0]["stem"] == "1"
    assert report["pages"][0]["staff_space_px"] == 12
    assert report["pages"][0]["outputs"] == {
        "processed": "1.png",
        "original": "1 (original).jpg",
        "binary": "binary/1.png",
    }
    assert report["parameters"]["background_method"] == "morph"


def test_run_pipeline_feeds_image2ly_smoothly(tmp_path, monkeypatch):
    """The chaining contract: image2ly on the same dir sees exactly the
    cleaned pages, in natural page order, and nothing else."""
    monkeypatch.chdir(tmp_path)
    work = tmp_path / "output" / "Chained"
    work.mkdir(parents=True)
    save_scan(make_scan(), work / "1.jpg")
    save_scan(make_scan(), work / "2.jpg")
    save_scan(make_scan(), work / "10.jpg")

    run_pipeline(ScanPaths.for_work_dir(work), PrepOptions())

    assert [p.name for p in find_image_files(work)] == ["1.png", "2.png", "10.png"]

    ipaths, ititle = ImagePaths.from_target("Chained")
    assert ititle == "Chained"
    assert [p.name for p in ipaths.source_images] == ["1.png", "2.png", "10.png"]
    assert ipaths.work_dir == work.resolve()


def test_run_pipeline_idempotent_rerun(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    work = tmp_path / "output" / "Idem"
    work.mkdir(parents=True)
    save_scan(make_scan(paper_low=180, paper_high=240), work / "1.jpg")

    paths = ScanPaths.for_work_dir(work)
    run_pipeline(paths, PrepOptions())
    first_mtime = (work / "1.png").stat().st_mtime_ns

    run_pipeline(paths, PrepOptions())  # re-run without --resume re-processes

    # Raw never gets double-renamed; processed page regenerated from the raw.
    backups = [f for f in work.iterdir() if "(original)" in f.name]
    assert [f.name for f in backups] == ["1 (original).jpg"]
    assert (work / "1.png").exists()
    assert not (work / "1.jpg").exists()


def test_run_pipeline_resume_skips_cleaned(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    work = tmp_path / "output" / "Resume"
    work.mkdir(parents=True)
    save_scan(make_scan(), work / "1.jpg")
    save_scan(make_scan(), work / "2.jpg")

    paths = ScanPaths.for_work_dir(work)
    run_pipeline(paths, PrepOptions())

    # Replace page 1 with a sentinel; resume must not overwrite it.
    sentinel = np.full((31, 41), 7, dtype=np.uint8)
    Image.fromarray(sentinel).save(work / "1.png")

    run_pipeline(paths, PrepOptions(resume=True))
    restored = np.array(Image.open(work / "1.png"))
    assert restored.shape == (31, 41)
    assert (restored == 7).all()


def test_run_pipeline_resume_processes_fresh_raw(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    work = tmp_path / "output" / "Fresh"
    work.mkdir(parents=True)
    save_scan(make_scan(), work / "1.jpg")

    paths = ScanPaths.for_work_dir(work)
    run_pipeline(paths, PrepOptions(resume=True))

    # A fresh raw has no backup yet: resume must not skip the rename+clean.
    assert (work / "1 (original).jpg").exists()
    assert (work / "1.png").exists()


def test_run_pipeline_no_images_raises(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    work = tmp_path / "output" / "Empty"
    work.mkdir(parents=True)
    paths, _ = ScanPaths.from_target("Empty")
    with pytest.raises(FileNotFoundError, match="No sheet music images found"):
        run_pipeline(paths, PrepOptions())


def test_run_pipeline_reports_warnings(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    work = tmp_path / "output" / "Warny"
    work.mkdir(parents=True)
    dark_border = make_scan()
    dark_border[:8, :] = 30
    dark_border[-8:, :] = 30
    save_scan(dark_border, work / "1.png")

    paths, _ = ScanPaths.from_target("Warny")
    run_pipeline(paths, PrepOptions())
    report = json.loads(paths.report_path.read_text(encoding="utf-8"))
    assert report["pages"][0]["dark_border"] is True
    assert any("dark border" in w for w in report["pages"][0]["warnings"])


# --- target resolution ------------------------------------------------------


def test_scan_paths_from_single_file_copies_raw(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    src = save_scan(make_scan(), tmp_path / "raw" / "Innocent 1.jpg")
    paths, title = ScanPaths.from_target(src)
    assert title == "Innocent 1"
    assert paths.work_dir == (tmp_path / "output" / "Innocent 1").resolve()
    assert (paths.work_dir / "Innocent 1.jpg").exists()  # copied in like image2ly
    assert paths.binary_dir == paths.work_dir / "binary"
    assert paths.report_path == paths.scanprep_dir / "scanprep.json"

    # Re-resolving after the stem is settled must not re-copy the raw.
    (paths.work_dir / "Innocent 1.jpg").rename(paths.work_dir / "Innocent 1 (original).jpg")
    save_scan(make_scan(), paths.work_dir / "Innocent 1.png")
    ScanPaths.from_target(src)
    assert not (paths.work_dir / "Innocent 1.jpg").exists()


def test_scan_paths_from_directory_with_title_override(tmp_path):
    work = tmp_path / "scans"
    work.mkdir()
    save_scan(make_scan(), work / "a.png")
    paths, title = ScanPaths.from_target(work, title="Custom Title")
    assert title == "Custom Title"
    assert paths.work_dir == work.resolve()
    assert paths.preview_path == work / "scanprep" / "preview.png"


# --- CLI --------------------------------------------------------------------


def test_cli_parser_defaults():
    parser = build_parser()
    args = parser.parse_args(["Some Song"])
    assert args.title is None
    assert args.no_deskew is False
    assert args.max_skew == 3.0
    assert args.background_method == "morph"
    assert args.background_scale == 4.0
    assert args.paper_target == 245
    assert args.no_binary is False
    assert args.sauvola_k is None
    assert args.sauvola_window_scale == 5.0
    assert args.denoise is None
    assert args.no_preview is False
    assert args.resume is False


def test_cli_parser_custom_options():
    parser = build_parser()
    args = parser.parse_args(
        [
            "path/to/scans",
            "--title", "T",
            "--no-deskew",
            "--background-method", "morph",
            "--background-scale", "6",
            "--paper-target", "250",
            "--no-binary",
            "--sauvola-k", "0.2",
            "--denoise", "off",
            "--no-preview",
            "--resume",
        ]
    )
    assert args.title == "T"
    assert args.no_deskew is True
    assert args.background_method == "morph"
    assert args.background_scale == 6.0
    assert args.paper_target == 250
    assert args.no_binary is True
    assert args.sauvola_k == 0.2
    assert args.denoise is False
    assert args.no_preview is True
    assert args.resume is True


def test_cli_main_end_to_end(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    work = tmp_path / "output" / "CliScan"
    work.mkdir(parents=True)
    save_scan(make_scan(paper_low=170, paper_high=240), work / "page1.png")

    exit_code = main(["CliScan"])
    assert exit_code == 0
    assert (work / "page1.png").exists()
    assert (work / "page1 (original).png").exists()
    assert (work / "binary" / "page1.png").exists()
    assert (work / "scanprep" / "scanprep.json").exists()
    # image2ly chaining: only the cleaned page remains in the listing
    assert [p.name for p in find_image_files(work)] == ["page1.png"]


def test_cli_main_no_images_fails(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    (tmp_path / "output" / "Nothing").mkdir(parents=True)
    exit_code = main(["Nothing"])
    assert exit_code == 1
