#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Render a Supplementary Note (small, self-contained markdown) to DOCX.

Unlike `md_to_docx_frontiers.py`, this makes no assumption about manuscript
structure: it takes whatever headings, paragraphs, bullet lists and pipe tables
the file contains and lays them out. That matters because the supplementary
notes have no Abstract or Figure-legend section, and the manuscript renderer
stops with StopIteration on them.

Layout matches the other submission files: A4, 11 pt, 1.15 spacing, and tables
as three-line tables without vertical rules (R3-12).

Usage
-----
    python code/md_to_docx_note.py --in <note.md> --out <note.docx>
"""

import argparse
import re

from docx import Document
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Cm, Pt

BODY_FONT = "Times New Roman"
BODY_PT = 11


def _set_cell_border(cell, top=None, bottom=None):
    """Write tcBorders for one edge; sz is in eighths of a point."""
    tcPr = cell._tc.get_or_add_tcPr()
    borders = tcPr.find(qn("w:tcBorders"))
    if borders is None:
        borders = OxmlElement("w:tcBorders")
        tcPr.append(borders)
    for edge, sz in (("top", top), ("bottom", bottom)):
        if sz is None:
            continue
        el = borders.find(qn("w:" + edge))
        if el is None:
            el = OxmlElement("w:" + edge)
            borders.append(el)
        el.set(qn("w:val"), "single")
        el.set(qn("w:sz"), str(sz))
        el.set(qn("w:space"), "0")
        el.set(qn("w:color"), "000000")


def _three_line(table):
    """Clear all borders, then rule header top/bottom and table bottom."""
    tblPr = table._tbl.tblPr
    old = tblPr.find(qn("w:tblBorders"))
    if old is not None:
        tblPr.remove(old)
    none = OxmlElement("w:tblBorders")
    for edge in ("top", "left", "bottom", "right", "insideH", "insideV"):
        el = OxmlElement("w:" + edge)
        el.set(qn("w:val"), "none")
        el.set(qn("w:sz"), "0")
        none.append(el)
    tblPr.append(none)

    nrows = len(table.rows)
    for c in table.rows[0].cells:
        _set_cell_border(c, top=12, bottom=8)
    for c in table.rows[nrows - 1].cells:
        _set_cell_border(c, bottom=12)


def _add_runs(par, text):
    """Split on **bold** and *italic* and emit real Word runs."""
    for tok in re.split(r"(\*\*[^*]+\*\*|\*[^*]+\*)", text):
        if not tok:
            continue
        if tok.startswith("**") and tok.endswith("**") and len(tok) > 4:
            par.add_run(tok[2:-2]).bold = True
        elif tok.startswith("*") and tok.endswith("*") and len(tok) > 2:
            par.add_run(tok[1:-1]).italic = True
        else:
            par.add_run(tok)


def _md_cells(line):
    return [c.strip() for c in line.strip().strip("|").split("|")]


def build(src, dst, landscape=False, table_pt=9):
    lines = open(src, encoding="utf-8").read().split("\n")
    doc = Document()

    sec = doc.sections[0]
    if landscape:
        sec.page_width, sec.page_height = Cm(29.7), Cm(21.0)
        for m in ("top_margin", "bottom_margin", "left_margin", "right_margin"):
            setattr(sec, m, Cm(1.8))
    else:
        sec.page_width, sec.page_height = Cm(21.0), Cm(29.7)
        for m in ("top_margin", "bottom_margin", "left_margin", "right_margin"):
            setattr(sec, m, Cm(2.54))

    style = doc.styles["Normal"]
    style.font.name = BODY_FONT
    style.font.size = Pt(BODY_PT)
    style.element.rPr.rFonts.set(qn("w:eastAsia"), BODY_FONT)
    style.paragraph_format.line_spacing = 1.15
    style.paragraph_format.space_after = Pt(6)

    i = 0
    while i < len(lines):
        line = lines[i]
        s = line.strip()

        if not s:
            i += 1
            continue

        # fenced code block: keep verbatim, monospace, no justification
        if s.startswith("```"):
            j = i + 1
            block = []
            while j < len(lines) and not lines[j].strip().startswith("```"):
                block.append(lines[j])
                j += 1
            for raw in block:
                par = doc.add_paragraph()
                par.alignment = WD_ALIGN_PARAGRAPH.LEFT
                par.paragraph_format.space_after = Pt(0)
                par.paragraph_format.line_spacing = 1.0
                run = par.add_run(raw.rstrip() if raw.strip() else "")
                run.font.name = "Consolas"
                run.font.size = Pt(9)
                run.element.rPr.rFonts.set(qn("w:eastAsia"), "Consolas")
            doc.add_paragraph()
            i = j + 1
            continue

        # pipe table
        if s.startswith("|") and i + 1 < len(lines) and re.match(r"^\|[\s:|-]+\|$", lines[i + 1].strip()):
            header = _md_cells(s)
            rows = []
            j = i + 2
            while j < len(lines) and lines[j].strip().startswith("|"):
                rows.append(_md_cells(lines[j]))
                j += 1
            table = doc.add_table(rows=1 + len(rows), cols=len(header))
            table.alignment = WD_TABLE_ALIGNMENT.CENTER
            table.autofit = True
            for k, h in enumerate(header):
                cell = table.rows[0].cells[k]
                cell.text = ""
                _add_runs(cell.paragraphs[0], h)
                for r in cell.paragraphs[0].runs:
                    r.bold = True
                    r.font.size = Pt(table_pt)
            for ri, row in enumerate(rows, start=1):
                for k in range(len(header)):
                    cell = table.rows[ri].cells[k]
                    cell.text = ""
                    _add_runs(cell.paragraphs[0], row[k] if k < len(row) else "")
                    for r in cell.paragraphs[0].runs:
                        r.font.size = Pt(table_pt)
            _three_line(table)
            doc.add_paragraph()
            i = j
            continue

        # headings
        m = re.match(r"^(#{1,4})\s+(.*)$", s)
        if m:
            level = len(m.group(1))
            par = doc.add_heading(level=min(level, 4))
            _add_runs(par, m.group(2))
            i += 1
            continue

        # bullets
        if re.match(r"^[-*]\s+", s):
            par = doc.add_paragraph(style="List Bullet")
            _add_runs(par, re.sub(r"^[-*]\s+", "", s))
            i += 1
            continue

        # numbered
        if re.match(r"^\d+\.\s+", s):
            par = doc.add_paragraph(style="List Number")
            _add_runs(par, re.sub(r"^\d+\.\s+", "", s))
            i += 1
            continue

        par = doc.add_paragraph()
        par.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        _add_runs(par, s)
        i += 1

    doc.save(dst)
    return dst


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--in", dest="inp", required=True)
    ap.add_argument("--out", dest="out", required=True)
    ap.add_argument("--landscape", action="store_true", help="A4 landscape (for wide tables)")
    ap.add_argument("--table-pt", type=int, default=9, help="table font size in points")
    a = ap.parse_args()
    print("wrote", build(a.inp, a.out, landscape=a.landscape, table_pt=a.table_pt))
