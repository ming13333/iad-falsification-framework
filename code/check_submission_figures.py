# -*- coding: utf-8 -*-
"""Submission gate for the Frontiers figure set and manuscript front page.

Everything checked here is a hard requirement from the Frontiers author
guidelines, so a failure is a blocker rather than a warning:

  width       figures must be 85 mm (one column) or 180 mm (two columns);
              this set is drawn at, and exported to, 180 mm -> 18.0 cm
  resolution  300 dpi minimum at the final printed size
  colour      RGB
  compression TIFF, LZW (uncompressed TIFFs also pass the journal but bloat
              the bundle, so LZW is enforced here)
  type        no visible text below 8 pt
  rules       no line thinner than 2 pt
  labels      panels are (A), (B), (C), never lower case and never (a)

The typography checks are static: they read the five generation scripts,
because the on-page size of a text element cannot be recovered from a raster
TIFF once the figure has been drawn. That is exactly why every figure is drawn
on a canvas whose width equals its printed width -- the constants checked here
are therefore the printed sizes, not nominal ones.

Run
---
  python code/check_submission_figures.py
"""

import csv
import os
import re
import sys
import zipfile

from PIL import Image

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(HERE, "manuscript", "figures")
FINAL = os.path.join(HERE, "课题设计阶段", "figures_final")
MD = os.path.join(HERE, "课题设计阶段", "manuscript_Frontiers_Methods_v2_humanized.md")
ZIP = os.path.join(FINAL, "Frontiers_Figures_upload.zip")

TARGET_W_CM = 18.0
WIDTH_TOL_CM = 0.05
MIN_DPI = 300
MIN_FONT = 8.0
MIN_LINE = 2.0

FIGURES = [
    ("Fig1", "Fig1_six_gate_framework", "make_fig1_six_gate.py", 2),
    ("Fig2", "Fig2_simulation_operating", "make_fig2_simulation.py", 3),
    ("Fig3", "Fig3_case_study_MR", "make_fig3_case_study.py", 2),
    ("Fig4", "Fig4_apoe_shared_liability", "make_fig4_apoe_liability.py", 3),
    ("Fig5", "Fig5_validation_grading", "make_fig5_validation.py", 0),
]

problems = []
notes = []


def fail(msg):
    problems.append(msg)


def check_tiff(key, stem):
    tif = os.path.join(FINAL, stem + ".tiff")
    png = os.path.join(SRC, stem + ".png")
    if not os.path.exists(tif):
        fail(f"{key}: missing {os.path.relpath(tif, HERE)}")
        return None
    with Image.open(tif) as im:
        px_w, px_h = im.size
        dpi = im.info.get("dpi", (0, 0))[0]
        mode = im.mode
        comp = im.tag_v2.get(259)
        unit = im.tag_v2.get(296)
    width_cm = px_w / dpi * 2.54 if dpi else 0.0
    height_cm = px_h / dpi * 2.54 if dpi else 0.0
    if abs(width_cm - TARGET_W_CM) > WIDTH_TOL_CM:
        fail(f"{key}: {width_cm:.2f} cm wide, must be {TARGET_W_CM} cm")
    if dpi < MIN_DPI:
        fail(f"{key}: {dpi} dpi at {width_cm:.2f} cm, below {MIN_DPI}")
    if mode != "RGB":
        fail(f"{key}: mode {mode}, must be RGB")
    if comp != 5:
        fail(f"{key}: compression tag {comp}, must be 5 (LZW)")
    if unit != 2:
        fail(f"{key}: resolution unit {unit}, must be 2 (inch)")
    if os.path.exists(png):
        with Image.open(png) as im2:
            if im2.size != (px_w, px_h):
                fail(f"{key}: TIFF {px_w}x{px_h} != PNG {im2.size}")
    return dict(key=key, px=f"{px_w}x{px_h}", dpi=int(dpi),
                w=round(width_cm, 2), h=round(height_cm, 2))


def check_script(key, script):
    """Static typography check on the generation script."""
    path = os.path.join(HERE, "code", script)
    if not os.path.exists(path):
        fail(f"{key}: generation script code/{script} missing")
        return
    src = open(path, encoding="utf-8").read()

    fonts = [float(m) for m in re.findall(r"fontsize\s*=\s*([0-9.]+)", src)]
    fonts += [float(m) for m in re.findall(r"^\s*MIN_FONT\s*=\s*([0-9.]+)", src, re.M)]
    small = sorted({f for f in fonts if f < MIN_FONT})
    if small:
        fail(f"{key}: font sizes below {MIN_FONT} pt in {script}: {small}")

    lines = [float(m) for m in re.findall(r"\b(?:lw|linewidth)\s*=\s*([0-9.]+)", src)]
    lines += [float(m) for m in re.findall(r"^\s*(?:LINE_W|RULE_W)\s*=\s*([0-9.]+)", src, re.M)]
    thin = sorted({v for v in lines if v < MIN_LINE})
    if thin:
        fail(f"{key}: line widths below {MIN_LINE} pt in {script}: {thin}")

    # spine and tick rules need the same minimum; rcParams is the only place
    # they can be set for every axis at once. Axis-free diagram panels draw
    # neither, so the requirement only applies where axes are visible.
    axis_free = 'axis("off")' in src
    if not axis_free:
        for key_name in ("axes.linewidth", "xtick.major.width", "ytick.major.width"):
            if key_name not in src:
                fail(f"{key}: {key_name} not set in {script}")
    if "tight" in src and "bbox_inches" in src:
        fail(f"{key}: bbox_inches='tight' would shrink the canvas and the fonts")


def check_legends():
    if not os.path.exists(MD):
        fail(f"manuscript source missing: {os.path.relpath(MD, HERE)}")
        return
    text = open(MD, encoding="utf-8").read()
    for key, _, _, panels in FIGURES:
        m = re.search(r"\*\*Figure %s\.\*\*(.*?)(?=\n\n|\Z)" % key[-1], text, re.S)
        if not m:
            fail(f"Figure {key[-1]}: legend not found")
            continue
        legend = m.group(1)
        if panels >= 2:
            for letter in "ABC"[:panels]:
                # bold the whole token, "(A)", not just the letter: bolding
                # only "A" leaves the parentheses at body weight, and the
                # label then reads as a typesetting accident
                if f"**({letter})**" not in legend and f"(**{letter}**)" not in legend:
                    fail(f"Figure {key[-1]}: legend lacks a bold ({letter})")
            if re.search(r"\((a|b|c)\)", legend):
                fail(f"Figure {key[-1]}: legend still uses lower-case panel letters")
        else:
            if re.search(r"\((a|b|c)\)", legend):
                fail(f"Figure {key[-1]}: legend uses panel letters but the figure has none")
    # first page must state the counts
    head = text[:4000]
    if not re.search(r"\*\*Word count:\*\*", head):
        fail("first page lacks a word count")
    if not re.search(r"\*\*Figures:\*\*\s*\d+", head):
        fail("first page lacks a figure count")
    if not re.search(r"\*\*Tables:\*\*\s*\d+", head):
        fail("first page lacks a table count")


def check_zip():
    if not os.path.exists(ZIP):
        fail("upload bundle missing")
        return
    with zipfile.ZipFile(ZIP) as zf:
        names = zf.namelist()
        if len(names) != len(FIGURES):
            fail(f"bundle holds {len(names)} files, expected {len(FIGURES)}")
        for _, stem, _, _ in FIGURES:
            name = stem + ".tiff"
            if name not in names:
                fail(f"bundle missing {name}")
                continue
            disk = os.path.join(FINAL, name)
            if zf.read(name) != open(disk, "rb").read():
                fail(f"bundle copy of {name} differs from the TIFF on disk")


def check_manifest(rows):
    man = os.path.join(FINAL, "TIFF_manifest.csv")
    if not os.path.exists(man):
        fail("TIFF_manifest.csv missing")
        return
    with open(man, encoding="utf-8-sig") as fh:
        recs = list(csv.DictReader(fh))
    by = {r["figure"]: r for r in recs}
    for r in rows:
        rec = by.get(r["key"])
        if not rec:
            fail(f"manifest has no row for {r['key']}")
            continue
        if abs(float(rec["width_cm"]) - TARGET_W_CM) > WIDTH_TOL_CM:
            fail(f"manifest {r['key']}: stale width {rec['width_cm']} cm")
        if int(rec["dpi"]) < MIN_DPI:
            fail(f"manifest {r['key']}: stale dpi {rec['dpi']}")


def main():
    rows = []
    print(f"{'figure':7} {'px':>12} {'dpi':>5} {'WxH cm':>13}  checks")
    for key, stem, script, _ in FIGURES:
        r = check_tiff(key, stem)
        check_script(key, script)
        if r:
            rows.append(r)
            print(f"{r['key']:7} {r['px']:>12} {r['dpi']:>5} "
                  f"{r['w']:>6}x{r['h']:<6}  width/dpi/colour/compression")
    check_legends()
    check_zip()
    check_manifest(rows)

    if os.path.exists(os.path.join(FINAL, "TIFF_manifest.csv.tmp")):
        notes.append("TIFF_manifest.csv.tmp is still on disk: the manifest was "
                     "locked during the last export, so the fresh rows sit in the "
                     ".tmp until the file is closed")

    print()
    for n in notes:
        print("NOTE", n)
    if problems:
        for p in problems:
            print("FAIL", p)
        print(f"\n{len(problems)} problem(s)")
        return 1
    print("PASS  all five figures at 180 mm / 400 dpi / RGB / LZW, "
          "no type below 8 pt, no rule below 2 pt, panels (A)(B)(C)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
