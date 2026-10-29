"""scanprep: raw scanned sheet-music image -> clean, OMR-ready page images.

Adaptive pre-processing for low-quality scans and photocopies of sheet
music: deskew, staff-metric estimation, illumination/background
correction, contrast levels, document-scanner restoration (ink
solidifying, edge smoothing, paper whitening, despeckling), and an
internal Sauvola threshold for QC. The restored page keeps smooth
anti-aliased edges like a professionally scanned document; strict
black-and-white is opt-in. Pages are cleaned in place: raws are moved
as-is into an "original/" subdirectory and cleaned pages written as
"<stem>.png", so image2ly run on the same directory picks up exactly
the cleaned pages.

All kernel sizes and thresholds derive from per-page measurements
(staff-line spacing, background flatness, noise level), so heterogeneous
inputs converge on a uniform output quality instead of assuming one
fixed scan profile.
"""

__version__ = "0.1.0"
