#!/usr/bin/env python3
"""
Render Supplementary Table S12 (threshold robustness) from its markdown source
to a submittable .docx.

Why this file exists: R3-12 answers that the supplementary tables travel as
CSVs plus one workbook, with S12 supplied "as its own file rather than as a
workbook sheet" because it carries five panels of prose and tabulation. That
promise was made in the response letter while the only artefact on disk was
`S12_threshold_robustness.md` - a format no journal will typeset. This script
closes the gap.

The docx is a faithful rendering of the markdown, not a re-edit: every string
is carried across, so the two cannot drift. The only additions are structural -
a bold title, bold panel headings, and three-line rules on each table (the same
rule set R3-12 required of the main-text tables; the markdown source encodes no
borders at all).

Verification is built in rather than bolted on:
  * every markdown table row must appear in the docx, cell for cell;
  * every table must carry the three-line rule set (top 12, header-bottom 8,
    last-row bottom 12 half-points, no vertical or interior rules);
  * the document text must contain no leftover markdown markers.

Usage:
    python code/build_s12_docx.py                     # build + verify
    python code/build_s12_docx.py --check             # verify an existing file
"""

import argparse
import os
import sys

from docx import Document
from docx.enum.section import WD_SECTION
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.shared import Cm, Pt

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)

import md_to_docx_frontiers as cv  # noqa: E402

SRC = os.path.join(ROOT, "manuscript", "supplementary", "S12_threshold_robustness.md")
OUT = os.path.join(ROOT, "manuscript", "supplementary", "S12_threshold_robustness.docx")

TITLE_SIZE = 13
HEAD_SIZE = 11
SUBHEAD_SIZE = 10.5
BODY_SIZE = 10
RULE_TOP = 12
RULE_HEAD_BOTTOM = 8
RULE_LAST_BOTTOM = 12
MIN_COL_CM = 1.9   # keeps a numeric column from collapsing to a minimum-width sliver


# --------------------------------------------------------------------------
# markdown parsing
# --------------------------------------------------------------------------

def parse_md(path):
    """Return a list of blocks: ('title'|'head'|'subhead'|'para'|'table', payload)."""
    with open(path, encoding="utf-8") as fh:
        lines = fh.read().split("\n")

    blocks = []
    i = 0
    while i < len(lines):
        line = lines[i]
        stripped = line.strip()

        if stripped.startswith("|"):
            chunk = []
            while i < len(lines) and lines[i].strip().startswith("|"):
                chunk.append(lines[i])
                i += 1
            blocks.append(("table", cv.parse_table(chunk)))
            continue

        if stripped.startswith("### "):
            blocks.append(("subhead", stripped[4:].strip()))
        elif stripped.startswith("## "):
            blocks.append(("head", stripped[3:].strip()))
        elif stripped.startswith("# "):
            blocks.append(("title", stripped[2:].strip()))
        elif stripped:
            blocks.append(("para", stripped))
        i += 1
    return blocks


# --------------------------------------------------------------------------
# document assembly
# --------------------------------------------------------------------------

def setup(doc):
    sec = doc.sections[0]
    sec.page_width = Cm(21.0)
    sec.page_height = Cm(29.7)
    for edge in ("top_margin", "bottom_margin", "left_margin", "right_margin"):
        setattr(sec, edge, Cm(2.54))

    normal = doc.styles["Normal"]
    normal.font.name = cv.BODY_FONT
    normal.font.size = Pt(BODY_SIZE)
    normal.element.rPr.rFonts.set(cv.qn("w:eastAsia"), cv.BODY_FONT)
    pf = normal.paragraph_format
    pf.line_spacing = 1.15
    pf.space_before = Pt(0)
    pf.space_after = Pt(6)

    cv.add_page_number(sec)


def build(src=SRC, out=OUT):
    blocks = parse_md(src)
    doc = Document()
    setup(doc)

    for kind, payload in blocks:
        if kind == "title":
            p = cv.para(doc, payload, size=TITLE_SIZE, bold=True,
                        align=WD_ALIGN_PARAGRAPH.LEFT,
                        space_after=12, line=None)
            p.paragraph_format.keep_with_next = True
        elif kind == "head":
            p = cv.para(doc, payload, size=HEAD_SIZE, bold=True,
                        space_before=14, space_after=6, line=None)
            p.paragraph_format.keep_with_next = True
        elif kind == "subhead":
            p = cv.para(doc, payload, size=SUBHEAD_SIZE, bold=True,
                        space_before=10, space_after=4, line=None)
            p.paragraph_format.keep_with_next = True
        elif kind == "para":
            cv.para(doc, payload, size=BODY_SIZE, align=WD_ALIGN_PARAGRAPH.JUSTIFY,
                    space_after=6, line=None)
        elif kind == "table":
            widths = cv.column_widths(payload, total_cm=15.9, min_cm=MIN_COL_CM)
            cv.add_table(doc, payload, fixed_widths=widths)
            # tighten the trailing spacer the manuscript builder inserts
            spacer = doc.paragraphs[-1]
            spacer.paragraph_format.space_after = Pt(0)

    doc.save(out)
    return blocks


# --------------------------------------------------------------------------
# verification
# --------------------------------------------------------------------------

def _cell_borders(cell):
    tcPr = cell._tc.tcPr
    if tcPr is None:
        return {}
    out = {}
    for el in tcPr.findall(cv.qn("w:tcBorders")):
        for edge in el:
            tag = edge.tag.split("}")[1]
            out[tag] = edge.get(cv.qn("w:sz"))
    return out


def verify(src=SRC, out=OUT):
    problems = []

    if not os.path.exists(out):
        return ["output file does not exist: " + out]

    blocks = parse_md(src)
    md_tables = [p for k, p in blocks if k == "table"]

    doc = Document(out)
    if len(doc.tables) != len(md_tables):
        problems.append(f"table count {len(doc.tables)} != markdown {len(md_tables)}")

    for ti, rows in enumerate(md_tables):
        if ti >= len(doc.tables):
            break
        table = doc.tables[ti]
        if len(table.rows) != len(rows):
            problems.append(f"table {ti + 1}: {len(table.rows)} rows != {len(rows)}")
            continue
        for ri, row in enumerate(rows):
            got = [c.text.strip() for c in table.rows[ri].cells]
            want = [c.strip().replace("**", "").replace("`", "") for c in row]
            if got != want:
                problems.append(f"table {ti + 1} row {ri + 1}: {got} != {want}")
        # three-line rules
        for cell in table.rows[0].cells:
            b = _cell_borders(cell)
            if b.get("top") != str(RULE_TOP):
                problems.append(f"table {ti + 1}: header top rule {b.get('top')} != {RULE_TOP}")
                break
        for cell in table.rows[0].cells:
            b = _cell_borders(cell)
            if b.get("bottom") != str(RULE_HEAD_BOTTOM):
                problems.append(
                    f"table {ti + 1}: header bottom rule {b.get('bottom')} != {RULE_HEAD_BOTTOM}")
                break
        for cell in table.rows[-1].cells:
            b = _cell_borders(cell)
            if b.get("bottom") != str(RULE_LAST_BOTTOM):
                problems.append(
                    f"table {ti + 1}: last-row bottom rule {b.get('bottom')} != {RULE_LAST_BOTTOM}")
                break
        for row in table.rows:
            for cell in row.cells:
                b = _cell_borders(cell)
                if "insideV" in b or "left" in b or "right" in b or "insideH" in b:
                    problems.append(f"table {ti + 1}: interior or vertical rule present ({b})")
                    break

    text = "\n".join(p.text for p in doc.paragraphs)
    for marker in ("**", "`", "|---"):
        if marker in text:
            problems.append(f"markdown marker {marker!r} left in the document text")

    # the whole markdown prose must be present, not just the tables
    for kind, payload in blocks:
        if kind == "para" and payload.replace("`", "") not in text.replace("`", ""):
            problems.append(f"paragraph lost: {payload[:70]}...")
        if kind in ("title", "head", "subhead") and payload not in text:
            problems.append(f"heading lost: {payload}")

    return problems


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--src", default=SRC)
    ap.add_argument("--out", default=OUT)
    ap.add_argument("--check", action="store_true", help="verify only, do not rebuild")
    args = ap.parse_args()

    if not args.check:
        blocks = build(args.src, args.out)
        n_tab = sum(1 for k, _ in blocks if k == "table")
        print(f"wrote {os.path.relpath(args.out, ROOT)}")
        print(f"  blocks: {len(blocks)}, tables: {n_tab}")

    problems = verify(args.src, args.out)
    if problems:
        print(f"FAIL - {len(problems)} problem(s)")
        for p in problems:
            print("  -", p)
        return 1

    doc = Document(args.out)
    print("PASS")
    print(f"  tables: {len(doc.tables)}  paragraphs: {len(doc.paragraphs)}")
    print(f"  three-line rules: {len(doc.tables)}/{len(doc.tables)} tables")
    return 0


if __name__ == "__main__":
    sys.exit(main())
