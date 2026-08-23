# !/usr/bin/env python3
"""Compare manuscript reference fields against Crossref metadata."""
import json, re

REFS = json.load(open(r"./output/refs_dump.json", encoding='utf-8'))
CR = json.load(open(r"./output/crossref_results.json", encoding='utf-8'))

def norm(s):
    if s is None: return ''
    return re.sub(r'[\s\-–-]+', '', str(s)).lower().lstrip('0') or '0'

def parse_ms(text):
    out = {}
    mj = re.search(r'\*([^*]+)\*', text);        out['journal'] = mj.group(1).strip() if mj else ''
    mv = re.search(r'\*\*([^*]+)\*\*', text);    out['volume'] = mv.group(1).strip() if mv else ''
    my = re.search(r'\((\d{4})\)', text);        out['year'] = my.group(1) if my else ''
    # pages/article token between volume-bold and year
    mp = re.search(r'\*\*[^*]+\*\*\s+([\S]+)\s+\(\d{4}\)', text)
    out['page'] = mp.group(1).strip() if mp else ''
    ma = re.search(r'^(\d+)\.\s+([A-Za-zÀ-ÿ\-]+)', text)
    out['first_author'] = ma.group(2) if ma else ''
    return out

rows = []
for num in sorted(REFS, key=int):
    ms = parse_ms(REFS[num])
    cr = CR.get(num, {})
    issues = []
    if cr.get('status') != 'OK':
        issues.append(f"DOI_FAIL({cr.get('status')})")
    else:
        cr_year = cr.get('year')
        if ms['year'] and cr_year and norm(ms['year']) != norm(cr_year):
            issues.append(f"year ms={ms['year']} vs cr={cr_year}")
        if ms['volume'] and cr.get('volume') and norm(ms['volume']) != norm(cr['volume']):
            issues.append(f"vol ms={ms['volume']} vs cr={cr['volume']}")
        # page: ms page may be abbreviated range 658-65 vs 658-665 or article id
        ms_page, cr_page = ms['page'], (cr.get('page') or cr.get('article_number') or '')
        if ms_page and cr_page:
            msp, crp = norm(ms_page), norm(cr_page)
            if msp != crp:
                # allow abbreviated range: "658-65" vs "658-665"
                mm = re.fullmatch(r'(\d+)-(\d+)', msp); cc = re.fullmatch(r'(\d+)-(\d+)', crp)
                if mm and cc and mm.group(1) == cc.group(1) and cc.group(2).startswith(mm.group(2)) and len(cc.group(2)) - len(mm.group(2)) <= 1:
                    pass  # range abbreviation, acceptable
                else:
                    issues.append(f"page ms={ms_page} vs cr={cr_page}")
        # first author surname
        if ms['first_author'] and cr.get('authors'):
            fam = cr['authors'][0][0] or ''
            if norm(ms['first_author']) != norm(fam):
                issues.append(f"author1 ms={ms['first_author']} vs cr={fam}")
        # title head first 5 words - lowercase compare
        ms_title = re.search(r'\.\s+(.+?)\s+\.?\s*\*', REFS[num])
        cr_title = cr.get('title') or ''
        if ms_title and cr_title:
            tw = ' '.join(ms_title.group(1).split()[:5])
            cw = ' '.join(cr_title.split()[:5])
            if norm(tw) != norm(cw):
                issues.append(f"title ms='{tw}' vs cr='{cw}'")
    rows.append((num, ms, cr, issues))

print("=== per-ref issues ===")
n_issue = 0
for num, ms, cr, issues in rows:
    tag = "OK " if not issues else "!! "
    if issues:
        n_issue += 1
    print(f"{tag}ref{num} [{cr.get('status','?')}] " + "; ".join(issues) if issues else f"{tag}ref{num} all-fields-match")
print(f"\nrefs with at least one flagged issue: {n_issue}/79")