"""Core scan-enhancement algorithms (pure functions over numpy arrays).

Every kernel size and threshold derives from measurements of the input
page (staff-line spacing, background flatness, noise level) so scans of
any resolution, exposure, or paper tone converge on uniform output
quality. OpenCV is used only for pixel math; all file I/O goes through
Pillow so non-ASCII output paths work on Windows.
"""

from __future__ import annotations

from pathlib import Path

import cv2
import numpy as np

# --- adaptive defaults and decision thresholds -------------------------

DEFAULT_STAFF_SPACE = 10   # fallback staff-line spacing (px) when estimation fails
MIN_STAFF_SPACE = 6       # below this the scan is too coarse for reliable OMR
MIN_DESKEW_ANGLE = 0.05    # don't rotate for angles smaller than this (degrees)
SKEW_MIN_LINES = 3         # long lines required to trust a skew estimate
FLAT_BG_RANGE = 12.0       # background p95-p5 below this: skip division correction
DENOISE_NOISE_THRESHOLD = 0.05   # % isolated specks above this: remove them
SAUVOLA_NOISE_THRESHOLD = 0.2    # % isolated specks above this: raise Sauvola k
SAUVOLA_K_BASE = 0.15
SAUVOLA_K_NOISY = 0.22
BG_FLOOR_RATIO = 0.45      # background floor: fraction of paper brightness; keeps
                           # large solid ink regions (titles) from blowing out
DARK_BORDER_RATIO = 0.7    # frame mean below this fraction of paper: dark border
PAPER_ANCHOR_PCT = 99.5    # brightness percentile treated as "paper" for normalization
MAX_PAPER_GAIN = 4.0       # cap for the paper->white gain (never darken, never explode)
PAPER_TARGET = 245

# --- restoration knobs: the "document scanner" pass -----------------------
# Goal: restore a photographed/photocopied page to what it looked like
# when it was printed - solid dark notation on clean white paper, smooth
# natural edges, no photo traits (grain, shading, gray wash). The final
# page keeps the anti-aliased grayscale (hard 1-bit thresholding is what
# makes edges look crystallized; a real scanner/PDF keeps the edge ramp),
# with Sauvola used internally to find specks and QC ink coverage.
# Strict pure black-and-white output is opt-in via --binary.
#
# The active values below are the "balanced" preset; copy one of the
# preset columns over them to move between fidelity and extreme punch.
#
#   knob                  fidelity      balanced      extreme
#   --------------------  -----------  -----------  -----------
#   CONTRAST_INK_PCT      5.0           2.0           0.5
#   CONTRAST_INK_TARGET   80.0          55.0          30.0
#   CONTRAST_GAMMA        1.0           1.05          1.35
#   CONTRAST_MIN_SPAN     140.0         200.0         240.0
#   EDGE_SMOOTH_SIGMA     0.5           0.75          0.5
#   PAPER_WHITE_MARGIN    25.0          40.0          60.0
#   SHARPEN_AMOUNT        0.0           0.25          1.2
#   SHARPEN_SIGMA_SCALE   0.35          0.5           0.75
#   DESPECKLE_AREA_SCALE  0.03          0.05          0.12
#
# How each level works as a whole (the values trade off against each
# other, so mix-and-matching between columns can misfire):
#
# fidelity — reads like the original page with clean paper: healthy scans
#   (ink-paper span >= 140) skip the contrast remap entirely; washed-out
#   pages are rescued gently (anchor to 80, no gamma). Zero sharpening,
#   light edge smoothing, low white saturation (only the faintest grain
#   goes), gentle despeckling. For literally zero processing of the tones
#   use --no-contrast --no-sharpen (whiten/despeckle/smooth remain -
#   they are restoration, not enhancement).
#
# balanced — the professional-scan look and the working default: the
#   span gate (200) lets everything short of a pristine scan through the
#   remap, but the anchor target (55) sits near where healthy ink already
#   lands after levels, so good pages barely move while faint pages
#   darken in proportion to how washed they are. Gamma 1.05 keeps stroke
#   edges firm without crushing their anti-aliasing ramp. Edge smoothing
#   (sigma 0.75) melts pixel jaggies and JPEG blockiness; the whisper of
#   sharpening (0.25) keeps strokes from going soft. White margin 40 is
#   the scanner-look sweet spot: paper grain (which lives within ~40 of
#   white after levels) vanishes; genuinely faint notation is darker
#   than that and survives. Despeckle 0.05 staff spaces squared (~7px at
#   12px spacing) clears grain blobs while staccato/augmentation dots
#   (12px+) and staff-line fragments stay.
#
# extreme — maximum punch for mushy sources, accepting harsher edges:
#   the darkest-percentile anchor (0.5) crushed toward black (target 30),
#   gamma 1.35 drags midtones down with it - faint pencil becomes solid
#   ink, and everything short of a perfect scan gets remapped (span gate
#   240). White margin 60 erases even heavy grain but also swallows the
#   very faintest marks. Sharpen 1.2 deliberately pairs with a LARGER
#   radius (0.75 staff spaces): at that strength a small radius amplifies
#   paper grain instead of strokes. Despeckle 0.12 (~17px) starts to eat
#   small staccato dots - only use it when the source is truly speckled.
#   When it goes too far back off SHARPEN_AMOUNT first, then
#   CONTRAST_GAMMA, then CONTRAST_INK_TARGET.

CONTRAST_INK_PCT = 2.0      # percentile within ink pixels defining the black anchor
                            # (lower = only the darkest ink defines black -> stronger pull)
CONTRAST_INK_TARGET = 55.0  # brightness the black anchor is remapped to (lower = punchier)
CONTRAST_GAMMA = 1.05       # midtone gamma applied after the remap (>1 darkens midtones)
CONTRAST_MIN_SPAN = 200.0   # remap only pages whose ink-paper span is narrower than this;
                            # pages already this contrasty are left alone
EDGE_SMOOTH_SIGMA = 0.75    # gentle blur that melts pixel jaggies and JPEG blocks on
                            # stroke edges (0 = off); keeps the page looking scanned,
                            # not crystallized. Heavy values thin faint 1px staff lines.
PAPER_WHITE_MARGIN = 40.0   # grayscale tones within this distance of 255 saturate to pure
                            # white: paper grain lives here. Trade-off: marks only
                            # slightly darker than paper are erased with it.
SHARPEN_AMOUNT = 0.25       # unsharp-mask strength (0 = off; 0.5 subtle, 2 very crisp)
SHARPEN_SIGMA_SCALE = 0.5   # unsharp radius = this * staff spacing (px); raise when
                            # raising amount, so grain is not amplified ahead of strokes
DESPECKLE_AREA_SCALE = 0.05 # drop ink blobs (per the Sauvola mask) whose area is at most
                            # this * staff_spacing^2 px (grain clusters); musical dots
                            # and staff-line fragments are larger and survive


def load_grayscale(path: Path) -> np.ndarray:
    """Load an image as grayscale, honoring EXIF orientation."""
    from PIL import Image, ImageOps

    with Image.open(path) as im:
        im = ImageOps.exif_transpose(im)
        return np.array(im.convert("L"))


def save_image(arr: np.ndarray, path: Path) -> None:
    """Save a grayscale array as PNG (Pillow handles non-ASCII paths)."""
    from PIL import Image

    path.parent.mkdir(parents=True, exist_ok=True)
    Image.fromarray(arr).save(path)


# --- measurement --------------------------------------------------------


def otsu_ink(gray: np.ndarray) -> np.ndarray:
    """Rough ink mask (255 = ink) via global Otsu; used only for measurement."""
    _, ink = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
    return ink


def paper_stats(gray: np.ndarray) -> dict:
    """Spatial paper flatness: mean and std of per-cell paper means.

    A 10x10 grid of non-ink pixel means measures large-scale shading
    (what illumination correction should remove) without conflating
    paper grain or anti-aliasing with unevenness.
    """
    h, w = gray.shape
    ink = otsu_ink(gray) > 0
    if ink.mean() > 0.5:
        return {"mean": round(float(gray.mean()), 1), "std": 0.0}
    ys = np.linspace(0, h, 11).astype(int)
    xs = np.linspace(0, w, 11).astype(int)
    cell_means = []
    for i in range(10):
        for j in range(10):
            cell_paper = gray[ys[i]:ys[i + 1], xs[j]:xs[j + 1]][
                ~ink[ys[i]:ys[i + 1], xs[j]:xs[j + 1]]
            ]
            if cell_paper.size:
                cell_means.append(float(cell_paper.mean()))
    if not cell_means:
        return {"mean": 0.0, "std": 0.0}
    return {
        "mean": round(float(np.mean(cell_means)), 1),
        "std": round(float(np.std(cell_means)), 1),
    }


def estimate_skew(
    gray: np.ndarray,
    max_angle: float = 3.0,
    min_lines: int = SKEW_MIN_LINES,
) -> tuple[float, int]:
    """Estimate in-plane page skew in degrees from long near-horizontal lines.

    Staff lines are the dominant long horizontal structures in sheet music,
    so the length-weighted median of Hough segment angles near 0° is a
    reliable skew estimate. Returns (angle, line_count); angle is 0.0 when
    too few lines agree.
    """
    h, w = gray.shape
    ink = otsu_ink(gray)
    lines = cv2.HoughLinesP(
        ink,
        1,
        np.pi / 720,
        threshold=100,
        minLineLength=max(w // 4, 50),
        maxLineGap=20,
    )
    if lines is None:
        return 0.0, 0
    angles = []
    for x1, y1, x2, y2 in np.asarray(lines).reshape(-1, 4):
        angle = float(np.degrees(np.arctan2(float(y2) - float(y1), float(x2) - float(x1))))
        if abs(angle) <= max_angle:
            angles.append(angle)
    if len(angles) < min_lines:
        return 0.0, len(angles)
    return float(np.median(angles)), len(angles)


def estimate_staff_space(gray: np.ndarray) -> tuple[int, list[int]]:
    """Estimate vertical staff-line spacing in pixels.

    Binarizes roughly, projects ink onto rows, and autocorrelates the row
    profile: evenly spaced staff lines show the first strong peak at the
    line spacing. All later kernel sizes scale with this value, which makes
    the pipeline resolution-independent. Returns (spacing, peaks);
    falls back to DEFAULT_STAFF_SPACE when no clean peak is found.
    """
    h = gray.shape[0]
    prof = otsu_ink(gray).astype(np.float32).sum(axis=1)
    prof -= prof.mean()
    var = float((prof * prof).sum())
    if var <= 0:
        return DEFAULT_STAFF_SPACE, []
    acf = np.correlate(prof, prof, mode="full")[len(prof) - 1:] / var
    peaks = [
        lag
        for lag in range(6, min(h // 3, 400))
        if acf[lag] > acf[lag - 1] and acf[lag] >= acf[lag + 1] and acf[lag] > 0.2
    ]
    if not peaks:
        return DEFAULT_STAFF_SPACE, []
    return int(peaks[0]), peaks[:6]


def _isolated_speck_mask(gray: np.ndarray) -> np.ndarray:
    """Dark pixels with no dark neighbor in their 3x3 neighborhood.

    Only truly isolated pixels qualify, so any connected structure —
    including 1px staff lines, stems, and small dots — is never noise.
    """
    ink = otsu_ink(gray) > 0
    if ink.mean() > 0.5:  # degenerate image (no paper); Otsu unusable
        return np.zeros_like(ink)
    neighbor_count = cv2.boxFilter(ink.astype(np.float32), -1, (3, 3), normalize=False)
    return ink & (neighbor_count <= 1.0)


def measure_noise(gray: np.ndarray) -> float:
    """Isolated-speck noise level: percent of pixels that are lone dark
    dots on paper (photocopy speckle, sensor dust, salt noise)."""
    return float(100.0 * _isolated_speck_mask(gray).mean())


def detect_dark_border(gray: np.ndarray, ratio: float = DARK_BORDER_RATIO) -> bool:
    """True when the outer frame band is much darker than the paper.

    Common on photocopies where the platen edge prints black; the fix
    (cropping) is left to the user because staff lines legitimately run
    to the page edges.
    """
    h, w = gray.shape
    band = max(3, min(h, w) // 100)
    frame = np.concatenate([
        gray[:band].ravel(),
        gray[-band:].ravel(),
        gray[:, :band].ravel(),
        gray[:, -band:].ravel(),
    ])
    paper = float(np.percentile(gray, 90))
    if paper <= 0:
        return False
    return float(frame.mean()) < ratio * paper


# --- geometry ------------------------------------------------------------


def deskew(gray: np.ndarray, angle_deg: float) -> np.ndarray:
    """Rotate by -angle_deg around the center, filling borders with the
    paper brightness so corners don't flash white on dark scans."""
    h, w = gray.shape
    border = float(np.percentile(gray, 75))
    M = cv2.getRotationMatrix2D((w / 2, h / 2), angle_deg, 1.0)
    return cv2.warpAffine(
        gray,
        M,
        (w, h),
        flags=cv2.INTER_LINEAR,
        borderMode=cv2.BORDER_CONSTANT,
        borderValue=border,
    )


# --- tone ----------------------------------------------------------------


def estimate_background(
    gray: np.ndarray,
    staff_space: int,
    method: str = "morph",
    scale: float = 4.0,
) -> np.ndarray:
    """Estimate the slowly varying paper brightness under the notation.

    morph (default): dilate with an elliptical kernel of 2*scale*staff_space
    (a max filter that sees past solid marks up to that size - noteheads,
    fat title letters, beams), then blur with sigma = scale*staff_space to
    smooth the dilation steps into a realistic shading field.
    gaussian: blur with sigma = scale*staff_space. Smooth and cheap, but
    dense or large dark regions (title blocks) leak into the estimate and
    get partially washed out by the later division.
    """
    if method == "morph":
        k = max(int(2 * scale * staff_space) | 1, 9)
        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (k, k))
        bg = cv2.dilate(gray, kernel)
        return cv2.GaussianBlur(bg, (0, 0), max(scale * float(staff_space), 3.0))
    sigma = max(scale * float(staff_space), 5.0)
    return cv2.GaussianBlur(gray, (0, 0), sigma)


def background_range(background: np.ndarray) -> float:
    """Spread of the background estimate (p95 - p5): how uneven the page is."""
    return float(np.percentile(background, 95) - np.percentile(background, 5))


def needs_illumination(background: np.ndarray, flat_range: float = FLAT_BG_RANGE) -> bool:
    """Division correction only pays off when illumination is actually uneven;
    on already-flat scans it just amplifies noise, so it is skipped."""
    return background_range(background) >= flat_range


def correct_illumination(
    gray: np.ndarray,
    background: np.ndarray,
    paper_target: int = PAPER_TARGET,
    floor_ratio: float = BG_FLOOR_RATIO,
) -> np.ndarray:
    """Divide out the paper brightness: I/bg * paper_target.

    The background is floored at floor_ratio * (p90 of background): inside
    large solid ink regions the estimate collapses to the ink itself and
    plain division would erase the region (white hole); the floor keeps
    solid blacks black while still lifting shadows.
    """
    bg_ref = float(np.percentile(background, 90))
    floor = max(floor_ratio * bg_ref, 1.0)
    bg = np.maximum(background.astype(np.float32), floor)
    corrected = gray.astype(np.float32) / bg * float(paper_target)
    return np.clip(corrected, 0, 255).astype(np.uint8)


def apply_levels(
    gray: np.ndarray,
    anchor_pct: float = PAPER_ANCHOR_PCT,
    max_gain: float = MAX_PAPER_GAIN,
) -> np.ndarray:
    """Normalize the paper to white: multiply by 255 / paper brightness.

    The anchor is a high brightness percentile (paper), so ink is scaled
    by the same gain but never stretched or clipped: faint notation keeps
    its relative contrast and paper grain is not amplified, unlike a full
    black-point/white-point stretch.
    """
    anchor = float(np.percentile(gray, anchor_pct))
    if anchor <= 0:
        return gray
    gain = min(255.0 / anchor, max_gain)
    return np.clip(gray.astype(np.float32) * gain, 0, 255).astype(np.uint8)


def apply_contrast(
    gray: np.ndarray,
    ink_pct: float = CONTRAST_INK_PCT,
    ink_target: float = CONTRAST_INK_TARGET,
    gamma: float = CONTRAST_GAMMA,
    min_span: float = CONTRAST_MIN_SPAN,
) -> np.ndarray:
    """Aggressive linear contrast remap: black anchor -> ink_target,
    paper -> 255, then a gamma tilt for darker midtones.

    The black anchor is a low percentile of ink-pixel brightness (below
    Otsu), so faint notation is pulled toward true black without touching
    the paper. Skipped when the ink-paper span is already at least
    `min_span` wide: on contrasty pages the remap would only fatten
    strokes or wash ink, so they pass through untouched.
    """
    thr, _ = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    ink_pixels = gray[gray <= thr]
    if ink_pixels.size == 0:
        return gray
    black = float(np.percentile(ink_pixels, ink_pct))
    paper = float(np.percentile(gray, PAPER_ANCHOR_PCT))
    if paper - black >= min_span:
        return gray
    scale = (255.0 - ink_target) / (paper - black)
    out = ink_target + (gray.astype(np.float32) - black) * scale
    out = 255.0 * np.clip(out / 255.0, 0.0, 1.0) ** gamma
    return np.clip(out, 0, 255).astype(np.uint8)


def sharpen(
    gray: np.ndarray,
    staff_space: int,
    amount: float = SHARPEN_AMOUNT,
    sigma_scale: float = SHARPEN_SIGMA_SCALE,
) -> np.ndarray:
    """Unsharp mask sized to the notation: radius = sigma_scale * staff
    spacing, so staff-line thickness and stem edges are crispened without
    paper-grain-scale noise being amplified. Run after denoise."""
    if amount <= 0:
        return gray
    sigma = max(sigma_scale * float(staff_space), 0.5)
    blur = cv2.GaussianBlur(gray, (0, 0), sigma)
    out = gray.astype(np.float32) + amount * (gray.astype(np.float32) - blur)
    return np.clip(out, 0, 255).astype(np.uint8)


def denoise(gray: np.ndarray) -> np.ndarray:
    """Remove isolated single-pixel specks, filling them with the local
    paper level (3x3 max). Structurally safe: every connected structure —
    1px staff lines, stems, staccato/augmentation dots — survives because
    its pixels have dark neighbors."""
    isolated = _isolated_speck_mask(gray)
    if not isolated.any():
        return gray
    fill = cv2.dilate(gray, cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3)))
    out = gray.copy()
    out[isolated] = fill[isolated]
    return out


def sauvola_k_for(noise: float) -> float:
    """Speckled scans get a more conservative Sauvola k so binarization
    doesn't shatter paper grain into specks."""
    return SAUVOLA_K_NOISY if noise >= SAUVOLA_NOISE_THRESHOLD else SAUVOLA_K_BASE


def sauvola_binary(gray: np.ndarray, window: int, k: float) -> np.ndarray:
    """Sauvola local thresholding via box-filter mean/std (integral-image
    math), equivalent to scikit-image's threshold_sauvola without the heavy
    dependency: T = mean * (1 + k * (std/128 - 1))."""
    h, w = gray.shape
    win = max(3, min(window, min(h, w)) | 1)
    g = gray.astype(np.float32)
    mean = cv2.boxFilter(g, -1, (win, win), normalize=True)
    sq = cv2.boxFilter(g * g, -1, (win, win), normalize=True)
    std = np.sqrt(np.maximum(sq - mean * mean, 0.0))
    threshold = mean * (1.0 + k * (std / 128.0 - 1.0))
    return np.where(gray > threshold, 255, 0).astype(np.uint8)


def saturate_white(
    gray: np.ndarray,
    margin: float = PAPER_WHITE_MARGIN,
) -> np.ndarray:
    """Document-scanner restoration: every tone within `margin` of pure
    white becomes pure white.

    This is what removes paper grain: after levels, grain lives just
    below 255 while real notation is far darker, so saturating the top of
    the range erases the photo texture without touching the music. The
    trade-off is that marks only slightly darker than paper (very faint
    pencil) are erased together with the grain."""
    if margin <= 0:
        return gray
    return np.where(gray >= 255.0 - margin, 255, gray).astype(np.uint8)


def smooth_edges(gray: np.ndarray, sigma: float = EDGE_SMOOTH_SIGMA) -> np.ndarray:
    """Gentle blur that melts pixel-scale jaggies and JPEG blockiness on
    stroke edges, so the restored page looks scanned rather than
    crystallized (0 disables). Deliberately subtle: a heavy blur would
    thin faint 1px staff lines and soften small marks."""
    if sigma <= 0:
        return gray
    return cv2.GaussianBlur(gray, (0, 0), sigma)


def speck_mask(
    binary: np.ndarray,
    staff_space: int,
    area_scale: float = DESPECKLE_AREA_SCALE,
) -> tuple[np.ndarray, int]:
    """Boolean mask (True = speck) of ink components whose area is at
    most area_scale * staff_spacing^2 pixels — photocopy speckle, sensor
    dust, grain clusters — plus how many components were flagged.

    Area-filtered, not morphological: 1px staff lines and stems are long
    (large area) so they survive, and every connected musical mark
    (staccato/augmentation dots included) is either bigger than the grain
    cutoff or part of a bigger structure."""
    ink = (binary == 0).astype(np.uint8)
    n, labels, stats, _ = cv2.connectedComponentsWithStats(ink, connectivity=8)
    if n <= 1:
        return np.zeros_like(ink, dtype=bool), 0
    max_area = max(4.0, area_scale * float(staff_space) ** 2)
    remove = np.zeros(n, dtype=bool)
    remove[1:] = stats[1:, cv2.CC_STAT_AREA] <= max_area
    return remove[labels], int(remove.sum())


def despeckle_binary(
    binary: np.ndarray,
    staff_space: int,
    area_scale: float = DESPECKLE_AREA_SCALE,
) -> tuple[np.ndarray, int]:
    """Drop grain-sized ink blobs from a 1-bit page (thin wrapper over
    speck_mask). Returns (cleaned, n_removed)."""
    mask, removed = speck_mask(binary, staff_space, area_scale)
    if not removed:
        return binary, 0
    out = binary.copy()
    out[mask] = 255
    return out, removed


# --- diagnostics ----------------------------------------------------------


def make_preview(rows: list[list[np.ndarray]], width: int = 700) -> np.ndarray:
    """Contact sheet: one row of panels per page, panels scaled to `width`.

    Each row has 2 panels (original | clean). A 4px white gutter
    separates panels and rows.
    """
    scaled_rows: list[np.ndarray] = []
    for row in rows:
        panels = []
        row_h = 0
        for img in row:
            h, w = img.shape[:2]
            scale = width / float(w)
            resized = cv2.resize(img, (width, max(1, int(round(h * scale)))))
            panels.append(resized)
            row_h = max(row_h, resized.shape[0])
        padded = []
        for panel in panels:
            if panel.shape[0] < row_h:
                pad = np.full((row_h - panel.shape[0], width), 255, dtype=np.uint8)
                panel = np.vstack([panel, pad])
            padded.append(panel)
        scaled_rows.append(np.hstack(padded))
    total_w = max(r.shape[1] for r in scaled_rows)
    gutter = np.full((4, total_w), 255, dtype=np.uint8)
    out: list[np.ndarray] = []
    for r in scaled_rows:
        pad = np.full((r.shape[0], total_w - r.shape[1]), 255, dtype=np.uint8)
        out.append(np.hstack([r, pad]))
        out.append(gutter)
    return np.vstack(out)
