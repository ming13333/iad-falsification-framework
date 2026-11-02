#!/usr/bin/env python3
"""
Apply the manuscript's three-line table rule set to an existing .docx.

Why this exists rather than a one-off patch: R3-12 answers the reviewer with a
single table convention - one rule above the header, one below it, one below
the last row, no vertical and no interior horizontal rules - and any file in
the package that renders differently undercuts that answer. The manuscript and
Supplementary Table S12 are built by md_to_docx_frontiers.py / build_s12_docx.py,
which draw the rules at cell level. Files that come from elsewhere (today:
S5_Checklist_STROBE-MR.docx, which carried the Word stock "Table Grid" style and
therefore a full grid of vertical rules) need the same treatment applied after
the fact, and applying it by hand is how conventions drift.

What it does to every table in the given document:

  1. clears tblBorders to "none" on all six edges, so no rule can arrive from
     the table style (Table Grid's insideV is what put vertical lines in S5);
  2. writes cell-level tcBorders: header row top sz=12, header row bottom sz=8,
     last row bottom sz=12, nothing on the other cells;
  3. switches the table to fixed layout with an explicit tblW equal to the
     section text width, and rescales the stored column widths proportionally
     to that width - an autofit table lets the renderer choose, and S5 stored
     widths totalling 18.29 cm on a 15.24 cm text column;
  4. marks the header row to repeat and stops rows from splitting across pages.

Nothing else is touched: fonts, text, paragraph styles and row order are left
exactly as they were, and the script asserts that before writing.

Usage:
    python code/apply_three_line_rules.py <file.docx> [...]
    python code/apply_three_line_rules.py <file.docx> --check
"""

import argparse
import os
import shutil
import sys
import tempfile

from docx import Document
from docx.oxml import OxmlElement
from docx.shared import Cm

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import md_to_docx_frontiers as cv  # noqa: E402

RULE_TOP = 12
RULE_HEAD_BOTTOM = 8
RULE_LAST_BOTTOM = 12


# --------------------------------------------------------------------------
# helpers
# --------------------------------------------------------------------------

def text_width_cm(doc):
    sec = doc.sections[0]
    # subtracting Length objects yields a plain int of EMU, so take each .cm first
    return sec.page_width.cm - sec.left_margin.cm - sec.right_margin.cm


def snapshot(doc):
    """Everything that must survive the operation, in comparable form."""
    paras = [p.text for p in doc.paragraphs]
    cells = []
    for t in doc.tables:
        cells.append([[c.text for c in row.cells] for row in t.rows])
    return paras, cells


def set_fixed_layout(table, widths_cm):
    tblPr = table._tbl.tblPr
    for tag in ("w:tblW", "w:tblLayout"):
        for el in tblPr.findall(cv.qn(tag)):
            tblPr.remove(el)

    tblW = OxmlElement("w:tblW")
    tblW.set(cv.qn("w:type"), "dxa")
    tblW.set(cv.qn("w:w"), str(int(round(sum(widths_cm) * 567))))
    tblPr.insert_element_before(
        tblW, "w:jc", "w:tblCellSpacing", "w:tblInd", "w:tblBorders", "w:shd",
        "w:tblLayout", "w:tblCellMar", "w:tblLook")

    layout = OxmlElement("w:tblLayout")
    layout.set(cv.qn("w:type"), "fixed")
    tblPr.insert_element_before(layout, "w:tblCellMar", "w:tblLook")


def clear_cell_borders(table):
    """Drop any cell-level rules first, so the run is idempotent."""
    for row in table.rows:
        for cell in row.cells:
            tcPr = cell._tc.tcPr
            if tcPr is None:
                continue
            for el in tcPr.findall(cv.qn("w:tcBorders")):
                tcPr.remove(el)


def apply_rules(doc, total_cm=None):
    if total_cm is None:
        total_cm = text_width_cm(doc)

    report = []
    for ti, table in enumerate(doc.tables):
        cv._borders_none(table)
        clear_cell_borders(table)

        stored = [c.width.cm if c.width else None for c in table.rows[0].cells]
        if any(w is None for w in stored):
            stored = [total_cm / len(stored)] * len(stored)
        share = sum(stored)
        widths = [w * total_cm / share for w in stored]

        set_fixed_layout(table, widths)
        for row in table.rows:
            cv._cant_split(row)
            for ci, cell in enumerate(row.cells):
                cell.width = Cm(widths[ci])
        cv._repeat_header(table.rows[0])

        for cell in table.rows[0].cells:
            cv._cell_border(cell, "top", RULE_TOP)
            cv._cell_border(cell, "bottom", RULE_HEAD_BOTTOM)
        for cell in table.rows[-1].cells:
            cv._cell_border(cell, "bottom", RULE_LAST_BOTTOM)

        report.append({
            "table": ti + 1,
            "rows": len(table.rows),
            "cols": len(table.columns),
            "stored_total_cm": round(share, 2),
            "applied_total_cm": round(sum(widths), 2),
        })
    return report


# --------------------------------------------------------------------------
# verification
# --------------------------------------------------------------------------

def cell_rules(cell):
    out = {}
    tcPr = cell._tc.tcPr
    if tcPr is None:
        return out
    for el in tcPr.findall(cv.qn("w:tcBorders")):
        for edge in el:
            out[edge.tag.split("}")[1]] = edge.get(cv.qn("w:sz"))
    return out


def verify(path):
    problems = []
    doc = Document(path)
    if not doc.tables:
        return ["no tables found"]

    width = text_width_cm(doc)

    for ti, table in enumerate(doc.tables):
        tblPr = table._tbl.tblPr
        borders = tblPr.find(cv.qn("w:tblBorders"))
        if borders is None:
            problems.append(f"table {ti + 1}: no tblBorders element")
        else:
            for edge in borders:
                if edge.get(cv.qn("w:val")) != "none":
                    problems.append(
                        f"table {ti + 1}: tblBorders {edge.tag.split('}')[1]} "
                        f"= {edge.get(cv.qn('w:val'))}")
        layout = tblPr.find(cv.qn("w:tblLayout"))
        if layout is None or layout.get(cv.qn("w:type")) != "fixed":
            problems.append(f"table {ti + 1}: layout is not fixed")

        total = sum((c.width.cm if c.width else 0) for c in table.rows[0].cells)
        if abs(total - width) > 0.05:
            problems.append(
                f"table {ti + 1}: column widths total {total:.2f} cm, "
                f"text width is {width:.2f} cm")

        for cell in table.rows[0].cells:
            r = cell_rules(cell)
            if r.get("top") != str(RULE_TOP) or r.get("bottom") != str(RULE_HEAD_BOTTOM):
                problems.append(f"table {ti + 1}: header rules {r}")
                break
        for cell in table.rows[-1].cells:
            r = cell_rules(cell)
            if r.get("bottom") != str(RULE_LAST_BOTTOM):
                problems.append(f"table {ti + 1}: last-row rule {r}")
                break
        for ri in range(1, len(table.rows) - 1):
            for cell in table.rows[ri].cells:
                r = cell_rules(cell)
                if r:
                    problems.append(f"table {ti + 1} row {ri + 1}: interior rules {r}")
                    break
        trPr = table.rows[0]._tr.trPr
        if trPr is None or trPr.find(cv.qn("w:tblHeader")) is None:
            problems.append(f"table {ti + 1}: header row does not repeat")

    return problems


# --------------------------------------------------------------------------
# entry point
# --------------------------------------------------------------------------

def process(path, check_only=False):
    if check_only:
        return verify(path)

    before = snapshot(Document(path))
    doc = Document(path)
    report = apply_rules(doc)

    after = snapshot(doc)
    if before != after:
        return ["text changed while applying rules - nothing was written"]

    fd, tmp = tempfile.mkstemp(suffix=".docx", dir=os.path.dirname(path))
    os.close(fd)
    doc.save(tmp)
    problems = verify(tmp)
    if problems:
        os.unlink(tmp)
        return problems
    shutil.move(tmp, path)

    for r in report:
        print(f"  table {r['table']}: {r['rows']}x{r['cols']} rows x cols, "
              f"widths {r['stored_total_cm']} -> {r['applied_total_cm']} cm")
    return []


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("files", nargs="+")
    ap.add_argument("--check", action="store_true", help="verify only, do not rewrite")
    args = ap.parse_args()

    failed = 0
    for path in args.files:
        rel = os.path.relpath(path, os.path.dirname(HERE))
        print(rel)
        problems = process(path, check_only=args.check)
        if problems:
            failed += 1
            print(f"  FAIL - {len(problems)} problem(s)")
            for p in problems:
                print("    -", p)
        else:
            print("  PASS")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
