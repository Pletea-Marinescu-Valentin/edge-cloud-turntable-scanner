"""Rebuilds the paper from its sources (cross-platform alternative to the Makefile).

  python scripts/build.py            # figures, PDF, checks and dist/ (same as "all")
  python scripts/build.py figures    # only the Python figures in paper/figs/
  python scripts/build.py paper      # only the PDF (latexmk; TikZ figures are compiled with the paper)
  python scripts/build.py check      # only the checks of scripts/check_paper.py
  python scripts/build.py dist       # copy the PDF to dist/ and pack the Overleaf archive
"""

import shutil
import subprocess
import sys
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PAPER = ROOT / "paper"
DIST = ROOT / "dist"
FIGURE_SCRIPTS = ["fig_geometry.py", "fig_result.py"]
OVERLEAF_FILES = ["main.tex", "refs.bib", "IEEEtran.cls", "IEEEtran.bst"]


def run(cmd, cwd):
    print("+", " ".join(cmd))
    subprocess.run(cmd, cwd=cwd, check=True)


def figures():
    for script in FIGURE_SCRIPTS:
        run([sys.executable, str(ROOT / "scripts" / script)], cwd=ROOT / "scripts")


def paper():
    run(["latexmk", "-pdf", "-interaction=nonstopmode", "-halt-on-error", "main.tex"], cwd=PAPER)


def check():
    run([sys.executable, str(ROOT / "scripts" / "check_paper.py")], cwd=ROOT)


def dist():
    DIST.mkdir(exist_ok=True)
    shutil.copy2(PAPER / "main.pdf", DIST / "edge-cloud-turntable-scanner.pdf")
    archive = DIST / "overleaf.zip"
    with zipfile.ZipFile(archive, "w", zipfile.ZIP_DEFLATED) as z:
        for name in OVERLEAF_FILES:
            z.write(PAPER / name, name)
        for fig in sorted((PAPER / "figs").iterdir()):
            z.write(fig, f"figs/{fig.name}")
    print(f"wrote {DIST / 'edge-cloud-turntable-scanner.pdf'} and {archive}")


STEPS = {"figures": [figures], "paper": [paper], "check": [check], "dist": [dist],
         "all": [figures, paper, check, dist]}

if __name__ == "__main__":
    target = sys.argv[1] if len(sys.argv) > 1 else "all"
    if target not in STEPS:
        sys.exit(f"unknown target '{target}'; use one of: {', '.join(STEPS)}")
    for step in STEPS[target]:
        step()
