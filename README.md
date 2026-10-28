# iad-falsification-framework

Analysis pipeline and frozen results for a six-gate falsification framework for Mendelian randomization (MR)-based causal claims, applied to insomnia–Alzheimer's disease (AD) comorbidity as a worked example.

**Version**: v1.2.1

## Citation

Luo M, Ye W, Liu Q. A six-gate falsification framework for diagnosing locus-driven confounding in Mendelian randomization: analysis code, simulation benchmark and frozen results (v1.2.1). Zenodo. doi:10.5281/zenodo.23733172

Cite the version DOI above rather than the concept DOI (10.5281/zenodo.23732880) when referring to specific numerical results, because the benchmark values changed between v1.0.0 and v1.2.0. The older deposits under DOI 10.5281/zenodo.21858125 (v1.0.0 and v1.1.0) were made under an earlier repository link and are not versions of the record above; they are superseded.

## Summary of results

- Six falsification gates: Association → Robustness → Genetic architecture → Direct effect → Biological mediation → Directional external validation. Each gate contributes 0–2 points; the total maps to Grade A (10–12), B (7–9), C (4–6) or D (0–3). Failure at the robustness gate caps the total at 6.
- Primary case: insomnia → AD is **Grade C** — shared liability confined to the *APOE* locus, not an independent upstream cause. The unclumped positive estimate (β = +0.10) reverses and becomes null after LD clumping (β = −0.13, P = 0.52); genome-wide r_g ≈ 0 (P = 0.57); colocalization is consistent with reverse-direction sharing; no protein mediator survives correction.
- Control case: education → AD remains inverse (β = −0.33, P = 1.1 × 10⁻⁵) and is Grade A, so the framework is not simply returning nulls.
- Benchmark: 43,200 simulated replicates over effect size, clumping granularity, pleiotropy regime, sample overlap and instrument count. With the decisive-failure cap applied, sensitivity at β = 0.15 is 0.878 / 0.724 / 0.691 and marginal FDR is 0.100 / 0.151 for none / balanced / directional pleiotropy; specificity under the C/D convention is 1.00 / 0.88 / 0.81.
- Twelve-case validation cohort (A3 / B2 / C4 / D3), plus five East Asian cross-ancestry directional screens.

## Repository structure

```
.
├── CITATION.cff            # Citation metadata
├── LICENSE                 # MIT
├── MANIFEST_sha256.csv     # SHA-256 of every deposited file (code/build_manifest.py)
├── README.md               # This file
├── renv.lock               # R environment (renv::restore())
├── .zenodo.json            # Deposit metadata
├── code/
│   ├── README.md           # Pipeline map (gate → script)
│   ├── requirements.txt    # Python environment
│   ├── r_analysis/         # 25 R modules (00_config.R entry point)
│   └── *.py                # simulation, threshold robustness, figures, EAS replication, ref audits
├── results/
│   ├── simulation/         # frozen benchmark outputs, incl. _precap/ (pre-cap comparison)
│   ├── ea_mr/              # East Asian replication outputs
│   ├── G2b_edu/            # protein-mediation outputs
│   └── MetMediation_local/ # metabolite mediation outputs
└── manuscript/
    ├── figures/            # Fig 1–5 (PNG + SVG)
    └── supplementary/      # Supplementary Tables S1–S12 and Supplementary Notes
```

## Reproduction workflow

1. **R environment** — restore the exact package versions:
   ```r
   install.packages("renv")
   renv::restore()
   ```
   R 4.5.2 was used; see `renv.lock`.

2. **Python environment** — Python 3.13.14 with the pinned versions:
   ```bash
   pip install -r code/requirements.txt
   ```

3. **Simulation benchmark (fully self-contained, no external data)**:
   ```bash
   python code/sim_framework_operating_chars.py    # 43,200 replicates, seed 20260804, ~25 s
   python code/sim_marginal_fdr.py                 # marginal FDR with Wilson intervals
   python code/make_table2_uncertainty.py          # Table 2 point estimates + CIs
   python code/threshold_robustness.py             # Supplementary Table S12
   ```
   Outputs are written to `output/results/Simulation/`. They should match `results/simulation/` byte for byte; `MANIFEST_sha256.csv` lists the expected hashes.

4. **Empirical pipeline** — entry points, one per gate:
   - `code/r_analysis/00_config.R` — global configuration (paths, thresholds, LD reference)
   - `code/r_analysis/01_bidirectional_mr_coloc.R` — bidirectional MR + colocalization (G1, G2)
   - `code/r_analysis/06c_ldsc_final.R` — LD score regression (G3)
   - `code/r_analysis/04_mvmr.R` — multivariable MR (G4)
   - `code/r_analysis/09_metabolite_mediation.R` — two-step mediation (G5)
   - `code/ea02_instruments.py` → `code/ea04_mr.py` → `code/ea05_transethnic_insomnia_ad.py` — cross-ancestry screens (G6)

5. **Integrity check**:
   ```bash
   python code/build_manifest.py --check
   ```

6. **External data** — the empirical gates use GWAS summary statistics from IEU OpenGWAS, GWAS Catalog and NIAGADS GARD, downloaded on demand by the fetch scripts under `code/`. **Raw and harmonised summary statistics are not deposited** (size and data-use terms); the empirical gate scores can be audited against the cited sources but not recomputed from this deposit alone.

## Release history

| Version | Change |
|---|---|
| v1.2.1 | Corrects the file manifest only. `MANIFEST_sha256.csv` in v1.2.0 hashed the author's CRLF checkout rather than the archived bytes, so 125 of 159 entries failed verification on any other machine; entry sizes are now the blob sizes for the same reason. Archived content is otherwise identical to v1.2.0. |
| v1.2.0 | Simulation now applies the decisive-failure cap (4,363 of 43,200 replicates regrade B → C; sensitivity at β = 0.15 falls 0.973 → 0.878 without pleiotropy; specificity unchanged). Adds Supplementary Tables S10–S12, `threshold_robustness.py`, `build_manifest.py`, frozen outputs under `results/simulation/` including `_precap/` copies, and a deterministic reproduction check. |
| v1.1.0 | English-only cleaned release. |
| v1.0.0 | First deposit (DOI 10.5281/zenodo.21858125). Its simulation script did not apply the decisive-failure cap; do not use it to reproduce the current Table 2. |

## Notes on this release

- Chinese-language development documents (project design notes, session handoffs, reviewer correspondence) are intentionally excluded; they are not required for reproduction.
- File names are ASCII; code comments and documentation are in English.
- The `data/` directory (raw and harmonised inputs, liftover chains) is excluded from this repository and from the tagged archive by `.gitignore`.
- The manuscript text, figures and supplementary tables are in `manuscript/`. The typeset version is published separately; this deposit is the code and results archive cited by it.

## License

MIT. See LICENSE.
