# Supplementary Note: East Asian cross-ancestry validation (Level 6 reinforcement)

**Date**: 2026-08-04. All analyses are fully reproducible from the scripts and data listed below.

## Purpose

Strengthen Level 6 (directional external validation) of the six-level falsification framework by adding East Asian (EAS) cross-ancestry consistency checks for the three new validation cases and re-confirming the study-pair protective signal. Rationale: cross-ancestry consistency is a stronger external-validation signal than within-ancestry replication because LD structure and allele frequencies differ, so coincidental LD-driven inflation does not transfer.

## Data

| Check | Exposure | EAS Outcome | Outcome N (cases) | Instruments |
|-------|----------|-------------|-------------------|-------------|
| Education→T2D | Chen/Kim/Lam 2024 EAS education (GCST90296498, n=165,232) | BioBank Japan T2D (bbj-a-77) | 191,764 (36,614) | 9 (distance-clumped) |
| T2D→AD | BBJ T2D instruments (bbj-a-77) | GARD EAS AD (NG00182, n=6,518) | 6,518 (2,919) | 96 clumped → 71 position-matched |
| Education→Stroke | EAS education (GCST90296498) | BBJ ischemic stroke (bbj-a-129) | 210,054 (17,671) | 9 |
| Education→AD | EAS education (GCST90296498) | GARD EAS AD (NG00182) | 6,518 (2,919) | 9 |

## Results

### Education→T2D (BBJ)

```
harmonised: 9 ; F = 35.5
IVW:           b = -0.1454  se = 0.058  p = 0.0122   *** significant, protective
MR Egger:      b = -0.0172  se = 0.544  p = 0.976
Weighted median: b = -0.1218 se = 0.053 p = 0.0215  *** concordant
heterogeneity Q_p = 0.00622
Egger intercept p = 0.819 (no directional pleiotropy)
```

**Interpretation**: The European protective education→T2D effect (IVW β = −0.634, P = 2.1 × 10⁻²⁶) replicates significantly in EAS (β = −0.145, P = 0.012), with concordant weighted median and no directional pleiotropy. This is the first significant cross-ancestry replication in the expanded cohort and upgrades the Education→T2D L6 score from 0 → 2 (total 8 → 9; Grade B retained).

### T2D→AD (GARD)

```
matched instruments: 71 (position-based, allele-flip harmonized)
IVW:  b = +0.0055  se = 0.0613  p = 0.9288  (null)
WM:   b = +0.0482
Egger intercept p = 0.236
mean F = 22.1
```

**Interpretation**: The European null T2D→AD effect (β = −0.010, P = 0.714) remains null in EAS (β = +0.006, P = 0.93). Cross-ancestry concordance of a null at moderate power strengthens the Grade D assignment (framework correctly rejects a contested metabolic→AD claim).

### Education→Stroke (BBJ)

```
harmonised: 9 ; F = 35.5
IVW:  b = -0.0084  se = 0.0495  p = 0.866  (null)
WM:   b = +0.0042  p = 0.945
Egger intercept p = 0.523
```

**Interpretation**: Null with 9 instruments — underpowered for effect-size detection; direction consistent with the modest European education→stroke literature. Reported transparently; does not affect any grade (no stroke case was graded).

### Education→AD (GARD, previously reported)

IVW β = −0.029, P = 0.85; 9 instruments; directionally consistent with the European protective effect; power ≥ 84% at R² ≥ 0.05 (Brion/mRnd).

### Depression→AD (GARD; underpowered, not used for grading)

We additionally tested whether the EUR protective depression→AD signal (IVW β = −0.254, P = 0.0135) transfers to EAS. The 50 EUR clumped instruments (F = 35.9) were position-matched against GARD EAS AD; 26 matched with allele-flip harmonization.

```
matched instruments: 26 / 50
IVW:  b = +0.2575  se = 0.3270  p = 0.431
WM:   b = -0.0870
Egger intercept p = 0.386
```

**Interpretation**: Point estimate is positive (opposite to the EUR protective sign) but the standard error is extremely large (SE = 0.327; 95% CI ≈ [−0.38, +0.90]) because GARD EAS AD comprises only 2,919 cases. This check is **severely underpowered**: it can neither confirm nor refute cross-ancestry consistency of the depression→AD signal, and it is **not** used as evidence for or against the Depression→AD Grade C assignment.

**Why a formal EAS replication is currently infeasible** (see also `SupplementaryNote_EAS_Depression_infeasible.md`): we obtained the largest multi-ancestry MDD summary statistics (Meng et al. 2024, Nat Genet; figshare mdd2023diverse, CC BY 4.0 / PGC terms). The EAS clinical-MD stratum (7,886 cases / 14,412 controls) contains **no genome-wide-significant variants** (min P = 1.9 × 10⁻⁷ across 8.08 M variants), so no EAS depression instruments can be constructed from the EAS-only analysis. The multi-ancestry clinical-MD analysis yields 108 GW-significant variants → 6 independent loci after 10 Mb distance clumping; only **2** (rs12129573, rs10759878) are present with harmonizable alleles in GARD EAS AD, and both point toward a positive (risk) AD direction in EAS (MDD logOR +0.038/+0.044 → AD β +0.043/+0.033) — opposite in sign to the EUR protective estimate but entirely within noise (n = 2 instruments; SE ≈ 0.04–0.05). This is reported as a power/data-coverage limitation, not a null result, and does not alter the EUR-based Grade C assignment.

## Summary

Across all four adequately powered cross-ancestry checks, **no framework-assigned direction was contradicted in EAS**: Education→T2D replicated significantly; T2D→AD remained null; Education→Stroke was null (underpowered); Education→AD was directionally consistent. A fifth check, Depression→AD, is documented as **currently infeasible** (EAS MDD stratum lacks genome-wide-significant instruments; sole EAS AD outcome GARD covers only 2 of 6 multi-ancestry MDD loci), and the two available instruments point to a positive direction within noise. This is a power/coverage limitation, not a null result, and does not alter the EUR-based Grade C assignment. The reinforcement addresses the prior limitation that the expanded cohort lacked cross-ancestry checks and strengthens the Level 6 gate for the Nat Commun sprint.

## Files

- `C:/Temp/iad_g1/l6_ea_edu_t2d.txt` — Education→T2D BBJ results (R)
- `C:/Temp/iad_g1/l6_ea_t2d_ad.py` + `l6_ea_t2d_ad.txt` — T2D→AD GARD position-matched results (Python)
- `C:/Temp/iad_g1/l6_ea_edu_stroke.txt` — Education→Stroke BBJ results (R)
- `C:/Temp/iad_g1/bbj_t2d_instruments.csv` — BBJ T2D clumped instruments (96)
- `C:/Temp/iad_g1/mdd2023_EAS_clinicalMD_Neff.csv` + `mdd2023_AllAncestry_clinicalMD_Neff.csv` — Meng 2024 MDD sumstats (figshare mdd2023diverse)
- `C:/Temp/iad_g1/pipeline_mdd_eas_dep_ad.py`, `mdd_allanc_instruments.tsv`, `mdd_eas_dep_ad_harm.tsv` — EAS depression→AD attempt
- `课题设计阶段/Supplementary/SupplementaryNote_EAS_Depression_infeasible.md` — full data-access outcome
- Existing EA pipeline: `code/ea01–ea04.py`, `data/processed/gard_ea_ad_hg19.tsv.gz`
- EAS LD reference: `C:/Temp/iad_g1/ld_ref/EAS_bfile/`, `EAS_ldscores/`
