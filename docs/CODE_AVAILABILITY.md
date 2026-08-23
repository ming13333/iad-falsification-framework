# Code and Data Availability

This archive accompanies the manuscript:

> A falsification framework for causal claims in polygenic epidemiology: the insomnia–Alzheimer's disease test case

## Availability statement (as used in the manuscript)

> **Data availability.** All analyses used publicly available summary statistics: IEU OpenGWAS (ukb-b-3957 [insomnia], ieu-b-2 [Alzheimer's disease], ieu-a-1239 [Alzheimer's disease, IGAP], bbj-a-77 / bbj-a-129 [East Asian traits], GCST90296498 [East Asian education], GCST90027158 [East Asian Alzheimer's disease]) and NIAGADS NG00182 (GARD cohort, East Asian Alzheimer's disease). Full accession identifiers, sample sizes, ancestry and citations are provided in Supplementary Table S2. Cached harmonised inputs for the primary mediation analyses are included in this archive (`data/raw/c1_cache/`, see `MANIFEST.csv`) to enable zero-API reproduction.

> **Code availability.** Custom R (25 modules) and Python analysis code are provided in this archive (`code/`), with the environment frozen in `renv.lock`. Reproduction instructions are in `README.md` and `code/README.md`.

## What is in this archive

- `code/r_analysis/` — 25 R modules implementing the six falsification gates (bidirectional MR, MRlap, CAUSE, coloc, MVMR, two-step mediation, LDSC, Steiger, power calculations).
- `code/*.py` — Python scripts for East Asian liftover/instruments/MR, the 43,200-replicate simulation, figure generation, and reference audits.
- `data/raw/c1_cache/` — cached harmonised two-sample MR inputs (instruments + harmonised datasets) with provenance in `MANIFEST.csv`.
- `data/processed/` — East Asian education instruments and harmonised datasets (GRCh37).
- `data/ref/` — GRCh38-to-GRCh37 liftover chain file.
- `results/` — curated analysis outputs (summary tables and reports).

## Reproduction steps

1. Restore the R environment: `renv::restore()` (see `renv.lock`).
2. Run `code/r_analysis/00_config.R` to set the configuration, then execute modules in gate order (see `code/README.md` for the gate → script map).
3. Core mediation analyses can be re-run offline using `data/raw/c1_cache/` (zero API calls).
4. EAS replication and simulation scripts require Python ≥ 3.9 (imports listed in `code/README.md`).

## External dependencies

Analyses that are not covered by the cached inputs require downloading public GWAS summary statistics at runtime; the fetch scripts (`code/r_analysis/B1_fetch_opengwas.R`, `code/ea01_liftover_gard.py`) document the exact accession IDs. These downloads are free and require no credentials for the IEU OpenGWAS public endpoints.

## Notes

- All file names are ASCII; all documentation and code comments are in English.
- Chinese-language development documents (design notes, session handoffs) are excluded from this archive by design; they are not required for reproduction.
