#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Convert the Genome Medicine markdown manuscript to a submission-compliant .docx.

Formatting enforced (BMC / Genome Medicine submission guidelines):
  - Font: Times New Roman 12 pt (body)
  - Line spacing: double throughout
  - Continuous line numbers in the margin
  - Page numbers (centred footer)
  - 1-inch (2.54 cm) margins all round
  - Real Word table objects (no shading, header row bold, bordered)
  - Superscripts (<sup>) for author/affiliation markers
  - Hanging-indent numbered reference list
"""
import re
from docx import Document
from docx.shared import Pt, Inches
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_LINE_SPACING
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

SRC = r"C:/D/workbuddy/科研/共病分析/课题设计阶段/manuscript_draft_with_23refs.md"
OUT = r"C:/D/workbuddy/科研/共病分析/课题设计阶段/manuscript_GenomeMedicine_submission.docx"

TOKEN_RE = re.compile(r'\*\*(.+?)\*\*|\*(.+?)\*|<sup>(.*?)</sup>')

def add_runs(par, text):
    """Add runs to a paragraph handling **bold**, *italic*, and <sup>..</sup>."""
    pos = 0
    for m in TOKEN_RE.finditer(text):
        if m.start() > pos:
            par.add_run(text[pos:m.start()])
        if m.group(1) is not None:
            r = par.add_run(m.group(1)); r.bold = True
        elif m.group(2) is not None:
            r = par.add_run(m.group(2)); r.italic = True
        elif m.group(3) is not None:
            r = par.add_run(m.group(3)); r.font.superscript = True
        pos = m.end()
    if pos < len(text):
        par.add_run(text[pos:])

def is_sep(line):
    s = line.strip()
    return bool(re.match(r'^[\s|:\-]+$', s)) and '-' in s

def split_row(line):
    s = line.strip()
    if s.startswith('|'):
        s = s[1:]
    if s.endswith('|'):
        s = s[:-1]
    return [c.strip() for c in s.split('|')]

def set_cell_text(cell, text, bold=False, size=10):
    cell.text = ''
    p = cell.paragraphs[0]
    p.paragraph_format.line_spacing_rule = WD_LINE_SPACING.SINGLE
    p.paragraph_format.space_after = Pt(2)
    p.paragraph_format.space_before = Pt(2)
    if text == '':
        return
    # handle inline formatting inside cells
    add_runs(p, text)
    for r in p.runs:
        r.font.name = 'Times New Roman'
        r.font.size = Pt(size)
        if bold:
            r.bold = True

def add_table(doc, header, rows):
    ncol = len(header)
    t = doc.add_table(rows=1, cols=ncol)
    t.style = 'Table Grid'
    t.alignment = WD_TABLE_ALIGNMENT.CENTER
    # header
    hdr = t.rows[0].cells
    for i, h in enumerate(header):
        set_cell_text(hdr[i], h, bold=True, size=10)
    # body
    for row in rows:
        cells = t.add_row().cells
        for i in range(ncol):
            val = row[i] if i < len(row) else ''
            set_cell_text(cells[i], val, size=10)
    # small spacer after table
    sp = doc.add_paragraph()
    sp.paragraph_format.space_after = Pt(6)
    return t

def add_heading(doc, text, level):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(12 if level <= 1 else 6)
    p.paragraph_format.space_after = Pt(6)
    r = p.add_run(text)
    r.font.name = 'Times New Roman'
    if level == 0:
        r.bold = True; r.font.size = Pt(16); p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    elif level == 1:
        r.bold = True; r.font.size = Pt(14)
    elif level == 2:
        r.bold = True; r.font.size = Pt(13)
    else:
        r.bold = True; r.font.size = Pt(12)
    return p

def add_line_numbers(section):
    sectPr = section._sectPr
    ln = sectPr.find(qn('w:lnNumType'))
    if ln is None:
        ln = OxmlElement('w:lnNumType')
        sectPr.append(ln)
    ln.set(qn('w:countBy'), '1')
    ln.set(qn('w:start'), '1')
    ln.set(qn('w:restart'), 'continuous')
    ln.set(qn('w:distance'), '360')

def add_page_number_footer(section):
    footer = section.footer
    p = footer.paragraphs[0]
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = p.add_run()
    f1 = OxmlElement('w:fldChar'); f1.set(qn('w:fldCharType'), 'begin')
    it = OxmlElement('w:instrText'); it.set(qn('xml:space'), 'preserve'); it.text = 'PAGE'
    f2 = OxmlElement('w:fldChar'); f2.set(qn('w:fldCharType'), 'end')
    run._r.append(f1); run._r.append(it); run._r.append(f2)
    run.font.name = 'Times New Roman'
    run.font.size = Pt(10)

def main():
    with open(SRC, 'r', encoding='utf-8') as f:
        text = f.read()
    lines = text.split('\n')

    doc = Document()

    # --- base styles ---
    normal = doc.styles['Normal']
    normal.font.name = 'Times New Roman'
    normal.font.size = Pt(12)
    normal.paragraph_format.line_spacing_rule = WD_LINE_SPACING.DOUBLE

    # --- section page setup ---
    sec = doc.sections[0]
    sec.top_margin = Inches(1); sec.bottom_margin = Inches(1)
    sec.left_margin = Inches(1); sec.right_margin = Inches(1)
    add_line_numbers(sec)
    add_page_number_footer(sec)

    in_front_matter = True
    in_references = False
    i = 0
    n = len(lines)
    while i < n:
        line = lines[i]
        stripped = line.strip()

        # horizontal rule
        if stripped in ('---', '***', '___'):
            i += 1
            continue

        # table
        if stripped.startswith('|') and i + 1 < n and is_sep(lines[i + 1]):
            header = split_row(lines[i])
            i += 2
            rows = []
            while i < n and lines[i].strip().startswith('|'):
                rows.append(split_row(lines[i]))
                i += 1
            add_table(doc, header, rows)
            continue

        # headings
        m = re.match(r'^(#{1,4})\s+(.*)$', line)
        if m:
            level = len(m.group(1))
            htext = m.group(2).strip()
            if level == 1:          # title "#"
                in_front_matter = False
            elif level == 2:        # sections "##"
                if htext.lower() == 'references':
                    in_references = True
                else:
                    in_references = False
            add_heading(doc, htext, level - 1)   # style levels: 0=title, 1=##, 2=###, 3=####
            i += 1
            continue

        # bullet list
        if re.match(r'^\s*-\s+', line):
            while i < n and re.match(r'^\s*-\s+', lines[i]):
                content = re.sub(r'^\s*-\s+', '', lines[i])
                p = doc.add_paragraph(style='List Bullet')
                add_runs(p, content)
                i += 1
            continue

        # ordered list (numbered "1. ") outside references -> List Number, strip number
        if re.match(r'^\d+\.\s+', line) and not in_references:
            while i < n and re.match(r'^\d+\.\s+', lines[i]):
                content = re.sub(r'^\d+\.\s+', '', lines[i])
                p = doc.add_paragraph(style='List Number')
                add_runs(p, content)
                i += 1
            continue

        # blockquote note
        if stripped.startswith('>'):
            content = stripped.lstrip('>').strip()
            p = doc.add_paragraph()
            p.paragraph_format.left_indent = Pt(18)
            r = p.add_run(content)
            r.italic = True
            i += 1
            continue

        # blank
        if stripped == '':
            i += 1
            continue

        # normal paragraph
        p = doc.add_paragraph()
        if in_front_matter:
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            add_runs(p, line)
            for r in p.runs:
                r.font.name = 'Times New Roman'
                if ('@' in line) or ('Department' in line) or ('These authors' in line) or ('Correspondence' in line):
                    r.font.size = Pt(10)
                else:
                    r.font.size = Pt(12)
        elif in_references:
            p.paragraph_format.left_indent = Pt(36)
            p.paragraph_format.first_line_indent = Pt(-36)
            p.paragraph_format.line_spacing_rule = WD_LINE_SPACING.SINGLE
            add_runs(p, line)
        else:
            add_runs(p, line)
        i += 1

    # metadata
    cp = doc.core_properties
    cp.title = "A falsification framework for causal claims in polygenic epidemiology: the insomnia-Alzheimer's disease test case"
    cp.author = "Ming Luo, Wangyang Ye, Qin Liu"

    doc.save(OUT)
    print("Saved:", OUT)

if __name__ == '__main__':
    main()
