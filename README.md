# A Five-Layer Causal Verification Framework for Genetic Comorbidity: Recalibrating Insomnia–Alzheimer's Disease

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.XXXXXXX.svg)](https://doi.org/10.5281/zenodo.XXXXXXX)

## Overview

This repository contains the complete analysis pipeline for the paper **"A five-layer causal verification framework for genetic comorbidity: recalibrating insomnia–Alzheimer's disease from a presumed causal upstream to APOE-locus-specific shared liability with cross-ancestry educational protection."**

We propose and validate a **five-layer framework** for genetic comorbidity verification, using insomnia–AD as a proof-of-concept:
1. **Phenomenological**: Bidirectional MR with LD-clump sensitivity
2. **Genome-wide**: LDSC genetic correlation ± chromosome-19/APOE removal
3. **Locus-level**: Colocalization (forward + reverse)
4. **Mechanistic**: Two-step protein- and metabolite-mediation MR
5. **Protective-factor**: MVMR + educational-attainment PheWAS + East Asian replication

## Key Findings

- Unclumped insomnia→AD MR (+0.10, p=0.0009) was a **false positive** — reversed to null after LD-clumping
- Genome-wide genetic correlation rg≈0; shared signal confined to **APOE locus only**
- Educational attainment is a cross-ancestry protective factor for AD and PD (but not MS)
- **No plasma protein mediates education→AD** (36-targeted screen, FDR=0; UKB-PPP verification confirms null)
- Triglycerides are a genetically proxied mediator of education's AD protection (indirect=−0.031, q=0.0006)
- Insomnia–AD classified as **quadrant III (shared liability, no independent causal upstream)**

## Repository Structure

```
├── README.md                          # This file
├── CITATION.cff                       # Citation metadata for Zenodo/GitHub
├── renv.lock                          # R package version lockfile
├── code/
│   ├── 00_config.R                    # Global configuration & paths
│   ├── 01_bidirectional_mr_coloc.R    # Layer 1+3: Bidirectional MR + coloc
│   ├── 01b_overlap_correction.R       # MRlap sample overlap correction
│   ├── 01c_cause_patched.R            # CAUSE correlated pleiotropy
│   ├── 01d_g1_wrapup.R                # Layer 1+3 synthesis
│   ├── 02_g2_open_gwas.R             # G2 insomnia→protein→AD mediation
│   ├── 02b_g2_enhanced.R             # G2 enhanced protein screen
│   ├── 02e_g2b_curated.R             # G2b education→protein→AD curated (36-protein)
│   ├── 04_mvmr.R                      # Layer 5: MVMR
│   ├── 06_ldsc_genetic_correlation.R  # Layer 2: LDSC rg
│   ├── 07_education_phewas_mr.R       # Layer 5: Education PheWAS
│   ├── 08h_steiger_py.py             # Steiger directionality (Python fallback)
│   ├── 09b_metabolite_mediation_slim.R # C1: Metabolite mediation
│   ├── 10b_power_calc_eas.R           # East Asian replication power calc
│   ├── g2b_fdr.py                     # G2b FDR correction
│   ├── make_g2b_curated_fig.py        # Fig3C generation
│   ├── recompute_g2b_bootci.py        # Bootstrap CI recomputation
│   ├── extract_ukbppp_pqtl.py         # UKB-PPP pQTL extraction from Nature supp tables
│   ├── make_figures.py                # Fig1/2/5 generation
│   ├── r_analysis/                    # Standardised R analysis scripts
│   └── README.md                      # Code documentation
├── 课题设计阶段/
│   ├── Phase1_comprehensive_results.md        # Complete results summary
│   ├── Phase2A_abstract_discussion_rewrite.md # Manuscript draft
│   ├── G1_conclusion_revision_2026-08-01.md   # Central argument revision
│   ├── Supplementary/                          # S1-S4 supplementary tables
│   └── figures/                                # Supplementary figures
└── data/
    └── raw/                           # Cached GWAS harmonised inputs
```

## Data Sources

| Data | Source | Accession |
|------|--------|-----------|
| Insomnia GWAS | UK Biobank / IEU OpenGWAS | `ukb-b-3957` |
| AD GWAS (Kunkle) | IGAP / IEU OpenGWAS | `ieu-b-2` |
| AD GWAS (Bellenguez) | IEU OpenGWAS | `ebi-a-GCST90027158` |
| Educational attainment | Lee 2018 / IEU OpenGWAS | `ieu-a-1239` |
| EA education (EAS) | Chen/Kim/Lam 2024 / GWAS Catalog | `GCST90296498` |
| EA AD (EAS) | GARD/NIAGADS | `NG00182` |
| INTERVAL plasma proteins | IEU OpenGWAS | `prot-a-1..2200` |
| Metabolites | IEU OpenGWAS | `met-d-*` |
| UKB-PPP pQTL | Sun et al. 2023, *Nature* | Supp Tables 9–10; Synapse `syn51364943` |

## Software Dependencies

- **R 4.5.2** — main analysis environment (`TwoSampleMR`, `ieugwasr`, `MendelianRandomization`, `GenomicSEM`, `cause`, `coloc`)
- **Python 3.13** — Steiger directionality fallback, figures, UKB-PPP extraction (`numpy`, `pandas`, `matplotlib`, `openpyxl`)
- **LDSC** — LD score regression (standalone)
- R package versions locked in `renv.lock`
- Known ABI issue: R 4.5.2 running packages compiled for R 4.5.3 may cause transient SIGSEGV; Python pyreadr path available as fallback

## Reproducibility

- All random number generation uses `set.seed()` (R) or `np.random.default_rng(42)` (Python)
- IEU OpenGWAS API calls are deterministic given the same server state; key API outputs are cached in `data/raw/c1_cache/`
- Bootstrap CI for G2b was cross-computed in Python/numpy after R quantile write failure; both converge to the same asymptotic distribution
- GWAS summary statistics from public repositories (IEU OpenGWAS, GWAS Catalog, NIAGADS, Nature supplementary tables)

## Citation

If you use this code or data, please cite:

```bibtex
@article{insomniaAD2025,
  title={A five-layer causal verification framework for genetic comorbidity: 
         recalibrating insomnia–Alzheimer's disease from a presumed causal 
         upstream to APOE-locus-specific shared liability},
  author={[Authors]},
  journal={[Journal]},
  year={2026},
  doi={[DOI]}
}
```

See `CITATION.cff` for complete metadata.

## License

This project is licensed under the MIT License — see [LICENSE](LICENSE) file for details.

## Contact

[Author contact information]
