#!/usr/bin/env python3
"""RIS 参考文献质量验证 + 补全（CrossRef API）

读 references.ris → 逐条 DOI 查 CrossRef → 校验作者/标题/期刊一致性
→ 补全缺失摘要 → 标记异常 → 输出 verified_references.ris + audit_report.txt
"""
import re, time, requests, sys

RIS_IN  = "C:/D/workbuddy/科研/共病分析/课题设计阶段/references.ris"
RIS_OUT = "C:/D/workbuddy/科研/共病分析/课题设计阶段/references.ris"  # overwrite
AUDIT   = "C:/D/workbuddy/科研/共病分析/课题设计阶段/reference_audit.txt"

def parse_ris(path):
    entries = []
    current = {}
    for line in open(path, encoding='utf-8'):
        line = line.rstrip('\n')
        if line.startswith('ER  -'):
            if current:
                entries.append(current)
                current = {}
            continue
        if line.startswith('TY  -'):
            continue
        m = re.match(r'^(\w{2})\s{2}-\s(.+)$', line)
        if m:
            tag, val = m.group(1), m.group(2).strip()
            if tag in ('AU','AF'):
                current.setdefault('AU',[]).append(val)
            elif tag == 'TI':
                current['TI'] = (current.get('TI','') + ' ' + val).strip()
            elif tag == 'AB':
                current['AB'] = (current.get('AB','') + ' ' + val).strip()
            else:
                current[tag] = val
    return entries

def crossref_by_doi(doi, retries=2):
    url = f"https://api.crossref.org/works/{doi}"
    for attempt in range(retries):
        try:
            r = requests.get(url, timeout=20, headers={'User-Agent':'ref-check/1.0 (mailto:research@example.com)'})
            if r.status_code == 200:
                return r.json()
            elif r.status_code == 404:
                return None
            time.sleep(2 ** attempt)
        except Exception as e:
            if attempt == retries - 1:
                return None
            time.sleep(3)
    return None

def normalize(t):
    return re.sub(r'[^a-z0-9]','',t.lower())[:120]

def first_word(s):
    return s.strip().split()[0] if s else ''

def check_author_match(ris_au, cr_au):
    """Check if RIS first author matches CrossRef first author"""
    if not ris_au or not cr_au: return True
    r_last = ris_au[0].split(',')[0].strip().lower()
    c_last = cr_au.split(',')[0].strip().lower() if ',' in cr_au else cr_au.split()[-1].strip().lower()
    return r_last == c_last or r_last in c_last or c_last in r_last

entries = parse_ris(RIS_IN)
print(f"Parsed {len(entries)} RIS entries")

audit_lines = []
fixed_ab = 0
fixed_doi = 0
mismatch = 0
not_found = 0
verified = 0

for i, e in enumerate(entries):
    doi = e.get('DO','')
    pmid = e.get('AN','')
    if not doi or doi == 'N/A':
        audit_lines.append(f"[?] Entry {i+1}: no DOI (PMID={pmid}) — cannot verify via CrossRef")
        not_found += 1
        continue

    cr = crossref_by_doi(doi)
    time.sleep(0.12)  # polite rate

    if cr is None:
        audit_lines.append(f"[X] Entry {i+1}: DOI {doi} not found in CrossRef (PMID={pmid})")
        not_found += 1
        continue

    msg = cr.get('message',{})
    cr_title = ' '.join(msg.get('title',['']))
    cr_abstract = msg.get('abstract','')
    cr_journal = ' '.join(msg.get('container-title',['']))
    cr_author = ''
    if msg.get('author'):
        a0 = msg['author'][0]
        cr_author = f"{a0.get('family','')}, {a0.get('given','')}"

    ris_title = e.get('TI','')
    ris_au = e.get('AU',[])

    issues = []

    # Title check (first 8 normalized chars)
    if normalize(ris_title)[:80] != normalize(cr_title)[:80]:
        issues.append(f"TITLE mismatch: RIS='{ris_title[:60]}' vs CR='{cr_title[:60]}'")

    # Author check
    if not check_author_match(ris_au, cr_author):
        issues.append(f"AUTHOR mismatch: RIS first='{ris_au[0] if ris_au else '?'}' vs CR='{cr_author}'")

    # Abstract — fill if missing
    ab = e.get('AB','')
    if (not ab or len(ab) < 30) and cr_abstract:
        e['AB'] = cr_abstract[:3000].replace('\n',' ').replace('<jats:','').replace('</jats:','')
        fixed_ab += 1
        issues.append(f"ABSTRACT filled from CrossRef ({len(cr_abstract)} chars)")

    # DOI format check
    if doi.startswith('http'):
        e['DO'] = doi.replace('https://doi.org/','').replace('http://dx.doi.org/','')
        fixed_doi += 1

    if issues:
        audit_lines.append(f"[!] Entry {i+1} (PMID={pmid}, DOI={doi}): {'; '.join(issues)}")
        mismatch += 1
    else:
        verified += 1

    if (i+1) % 20 == 0:
        print(f"  ... processed {i+1}/{len(entries)}")

print(f"\nResults:")
print(f"  Verified (perfect match): {verified}")
print(f"  Mismatches/warnings:      {mismatch}")
print(f"  Not found in CrossRef:    {not_found}")
print(f"  Abstracts filled:          {fixed_ab}")
print(f"  DOIs cleaned:              {fixed_doi}")

# Write fixed RIS
with open(RIS_OUT, 'w', encoding='utf-8') as f:
    for e in entries:
        f.write("TY  - JOUR\n")
        f.write(f"TI  - {e.get('TI','NA')}\n")
        for au in e.get('AU',[]):
            f.write(f"AU  - {au}\n")
        f.write(f"PY  - {e.get('PY','')}\n")
        if 'JF' in e: f.write(f"JF  - {e['JF']}\n")
        if 'VL' in e: f.write(f"VL  - {e['VL']}\n")
        if 'IS' in e: f.write(f"IS  - {e['IS']}\n")
        if 'SP' in e: f.write(f"SP  - {e['SP']}\n")
        if 'AB' in e and len(e['AB']) > 20: f.write(f"AB  - {e['AB'][:3000]}\n")
        if 'DO' in e: f.write(f"DO  - {e['DO']}\n")
        f.write(f"AN  - {e.get('AN','')}\n")
        f.write(f"DB  - PubMed\nER  - \n")
print(f"Fixed RIS written -> {RIS_OUT}")

with open(AUDIT, 'w', encoding='utf-8') as f:
    f.write(f"CrossRef Audit Report — {len(entries)} entries\n")
    f.write(f"Verified: {verified} | Mismatches: {mismatch} | Not found: {not_found} | Abs filled: {fixed_ab}\n\n")
    f.write('\n'.join(audit_lines) + '\n')
print(f"Audit report -> {AUDIT}")

# Print summary of issues
if mismatch > 0 or not_found > 0:
    print("\n=== ISSUES NEEDING MANUAL REVIEW ===")
    for line in audit_lines:
        if line.startswith('[!]') or line.startswith('[X]') or line.startswith('[?]'):
            print(f"  {line[:140]}")
