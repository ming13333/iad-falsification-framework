# !/usr/bin/env python3
"""Compare manuscript reference fields (parsed from MD, markdown intact) vs Crossref."""
import json, re

md = open(r"./docs/historical/manuscript_draft_with_23refs.md", encoding='utf-8').read()
refsec = md.split('## References')[1]
refs = {}
for line in refsec.split('\n'):
    m = re.match(r'^(\d+)\.\s+(.*)$', line.strip())
    if m:
        refs[int(m.group(1))] = m.group(2).strip()

CR = json.load(open(r"./output/crossref_results.json", encoding='utf-8'))

def norm(s):
    if s is None: return ''
    s = str(s)
    # normalize unicode punctuation & accents for comparison
    s = s.replace('\u2010', '-').replace('\u2011', '-').replace('\u2012', '-').replace('\u2013', '-').replace('\u2014', '-')
    s = s.replace('\u2018', "'").replace('\u2019', "'").replace('\u201c', '"').replace('\u201d', '"')
    s = re.sub(r'[\s\-–-]+', '', s).lower().lstrip('0') or '0'
    return s

def norm_title(s):
    if s is None: return ''
    s = norm(s)
    # drop accents for title compare
    import unicodedata
    s = ''.join(c for c in unicodedata.normalize('NFD', s) if not unicodedata.combining(c))
    return s

def parse_ms(text):
    out = {}
    mj = re.search(r'\*([^*]+)\*', text);        out['journal'] = mj.group(1).strip() if mj else ''
    mv = re.search(r'\*\*([^*]+)\*\*', text);    out['volume'] = mv.group(1).strip() if mv else ''
    my = re.search(r'\((\d{4})\)', text);        out['year'] = my.group(1) if my else ''
    mp = re.search(r'\*\*[^*]+\*\*\s+([\S]+)\s+\(\d{4}\)', text)
    out['page'] = mp.group(1).strip() if mp else ''
    ma = re.search(r'^([A-Za-zÀ-ÿ\-]+)', text)
    out['first_author'] = ma.group(1) if ma else ''
    return out

def is_range_abbrev(a, b):
    mm = re.fullmatch(r'(\d+)-(\d+)', a); cc = re.fullmatch(r'(\d+)-(\d+)', b)
    if mm and cc and mm.group(1) == cc.group(1) and cc.group(2).endswith(mm.group(2)):
        return True
    return False

rows = []
for num in sorted(refs, key=int):
    ms = parse_ms(refs[num])
    cr = CR.get(str(num), {})
    issues = []
    if cr.get('status') != 'OK':
        issues.append(f"DOI_FAIL({cr.get('status')})")
    else:
        cr_year = cr.get('year')
        if ms['year'] and cr_year and norm(ms['year']) != norm(cr_year):
            issues.append(f"year ms={ms['year']} vs cr={cr_year}")
        if ms['volume'] and cr.get('volume') and norm(ms['volume']) != norm(cr['volume']):
            issues.append(f"vol ms={ms['volume']} vs cr={cr['volume']}")
        ms_page, cr_page = ms['page'], (cr.get('page') or cr.get('article_number') or '')
        if ms_page and cr_page:
            msp, crp = norm(ms_page), norm(cr_page)
            if msp != crp and not is_range_abbrev(msp, crp) and not is_range_abbrev(crp, msp):
                issues.append(f"page ms={ms_page} vs cr={cr_page}")
        if ms['first_author'] and cr.get('authors'):
            fam = cr['authors'][0][0] or ''
            if norm(ms['first_author']) != norm(fam):
                issues.append(f"author1 ms={ms['first_author']} vs cr={fam}")
        # full-title compare normalized, accent/punct-insensitive
        mt = re.search(r'\.\s+(.+?)\s+\*', refs[num])
        crt = cr.get('title') or ''
        if mt and crt:
            ms_t, cr_t = norm_title(mt.group(1)), norm_title(crt)
            ms_t = ms_t.rstrip('.')
            cr_t = cr_t.rstrip('.')
            if ms_t != cr_t:
                if cr_t.startswith(ms_t) and len(cr_t) - len(ms_t) >= 4:
                    issues.append(f"TITLE-TRUNCATED: ms='{mt.group(1)}' CR='{crt}'")
                elif ms_t.startswith(cr_t) and len(ms_t) - len(cr_t) >= 4:
                    issues.append(f"TITLE-EXTENDED: ms='{mt.group(1)}' CR='{crt}'")
                else:
                    issues.append(f"TITLE-DIFF: ms='{mt.group(1)}' CR='{crt}'")
    rows.append((num, ms, cr, issues))

n_issue = 0
for num, ms, cr, issues in rows:
    if issues:
        n_issue += 1
        print(f"!! ref{num}: " + "; ".join(issues))
print(f"\nrefs flagged: {n_issue}/79")
# aggregate checks coverage
chk = {'year': 0, 'vol': 0, 'page': 0, 'author1': 0, 'title': 0, 'matched': 0}
for num, ms, cr, issues in rows:
    if cr.get('status') != 'OK': continue
    for k, msf, crf in [('year', ms['year'], cr.get('year')),
                        ('vol', ms['volume'], cr.get('volume')),
                        ('page', ms['page'], cr.get('page') or cr.get('article_number') or ''),
                        ('author1', ms['first_author'], (cr.get('authors') or [['']])[0][0]),
                        ('title', (re.search(r'\.\s+(.+?)\.\s*\*', refs[num]).group(1) if re.search(r'\.\s+(.+?)\.\s*\*', refs[num]) else ''), cr.get('title') or '')]:
        if msf and crf:
            chk[k] += 1
print("fields actually compared (non-empty both sides):", chk)