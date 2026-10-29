"""scanprep: raw scanned sheet-music image -> clean, OMR-ready page images.

Adaptive pre-processing for low-quality scans and photocopies of sheet
music: deskew, staff-metric estimation, illumination/background
correction, contrast levels, selective denoising, and optional Sauvola
binarization. Pages are cleaned in place: raws are renamed to
"<stem> (original)<ext>" and cleaned pages written as "<stem>.png", so
image2ly run on the same directory picks up exactly the cleaned pages.

All kernel sizes and thresholds derive from per-page measurements
(staff-line spacing, background flatness, noise level), so heterogeneous
inputs converge on a uniform output quality instead of assuming one
fixed scan profile.
"""

__version__ = "0.1.0"
