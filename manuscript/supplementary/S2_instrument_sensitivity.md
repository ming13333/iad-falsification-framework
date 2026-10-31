# Supplementary Table 2. Instrument-set sensitivity for insomnia -> AD

Unclumped G1 analysis reports full multi-method MR (IVW / MR-Egger / weighted median / weighted mode) plus Cochran's Q and MR-Egger intercept. UVMR rows from MVMR instrument-set sensitivity report IVW only for unclumped/clumped-loose/clumped-tight sets; Egger/WMed/WMode were not run for clumped subsets (NA).

**Two rows report the same analysis.** `G1 Insomnia -> AD (unclumped)` and `UVMR Insomnia -> AD (unclump2654)` use the same 2,462 variants and return the same coefficient (0.104). They differ only in the variance convention: the G1 row gives the multiplicative random-effects standard error (0.0381, P = 0.0066) and the UVMR row the fixed-effect standard error (0.0313, P = 9.3e-4). The ratio between them is exactly √(Q/df) = 1.220 (Q = 3,660 on 2,461 df), so the difference is a convention for handling heterogeneity, not a discrepancy between fits. Heterogeneity is extreme (Q P = 1.3e-50), which makes the random-effects value the more defensible of the two; the main text reports the fixed-effect value for the unclumped reference and the standard-error inflation ratios are computed on that convention, with the random-effects alternative given in Supplementary Table S11, note 4.

| analysis | n_snps | F_mean | F_min | b_ivw | se_ivw | p_ivw | b_egger | p_egger | b_wmed | p_wmed | b_wmode | p_wmode | Q_ivw | Q_p_ivw | egger_intercept | egger_intercept_p | se_egger | se_wmed | se_wmode |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| G1 Insomnia -> AD (unclumped) | 2462 | 38.5 | 29.7 | 0.104 | 0.0381 | 0.00663 | 2.15 | 1.73e-25 | 0.117 | 0.0148 | -0.138 | 0.667 | 3.66e+03 | 1.25e-50 | NA | NA | 0.2036037708 | 0.0481377550 | 0.3201596454 |
| G1 AD -> Insomnia (unclumped) | 1132 |  117 | 29.5 | -0.00273 | 0.000607 | 6.63e-06 | -0.0132 | 3.86e-48 | -0.00753 | 7.08e-53 | -0.00757 | 3.48e-50 | 5.25e+03 |    0 | NA | NA | 0.0008659358 | 0.0004922963 | 0.0004833684 |
| G1 Insomnia -> AD (replication, unclumped) | 2615 | 38.4 | 29.7 | 0.0963 | 0.0208 | 3.68e-06 | 1.34 | 5.11e-31 | 0.158 | 4.6e-09 | -0.722 | 0.000582 | 3.78e+03 | 5.4e-46 | NA | NA | 0.1142233193 | 0.0268782232 | 0.2096213144 |
| G1 AD -> Insomnia (replication, unclumped) | 4983 | 48.9 | 29.4 | 0.00731 | 0.000535 | 1.7e-42 | -0.0231 | 1.43e-64 | 0.00238 | 0.000213 | -0.0179 | 2.78e-10 | 1.09e+04 |    0 | NA | NA | 0.0013413194 | 0.0006429387 | 0.0028324455 |
| UVMR Insomnia -> AD (unclump2654) | 2462 | NA | NA | 0.104 | 0.0313 | 0.000929 | NA | NA | NA | NA | NA | NA | NA | NA | NA | NA | NA | NA | NA |
| UVMR Insomnia -> AD (clump_loose) |   54 | NA | NA | -0.13 | 0.203 | 0.523 | NA | NA | NA | NA | NA | NA | NA | NA | NA | NA | NA | NA | NA |
| UVMR Insomnia -> AD (clump_tight(42)) |   37 | NA | NA | -0.111 | 0.236 | 0.636 | NA | NA | NA | NA | NA | NA | NA | NA | NA | NA | NA | NA | NA |
