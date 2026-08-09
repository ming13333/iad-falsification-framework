#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Apply reference-audit fixes to the GM manuscript:
  1. discard refs 31, 35, 37 (doubtful per Crossref audit)
  2. drop the misplaced [43] marker in the 'BMI-AD contested' sentence
  3. recompute first-citation order -> full renumbering (old->new)
  4. rewrite ALL in-text citation tokens with the new mapping
  5. rebuild the reference list (BMC/Vancouver format, Crossref-verified) 1..N
  6. verify: no dangling, all cited, strict first-cite ordering
"""
import json, re, html

MD = r"C:/D/workbuddy/科研/共病分析/课题设计阶段/manuscript_draft_with_23refs.md"
CR = json.load(open(r"C:/Temp/iad_g1/crossref_results.json", encoding='utf-8'))
DEL = {31, 35, 37}

# ---------------- reference formatting helpers (from audit) ----------------
JRNL_MAP = {
    "International Journal of Epidemiology": "Int J Epidemiol",
    "Journal of Affective Disorders": "J Affect Disord",
    "Alzheimer's & Dementia": "Alzheimers Dement",
    "Nature Human Behaviour": "Nat Hum Behav",
    "Nature Communications": "Nat Commun",
    "Nature Genetics": "Nat Genet",
    "Nature Aging": "Nat Aging",
    "The Lancet Neurology": "Lancet Neurol",
    "The Lancet": "Lancet",
    "The New England Journal of Medicine": "N Engl J Med",
    "Journal of the American Heart Association": "J Am Heart Assoc",
    "Frontiers in Neurology": "Front Neurol",
    "Frontiers in Aging Neuroscience": "Front Aging Neurosci",
    "Frontiers in Genetics": "Front Genet",
    "Genetic Epidemiology": "Genet Epidemiol",
    "QJM: An International Journal of Medicine": "QJM",
    "Cold Spring Harbor Perspectives in Medicine": "Cold Spring Harb Perspect Med",
    "European Archives of Psychiatry and Clinical Neuroscience": "Eur Arch Psychiatry Clin Neurosci",
    "Journal of Alzheimer's Disease": "J Alzheimers Dis",
    "Cardiovascular Diabetology": "Cardiovasc Diabetol",
    "Circulation: Genomic and Precision Medicine": "Circ Genom Precis Med",
    "Sleep Medicine": "Sleep Med",
    "Seminars in Immunology": "Semin Immunol",
    "Acta Neuropathologica": "Acta Neuropathol",
    "Alzheimer's Research & Therapy": "Alzheimers Res Ther",
    "BMC Medicine": "BMC Med",
    "PLOS Medicine": "PLoS Med",
    "PLoS Genetics": "PLoS Genet",
    "American Journal of Epidemiology": "Am J Epidemiol",
    "eBioMedicine": "EBioMedicine",
}

def initials(given):
    if not given:
        return ''
    res = []
    for part in re.split(r'\s+', given):
        toks = part.split('-')
        res.append('-'.join(t[0].upper() if t and t[0].isalpha() else '' for t in toks))
    return ''.join(res)

def bmc_authors(authors):
    if not authors:
        return ''
    persons = [a for a in authors if not a.get('org', False)]
    orgs = [a for a in authors if a.get('org', False)]
    use = persons if persons else orgs
    parts = []
    for a in use[:6]:
        fam = (a.get('fam') or '').strip()
        ini = initials(a.get('giv') or '')
        parts.append((fam + ' ' + ini).strip())
    if len(use) > 6:
        parts.append('et al.')
    return ', '.join(p for p in parts if p).rstrip('.')

def parse_ms(text):
    out = {}
    mj = re.search(r'\*([^*]+)\*', text);        out['journal'] = mj.group(1).strip() if mj else ''
    mv = re.search(r'\*\*([^*]+)\*\*', text);    out['volume'] = mv.group(1).strip() if mv else ''
    my = re.search(r'\((\d{4})\)', text);        out['year'] = my.group(1) if my else ''
    mp = re.search(r'\*\*[^*]+\*\*\s+([\S]+)\s+\(\d{4}\)', text)
    out['page'] = mp.group(1).strip() if mp else ''
    mt = re.search(r'\.\s+(.+?)\s+\*', text)
    out['title'] = mt.group(1).strip() if mt else ''
    ma = re.search(r'^([^,]+)', text)
    out['first_author'] = ma.group(1).strip() if ma else ''
    return out

def norm_t(s):
    s = s.replace('\u2010', '-').replace('\u2011', '-').replace('\u2019', "'")
    return re.sub(r'[\s\-–—]+', '', s).lower().rstrip('.')

def pick_title(ms_t, cr_t):
    if not ms_t: return cr_t
    if not cr_t: return ms_t
    a, b = norm_t(ms_t), norm_t(cr_t)
    if len(a) > len(b) and a.startswith(b): return ms_t
    if len(b) > len(a) and b.startswith(a): return cr_t
    if a == b: return ms_t
    return cr_t

def build_bmc(num, ms):
    cr = CR.get(str(num), {})
    ok = cr.get('status') == 'OK'
    if num == 40:
        return "Popper KR. The Logic of Scientific Discovery. Routledge Classics ed. London: Routledge; 2002."
    title = pick_title(ms['title'], html.unescape(cr.get('title') or '') if ok else '')
    title = title.rstrip('*†').strip()
    au = bmc_authors(cr.get('authors') or []) if ok else ms['first_author']
    if not au:
        au = ms['first_author']
    jrn = ms['journal']
    if not jrn and ok:
        j = html.unescape(cr.get('short_container') or cr.get('container') or '')
        jrn = JRNL_MAP.get(j, j)
    jrn = jrn.replace('.', '').strip()
    if num == 10:
        year, vol, iss, pag = '2016', '45', '6', '1866–1886'
    else:
        year = cr.get('year') or ms['year']
        vol = cr.get('volume') or ms['volume']
        iss = cr.get('issue') or ''
        cr_page = cr.get('page') or cr.get('article_number') or ''
        pag = cr_page or ms['page'] or ''
        if pag and ms['page'] and cr_page:
            if re.fullmatch(r'\d+', cr_page) and re.match(rf'^{cr_page}-\d+', ms['page']):
                pag = ms['page']
        pag = re.sub(r'[\s\-–—]+', '–', str(pag).strip())
    tail = f"{jrn}. " if jrn else ''
    tail += f"{year}"
    if vol:
        tail += f";{vol}"
        if iss:
            tail += f"({iss})"
    if pag:
        tail += f":{pag}"
    tail += "."
    doi = f" {cr.get('doi')}." if ok and cr.get('doi') else ''
    return f"{au}. {title}. {tail}{doi}"

# ---------------- load original md & refs ----------------
orig = open(MD, encoding='utf-8').read()
main_orig, refsec_orig = orig.split('## References', 1)
REFS = {}
for line in refsec_orig.split('\n'):
    m = re.match(r'^(\d+)\.\s+(.*)$', line.strip())
    if m:
        REFS[int(m.group(1))] = m.group(2).strip()
print("original refs:", len(REFS))

# ---------------- 1) rewrite citation tokens: drop DEL numbers ----------------
CIT_RE = re.compile(r'\[(\d+(?:\s*[-,–]\s*\d+)?(?:\s*,\s*\d+(?:\s*[-,–]\s*\d+)?)*)\]')

def token_numbers(tok):
    nums = []
    for t in re.split(r'\s*,\s*', tok):
        mm = re.match(r'^(\d+)\s*[-–]\s*(\d+)$', t)
        if mm:
            nums += list(range(int(mm.group(1)), int(mm.group(2)) + 1))
        else:
            nums.append(int(t))
    return nums

def render_numbers(nums):
    """render sorted unique nums as Vancouver token: consecutive runs -> a-b."""
    nums = sorted(set(nums))
    if not nums:
        return None
    parts, start = [], nums[0]
    prev = nums[0]
    for n in nums[1:] + [None]:
        if n is not None and n == prev + 1:
            prev = n
            continue
        parts.append(str(start) if start == prev else f"{start}-{prev}")
        if n is not None:
            start = prev = n
    return ','.join(parts)

def rewrite_main(text):
    out, pos = [], 0
    for m in CIT_RE.finditer(text):
        nums = [n for n in token_numbers(m.group(1)) if n not in DEL]
        out.append(text[pos:m.start()])
        r = render_numbers(nums)
        if r is not None:
            out.append('[' + r + ']')
        pos = m.end()
    out.append(text[pos:])
    return ''.join(out)

main_rewritten = rewrite_main(main_orig)
# drop the misplaced [43] at the BMI-AD sentence (standalone marker)
main_rewritten = main_rewritten.replace('relationship [43]; assigning',
                                        'relationship; assigning')

# ---------------- 2) first-citation order on rewritten main ----------------
first = {}
for m in CIT_RE.finditer(main_rewritten):
    for n in token_numbers(m.group(1)):
        if n not in first:
            first[n] = m.start()
ordered = sorted((n for n in first if n not in DEL), key=lambda n: (first[n], n))
old_to_new = {n: i + 1 for i, n in enumerate(ordered)}
new_to_old = {v: k for k, v in old_to_new.items()}
print("refs kept:", len(ordered), "| mapping:", old_to_new)

# ---------------- 3) remap all tokens ----------------
def remap_token(tok):
    items = re.split(r'\s*,\s*', tok)
    new_items = []
    for it in items:
        mm = re.match(r'^(\d+)\s*[-–]\s*(\d+)$', it)
        if mm:
            a, b = old_to_new[int(mm.group(1))], old_to_new[int(mm.group(2))]
            new_items.append(f"{a}-{b}")
        else:
            new_items.append(str(old_to_new[int(it)]))
    return ','.join(new_items)

main_final, pos = [], 0
for m in CIT_RE.finditer(main_rewritten):
    main_final.append(main_rewritten[pos:m.start()])
    main_final.append('[' + remap_token(m.group(1).replace(' ', '')) + ']')
    pos = m.end()
main_final.append(main_rewritten[pos:])
main_final = ''.join(main_final)

# ---------------- 4) rebuild reference list ----------------
entries = []
for new_n in range(1, len(ordered) + 1):
    old_n = new_to_old[new_n]
    entry = build_bmc(old_n, parse_ms(REFS[old_n]))
    entry = re.sub(r'\.\.\s+', '. ', entry)
    entry = entry.replace('Artigas MS,', 'Soler Artigas M,')
    entries.append(f"{new_n}. {entry}")
ref_list = '\n'.join(entries)

new_md = main_final + '## References\n\n' + ref_list + '\n'
open(MD, 'w', encoding='utf-8').write(new_md)
json.dump({str(k): v for k, v in old_to_new.items()},
          open(r"C:/Temp/iad_g1/renumber_map_final.json", 'w'), indent=1)
print("written:", MD, "| new refs:", len(entries))

# ---------------- 5) verify ----------------
main_check = new_md.split('## References')[0]
cited = set()
for m in CIT_RE.finditer(main_check):
    cited.update(token_numbers(m.group(1)))
have = set(old_to_new)
dangling = sorted(cited - have)
uncited = sorted(have - cited)
seq = sorted(cited, key=lambda n: next(m.start() for m in CIT_RE.finditer(main_check) if n in token_numbers(m.group(1))))
# strict order check on rewritten main: refs must first-cite in 1..N order
order_ok = True
for i, n in enumerate(seq):
    if n != i + 1:
        order_ok = False
        print("ORDER VIOLATION at position", i + 1, "ref", n)
print("VERIFY: refs=", len(have), "cited=", len(cited),
      "dangling=", dangling, "uncited=", uncited, "strict-order=", order_ok)
