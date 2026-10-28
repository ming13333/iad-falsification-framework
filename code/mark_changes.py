#!/usr/bin/env python3
"""
Mark every change between the submitted manuscript and the revised one.

Two-stage design: the revised .docx is produced by md_to_docx_frontiers.py as
usual, then this script diffs it against the submitted .docx and paints the
differences at the OOXML run level. Nothing in the rendering path is touched,
so the marked copy keeps exactly the formatting of the clean copy.

Colour code
    yellow      words that differ from the submitted version (word-level diff)
    bright green  a whole paragraph that is new or rewritten beyond recognition

Outputs
    <out.docx>              marked-up copy
    marked_changes.csv      one row per changed paragraph / table cell
    marked_deletions.md     text present in the submitted version but not in the revision

Usage
    python code/mark_changes.py \
        --baseline <submitted.docx> \
        --target   <revised.docx> \
        --out      <marked.docx> \
        --csv      <changes.csv> \
        --deletions <deletions.md>
"""
from __future__ import annotations

import argparse
import csv
import difflib
import os
import re
import sys
from copy import deepcopy

from docx import Document
from docx.oxml import OxmlElement
from docx.oxml.ns import qn

# ---------------------------------------------------------------- constants
YELLOW = "yellow"
GREEN = "green"          # Word's "bright green"
WHOLE_PARAGRAPH_SIM = 0.55   # below this a paragraph is treated as rewritten
WORD_LEVEL_SIM = 0.85        # at or above this a paragraph gets word-level marks
BLOCK_PAIR_SIM = 0.30        # block-level greedy pairing floor
HEADER_SIM = 0.60            # minimum similarity to treat two columns as the same


# ---------------------------------------------------------------- text utils
_SUPERSCRIPT = str.maketrans({
    "⁰": "0", "¹": "1", "²": "2", "³": "3", "⁴": "4",
    "⁵": "5", "⁶": "6", "⁷": "7", "⁸": "8", "⁹": "9",
    "⁻": "-", "⁺": "+",
})


def norm(s: str) -> str:
    """Normalise for comparison only (never for display)."""
    s = s.replace("\u00a0", " ")
    s = s.translate(_SUPERSCRIPT)          # r² and r2 are the same formula
    s = s.replace("\u2013", "-").replace("\u2014", "-").replace("\u2212", "-")
    s = s.replace("\u2019", "'").replace("\u2018", "'")
    s = s.replace("\u201c", '"').replace("\u201d", '"')
    s = re.sub(r"-{2,}", "-", s)           # submitted text used a LaTeX en-dash
    s = s.replace("_", "")                 # LaTeX subscript: r_g -> rg
    s = re.sub(r"\s+", " ", s)
    return s.strip().lower()


def strip_numbering(s: str) -> str:
    """Drop a leading list marker, which a renumbered paragraph gains."""
    return re.sub(r"^\s*\d+\.\s+", "", s)


def tokenize(s: str):
    """Split into words plus their trailing whitespace, preserving offsets."""
    return re.findall(r"\S+\s*", s)


def merge_ranges(ranges):
    if not ranges:
        return []
    ranges = sorted(ranges)
    out = [list(ranges[0])]
    for a, b in ranges[1:]:
        if a <= out[-1][1]:
            out[-1][1] = max(out[-1][1], b)
        else:
            out.append([a, b])
    return [(a, b) for a, b in out if b > a]


def word_diff_ranges(base: str, new: str, filter_noise: bool = True):
    """Character ranges in *new* that are inserted or replaced."""
    bt = tokenize(base)
    nt = tokenize(new)
    sm = difflib.SequenceMatcher(
        None, [norm(x) for x in bt], [norm(x) for x in nt], autojunk=False
    )
    ranges = []
    pos = 0
    for tag, i1, i2, j1, j2 in sm.get_opcodes():
        seg = "".join(nt[j1:j2])
        if tag in ("insert", "replace") and seg.strip():
            # trim leading/trailing whitespace of the marked span
            lead = len(seg) - len(seg.lstrip())
            tail = len(seg) - len(seg.rstrip())
            ranges.append((pos + lead, pos + len(seg) - tail))
        pos += len(seg)
    ranges = merge_ranges(ranges)
    if filter_noise:
        ranges = [r for r in ranges if _worth_marking(new, *r)]
    return ranges


def split_sentences(s):
    """[(sentence_text, start_offset)] cut on '. ' followed by a capital."""
    out, start = [], 0
    for m in re.finditer(r"(?<=[.!?])\s+(?=[A-Z(\[])", s):
        out.append((s[start:m.start()], start))
        start = m.end()
    out.append((s[start:], start))
    return [x for x in out if x[0].strip()]


def sentence_diff_ranges(base: str, new: str):
    """Character ranges in *new* covering whole inserted or replaced sentences.

    Used for paragraphs that were re-ordered rather than re-worded: a word-level
    diff on such text scatters marks across half the sentence and reads as noise.
    """
    bs, ns = split_sentences(base), split_sentences(new)
    if not ns:
        return []
    sm = difflib.SequenceMatcher(
        None, [norm(x[0]) for x in bs], [norm(x[0]) for x in ns], autojunk=False
    )
    ranges = []
    for tag, i1, i2, j1, j2 in sm.get_opcodes():
        if tag not in ("insert", "replace") or j2 <= j1:
            continue
        a = ns[j1][1]
        last_txt, last_off = ns[j2 - 1]
        b = last_off + len(last_txt)
        ranges.append((a, b))
    return merge_ranges(ranges)


def _worth_marking(text, a, b):
    """Drop marks that carry no information (whitespace, punctuation only)."""
    span = text[a:b]
    if len(span.strip()) >= 2 and re.search(r"[A-Za-z0-9]", span):
        return True
    return len(span.strip()) >= 4


def choose_mode(base: str, new: str, sim: float):
    """Return (mode, ranges, note).

    small edit   -> word level marks, only the words that moved
    re-ordered   -> sentence level marks, whole sentences
    rewritten    -> whole paragraph
    """
    if sim < WHOLE_PARAGRAPH_SIM:
        return "all", [], f"rewritten (sim {sim:.2f})"

    if sim >= WORD_LEVEL_SIM:
        ranges = word_diff_ranges(base, new, filter_noise=True)
        if not ranges:
            # only trivial punctuation moved; still mark it rather than fall
            # through to sentence level and paint the whole sentence
            ranges = word_diff_ranges(base, new, filter_noise=False)
        if ranges and not _fragmented(ranges, new):
            return "partial", ranges, f"edited (sim {sim:.2f})"
        if _fragmented(ranges, new):
            return "all", [], f"re-ordered (sim {sim:.2f})"

    ranges = sentence_diff_ranges(base, new)
    if ranges:
        return "partial", ranges, f"edited, sentence level (sim {sim:.2f})"

    ranges = word_diff_ranges(base, new, filter_noise=False)
    if ranges:
        return "partial", ranges, f"edited (sim {sim:.2f})"
    return None, [], ""


def _fragmented(ranges, text):
    """Too many islands relative to the amount of changed text."""
    covered = sum(b - a for a, b in ranges)
    return len(ranges) > 5 and covered / max(len(text), 1) > 0.40


# ---------------------------------------------------------------- doc model
def body_paragraphs(doc):
    """All body-level paragraphs, preserving their index in doc.paragraphs."""
    return list(doc.paragraphs)


def nonempty_map(doc):
    """Indices into doc.paragraphs of non-empty paragraphs, plus their text."""
    idx, txt = [], []
    for k, p in enumerate(doc.paragraphs):
        t = p.text.strip()
        if t:
            idx.append(k)
            txt.append(t)
    return idx, txt


def table_headers(table):
    return [norm(c.text) for c in table.rows[0].cells]


def head_key(h):
    """Leading label of a column header, ignoring any parenthetical qualifier.

    "specificity (grade c/d)" and "sensitivity (grade a/b)" share the same
    parenthetical shape but are different columns, so the qualifier must not
    drive the match.
    """
    i = h.find("(")
    return (h[:i] if i > 0 else h).strip()


def column_numbers(table, col):
    """Every numeric token in a column, as a set."""
    toks = []
    for row in table.rows[1:]:
        for m in re.findall(r"\d+\.\d+|\d+", row.cells[col].text):
            toks.append(m)
    return set(toks)


def column_score(target, jc, base, ib, th, bh):
    """Header similarity blended with data similarity.

    Names alone cannot separate a renamed column from a new one: when
    "Specificity (Grade D)" grows a sibling "Specificity (Grade C/D)", the
    sibling is the closer string match. The numbers settle it — the renamed
    column still holds the old values, the new one does not.
    """
    h = difflib.SequenceMatcher(None, th[jc], bh[ib], autojunk=False).ratio()
    a, b = column_numbers(target, jc), column_numbers(base, ib)
    d = len(a & b) / len(a | b) if a and b else 0.0
    return 0.5 * h + 0.5 * d


def map_columns(target, base):
    """Align the two header rows as sequences, then pair inside replaced runs."""
    th, bh = table_headers(target), table_headers(base)
    sm = difflib.SequenceMatcher(None, th, bh, autojunk=False)
    col_map, dropped = {}, []
    for tag, i1, i2, j1, j2 in sm.get_opcodes():
        if tag == "equal":
            for k in range(i2 - i1):
                col_map[i1 + k] = j1 + k
            continue
        if tag == "insert":
            continue          # extra target columns: genuinely new
        if tag == "delete":
            dropped.extend(range(j1, j2))
            continue
        cand = []
        for i in range(i1, i2):
            for j in range(j1, j2):
                if head_key(th[i]) != head_key(bh[j]):
                    continue
                s = column_score(target, i, base, j, th, bh)
                if s >= HEADER_SIM:
                    cand.append((s, i, j))
        cand.sort(reverse=True)
        used_i, used_j = set(), set()
        for s, i, j in cand:
            if i in used_i or j in used_j:
                continue
            col_map[i] = j
            used_i.add(i)
            used_j.add(j)
        dropped.extend(j for j in range(j1, j2) if j not in used_j)
    return col_map, dropped


# ---------------------------------------------------------------- alignment
CAPTION_RE = re.compile(r"^\s*(figure|table)\s*(\d+)", re.I)


def caption_key(s):
    """('figure', '2') for a caption paragraph, otherwise None."""
    m = CAPTION_RE.match(s)
    return (m.group(1).lower(), m.group(2)) if m else None


def align_blocks(base_texts, new_texts):
    """Map new-paragraph index -> (kind, base_index, similarity).

    kind in {'equal', 'mod', 'new'}
    """
    sm = difflib.SequenceMatcher(
        None, [norm(x) for x in base_texts], [norm(x) for x in new_texts],
        autojunk=False,
    )
    mapping = {}
    deleted = []
    for tag, i1, i2, j1, j2 in sm.get_opcodes():
        if tag == "equal":
            for k in range(i2 - i1):
                mapping[j1 + k] = ("equal", i1 + k, 1.0)
            continue
        if tag == "insert":
            for j in range(j1, j2):
                mapping[j] = ("new", None, 0.0)
            continue
        if tag == "delete":
            deleted.extend(range(i1, i2))
            continue
        # A submitted paragraph was often split into several revised ones (the
        # Methods step list, for instance). Detect that first: containment is
        # evidence of a split, and left to the one-to-one pass the long merged
        # paragraph would swallow one of its own children as a "rewrite".
        used_i, used_j = set(), set()
        for j in range(j1, j2):
            nt = strip_numbering(norm(new_texts[j]))
            if len(nt) < 50:
                continue
            best_i, best_cov = None, 0.0
            for i in range(i1, i2):
                bt = strip_numbering(norm(base_texts[i]))
                if nt and nt in bt:
                    cov = len(nt) / len(bt)
                    if cov > best_cov:
                        best_i, best_cov = i, cov
            if best_i is not None:
                mapping[j] = ("sub", best_i, 1.0)
                used_i.add(best_i)
                used_j.add(j)

        # Figure and table captions are rewritten wholesale but stay the same
        # caption; pair them by number so a reworded legend does not read as
        # one caption deleted and another added.
        for j in range(j1, j2):
            if j in used_j:
                continue
            ck = caption_key(new_texts[j])
            if not ck:
                continue
            for i in range(i1, i2):
                if i in used_i or caption_key(base_texts[i]) != ck:
                    continue
                r = difflib.SequenceMatcher(
                    None, norm(base_texts[i]), norm(new_texts[j]), autojunk=False
                ).ratio()
                mapping[j] = ("mod", i, r)
                used_i.add(i)
                used_j.add(j)
                break

        # remaining paragraphs: greedy one-to-one pairing inside the block
        cand = []
        for i in range(i1, i2):
            for j in range(j1, j2):
                if j in used_j:
                    continue
                r = difflib.SequenceMatcher(
                    None, strip_numbering(norm(base_texts[i])),
                    strip_numbering(norm(new_texts[j])), autojunk=False
                ).ratio()
                if r >= BLOCK_PAIR_SIM:
                    cand.append((r, i, j))
        cand.sort(reverse=True)
        for r, i, j in cand:
            if i in used_i or j in used_j:
                continue
            used_i.add(i)
            used_j.add(j)
            mapping[j] = ("mod" if r < 0.999 else "equal", i, r)

        for i in range(i1, i2):
            if i not in used_i:
                deleted.append(i)
        for j in range(j1, j2):
            if j not in used_j:
                mapping[j] = ("new", None, 0.0)
    return mapping, sorted(set(deleted))


# ---------------------------------------------------------------- run painter
def _set_highlight(rPr, colour):
    for h in rPr.findall(qn("w:highlight")):
        rPr.remove(h)
    if colour:
        h = rPr.get_or_add_highlight()
        h.set(qn("w:val"), colour)


def paint_paragraph(par, mode, ranges, colour=None):
    """Split the paragraph's runs and highlight according to `mode`.

    mode 'all'     : every non-empty run is highlighted (GREEN by default)
    mode 'partial' : runs are split at the boundaries in `ranges` and the
                     covered characters are highlighted YELLOW

    `colour` overrides the whole-paragraph colour, used to keep table cells
    yellow: a green cell would read as a newly added column even when only the
    number inside it changed.
    """
    if mode is None:
        return 0

    def colour_at(pos, length):
        if mode == "all":
            return colour or GREEN
        for a, b in ranges:
            if pos < b and pos + length > a:
                return YELLOW
        return None

    # a run can straddle a boundary, so expand it into single-character groups
    changed = 0
    pos = 0
    for run in list(par.runs):
        text = run.text
        if not text:
            continue
        start, end = pos, pos + len(text)
        pos = end

        # decide the colour profile of this run character by character
        profile = [colour_at(p, 1) for p in range(start, end)]
        if all(c == profile[0] for c in profile):
            if profile[0]:
                rPr = run._r.get_or_add_rPr()
                _set_highlight(rPr, profile[0])
                changed += 1
            continue

        # split into maximal constant-colour segments
        segs = []
        cur_c, cur_s = profile[0], 0
        for k in range(1, len(profile)):
            if profile[k] != cur_c:
                segs.append((text[cur_s:k], cur_c))
                cur_c, cur_s = profile[k], k
        segs.append((text[cur_s:], cur_c))
        _split_run(run, segs)
        changed += 1
    return changed


def _split_run(run, segs):
    el = run._r
    rPr = el.find(qn("w:rPr"))
    rPr_base = deepcopy(rPr) if rPr is not None else None
    new_els = []
    for text, colour in segs:
        if text == "":
            continue
        r = OxmlElement("w:r")
        if rPr_base is not None:
            rp = deepcopy(rPr_base)
            _set_highlight(rp, colour)
            r.append(rp)
        t = OxmlElement("w:t")
        t.set(qn("xml:space"), "preserve")
        t.text = text
        r.append(t)
        new_els.append(r)
    parent = el.getparent()
    at = list(parent).index(el)
    for k, r in enumerate(new_els):
        parent.insert(at + k, r)
    parent.remove(el)


# ---------------------------------------------------------------- main logic
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--baseline", required=True)
    ap.add_argument("--target", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--csv", default=None)
    ap.add_argument("--deletions", default=None)
    args = ap.parse_args()

    base = Document(args.baseline)
    target = Document(args.target)

    b_idx, b_txt = nonempty_map(base)
    t_idx, t_txt = nonempty_map(target)
    t_pos = {k: i for i, k in enumerate(t_idx)}   # doc.paragraphs index -> text list index

    mapping, deleted = align_blocks(b_txt, t_txt)

    rows = []
    n_par = n_word = n_all = 0
    for j, text in enumerate(t_txt):
        kind, i, sim = mapping.get(j, ("new", None, 0.0))
        if kind == "equal":
            continue
        if i is None:
            mode, ranges = "all", []
            note = "new paragraph"
            n_all += 1
        elif kind == "sub":
            # lifted out of a paragraph that is still present: only the words
            # added while splitting (usually the list number) get marked
            mode, ranges, _ = choose_mode(b_txt[i], text, 1.0)
            note = "split from a merged paragraph"
            if mode == "all":
                mode = None
            n_word += 1 if mode else 0
        else:
            mode, ranges, note = choose_mode(b_txt[i], text, sim)
            if mode is None:
                continue
            if mode == "all":
                n_all += 1
            else:
                n_word += 1
        if mode is None:
            continue
        par = target.paragraphs[t_idx[j]]
        painted = paint_paragraph(par, mode, ranges)
        if painted:
            n_par += 1
            rows.append({
                "scope": "body paragraph",
                "location": f"para {t_idx[j]}",
                "change": note,
                "highlight": mode,
                "chars_marked": len(text) if mode == "all" else sum(b - a for a, b in ranges),
                "text_preview": text[:140].replace("\n", " "),
            })

    # ---------------- tables ----------------
    for k in range(min(len(base.tables), len(target.tables))):
        bt, tt = base.tables[k], target.tables[k]
        bh, th = table_headers(bt), table_headers(tt)
        # map target column -> base column by header text and cell values
        col_map, dropped_cols = map_columns(tt, bt)
        if dropped_cols:
            print(f"  note: table {k + 1} columns absent from the revision "
                  f"(compared by position only): {dropped_cols}")
        for jr in range(min(len(bt.rows), len(tt.rows))):
            for jc in range(len(tt.columns)):
                cell = tt.rows[jr].cells[jc]
                if jc not in col_map:
                    mode = "all"
                    note = "new column"
                    i_ok = False
                else:
                    mode, note = None, None
                    i_ok = True
                    bcell = bt.rows[jr].cells[col_map[jc]]
                    btxt, ttxt = bcell.text.strip(), cell.text.strip()
                    if not ttxt and not btxt:
                        continue
                    if not ttxt:
                        continue
                    if norm(btxt) == norm(ttxt):
                        continue
                    r = difflib.SequenceMatcher(None, norm(btxt), norm(ttxt),
                                                autojunk=False).ratio()
                    mode, ranges, note = choose_mode(btxt, ttxt, r)
                    if mode is None:
                        continue
                if mode == "all" and not cell.text.strip():
                    continue
                for par in cell.paragraphs:
                    paint_paragraph(par, mode,
                                    ranges if mode == "partial" else [],
                                    colour=YELLOW)
                rows.append({
                    "scope": f"table {k + 1}",
                    "location": f"r{jr + 1}c{jc + 1}",
                    "change": note,
                    "highlight": mode,
                    "chars_marked": len(cell.text),
                    "text_preview": cell.text[:140].replace("\n", " "),
                })

    target.core_properties.comments = (
        "Marked-up copy. Yellow = edited text; bright green = new or rewritten "
        f"paragraph. Baseline: {os.path.basename(args.baseline)} (submitted version)."
    )
    target.save(args.out)

    # ---------------- side reports ----------------
    csv_path = args.csv or os.path.splitext(args.out)[0] + "_changes.csv"
    with open(csv_path, "w", encoding="utf-8-sig", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0].keys()) if rows else
                           ["scope", "location", "change", "highlight",
                            "chars_marked", "text_preview"])
        w.writeheader()
        w.writerows(rows)

    del_path = args.deletions or os.path.splitext(args.out)[0] + "_deletions.md"
    with open(del_path, "w", encoding="utf-8") as fh:
        fh.write("# Text removed since the submitted version\n\n")
        fh.write(f"Baseline: `{os.path.basename(args.baseline)}`  \n")
        if deleted:
            fh.write(f"Paragraphs present in the submission but not in the revision: "
                     f"**{len(deleted)}**\n\n")
            for i in deleted:
                fh.write(f"- (para {b_idx[i]}) {b_txt[i]}\n\n")
        else:
            fh.write("**None.** Every paragraph of the submitted version is "
                     "either unchanged or still recognisable in the revision; "
                     "wording changes are marked in place with highlight.\n")

    print(f"paragraphs marked : {n_par}  (word-level {n_word}, whole {n_all})")
    print(f"table cells marked: {sum(1 for r in rows if r['scope'].startswith('table'))}")
    print(f"deleted paragraphs: {len(deleted)}")
    print(f"written           : {args.out}")
    print(f"                    {csv_path}")


if __name__ == "__main__":
    main()
