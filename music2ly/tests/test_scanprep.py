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


def test_apply_contrast_pulls_washed_pages_and_gates_contrasty_ones():
    """The span gate: pages with at least min_span of ink-paper contrast
    pass through untouched; narrower (washed-out) pages get ink pulled
    darker and paper pushed to white."""
    washed = np.full((100, 100), 200, dtype=np.uint8)
    washed[10:20, 10:20] = 120  # span 80 < gate -> remapped
    out = enhance.apply_contrast(washed, min_span=100)
    assert float(out[10:20, 10:20].mean()) < 120  # ink pulled darker
    assert float(out[0:10, 0:10].mean()) > 240  # paper pushed to white

    crisp = np.full((100, 100), 255, dtype=np.uint8)
    crisp[10:20, 10:20] = 10  # span 245 >= gate -> untouched
    crisp_out = enhance.apply_contrast(crisp, min_span=200)
    assert np.array_equal(crisp_out, crisp)


def test_sharpen_steepens_edges_without_clipping():
    edge = np.full((60, 60), 220, dtype=np.uint8)
    edge[:, 30:] = 40
    soft = cv2.GaussianBlur(edge, (0, 0), 2.0)
    out = enhance.sharpen(soft, staff_space=10, amount=0.9)
    assert out.min() >= 0 and out.max() <= 255
    # the step must get steeper: overshoot on the light side (cols < 30),
    # undershoot on the dark side (cols > 30) - that reads as "crisp"
    assert float(out[:, 24:27].mean()) > float(soft[:, 24:27].mean())
    assert float(out[:, 33:36].mean()) < float(soft[:, 33:36].mean())
    # amount 0 must be an exact no-op
    assert np.array_equal(enhance.sharpen(soft, 10, amount=0.0), soft)


def test_saturate_white_erases_grain_not_ink():
    """Scanner look: near-white tones (paper grain) become pure white;
    notation and midtones are untouched; margin 0 is a no-op."""
    img = np.full((50, 50), 255, dtype=np.uint8)
    img[0:10, 0:10] = 230  # paper grain, just below white
    img[20:30, 20:30] = 180  # faint but real mark
    img[40:50, 40:50] = 60   # solid ink
    out = enhance.saturate_white(img, margin=40)
    assert (out[0:10, 0:10] == 255).all()  # grain erased
    assert (out[20:30, 20:30] == 180).all()  # faint mark survives
    assert (out[40:50, 40:50] == 60).all()  # ink untouched
    assert np.array_equal(enhance.saturate_white(img, margin=0), img)


def test_despeckle_drops_grain_keeps_musical_marks():
    """Area filter: 2-4px grain blobs vanish; staccato-dot-sized marks and
    long 1px line fragments (staff lines, stems) survive."""
    binary = np.full((200, 200), 255, dtype=np.uint8)
    binary[5, 5] = 0  # single grain pixel
    binary[50:52, 50:52] = 0  # 2x2 grain cluster (area 4)
    cv2.circle(binary, (100, 100), 2, 0, -1)  # staccato-dot-sized mark
    cv2.line(binary, (0, 150), (199, 150), 0, 1)  # 1px staff-line fragment
    out, removed = enhance.despeckle_binary(binary, staff_space=12, area_scale=0.05)
    assert removed == 2  # the pixel and the 2x2 cluster
    assert out[5, 5] == 255
    assert (out[50:52, 50:52] == 255).all()
    assert out[100, 100] == 0  # musical dot kept
    assert (out[150] == 0).all()  # line fragment kept


def test_process_page_restores_grainy_scan(tmp_path):
    """End to end: clustered grain (what denoise's isolated-speck filter
    misses) must not survive into the binarized page."""
    scan = make_scan()
    rng = np.random.default_rng(7)
    for _ in range(40):  # 2x2 grain blobs scattered over the paper
        y = int(rng.integers(5, 590))
        x = int(rng.integers(5, 390))
        scan[y:y + 2, x:x + 2] = 150
    src = save_scan(scan, tmp_path / "grainy.png")

    result = process_page(src, 1, "grainy", PrepOptions())
    assert result.report.specks_removed > 0
    # the page is still notation, not confetti
    assert 0.001 < result.report.ink_ratio < 0.25


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


def test_process_page_output_default_smooth_binary_optional(tmp_path):
    src = save_scan(make_scan(), tmp_path / "scan.png")
    result = process_page(src, 1, "scan", PrepOptions())
    assert result.report.noise_pct < enhance.DENOISE_NOISE_THRESHOLD
    assert 0.001 < result.report.ink_ratio < 0.25
    # Default: restored grayscale - solid dark ink, pure white paper, and
    # anti-aliased edges kept (the natural scanned-PDF look).
    assert result.clean.min() < 80
    assert result.clean.max() == 255
    assert result.report.sauvola_k == enhance.SAUVOLA_K_BASE

    # Strict 1-bit output on request: pure black and white.
    strict = process_page(src, 1, "scan", PrepOptions(binary_output=True))
    assert set(np.unique(strict.clean)) <= {0, 255}


def test_restored_page_keeps_anti_aliased_edges(tmp_path):
    """A hard threshold crystallizes edges; the default page must keep the
    source's anti-aliasing ramp so lines look smooth, not staircased."""
    img = make_scan()
    cv2.line(img, (0, 300), (399, 300), 40, 1, lineType=cv2.LINE_AA)
    src = save_scan(img, tmp_path / "aa.png")

    result = process_page(src, 1, "aa", PrepOptions())
    band = result.clean[295:306, 100:300]
    assert set(np.unique(band)) - {0, 255}  # intermediate edge tones survive

    strict = process_page(src, 1, "aa", PrepOptions(binary_output=True))
    assert not set(np.unique(strict.clean[295:306, 100:300])) - {0, 255}


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
    assert sources[0].backup_path == work / "original" / "1.jpg"  # kept as-is
    assert sources[0].processed_path.name == "1.png"


def test_discover_pages_rerun_uses_original_dir(tmp_path):
    work = tmp_path / "output" / "Song"
    work.mkdir(parents=True)
    save_scan(make_scan(), work / "original" / "1.jpg")
    save_scan(make_scan(), work / "1.png")

    sources = discover_page_sources(work)
    assert len(sources) == 1
    assert sources[0].raw_path == work / "original" / "1.jpg"
    assert sources[0].backup_path is None  # already preserved
    assert sources[0].processed_path.name == "1.png"


def test_discover_pages_legacy_backup_migrates(tmp_path):
    """Legacy top-level "1 (original).jpg" is still a raw; it migrates into
    original/ under its original name."""
    work = tmp_path / "output" / "Song"
    work.mkdir(parents=True)
    save_scan(make_scan(), work / "1 (original).jpg")
    save_scan(make_scan(), work / "1.png")

    sources = discover_page_sources(work)
    assert len(sources) == 1
    assert sources[0].raw_path.name == "1 (original).jpg"
    assert sources[0].backup_path == work / "original" / "1.jpg"
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
    assert sources[0].backup_path == work / "original" / "1.png"  # kept as-is
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

    # Originals preserved as-is in original/; processed pages keep the stems.
    assert (work / "original" / "1.jpg").exists()
    assert (work / "original" / "2.jpg").exists()
    assert not (work / "1.jpg").exists()
    assert (work / "1.png").exists()
    assert (work / "2.png").exists()
    assert not (work / "binary").exists()  # no side artifacts anymore
    assert (work / "scanprep" / "preview.png").exists()

    # Cleaned pages: solid dark ink on pure white paper (anti-aliased
    # edges by default - the smooth scanned-page look).
    for page in ("1.png", "2.png"):
        restored = np.array(Image.open(work / page))
        assert restored.max() == 255
        assert restored.min() < 80

    report = json.loads((work / "scanprep" / "scanprep.json").read_text(encoding="utf-8"))
    assert report["tool"] == "scanprep"
    assert len(report["pages"]) == 2
    assert report["pages"][0]["stem"] == "1"
    assert report["pages"][0]["staff_space_px"] == 12
    assert report["pages"][0]["outputs"] == {
        "processed": "1.png",
        "original": "original/1.jpg",
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

    # Raw never gets double-moved; processed page regenerated from the raw.
    assert (work / "original" / "1.jpg").exists()
    assert [f.name for f in (work / "original").iterdir()] == ["1.jpg"]
    assert (work / "1.png").exists()
    assert not (work / "1.jpg").exists()


def test_run_pipeline_overwrites_existing_original(tmp_path, monkeypatch):
    """A same-named raw already in original/ is overwritten, not an error."""
    monkeypatch.chdir(tmp_path)
    work = tmp_path / "output" / "Overwrite"
    work.mkdir(parents=True)
    save_scan(make_scan(), work / "1.jpg")
    stale = np.full((21, 13), 200, dtype=np.uint8)
    save_scan(stale, work / "original" / "1.jpg")  # leftover from an earlier run

    paths, _ = ScanPaths.from_target("Overwrite")
    run_pipeline(paths, PrepOptions())

    kept = np.array(Image.open(work / "original" / "1.jpg"))
    assert kept.shape == (600, 400)  # the new raw replaced the stale one
    assert [f.name for f in (work / "original").iterdir()] == ["1.jpg"]
    assert (work / "1.png").exists()


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

    # A fresh raw is not preserved yet: resume must not skip the move+clean.
    assert (work / "original" / "1.jpg").exists()
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
    assert paths.original_dir == paths.work_dir / "original"
    assert paths.report_path == paths.scanprep_dir / "scanprep.json"

    # Re-resolving after the stem is settled must not re-copy the raw.
    # (A preserved raw in original/ counts as settled; so does a legacy
    # "(original)" backup.)
    save_scan(make_scan(), paths.original_dir / "Innocent 1.jpg")
    (paths.work_dir / "Innocent 1.jpg").unlink()
    save_scan(make_scan(), paths.work_dir / "Innocent 1.png")
    ScanPaths.from_target(src)
    assert not (paths.work_dir / "Innocent 1.jpg").exists()

    (paths.original_dir / "Innocent 1.jpg").rename(
        paths.work_dir / "Innocent 1 (original).jpg"
    )
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
    assert args.no_contrast is False
    assert args.no_whiten is False
    assert args.no_sharpen is False
    assert args.no_despeckle is False
    assert args.binary is False
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
            "--no-contrast",
            "--no-whiten",
            "--no-sharpen",
            "--no-despeckle",
            "--binary",
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
    assert args.no_contrast is True
    assert args.no_whiten is True
    assert args.no_sharpen is True
    assert args.no_despeckle is True
    assert args.binary is True
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
    assert (work / "original" / "page1.png").exists()
    restored = np.array(Image.open(work / "page1.png"))
    assert restored.max() == 255 and restored.min() < 80  # restored page
    assert (work / "scanprep" / "scanprep.json").exists()
    # image2ly chaining: only the cleaned page remains in the listing
    assert [p.name for p in find_image_files(work)] == ["page1.png"]


def test_cli_main_no_images_fails(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    (tmp_path / "output" / "Nothing").mkdir(parents=True)
    exit_code = main(["Nothing"])
    assert exit_code == 1
