# !/usr/bin/env python3
"""Parse the GM manuscript: extract in-text citations + reference list; check
coverage (dangling / uncited) and BMC ordering (numbering by order of first citation)."""
import re
from docx import Document

DOCX = r"./docs/historical/manuscript_GenomeMedicine_submission.docx"
MD   = r"./docs/historical/manuscript_draft_with_23refs.md"

# ---------- 1. reference list from docx
d = Document(DOCX)
paras = [p.text for p in d.paragraphs]
ref_idx = [i for i, t in enumerate(paras) if t.strip() == 'References']
assert ref_idx, "References heading not found"
ref_paras = [t for t in paras[ref_idx[0]+1:] if t.strip()]
refs = {}
for t in ref_paras:
    m = re.match(r'^(\d+)\.\s+(.*)$', t.strip())
    if m:
        refs[int(m.group(1))] = m.group(2).strip()
    else:
        print("WARN non-ref paragraph in refs section:", t[:60])
print("refs parsed from docx:", len(refs), "min:", min(refs), "max:", max(refs))

# ---------- 2. citations from md full text
with open(MD, encoding='utf-8') as f:
    mdtext = f.read()

# strip the reference list section itself so list lines don't pollute
md_main = mdtext.split('## References')[0]

CIT_RE = re.compile(r'\[(\d+(?:\s*[-,–]\s*\d+)?(?:\s*,\s*\d+(?:\s*[-,–]\s*\d+)?)*)\]')

def expand(tok):
    toks = re.split(r'\s*,\s*', tok)
    out = []
    for t in toks:
        t = t.strip()
        mm = re.match(r'^(\d+)\s*[-–]\s*(\d+)$', t)
        if mm:
            a, b = int(mm.group(1)), int(mm.group(2))
            out.extend(range(a, b+1))
        else:
            out.append(int(t))
    # dedupe preserving ascending order
    seen = set(); res = []
    for n in out:
        if n not in seen:
            seen.add(n); res.append(n)
    return res

first_cite = {}          # refnum -> (char offset, snippet)
cited_nums = set()
cit_tokens = []
for m in CIT_RE.finditer(md_main):
    nums = expand(m.group(1))
    cited_nums.update(nums)
    cit_tokens.append(m.group(0))
    for n in nums:
        if n not in first_cite:
            first_cite[n] = (m.start(), md_main[max(0, m.start()-60):m.end()+10].replace('\n', ' '))

missing = sorted(cited_nums - set(refs))          # cited but not defined
uncited = sorted(set(refs) - cited_nums)          # defined but never cited

print("\n=== citation token count:", len(cit_tokens))
print("cited distinct ref numbers:", len(cited_nums))
print("dangling citations (cited but no ref):", missing)
print("uncited refs (in list, never cited):", uncited)

# ---------- 3. BMC ordering: refs should be numbered by first citation
order = sorted(first_cite.items(), key=lambda kv: kv[1][0])
seq = [n for n, _ in order]
print("\n=== first-citation order of reference numbers ===")
print(seq)
viol = []
for i in range(1, len(seq)):
    if seq[i] < seq[i-1]:
        viol.append((seq[i-1], seq[i]))
print("ordering descents (prev, current):", viol)

# which list positions violate the strict 1..N first-citation sequence
bad_pos = [i+1 for i, n in enumerate(seq) if n != i+1]
print("list positions whose number != first-citation index:", bad_pos[:40], "count:", len(bad_pos))

# also: refs never cited appear at the end? show their position
print("\nuncited ref numbers (with first-cite offset if any):")
for n in uncited:
    print("  ref", n, "first_cite:", first_cite.get(n, "NEVER"))

# ---------- 4. contexts for flagged numbers
import json
print("\n=== first-citation contexts for flagged refs ===")
for n in [6, 7, 8, 9, 30, 31, 32, 43, 44, 45, 46, 47, 48, 51, 78, 79]:
    off, snip = first_cite.get(n, (None, "NOT CITED"))
    print(f"ref {n}: offset={off} | ...{snip}...")

# ---------- 5. dump refs for crossref stage
with open(r"./output/refs_dump.json", 'w', encoding='utf-8') as f:
    json.dump({str(k): v for k, v in sorted(refs.items())}, f, ensure_ascii=False, indent=1)
print("\ndumped refs to ./output/refs_dump.json")