# Marked-up copy — reading guide

**File** `课题设计阶段/manuscript_Frontiers_Methods_v2_marked.docx` — regenerated 2026-10-28 20:20 with the revised title (D3)
**Baseline** `课题设计阶段/manuscript Frontiers 0902.docx` — the version received by Frontiers on 02 Sep 2026
**Prepared** 2026-10-28
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
| Body paragraphs in the revision | 157 |
| Body paragraphs carrying a mark | **71** |
| — word-level edits | 25 |
| — sentence-level edits | 16 (includes the title) |
| — rewritten paragraphs | 12 |
| — list items split out of a merged paragraph | 12 |
| — new paragraphs | 6 |
| Table cells carrying a mark | **55** (Table 1: 29, Table 2: 26) |
| Tables unchanged | Table 3, Table 4, Table 5 |
| Characters highlighted, body text | yellow 18.5%, green 32.9% |

Word count went from 6,845 (submitted) to 10,987 (revision, body text), so roughly a third of the document is genuinely new prose. That is why the green proportion is high: this is a major revision, not a set of local corrections.

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

---

## 4. Companion files

| File | Contents |
|---|---|
| `reviews/marked_changes.csv` | One row per marked paragraph or cell: location, change type, highlighted character count, text preview |
| `reviews/marked_deletions.md` | Text present in the submission but absent from the revision (currently none) |
| `课题设计阶段/manuscript_Frontiers_Methods_v2.docx` | Clean copy, same text, no marks — this is the file to upload as the main manuscript |
| `code/mark_changes.py` | Regenerates the marked copy from the clean one and the baseline |

Regenerate after any further edit to the manuscript:

```bash
python code/mark_changes.py \
  --baseline "课题设计阶段/manuscript Frontiers 0902.docx" \
  --target   "课题设计阶段/manuscript_Frontiers_Methods_v2.docx" \
  --out      "课题设计阶段/manuscript_Frontiers_Methods_v2_marked.docx" \
  --csv      "reviews/marked_changes.csv" \
  --deletions "reviews/marked_deletions.md"
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
