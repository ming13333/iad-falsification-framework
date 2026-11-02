#!/usr/bin/env python3
"""
Build the marked-up revision in which every highlighted passage is traceable to
a numbered reviewer comment.

Rules enforced by this script
----------------------------
1. Only differences that answer a comment are highlighted. A difference the map
   cannot place in a reviewer comment is either a journal/technical requirement
   (FMT) or a conversion artefact (NOISE); neither is painted.
2. Nothing is highlighted without an attached comment id. Each highlighted
   paragraph carries a Word comment naming the comment it answers, so a reader
   who clicks a yellow passage sees "R1-4 - ..." rather than a bare colour.
3. The rest of the manuscript is unchanged. The plain text of the marked copy is
   identical to the clean copy; only highlight and comment anchors are added.
4. A difference that the map does not cover stops the build. That is the point
   of the exercise: the map is the claim that every change has a home, and the
   script refuses to produce a copy in which that claim would be false.

Also applies the three-line table rule (R3-12), which the response letter states
as done but which the rebuilt .docx had lost: the markdown converter emits
tables with no rules at all, and the submitted version carried a full grid.

Outputs
    <out.docx>                  marked copy (highlight + comments)
    <csv>                       one row per highlighted passage
    <coverage>                  one row per comment id
    <unattributed>              differences with no reviewer home
    <report>                    markdown traceability report
"""

import argparse
import collections
import csv
import difflib
import importlib.util
import io
import os
import sys

from docx import Document
from docx.oxml import OxmlElement
from docx.oxml.ns import qn

HERE = os.path.dirname(os.path.abspath(__file__))
_spec = importlib.util.spec_from_file_location("mc", os.path.join(HERE, "mark_changes.py"))
mc = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(mc)

_spec2 = importlib.util.spec_from_file_location("am", os.path.join(HERE, "attribution_map.py"))
am = importlib.util.module_from_spec(_spec2)
_spec2.loader.exec_module(am)

REV, FMT, ED, NOISE, FIX = "REV", "FMT", "ED", "NOISE", "FIX"
AUTHOR = "Revision map"


# ---------------------------------------------------------------- comments
def anchor_comment(par, cid):
    """Wrap the paragraph in w:commentRangeStart/End and add the reference run."""
    p = par._p
    start = OxmlElement("w:commentRangeStart")
    start.set(qn("w:id"), str(cid))
    end = OxmlElement("w:commentRangeEnd")
    end.set(qn("w:id"), str(cid))

    ref_run = OxmlElement("w:r")
    rPr = OxmlElement("w:rPr")
    style = OxmlElement("w:rStyle")
    style.set(qn("w:val"), "CommentReference")
    rPr.append(style)
    ref_run.append(rPr)
    ref = OxmlElement("w:commentReference")
    ref.set(qn("w:id"), str(cid))
    ref_run.append(ref)

    kids = list(p)
    at = 1 if (kids and kids[0].tag == qn("w:pPr")) else 0
    p.insert(at, start)
    p.append(end)
    p.append(ref_run)


def brief(text, n=52):
    """Cut at a word boundary; a mid-word cut reads as a typo in the index."""
    text = text.replace("\n", " ").strip()
    if len(text) <= n:
        return text
    cut = text[:n].rsplit(" ", 1)[0]
    return cut + "\u2026"


def insert_in_order(parent, element, successors):
    """Insert keeping the CT_* schema order, otherwise Word offers to repair."""
    for child in parent:
        if child.tag in successors:
            child.addprevious(element)
            return
    parent.append(element)


# ---------------------------------------------------------------- tables
def borders_are_three_line(table):
    """One rule above the header, one below it, one below the last row, no verticals.

    md_to_docx_frontiers.py draws the rules as cell borders rather than table
    borders (tblBorders is switched to none and the three rules are set on the
    cells), so the check has to look at tcBorders, not at tblPr.
    """
    def rules(cell):
        tcPr = cell._tc.tcPr
        if tcPr is None:
            return {}
        tb = tcPr.find(qn("w:tcBorders"))
        if tb is None:
            return {}
        return {e.tag.split("}")[1]: e.get(qn("w:val")) for e in tb}

    first = [rules(c) for c in table.rows[0].cells]
    last = [rules(c) for c in table.rows[-1].cells]
    top_ok = all(r.get("top") == "single" for r in first)
    head_ok = all(r.get("bottom") == "single" for r in first)
    foot_ok = all(r.get("bottom") == "single" for r in last)
    verticals = any(k in r for r in first + last for k in ("left", "right", "insideV"))
    return top_ok and head_ok and foot_ok and not verticals


# ---------------------------------------------------------------- diffing
def changed_paragraphs(base, target):
    b_idx, b_txt = mc.nonempty_map(base)
    t_idx, t_txt = mc.nonempty_map(target)
    mapping, deleted = mc.align_blocks(b_txt, t_txt)

    rows = []
    for j, text in enumerate(t_txt):
        kind, i, sim = mapping.get(j, ("new", None, 0.0))
        if kind == "equal":
            continue
        if i is None:
            mode, ranges, note = "all", [], "new paragraph"
        elif kind == "sub":
            mode, ranges, note = mc.choose_mode(b_txt[i], text, 1.0)
            note = "split from a merged paragraph"
            if mode == "all":
                continue          # only the split itself, nothing to show
        else:
            mode, ranges, note = mc.choose_mode(b_txt[i], text, sim)
            if mode is None:
                continue
        chars = len(text) if mode == "all" else sum(b - a for a, b in ranges)
        rows.append({"idx": t_idx[j], "mode": mode, "ranges": ranges,
                     "chars": chars, "len": len(text), "note": note, "text": text})
    return rows, deleted


def changed_cells(base_tbl, target_tbl):
    """Yield (row, col, mode, ranges, text) for every changed cell."""
    col_map, _dropped = mc.map_columns(target_tbl, base_tbl)
    for jr in range(min(len(base_tbl.rows), len(target_tbl.rows))):
        for jc in range(len(target_tbl.columns)):
            cell = target_tbl.rows[jr].cells[jc]
            if jc not in col_map:
                if cell.text.strip():
                    yield jr, jc, "all", [], cell.text.strip()
                continue
            btxt = base_tbl.rows[jr].cells[col_map[jc]].text.strip()
            ttxt = cell.text.strip()
            if not ttxt or mc.norm(btxt) == mc.norm(ttxt):
                continue
            mode, ranges, _note = mc.choose_mode(btxt, ttxt,
                                                 difflib.SequenceMatcher(
                                                     None, mc.norm(btxt), mc.norm(ttxt),
                                                     autojunk=False).ratio())
            if mode is None:
                continue
            yield jr, jc, mode, ranges, ttxt


# ---------------------------------------------------------------- main
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--baseline", default="课题设计阶段/manuscript Frontiers 0902.docx")
    ap.add_argument("--target", default="课题设计阶段/manuscript_Frontiers_Methods_v2.docx")
    ap.add_argument("--out", default="课题设计阶段/manuscript_Frontiers_Methods_v2_marked.docx")
    ap.add_argument("--csv", default="课题设计阶段/manuscript_Frontiers_Methods_v2_marked_changes.csv")
    ap.add_argument("--coverage", default="课题设计阶段/manuscript_Frontiers_Methods_v2_comment_coverage.csv")
    ap.add_argument("--unattributed", default="课题设计阶段/manuscript_Frontiers_Methods_v2_unattributed.csv")
    ap.add_argument("--report", default="课题设计阶段/Reviewer_traceability_report.md")
    ap.add_argument("--deletions", default="课题设计阶段/manuscript_Frontiers_Methods_v2_marked_deletions.md")
    ap.add_argument("--no-borders", action="store_true", help="skip the R3-12 three-line table rule")
    args = ap.parse_args()

    base = Document(args.baseline)
    target = Document(args.target)
    paras = [p for p in target.paragraphs]

    # -- 1. every mapped head must match the paragraph it claims -------------
    bad = []
    for idx, (cat, payload, why, head) in am.MAP.items():
        if idx >= len(paras):
            bad.append((idx, head, "<out of range>"))
            continue
        actual = paras[idx].text.strip()
        if not actual.startswith(head):
            bad.append((idx, head, actual[:60]))
    if bad:
        print("attribution map does not match the document:")
        for idx, head, actual in bad:
            print(f"  para {idx}: expected {head!r}, found {actual!r}")
        return 1

    # -- 2. diff ------------------------------------------------------------
    rows, deleted = changed_paragraphs(base, target)
    by_idx = {r["idx"]: r for r in rows}

    unmapped = sorted(set(by_idx) - set(am.MAP))
    if unmapped:
        print(f"{len(unmapped)} changed paragraph(s) have no entry in the "
              f"attribution map; refusing to build a copy that would claim "
              f"otherwise:")
        for idx in unmapped:
            print(f"  para {idx}: {by_idx[idx]['text'][:90]}")
        return 1

    # entries whose difference the differ already treats as structural (list
    # renumbering, block splits) are expected to fall out; only an entry that
    # claims a comment and finds nothing to paint is worth reporting
    stale = sorted(i for i in set(am.MAP) - set(by_idx) if am.MAP[i][0] == REV)
    if stale:
        print("warning: mapped to a comment but no difference found:",
              ", ".join(str(i) for i in stale))

    # -- 3. paint and comment ----------------------------------------------
    index_rows = []
    n_comments = 0
    comment_ids = {}

    def comment_for(ids, why, where):
        nonlocal n_comments
        body = "\n".join(f"{i} \u2014 {am.TOPIC[i]}" for i in ids) + f"\n\n{why}"
        c = target.comments.add_comment(body, author=AUTHOR, initials="RM")
        n_comments += 1
        for i in ids:
            comment_ids.setdefault(i, []).append(where)
        return c.comment_id

    for idx, row in sorted(by_idx.items()):
        cat, payload, why, _head = am.MAP[idx]
        if cat != REV:
            continue
        par = paras[idx]
        # colour is explicit: paint_paragraph falls back to bright green for
        # whole-paragraph marks, and a two-colour copy invites the question of
        # what the second colour means. One colour, one meaning: an answer to
        # a comment, identified by the attached Word comment.
        painted = mc.paint_paragraph(par, row["mode"], row["ranges"], colour=mc.YELLOW)
        if not painted:
            print(f"warning: para {idx} mapped to {payload} but nothing painted")
            continue
        cid = comment_for(payload, why, f"para {idx}")
        anchor_comment(par, cid)
        index_rows.append({
            "location": f"para {idx}",
            "comments": ";".join(payload),
            "section": brief(row["text"]),
            "change": row["note"],
            "chars_marked": row["chars"],
            "chars_total": row["len"],
            "why": why,
        })

    # -- 4. tables ----------------------------------------------------------
    for k in range(min(len(base.tables), len(target.tables))):
        tgt = target.tables[k]
        if not args.no_borders and not borders_are_three_line(tgt):
            print(f"warning: table {k+1} is not a three-line table (R3-12)")
        if k in am.TABLE_MAP:
            base_ids, base_why = am.TABLE_MAP[k]
            col_ids = am.TABLE_COL_MAP.get(k, {})
            cells = list(changed_cells(base.tables[k], tgt))
            for jr, jc, mode, ranges, ttxt in cells:
                ids = col_ids.get(jc, base_ids)
                why = base_why if jc not in col_ids else (
                    "Recomputed value: the benchmark was re-scored with the decisive-failure rule"
                    if "R1-2" in col_ids[jc] else
                    "Specificity reported under both conventions, with intervals")
                cell = tgt.rows[jr].cells[jc]
                for par in cell.paragraphs:
                    mc.paint_paragraph(par, mode, ranges, colour=mc.YELLOW)
                cid = comment_for(ids, why, f"table {k+1} r{jr+1}c{jc+1}")
                for par in cell.paragraphs:
                    anchor_comment(par, cid)
                index_rows.append({
                    "location": f"table {k+1} r{jr+1}c{jc+1}",
                    "comments": ";".join(ids),
                    "section": brief(ttxt),
                    "change": mode,
                    "chars_marked": len(ttxt) if mode == "all" else len(ttxt),
                    "chars_total": len(ttxt),
                    "why": why,
                })
        elif k in am.TABLE_CELL_MAP:
            for (jr, jc), (ids, why) in am.TABLE_CELL_MAP[k].items():
                cell = tgt.rows[jr].cells[jc]
                btxt = base.tables[k].rows[jr].cells[jc].text.strip()
                ttxt = cell.text.strip()
                mode, ranges, _ = mc.choose_mode(btxt, ttxt,
                                                 difflib.SequenceMatcher(
                                                     None, mc.norm(btxt), mc.norm(ttxt),
                                                     autojunk=False).ratio())
                for par in cell.paragraphs:
                    mc.paint_paragraph(par, mode or "all", ranges, colour=mc.YELLOW)
                cid = comment_for(ids, why, f"table {k+1} r{jr+1}c{jc+1}")
                for par in cell.paragraphs:
                    anchor_comment(par, cid)
                index_rows.append({
                    "location": f"table {k+1} r{jr+1}c{jc+1}",
                    "comments": ";".join(ids),
                    "section": brief(ttxt),
                    "change": mode or "all",
                    "chars_marked": len(ttxt),
                    "chars_total": len(ttxt),
                    "why": why,
                })

    # R3-12 asks for three-line tables. It changes rules, not words, so it has
    # no highlighted text; it is recorded in the coverage table instead, with
    # the tables it was applied to. Without this the report would claim that one
    # comment out of twenty-two has no landing spot, which is untrue.
    extra_cov = {}
    if not args.no_borders and all(borders_are_three_line(t) for t in target.tables):
        extra_cov["R3-12"] = {"locations": [f"Table {k+1}" for k in range(len(target.tables))],
                              "chars": 0}

    # -- 5. the residue -----------------------------------------------------
    residue = []
    for idx, row in sorted(by_idx.items()):
        cat, payload, why, _head = am.MAP[idx]
        if cat == REV:
            continue
        residue.append({
            "category": {"FMT": "journal/technical requirement",
                         "ED": "editorial, not requested by a reviewer",
                         "FIX": "corrected during the reference audit; no reviewer asked",
                         "NOISE": "conversion artefact / alignment"}[cat],
            "location": f"para {idx}",
            "chars": row["chars"] if cat == FMT else row["chars"],
            "text": row["text"][:140].replace("\n", " "),
            "why": why,
        })

    target.save(args.out)

    if args.deletions:
        with io.open(args.deletions, "w", encoding="utf-8", newline="") as f:
            f.write("# Text removed since the submitted version\n\n")
            f.write(f"Baseline: `{os.path.basename(args.baseline)}`  \n")
            f.write(f"Paragraphs present in the submission but not in the revision: "
                    f"**{len(deleted)}**\n\n")
            for i in deleted:
                f.write(f"- {mc.nonempty_map(base)[1][i][:300]}\n")

    # -- 6. outputs ---------------------------------------------------------
    with io.open(args.csv, "w", encoding="utf-8-sig", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["location", "comments", "section", "change",
                                          "chars_marked", "chars_total", "why"])
        w.writeheader()
        w.writerows(index_rows)

    cov = collections.OrderedDict(extra_cov)
    for r in index_rows:
        for cid in r["comments"].split(";"):
            cov.setdefault(cid, {"locations": [], "chars": 0})["locations"].append(r["location"])
            cov[cid]["chars"] += r["chars_marked"]
    with io.open(args.coverage, "w", encoding="utf-8-sig", newline="") as f:
        w = csv.writer(f)
        w.writerow(["comment_id", "topic", "n_locations", "chars_highlighted", "locations"])
        for cid in sorted(cov, key=lambda s: (s[1], int(s.split("-")[1]))):
            w.writerow([cid, am.TOPIC[cid], len(cov[cid]["locations"]),
                        cov[cid]["chars"], "; ".join(cov[cid]["locations"])])

    with io.open(args.unattributed, "w", encoding="utf-8-sig", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["category", "location", "chars", "text", "why"])
        w.writeheader()
        w.writerows(residue)

    write_report(args.report, index_rows, cov, residue, deleted, len(by_idx), n_comments, args)

    hl_chars = sum(r["chars_marked"] for r in index_rows)
    print(f"highlighted passages : {len(index_rows)} in {n_comments} comment anchors")
    print(f"highlighted chars    : {hl_chars:,}")
    print(f"not highlighted      : {len(residue)} difference(s), "
          f"{sum(r['chars'] for r in residue):,} chars")
    print(f"comments covered     : {len(cov)}/22")
    missing = [c for c in am.TOPIC if c not in cov]
    if missing:
        print("comments with no highlighted landing spot:", ", ".join(missing))
    print("written:", args.out)
    return 0


def write_report(path, index_rows, cov, residue, deleted, n_changed, n_comments, args):
    missing = [c for c in am.TOPIC if c not in cov]
    lines = []
    lines.append("# Reviewer traceability report")
    lines.append("")
    lines.append(f"Baseline: `{os.path.basename(args.baseline)}` (submitted)  ")
    lines.append(f"Revision: `{os.path.basename(args.target)}`  ")
    lines.append(f"Marked copy: `{os.path.basename(args.out)}`")
    lines.append("")
    n_para = sum(1 for r in index_rows if r["location"].startswith("para"))
    n_cell = len(index_rows) - n_para
    cat_counts = collections.Counter(r["category"] for r in residue)
    lines.append(f"- Differences detected: **{n_changed}** body paragraphs"
                 + (f" and **{n_cell}** table cells" if n_cell else ""))
    lines.append(f"- Highlighted as answers to a reviewer comment: **{n_para}** paragraphs"
                 + (f" and **{n_cell}** cells" if n_cell else "")
                 + f", {sum(r['chars_marked'] for r in index_rows):,} characters")
    detail = ", ".join(f"{k} {v}" for k, v in cat_counts.items())
    lines.append(f"- Not highlighted: **{len(residue)}** differences ({detail})")
    lines.append(f"- Comments with a landing spot: **{len(cov)}/22**"
                 + (f"; without: {', '.join(missing)}" if missing else ""))
    lines.append("")
    lines.append("## 1. Where each comment is answered")
    lines.append("")
    lines.append("| Comment | Topic | Passages | Characters | Where |")
    lines.append("|---|---|---|---|---|")
    for cid in sorted(cov, key=lambda s: (s[1], int(s.split("-")[1]))):
        locs = cov[cid]["locations"]
        shown = ", ".join(locs[:6]) + (f" +{len(locs)-6}" if len(locs) > 6 else "")
        lines.append(f"| {cid} | {am.TOPIC[cid]} | {len(locs)} | {cov[cid]['chars']:,} | {shown} |")
    lines.append("")
    if missing:
        lines.append("**No highlighted landing spot:** " + ", ".join(missing))
        lines.append("")
    lines.append("## 2. Passage-by-passage index")
    lines.append("")
    lines.append("| Location | Comments | Opening words | Change | Chars | Why |")
    lines.append("|---|---|---|---|---|---|")
    for r in index_rows:
        lines.append(f"| {r['location']} | {r['comments']} | {r['section']} | {r['change']} "
                     f"| {r['chars_marked']} | {brief(r['why'], 90)} |")
    lines.append("")
    lines.append("## 3. Differences that do not answer a reviewer comment")
    lines.append("")
    if residue:
        lines.append("| Category | Location | Chars | Text | Reason |")
        lines.append("|---|---|---|---|---|")
        for r in residue:
            lines.append(f"| {r['category']} | {r['location']} | {r['chars']} | "
                         f"{brief(r['text'], 70)} | {r['why']} |")
        lines.append("")
        lines.append("Journal/technical items are required by the Frontiers author guidelines "
                     "or the submission system; they are not answers to a comment and are "
                     "therefore not highlighted. Conversion artefacts are listed so that "
                     "nobody mistakes them for editorial changes.")
    else:
        lines.append("None.")
    lines.append("")
    if deleted:
        lines.append("## 4. Deleted text")
        lines.append("")
        lines.append(f"{len(deleted)} paragraph(s) present in the submitted version and absent "
                     f"from the revision, listed in "
                     f"`manuscript_Frontiers_Methods_v2_marked_deletions.md`. Deletions are not "
                     f"visible in a highlight-only copy; a tracked-changes copy would show them.")
        lines.append("")
    if getattr(am, "NOTES", None):
        lines.append("## 5. Notes from building the map")
        lines.append("")
        for i, note in enumerate(am.NOTES, 1):
            lines.append(f"{i}. {note}")
        lines.append("")

    with io.open(path, "w", encoding="utf-8", newline="") as f:
        f.write("\n".join(lines) + "\n")


if __name__ == "__main__":
    sys.exit(main())
