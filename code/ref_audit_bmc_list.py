# !/usr/bin/env python3
"""Generate BMC/Vancouver-formatted reference list (renumbered by first-citation
order). Manuscript fields parsed from MD (markdown intact); official titles/authors
from Crossref (longer-title wins; person authors preferred over consortium orgs)."""
import json, re, html

CR = json.load(open(r"./output/crossref_results.json", encoding='utf-8'))

md = open(r"./docs/historical/manuscript_draft_with_23refs.md", encoding='utf-8').read()
refsec = md.split('## References')[1]
REFS = {}
for line in refsec.split('\n'):
    m = re.match(r'^(\d+)\.\s+(.*)$', line.strip())
    if m:
        REFS[int(m.group(1))] = m.group(2).strip()

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
    s = re.sub(r'[\s\-–-]+', '', s).lower().rstrip('.')
    return s

def pick_title(ms_t, cr_t):
    if not ms_t: return cr_t
    if not cr_t: return ms_t
    a, b = norm_t(ms_t), norm_t(cr_t)
    if len(a) > len(b) and a.startswith(b): return ms_t
    if len(b) > len(a) and b.startswith(a): return cr_t
    if a == b: return ms_t
    return cr_t  # official title wins

def build_bmc(num):
    ms = parse_ms(REFS[num])
    cr = CR.get(str(num), {})
    ok = cr.get('status') == 'OK'
    if num == 40:
        return "Popper KR. The Logic of Scientific Discovery. Routledge Classics ed. London: Routledge; 2002."
    title = pick_title(ms['title'], html.unescape(cr.get('title') or '') if ok else '')
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
        # if Crossref gives only the first page of a range that manuscript has fully, prefer manuscript range
        if pag and ms['page'] and cr_page:
            if re.fullmatch(r'\d+', cr_page) and re.match(rf'^{cr_page}-\d+', ms['page']):
                pag = ms['page']
        pag = re.sub(r'[\s\-–-]+', '–', str(pag).strip())
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

# ---------- old -> new renumbering first-citation order
old_to_new = {n: n for n in range(1, 51)}
for n in range(51, 78):
    old_to_new[n] = n + 2
old_to_new[78], old_to_new[79] = 51, 52
new_to_old = {v: k for k, v in old_to_new.items()}

new_list = []
for new_n in range(1, 80):
    old_n = new_to_old[new_n]
    new_list.append((new_n, old_n, build_bmc(old_n)))

clean = []
for new_n, old_n, txt in new_list:
    txt = re.sub(r'^\d+\.\s+', '', txt, count=1)
    clean.append(f"{new_n}. {txt}")
open(r"./output/bmc_references_clean.txt", 'w', encoding='utf-8').write('\n'.join(clean))

json.dump(old_to_new, open(r"./output/renumber_map.json", 'w'), indent=1)
print("written bmc_references_clean.txt (79 refs) + renumber_map.json")
print("\n--- full corrected list (new numbering) ---")
for l in clean:
    print(l)