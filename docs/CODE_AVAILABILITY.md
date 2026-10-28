# Code and Data Availability

This archive accompanies the manuscript:

> A six-gate falsification framework for diagnosing locus-driven confounding in Mendelian randomization

## Availability statement (as used in the manuscript)

> **Data availability.** All GWAS summary statistics analysed here are publicly available: IEU OpenGWAS (ukb-b-3957 [insomnia], ieu-b-2 and ieu-a-1239 [Alzheimer's disease], bbj-a-77, bbj-a-129 [East Asian traits], GCST90296498 [East Asian education], GCST90027158 [East Asian Alzheimer's disease]) and NIAGADS NG00182 (GARD cohort). Accessions, sample sizes, ancestries and citations are listed in the Materials and Equipment section and Supplementary Table S2. No individual-level data were used. Derived results, simulation outputs, analysis code and environment specifications are archived on Zenodo (DOI 10.5281/zenodo.23733172, version v1.2.1) and maintained at GitHub (ming13333/iad-falsification-framework).

> **Code availability.** Custom R (25 modules) and Python analysis code are provided in this archive (`code/`), with both runtimes frozen (`renv.lock` for R 4.5.2, `code/requirements.txt` for Python 3.13.14). Reproduction instructions are in `README.md` and `code/README.md`.

## What is in this archive

- `code/r_analysis/` — 25 R modules implementing the six falsification gates (bidirectional MR, MRlap, CAUSE, colocalization, MVMR, two-step mediation, LDSC, Steiger, power calculations).
- `code/*.py` — Python scripts for East Asian liftover, instruments and MR; the 43,200-replicate simulation and its summarisers; threshold and cap robustness; figure generation; manifest and workbook builders.
- `results/simulation/` — frozen benchmark outputs, including the post-cap values behind Table 2 and Figure 2, and `_precap/` copies kept for the before/after comparison in Supplementary Table S12.5.
- `results/validation/`, `results/ea_mr/`, `results/G2b_edu/`, `results/MetMediation_local/` — curated analysis outputs behind the twelve-case cohort, the cross-ancestry screens and the mediation analyses.
- `manuscript/figures/`, `manuscript/supplementary/` — Figures 1–5 (PNG + SVG) and Supplementary Tables S1–S12.
- `MANIFEST_sha256.csv` — SHA-256 of every deposited file; verify with `python code/build_manifest.py --check`.

## What is not in this archive

Raw and harmonised GWAS summary statistics. These are excluded for size and because they remain under their own data-use terms; they are downloaded at run time by the fetch scripts (`code/r_analysis/B1_fetch_opengwas.R`, `code/ea01_liftover_gard.py`, `code/cache_c1_inputs.R`), which name the exact accessions. As a consequence, the empirical gate scores can be audited against the cited sources but cannot be recomputed from this deposit alone. The simulation benchmark, by contrast, is fully self-contained and reproduces in about 25 s.

## Reproduction steps

1. Restore the R environment: `renv::restore()` (see `renv.lock`).
2. Install the Python environment: `pip install -r code/requirements.txt`.
3. Run the benchmark: `python code/sim_framework_operating_chars.py`, then `code/sim_marginal_fdr.py`, `code/make_table2_uncertainty.py`, `code/threshold_robustness.py`. Outputs should match `results/simulation/` byte for byte.
4. For the empirical pipeline, run `code/r_analysis/00_config.R` to set the configuration, then execute modules in gate order (see `code/README.md` for the gate → script map).

## External dependencies

The fetch scripts document the exact accession identifiers. IEU OpenGWAS, GWAS Catalog and NIAGADS downloads are free of charge; some require accepting the source study's data-use terms.

## Notes

- All file names are ASCII; all documentation and code comments are in English.
- Chinese-language development documents (design notes, session handoffs, reviewer correspondence) are excluded by design; they are not required for reproduction.
