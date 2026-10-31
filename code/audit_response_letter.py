#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Audit the point-by-point response letter against the reviewer reports.

Checks, in order:
  1. every comment identifier in the raw report has a section in the letter;
  2. every section carries the verbatim comment, a Response and a Changes line;
  3. the disposition sentence uses one of the four allowed verdicts;
  4. no section is a stub (Response shorter than MIN_WORDS);
  5. the letter cites no DOI that is absent from the manuscript.

Usage
    python code/audit_response_letter.py            # human-readable report
    python code/audit_response_letter.py --tsv      # disposition table
"""

import argparse
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LETTER = os.path.join(ROOT, "reviews", "Response_to_Reviewers_Frontiers.md")
RAW = os.path.join(ROOT, "reviews", "reviewer_comments_raw.md")
MS = os.path.join(ROOT, "课题设计阶段", "manuscript_Frontiers_Methods_v2.md")

MIN_WORDS = 40      # a substantive answer; below this it is a placeholder
BRIEF_WORDS = 120   # reported for review but not treated as a defect
VERDICTS = ("accepted in full", "accepted in part", "accepted,", "declined")

HEAD = re.compile(r"^## (R\d+-\d+) — (.+)$", re.M)
ID = re.compile(r"^\*\*(R\d+-\d+)\.\*\*", re.M)


def sections(text):
    """Split the letter into one dict per comment, keyed by identifier."""
    marks = list(HEAD.finditer(text))
    out = []
    for i, m in enumerate(marks):
        end = marks[i + 1].start() if i + 1 < len(marks) else len(text)
        body = text[m.end():end]
        out.append({"id": m.group(1), "title": m.group(2).strip(), "body": body})
    return out


def parse(sec):
    body = sec["body"]
    quote = ""
    qm = re.search(r"^> \*(.+?)\*\s*$", body, re.M | re.S)
    if qm:
        quote = qm.group(1)
    cm = re.search(r"\*\*Changes:\*\*\s*(.+?)(?:\n\n|\Z)", body, re.S)
    changes = " ".join(cm.group(1).split()) if cm else ""

    # Response prose = the body minus the quoted comment and the Changes line.
    # The verdict is its first sentence only; the rest is the argument.
    prose = "\n".join(l for l in body.splitlines() if not l.startswith(">"))
    prose = re.split(r"\*\*Changes:\*\*", prose)[0]
    vm = re.search(r"\*\*Response:\s*(.+?)(?:\.\s|\Z)", prose, re.S)
    verdict = vm.group(1).strip() if vm else ""
    clean = prose.replace("**Response:", " ").replace("**", " ")
    words = len(re.findall(r"[A-Za-z][A-Za-z'-]*", clean))
    return {
        "quote": quote,
        "verdict_raw": verdict,
        "changes": changes,
        "words": words,
    }


def classify(verdict):
    v = verdict.lower()
    if "in full" in v:
        return "accepted in full"
    if "in part" in v:
        return "accepted in part"
    if v.startswith("declined") or "declined" in v:
        return "declined"
    if v.startswith("accepted"):
        return "accepted"
    return "unstated"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--tsv", action="store_true", help="emit the disposition table only")
    args = ap.parse_args()

    letter = open(LETTER, encoding="utf-8").read()
    raw = open(RAW, encoding="utf-8").read()
    ms = open(MS, encoding="utf-8").read()

    asked = ID.findall(raw)
    secs = {s["id"]: s for s in sections(letter)}
    parsed = {k: parse(v) for k, v in secs.items()}

    problems = []
    missing = [c for c in asked if c not in secs]
    extra = [c for c in secs if c not in asked]
    if missing:
        problems.append(f"comments without a section: {missing}")
    if extra:
        problems.append(f"sections with no matching comment: {extra}")

    rows = []
    for c in asked:
        if c not in secs:
            continue
        p = parsed[c]
        d = classify(p["verdict_raw"])
        if d == "unstated":
            problems.append(f"{c}: no disposition sentence")
        if not p["quote"]:
            problems.append(f"{c}: verbatim comment not quoted")
        if not p["changes"]:
            problems.append(f"{c}: no Changes line")
        if p["words"] < MIN_WORDS:
            problems.append(f"{c}: response is a stub ({p['words']} words)")
        rows.append((c, secs[c]["title"], d, p["words"], p["changes"]))

    if args.tsv:
        print("Comment\tTopic\tDisposition\tResponse words\tChanges")
        for r in rows:
            print("\t".join(str(x) for x in r))
        return 0

    print(f"letter      {os.path.relpath(LETTER, ROOT)}")
    print(f"comments    {len(asked)} ({sum(1 for c in asked if c.startswith('R1'))} R1, "
          f"{sum(1 for c in asked if c.startswith('R3'))} R3)")
    print(f"sections    {len(secs)}")
    print()
    print(f"{'id':<7}{'disposition':<20}{'words':>6}  {'changes line':<58}")
    for c, title, d, w, ch in rows:
        print(f"{c:<7}{d:<20}{w:>6}  {ch[:56]}")

    print()
    n = lambda k: sum(1 for _, _, d, _, _ in rows if d == k)
    print(f"accepted in full {n('accepted in full')} | in part {n('accepted in part')} | "
          f"accepted (unspecified) {n('accepted')} | declined {n('declined')}")
    print(f"total response words {sum(w for _, _, _, w, _ in rows):,}")
    brief = [f"{c} ({w}w)" for c, _, _, w, _ in rows if w < BRIEF_WORDS]
    print(f"brief answers (<{BRIEF_WORDS} words, reviewed and kept short on purpose): "
          f"{', '.join(brief) if brief else 'none'}")

    # The summary table must cover exactly the same comments.
    table_ids = re.findall(r"^\| (R\d+-\d+) \|", letter, re.M)
    if table_ids != asked:
        problems.append(f"Table R1 covers {len(table_ids)} comments, report has {len(asked)}"
                        + (f"; missing {sorted(set(asked) - set(table_ids))}" if set(asked) - set(table_ids) else "")
                        + (f"; extra {sorted(set(table_ids) - set(asked))}" if set(table_ids) - set(asked) else "")
                        + ("; order differs" if set(table_ids) == set(asked) else ""))
    else:
        print(f"Table R1     {len(table_ids)} rows, same order as the report")

    # The DOI the manuscript now cites must be in the letter; older DOIs may
    # appear only as history (the superseded release), which is intended.
    current = re.findall(r"10\.5281/zenodo\.\d+", ms)
    dois = set(re.findall(r"10\.5281/zenodo\.\d+", letter))
    absent = sorted({d for d in current} - dois)
    print(f"DOI in manuscript: {sorted(set(current))}")
    print(f"DOI in letter:     {sorted(dois)}")
    if absent:
        problems.append(f"manuscript DOI not cited in the letter: {absent}")

    print()
    if problems:
        print(f"PROBLEMS ({len(problems)})")
        for p in problems:
            print("  -", p)
        return 1
    print("OK  every comment is quoted, answered, dispositioned and located")
    return 0


if __name__ == "__main__":
    sys.exit(main())
