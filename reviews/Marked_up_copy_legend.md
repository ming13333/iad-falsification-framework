# Marked-up copy — reading guide

**File** `课题设计阶段/manuscript_Frontiers_Methods_v2_marked.docx` — regenerated 2026-10-31 19:44, after all 17 audit items in `reviews/ACTION_ITEMS_2026-10-30.md` were applied (16 from the first three reports, 1 from the fourth)
**Baseline** `课题设计阶段/manuscript Frontiers 0902.docx` — the version received by Frontiers on 02 Sep 2026
**Prepared** 2026-10-28; **regenerated** 2026-10-31
**Manuscript** 1986036, *Frontiers in Genetics* (Computational Genomics / Methods)

---

## 1. What the colours mean

| Colour | Meaning | How it was produced |
|---|---|---|
| **Yellow** | Text that differs from the submitted version | Word- or sentence-level diff against the baseline; unchanged words inside an edited paragraph stay unmarked |
| **Bright green** | A paragraph that is new, or rewritten too heavily for a word diff to be meaningful | Paragraph similarity below 0.55, or no counterpart in the baseline |
| No colour | Unchanged from the submitted version | Byte-identical after normalisation |

Two rules kept the marking honest rather than merely colourful:

- A paragraph re-ordered by more than a few words is marked at **sentence** level, because a word-level diff on re-ordered prose scatters marks across half the sentence and reads as noise.
- A paragraph that the revision merely **split out of a longer submitted paragraph** (the Methods step list, the operational-challenges list) marks only the list number that was added — the prose itself is unchanged.

Nothing was deleted from the submitted text: every submitted paragraph is still present, either intact or in edited form. The companion file `..._marked_deletions.md` records this explicitly.

---

## 2. Extent of the revision

| | Count |
|---|---|
| Body paragraphs in the revision | 162 |
| Body paragraphs carrying a mark | **71** |
| — word-level edits | 23 |
| — sentence-level edits | 18 (includes the title) |
| — rewritten paragraphs | 12 |
| — list items split out of a merged paragraph | 11 |
| — new paragraphs | 7 |

The five rows above sum to 71 by change type; `mark_changes.py` prints the same set as the coarser split "52 word-level / 19 whole" (52 = 23 + 18 + 11; 19 = 12 + 7). Both describe the same marks at different granularity.
| Table cells carrying a mark | **56** (Table 1: 29, Table 2: 26, Table 4: 1) |
| Tables unchanged | Table 3, Table 5 |
| Characters highlighted, body text | yellow 22.3%, green 33.8% |

Both percentages are recomputed on each regeneration; the denominator is the body paragraphs only, excluding table cells (counting table cells gives yellow 23.4%, green 31.7%, because table cells carry marks too and are a larger share of the whole). The earlier figures in this file (20.7% / 31.2%) could not be reproduced from any build and have been replaced.

Word count went from 6,845 (submitted) to 11,235 (revision, body paragraphs), so roughly a third of the document is genuinely new prose. That is why the green proportion is high: this is a major revision, not a set of local corrections.

---

## 3. Where the changes concentrate

| Section | What changed |
|---|---|
| Title | `correcting` → `diagnosing`; `43,200-simulation validation` → `a 43,200-replicate benchmark of its scoring rule` (D3, see §6) |
| Archive DOI | `10.5281/zenodo.21858125` → `10.5281/zenodo.23733172` in all six places the manuscript cites the deposit (v1.2.1) |
| Abstract | Claim narrowed to the scoring rule; sensitivity 0.97 → 0.88, FDR 0.08 → 0.10 |
| Introduction | New **Terminology** paragraph defining causal claim / association / directed effect |
| Methods — gates | New **What each correction operates on** paragraph; G4 rewritten; **Trans-ethnic re-clumping** added |
| Methods — protocol | Six steps renumbered and split; new **What LD correction changes: precision, not only direction** |
| Methods — simulation | Data-generating process stated as implemented (independent instruments; G3 as block coverage, G4 as leave-one-out; LDSC, colocalization, MVMR, CAUSE and MRlap not instantiated) |
| Results | Table 2 recomputed with the decisive-failure cap applied; G2 and G3 narrative updated; **Insufficient evidence versus evidence against** added |
| Discussion | New paragraph on drug-target prioritisation; complementarity with STROBE-MR rewritten |
| Limitations | Five boundaries rewritten, now quantitative (threshold perturbation, FDR dependence on null fraction) |
| Declarations | Use-of-AI statement rewritten to name the models actually used |
| Tables | Table 1 rebuilt as a two-layer specification (4 columns → 6); Table 2 gains the specificity (C/D) column and recomputed values |

### 2.1 Added by the 2026-10-31 regeneration

The 17 audit items changed nine places in the body and one table cell. All are visible as marks in this copy.

| Location | What changed |
|---|---|
| Methods, Gate G2 (§clumping) | Primary threshold declared as `r² < 0.1`, with `r² < 0.001` reported as a stricter tier — the submitted Methods had named the wrong threshold for the results it reported (M0) |
| Methods, steps 3 and the protocol table | Same correction in the procedure text and in Table 4 row 3 (M0) |
| Results, G2 narrative | 54 variants reattributed from `r² < 0.001` to `r² < 0.1` in both the opening sentence and the instrument-count chain; the tighter tier now reports 37 harmonised variants (M1, M2) |
| Results, chromosome-19 exclusion | Conclusion removed; the paragraph now reports only that attenuation is not attributable to chromosome 19 alone and defers to G3 (M3) |
| Results, precision passage | "restores the sampling variance" replaced by the narrower claim that clumping changed both the instrument set and the reported SE (W1) |
| Results, insufficient-evidence passage | "low power attenuates towards zero and cannot reverse the sign" replaced by the resolution claim (W2) |
| Results, trans-ethnic screen | Sign-exemption guarantee removed; the step is now explicitly an underpowered directional screen receiving no points; the 40 → 30 instrument attrition is stated in both the G2 narrative and the G6 result paragraph (W3, D3) |
| Methods, effect grid | The {0, 0.08, 0.15} grid is now described as lying below the 0.226 threshold rather than bracketing it (W4) |
| Discussion, drug targets | "passes all six gates" and "warrant target investment" replaced by the rubric grade and a hypothesis-prioritisation claim (M6) |
| Results, Table 2 narrative | Specificity 0.80 labelled as the D-only convention; Wilson intervals scoped to sensitivity and the two specificity columns, with the reason each of P(Grade A) and FDR is not given an interval now stated (D2, D4, W6) |
| Methods, Gate G4 and Table 2 footnote | "its collapse indicates collinearity rather than weak instruments" replaced by the narrower claim that the collapse identifies conditional weak instruments whose origin is collinearity, not a failure of unconditional instrument relevance (W6) |

The response letter carries the matching counterpart text; both files were re-exported from their Markdown sources at the same time, so the letter and the manuscript cite the same numbers.

---

## 4. Companion files

| File | Contents |
|---|---|
| `课题设计阶段/manuscript_Frontiers_Methods_v2_marked_changes.csv` | One row per marked paragraph or cell: location, change type, highlighted character count, text preview (127 rows: 71 body + 56 cells) |
| `课题设计阶段/manuscript_Frontiers_Methods_v2_marked_deletions.md` | Text present in the submission but absent from the revision (currently none) |
| `课题设计阶段/manuscript_Frontiers_Methods_v2.docx` | Clean copy, same text, no marks — this is the file to upload as the main manuscript |
| `code/mark_changes.py` | Regenerates the marked copy from the clean one and the baseline |

> An earlier generation wrote the CSV and deletions file into `reviews/`. Those stale copies were removed on 2026-10-31 so that only one pair exists — two files with the same name and different numbers is how the wrong one gets shipped.

### Which manuscript file is the manuscript

Four files in `课题设计阶段/` carry nearly the same name. Only one of them is the manuscript.

| File | Role |
|---|---|
| `manuscript_Frontiers_Methods_v2_humanized.md` | **Source of record.** 12,258 words; the file the submission `.docx` is rendered from |
| `manuscript_Frontiers_Methods_v2.docx` | **The file to upload.** 162 paragraphs / 5 tables / 11,162 words, rendered from the line above |
| `manuscript_Frontiers_Methods_v2.md` | Internal draft (`**Status:** v2 draft for internal review` in its header), 7,305 words, no author block, predates the revision edits. Not for submission |
| `manuscript_Frontiers_Methods_v2_humanized_SUPERSEDED_20260902.docx` | Intermediate export done before the 02 Sep submission (6,794 words, old title). Renamed on 2026-10-31 because its name was one substring away from the live file |

`manuscript Frontiers 0902.docx` is the version Frontiers received and is used **only** as this diff's baseline.

Regenerate after any further edit to the manuscript:

```bash
python code/mark_changes.py \
  --baseline "课题设计阶段/manuscript Frontiers 0902.docx" \
  --target   "课题设计阶段/manuscript_Frontiers_Methods_v2.docx" \
  --out      "课题设计阶段/manuscript_Frontiers_Methods_v2_marked.docx" \
  --csv      "课题设计阶段/manuscript_Frontiers_Methods_v2_marked_changes.csv" \
  --deletions "课题设计阶段/manuscript_Frontiers_Methods_v2_marked_deletions.md"
```

If the output file is open in a viewer, the save fails with `PermissionError`. Close the preview and rerun; do not write to a second filename, because two marked copies differing only in suffix is how the wrong file gets uploaded.

---

## 5. Before submitting

- Upload the **clean** file as the manuscript and the **marked** file as the supplementary "marked-up copy", if the journal asks for one. Frontiers does not require tracked changes; the marked copy is for the reviewers' convenience.
- The highlighted copy is generated from the clean file, so the two can never diverge in wording — only in colour.
- If the reviewers ask for a Word document with **tracked changes** (revision marks that can be accepted or rejected), this file is not that: it shows where the text changed, not an accept/reject record. Producing genuine tracked changes would require rebuilding the document through Word's revision engine, which this environment cannot run.

---

## 6. Title change (D3)

| | Text |
|---|---|
| Submitted | A six-gate falsification framework for **correcting** locus-driven confounding in Mendelian randomization: architecture, **43,200-simulation validation**, and application to complex traits |
| Revision | A six-gate falsification framework for **diagnosing** locus-driven confounding in Mendelian randomization: architecture, **a 43,200-replicate benchmark of its scoring rule**, and application to complex traits |

Two clauses were at fault, for different reasons.

1. **`43,200-simulation validation` → `a 43,200-replicate benchmark of its scoring rule`.** In the benchmark G3 is determined by G1 and G4 is 99.1% concordant with G2, so what was evaluated is the mapping from four gate signals onto the 0–12 scale, through proxy implementations. No genomic estimator was validated. The word "validation" asserted more than the experiment delivers.
2. **`correcting` → `diagnosing`.** The framework does not adjust, stratify or remove locus-driven confounding; it detects the pattern and regrades the claim it produced. "Correcting" invited the reading that the pipeline returns a bias-corrected estimate, which it does not.

The short form used in correspondence and figure legends — "a six-gate falsification framework for locus-driven confounding" — is unaffected, because it carries neither claim. The response letter (R1-2) now reports both changes as made in this revision rather than deferred, so the letter and the manuscript agree on the title actually submitted.
