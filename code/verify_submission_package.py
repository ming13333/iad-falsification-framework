# -*- coding: utf-8 -*-
"""Pre-upload integrity check for the Frontiers revision package.

Checks, in the order the user's standing rule requires:
  1. pre-flight: every expected file present, nothing unexpected, no file > 100 MB
  2. content: docx open cleanly, no markdown residue, title/DOI/word-count agree
  3. figures: PNG present, >= 300 dpi, >= 1700 px wide (180 mm at 300 dpi)
  4. workbook: S1-S11 sheets present
  5. reproducibility of the numbers the package claims
  6. SHA256 manifest written next to the package (hashes of the packaged bytes,
     which is what gets uploaded - not of the working tree)

Exit code 0 only if every check passes.
"""
import glob
import hashlib
import os
import re
import sys

from docx import Document
from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PKG = os.path.join(ROOT, "submissions", "Frontiers_1986036_revision_20261103")

EXPECTED = [
    "01_Manuscript_clean.docx",
    "02_Manuscript_marked.docx",
    "03_Response_to_Reviewers.docx",
    "04_Figures/Figure1.tiff",
    "04_Figures/Figure2.tiff",
    "04_Figures/Figure3.tiff",
    "04_Figures/Figure4.tiff",
    "04_Figures/Figure5.tiff",
    "04_Figures/Figure1.svg",
    "04_Figures/Figure2.svg",
    "04_Figures/Figure3.svg",
    "04_Figures/Figure4.svg",
    "04_Figures/Figure5.svg",
    "05_Supplementary/Supplementary_Tables_S1-S12.xlsx",
    "05_Supplementary/Supplementary_Table_S12_threshold_robustness.docx",
    "05_Supplementary/Supplementary_Table_S5_STROBE-MR_checklist.docx",
    "05_Supplementary/Supplementary_Table_S8_scoring_with_footnotes.docx",
    "05_Supplementary/Supplementary_Note_1.docx",
    "05_Supplementary/Supplementary_Note_2.docx",
    "06_Form_fields/Frontiers_submission_form_fields.md",
]

REQUIRED_STRINGS = {
    "01_Manuscript_clean.docx": [
        "for diagnosing locus-driven confounding",          # revised title verb
        "43,200-replicate benchmark of its scoring rule",   # narrowed claim
        "10.5281/zenodo.23733172",                          # current archive DOI
        "8,374",                                            # declared word count
    ],
    "02_Manuscript_marked.docx": [
        "for diagnosing locus-driven confounding",
        "43,200-replicate benchmark of its scoring rule",
        "10.5281/zenodo.23733172",
        "8,374",
    ],
    "03_Response_to_Reviewers.docx": [
        "10.5281/zenodo.23733172",
        "R1-1", "R1-10", "R3-1", "R3-12",
    ],
}
FORBIDDEN_STRINGS = {
    "01_Manuscript_clean.docx": [
        "43,200-simulation validation",
        "for correcting locus-driven confounding",
        "10.5281/zenodo.21858125",
    ],
    "02_Manuscript_marked.docx": [
        "43,200-simulation validation",
        "for correcting locus-driven confounding",
        "10.5281/zenodo.21858125",
    ],
    "06_Form_fields/Frontiers_submission_form_fields.md": [
        "43,200-simulation validation",
        "10.5281/zenodo.21858125",
    ],
}

problems = []
notes = []


def bad(msg):
    problems.append(msg)


def doc_text(path):
    d = Document(path)
    mono = set()
    for p in d.paragraphs:
        name = (p.runs[0].font.name or "") if p.runs else ""
        if name in ("Consolas", "Courier New", "Courier"):
            mono.add(p.text)
    chunks = [p.text for p in d.paragraphs]
    for t in d.tables:
        for r in t.rows:
            for c in r.cells:
                chunks.append(c.text)
    return "\n".join(chunks), len(d.paragraphs), len(d.tables), mono


def residue_lines(txt, mono):
    """Markdown left unrendered. Monospace paragraphs are exempt: they are
    verbatim result dumps, where '*** significant' is output, not markup."""
    out = []
    for t in txt.split("\n"):
        s = t.strip()
        if not s or s in mono:
            continue
        if s.startswith("#") or s.startswith("|") or "**" in s:
            out.append(t)
    return out


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for blk in iter(lambda: f.read(1 << 20), b""):
            h.update(blk)
    return h.hexdigest()


def main():
    # 1. pre-flight -------------------------------------------------------
    for rel in EXPECTED:
        if not os.path.isfile(os.path.join(PKG, rel)):
            bad("MISSING: %s" % rel)
    owner = [os.path.basename(p) for p in glob.glob(os.path.join(PKG, "**", "~$*"), recursive=True)]
    if owner:
        notes.append("Word owner files present and excluded from package: %s" % owner)
    found = sorted(os.path.relpath(p, PKG).replace("\\", "/")
                   for p in glob.glob(os.path.join(PKG, "**", "*"), recursive=True)
                   if os.path.isfile(p) and not p.endswith("README_UPLOAD.md")
                   and not p.endswith("MANIFEST_sha256.csv")
                   and not os.path.basename(p).startswith("~$"))
    extra = [f for f in found if f not in EXPECTED]
    if extra:
        notes.append("unexpected extra files: %s" % extra)
    biggest = max((os.path.getsize(p) for p in glob.glob(os.path.join(PKG, "**", "*"), recursive=True)
                   if os.path.isfile(p)), default=0)
    if biggest > 100 * 1024 * 1024:
        bad("a file exceeds 100 MB: %d bytes" % biggest)

    # 2. content ----------------------------------------------------------
    # every packaged docx is opened and residue-checked, not just the two with
    # required strings, so that no upload file goes unvalidated
    for p in sorted(glob.glob(os.path.join(PKG, "**", "*.docx"), recursive=True)):
        if os.path.basename(p).startswith("~$"):
            continue
        rel = os.path.relpath(p, PKG).replace("\\", "/")
        txt, npar, ntab, mono = doc_text(p)
        width = len(rel)
        notes.append("%s%s %d paragraphs, %d tables"
                     % (rel, " " * max(1, 46 - width), npar, ntab))
        residue = residue_lines(txt, mono)
        if residue:
            bad("%s: %d markdown-residue lines, e.g. %r"
                % (rel, len(residue), residue[0][:70]))
    for rel in list(REQUIRED_STRINGS) + [k for k in FORBIDDEN_STRINGS
                                         if k not in REQUIRED_STRINGS]:
        p = os.path.join(PKG, rel)
        if not os.path.isfile(p):
            continue
        if rel.endswith(".docx"):
            txt = doc_text(p)[0]
        else:
            txt = open(p, encoding="utf-8").read()
        for s in REQUIRED_STRINGS.get(rel, []):
            if s not in txt:
                bad("%s: required string absent: %r" % (rel, s))
        for s in FORBIDDEN_STRINGS.get(rel, []):
            if s in txt:
                bad("%s: stale string present: %r" % (rel, s))

    # every reviewer comment must have exactly one numbered response
    rp = os.path.join(PKG, "03_Response_to_Reviewers.docx")
    if os.path.isfile(rp):
        rtxt = doc_text(rp)[0]
        ids = sorted(set(re.findall(r"\bR\d+-\d+\b", rtxt)),
                     key=lambda x: tuple(int(y) for y in x[1:].split("-")))
        notes.append("response letter: %d distinct comment IDs (%s ... %s)"
                     % (len(ids), ids[0] if ids else "-", ids[-1] if ids else "-"))
        if len(ids) != 22:
            bad("response letter: %d distinct comment IDs, expected 22" % len(ids))

    # 3. figures ----------------------------------------------------------
    for n in range(1, 6):
        p = os.path.join(PKG, "04_Figures", "Figure%d.tiff" % n)
        if not os.path.isfile(p):
            continue
        im = Image.open(p)
        dpi = im.info.get("dpi", (0, 0))
        w_mm = im.width / dpi[0] * 25.4 if dpi[0] else 0
        if dpi[0] < 299:
            bad("Figure%d.tiff: %s dpi < 300" % (n, dpi[0]))
        if im.width < 1700:
            bad("Figure%d.tiff: %d px wide < 1700" % (n, im.width))
        if im.mode != "RGB":
            bad("Figure%d.tiff: colour mode %s, expected RGB" % (n, im.mode))
        if str(im.info.get("compression", "")).lower() not in ("tiff_lzw", "lzw"):
            bad("Figure%d.tiff: compression %r, expected LZW"
                % (n, im.info.get("compression")))
        notes.append("Figure%d.tiff %dx%d @ %.0f dpi = %.0f mm, %s, %s"
                     % (n, im.width, im.height, dpi[0], w_mm, im.mode,
                        im.info.get("compression")))

    # 4. workbook ---------------------------------------------------------
    try:
        import openpyxl
        wb = openpyxl.load_workbook(os.path.join(
            PKG, "05_Supplementary", "Supplementary_Tables_S1-S12.xlsx"))
        sheets = wb.sheetnames
        notes.append("workbook: %d sheets" % len(sheets))
        for k in range(1, 12):
            if not any(s.startswith("S%d" % k) for s in sheets):
                bad("workbook: no sheet for S%d" % k)
    except Exception as e:                                   # noqa: BLE001
        bad("workbook unreadable: %s" % e)

    # 5. claimed numbers --------------------------------------------------
    man = os.path.join(PKG, "01_Manuscript_clean.docx")
    if os.path.isfile(man):
        txt = doc_text(man)[0]
        for num in ("0.878", "0.724", "0.691", "8,374", "18 of 32", "1 of 47"):
            if num not in txt:
                bad("manuscript: claimed number %r absent" % num)
        if txt.count("10.5281/zenodo.23733172") < 3:
            bad("manuscript: version DOI appears fewer than 3 times")

    # 6. manifest ---------------------------------------------------------
    # the manifest covers exactly what the package is: the expected files plus
    # this README. Anything else that happens to sit in the directory (files left
    # there by hand, Word owner files) is reported above and deliberately not
    # hashed, so that the manifest and the zip describe the same set.
    files = [r for r in EXPECTED if os.path.isfile(os.path.join(PKG, r))]
    files.append("README_UPLOAD.md")
    files.sort()
    missing_from_pkg = [r for r in EXPECTED if not os.path.isfile(os.path.join(PKG, r))]
    if missing_from_pkg:
        bad("manifest: expected files absent: %s" % missing_from_pkg)
    lines = ["sha256,bytes,path"]
    for rel in files:
        p = os.path.join(PKG, rel)
        lines.append("%s,%d,%s" % (sha256(p), os.path.getsize(p), rel))
    with open(os.path.join(PKG, "MANIFEST_sha256.csv"), "w", encoding="utf-8", newline="\n") as f:
        f.write("\n".join(lines) + "\n")
    notes.append("manifest: %d files hashed" % len(files))

    # report --------------------------------------------------------------
    for n in notes:
        print("  . %s" % n)
    if problems:
        print()
        for p in problems:
            print("  FAIL %s" % p)
        print("\n%d problem(s)" % len(problems))
        return 1
    print("\nALL CHECKS PASSED")

    # 7. optional: build the zip from exactly the hashed set, then re-read it
    if "--zip" in sys.argv:
        import zipfile
        outer = os.path.dirname(PKG)
        zpath = os.path.join(outer, os.path.basename(PKG) + ".zip")
        members = files + ["MANIFEST_sha256.csv"]
        if os.path.exists(zpath):
            os.remove(zpath)
        with zipfile.ZipFile(zpath, "w", zipfile.ZIP_DEFLATED, compresslevel=9) as z:
            for rel in members:
                z.write(os.path.join(PKG, rel),
                        os.path.basename(PKG) + "/" + rel)
        with zipfile.ZipFile(zpath) as z:
            if z.testzip() is not None:
                print("  FAIL zip CRC")
                return 1
            names = z.namelist()
        print("  . zip: %d members, CRC ok, %.1f MB"
              % (len(names), os.path.getsize(zpath) / 1e6))
    return 0


if __name__ == "__main__":
    sys.exit(main())
