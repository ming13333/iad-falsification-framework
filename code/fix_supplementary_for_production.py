"""Prepare the supplementary documents for production (ready-to-publish condition).

Frontiers production does not typeset supplementary material, so whatever is in the
docx is what appears in the published article. Three defects were present in the
version uploaded on 2026-11-03:

1. Bare workstation paths (``C:/Temp/iad_g1/...``) in the file lists of Notes 1 and 2,
   including one path with Chinese directory names.
2. Literal Markdown backticks left in the text (28 in Note 1, 40 in Note 2), which
   would print verbatim.
3. Heading styles carried the Word default theme blue (365F91 / 4F81BD).

This script fixes all three and rewrites the two file lists so that every item is
either a repository-relative path (present in the archived release) or explicitly
marked as not deposited and available from the corresponding author.

The originals are preserved in 05_Supplementary/_backup_pre_prod_20261124/.

Usage:  python code/fix_supplementary_for_production.py
"""

from __future__ import annotations

import copy
import os
import shutil
import sys

from docx import Document
from docx.oxml.ns import qn

SUPP = os.path.join(
    "submissions",
    "Frontiers_1986036_revision_20261103",
    "05_Supplementary",
)

DOCX = [
    "Supplementary_Note_1.docx",
    "Supplementary_Note_2.docx",
    "Supplementary_Table_S5_STROBE-MR_checklist.docx",
    "Supplementary_Table_S8_scoring_with_footnotes.docx",
    "Supplementary_Table_S12_threshold_robustness.docx",
]

HEADING_IDS = ["Heading1", "Heading2", "Heading3", "Title"]


# ---------------------------------------------------------------- styles


def blacken_headings(doc):
    """Force heading styles to black so nothing prints in colour."""
    styles_el = doc.styles.element
    changed = 0
    for sid in HEADING_IDS:
        for st in styles_el.findall(qn("w:style")):
            if st.get(qn("w:styleId")) != sid:
                continue
            for col in st.iter(qn("w:color")):
                col.set(qn("w:val"), "000000")
                for attr in ("themeColor", "themeShade", "themeTint"):
                    if col.get(qn("w:" + attr)) is not None:
                        del col.attrib[qn("w:" + attr)]
                changed += 1
    return changed


# ---------------------------------------------------------------- backticks


def iter_paragraphs(doc):
    for p in doc.paragraphs:
        yield p
    for t in doc.tables:
        for row in t.rows:
            for cell in row.cells:
                for p in cell.paragraphs:
                    yield p


def deliteralize(doc):
    """Turn `file` into a Consolas run and drop the backtick characters."""
    fixed = 0
    for p in list(iter_paragraphs(doc)):
        for r in list(p.runs):
            if "`" not in r.text:
                continue
            parts = r.text.split("`")
            rPr = copy.deepcopy(r._element.rPr) if r._element.rPr is not None else None
            r.text = parts[0]
            anchor = r._element
            for i, seg in enumerate(parts[1:], 1):
                nr = p.add_run(seg)
                if rPr is not None:
                    if nr._element.rPr is not None:
                        nr._element.remove(nr._element.rPr)
                    nr._element.insert(0, copy.deepcopy(rPr))
                if i % 2 == 1 and seg:
                    if nr._element.rPr is None:
                        nr.font.name = "Consolas"
                    else:
                        rf = nr._element.rPr.find(qn("w:rFonts"))
                        if rf is not None:
                            rf.set(qn("w:ascii"), "Consolas")
                            rf.set(qn("w:hAnsi"), "Consolas")
                        else:
                            nr.font.name = "Consolas"
                anchor.addnext(nr._element)
                anchor = nr._element
                fixed += 1
    return fixed


# ---------------------------------------------------------------- text surgery


def set_text(p, text):
    """Replace a paragraph's content with a single run, keeping its formatting."""
    tmpl = None
    if p.runs and p.runs[0]._element.rPr is not None:
        tmpl = copy.deepcopy(p.runs[0]._element.rPr)
    for r in list(p.runs):
        r._element.getparent().remove(r._element)
    nr = p.add_run(text)
    if tmpl is not None:
        if nr._element.rPr is not None:
            nr._element.remove(nr._element.rPr)
        nr._element.insert(0, tmpl)


def drop(p):
    p._element.getparent().remove(p._element)


NOTE1_FILES = [
    "`mdd2023_EAS_clinicalMD_Neff.csv` (781 MB) and "
    "`mdd2023_AllAncestry_clinicalMD_Neff.csv` (2.8 GB) \u2014 clinical MDD summary "
    "statistics from the figshare deposit mdd2023diverse "
    "(doi 10.6084/m9.figshare.24799299), file ids 43621254 and 43621302. "
    "Not deposited with this article; available from the corresponding author.",
    "Scripts `extract_mdd_eas.py`, `pipeline_mdd_eas_dep_ad.py` and "
    "`mr_eas_dep_mdd.py`, with the intermediate files `mdd_eas_gwsig.tsv`, "
    "`mdd_allanc_gwsig.tsv`, `mdd_allanc_instruments.tsv`, "
    "`mdd_eas_dep_ad_harm.tsv` (2 rows) and `l6_ea_dep_mdd.txt` \u2014 not deposited; "
    "available from the corresponding author on request.",
    "The ReadMe distributed with the figshare deposit documents the exclusion of "
    "the 23andMe, WHI and JHS cohorts from all shared summary statistics.",
]

NOTE2_FILES = [
    "`code/ea01_liftover_gard.py`, `code/ea02_instruments.py`, "
    "`code/ea03_harmonize.py` and `code/ea04_mr.py` \u2014 East Asian AD pipeline; "
    "deposited in the archived code release.",
    "`code/ea05_transethnic_insomnia_ad.py` \u2014 trans-ethnic insomnia\u2192AD, European "
    "instruments transferred into GARD; deposited.",
    "`results/ea_mr/ea_mr_results.csv` and `results/ea_mr/ea_mr_report.txt` \u2014 "
    "East Asian education\u2192AD replication; deposited.",
    "`results/ea_mr/ea_transethnic_insomnia_ad_results.csv`, `_report.txt` and "
    "`_harm.tsv` \u2014 trans-ethnic insomnia\u2192AD outputs; deposited.",
    "`data/processed/gard_ea_ad_hg19.tsv.gz` \u2014 GARD East Asian AD summary "
    "statistics after lift-over; third-party data, not deposited, available from "
    "the corresponding author.",
    "Scripts and intermediate files for the education\u2192T2D, T2D\u2192AD, "
    "education\u2192stroke and depression\u2192AD checks: `l6_ea_edu_t2d.txt`, "
    "`l6_ea_t2d_ad.py`, `l6_ea_edu_stroke.txt`, `bbj_t2d_instruments.csv`, "
    "`pipeline_mdd_eas_dep_ad.py`, `mdd_allanc_instruments.tsv` and "
    "`mdd_eas_dep_ad_harm.tsv`; not deposited, available from the corresponding "
    "author on request.",
    "Data-access outcome for the depression\u2192AD attempt: Supplementary Note 1.",
]


def fix_note1(doc):
    ps = doc.paragraphs
    # locate the Files heading, then rewrite the bullets that follow it
    start = None
    for i, p in enumerate(ps):
        if p.text.strip().lower() == "files":
            start = i
            break
    if start is None:
        raise RuntimeError("Note 1: Files heading not found")
    body = [p for p in ps[start + 1:] if p.text.strip()]
    for j, txt in enumerate(NOTE1_FILES):
        set_text(body[j], txt)
    for p in body[len(NOTE1_FILES):]:
        drop(p)
    return len(body)


def fix_note2(doc):
    ps = doc.paragraphs
    # 1. opening line: no longer claim full reproducibility from undeposited inputs
    for p in ps:
        if p.text.strip().startswith("Date: 2026-08-04."):
            set_text(
                p,
                "Date: 2026-08-04. All analyses are reproducible from the archived "
                "scripts and the files listed below; files that are third-party or "
                "not deposited are marked as such.",
            )
            break
    # 2. stale reference to the .md working copy
    for p in ps:
        if "SupplementaryNote_EAS_Depression_infeasible.md" in p.text:
            for r in p.runs:
                if "SupplementaryNote_EAS_Depression_infeasible.md" in r.text:
                    r.text = r.text.replace(
                        "SupplementaryNote_EAS_Depression_infeasible.md",
                        "Supplementary Note 1",
                    )
    # 3. file list
    start = None
    for i, p in enumerate(ps):
        if p.text.strip().lower() == "files":
            start = i
    if start is None:
        raise RuntimeError("Note 2: Files heading not found")
    body = [p for p in ps[start + 1:] if p.text.strip()]
    for j, txt in enumerate(NOTE2_FILES):
        set_text(body[j], txt)
    for p in body[len(NOTE2_FILES):]:
        drop(p)
    return len(body)


# ---------------------------------------------------------------- main


def main():
    if not os.path.isdir(SUPP):
        sys.exit("run from the project root; %s not found" % SUPP)

    for name in DOCX:
        path = os.path.join(SUPP, name)
        doc = Document(path)
        n_col = blacken_headings(doc)
        if name == "Supplementary_Note_1.docx":
            n_old = fix_note1(doc)
        elif name == "Supplementary_Note_2.docx":
            n_old = fix_note2(doc)
        else:
            n_old = 0
        n_mono = deliteralize(doc)
        doc.save(path)
        print(
            "%-58s heading-colour=%d  mono-spans=%3d  file-list-rewritten=%s"
            % (name, n_col, n_mono, ("%d paras" % n_old) if n_old else "-")
        )


if __name__ == "__main__":
    main()
