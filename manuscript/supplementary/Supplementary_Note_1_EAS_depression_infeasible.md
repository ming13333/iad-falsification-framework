# Supplementary Note 1: EAS Depression→AD cross-ancestry replication: outcome of data-access attempt

**Date**: 2026-08-05. **Conclusion: infeasible with currently accessible data — reported as a data limitation, not a null result.**

## Why we attempted this

The European depression→AD signal (ieu-b-102 → ieu-b-2; IVW β = −0.254, P = 0.0135, Grade C) is the only
validation case without a cross-ancestry check. An earlier attempt using EUR instruments against GARD EAS AD
(2,919 cases) was severely underpowered. This note documents the attempt to obtain the proper EAS exposure
GWAS (Meng et al. 2024, Nat Genet) and why a formal EAS replication is not currently possible.

## Data acquisition (successful)

- Source: figshare `mdd2023diverse` (doi 10.6084/m9.figshare.24799299, CC BY 4.0; PGC data terms apply)
- Downloaded:
  - `mdd2023_EAS_clinicalMD_Neff.csv` (781 MB) — East Asian clinical MD meta-analysis
    (7,886 cases / 14,412 controls, GRCh37) — file id 43621254
  - `mdd2023_AllAncestry_clinicalMD_Neff.csv` (2.8 GB) — multi-ancestry clinical MD
    (88,316 cases / 902,757 controls, GRCh37) — file id 43621302
- Format: Chromosome,Position,SNP,EA,NEA,EAF,logOR,SE,P,N_study,Direction,HetISq,HetPVal,Ncase,Ncontrol,Neff
- Note: 23andMe, WHI and JHS excluded from all shared sumstats (ReadMe.txt)

## Key empirical findings

1. **EAS clinical MDD has NO genome-wide significant variants** (min P = 1.9 × 10⁻⁷ across 8,079,156 variants).
   With 7,886 cases the EAS stratum is underpowered at genome-wide scale — consistent with Meng et al. 2024
   reporting that MDD loci transfer to non-European ancestries less often than expected.

2. **Multi-ancestry clinical MDD (AllAncestry)** yields 108 GW-significant variants → 6 independent loci after
   distance clumping (10 Mb). Of these, only **2** have positions + harmonizable alleles present in GARD EAS AD
   (2,919 cases): rs12129573 and rs10759878.

3. **Exploratory 2-instrument direction check** (multi-ancestry MDD → GARD EAS AD):
   - rs12129573: MDD logOR = +0.038 → AD β = +0.0425 (SE 0.045)
   - rs10759878: MDD logOR = +0.044 → AD β = +0.033 (SE 0.041)
   - Both instruments point to a **positive (risk) direction** in EAS, opposite to the EUR protective estimate
     (β = −0.254). With n = 2 instruments and SE ≈ 0.04–0.05 this is **not an MR estimate** and must not be
     interpreted as a replication; it is reported only to document direction within noise.

## Conclusion for the manuscript

- A formal EAS depression→AD replication is **not feasible with currently accessible data**:
  the EAS MDD stratum lacks GW-significant instruments, and the only EAS AD outcome (GARD, 2,919 cases) has
  sparse coverage of the multi-ancestry MDD loci.
- This is **not** a negative result; it is a **power/coverage limitation**, reported transparently in the
  Limitations section. The Depression→AD Grade C assignment (based on EUR evidence) is unchanged.
- Future path: a larger EAS AD GWAS (e.g., a forthcoming East Asian AD meta-analysis) and/or the PGC East Asian
  MDD release with more cases would enable this check. This is listed as a limitation, not a blocker.

## Files

- `C:/Temp/iad_g1/mdd2023_EAS_clinicalMD_Neff.csv` (781 MB)
- `C:/Temp/iad_g1/mdd2023_AllAncestry_clinicalMD_Neff.csv` (2.8 GB)
- `C:/Temp/iad_g1/mdd2023_ReadMe.txt`
- `C:/Temp/iad_g1/extract_mdd_eas.py`, `pipeline_mdd_eas_dep_ad.py`, `mr_eas_dep_mdd.py`
- `C:/Temp/iad_g1/mdd_eas_gwsig.tsv`, `mdd_allanc_gwsig.tsv`, `mdd_allanc_instruments.tsv`,
  `mdd_eas_dep_ad_harm.tsv` (2 rows), `l6_ea_dep_mdd.txt`
