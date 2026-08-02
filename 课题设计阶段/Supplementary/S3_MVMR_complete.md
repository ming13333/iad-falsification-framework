# Supplementary Table 3. Multivariable MR (MVMR) and UVMR sensitivity results

condF = conditional F-statistic for the exposure in the MVMR model (NA for UVMR rows and when not computable).

| model | instrument_set | data_source | n_snps | exposure | method | b | se | p | condF | note |
|---|---|---|---|---|---|---|---|---|---|---|
| UVMR_insomnia | unclump2654 | local | 2462 | NA | IVW(local) | 0.104 | 0.0313 | 0.000929 | NA | Univariable MR of insomnia on AD across instrument sets |
| UVMR_insomnia | clump_loose | local |   54 | NA | IVW(local) | -0.13 | 0.203 | 0.523 | NA | Univariable MR of insomnia on AD across instrument sets |
| UVMR_insomnia | clump_tight(42) | local |   37 | NA | IVW(local) | -0.111 | 0.236 | 0.636 | NA | Univariable MR of insomnia on AD across instrument sets |
| MVMR_full | clump_loose | online |   44 | depression | MVIVW | 0.256 | 0.183 | 0.162 | NA | Multivariable MR with insomnia + LDL + depression + education |
| MVMR_full | clump_loose | online |   44 | education | MVIVW | -1.29 | 0.489 | 0.00847 | NA | Multivariable MR with insomnia + LDL + depression + education |
| MVMR_full | clump_loose | online |   44 | ldl | MVIVW | 1.26 | 0.686 | 0.0672 | NA | Multivariable MR with insomnia + LDL + depression + education |
| MVMR_full | clump_loose | online |   44 | insomnia | MVIVW | -0.567 | 0.283 | 0.0449 | NA | Multivariable MR with insomnia + LDL + depression + education |
| MVMR_no_chr19 | clump_loose | online |   43 | depression | MVIVW | 0.281 | 0.185 | 0.127 | NA |  |
| MVMR_no_chr19 | clump_loose | online |   43 | education | MVIVW | -1.28 | 0.489 | 0.00885 | NA |  |
| MVMR_no_chr19 | clump_loose | online |   43 | ldl | MVIVW | 1.52 | 0.724 | 0.0357 | NA |  |
| MVMR_no_chr19 | clump_loose | online |   43 | insomnia | MVIVW | -0.636 | 0.289 | 0.0279 | NA |  |
| MVMR_full | clump_tight(42) | online |   29 | depression | MVIVW | 0.198 | 0.269 | 0.462 | NA | Multivariable MR with insomnia + LDL + depression + education |
| MVMR_full | clump_tight(42) | online |   29 | education | MVIVW | -1.39 | 0.692 | 0.0449 | NA | Multivariable MR with insomnia + LDL + depression + education |
| MVMR_full | clump_tight(42) | online |   29 | ldl | MVIVW | 1.18 | 0.854 | 0.167 | NA | Multivariable MR with insomnia + LDL + depression + education |
| MVMR_full | clump_tight(42) | online |   29 | insomnia | MVIVW | -0.527 | 0.378 | 0.163 | NA | Multivariable MR with insomnia + LDL + depression + education |
| MVMR_no_chr19 | clump_tight(42) | online |   28 | depression | MVIVW | 0.271 | 0.278 | 0.329 | NA |  |
| MVMR_no_chr19 | clump_tight(42) | online |   28 | education | MVIVW | -1.34 | 0.693 | 0.0531 | NA |  |
| MVMR_no_chr19 | clump_tight(42) | online |   28 | ldl | MVIVW |  1.6 | 0.944 | 0.0909 | NA |  |
| MVMR_no_chr19 | clump_tight(42) | online |   28 | insomnia | MVIVW | -0.659 | 0.398 | 0.0981 | NA |  |
| MVMR_full | clump_tight(42) | online |   31 | depression | NA | 0.191 | 0.254 | 0.451 | NA | Multivariable MR with insomnia + LDL + depression + education |
| MVMR_full | clump_tight(42) | online |   31 | education | NA | -1.36 | 0.635 | 0.0318 | NA | Multivariable MR with insomnia + LDL + depression + education |
| MVMR_full | clump_tight(42) | online |   31 | ldl | NA | 1.17 | 0.811 | 0.149 | NA | Multivariable MR with insomnia + LDL + depression + education |
| MVMR_full | clump_tight(42) | online |   31 | insomnia | NA | -0.539 | 0.355 | 0.129 | NA | Multivariable MR with insomnia + LDL + depression + education |
| MVMR_no_chr19 | clump_tight(42) | online |   30 | depression | NA | 0.261 | 0.261 | 0.319 | NA |  |
| MVMR_no_chr19 | clump_tight(42) | online |   30 | education | NA | -1.31 | 0.635 | 0.0393 | NA |  |
| MVMR_no_chr19 | clump_tight(42) | online |   30 | ldl | NA | 1.56 | 0.89 | 0.0789 | NA |  |
| MVMR_no_chr19 | clump_tight(42) | online |   30 | insomnia | NA | -0.66 | 0.372 | 0.0761 | NA |  |
