# Code Map: Six-Level Falsification Framework

This directory contains the analysis code for the six-level falsification framework. Each module is listed below with its corresponding gate.

## Layout

- `code/r_analysis/` — R modules (25 files). Entry point: `00_config.R`.
- `code/*.py` — Python scripts for East Asian (EAS) replication, simulations, figure generation, and reference audits.
- Cached harmonised inputs for the primary mediation analyses live in `data/raw/c1_cache/` (see `MANIFEST.csv` for provenance).

## Gate → script map

| Script(s) | Purpose |
|-----------|---------|
| `00_config.R` | Global configuration: GWAS IDs, thresholds, LD reference, output dirs |
| `01_bidirectional_mr_coloc.R`, `01b_overlap_correction.R`, `01c_cause_patched.R`, `01d_g1_wrapup.R`, `01e_cause_fwd_ns1000.R`, `01f_cause_clumped.R` | Gate 1/2: bidirectional MR, MRlap overlap correction, CAUSE, LD clumping |
| `02_g2_open_gwas.R`, `02b_g2_enhanced.R`, `02c_g2b_edu.R` | Gate 5 (protein mediation): CRP/IL-6 → AD and education → protein → AD |
| `04_mvmr.R` | Gate 4: multivariable MR (direct effect of insomnia on AD) |
| `05_g1_verify.R` | Gate 1 verification with local harmonised data |
| `06_ldsc_genetic_correlation.R`, `06b_ldsc_diag.R`, `06c_ldsc_final.R` | Gate 3: LD score regression (genome-wide and APOE-excluded) |
| `07_education_phewas_mr.R` | Education PheWAS across AD / PD / MS |
| `08_steiger_eaf.R`, `08c_steiger_final.R` | Gate 5/6: Steiger directionality (R; Python fallback in `08h_steiger_py.py` if R crashes) |
| `09_metabolite_mediation.R`, `09b_metabolite_mediation_slim.R` | Gate 5: metabolite mediation (full and slim versions) |
| `10b_power_calc_eas.R` | EAS power calculations |
| `B1_fetch_opengwas.R`, `B1_fetch_ukbppp.py`, `B1_verify.py` | Data acquisition: IEU OpenGWAS, UKB-PPP pQTL (Synapse), download verification |
| `package_versions.md` | Frozen R package versions used in the analyses |

## Python scripts

- `ea01_liftover_gard.py` / `ea02_instruments.py` / `ea03_harmonize.py` / `ea04_mr.py` / `ea05_transethnic_insomnia_ad.py` — EAS cross-ancestry replication (GRCh38 → GRCh37 liftover, instrument extraction, harmonisation, MR).
- `sim_framework_operating_chars.py` — 43,200-replicate simulation of framework operating characteristics.
- `make_figures.py`, `make_fig3_supp.py`, `make_fig4.py`, `make_g2b_curated_fig.py`, `make_g2b_screen_fig.py`, `make_sim_suppfig.py` — figure generation.
- `g2b_fdr.py`, `recompute_g2b_bootci.py` — FDR correction and bootstrap CIs for protein mediation.
- `extract_ukbppp_pqtl.py` — UKB-PPP pQTL extraction (Synapse syn51364943).
- `audit_ref_placement.py`, `build_references.py`, `classify_refs_enhanced.py`, `verify_refs_crossref.py`, `ref_audit_*.py` — reference auditing utilities.
- `interrater_reliability.py` — inter-rater reliability analysis.
- `md_to_docx_gm.py` — markdown-to-docx conversion helper (local use).

## Environment notes

- **R**: tested with R 4.5.2 (`renv.lock` freezes package versions; run `renv::restore()`).
- **Python**: Python ≥ 3.9 with `numpy`, `pandas`, `scipy`, `matplotlib`, `pyreadr`, `statsmodels`, `synapseclient` (for UKB-PPP fetch only).
- **IEU OpenGWAS API**: the static full-summary-statistics endpoint is deprecated (301 → 404); use `gwasinfo()` for metadata, `extract_instruments` with p ≤ 0.01, and `associations(id, variants=)` chunked by ~64 variants. Cached harmonised inputs (`data/raw/c1_cache/`) allow offline re-running of the primary mediation analyses without API calls.
- R cannot write to non-ASCII paths on this system; output to an ASCII working directory (e.g. `./output`) and copy results afterwards.

## Reproduction order

1. `renv::restore()` (R) and install Python dependencies.
2. Run `00_config.R` to confirm GWAS IDs and paths.
3. Execute modules in gate order: `01_*` → `02_*`/`02b_*` → `04_mvmr.R` → `06_*` → `07_*` → `08_*` → `09_*`.
4. For zero-API runs of the C1 mediation analyses, use `local_run_C1.R` with the cached inputs in `data/raw/c1_cache/`.
