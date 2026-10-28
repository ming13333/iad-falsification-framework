#!/usr/bin/env python3
"""Assemble Supplementary_Tables.xlsx from the per-table CSVs.

The workbook is a convenience compilation of the individual supplementary
tables; the CSVs remain the source of truth and the workbook is regenerated
from them, never edited by hand. Supplementary Table S12 is prose with embedded
tables and is therefore not included as a sheet.

Usage
    python code/build_supplementary_workbook.py
    python code/build_supplementary_workbook.py --check   # compare sheet names + row counts
"""
from __future__ import annotations

import argparse
import csv
import os
import re
import sys

from openpyxl import Workbook, load_workbook
from openpyxl.styles import Alignment, Font
from openpyxl.utils import get_column_letter

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SUPP = os.path.join(ROOT, os.environ.get("IAD_SUPP_DIR", "manuscript/supplementary"))
OUT = os.path.join(SUPP, "Supplementary_Tables.xlsx")

# Sheet order follows the manuscript's citation order.
TABLES = [
    ("S1_coloc_loci.csv", "S1_coloc_loci"),
    ("S2_instrument_sensitivity.csv", "S2_instrument_sensitivity"),
    ("S3_MVMR_complete.csv", "S3_MVMR_complete"),
    ("S4_education_PheWAS.csv", "S4_education_PheWAS"),
    ("S5_STROBE_MR.csv", "S5_STROBE_MR"),
    ("S6_Height_AD_exploratory.csv", "S6_Height_AD_exploratory"),
    ("S7_iv_annotation_confounder.csv", "S7_iv_annotation_confounder"),
    ("S8_twelve_case_validation.csv", "S8_twelve_case_validation"),
    ("S9_simulation_operating.csv", "S9_simulation_operating"),
    # Excel caps sheet names at 31 characters, so the marginal table is abbreviated.
    ("S9_simulation_operating_marginal.csv", "S9_sim_operating_marginal"),
    ("S10_gate_ablation.csv", "S10_gate_ablation"),
    ("S11_instrument_tiers.csv", "S11_instrument_tiers"),
]

INT_RE = re.compile(r"^-?\d+$")


def read_csv(path):
    """Yield rows, skipping leading '#' comment lines and blank lines."""
    with open(path, encoding="utf-8-sig", newline="") as fh:
        rows = [r for r in csv.reader(fh) if r and not r[0].startswith("#")]
    return rows


def coerce(value):
    v = value.strip()
    if v == "":
        return None
    if INT_RE.match(v):
        return int(v)
    try:
        return float(v)
    except ValueError:
        return value


def build():
    wb = Workbook()
    wb.remove(wb.active)
    for fname, sheet in TABLES:
        path = os.path.join(SUPP, fname)
        rows = read_csv(path)
        ws = wb.create_sheet(sheet)
        widths = {}
        for r_i, row in enumerate(rows, start=1):
            for c_i, value in enumerate(row, start=1):
                cell = ws.cell(row=r_i, column=c_i, value=coerce(value) if r_i > 1 else value)
                if r_i == 1:
                    cell.font = Font(bold=True)
                    cell.alignment = Alignment(vertical="top", wrap_text=True)
                else:
                    cell.alignment = Alignment(vertical="top")
                widths[c_i] = max(widths.get(c_i, 8), min(len(str(value)) + 2, 48))
        for c_i, w in widths.items():
            ws.column_dimensions[get_column_letter(c_i)].width = w
        ws.freeze_panes = "A2"
        if rows and len(rows) > 1:
            ws.auto_filter.ref = f"A1:{get_column_letter(len(rows[0]))}{len(rows)}"
    wb.save(OUT)
    print(f"wrote {os.path.relpath(OUT, ROOT)}: {len(TABLES)} sheets")


def check():
    if not os.path.exists(OUT):
        print("workbook missing; run without --check first", file=sys.stderr)
        return 1
    wb = load_workbook(OUT, read_only=True)
    problems = 0
    if wb.sheetnames != [s for _, s in TABLES]:
        print(f"sheet order differs: {wb.sheetnames}")
        problems += 1
    for fname, sheet in TABLES:
        expected = len(read_csv(os.path.join(SUPP, fname)))
        actual = wb[sheet].max_row
        if expected != actual:
            print(f"{sheet}: csv {expected} rows, workbook {actual}")
            problems += 1
    print("workbook OK" if not problems else f"{problems} problem(s)")
    return 1 if problems else 0


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true")
    args = ap.parse_args()
    return check() if args.check else build()


if __name__ == "__main__":
    sys.exit(main())
