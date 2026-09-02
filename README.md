# iad-falsification-framework

Analysis pipeline for a six-level falsification framework for Mendelian randomization (MR)-based causal claims, applied to the insomnia–Alzheimer's disease (AD) comorbidity as a test case.

**Version**: v1.1.0 (English-only release)

## Citation

Luo M, Ye W, Liu Q. A falsification framework for causal claims in polygenic epidemiology: the insomnia–Alzheimer's disease test case. Zenodo. doi:10.5281/zenodo.21858125

## Summary of results

- Six falsification gates: Association → Robustness → Genetic architecture → Direct effect → Biological mediation → Directional external validation.
- Outcome: Grade C — evidence supports shared liability (APOE-locus-specific sharing) rather than insomnia as an independent upstream cause of AD.
- Genome-wide genetic correlation rg ≈ 0 (LDSC); positive unclumped UVMR signal is a clumping artifact and flips to null after LD clumping.
- Extension: 12 trait pairs × 4 disease domains × 43,200 simulations; 5 East Asian (EAS) cross-ancestry replications.

## Repository structure

```
.
├── CITATION.cff          # Citation metadata
├── LICENSE               # MIT
├── README.md             # This file
├── renv.lock             # R package environment (renv::restore())
├── code/
│   ├── README.md         # Pipeline map (gate → script)
│   ├── r_analysis/       # 25 R modules (00_config.R entry point)
│   └── *.py              # Python: EAS liftover/instruments/MR, simulations, figures, ref audits
├── data/
│   ├── raw/c1_cache/     # Cached harmonised MR inputs (zero-API reproduction)
│   ├── processed/        # EAS instruments & harmonised datasets
│   └── ref/              # Liftover chain files (GRCh38 → GRCh37)
├── results/              # Curated analysis outputs (CSV/reports)
└── manuscript/           # Frontiers in Genetics submission (v1): docx + md source, figures/, supplementary/
```

## Reproduction workflow

1. **Environment (R)**: restore the exact package versions:
   ```r
   install.packages("renv")
   renv::restore()
   ```
   R ≥ 4.2 recommended; see `code/r_analysis/package_versions.md` for the frozen version list.

2. **Python**: Python ≥ 3.9 with `numpy`, `pandas`, `scipy`, `matplotlib`, `pyreadr`, `statsmodels` (see `code/README.md` for per-script imports).

3. **Entry points**:
   - `code/r_analysis/00_config.R` — global configuration (paths, thresholds, LD reference).
   - `code/r_analysis/01_bidirectional_mr_coloc.R` — bidirectional MR + coloc (Gate 2).
   - `code/r_analysis/06c_ldsc_final.R` — LD score regression (Gate 3).
   - `code/r_analysis/04_mvmr.R` — multivariable MR (Gate 4).
   - `code/r_analysis/09_metabolite_mediation.R` — two-step mediation (Gate 5).
   - `code/ea02_instruments.py` → `code/ea04_mr.py` — EAS replication (Gate 6).
   - `code/sim_framework_operating_chars.py` — 43,200-replicate simulation.

4. **Zero-API reproduction**: cached harmonised inputs in `data/raw/c1_cache/` allow re-running the core MR analyses offline. See `data/raw/c1_cache/MANIFEST.csv` for provenance of each cached file.

5. **Caveats on external data**: some analyses require GWAS summary statistics from IEU OpenGWAS / GWAS Catalog / NIAGADS GARD. These are downloaded on demand by the fetch scripts; the cached inputs cover the primary mediation analyses.

## Notes on this release

- v1.1.0 is an English-only, cleaned release for journal submission reproducibility.
- Chinese-language development documents (project design notes, session handoffs) are intentionally excluded from this archive; they are not required for reproduction.
- All file names are ASCII; all comments and documentation are in English.
- The `data/` directory (cached harmonised inputs, processed EAS datasets, liftover chains) is **not** included in this GitHub repository; it is archived in full in the Zenodo record (doi:10.5281/zenodo.21858125, `data/` subdirectory). To reproduce offline, download the Zenodo archive and place its `data/` alongside this repository, or run the fetch scripts to re-download inputs from public sources.
- Manuscript text, figures and supplementary tables are provided in the `manuscript/` directory of this repository (Frontiers in Genetics submission, v1).

## License

MIT. See LICENSE.
