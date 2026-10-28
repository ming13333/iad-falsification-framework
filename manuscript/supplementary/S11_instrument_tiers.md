# Supplementary Table S11

**Instrument-tier sensitivity of the insomnia -> AD IVW estimate.** All values are taken from Supplementary Table S2 (local harmonised summary statistics; Kunkle et al., 2019 outcome). SE inflation is the ratio of the clumped standard error to the unclumped standard error. No estimate was re-fitted for this table.

| Instrument tier | Clumping | n IV | beta | SE | P | SE inflation vs unclumped | Direction | Gate G2 |
|---|---|---|---|---|---|---|---|---|
| Unclumped | None (genome-wide significant only) | 2462 | +0.104 | 0.031 | 0.000929 | 1.00x | positive | Pass |
| Loose | r2 < 0.1, 10,000 kb | 54 | -0.130 | 0.203 | 0.523 | 6.50x | negative | Fail |
| Tight | r2 < 0.001, 10,000 kb | 37 | -0.111 | 0.236 | 0.636 | 7.54x | negative | Fail |

**Notes.** (1) The tight tier is defined by r2 < 0.001 clumping at a 10,000-kb window, which leaves 42 loci; 37 variants remain after harmonisation and the 5,000-kb window reported in the main text. (2) Gate G2 requires a clumped IVW estimate that remains significant in the claimed direction, so no tier passes. (3) The unclumped estimate is shown for reference only; correlated instruments violate the independence assumption and its standard error is not interpretable as sampling precision.
