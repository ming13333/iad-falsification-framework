#!/usr/bin/env python3
"""Measure AI-writing tells in a markdown manuscript, before and after an edit.

The detector is deliberately mechanical - it reports counts a second reader can
verify, not a "score".  Five families are measured:

  1. Sentence rhythm.  Academic prose written by a person varies; machine prose is
     uniform and long.  Reported as mean, standard deviation and longest sentence,
     with anything over 70 words listed by position.
  2. Connectives.  'Moreover / Furthermore / In addition / Notably / Importantly'
     opening a sentence, and the same word repeated across paragraphs.
  3. Abstract vocabulary.  Words that assert importance instead of describing work
     ('robust', 'comprehensive', 'crucial', 'novel', 'underscore', 'leverage').
  4. Typographic tics.  Em-dash pairs used as parentheses, and rhetorical triples.
  5. Overclaiming.  'demonstrates / proves / establishes' with no object the data
     could support, and the summary openers ('Overall,' 'Taken together,').

Usage:
    python code/detect_ai_style.py FILE [FILE ...]
    python code/detect_ai_style.py --compare BEFORE.md AFTER.md
"""

import argparse
import os
import re
import statistics
import sys

# periods that do not end a sentence
ABBREV = [
    "et al.", "e.g.", "i.e.", "vs.", "cf.", "approx.", "Fig.", "Figs.", "No.",
    "Dr.", "St.", "esp.", "etc.", "Suppl.", "Tab.", "Ref.", "Eq.", "resp.",
    "al.", "ed.", "eds.", "vol.", "pp.", "ca.",
]

OPENERS = [
    "Moreover", "Furthermore", "In addition", "Additionally", "Notably",
    "Importantly", "Crucially", "Indeed", "Overall", "Taken together",
    "In summary", "In conclusion", "Collectively", "Ultimately", "Consequently",
    "Therefore", "Thus", "Hence", "Nevertheless", "Nonetheless", "However",
]

ABSTRACT_WORDS = [
    "robust", "robustly", "comprehensive", "comprehensively", "crucial",
    "crucially", "pivotal", "paramount", "novel", "nuanced", "intricate",
    "multifaceted", "seamless", "holistic", "landscape", "realm", "testament",
    "underscore", "underscores", "underscoring", "highlight", "highlights",
    "highlighting", "leverage", "leverages", "leveraging", "delve", "delves",
    "delve into", "shed light", "pave the way", "plays a key role",
    "plays a crucial role", "it is worth noting", "it should be noted",
    "a growing body of", "in the realm of", "state-of-the-art", "cutting-edge",
    "meticulous", "meticulously", "invaluable", "game-changer", "paradigm shift",
]

OVERCLAIM = [
    "demonstrates that", "proves that", "establishes that", "confirms that",
    "clearly shows", "definitively", "unequivocally", "unprecedented",
    "first ever", "for the first time",
]


def strip_markdown(text):
    text = re.sub(r"```.*?```", " ", text, flags=re.S)
    text = re.sub(r"^\s*\|.*$", " ", text, flags=re.M)          # table rows
    text = re.sub(r"^\s*!\[.*$", " ", text, flags=re.M)         # images
    text = re.sub(r"\$[^$]*\$", " MATH ", text)                 # inline math
    text = re.sub(r"^\s*#+\s*", "", text, flags=re.M)           # heading marks
    text = re.sub(r"[*_`>]", "", text)
    return text


def paragraphs(text):
    """One line = one paragraph.  Splitting on blank lines alone merges bulleted
    lists and headings into the paragraph above them, which then reads as a single
    100-word 'sentence' that nobody wrote."""
    out = []
    for block in re.split(r"\n\s*\n", text):
        for line in block.split("\n"):
            line = line.strip()
            if line and not line.startswith("#"):
                out.append(line)
    return out


def sentences(text):
    """Split on sentence boundaries after masking abbreviations and initials."""
    masked = text
    # Word boundaries are required: a plain substring replacement of 'ed.' also
    # fires in the middle of 'specified.', which then never ends a sentence and
    # merges the following sentence into a phantom long one.
    abbr_re = re.compile(r"\b(" + "|".join(re.escape(a) for a in ABBREV) + r")")
    masked = abbr_re.sub(lambda m: m.group(1)[:-1] + "\u2024", masked)
    # Mask initials only where they are provably initials: after a comma inside an
    # author list ('Smith, J. C.') or in a run of single capitals ('J. C.').
    # Masking every capital-plus-period also swallowed sentence ends such as
    # 'Grade C. The total ...', which hid a genuine sentence boundary and made a
    # three-sentence passage read as one 115-word sentence.
    masked = re.sub(r"(?<=, )([A-Z])\.", lambda m: m.group(1) + "\u2024", masked)
    masked = re.sub(r"\b([A-Z])\.(?= [A-Z]\.)", lambda m: m.group(1) + "\u2024", masked)
    masked = re.sub(r"(\d)\.(\d)", lambda m: m.group(1) + "\u2024" + m.group(2), masked)
    parts = re.split(r"(?<=[.!?])\s+(?=[A-Z(\"'\u2018\u201c])", masked)
    return [p.replace("\u2024", ".").strip() for p in parts if p.strip()]


def words(s):
    return [w for w in re.split(r"\s+", s) if w]


def count_phrase(text, phrase):
    return len(re.findall(r"\b" + re.escape(phrase) + r"\b", text, re.I))


def body_of(raw):
    """Prose only: drop the reference list and anything before the abstract."""
    i = raw.find("## Introduction")
    j = raw.find("## References")
    if i < 0 or j < i:
        return raw
    head = raw[:i]
    tail = raw[j:]
    k = tail.find("\n## Tables")
    return head + raw[i:j] + (tail[k:] if k >= 0 else "")


def analyse(path):
    raw = open(path, encoding="utf-8").read()
    body = strip_markdown(body_of(raw))
    paras = paragraphs(body)
    sents = [s for p in paras for s in sentences(p)]
    lens = [len(words(s)) for s in sents]

    opener_hits = {}
    for p in paras:
        first = sentences(p)
        if not first:
            continue
        head = first[0]
        for o in OPENERS:
            if head.lower().startswith(o.lower()):
                opener_hits[o] = opener_hits.get(o, 0) + 1

    abstract_hits = {}
    for w in ABSTRACT_WORDS:
        n = count_phrase(body, w)
        if n:
            abstract_hits[w] = n

    overclaim_hits = {}
    for w in OVERCLAIM:
        n = count_phrase(body, w)
        if n:
            overclaim_hits[w] = n

    dashes = body.count("\u2014")
    dash_pairs = len(re.findall(r"\u2014[^\u2014]{1,80}\u2014", body))

    long_sents = [(i, len(words(s)), s) for i, s in enumerate(sents) if len(words(s)) > 70]

    return {
        "path": path,
        "paragraphs": len(paras),
        "sentences": len(sents),
        "words": sum(lens),
        "len_mean": statistics.mean(lens) if lens else 0,
        "len_sd": statistics.pstdev(lens) if len(lens) > 1 else 0,
        "len_max": max(lens) if lens else 0,
        "long_sentences": long_sents,
        "openers": opener_hits,
        "opener_total": sum(opener_hits.values()),
        "abstract": abstract_hits,
        "abstract_total": sum(abstract_hits.values()),
        "overclaim": overclaim_hits,
        "dashes": dashes,
        "dash_pairs": dash_pairs,
    }


def show(r):
    print(f"== {os.path.basename(r['path'])} ==")
    print(f"   {r['paragraphs']} paragraphs, {r['sentences']} sentences, {r['words']} words")
    print(f"   sentence length  mean {r['len_mean']:.1f}  sd {r['len_sd']:.1f}  max {r['len_max']}")
    print(f"   sentences > 70 words: {len(r['long_sentences'])}")
    for i, n, s in r["long_sentences"]:
        print(f"      #{i} ({n}w): {s[:100]}...")
    print(f"   sentence-opening connectives: {r['opener_total']} {r['openers'] or ''}")
    print(f"   abstract vocabulary: {r['abstract_total']} {r['abstract'] or ''}")
    print(f"   overclaiming: {r['overclaim'] or 'none'}")
    print(f"   em-dashes: {r['dashes']}  (parenthetical pairs: {r['dash_pairs']})")
    print()
    # per-paragraph flag list, so edits can be aimed rather than guessed
    print("   paragraphs with more than one tell:")
    for k, p in enumerate(paragraphs(strip_markdown(body_of(open(r["path"], encoding="utf-8").read())))):
        ss = sentences(p)
        flags = []
        if any(len(words(s)) > 70 for s in ss):
            flags.append("long")
        if ss and any(ss[0].lower().startswith(o.lower()) for o in OPENERS):
            flags.append("opener")
        aw = [w for w in ABSTRACT_WORDS if count_phrase(p, w)]
        if aw:
            flags.append("abstract:" + ",".join(aw[:3]))
        if len(re.findall(r"\u2014[^\u2014]{1,80}\u2014", p)):
            flags.append("dashpair")
        if len(flags) > 1:
            print(f"      p{k:02d} [{'; '.join(flags)}] {p[:90]}...")
    print()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("files", nargs="+")
    ap.add_argument("--compare", nargs=2, metavar=("BEFORE", "AFTER"))
    args = ap.parse_args()

    if args.compare:
        a, b = analyse(args.compare[0]), analyse(args.compare[1])
        for key, label, fmt in [
            ("words", "words", "{:.0f}"),
            ("len_mean", "mean sentence length", "{:.1f}"),
            ("len_sd", "sentence-length sd", "{:.1f}"),
            ("len_max", "longest sentence", "{:.0f}"),
            ("opener_total", "opening connectives", "{:.0f}"),
            ("abstract_total", "abstract vocabulary", "{:.0f}"),
            ("dashes", "em-dashes", "{:.0f}"),
            ("dash_pairs", "em-dash pairs", "{:.0f}"),
        ]:
            print(f"{label:26s} {fmt.format(a[key]):>7} -> {fmt.format(b[key]):>7}")
        print(f"{'sentences > 70 words':26s} {len(a['long_sentences']):>7} -> "
              f"{len(b['long_sentences']):>7}")
        return 0

    for f in args.files:
        show(analyse(f))
    return 0


if __name__ == "__main__":
    sys.exit(main())
