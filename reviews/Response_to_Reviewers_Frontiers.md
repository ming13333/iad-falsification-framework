# Response to Reviewers

**Manuscript:** A six-gate falsification framework for locus-driven confounding in Mendelian randomization
**Journal:** Frontiers in Genetics
**Manuscript ID:** 1986036

We thank both reviewers for detailed and technically substantive reports. The revision is not a rewriting exercise: four analyses were re-run or newly computed, one scoring rule was tightened in a way that changes a published grade, one previously awarded point was withdrawn, and two new supplementary tables were added. We state below, for each comment, whether we accepted it in full, accepted it in part, or declined it with reasons.

## Summary of the major changes

1. **One scoring table, one rubric file.** The 0/1/2 tiers, the binary gates, decisive-failure rules, and the rule for unavailable or underpowered analyses are now specified in a single place (Table 1, two layers: empirical criterion and proxy implementation) and in `rubric_spec_v3.csv`. Earlier, mutually inconsistent descriptions have been withdrawn. The stability of the remaining design choices — the band boundaries and the cap — is now quantified rather than asserted (Supplementary Table S12).
2. **Decisive-failure rule added.** Failing G2 now caps the total at 6, so a claim that does not survive clumping, overlap correction and pleiotropy diagnostics can no longer reach Grade A through the additive total. This closes the logical gap the reviewer identified. It changes no grade in the cohort (only Insomnia→AD fails G2, and it was already Grade C).
3. **The simulation is now described as what it is, and scored as the rule says.** The Methods state the actual data-generating process: instruments drawn independently (no inter-instrument LD), G3 implemented as block coverage and G4 as leave-one-out stability, and LDSC, colocalization, MVMR, CAUSE and MRlap not instantiated at all. The conclusions drawn from the benchmark are narrowed accordingly. The benchmark has also been re-run with the decisive-failure cap, which the published rule requires and the archived script never applied; this lowers the reported sensitivity and raises the reported FDR (Table 2; Supplementary Table S12.5).
4. **Two empirical analyses replace what the simulation cannot do.** A three-tier instrument sensitivity table (unclumped → r²<0.1 → r²<0.001) now quantifies what LD correction changes, including a 6.5- to 7.5-fold inflation of the standard error. A leave-one-gate-out ablation over the 12-case cohort now shows the contribution of each gate (Supplementary Tables S10, S11).
5. **Consistent operating-characteristic definitions with uncertainty.** Specificity is reported under both conventions (Grade D only, and Grade C+D), sensitivity and both specificity columns carry 95% Wilson intervals, the 0.20 FDR threshold is justified, and the dependence of FDR on the proportion of true nulls is quantified.
6. **One published grade changed, and every score that moved is accounted for.** The cap in point 2 changes no grade in this cohort; the G6 withdrawal does. Four cases had been awarded G6 points on evidence that does not support them, and all four lose 2 points. Education→AD rested on a replication that was null (P = 0.85) at achieved power ≥ 84%; direction concordance without replication is not validation. LDL→CAD and BMI→T2D rested on no cross-ancestry or independent-cohort record at all — the archive holds none — which is the same failure in its barest form. All three keep 12 → 10 and remain Grade A. Height→CAD falls from Grade A (10 points) to Grade B (8) on the same ground and is the only grade crossing in the cohort; it had been accepted in the submitted version as a genuine protective effect. HDL→CAD loses the single G6 point it held (6 → 5) but stays in Grade C. Three further cases scored 1 at G1 under the old rule and now score 0, because G1 is binary; none of them changes grade. Every one of these revisions is itemised in Table S8, which reports the submitted score (`score_v1`), the difference (`delta`) and whether the grade moved (`grade_changed`) for all twelve cases: eight of the twelve moved, and all eight are named here.
7. **Transparency additions.** Conditional F-statistics were not retrieved from the archived MVMR fits and are now declared as a reporting gap rather than implied to exist; the 10 of 12 cases whose GWAS are not held locally are identified as re-scorings of published evidence; the CAUSE and MRlap inputs are stated exactly (15,564 variants at P < 1e-3 and the full shared-variant set, respectively — neither is the clumped set, as previously implied).

### Table R1. Disposition of every comment

| Comment | Topic | Disposition | Where the revision answers it |
|---|---|---|---|
| R1-1 | Inconsistent scoring rules; G2 failure could still reach Grade A | Accepted in full | Table 1; Methods, *Grading rubric*; Tables S8, S12 |
| R1-2 | Archived simulation code differs from the described workflow | Accepted in full | Methods, *Simulation*; Table 2; Tables S9, S12.5; Title |
| R1-3 | What the framework adds beyond routine LD handling | Accepted in part | Tables S10, S11; Results, *What LD correction changes*; Limitations |
| R1-4 | Sensitivity/specificity definitions; the 0.20 threshold; effect mix | Accepted in full | Table 2; Results, *Operating characteristics*; Limitations |
| R1-5 | Insufficient evidence is not evidence against the claim | Accepted in full | Results, *Insufficient evidence versus evidence against*; Limitations |
| R1-6 | Chromosome 19 is not the APOE region; region definition | Accepted in full | Results, G3 paragraph; Discussion |
| R1-7 | "Three null results" contradicts a negative direct effect; CAUSE inputs | Accepted in full | Results, G2 paragraph; Methods, *What each correction operates on*; Table 1 footnote |
| R1-8 | Conditional instrument strength; mediation detail | Accepted in full (one gap declared) | Results, G4 and G5 paragraphs; Methods, *G4*; Limitations |
| R1-9 | Evidence behind the G6 scores; κ is not causal accuracy | Accepted in full | Results, G6 paragraph; Table S8; `code/scoring_reproducibility.py` |
| R1-10 | From risk factors to drug targets | Accepted in full | Discussion, *Implications for drug-target prioritization* |
| R3-1 | Harmonise terminology for directional and causal claims | Accepted in full | Methods, *Terminology*; Abstract |
| R3-2 | What "precise" means | Accepted in full | Abstract; Results, *What LD correction changes* |
| R3-3 | European LD panel applied to East Asian data | Accepted in full | Methods, *Trans-ethnic re-clumping*; Results, G6 paragraph; Limitations |
| R3-4 | Rationale for r² < 0.001 with a 10,000-kb window | Accepted in part; Methods corrected | Methods, *G2* (threshold corrected to r² < 0.1); Table S11 |
| R3-5 | Whether the three corrections act in sequence on the variant set | Accepted in full | Methods, *What each correction operates on* |
| R3-6 | Confounder selection; why F > 10 sits at G4 | Accepted in full | Methods, *G4* |
| R3-7 | Power comparability and bias across ancestries | Accepted in full | Results, G6 paragraph; Methods, *Trans-ethnic re-clumping*; Limitations |
| R3-8 | Where MR-Egger, Cochran's Q, MRlap and CAUSE sit | Accepted in full | Methods, *What each correction operates on*; Table 1 footnote |
| R3-9 | Justification of the simulation parameter grid | Accepted in full | Methods, *Simulation* |
| R3-10 | Definition and algorithm of trans-ethnic re-clumping | Accepted in full | Methods, *Trans-ethnic re-clumping* |
| R3-11 | Do not describe a null r_g as "unchanged" | Accepted in full | Results, G3 paragraph |
| R3-12 | Three-line tables without vertical rules | Accepted in full | Tables 1–5; all sheets of `Supplementary_Tables.xlsx` |

Two comments are accepted in part. R1-3 asks for a three-way comparison on simulated data, which the benchmark's data-generating process cannot support: instruments are drawn independently, so LD-adjusted and unadjusted IVW are the same estimator there, and delivering the comparison would mean replacing the simulation rather than revising it. We substituted the empirical analyses the comment's logic implies (Tables S10, S11) and removed the implication that the simulation speaks to LD correction. R3-4 asks for a principled justification of r² < 0.001 with a 10,000-kb window; the comment led us to find and correct a description error in the Methods, which stated the primary clumping tier as r² < 0.001 when the reported estimate came from r² < 0.1, and we can show that the verdict does not depend on the setting but cannot derive the setting from a principle, and we say so. No comment is declined.

---

# Reviewer 1

## R1-1 — Inconsistent scoring rules; G2 failure could still yield Grade A

> *The scoring rules differ across the text, Table 1, Figure 1 and Table S8: some allow only 0 or 2 points, while others also use 1 point. The education-T2D score of 9 therefore needs explanation. Also, failure at G2 could still produce Grade A under the additive rule. Please provide one consistent scoring table covering partial scores, decisive failures, conflicting results and unavailable or underpowered analyses.*

**Response: accepted in full.** The reviewer is correct on all three counts, and the third is a genuine design flaw rather than a reporting error.

*Partial scores.* The 0/1/2 tiers existed in the scoring code but were described in the text as 0/2 only. We have adopted the three-tier scheme as the published rule, with the two exceptions stated explicitly: G1 and G6 are binary, because a screening test and a directional external screen cannot support partial credit in a defensible way. The education–T2D score of 9 is therefore 2 (G1) + 1 (G2: clumped IVW significant but one diagnostic failed) + 2 (G3) + 1 (G4) + 1 (G5) + 2 (G6). Making G1 binary also removes the single point it previously carried in three cases (CRP→CAD, BMI→AD, T2D→AD); each falls from 1 to 0 and stays in Grade D, so no grade moves. Table S8 reports the submitted score, the difference and any grade change for every case, so the effect of each rubric decision can be read off directly rather than inferred.

*Decisive failures.* Failure at G2 now caps the total at 6, the upper bound of Grade C. The reasoning is the framework's own: a claim that does not survive LD clumping, sample-overlap correction and pleiotropy diagnostics is falsified on robustness grounds, and an additive total must not be able to promote a robustness failure to Grade A. The rule is implemented in the scoring script, applied in Supplementary Table S8, and declared in Table 1 and the Methods. It changes no grade in the current cohort, because the only case failing G2 (Insomnia→AD, total 4) was already Grade C. It is not inert outside the cohort, however: applying it to the 43,200-replicate benchmark regrades 10.1% of replicates from B to C, and the benchmark had not been scoring with it. That inconsistency, found while checking this comment, is corrected in Table 2, Supplementary Table S9 and Figure 2, and its quantitative effect is given in Supplementary Table S12.5 and under R1-2.

*Conflicting results.* Where methods disagree, the gate scores on its primary criterion and the disagreement is recorded rather than averaged. The clearest instance is CAUSE, which returns a boundary forward CAUSAL classification while clumped IVW, MRlap and the MVMR direct effect do not support the claim. CAUSE and MRlap are diagnostics that do not contribute points independently; the conflict is reported in the case narrative.

*Unavailable or underpowered analyses.* The rule is "not evaluable scores 0", stated per gate in `rubric_spec_v3.csv`: fewer than three independent instruments (G2); neither LDSC nor colocalization runnable (G3), noting that absent colocalization alone scores 1 rather than 0; conditional F ≤ 10 or no estimable model (G4); no mediator surviving instrument filtering (G5); power < 80% or no independent-ancestry data (G6).

*Cut-off values.* Unifying the rubric exposes the next question — why 10, 7 and 4 — and we answer it with numbers rather than with an appeal to convention, because the band boundaries are our own design choice and not an inherited standard. Supplementary Table S12 reports three analyses. Moving any single parameter by one point while holding the others reverses the polarity (A/B versus C/D) of no case in the cohort; the three Grade A cases would drop to Grade B if the A boundary moved to 11, the three cases scoring 5 would rise to Grade B only if the B boundary moved to 5, and the primary case would move from C to D only if the C boundary moved to 5 (Table S12.1). Enumerating all 220 monotone four-band partitions of the 0–12 scale, the primary case (score 4) keeps its negative call under 89% of the non-degenerate partitions and requires the A/B boundary to move three points before it changes side (Table S12.2). Finally, the three boundaries sit on the benchmark's own ROC at false-positive rates of 3.6%, 10.3% and 17.5%, so each is a nested false-positive level rather than an isolated number (Table S12.4). That correspondence was checked after the reviewer raised the point and is not how the cut-offs were originally set; we do not claim otherwise. The decisive-failure cap cannot bind in this cohort — no case both fails G2 and exceeds 6 — so its position follows from its definition as the upper bound of Grade C rather than from these data (Table S12.3). We therefore treat the total score as the datum and the band as a label: both are reported for every case, and assignments within one point of a boundary are flagged as provisional.

**Changes:** Table 1 rewritten as a six-column, two-layer table; Methods scoring paragraph; Supplementary Table S8 (new `decisive_failure` column and footnotes 6–7); `rubric_spec_v3.csv` (new, supersedes all earlier rubric files); new Supplementary Table S12 and `code/threshold_robustness.py`; Limitations (Fifth, revised to cite the perturbation counts).

## R1-2 — Archived simulation code differs from the described workflow

> *The simulation script in the cited Zenodo archive differs from the described workflow. G3 uses block coverage and G4 uses leave-one-out variation instead of LDSC/colocalization and MVMR; CAUSE/MRlap and the G6 power check are absent. The code also does not generate the described LD covariance or correlated exposure-outcome errors, and adds outcome noise with SD 0.01 while supplying SE 0.03. Mediator values depend on the true effect but do not generate the outcome. Please confirm the code version used and describe the actual simulation procedure in the Methods, explaining these differences. If they affect the performance results, please update those results.*

**Response: accepted in full.** This is the most serious comment in the report. We verified each item against the archived code and report what we found rather than what we intended; one item turned out to describe the code inaccurately, and we set out the correction under (iv).

*Code version.* The version DOI cited in the submitted manuscript (10.5281/zenodo.21858125) points to release v1.0.0 (9 August 2026), whose simulation script corresponds to commit `b983865` (6 August). The version used for the submitted results corresponds to commit `3225fea` (2 September), which differs from the archived script by one aggregation fix in the marginal summary. The archived release was therefore older than the results it is cited for, and a reader who runs it will not reproduce the published marginal figures. Release v1.2.1 has now been deposited (DOI 10.5281/zenodo.23733172, GitHub tag `v1.2.1`); it contains the scoring rule as published in this revision, reproduces Table 2 digit for digit from the deposited script, and every DOI reference in the manuscript now points to it. Its `MANIFEST_sha256.csv` lets a reader confirm that their copy and their re-run match the archive.

*Discrepancies, item by item.* (i) G3 in the simulation is block coverage, not LDSC plus colocalization. (ii) G4 is leave-one-out stability of the clumped IVW estimate, not multivariable MR with confounders. (iii) CAUSE, MRlap and the G6 power check are absent: they require external genomic reference resources and cannot be instantiated in a simulated setting. (iv) Two claims are bundled here and they have different fates. No LD covariance is generated: instrument effects are drawn independently, so the simulation contains no inter-instrument LD at all. Correlated exposure–outcome errors, however, are generated: sample overlap was implemented exactly as a correlated residual, `e_y = overlap × e_x + sqrt(1 − overlap²) × e_y` at 0% and 30% overlap, so this half of the comment does not hold. The Methods now state the two levels separately so that instrument-level independence and sample-level correlation cannot be read as contradicting each other. The block partition enters only through the clumping step, which retains the strongest variant per block. We had described "LD blocks simulated from block-diagonal correlation matrices", which is not what the code does, and that sentence has been removed. (v) Outcome noise is added with SD 0.01 while SEs of 0.03 are supplied; the two are not consistent, and the simulation is therefore not calibrated to a realistic sampling variance. (vi) Mediator values are generated from the true effect but do not in turn generate the outcome, so the mediation path is imposed rather than propagated.

*Consequences for the results.* Two further properties, which we had not previously reported, follow from the same design and we state them in the Methods, the Table 1 and Table 2 footnotes, and the Limitations. G3 is fully determined by G1 in the benchmark (G3 = 2 in 100% of replicates with G1 > 0), and G4 agrees with G2 in 99.1% of replicates. The 43,200-replicate benchmark therefore evaluates the mapping from four gate signals (G1, G2, G5, G6) onto the 0–12 scale, not six.

Checking the archived code against the published rule exposed a second, unrelated defect that we report rather than leave for a third reviewer. The benchmark applied the plain additive total and never applied the decisive-failure cap introduced in R1-1, so Table 2 as submitted described a rule the manuscript no longer uses. Applying the cap regrades 4,363 of 43,200 replicates, all from Grade B to Grade C and all with a true non-zero effect: marginal sensitivity at β = 0.15 falls from 0.973 to 0.878 without pleiotropy, from 0.847 to 0.724 under balanced pleiotropy and from 0.804 to 0.691 under directional pleiotropy, while specificity and the Grade A frequency are unchanged because the cap can only remove B calls. Table 2, Supplementary Table S9 and Figure 2 have been recomputed with the cap, and the before/after comparison is in Supplementary Table S12.5. The per-cell estimates are now reproduced digit for digit by the deposited script; they are not the estimates in the submitted version, and we have not pretended otherwise. The claim that the benchmark characterises "the framework" has been narrowed throughout to "the scoring rule under proxy gate implementations", including in the abstract, Results, Discussion and Conclusions. The title has been changed in this revision rather than deferred. It now reads: *"A six-gate falsification framework for diagnosing locus-driven confounding in Mendelian randomization: architecture, a 43,200-replicate benchmark of its scoring rule, and application to complex traits"*. Two words were changed. "43,200-simulation validation" became "a 43,200-replicate benchmark of its scoring rule", because the benchmark scores a rule under proxy gates and validates no genomic estimator. "Correcting" became "diagnosing", because the framework does not adjust or remove confounding: it detects locus-driven confounding and regrades the claim that it produced, and a reader who expected a correction procedure would have been misled by the verb. The short form used in correspondence and figure legends is unchanged. We do not claim, and no longer imply, that the simulation validates LDSC, colocalization, MVMR, CAUSE or MRlap.

**Changes:** Title (both clauses revised — see above); Methods (simulation section rewritten, including the independence of instrument effects and the G3/G4 degeneracy); Abstract; Results; Discussion; Limitations ("Second" and "Seventh"); Table 1 and Table 2 footnotes; new `code/sim_marginal_fdr.py`, `code/make_table2_uncertainty.py`, `code/build_manifest.py`; `requirements.txt`; archived release v1.2.1 (DOI 10.5281/zenodo.23733172).

## R1-3 — What does the framework add beyond routine LD handling? Compare on the same simulated datasets

> *Please compare correctly LD-adjusted IVW, a conventional MR workflow with specified robustness analyses, and the complete six-gate framework on the same simulated datasets. State the rules for each approach and compare both false positives and missed true effects. Adding gates sequentially or removing one at a time would also help show the contribution of each gate.*

**Response: accepted in part; the first half cannot be delivered as specified, and we say so rather than substituting something that looks like it.**

*Why the three-way simulation comparison is not possible.* The benchmark draws instrument effects independently, so there is no inter-instrument LD in the simulated data. A "correctly LD-adjusted IVW" and an "unadjusted IVW" are therefore the same estimator on these data: clumping can only remove arbitrary blocks, not correlated variants, and no difference between the three arms can arise. Delivering the requested comparison would require rebuilding the data-generating process with a real LD reference panel, MVMR with confounders, LDSC and colocalization — that is, replacing the simulation rather than revising it. We have not done this, and we have removed the implication that the simulation speaks to LD correction at all.

*What we did instead — empirical, on the reviewer's own logic.* (a) **Three instrument tiers on the real data** (Supplementary Table S11). Unclumped: β = +0.104, SE = 0.031, 2,462 variants. After clumping at r² < 0.1: β = −0.130, SE = 0.203, 54 variants (SE 6.5-fold larger). At r² < 0.001: β = −0.111, SE = 0.236, 37 variants (SE 7.5-fold larger). This is what LD correction changes: it does not merely attenuate the coefficient. Clumping also changed the instrument set, so the SE ratio does not by itself identify the sampling variance of the original set; what is unambiguous is that the apparent significance of the unclumped estimate (P = 9.3 × 10⁻⁴) does not survive at Gate G2. (b) **Leave-one-gate-out ablation across the 12-case cohort** (Supplementary Table S10, 72 rows), which is exactly the second analysis the reviewer suggested. Removing a single gate changes at most 7 of 12 grades; the per-gate counts are G1 7/12, G2 3/12, G3 4/12, G4 4/12, G5 3/12, G6 0/12. No gate carries the verdict alone.

*Statement of the rules.* The rules for the framework are in Table 1 and `rubric_spec_v3.csv`. We do not state rules for the two comparator arms, because we did not run them, and inventing rules for analyses we did not perform would repeat the error this revision is correcting.

**Changes:** new Supplementary Table S11; new Supplementary Table S10; new Results subsection "What LD correction changes: precision, not only direction"; Methods (G2, instrument-tier reporting); Limitations (the benchmark cannot quantify the benefit of LD clumping).

## R1-4 — Sensitivity/specificity definitions; Grade C; uncertainty; the 0.20 threshold; effect-mix dependence

> *Sensitivity treats A/B as positive, but specificity counts only D as a correct negative. How is Grade C handled? If A/B is positive and C/D is negative, specificity should include both C and D. Please use consistent definitions for sensitivity, specificity, false-positive rate and FDR, and report their uncertainty. Also explain the 0.20 threshold in the Results and how the simulated mix of true and null effects affects FDR.*

**Response: accepted in full.** The asymmetry was a genuine inconsistency: a Grade C verdict asserts that no directed causal effect is supported, which is a negative call, yet it was excluded from specificity.

*Both conventions now reported.* Specificity (Grade D only) is 1.000 / 0.796 / 0.679 across the three pleiotropy regimes. Specificity (Grade C+D) is 1.000 / 0.882 / 0.809. We state that the framework's operating claim refers to the C/D convention, since a Grade C case asserts no directed effect, and that the D-only column is retained for comparability with binary screens.

*Uncertainty.* Sensitivity and both specificity columns in Table 2 now carry 95% Wilson score intervals computed on the pooled 4,800 replicates per row (for example, balanced specificity C/D = 0.882, 95% CI 0.873–0.891). P(Grade A) is reported as a point estimate and empirical FDR as the range across the 12 parameter cells, because neither is a frequency over the pooled set. Per-cell values remain in Supplementary Table S9.

*The 0.20 threshold.* It is now justified in the Results rather than asserted: 0.20 is a pre-specified tolerance for a triage instrument rather than a confirmatory test, four times the conventional 0.05 because a Grade A/B verdict is intended to trigger the gate-specific analyses it summarises, not to license a causal conclusion.

*Dependence on the effect mix.* FDR is not a fixed property of the rule. The published figures assume one-third nulls. Re-weighting the same per-cell estimates to a one-half null mixture gives 0.18 under balanced pleiotropy and 0.26 under directional pleiotropy — the latter exceeding the 0.20 tolerance. This is now stated in the Results and the Limitations, with the full sensitivity table deposited.

*Recomputation note.* Table 2 in this revision differs from the submitted version not only by the added column and intervals. While unifying the rubric (R1-1) we found that the archived benchmark had never applied the decisive-failure cap; applying it lowers the sensitivity column and raises the FDR column, leaving specificity and P(Grade A) unchanged. The full before/after comparison is in Supplementary Table S12.5 and the reasoning is given under R1-1 and R1-2.

**Changes:** Table 2 (new column, intervals, rewritten footnote, sensitivity and FDR columns recomputed with the decisive-failure cap); Figure 2 regenerated by `code/make_fig2_simulation.py`; Results (simulation paragraph); Limitations ("Fourth"); new `code/make_table2_uncertainty.py`, `code/make_s9.py` and `fdr_null_fraction_sensitivity.csv`.

## R1-5 — Insufficient evidence is not evidence against

> *The clumped insomnia-AD estimate has an approximate 95% confidence interval of -0.528 to 0.268, which includes the positive effect of 0.10 discussed in the paper. Power to detect that effect is only 24%, and the East Asian analysis has less than 6% power. These findings do not exclude a smaller causal effect. Please distinguish insufficient evidence from evidence against a claim.*

**Response: accepted in full.** This distinction is central to the framework's validity and it was not made explicitly enough.

We have added a dedicated passage stating the criterion: the two are separated by direction and by convergence across gates, not by the P value of any single estimate. On the reviewer's own numbers, the clumped null alone establishes only that this dataset cannot resolve an effect of size 0.10 — the 95% CI of −0.53 to 0.27 excludes neither zero nor the originally proposed effect, and the East Asian screen at < 6% power is weaker still. What raises the verdict above non-resolution is the conjunction of four observations: the point estimate changes sign after clumping (+0.104 to −0.130); the forward genetic architecture is null while the reverse direction yields 18 loci with PP.H4 ≥ 0.80; the MVMR direct effect is negative (β = −0.57, P = 0.045); and no protein mediator survives correction. Underpowering lowers resolution rather than biasing an estimate towards zero, so a single sign reversal is weak evidence on its own; what underpowering does not produce is locus-specific colocalization concentrated in the opposite direction.

We also state the limit of the claim: Grade C asserts that no directed causal upstream is supported by these data, not that the true effect is exactly zero, and a small effect below the detection limit remains compatible with the evidence.

**Changes:** new Results subsection "Insufficient evidence versus evidence against"; Limitations ("Third"); G6 scoring rule (a null replication now scores 0 rather than 2 — see R1-9).

## R1-6 — Chromosome 19 is not the APOE region; region definition; how 32 and 47 were selected

> *On PDF p. 12, the authors use removal of 118 chromosome-19 instruments to assess the influence of APOE. Please explicitly state that APOE lies on chromosome 19 ... it is not an APOE-specific exclusion ... If attributing the MR result to APOE, define the region and compare results with and without it using the same LD-handling settings. Explain how this evidence and colocalization support Grade C. Also clarify how the 32 reverse and 47 forward regions were selected and whether they overlap; colocalization alone does not establish causal direction.*

**Response: accepted in full.** All four sub-points required changes to the text, and the first required us to withdraw an implication.

*APOE is on chromosome 19, and the exclusion is not APOE-specific.* The text now states that APOE lies at 19q13.32, that excluding chromosome 19 removes the whole chromosome rather than the APOE region, and that we therefore make no APOE-specific claim from that analysis. The persistence of the unclumped association without chromosome 19 (β = 0.094, P = 0.003) is reported as showing only that the unclumped signal is not confined to chromosome 19.

*Region definition.* We now define the APOE region explicitly as GRCh37 chr19:45.06–45.82 Mb. Within it, 16 of the 18 reverse-direction colocalization signals fall, at PP.H4 > 0.98; the remaining two lie at chr11p11.2. We have not performed the matched LD-handling comparison the reviewer suggests (same clumping settings with and without the region), because the clumped instrument set contains only 54 variants and removing the APOE-region variants from it leaves too few for a stable estimate. We say so rather than presenting an underpowered comparison as if it were informative.

*How the 32 and 47 regions were selected, and whether they overlap.* Windows were built around LD-independent lead variants in each trait: 47 insomnia leads tested against AD windows (forward), and 32 AD leads tested against insomnia windows (reverse). The two lead sets share no variant, so the scans are disjoint rather than re-classifications of the same regions. This is now stated in the Results.

*Colocalization does not establish direction.* We agree and have said so: colocalization identifies a shared causal variant for the two traits. The directional reading rests on the conjunction of the colocalization asymmetry, the null forward LDSC and the clumped MR results, not on colocalization alone.

**Changes:** Results G3 paragraph (rewritten); Discussion; no new analysis claimed.

## R1-7 — "Three null results" is inconsistent with a nominally negative direct effect; CAUSE inputs

> *This estimate is nominally significant and points in the opposite direction, so calling all three results null is inconsistent. Please use wording such as "none of the three analyses supported the original positive causal hypothesis" and describe nonsignificant and opposite-direction results separately. Also explain why the forward CAUSE results (P = 0.039 and 0.002) are called borderline and how the disagreement affects scoring. Clarify the CAUSE/MRlap inputs and main settings, the reference to extending an MCMC chain, and any effect-unit conversions.*

**Response: accepted in full.** The inconsistency was ours, and checking the inputs as requested exposed a further error in the text.

*Wording.* The sentence now reads that CAUSE disagrees with three analyses "that did not support the original positive hypothesis", with the two null results (clumped IVW P = 0.52; MRlap P = 0.43) and the nominally negative direct effect (P = 0.045) described separately rather than pooled as "null".

*CAUSE inputs — a correction.* The text previously said CAUSE was fitted "on the clumped instrument sets". That is wrong. CAUSE used the 15,564 variants passing its exposure pre-filter at P < 1e-3, with 1,000 MCMC samples; it was never restricted to the clumped 54. MRlap likewise used the full shared-variant set and performed its own internal LD pruning. The Methods now state what each method operated on, and a new paragraph makes the general point: only clumping changes the instrument set; MR-Egger, Cochran's Q, the weighted median and the mode-based estimator are post-estimation diagnostics computed on the clumped set and remove nothing.

*Why the forward CAUSE result is called borderline and how it affects scoring.* The Kunkle classification (P = 0.039) sits immediately below the 0.05 boundary, and the Bellenguez classification (P = 0.002) comes from an AD source with extreme heterogeneity in related analyses (Cochran Q P = 1.7 × 10⁻¹¹), which makes its estimates unreliable. CAUSE does not contribute points to G2 independently; the conflict is recorded in the case report and does not alter the gate score. This is now stated in the Table 1 footnote so that a reader cannot mistake the CAUSE label for a scoring input.

*MCMC chain and effect units.* The "extending an MCMC chain" reference is a troubleshooting recommendation, not something we did for the primary analysis; the primary fit used the default chain with 1,000 samples. No effect-unit conversion was applied: all estimates are on the log-odds scale per standard deviation of genetically predicted exposure, and beta coefficients are reported untransformed.

**Changes:** Results G2 paragraph; Methods (G2, new paragraph "What each correction operates on"); Table 1 footnote.

## R1-8 — Conditional instrument strength; confounder handling; mediation details

> *The total effect and the effect remaining after adjustment answer different questions. Report conditional instrument strength and how correlated estimates and SNPs were handled. For mediation, clarify the 36-versus-25 protein counts, both path estimates, multiple-testing correction and the calculation of 9% triglyceride mediation. Finding no mediator among the 25 proteins analysed does not rule out mediation through other proteins or pathways.*

**Response: accepted in full, with one gap declared rather than papered over.**

*Conditional instrument strength — a reporting gap, stated as such.* We re-examined the archived MVMR output and found that conditional F-statistics were never extracted: the MVIVW fit object did not supply the conditional-F slot, and the archived table records NA in that column for all 28 model rows. We could not recompute them, because the harmonised multivariable input matrices were not retained and the upstream API is no longer reachable from our environment. The text therefore states plainly that conditional F was not retrieved, that G4 scores in the validation cohort rest on the significance and direction of the direct effects rather than on a verified conditional-strength threshold, and that this is a reporting gap rather than a computational failure. Instrument strength is documented instead by the first-stage statistics (R² = 0.0022; mean F = 44.3, minimum 29.8) and by the variant counts of each fitted model (44 loose-clump; 29–31 tight-clump).

*Correlated estimates and SNPs.* The four exposures were fitted jointly in a single multivariable model rather than by pooling separate univariable estimates, so their correlation is absorbed by the joint estimation. Variants were clumped before the joint fit, so the model's variant set is LD-independent by construction.

*36 versus 25.* The 25 evaluable proteins are those with at least three independent cis-pQTLs after clumping at r² < 0.001; the 11 excluded proteins failed that threshold a priori. The rule and the excluded set are recorded in the archived screening output, and the text now states both the rule and the consequence: absence of mediation among 25 proteins does not exclude mediation through other proteins or pathways, and the gate scores the panel tested rather than the pathway as a whole.

*Both path estimates and the 9% figure.* Education→triglycerides: β = −0.183 (SE 0.019, P = 2.5 × 10⁻²²). Triglycerides→AD: β = +0.169 (SE 0.038, P = 9.7 × 10⁻⁶). Indirect effect −0.031 (SE 0.008, q = 5.7 × 10⁻⁴; bootstrap 95% CI −0.047 to −0.017). The mediation fraction is the indirect effect divided by the univariable total effect of education on AD (β = −0.328, P = 1.1 × 10⁻⁵), giving 9.5%; the text previously said 9% without showing the denominator, and now shows it. Multiple testing across the ten metabolites used Benjamini–Hochberg on the indirect-effect P values.

**Changes:** Results G4 and G5 paragraphs; Methods (G4); Limitations ("Seventh").

## R1-9 — Evidence behind the external-validation scores; κ is not causal accuracy

> *Please identify the evidence behind the external-validation scores. The text reports East Asian education-T2D results, while S8 gives education-AD full validation points. A fully worked Grade A example would help explain the framework. For all 12 cases, clarify the reference labels and supporting gate results; Cohen's κ measures rater agreement, not causal accuracy.*

**Response: accepted in full, and the specific discrepancy the reviewer found has led us to withdraw a point.**

*The education–AD discrepancy.* The reviewer is right that the text reported education→T2D while the table awarded education→AD full validation points. On checking, the East Asian replication of education→AD was β = −0.029 with P = 0.85 at achieved power ≥ 84%. A replication powered to detect the claimed effect that returns no effect has not replicated it. Direction concordance alone is not external validation, so the point has been withdrawn: G6 is now 0 for this case, the score falls from 12 to 10, and the grade remains A. The G6 criterion has been rewritten accordingly (direction consistent **and** nominally significant at power ≥ 80%), and the East Asian education→AD result is now reported in the Results so that the reader can see the evidence that produced the score. Applying the same criterion to the rest of the cohort withdraws three further point-bearing scores. LDL→CAD and BMI→T2D each held 2 points at G6 on no cross-ancestry or independent-cohort record that the archive can produce; both lose the two points and go from 12 to 10 without leaving Grade A. Height→CAD held 2 points on the same absent basis, loses both, and falls from Grade A (10) to Grade B (8) — the only grade crossing produced by the revision. We state all three here because the reviewer's question about the evidence behind the G6 scores applies to them as much as to education→AD.

*Evidence for every G6 score.* Supplementary Table S8 now carries a `G6 evidence` column recording, per case, exactly what supports the score (or that nothing does), including the accession, estimate, P value and power where applicable.

*A worked Grade A example.* LDL→CAD now serves this role: 10 points, with each gate's evidence stated in S8 (12 points in the submitted version, since G6 was then awarded without any documented replication; 10 now, still Grade A). We note in the Limitations that all three Grade A cases sit at the lower bound of the band (10 points), so the example is a threshold case rather than a comfortable one.

*Reference labels and κ.* The two passes are not two independent human raters. There is no second-rater identity, date, blinded sheet or consensus record in the archive: the second pass is a pre-specified stricter reading by the author team. The statistic is therefore reported as **scoring reproducibility** (two blinded passes on identical evidence: 11/12 grades, κ = 0.89, 95% CI 0.64–1.00; quadratic κ = 0.97; per-gate κ across 72 items = 0.91), and the text states explicitly that κ quantifies the reproducibility of the scoring rule, not the validity of the causal inference. We have removed the phrase "two independent raters" and the earlier script that encoded it is marked deprecated.

**Changes:** Results G6 paragraph; Methods (scoring paragraph, G6 definition); Supplementary Table S8 (new column, footnotes 5–7, revised reproducibility paragraph); new `code/scoring_reproducibility.py`; `code/interrater_reliability.py` marked deprecated; Limitations ("Fifth").

## R1-10 — From risk factors to drug targets

> *Please explain how the framework could move from assessing risk factors to assessing specific genes or proteins ... A short discussion of target-specific genetic evidence, relevant tissues, inhibition versus activation, safety and druggability would be helpful. Present prediction of drug-development success as a possible application requiring further validation.*

**Response: accepted in full.** The Discussion section has been expanded along the lines requested.

We now state that a trait-level claim does not identify a target: an LDL–coronary association establishes that LDL cholesterol is causal without identifying the protein a drug should inhibit. Moving to a target requires a cis-pQTL, coding variant or expression QTL to anchor the signal to a specific gene product; evidence that the relevant tissue expresses it; an explicit expectation about the direction of modulation (lowering LDL-cholesterol activity is protective, whereas for many neuroinflammatory targets the beneficial direction of inhibition versus activation is unknown and a genetic association cannot settle it); and separate assessment of safety and druggability, since germline evidence says nothing about on-target toxicity in peripheral tissues or about whether a molecule can engage the target at tolerable exposure. We present grade-based prediction of drug-development success as a hypothesis to be tested prospectively against trial outcomes, not as a demonstrated capability.

**Changes:** Discussion, "Implications for drug-target prioritization" (expanded).

---

# Reviewer 3

## R3-1 — Harmonize terminology for directional/causal claims

> *In the Abstract, I suggest the authors clarify and harmonize the terminology used for directional/causal claims (e.g., "causal claims", "positive association", "an inverse association", etc.) to ensure consistent messaging.*

**Response: accepted in full.** A terminology paragraph has been added at the start of the Methods fixing three terms: a *causal claim* is the hypothesis under test (a proposition, not a finding); an *association* is the observed statistical relationship, reported without causal commitment; a *directed effect* is the causal quantity MR targets. The Abstract and Results now use "association" only for observed relationships and reserve "causal claim" for the proposition being tested, so that a sentence such as "the association attenuated to the null" can no longer be read as a statement about causation.

**Changes:** Methods, new "Terminology" paragraph; Abstract; Results (passim).

## R3-2 — What does "precise" mean?

> *In the Abstract, the authors state that "standard MR pipelines often yield precise, statistically significant estimates that do not reflect directed causal effects." Could the authors clarify what is meant by "precise" in this context?*

**Response: accepted in full; the wording has been replaced rather than footnoted.** "Precise" was doing double duty: it described a small standard error and implied accuracy, which are opposites in this context. The sentence now reads that standard pipelines "often return statistically significant estimates whose apparent precision reflects correlated instruments rather than information, and which do not reflect a directed causal effect." The quantity is defined in the Results: unclumped estimation returns SE = 0.031 from 2,462 correlated variants, and clumping widens the same estimate's SE to 0.203–0.236 — a 6.5- to 7.5-fold increase in the reported standard error, corresponding to a 42- to 56-fold difference in variance. Precision in this paper therefore means nominal precision, the standard error the estimator reports, not the information the data contain.

**Changes:** Abstract; Results, "What LD correction changes"; new Supplementary Table S11.

## R3-3 — European LD reference panel applied to East Asian data

> *When analyzing the East Asian AD dataset, did the authors use the European reference panel for LD clumping? If so, please address whether this mismatch introduces linkage disequilibrium mismatch or bias.*

**Response: accepted in full. The answer is yes, and we state the consequence rather than softening it.**

The cross-ancestry step used European-derived LD-independent instruments in the East Asian outcome; no East Asian LD reference panel was accessible to us, so ancestry-matched re-clumping could not be performed. The text now says this explicitly and names the two biases that follow: residual LD among imported instruments can understate the standard error, and differences in LD structure and allele frequency between ancestries can shift the estimate irrespective of biology. Both affect precision and the magnitude of the point estimate, and can affect its sign as well, which is why the step is read only for directional concordance — and why, at the power achieved (< 6%), the framework assigns it no points at all.

**Changes:** Results G6 paragraph; Methods, new subsection "Trans-ethnic re-clumping" (algorithm, and what happens when no ancestry-matched panel exists); Limitations ("Third").

## R3-4 — Rationale for r² < 0.001 with a 10,000-kb window *(Methods corrected in revision)*

> *What was the rationale for adopting such an unusually stringent clumping threshold (r2 < 0.001) paired with a very large 10,000-kb window? These parameters deviate significantly from common practice in the field.*

**Response: accepted in part.** We can document the choice and show that the verdict does not depend on it; we cannot claim that the parameters follow from a principle.

We must first correct an error in the submitted Methods, because it bears directly on the question. The primary analysis used LD clumping at r² < 0.1 within 10,000 kb, and the clumped estimate reported in the Results (β = −0.130, SE = 0.203, P = 0.52) comes from that tier rather than from r² < 0.001. The archived pipeline fits both tiers explicitly (`r2_loose = 0.1`, `r2_tight = 0.001`). The Methods and the step-by-step protocol now state r² < 0.1 as the primary tier and r² < 0.001 as a sensitivity tier.

With that correction, the premise of the question no longer holds: the primary analysis was not run at an unusually stringent threshold, so the null result cannot be an artefact of over-conservative clumping. The correction makes the response stronger rather than weaker, because the reversal is present in the more permissive tier already. Three tiers are now reported on the same data (Supplementary Table S11): unclumped (β = +0.104, SE = 0.031, 2,462 variants); r² < 0.1 / 10,000 kb (β = −0.130, SE = 0.203, P = 0.52, 54 variants); r² < 0.001 / 10,000 kb (42 loci, 37 variants after harmonisation; β = −0.111, SE = 0.236, P = 0.64); and r² < 0.001 / 5,000 kb (37 variants, same estimate). What we cannot do is justify 10,000 kb over 5,000 kb on first principles; the two give the same answer here, and we report both.

**Changes:** Methods, Gate G2 — clumping threshold **corrected** to r² < 0.1, with the r² < 0.001 tier stated as a sensitivity analysis (Methods text and the step-by-step protocol table); Results, "What LD correction changes" (three tiers); new Supplementary Table S11.

## R3-5 — Does the pipeline feed surviving variables into clumped IVW?

> *To ensure I understand correctly: does the analytical pipeline take the variables that survive these three distinct corrections, input them into clumped IVW, and then test whether the causal effect retains statistical significance? Please clarify this step in the text.*

**Response: accepted in full — the description was ambiguous, and in one place wrong.** The three corrections do not operate in sequence on the variant set. Only the first, LD clumping, changes the instruments. Clumped IVW is then estimated once on that set. MR-Egger, Cochran's Q and the weighted median are diagnostics computed on the same clumped set and remove nothing. MRlap re-estimates the effect from the full shared-variant set with its own internal pruning, and CAUSE fits its model to variants selected at exposure P < 1e-3. A new Methods paragraph states this; the Results previously implied that CAUSE was fitted to the clumped set, and that has been corrected.

**Changes:** Methods, "What each correction operates on"; Results G2 paragraph.

## R3-6 — How were confounders chosen, and why is F > 10 at G4 rather than G1/G2?

> *Could the authors explain how confounders were selected for inclusion in the Multivariable MR? Additionally, why was the requirement for an F-statistic > 10 evaluated at Gate G4 rather than being established at Gate G1 or Gate G2 ... because the F-statistic to some extent is correlated with the significance level (p-value)?*

**Response: accepted in full.** Confounders were not selected automatically: they are traits with published evidence of association with both the exposure and the outcome, restricted to those with a large available GWAS — educational attainment, major depression and LDL cholesterol for insomnia. We state the limitation that such a set is necessarily incomplete and that an omitted confounder leaves the direct effect partly unadjusted.

On the F-statistic, the two quantities are different and the text now separates them. The unconditional F at instrument selection (mean 44.3, minimum 29.8 here) measures whether a variant predicts the exposure and is closely tied to the exposure GWAS P value, as the reviewer notes. The conditional F measures whether, within the multivariable model, the exposure retains genetic variation not already explained by the other exposures. It is undefined until that model exists, so it cannot be applied at G1 or G2; and because it falls as exposures become genetically correlated, its collapse identifies conditional weak instruments whose origin is collinearity rather than a failure of unconditional instrument relevance.

**Changes:** Methods (G4, expanded).

## R3-7 — Comparability of power across ancestries and cross-ancestry bias

> *For Gate G6 ... Is the statistical power comparable between these ancestry cohorts? Furthermore, given that biological mechanisms or causal architecture may differ across population ancestries, please discuss potential bias introduced by cross-ancestry evaluation.*

**Response: accepted in full.** Power is not comparable and the text now says so at each point of use: the East Asian screen achieved < 6% power for the insomnia case and ≥ 84% only under an optimistic R² assumption for education, which is why the gate scores nothing below 80% and why a null replication at adequate power is now treated as a failure rather than a success. On architecture, we state that allele frequencies, LD structure and causal variant composition can differ between ancestries, so a cross-ancestry estimate can shift for reasons unrelated to the biology of the exposure, and that the step is therefore read for sign concordance rather than magnitude. Where no ancestry-matched panel was available, the residual LD mismatch is disclosed rather than removed.

**Changes:** Results G6 paragraph; Methods ("Trans-ethnic re-clumping"); Limitations ("Third").

## R3-8 — Where do MR-Egger, Cochran's Q, MRlap and CAUSE sit in the framework?

> *Were these methods applied to filter/select instrumental variables or used purely as post-estimation sensitivity checks?*

**Response: accepted in full.** None of them filters or selects instruments. They are post-estimation checks, and the Methods now say so in one place, together with what each one operates on: Egger, Q, weighted median and mode on the clumped set; MRlap on the full shared-variant set; CAUSE on variants at exposure P < 1e-3. Only clumping alters the instrument set. This also clarifies why the gate can report a CAUSE classification that disagrees with the clumped IVW without the score changing: CAUSE is a diagnostic, not a scoring input.

**Changes:** Methods, "What each correction operates on"; Table 1 footnote.

## R3-9 — How were the simulation parameter values chosen?

> *What guided the choice of 20 and 60 as instrument counts? Additionally, given a mean F-statistic around 36, the tested causal effect sizes (0, 0.08, and 0.15) seem relatively low; please provide justification for these parameter choices.*

**Response: accepted in full.** The grid was chosen to bracket, not centre on, applied settings: 20 and 60 instruments span the range typical of complex-trait exposures (the 12-case cohort itself ranges from 37 to 312 clumped variants); effect sizes of 0, 0.08 and 0.15 per SD represent a null, a small effect near the median reported for behavioural exposures, and a medium effect at the upper end of what liability to insomnia plausibly exerts on AD risk. The reviewer's point that 0.15 is low relative to F ≈ 36 is well taken and is the reason the grid includes it: 0.15 sits just below the 0.226 threshold at which the worked example reaches 80% power, so every grid point lies below that boundary. The grid therefore samples the underpowered range, in which a scoring rule is most likely to be misled, rather than spanning detectable and undetectable effects. A per-variant F of 36 was set as strong but not trivially strong; block counts of 5, 12 and 40 span coarse to fine partitions.

**Changes:** Methods (simulation parameters).

## R3-10 — What is "trans-ethnic re-clumping" and what are the algorithmic steps?

> *Could the authors clarify what is meant by "trans-ethnic re-clumping" and outline the specific algorithmic steps involved?*

**Response: accepted in full.** A Methods subsection now gives the sequence: extract discovery-ancestry lead variants from the target-ancestry summary statistics; compute pairwise r² using an ancestry-matched LD reference panel; prune variants above r² = 0.001 within 10,000 kb; harmonise alleles, strand and frequencies; compare the resulting IVW estimate with the discovery estimate in sign rather than magnitude, because allele frequencies and LD structure differ between ancestries. The subsection also states what happens when no ancestry-matched panel is accessible — the step is fitted with European-derived LD-independent instruments, labelled a directional screen, scores no points, and the residual LD mismatch is disclosed.

**Changes:** Methods, "Trans-ethnic re-clumping".

## R3-11 — Do not say the r_g estimate "remained unchanged"

> *While a non-significant result indicates no significant genetic correlation, the authors should refrain from asserting that the relationship "remained unchanged after excluding chromosome 19."*

**Response: accepted in full; the sentence has been rewritten.** A null estimate cannot be described as unchanged, since there is no estimate to preserve. The text now reads that r_g was not significantly different from zero (r_g = −0.028, SE = 0.050, P = 0.57), and that excluding chromosome 19 gave a comparably null estimate (r_g = −0.031, P = 0.53), "not a numerically identical one".

**Changes:** Results G3 paragraph.

## R3-12 — Three-line tables without vertical rules

> *Please format all tables according to standard scientific formatting rules (e.g., standard three-line tables without vertical rules).*

**Response: accepted in full.** All five tables in the revised manuscript are set as three-line tables: one rule above the header row, one below it, one below the last row, and no vertical or interior horizontal rules. The supplementary tables are supplied as CSVs with the same structure and as a single workbook (`Supplementary_Tables.xlsx`, twelve sheets) generated from those CSVs by script; neither carries vertical rules, and the CSVs remain the source of truth so that the layout cannot drift from the data. If the journal would rather have the supplementary tables rendered with three-line rules as well, one flag on the build script produces that version, and we will supply it on request.

**Changes:** all manuscript tables; Supplementary Tables S1–S11.

---

# Note on new and revised supplementary material

| Item | Status | Content |
|---|---|---|
| Table S8 | revised | Twelve-case scoring with per-gate evidence: new `decisive_failure` column, `Egger P semantics`, `n instruments`, `G6 evidence`; footnotes 1–7. In the CSV the six gates keep their internal identifiers `L1`–`L6`; `L`*n* is `G`*n* throughout, and the rendered table uses `G1`–`G6` |
| Table S10 | new | Leave-one-gate-out ablation, 72 rows: grade changes per removed gate (same `L`/`G` column convention) |
| Table S11 | new | Three instrument tiers: estimate, SE, SE inflation, G2 verdict |
| Table S12 | new | Threshold robustness: one-at-a-time perturbation, 220 monotone bandings, benchmark ROC location of each boundary, and the before/after effect of the decisive-failure cap (S12.5) |
| `code/threshold_robustness.py` | new | Generates Table S12 in full |
| `code/make_fig2_simulation.py` | new | Regenerates Figure 2 from `sim_marginal.csv` (the submitted figure had no generator script) |
| `code/make_s9.py` | new | Regenerates Supplementary Table S9 from the replicate table |
| `code/sim_marginal_fdr.py` | new | Reproduces the marginal FDR (cell-mean definition) and the null-fraction sensitivity |
| `code/make_table2_uncertainty.py` | new | Wilson intervals, Grade C+D specificity, FDR versus proportion of true nulls |
| `code/make_s11_instrument_tiers.py` | new | Derives Table S11 from the archived instrument-sensitivity table |
| `code/scoring_reproducibility.py` | new | Two-pass scoring reproducibility (supersedes `interrater_reliability.py`, now deprecated) |
| `code/build_s8_v3.py`, `code/build_rubric_spec_v3.py` | new | Generate the scoring table and the single rubric specification |
| `requirements.txt` | new | Python environment for the simulation and tables |
| Zenodo release v1.2.1 | **deposited, DOI 10.5281/zenodo.23733172** | Adds S10, S11, the scripts above, the decisive-failure cap and the aggregation fix; all citations now point to this version DOI |

We are aware that several of the changes above reduce the strength of our original claims: one published case has been regraded from A to B and a G6 point withdrawn from another, the benchmark is now described as covering four gate signals rather than six, the simulation is declared unable to answer the LD-correction question that motivated part of it, and its sensitivity at the largest effect size is 0.88 rather than 0.97 once the published decisive-failure rule is applied. We have made these changes because the reviewers' objections were correct, and because a framework whose purpose is to falsify claims cannot exempt its own.
