# Reference audit against Crossref — 2026-11-02

Scope: the 42 entries in `## References` of `manuscript_Frontiers_Methods_v2_humanized.md`,
the source of the submission `.docx`.

Method: every entry is resolved by its DOI through `api.crossref.org/works/{doi}` and
compared field by field — first author, year, title (with subtitle concatenated, since
Crossref stores the two separately), journal, volume, issue, pages. Journal names are
compared by token alignment so that an abbreviated name (`Circ. Genom. Precis. Med.`)
can be checked against a full one (`Circulation: Genomic and Precision Medicine`)
rather than by substring. Page ranges are expanded from the NLM compressed form
(`512–25` → `512–525`) before comparison, and a first page alone in Crossref is
accepted when it matches the start of the range in the entry. Entries whose DOI
returns nothing fall back to a bibliographic query so a candidate DOI can be suggested
instead of the entry being dropped from the audit.

Where Crossref and the entry disagreed, `Europe PMC` was consulted as a second source,
because some publishers deposit only the advance-access record: no volume, no issue, an
article identifier where the page range belongs, and the year of online posting rather
than of the issue.

Reproduce: `python code/verify_refs_frontiers.py`. The script caches every response in
`results/refs/crossref_cache.json` and can re-run offline against that cache. It exits
non-zero if any entry contradicts its DOI, so it can serve as a submission gate.

## Result

| Outcome | n |
|---|---|
| Resolved and consistent on every compared field | 40 |
| Discrepancy, resolved in the entry's favour by the second source | 1 |
| Book, no version-of-record DOI | 1 |
| Contradicted by its DOI | 0 |
| DOI did not resolve | 0 |

Structural checks on the same run:

- duplicate DOIs: none
- alphabetical order: intact (42/42 in order by first surname)
- 46 author–year citation pairs in the body and tables, every one resolving to an entry
- entries never cited: none
- citations with no entry: none

## The two findings, and what was done

**1. Popper (1959) carried a DOI belonging to a different edition — corrected.**

The entry read

> Popper, K. (1959). The Logic of Scientific Discovery. London: Hutchinson.
> doi: 10.4324/9780203994627

That DOI resolves to *The Logic of Scientific Discovery*, Routledge, published
2005-11-04 — the Routledge Classics reprint, not the 1959 Hutchinson first edition.
Keeping it would have been two defects at once: a citation whose DOI does not
identify the cited object, and a 1959 imprint attached to a 2005 record, which is
exactly what a copy-editor checks first.

The DOI was removed and the imprint left as it was. A 1959 book has no
version-of-record DOI, and citing the 1959 edition is right on the merits: the
sentence in the Introduction invokes the falsification doctrine as originally stated.
A bibliographic query suggests `10.2307/2550489`, which is a *review* of the book, not
the book — deliberately not used.

**2. Lawlor et al. (2016) looked wrong and is right — no change made.**

Crossref returns for `10.1093/ije/dyw314`: no volume, no issue, `page: dyw314`, and
`published-online: 2017-01-20`. On those fields alone the entry
(`Int. J. Epidemiol. 45(6), 1866–1886`, year 2016) fails on year, volume and pages
simultaneously.

Europe PMC returns for the same DOI: `pubYear 2016`, volume 45, issue 6,
`pageInfo 1866-1886`. The Crossref record is the advance-access deposit and was never
updated with the issue. The entry is correct as it stands; the script now reports this
as a resolved warning rather than an error, and says which source it followed.

This is worth recording because it is the failure mode of any single-source reference
check: a correct citation can be flagged by stale registry metadata, and "fixing" it
would have introduced the error.

## Two things this audit does not establish

- **That the cited papers say what the sentence claims.** DOI resolution verifies
  identity, not content. The citation–content match was checked separately when each
  claim was written and is outside what an API can answer.
- **That the reference list matches the journal's house style.** Frontiers wants a
  specific author-list truncation, journal abbreviation set and punctuation; this audit
  confirms the bibliographic data is true, not that the formatting is theirs.
