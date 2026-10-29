"""Shared figure style for the paper (IEEE two-column layout, Times-like text at 8 pt).

Colors: camera 1 and camera 2 take the first two slots of a categorical palette that was checked for
color-vision deficiency (blue/orange, all-pairs CVD Delta E 24.7 on white); every series also has its own
marker shape, so the figures stay readable in grayscale print.
"""

from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
FIGS = ROOT / "paper" / "figs"

COLUMN_IN = 3.5      # IEEE column width
TEXT_IN = 7.16       # IEEE text width (two columns)

CAM1 = "#2a78d6"     # camera 1 (blue)
CAM2 = "#eb6834"     # camera 2 (orange)
INK = "#0b0b0b"      # primary text
INK2 = "#52514e"     # secondary text
MUTED = "#898781"    # annotations
GRID = "#e1e0d9"     # hairline grid
AXIS = "#c3c2b7"     # axis lines
TAG = "#3a3936"      # printed AprilTags
DISC = "#f3f2ee"     # turntable paper


def apply():
    plt.rcParams.update({
        "font.family": "serif",
        "font.serif": ["Times New Roman", "STIXGeneral", "DejaVu Serif"],
        "mathtext.fontset": "stix",
        "font.size": 8,
        "axes.labelsize": 8,
        "axes.titlesize": 8,
        "xtick.labelsize": 7,
        "ytick.labelsize": 7,
        "legend.fontsize": 7,
        "axes.edgecolor": AXIS,
        "axes.labelcolor": INK,
        "axes.linewidth": 0.6,
        "xtick.color": INK2,
        "ytick.color": INK2,
        "xtick.major.width": 0.6,
        "ytick.major.width": 0.6,
        "xtick.major.size": 2.5,
        "ytick.major.size": 2.5,
        "grid.color": GRID,
        "grid.linewidth": 0.5,
        "lines.linewidth": 1.2,
        "lines.solid_capstyle": "round",
        "lines.solid_joinstyle": "round",
        "legend.frameon": False,
        "pdf.fonttype": 42,          # embed TrueType fonts (IEEE PDF eXpress)
        "savefig.bbox": "tight",
        "savefig.pad_inches": 0.02,
        "figure.dpi": 150,
    })


def save(fig, name):
    FIGS.mkdir(parents=True, exist_ok=True)
    out = FIGS / name
    # fixed metadata so that a rebuild produces the same file
    fig.savefig(out, metadata={"CreationDate": None, "Creator": "scripts/" + name.replace(".pdf", ".py")})
    plt.close(fig)
    print(f"wrote {out.relative_to(ROOT)}")
