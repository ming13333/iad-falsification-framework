# Reviewer traceability report

Baseline: `manuscript Frontiers 0902.docx` (submitted)  
Revision: `manuscript_Frontiers_Methods_v2.docx`  
Marked copy: `manuscript_Frontiers_Methods_v2_marked.docx`

- Differences detected: **71** body paragraphs and **56** table cells
- Highlighted as answers to a reviewer comment: **47** paragraphs and **56** cells, 47,908 characters
- Not highlighted: **24** differences (conversion artefact / alignment 17, journal/technical requirement 7)
- Comments with a landing spot: **22/22**

## 1. Where each comment is answered

| Comment | Topic | Passages | Characters | Where |
|---|---|---|---|---|
| R1-1 | Scoring rules inconsistent across text, Table 1 and S8; G2 failure could still reach Grade A | 35 | 5,337 | para 39, para 42, para 48, para 99, para 150, para 152 +29 |
| R1-2 | Archived simulation code differs from the described workflow | 36 | 22,353 | para 0, para 8, para 9, para 14, para 15, para 16 +30 |
| R1-3 | What the framework adds beyond routine LD handling | 5 | 4,098 | para 40, para 69, para 87, para 88, para 99 |
| R1-4 | Sensitivity/specificity definitions; Grade C; uncertainty; the 0.20 threshold; effect mix | 22 | 13,147 | para 9, para 14, para 63, para 86, para 90, para 145 +16 |
| R1-5 | Insufficient evidence is not evidence against | 2 | 6,350 | para 77, para 90 |
| R1-6 | Chromosome 19 is not the APOE region; region definition; how 32 and 47 were selected | 2 | 3,239 | para 70, para 86 |
| R1-7 | 'Three null results' contradicts a negative direct effect; CAUSE inputs | 3 | 4,659 | para 41, para 68, para 152 |
| R1-8 | Conditional instrument strength; confounder handling; mediation details | 5 | 9,554 | para 43, para 44, para 71, para 72, para 90 |
| R1-9 | Evidence behind the external-validation scores; kappa is not causal accuracy | 4 | 8,713 | para 40, para 45, para 73, para 90 |
| R1-10 | From risk factors to drug targets | 1 | 1,851 | para 89 |
| R3-1 | Harmonise terminology for directional and causal claims | 4 | 2,307 | para 8, para 12, para 35, para 36 |
| R3-2 | What 'precise' means | 3 | 3,018 | para 8, para 12, para 69 |
| R3-3 | European LD reference panel applied to East Asian data | 4 | 8,272 | para 45, para 46, para 73, para 90 |
| R3-4 | Rationale for r2 < 0.001 with a 10,000-kb window (Methods corrected) | 5 | 6,091 | para 40, para 53, para 68, para 69, table 4 r4c3 |
| R3-5 | Do the three corrections act in sequence on the variant set | 2 | 3,331 | para 41, para 68 |
| R3-6 | How confounders were chosen; why F > 10 sits at G4 | 1 | 2,117 | para 43 |
| R3-7 | Power comparability across ancestries; cross-ancestry bias | 4 | 8,272 | para 45, para 46, para 73, para 90 |
| R3-8 | Where MR-Egger, Cochran's Q, MRlap and CAUSE sit in the framework | 2 | 2,169 | para 41, para 152 |
| R3-9 | Justification of the simulation parameter grid | 2 | 4,154 | para 59, para 60 |
| R3-10 | Definition and algorithm of trans-ethnic re-clumping | 1 | 1,011 | para 46 |
| R3-11 | Do not describe a null r_g as 'unchanged' | 1 | 2,070 | para 70 |
| R3-12 | Three-line tables without vertical rules | 5 | 0 | Table 1, Table 2, Table 3, Table 4, Table 5 |

## 2. Passage-by-passage index

| Location | Comments | Opening words | Change | Chars | Why |
|---|---|---|---|---|---|
| para 0 | R1-2 | A six-gate falsification framework for diagnosing… | edited, sentence level (sim 0.74) | 200 | Title: '43,200-simulation validation' -> 'a 43,200-replicate benchmark of its scoring… |
| para 8 | R1-2;R3-1;R3-2 | Mendelian randomization (MR) uses germline variants… | edited, sentence level (sim 0.72) | 1386 | Abstract: claims narrowed to 'the scoring rule', 'precise' replaced, association/causal… |
| para 9 | R1-2;R1-4 | We evaluated the framework on the association… | edited (sim 0.94) | 116 | Abstract: benchmark characterised as proxy gate implementations; operating-characteristic… |
| para 12 | R3-1;R3-2 | Mendelian randomization uses germline genetic… | edited (sim 0.93) | 115 | Introduction: 'precise' unpacked into statistical significance vs information;… |
| para 14 | R1-2;R1-4 | Addressing this problem requires a structured… | edited (sim 0.92) | 93 | Introduction: what is characterised is the scoring rule under proxy gates;… |
| para 15 | R1-2 | Two structural properties distinguish this… | edited (sim 0.98) | 22 | Introduction: 'its operating characteristics' -> 'the operating characteristics of its… |
| para 16 | R1-2 | We benchmark the framework under controlled stress… | edited (sim 0.92) | 113 | Introduction: 'LD concentration' -> granularity of the clumping partition, which is what… |
| para 19 | R1-2 | Software environment. Analyses run in a… | edited, sentence level (sim 0.80) | 343 | Software environment: pinned requirement set with versions, as asked under the… |
| para 32 | R1-2 | Archived framework. Simulation outputs, executable… | edited (sim 0.96) | 25 | Archived framework: version DOI 10.5281/zenodo.21858125 -> 23733172 (v1.2.1) |
| para 35 | R3-1 | Terminology. Three terms are used consistently… | new paragraph | 717 | New Methods paragraph defining causal claim / association / directed effect |
| para 36 | R1-2;R3-1 | The framework converts a directional Mendelian… | edited (sim 0.91) | 89 | Framing: benchmark 'through proxy gate implementations', score-to-grade mapping,… |
| para 39 | R1-1 | Gate G1 (association, screening). An unclumped… | edited, sentence level (sim 0.80) | 177 | Gate G1: stated as a binary screening gate with no partial credit |
| para 40 | R3-4;R1-3;R1-9 | Gate G2 (robustness). The primary signal must… | edited, sentence level (sim 0.66) | 1452 | Gate G2: primary clumping tier corrected to r2 < 0.1 with the stricter tier as… |
| para 41 | R1-7;R3-5;R3-8 | What each correction operates on. Only LD clumping… | new paragraph | 841 | New paragraph: only clumping changes the instrument set; Egger/Q/median/mode are… |
| para 42 | R1-1 | Gate G3 (genetic architecture). LDSC tests… | edited, sentence level (sim 0.85) | 355 | Gate G3: scoring rule for the not-evaluable case (1 when rg is direction-consistent but… |
| para 43 | R1-8;R3-6 | Gate G4 (direct effect). Multivariable MR (Burgess… | rewritten (sim 0.30) | 2117 | Gate G4: conditional vs unconditional F separated, confounder selection and the reporting… |
| para 44 | R1-8 | Gate G5 (biological mediation). Two-step MR… | edited, sentence level (sim 0.74) | 286 | Gate G5: 36 versus 25 proteins, the clumping rule and the scope of the null result |
| para 45 | R1-9;R3-3;R3-7 | Gate G6 (external validation). Directional… | edited, sentence level (sim 0.57) | 562 | Gate G6: direction concordance alone is not validation; no ancestry-matched panel; power… |
| para 46 | R3-3;R3-7;R3-10 | Trans-ethnic re-clumping. The step proceeds as… | new paragraph | 1011 | New paragraph: trans-ethnic re-clumping algorithm and what happens without an… |
| para 48 | R1-1 | Cumulative scores range from 0 to 12 points, with… | rewritten (sim 0.47) | 1566 | Grading rubric: single 0/1/2 scheme, binary G1/G6, decisive-failure cap, not-evaluable… |
| para 53 | R3-4 | 3.  Gate G2 (2–4 h, includes CAUSE MCMC fitting).… | new paragraph | 381 | Protocol step 3: clumping threshold corrected from r2 < 0.001 to r2 < 0.1 |
| para 59 | R1-2;R3-9 | Because the framework is prescriptive, the… | rewritten (sim 0.38) | 3505 | Simulation: actual data-generating process stated, G3/G4 degeneracy and absent methods… |
| para 60 | R1-2;R3-9 | The full data-generating process is defined in the… | edited, sentence level (sim 0.78) | 649 | Simulation: archived-code pointer and parameter provenance |
| para 62 | R1-2 | Operating characteristics of the scoring rule… | edited, sentence level (sim 0.80) | 75 | Results subheading: '43,200-simulation benchmark' -> 'the scoring rule' |
| para 63 | R1-2;R1-4 | At the null (β = 0), the scoring rule assigned… | rewritten (sim 0.52) | 3326 | Operating characteristics: scoring rule rather than framework; D-only convention named |
| para 68 | R1-7;R3-5;R3-4 | G2: robustness. LD clumping (r2 < 0.1, 10,000 kb… | edited, sentence level (sim 0.78) | 2490 | Results G2: three analyses separated instead of pooled as 'null'; CAUSE/MRlap inputs;… |
| para 69 | R1-3;R3-2;R3-4 | What LD correction changes: precision, not only… | new paragraph | 1517 | New Results subsection: three instrument tiers, SE inflation, what LD correction changes |
| para 70 | R1-6;R3-11 | G3: genetic architecture. Cross-trait LD Score… | rewritten (sim 0.30) | 2070 | Results G3: APOE region defined, chromosome-19 exclusion withdrawn as APOE-specific; r_g… |
| para 71 | R1-8 | G4: direct effect. Multivariable MR (MVMR)… | edited, sentence level (sim 0.64) | 887 | Results G4: conditional F gap declared, first-stage statistics reported, mediation… |
| para 72 | R1-8 | G5: biological mediation. Protein mediation was… | rewritten (sim 0.44) | 1296 | Results G5: 25 evaluable proteins, both path estimates, 9.5% mediation, scope of the null |
| para 73 | R1-9;R3-3;R3-7 | G6: external validation. Directional consistency… | edited, sentence level (sim 0.57) | 1731 | Results G6: evidence per score, withdrawn points, European panel on East Asian data, power |
| para 76 | R1-2 | The benchmarked operating characteristics above… | edited (sim 0.95) | 13 | 'framework' -> 'scoring rule' in the precision sentence |
| para 77 | R1-5 | Insufficient evidence versus evidence against. The… | new paragraph | 1382 | New Results subsection: insufficient evidence versus evidence against |
| para 85 | R1-2 | The insomnia–AD findings demonstrate how a… | edited, sentence level (sim 0.79) | 541 | Discussion: 'operating characteristics derived from' -> 'of its scoring rule' |
| para 86 | R1-2;R1-4;R1-6 | The APOE result reflects a broader pattern in… | edited, sentence level (sim 0.61) | 1169 | Discussion: scoring rule rather than framework; FDR figures updated after the cap was… |
| para 87 | R1-3 | Complementarity with reporting standards. While… | edited, sentence level (sim 0.56) | 420 | R1-3 asks what the full framework adds beyond routine practice and robustness checks.… |
| para 88 | R1-2;R1-3 | Generalizability of the template. Although… | edited, sentence level (sim 0.72) | 703 | R1-2 asked which code version the results came from; the archived-release DOI cited here… |
| para 89 | R1-10 | Implications for drug-target prioritization.… | rewritten (sim 0.35) | 1851 | Discussion: trait-level claim -> target requires cis-pQTL, tissue, direction of… |
| para 90 | R1-2;R1-4;R1-5;R1-8;R1-9;R3-3;R3-7 | Limitations. Several methodological boundaries… | rewritten (sim 0.32) | 4968 | Limitations: proxy implementation, FDR vs null fraction, insufficient vs against,… |
| para 91 | R1-2 | Conclusions. A six-gate falsification framework,… | edited, sentence level (sim 0.85) | 178 | Conclusions: claim narrowed to the scoring rule under proxy gates |
| para 93 | R1-2 | Data availability statement. All GWAS summary… | edited (sim 0.98) | 25 | Data availability: version DOI 10.5281/zenodo.21858125 -> 23733172 |
| para 99 | R1-1;R1-3 | Supplementary material. The Supplementary Material… | edited (sim 0.96) | 6 | Supplementary material: new tables S10-S12 listed |
| para 145 | R1-4;R1-2 | Figure 2. Simulation operating characteristics… | rewritten (sim 0.15) | 1041 | Figure 2 legend: both specificity conventions, recomputed under the decisive-failure cap |
| para 150 | R1-1 | Table 1. Two-layer gate specification: the… | rewritten (sim 0.39) | 239 | Table 1 caption: two-layer gate specification |
| para 152 | R1-1;R1-2;R1-7;R3-8 | All gates apply fixed a priori thresholds and… | rewritten (sim 0.39) | 1328 | Table 1 footnote: scoring tiers, decisive failure, CAUSE as diagnostic not scoring input |
| para 153 | R1-2;R1-4 | Table 2. Simulation operating characteristics of… | edited, sentence level (sim 0.77) | 134 | Table 2 caption: scoring rule under proxy gate implementations |
| para 155 | R1-2;R1-4 | Values are marginal across clumping-block count… | rewritten (sim 0.29) | 2131 | Table 2 footnote: recomputation under the cap, Wilson intervals, both specificity… |
| table 1 r1c3 | R1-1 | Empirical: 2 points | all | 19 | Table 1 rebuilt as a six-column, two-layer table (empirical criterion + proxy… |
| table 1 r1c4 | R1-1 | Empirical: 1 point | all | 18 | Table 1 rebuilt as a six-column, two-layer table (empirical criterion + proxy… |
| table 1 r1c5 | R1-1 | Empirical: 0 points | all | 19 | Table 1 rebuilt as a six-column, two-layer table (empirical criterion + proxy… |
| table 1 r1c6 | R1-1 | Proxy implementation in the benchmark | all | 37 | Table 1 rebuilt as a six-column, two-layer table (empirical criterion + proxy… |
| table 1 r2c3 | R1-1 | Unclumped IVW P < 0.05 in the claimed direction | all | 47 | Table 1 rebuilt as a six-column, two-layer table (empirical criterion + proxy… |
| table 1 r2c4 | R1-1 | — (binary gate) | all | 15 | Table 1 rebuilt as a six-column, two-layer table (empirical criterion + proxy… |
| table 1 r2c5 | R1-1 | P ≥ 0.05, direction reversed, or <3 instruments | all | 47 | Table 1 rebuilt as a six-column, two-layer table (empirical criterion + proxy… |
| table 1 r2c6 | R1-1 | IVW P < 0.05 and | b | > 10-4 (2); 0.05 ≤ P < 0.20… | all | 68 | Table 1 rebuilt as a six-column, two-layer table (empirical criterion + proxy… |
| table 1 r3c2 | R1-1 | Robustness to LD, overlap and pleiotropy | partial | 40 | Table 1 rebuilt as a six-column, two-layer table (empirical criterion + proxy… |
| table 1 r3c3 | R1-1 | Clumped IVW significant in the claimed direction;… | all | 97 | Table 1 rebuilt as a six-column, two-layer table (empirical criterion + proxy… |
| table 1 r3c4 | R1-1 | Clumped IVW significant but ≥ 1 diagnostic fails | all | 48 | Table 1 rebuilt as a six-column, two-layer table (empirical criterion + proxy… |
| table 1 r3c5 | R1-1 | Clumped IVW null or reversed; <3 clumped instruments | all | 52 | Table 1 rebuilt as a six-column, two-layer table (empirical criterion + proxy… |
| table 1 r3c6 | R1-1 | Clumped P < 0.05 and intercept P > 0.05 (2);… | all | 78 | Table 1 rebuilt as a six-column, two-layer table (empirical criterion + proxy… |
| table 1 r4c3 | R1-1 | rg direction-consistent (or null) with coloc PP.H4… | all | 80 | Table 1 rebuilt as a six-column, two-layer table (empirical criterion + proxy… |
| table 1 r4c4 | R1-1 | rg consistent but colocalization absent or PP.H4 <… | all | 55 | Table 1 rebuilt as a six-column, two-layer table (empirical criterion + proxy… |
| table 1 r4c5 | R1-1 | Architecture contradicts the claim; neither LDSC… | all | 67 | Table 1 rebuilt as a six-column, two-layer table (empirical criterion + proxy… |
| table 1 r4c6 | R1-1 | ≥ 50% of blocks retained and ≥ 5 instruments (2); ≥… | all | 72 | Table 1 rebuilt as a six-column, two-layer table (empirical criterion + proxy… |
| table 1 r5c3 | R1-1 | MVMR direct effect significant in the claimed… | all | 75 | Table 1 rebuilt as a six-column, two-layer table (empirical criterion + proxy… |
| table 1 r5c4 | R1-1 | Model estimable (F > 10) but direct effect… | all | 70 | Table 1 rebuilt as a six-column, two-layer table (empirical criterion + proxy… |
| table 1 r5c5 | R1-1 | Conditional F ≤ 10; no estimable direct effect | all | 46 | Table 1 rebuilt as a six-column, two-layer table (empirical criterion + proxy… |
| table 1 r5c6 | R1-1 | Clumped P < 0.05 and leave-one-out spread < 0.50… | all | 87 | Table 1 rebuilt as a six-column, two-layer table (empirical criterion + proxy… |
| table 1 r6c3 | R1-1 | FDR-corrected indirect effect consistent with the… | all | 55 | Table 1 rebuilt as a six-column, two-layer table (empirical criterion + proxy… |
| table 1 r6c4 | R1-1 | Only one of the two mediation steps significant | all | 47 | Table 1 rebuilt as a six-column, two-layer table (empirical criterion + proxy… |
| table 1 r6c5 | R1-1 | Neither step significant; indirect effect reversed;… | all | 73 | Table 1 rebuilt as a six-column, two-layer table (empirical criterion + proxy… |
| table 1 r6c6 | R1-1 | Both steps P < 0.05 (2); one step P < 0.05 (1);… | all | 59 | Table 1 rebuilt as a six-column, two-layer table (empirical criterion + proxy… |
| table 1 r7c3 | R1-1 | Cross-ancestry replication, direction-consistent… | all | 99 | Table 1 rebuilt as a six-column, two-layer table (empirical criterion + proxy… |
| table 1 r7c4 | R1-1 | — (binary gate) | all | 15 | Table 1 rebuilt as a six-column, two-layer table (empirical criterion + proxy… |
| table 1 r7c5 | R1-1 | No independent-ancestry replication, direction… | all | 111 | Table 1 rebuilt as a six-column, two-layer table (empirical criterion + proxy… |
| table 1 r7c6 | R1-1 | Independent-sample P < 0.05 with concordant… | all | 70 | Table 1 rebuilt as a six-column, two-layer table (empirical criterion + proxy… |
| table 2 r1c4 | R1-4 | Specificity (Grade D only) | partial | 26 | Specificity reported under both conventions, with intervals |
| table 2 r1c5 | R1-4 | Specificity (Grade C/D) | all | 23 | Specificity reported under both conventions, with intervals |
| table 2 r2c4 | R1-4 | 1.000 (0.999–1.000) | partial | 19 | Specificity reported under both conventions, with intervals |
| table 2 r2c5 | R1-4 | 1.000 (0.999–1.000) | all | 19 | Specificity reported under both conventions, with intervals |
| table 2 r3c3 | R1-2 | 0.216 (0.204–0.228) | all | 19 | Recomputed value: the benchmark was re-scored with the decisive-failure rule |
| table 2 r3c5 | R1-4 | — | all | 1 | Specificity reported under both conventions, with intervals |
| table 2 r4c3 | R1-2 | 0.878 (0.869–0.887) | all | 19 | Recomputed value: the benchmark was re-scored with the decisive-failure rule |
| table 2 r4c5 | R1-4 | — | all | 1 | Specificity reported under both conventions, with intervals |
| table 2 r5c4 | R1-4 | 0.796 (0.785–0.807) | partial | 19 | Specificity reported under both conventions, with intervals |
| table 2 r5c5 | R1-4 | 0.882 (0.873–0.891) | all | 19 | Specificity reported under both conventions, with intervals |
| table 2 r5c7 | R1-2 | 0.060–0.145 | all | 11 | Recomputed value: the benchmark was re-scored with the decisive-failure rule |
| table 2 r6c3 | R1-2 | 0.376 (0.362–0.389) | all | 19 | Recomputed value: the benchmark was re-scored with the decisive-failure rule |
| table 2 r6c5 | R1-4 | — | all | 1 | Specificity reported under both conventions, with intervals |
| table 2 r6c7 | R1-2 | 0.060–0.145 | all | 11 | Recomputed value: the benchmark was re-scored with the decisive-failure rule |
| table 2 r7c3 | R1-2 | 0.724 (0.711–0.736) | all | 19 | Recomputed value: the benchmark was re-scored with the decisive-failure rule |
| table 2 r7c5 | R1-4 | — | all | 1 | Specificity reported under both conventions, with intervals |
| table 2 r7c7 | R1-2 | 0.060–0.145 | all | 11 | Recomputed value: the benchmark was re-scored with the decisive-failure rule |
| table 2 r8c4 | R1-4 | 0.679 (0.666–0.692) | partial | 19 | Specificity reported under both conventions, with intervals |
| table 2 r8c5 | R1-4 | 0.809 (0.798–0.820) | all | 19 | Specificity reported under both conventions, with intervals |
| table 2 r8c7 | R1-2 | 0.102–0.200 | all | 11 | Recomputed value: the benchmark was re-scored with the decisive-failure rule |
| table 2 r9c3 | R1-2 | 0.408 (0.394–0.422) | all | 19 | Recomputed value: the benchmark was re-scored with the decisive-failure rule |
| table 2 r9c5 | R1-4 | — | all | 1 | Specificity reported under both conventions, with intervals |
| table 2 r9c7 | R1-2 | 0.102–0.200 | all | 11 | Recomputed value: the benchmark was re-scored with the decisive-failure rule |
| table 2 r10c3 | R1-2 | 0.691 (0.678–0.704) | all | 19 | Recomputed value: the benchmark was re-scored with the decisive-failure rule |
| table 2 r10c5 | R1-4 | — | all | 1 | Specificity reported under both conventions, with intervals |
| table 2 r10c7 | R1-2 | 0.102–0.200 | all | 11 | Recomputed value: the benchmark was re-scored with the decisive-failure rule |
| table 4 r4c3 | R3-4 | Perform LD clumping at r2 < 0.1 within 10,000 kb,… | partial | 251 | Table 4 step 3: clumping threshold corrected to r2 < 0.1 with the stricter tier as… |

## 3. Differences that do not answer a reviewer comment

| Category | Location | Chars | Text | Reason |
|---|---|---|---|---|
| conversion artefact / alignment | para 2 | 12 | 1 Department of Neurosurgery, The Fifth Affiliated Hospital of… | affiliation line: one whitespace character |
| conversion artefact / alignment | para 4 | 44 | Correspondence: Ming Luo, lm962272@gmail.com | correspondence line: escaped asterisk lost in conversion |
| journal/technical requirement | para 5 | 216 | Word count: 8,372 (Introduction through Conclusions, including… | first-page word/figure/table count required by the Frontiers author guidelines |
| journal/technical requirement | para 6 | 22 | Article type: Methods. | article type declaration required by the submission system |
| conversion artefact / alignment | para 21 | 1 | •  TwoSampleMR v0.7.9 (Hemani et al., 2018): instrument extraction,… | bullet glyph inserted by the markdown converter |
| conversion artefact / alignment | para 22 | 1 | •  MendelianRandomization v0.10.0: multivariable MR (MVMR) with… | bullet glyph inserted by the markdown converter |
| conversion artefact / alignment | para 23 | 1 | •  MRlap (Mounier and Kutalik, 2023): sample-overlap correction using… | bullet glyph inserted by the markdown converter |
| conversion artefact / alignment | para 24 | 1 | •  CAUSE v1.2.0 (Morrison et al., 2020): correlated-pleiotropy model… | bullet glyph inserted by the markdown converter |
| conversion artefact / alignment | para 25 | 1 | •  coloc (Giambartolomei et al., 2014): Bayesian colocalization… | bullet glyph inserted by the markdown converter |
| conversion artefact / alignment | para 26 | 1 | •  GenomicSEM v0.0.5 (Grotzinger et al., 2019) and LDSC… | bullet glyph inserted; $r_g$ rendered as r plus a subscript g, which is the same text in a different encoding |
| conversion artefact / alignment | para 27 | 1 | •  ieugwasr v1.1.0: LD clumping against the 1000 Genomes European… | bullet glyph inserted by the markdown converter |
| conversion artefact / alignment | para 28 | 1 | •  Additional data manipulation and Bayesian diagnostic utilities:… | bullet glyph inserted by the markdown converter |
| conversion artefact / alignment | para 51 | 2 | 1.  Harmonization (≈ 1.5 h). Extract instruments at P < 5 × 10-8;… | list number inserted; the Unicode superscript 10-8 rewritten as a formatted superscript run |
| conversion artefact / alignment | para 78 | 41 | Principal operational challenges include: | lead-in sentence split out of the preceding paragraph by the converter |
| conversion artefact / alignment | para 79 | 2 | 1.  MRlap covariance non-positive-definiteness under substantial… | list number inserted by the converter |
| conversion artefact / alignment | para 80 | 2 | 2.  CAUSE non-convergence with sparse variant panels: Relax… | list number inserted by the converter |
| conversion artefact / alignment | para 81 | 2 | 3.  Colocalization power loss from incomplete regional coverage:… | list number inserted by the converter |
| conversion artefact / alignment | para 82 | 2 | 4.  Conditional F-statistics < 10 in MVMR due to collinearity:… | list number inserted by the converter |
| conversion artefact / alignment | para 83 | 2 | 5.  Cross-ancestry inflation driven by LD mismatch: Re-clump summary… | list number inserted by the converter |
| journal/technical requirement | para 98 | 672 | Use of AI. Large language models (GLM and DeepSeek, accessed through… | AI-use declaration: the version number was dropped, and the statement was widened from 'language editing only, no AI used to analyse data or generate results' to disclose that the models also re-executed and cross-checked computations and rebuilt the S8 scoring table. That widening corrects a claim which had become untrue rather than answering a comment, so it is filed here under the disclosure policy and is NOT highlighted - but it is a substantive correction, not a style edit |
| journal/technical requirement | para 144 | 115 | Figure 1. The six-gate falsification framework. (A) Six falsification… | Figure 1 legend: note on the 180 mm width and the generator script; journal figure specification, not a reviewer request |
| journal/technical requirement | para 146 | 497 | Figure 3. Case study MR results (insomnia–AD). (A) Key MR estimates… | Figure 3 legend: expanded panel description after the figure was redrawn for the 180 mm specification |
| journal/technical requirement | para 147 | 573 | Figure 4. APOE-locus shared liability. (A) Cross-trait LDSC genetic… | Figure 4 legend: expanded panel description after the figure was redrawn for the 180 mm specification |
| journal/technical requirement | para 148 | 326 | Figure 5. Validation cohort under the revised scoring: per-gate… | Figure 5 legend: expanded panel description after the figure was redrawn for the 180 mm specification |

Journal/technical items are required by the Frontiers author guidelines or the submission system; they are not answers to a comment and are therefore not highlighted. Conversion artefacts are listed so that nobody mistakes them for editorial changes.

## 4. Deleted text

1 paragraph(s) present in the submitted version and absent from the revision, listed in `manuscript_Frontiers_Methods_v2_marked_deletions.md`. Deletions are not visible in a highlight-only copy; a tracked-changes copy would show them.

## 5. Notes from building the map

1. R1-6 is now answered in two places. The Results G3 paragraph carries the region definition and the withdrawal of the chromosome-19 exclusion; the Discussion paragraph 'The APOE result' restates the region boundary, why no MR exclusion isolates it, and that no APOE-specific effect estimate is drawn, so the Changes line in the response letter ('Results, G3 paragraph; Discussion') is now true of the manuscript.
2. The earlier note that the converter flattened superscripts was wrong, and the error came from reading paragraph.text, which concatenates run text without formatting. The built .docx carries 45 superscript and 12 subscript runs in the same places as the source ($r^2$, $r_g$, $10^{-8}$ and so on); the flattened appearance is a limitation of plain-text preview, not of the file. Any future audit of typography has to inspect font.superscript in the runs or w:vertAlign in document.xml, never the concatenated string. The one place the source still uses a Unicode superscript (5x10-8 in the Introduction) is unchanged from the submitted version and was deliberately left alone.
3. Table 1 (4 to 6 columns) and Table 2 (6 to 7 columns) are attributed to the comments that asked for the restructure, R1-1 and R1-4. In Table 2 the value columns are attributed to R1-2 instead, because the numbers moved when the benchmark was re-scored with the decisive-failure rule.
4. R3-12 leaves no highlighted text: it is satisfied by the three-line cell borders that md_to_docx_frontiers.py already draws, which this build checks on all five tables rather than re-applies.
5. The two Discussion paragraphs now headed 'Complementarity with reporting standards' and 'Generalizability of the template' were previously filed as editorial (ED) because the run-in headings were not requested verbatim by any reviewer. They are now filed under REV, and the reasoning is worth stating rather than burying. R1-3 asks what the full framework adds beyond routine practice; the answer the manuscript gives is exactly the content of these two paragraphs - that the framework complements a reporting standard instead of duplicating it, and that the template is not tied to this locus or trait pair - so leaving them unlabelled buried the answer to a question the reviewer had asked. The revision did not only add labels: the generalizability paragraph now carries the deposited release DOI that R1-2 forced (10.5281/zenodo.23733172 in place of the superseded 21858125) and states the renv.lock pinning, and the reporting-standard paragraph now cites STROBE-MR and points at the completed checklist in Supplementary Table S5, which the submitted version did not signpost at all. Both Changes lines in the response letter were corrected to name these locations. A reader who still regards the headings themselves as cosmetic can revert the two bolded lead-ins without touching any answer, because the sentences beneath them are unchanged in substance.

