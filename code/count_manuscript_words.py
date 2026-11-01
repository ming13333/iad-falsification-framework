#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Count the words the first page declares, from the built .docx rather than from
the markdown, so that the declared figure describes the file a reviewer opens.

Scope conventions
-----------------
``main``     Introduction heading through the end of the Conclusions paragraph.
             Section headings, sub-headings, list items and table callouts are
             included, because Frontiers counts the submitted file, not a
             cleaned subset. Abstract, Declarations, References, figure legends
             and table bodies are excluded.
``abstract`` the paragraphs between the Abstract heading and the Introduction.
``legends``  the Figure legends and Tables blocks.
``refs``     the reference list.

Usage
-----
    python code/count_manuscript_words.py --docx <file.docx>
    python code/count_manuscript_words.py --docx <file.docx> --check
        exits 1 when the first page disagrees with the count

The check exists because the declared count had drifted: it read 8,261 while
the text it claimed to describe ran to 8,419 words on the same convention, and
nothing in the build compared the two.
"""

import argparse
import os
import re
import sys

from docx import Document

MAIN_START = "Introduction"
MAIN_END_MINOR = "Conclusions"
ABSTRACT_HEAD = "Abstract"
LEGENDS_HEAD = "Figure legends"
TABLES_HEAD = "Tables"
REFS_HEAD = "References"
DECL_HEAD = "Declarations"


def words(text):
    """Whitespace tokens; em dashes and arrows stand alone and are not words."""
    out = []
    for tok in re.split(r"\s+", text.strip()):
        if not tok:
            continue
        if re.fullmatch(r"[\u2013\u2014\u2192\u2190\u2194\u2264\u2265<>=+/,;:.\u2020*]+", tok):
            continue
        out.append(tok)
    return out


def count(text):
    return len(words(text))


def section_bounds(paras):
    """Return (main_start, main_end, abstract, legends, tables, refs, decl)."""
    def find(name, start=0):
        for i in range(start, len(paras)):
            if paras[i].strip() == name:
                return i
        return -1

    i_intro = find(MAIN_START)
    i_abs = find(ABSTRACT_HEAD)
    i_leg = find(LEGENDS_HEAD)
    i_tab = find(TABLES_HEAD)
    i_ref = find(REFS_HEAD)
    i_dec = find(DECL_HEAD)

    # Conclusions is the last paragraph whose text opens with the word; the
    # manuscript has no separate heading for it.
    i_end = -1
    for i in range(len(paras) - 1, i_intro, -1):
        if paras[i].strip().startswith(MAIN_END_MINOR):
            i_end = i
            break
    if i_end < 0:
        i_end = (i_dec - 1) if i_dec > 0 else len(paras) - 1
    return i_intro, i_end, i_abs, i_leg, i_tab, i_ref, i_dec


def measure(path):
    doc = Document(path)
    paras = [p.text for p in doc.paragraphs]
    i_intro, i_end, i_abs, i_leg, i_tab, i_ref, i_dec = section_bounds(paras)
    if i_intro < 0 or i_end < 0:
        raise SystemExit(f"{path}: cannot locate the main text")

    def span(a, b):
        if a < 0 or b < 0 or b < a:
            return 0
        return sum(count(t) for t in paras[a + 1:b + 1])

    abstract = span(i_abs, i_intro - 1)
    main = sum(count(t) for t in paras[i_intro:i_end + 1])
    legends = sum(count(t) for t in paras[i_leg:i_tab - 1]) if i_leg > 0 and i_tab > i_leg else 0
    # the reference list runs to the next block heading, which is Figure
    # legends in this manuscript; Declarations sits before References.
    ref_stop = i_leg if i_leg > i_ref else len(paras)
    refs = sum(count(t) for t in paras[i_ref + 1:ref_stop]) if i_ref > 0 else 0
    return {
        "abstract": abstract,
        "main": main,
        "legends": legends,
        "references": refs,
        "main_range": (i_intro, i_end),
        "reference_entries": sum(1 for t in paras[i_ref + 1:ref_stop] if t.strip()) if i_ref > 0 else 0,
    }


def declared(docx_path):
    """Read the first-page declaration, if any."""
    doc = Document(docx_path)
    head = []
    for p in doc.paragraphs[:40]:
        head.append(p.text)
    blob = "\n".join(head)
    m = re.search(r"Word count:\*{0,2}\s*([\d,]+)", blob)
    f = re.search(r"\*{0,2}Figures:\*{0,2}\s*(\d+)", blob)
    t = re.search(r"\*{0,2}Tables:\*{0,2}\s*(\d+)", blob)
    return (int(m.group(1).replace(",", "")) if m else None,
            int(f.group(1)) if f else None,
            int(t.group(1)) if t else None)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--docx", required=True)
    ap.add_argument("--check", action="store_true")
    args = ap.parse_args()

    if not os.path.exists(args.docx):
        raise SystemExit(f"missing {args.docx}")
    m = measure(args.docx)
    wc, nfig, ntab = declared(args.docx)

    print(f"{os.path.basename(args.docx)}")
    print(f"  abstract      {m['abstract']:>6}")
    print(f"  main text     {m['main']:>6}   (paragraphs {m['main_range'][0]}-{m['main_range'][1]})")
    print(f"  figure legends{m['legends']:>6}")
    print(f"  references    {m['references']:>6}   ({m['reference_entries']} entries)")

    if not args.check:
        return 0

    bad = []
    if wc is None:
        bad.append("no Word count declaration on the first page")
    elif wc != m["main"]:
        bad.append(f"declared {wc:,} words, text has {m['main']:,}")
    doc = Document(args.docx)
    real_figs = sum(1 for t in (p.text for p in doc.paragraphs)
                    if re.match(r"^Figure \d+\.", t.strip()))
    real_tabs = sum(1 for t in (p.text for p in doc.paragraphs)
                    if re.match(r"^Table \d+\.", t.strip()))
    if nfig is not None and nfig != real_figs:
        bad.append(f"declared {nfig} figures, found {real_figs} legends")
    if ntab is not None and ntab != real_tabs:
        bad.append(f"declared {ntab} tables, found {real_tabs} captions")
    if bad:
        for b in bad:
            print("  FAIL", b)
        return 1
    print("  OK    declaration matches the file")
    return 0


if __name__ == "__main__":
    sys.exit(main())
