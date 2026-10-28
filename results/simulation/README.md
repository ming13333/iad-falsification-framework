# Simulation benchmark — frozen outputs (v1.2.0)

Every file here is produced by `code/sim_framework_operating_chars.py` (seed `20260804`,
43,200 replicates = 3 effect sizes x 3 block counts x 3 pleiotropy regimes x 2 overlap
settings x 2 instrument counts x 400 replicates) and its downstream summarisers.

The **post-cap** files are the ones the manuscript reports. The decisive-failure rule
(G2 = 0 -> total capped at 6) is applied inside `grade_framework()`; the **pre-cap**
copies in `_precap/` are the identical grid scored with the plain additive total, and
exist so that Supplementary Table S12.5 can be checked in both directions.

| File | Produced by | Used for |
|---|---|---|
| `sim_operating_chars.csv` | `sim_framework_operating_chars.py` | per-cell operating characteristics; Table 2 source |
| `sim_marginal.csv` | `sim_framework_operating_chars.py` | marginal means across cells; Table 2 and Figure 2 source |
| `sim_cell_fdr.csv` | `sim_framework_operating_chars.py` | cell-level FDR, the input to re-weighting |
| `sim_marginal_fdr.csv` | `sim_marginal_fdr.py` | marginal FDR with Wilson intervals |
| `table2_uncertainty.csv` | `make_table2_uncertainty.py` | Table 2 point estimates with 95% Wilson CIs |
| `fdr_null_fraction_sensitivity.csv` | `sim_marginal_fdr.py` | half-null re-weighting quoted in Limitations (0.10 -> 0.18; 0.15 -> 0.26) |
| `sim_summary.txt` | `sim_framework_operating_chars.py` | plain-text audit log of the run |
| `S13_score_cut_roc.csv`, `S13_operating_points.json` | `threshold_robustness.py` | benchmark ROC; false-positive rates 3.6 / 10.3 / 17.5% (Table S12.4) |
| `S14_table2_cap_audit.csv` | `threshold_robustness.py` | the 4,363 B->C regrades (Table S12.5) |
| `_precap/sim_operating_chars_pre_cap_20261028.csv` | pre-cap run | Table S12.5, left-hand column |
| `_precap/sim_marginal_pre_cap_20261028.csv` | pre-cap run | Table S12.5, left-hand column |
| `_precap/rerun_capped_stdout.txt` | capped run | console record of the post-cap rerun |

## Not included

`sim_replicates.csv` (43,200 rows, 6.3 MB) and its pre-cap twin are **not** deposited.
They are deterministic given the seed and the pinned environment, and are regenerated in
about 25 s:

```bash
python code/sim_framework_operating_chars.py   # writes ./output/results/Simulation/
```

The SHA-256 of the regenerated file is listed in `MANIFEST_sha256.csv` at the repository
root, so a reader can confirm that their run matches the archived one byte for byte
without downloading the table itself. If the checksum differs, the environment or the
script has drifted — not the reported marginals.

## Reproduction check performed for this release

| | |
|---|---|
| Environment | Python 3.13.14, numpy 2.1.3, pandas 2.2.3 (see `code/requirements.txt`) |
| Run | fresh directory, script copied out of the repo, no cached inputs |
| Wall time | 24.5 s |
| Result | `sim_replicates.csv`, `sim_operating_chars.csv`, `sim_marginal.csv`, `sim_summary.txt` all byte-identical to the files here |

Key marginals at beta = 0.15: sensitivity 0.878 / 0.724 / 0.691 and marginal FDR
0.100 / 0.151 for none / balanced / directional pleiotropy, matching Table 2.
