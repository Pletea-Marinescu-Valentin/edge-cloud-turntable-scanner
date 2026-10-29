"""Checks the compiled paper against the submission rules and the house rules of this repository.

Run after a build (scripts/build.py does it automatically):
  python scripts/check_paper.py

Checks:
  * every BibTeX key in refs.bib is cited, and cited exactly once in main.tex;
  * the bibliography order of main.bbl equals the order of first citation (IEEEtran, unsorted);
  * the LaTeX log has no undefined references or citations, no errors and no overfull boxes;
  * ICE 2027 limits: at most 9 pages and at most 7000 words "all inclusive" (counted on the PDF text);
  * no forbidden phrasing ("not yet tested", "future measurements", ...);
  * the only tracked Markdown file is README.md.
"""

import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PAPER = ROOT / "paper"
MAX_PAGES, MAX_WORDS = 9, 7000
FORBIDDEN = [r"not yet tested", r"future measurements?", r"will be (measured|tested|evaluated)",
             r"remains? to be (measured|tested)", r"TODO", r"\?\?"]


def fail(errors, msg):
    errors.append(msg)
    print("FAIL", msg)


def tex_without_comments(text):
    return "\n".join(re.sub(r"(?<!\\)%.*$", "", line) for line in text.splitlines())


def main():
    errors = []
    tex = tex_without_comments((PAPER / "main.tex").read_text(encoding="utf-8"))
    bib = (PAPER / "refs.bib").read_text(encoding="utf-8")

    keys = re.findall(r"@\w+\{([^,\s]+),", bib)
    cites = [k.strip() for group in re.findall(r"\\cite\{([^}]*)\}", tex) for k in group.split(",")]
    for k in keys:
        n = cites.count(k)
        if n != 1:
            fail(errors, f"refs.bib key '{k}' is cited {n} times (must be exactly once)")
    for k in set(cites) - set(keys):
        fail(errors, f"cited key '{k}' is missing from refs.bib")
    print(f"citations: {len(cites)} cites, {len(keys)} entries")

    bbl = PAPER / "main.bbl"
    if bbl.exists():
        order = re.findall(r"\\bibitem\{([^}]+)\}", bbl.read_text(encoding="utf-8"))
        first = list(dict.fromkeys(cites))
        if order != first:
            fail(errors, "bibliography order differs from the order of first citation")
    else:
        fail(errors, "main.bbl not found (build the paper first)")

    log = (PAPER / "main.log").read_text(encoding="latin-1")
    for pat, what in [(r"undefined", "undefined reference or citation"), (r"^! ", "LaTeX error"),
                      (r"Overfull \\hbox", "overfull box"), (r"Rerun to get", "unresolved rerun")]:
        if re.search(pat, log, flags=re.M):
            fail(errors, f"main.log contains: {what}")

    pdf = PAPER / "main.pdf"
    info = subprocess.run(["pdfinfo", str(pdf)], capture_output=True, text=True).stdout
    pages = int(re.search(r"Pages:\s+(\d+)", info).group(1))
    text = subprocess.run(["pdftotext", "-enc", "UTF-8", str(pdf), "-"], capture_output=True).stdout.decode("utf-8")
    words = len(re.findall(r"[A-Za-z0-9][A-Za-z0-9\-.,/%'°]*", text))
    print(f"pages: {pages} (max {MAX_PAGES}), words in PDF: {words} (max {MAX_WORDS})")
    if pages > MAX_PAGES:
        fail(errors, f"{pages} pages > {MAX_PAGES}")
    if words > MAX_WORDS:
        fail(errors, f"{words} words > {MAX_WORDS}")

    flat = re.sub(r"\s+", " ", tex)
    for pat in FORBIDDEN:
        if re.search(pat, flat, flags=re.I):
            fail(errors, f"forbidden phrasing matched: {pat}")

    tracked = subprocess.run(["git", "ls-files"], cwd=ROOT, capture_output=True, text=True).stdout.split()
    md = [f for f in tracked if f.lower().endswith(".md")]
    if md and md != ["README.md"]:
        fail(errors, f"tracked Markdown files other than README.md: {md}")

    print("OK" if not errors else f"{len(errors)} problem(s)")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
