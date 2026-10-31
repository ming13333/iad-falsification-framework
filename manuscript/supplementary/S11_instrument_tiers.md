# Supplementary Table S11

**Instrument-tier sensitivity of the insomnia -> AD IVW estimate.** All values are taken from Supplementary Table S2 (local harmonised summary statistics; Kunkle et al., 2019 outcome). SE inflation is the ratio of the clumped standard error to the unclumped standard error. No estimate was re-fitted for this table.

| Instrument tier | Clumping | n IV | beta | SE | P | SE inflation vs unclumped | Direction | Gate G2 |
|---|---|---|---|---|---|---|---|---|
| Unclumped | None (genome-wide significant only) | 2462 | +0.104 | 0.031 | 0.000929 | 1.00x | positive | Pass |
| Loose | r2 < 0.1, 10,000 kb | 54 | -0.130 | 0.203 | 0.523 | 6.50x | negative | Fail |
| Tight | r2 < 0.001, 10,000 kb | 37 | -0.111 | 0.236 | 0.636 | 7.54x | negative | Fail |

**Notes.** (1) The tight tier is defined by r2 < 0.001 clumping at a 10,000-kb window, which leaves 42 loci; 37 variants remain after harmonisation. A 5,000-kb window returns the same 37 variants and the same estimate (beta = -0.111, P = 0.64), so the tier does not depend on the window width over this range. (2) Gate G2 requires a clumped IVW estimate that remains significant in the claimed direction, so no tier passes. (3) The unclumped estimate is shown for reference only; correlated instruments violate the independence assumption and its standard error is not interpretable as sampling precision. (4) The SE inflation ratios are computed on fixed-effect standard errors. The unclumped reference is 0.0313 (P = 9.3e-4), the value reported in the main text; under multiplicative random effects the unclumped SE is 0.0381 (P = 0.0066), which gives inflation ratios of 5.33x and 6.18x instead of 6.50x and 7.54x. Heterogeneity in the unclumped set is extreme (Q = 3,660 on 2,461 df, P = 1.3e-50), which favours the random-effects reference, but the heterogeneity of the clumped tiers was not archived, so the two conventions cannot be matched exactly within a tier. Under either convention the standard error widens more than fivefold and no tier passes G2, which is the only use made of these ratios.
