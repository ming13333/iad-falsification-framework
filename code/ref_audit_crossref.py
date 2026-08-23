# !/usr/bin/env python3
"""Batch-verify all 79 reference DOIs against Crossref API."""
import json, re, time, urllib.request, urllib.error

REFS = json.load(open(r"./output/refs_dump.json", encoding='utf-8'))
OUT = r"./output/crossref_results.json"

def extract_doi(text):
    m = re.search(r'doi:\s*([^\s]+)', text)
    if m:
        return m.group(1).rstrip('.,)')
    m = re.search(r'https?://(?:dx\.)?doi\.org/(\S+)', text)
    return m.group(1).rstrip('.,)') if m else None

def fetch(doi):
    url = f"https://api.crossref.org/works/{urllib.parse.quote(doi)}?mailto=refaudit@example.org"
    req = urllib.request.Request(url, headers={'User-Agent': 'RefAudit/1.0 (mailto:refaudit@example.org)'})
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.load(r)

results = {}
missing_doi = []
for num in sorted(REFS, key=int):
    doi = extract_doi(REFS[num])
    if not doi:
        missing_doi.append(num)
        results[num] = {"doi": None, "status": "NO_DOI"}
        continue
    try:
        j = fetch(doi)
        m = j.get('message', {})
        authors = []
        for a in m.get('author', [])[:12]:
            if 'name' in a:
                authors.append({"fam": a.get('name', ''), "giv": '', "org": True})
            else:
                authors.append({"fam": a.get('family', ''), "giv": a.get('given', ''), "org": False})
        results[num] = {
            "doi": doi, "status": "OK",
            "title": (m.get('title') or [''])[0],
            "container": (m.get('container-title') or [''])[0],
            "short_container": (m.get('short-container-title') or [''])[0],
            "year": (m.get('published-print') or m.get('published-online') or m.get('issued') or {}).get('date-parts', [[None]])[0][0],
            "volume": m.get('volume'),
            "issue": m.get('issue'),
            "page": m.get('page'),
            "article_number": m.get('article-number'),
            "authors": authors,
            "n_author": len(m.get('author', [])),
            "type": m.get('type'),
        }
        print(f"[OK] ref{num} {doi} -> {results[num]['container'][:45]} | {results[num]['year']} | {results[num]['volume']}:{results[num]['page']}")
    except urllib.error.HTTPError as e:
        results[num] = {"doi": doi, "status": f"HTTP_{e.code}"}
        print(f"[{e.code}] ref{num} {doi}")
    except Exception as e:
        results[num] = {"doi": doi, "status": f"ERR_{type(e).__name__}"}
        print(f"[ERR] ref{num} {doi}: {e}")
    time.sleep(0.2)

json.dump(results, open(OUT, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print("\nmissing DOI refs:", missing_doi)
ok = sum(1 for v in results.values() if v.get('status') == 'OK')
print(f"OK {ok}/{len(results)}; failures:", [k for k, v in results.items() if v.get('status') != 'OK'])