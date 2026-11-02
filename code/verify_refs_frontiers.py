#!/usr/bin/env python3
"""Field-level verification of the manuscript's reference list against Crossref.

Reads the References section of the manuscript markdown, resolves each entry by
DOI through api.crossref.org, and compares what the entry claims with what the
DOI actually points at: first author, year, title, journal, volume, issue, pages.

Anything the DOI cannot corroborate is reported, not silently accepted.  Two
classes of finding are kept apart:

  ERROR   the entry contradicts the DOI: wrong year, wrong volume, a title that
          is a different paper, an author who is not on the paper.  These must
          be fixed before submission.
  WARN    the entry is compatible but under-specified or differently formatted:
          abbreviated journal name, missing issue, page range given as an article
          number.  Worth a look, not necessarily wrong.

Entries with no DOI get a bibliographic query so a candidate DOI can be
suggested rather than the entry being dropped from the audit.

Usage:
    python code/verify_refs_frontiers.py
    python code/verify_refs_frontiers.py --offline      # reuse the cache only
    python code/verify_refs_frontiers.py --json out.json
"""

import argparse
import difflib
import json
import os
import re
import sys
import time
import unicodedata
import urllib.error
import urllib.parse
import urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
MD = os.path.join(ROOT, "课题设计阶段", "manuscript_Frontiers_Methods_v2_humanized.md")
CACHE = os.path.join(ROOT, "results", "refs", "crossref_cache.json")
MAILTO = "lm962272@gmail.com"
STOP = {"a", "an", "the", "of", "and", "in", "for", "on", "to", "de", "la", "der", "und"}


# ---------------------------------------------------------------- parsing

def load_references(path=MD):
    text = open(path, encoding="utf-8").read()
    i = text.index("## References")
    tail = text[i + len("## References"):]
    m = re.search(r"^## ", tail, re.M)
    block = tail[: m.start()] if m else tail
    entries = []
    for line in block.split("\n"):
        line = line.strip()
        if not line:
            continue
        entries.append(line)
    return entries


def split_authors_year(entry):
    """Return (author_string, year) from 'Surname, A. B., ... (2019). ...'."""
    m = re.search(r"\((\d{4}[a-z]?)\)", entry)
    year = m.group(1) if m else None
    authors = entry[: m.start()] if m else entry
    return authors.rstrip(" ."), year


def first_surname(entry):
    """The surname the entry sorts under and leads with."""
    stop = re.search(r"\((\d{4}[a-z]?)\)", entry)
    head = entry[: stop.start()] if stop else entry
    # 'Davey Smith, G.' and 'van der Berg, J.' keep their particles
    m = re.match(r"([A-Z][^,]*(?:,\s*[A-Z][^,]*\.)?)", head)
    if not m:
        return head.split(",")[0].strip()
    chunk = m.group(1)
    if ", " in chunk:
        surname = chunk.split(", ")[0]
    else:
        surname = chunk
    return surname.strip()


def extract_doi(entry):
    m = re.search(r"doi:\s*([^\s]+)", entry, re.I)
    if m:
        return m.group(1).rstrip(".,;)")
    m = re.search(r"doi\.org/(\S+)", entry, re.I)
    return m.group(1).rstrip(".,;)") if m else None


def extract_title(entry):
    m = re.search(r"\((\d{4}[a-z]?)\)\.\s*(.+?)\.\s", entry)
    if m:
        return m.group(2).strip()
    return ""


def extract_journal_volume_pages(entry):
    """Pull journal, volume, issue, pages out of the tail of the entry."""
    body = entry
    doi = extract_doi(entry)
    if doi:
        body = body[: body.lower().rfind("doi:")]
    # Volume/issue/pages are anchored at the end, which is unambiguous.  The
    # journal name is then whatever precedes them - matching it forward from the
    # left does not work, because abbreviated names carry internal periods
    # ('Circ. Genom. Precis. Med.') and the title on its own has none, so a
    # leftward match happily swallows the whole title.
    m = re.search(r"(\d+)(?:\((\d+[A-Za-z\-]*)\))?\s*[,:]\s*([^.]*)\.?\s*$", body)
    if m:
        prefix = body[: m.start()].rstrip()
        # 'Circ. Genom. Precis. Med.' ends in a period that belongs to the
        # abbreviation, so keep it; drop the separating one only
        journal = prefix[:-1] if prefix.endswith(".") else prefix
        return {
            "journal": journal.strip(),
            "volume": m.group(1),
            "issue": m.group(2),
            "pages": m.group(3).strip().rstrip("."),
        }
    m = re.search(r"\.\s+([A-Z][^.]*?)\.\s*$", body)
    if m:
        return {"journal": m.group(1).strip(), "volume": None, "issue": None, "pages": None}
    return {"journal": None, "volume": None, "issue": None, "pages": None}


# ---------------------------------------------------------------- matching

def norm(s):
    s = unicodedata.normalize("NFKD", s or "")
    s = "".join(c for c in s if not unicodedata.combining(c))
    s = s.replace("\u2013", "-").replace("\u2014", "-").replace("\u2019", "'")
    s = re.sub(r"[^a-z0-9 ]+", " ", s.lower())
    return re.sub(r"\s+", " ", s).strip()


def title_sim(a, b):
    return difflib.SequenceMatcher(None, norm(a), norm(b), autojunk=False).ratio()


def abbrev_matches(short, full):
    """'Circ. Genom. Precis. Med.' against 'Circulation: Genomic and Precision Medicine'.

    Token alignment rather than string comparison: each abbreviated word must be a
    mutual prefix of a word in the full title, in order.  Words the abbreviation
    omits ('and', 'of', 'the') are skipped, which is why 'Nat. Genet.' has to be
    compared as two tokens and not as a substring.
    """
    if not short or not full:
        return None
    tf = [t for t in norm(full).split() if t and t not in STOP and len(t) > 1]
    te = [t for t in norm(short).split() if t and t not in STOP and len(t) > 1]
    if not tf or not te:
        return None
    # Align from the right.  The journal name sits immediately before the volume,
    # so the last tokens of the fragment are the ones that must line up, and
    # aligning backwards means the internal periods of an abbreviation never have
    # to be parsed - they are just token separators.
    i, j, hit = len(te) - 1, len(tf) - 1, 0
    while i >= 0 and j >= 0:
        if tf[j].startswith(te[i]) or te[i].startswith(tf[j]):
            hit += 1
            i -= 1
            j -= 1
        else:
            j -= 1
    required = 1 if len(tf) == 1 else max(2, len(tf) - 1)
    return hit >= required


def expand_pages(p):
    """'512-25' is '512-525' written the NLM way; expand before comparing."""
    # norm() would collapse the dash to a space, so normalise dashes only here
    p = (p or "").replace("\u2013", "-").replace("\u2014", "-").replace(" ", "").lower()
    m = re.match(r"^(\d+)-(\d+)$", p)
    if m:
        a, b = m.group(1), m.group(2)
        if len(b) < len(a):
            b = a[: len(a) - len(b)] + b
        return a + "-" + b
    return p


def pages_match(entry_pages, cr_pages):
    a, b = expand_pages(entry_pages), expand_pages(cr_pages)
    if a == b:
        return True
    # Crossref sometimes carries only the first page of a range
    if "-" not in b and a.split("-")[0] == b:
        return True
    return False


def year_of(msg):
    for key in ("published-print", "published-online", "issued", "created"):
        parts = (msg.get(key) or {}).get("date-parts") or []
        if parts and parts[0] and parts[0][0]:
            return str(parts[0][0])
    return None


def years_of(msg):
    """Every year the record carries, by role.  Online-first papers have two."""
    out = {}
    for key in ("published-print", "published-online", "issued", "created"):
        parts = (msg.get(key) or {}).get("date-parts") or []
        if parts and parts[0] and parts[0][0]:
            out[key] = str(parts[0][0])
    return out


def pages_of(msg):
    return (msg.get("page") or "").strip() or (msg.get("article-number") or "").strip()


# ---------------------------------------------------------------- network

def _get(url, cache, key, offline=False, tries=3):
    if key in cache:
        return cache[key]
    if offline:
        return None
    last = None
    for attempt in range(tries):
        req = urllib.request.Request(
            url, headers={"User-Agent": f"ref-audit/1.0 (mailto:{MAILTO})"}
        )
        try:
            with urllib.request.urlopen(req, timeout=30) as r:
                data = json.load(r)
            cache[key] = data
            time.sleep(0.4)
            return data
        except urllib.error.HTTPError as e:
            if e.code == 404:
                cache[key] = {"__error__": "404 not found"}
                return cache[key]
            last = f"HTTP {e.code}"
        except Exception as e:  # noqa: BLE001 - network is allowed to fail
            last = type(e).__name__
        time.sleep(1.5 * (attempt + 1))
    cache[key] = {"__error__": last or "unreachable"}
    return cache[key]


def by_doi(doi, cache, offline=False):
    url = "https://api.crossref.org/works/" + urllib.parse.quote(doi) + f"?mailto={MAILTO}"
    return _get(url, cache, "doi:" + doi.lower(), offline)


EPMC = "https://www.ebi.ac.uk/europepmc/webservices/rest/search"


def by_europepmc(doi, cache, offline=False):
    """Second opinion for records Crossref has only as advance-access deposits.

    Crossref keeps the version deposited at online-first publication for some
    publishers: 10.1093/ije/dyw314 has no volume, no issue and 'dyw314' where the
    page range belongs, so every field disagrees with a correct citation.  Europe
    PMC carries the version of record.
    """
    url = f"{EPMC}?query=DOI:%22{urllib.parse.quote(doi)}%22&format=json&resultType=core"
    data = _get(url, cache, "epmc:" + doi.lower(), offline)
    if not data:
        return None
    res = (data.get("resultList") or {}).get("result") or []
    if not res:
        return None
    x = res[0]
    ji = x.get("journalInfo") or {}
    return {
        "year": x.get("pubYear"),
        "volume": ji.get("volume"),
        "issue": ji.get("issue"),
        "pages": x.get("pageInfo"),
        "title": x.get("title"),
        "journal": (ji.get("journal") or {}).get("title"),
    }


def by_bibliographic(entry, cache, offline=False):
    q = urllib.parse.quote(entry[:300])
    url = (
        "https://api.crossref.org/works?rows=3&select=DOI,title,author,issued,"
        f"container-title,type&query.bibliographic={q}&mailto={MAILTO}"
    )
    return _get(url, cache, "bib:" + entry[:120], offline)


# ---------------------------------------------------------------- comparison

def compare(n, entry, msg):
    """Return (errors, warns, facts) for one entry against one Crossref record."""
    err, warn = [], []
    authors, year = split_authors_year(entry)
    title = extract_title(entry)
    got = extract_journal_volume_pages(entry)

    cr_title = (msg.get("title") or [""])[0]
    if msg.get("subtitle"):
        cr_title = cr_title.rstrip(": ") + ": " + msg["subtitle"][0]
    cr_year = year_of(msg)
    cr_journal = (msg.get("container-title") or [""])[0]
    cr_vol = str(msg.get("volume") or "")
    cr_issue = str(msg.get("issue") or "")
    cr_pages = pages_of(msg)

    # first author.  Consortia are listed first by Crossref on many GWAS papers
    # (Kunkle, Lambert, Lane, Lee, Patsopoulos all carry a group as author 1), so
    # matching only position 1 reports a false error on every consortium paper.
    cr_authors = msg.get("author") or []
    cr_names = [a.get("family") or a.get("name") or "" for a in cr_authors]
    if cr_names:
        mine = first_surname(entry)
        hits = [i for i, nm in enumerate(cr_names) if norm(mine) and
                (norm(mine) == norm(nm) or norm(mine) in norm(nm) or norm(nm) in norm(mine))]
        if not hits:
            err.append(f"first author: entry '{mine}' absent from DOI authors "
                       f"(DOI leads with '{cr_names[0]}')")
        # a consortium listed first is a byline convention (1000 Genomes, ADGC,
        # 23andMe), not a citation error - only flag a really deep match
        elif hits[0] > 4:
            warn.append(f"author order: entry leads with '{mine}', which is DOI "
                        f"author {hits[0] + 1}")

    # year.  A paper published online in one year and in print the next is
    # legitimately citable as either; report the difference rather than call it
    # wrong, but flag it so a copy-editor does not.
    yl = years_of(msg)
    if year:
        y = year[:4]
        print_years = {yl.get("published-print"), yl.get("issued")}
        online_years = {yl.get("published-online")}
        if y not in print_years and y in online_years:
            warn.append(f"year: entry {year} is the online-first year, print is "
                        f"{yl.get('published-print') or yl.get('issued')}")
        elif y not in print_years | online_years:
            err.append(f"year: entry {year} vs DOI "
                       f"{yl.get('published-print') or yl.get('issued')}")

    # title
    if title and cr_title:
        s = title_sim(title, cr_title)
        if s < 0.80:
            err.append(f"title {s:.2f}: entry '{title[:70]}' vs DOI '{cr_title[:70]}'")
        elif s < 0.93:
            warn.append(f"title {s:.2f} differs in wording: '{title[:60]}' vs '{cr_title[:60]}'")

    # journal
    if got["journal"] and cr_journal:
        ok = abbrev_matches(got["journal"], cr_journal)
        if ok is False:
            err.append(f"journal: entry '{got['journal']}' vs DOI '{cr_journal}'")
        elif ok is None:
            warn.append(f"journal unchecked: '{got['journal']}' vs '{cr_journal}'")

    # volume / issue / pages
    if got["volume"] and cr_vol and got["volume"] != cr_vol:
        err.append(f"volume: entry {got['volume']} vs DOI {cr_vol}")
    if got["issue"] and cr_issue and got["issue"] != cr_issue:
        warn.append(f"issue: entry {got['issue']} vs DOI {cr_issue}")
    if got["pages"] and cr_pages and not pages_match(got["pages"], cr_pages):
        warn.append(f"pages: entry '{got['pages']}' vs DOI '{cr_pages}'")
    if not got["volume"] and cr_vol:
        warn.append(f"volume missing in entry (DOI says {cr_vol})")
    if not got["pages"] and cr_pages:
        warn.append(f"pages missing in entry (DOI says {cr_pages})")

    facts = {
        "crossref_title": cr_title,
        "crossref_year": cr_year,
        "crossref_journal": cr_journal,
        "crossref_volume": cr_vol,
        "crossref_issue": cr_issue,
        "crossref_pages": cr_pages,
        "crossref_type": msg.get("type"),
        "crossref_first_author": (cr_authors[0].get("family") if cr_authors else None),
    }
    return err, warn, facts


NON_NAMES = {"gcst", "doi", "ng", "rs", "pmid", "zenodo", "table", "figure",
             "supplementary", "s", "version", "release", "stage", "step", "gate"}


def check_citations(entries):
    """Author-year citations in the body against the list, both directions.

    A cited name is looked for among *all* authors of entries carrying that year,
    not just the first: 'Burgess and Thompson (2015)' and 'Lawlor, Tilling and
    Davey Smith (2016)' are second- and third-author citations of entries that sort
    under B and L.  Names are matched with Unicode accents intact, since stripping
    them turned Munafo into 'munaf' and produced a phantom missing reference.
    """
    text = open(MD, encoding="utf-8").read()
    # Table 4 lists the data sources and carries citations of its own
    # ('Suhre et al. (2017), KORA'), and it sits after the reference list, so a
    # body-only scan reports every source named only in a table as uncited.
    body = text[text.index("## Introduction"): text.index("## References")]
    if "\n## Tables" in text:
        body += text[text.index("\n## Tables"):]

    by_year = {}
    for e in entries:
        a, y = split_authors_year(e)
        if y:
            by_year.setdefault(y[:4], []).append((a, e))

    pat = re.compile(r"([A-Z][^\W\d_]+(?:[-'][^\W\d_]+)*)\s*(?:et\s+al\.?)?,?\s*\(?((?:19|20)\d{2})")
    cited = set()
    for m in pat.finditer(body):
        name, year = m.group(1), m.group(2)
        if name.lower() in NON_NAMES:
            continue
        cited.add((name, year))
    # Parentheticals hold several citations separated by semicolons, each with
    # its own year: '(Davey Smith and Ebrahim, 2003; Burgess et al., 2013)' is two
    # citations, not four names sharing 2013.
    for m in re.finditer(r"\(([^()]{2,300})\)", body):
        for seg in m.group(1).split(";"):
            y = re.search(r"((?:19|20)\d{2})[a-z]?\s*$", seg.strip())
            if not y:
                continue
            for w in re.findall(r"[A-Z][^\W\d_]+(?:[-'][^\W\d_]+)*", seg):
                if w.lower() not in NON_NAMES:
                    cited.add((w, y.group(1)))

    unlisted = []
    for name, year in sorted(cited):
        key = norm(name)
        pool = by_year.get(year, [])
        if not any(key in norm(a) for a, _ in pool):
            unlisted.append(f"{name} {year}")

    uncited = []
    for e in entries:
        a, y = split_authors_year(e)
        if not y:
            continue
        sn = first_surname(e)
        if norm(sn) not in norm(body):
            uncited.append(f"{sn} {y}")

    return {
        "cited_pairs": len(cited),
        "unlisted": unlisted,
        "uncited": uncited,
    }


def check_duplicates(entries):
    dois = {}
    for n, e in enumerate(entries, 1):
        d = extract_doi(e)
        if d:
            dois.setdefault(d.lower(), []).append(n)
    return {d: v for d, v in dois.items() if len(v) > 1}


def check_order(entries):
    keys = [norm(first_surname(e)) for e in entries]
    out = []
    for k in range(1, len(keys)):
        if keys[k] < keys[k - 1]:
            out.append((k, keys[k - 1], keys[k]))
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--offline", action="store_true")
    ap.add_argument("--json")
    args = ap.parse_args()

    cache = {}
    if os.path.exists(CACHE):
        cache = json.load(open(CACHE, encoding="utf-8"))
    os.makedirs(os.path.dirname(CACHE), exist_ok=True)

    entries = load_references()
    rows = []
    n_err = n_warn = n_ok = n_nodoi = n_unreach = 0

    for n, entry in enumerate(entries, 1):
        doi = extract_doi(entry)
        row = {"n": n, "doi": doi, "entry": entry, "errors": [], "warns": []}
        if not doi:
            n_nodoi += 1
            row["status"] = "NO_DOI"
            q = by_bibliographic(entry, cache, args.offline)
            items = ((q or {}).get("message") or {}).get("items") or []
            if items:
                top = items[0]
                row["suggested_doi"] = top.get("DOI")
                row["suggested_title"] = (top.get("title") or [""])[0]
                row["suggested_year"] = year_of(top)
            rows.append(row)
            continue
        data = by_doi(doi, cache, args.offline)
        if not data or "__error__" in (data or {}):
            n_unreach += 1
            row["status"] = "DOI_NOT_RESOLVED"
            row["note"] = (data or {}).get("__error__", "no data")
            rows.append(row)
            continue
        msg = data.get("message") or {}
        err, warn, facts = compare(n, entry, msg)
        row.update(facts)

        # A Crossref deposit is sometimes the advance-access record only: no
        # volume, no issue, an article id where pages belong, and the year of
        # online posting rather than of the issue.  Before calling the entry
        # wrong, ask the registry that carries the version of record.
        if err or warn:
            ep = by_europepmc(doi, cache, args.offline)
            if ep:
                row["europepmc"] = ep
                got = extract_journal_volume_pages(entry)
                _a, year = split_authors_year(entry)
                keep = []
                for e in err:
                    if e.startswith("year:") and year and ep.get("year") \
                            and year[:4] == str(ep["year"]):
                        row.setdefault("notes", []).append(
                            f"year {year} confirmed by Europe PMC; the Crossref "
                            f"deposit is the online-first record ({facts.get('crossref_year')})")
                        warn.append(f"year: Crossref says {facts.get('crossref_year')}, "
                                    f"Europe PMC says {ep['year']} - entry follows Europe PMC")
                        continue
                    if e.startswith("volume:") and got["volume"] \
                            and str(ep.get("volume")) == got["volume"]:
                        continue
                    keep.append(e)
                err = keep
                # drop page/volume warnings the second source resolves
                warn = [
                    w for w in warn
                    if not (
                        (w.startswith("pages:") and got["pages"] and ep.get("pages")
                         and pages_match(got["pages"], ep["pages"]))
                        or (w.startswith("issue:") and got["issue"]
                            and str(ep.get("issue")) == got["issue"])
                        or w.startswith("volume missing")
                        and got["volume"] and str(ep.get("volume")) == got["volume"]
                    )
                ]

        row["errors"] = err
        row["warns"] = warn
        if err:
            n_err += 1
            row["status"] = "ERROR"
        elif warn:
            n_warn += 1
            row["status"] = "WARN"
        else:
            n_ok += 1
            row["status"] = "OK"
        rows.append(row)

    json.dump(cache, open(CACHE, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    if args.json:
        json.dump(rows, open(args.json, "w", encoding="utf-8"), ensure_ascii=False, indent=1)

    print(f"entries: {len(entries)}   OK {n_ok}   WARN {n_warn}   ERROR {n_err}   "
          f"NO_DOI {n_nodoi}   UNRESOLVED {n_unreach}")
    print()
    for r in rows:
        if r["status"] == "OK":
            continue
        print(f"[{r['status']:16s}] {r['n']:2d}  {r['entry'][:95]}")
        for e in r.get("errors", []):
            print(f"      ERROR  {e}")
        for w in r.get("warns", []):
            print(f"      warn   {w}")
        if r.get("suggested_doi"):
            print(f"      suggest {r['suggested_doi']}  {(r.get('suggested_title') or '')[:70]}")
        if r.get("note"):
            print(f"      note   {r['note']}")
        print()

    dup = check_duplicates(entries)
    print("duplicate DOIs:", "none" if not dup else dup)
    order = check_order(entries)
    print("out-of-order entries:", "none" if not order else order)
    cit = check_citations(entries)
    print(f"citation pairs found in body: {cit['cited_pairs']}")
    print("cited but not listed:", cit["unlisted"] or "none")
    print("listed but never cited:", cit["uncited"] or "none")

    if not args.offline:
        print("cache:", os.path.relpath(CACHE, ROOT), f"({len(cache)} records)")
    return 1 if (n_err or n_unreach) else 0


if __name__ == "__main__":
    sys.exit(main())
