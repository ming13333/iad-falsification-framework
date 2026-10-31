<!-- verbatim extraction from 审稿人意见.docx; numbering synthesised from list markers -->

## Reviewer 1 (22 Oct 2026) — recommend major revision

**R1-1.** The scoring rules differ across the text, Table 1, Figure 1 and Table S8: some allow only 0 or 2 points, while others also use 1 point. The education-T2D score of 9 therefore needs explanation. Also, failure at G2 could still produce Grade A under the additive rule. Please provide one consistent scoring table covering partial scores, decisive failures, conflicting results and unavailable or underpowered analyses.

**R1-2.** The simulation script in the cited Zenodo archive differs from the described workflow. G3 uses block coverage and G4 uses leave-one-out variation instead of LDSC/colocalization and MVMR; CAUSE/MRlap and the G6 power check are absent. The code also does not generate the described LD covariance or correlated exposure-outcome errors, and adds outcome noise with SD 0.01 while supplying SE 0.03. Mediator values depend on the true effect but do not generate the outcome. Please confirm the code version used and describe the actual simulation procedure in the Methods, explaining these differences. If they affect the performance results, please update those results.

**R1-3.** What does the full framework add beyond routine LD handling and robustness checks? Please compare correctly LD-adjusted IVW, a conventional MR workflow with specified robustness analyses, and the complete six-gate framework on the same simulated datasets. State the rules for each approach and compare both false positives and missed true effects. Adding gates sequentially or removing one at a time would also help show the contribution of each gate.

**R1-4.** Sensitivity treats A/B as positive, but specificity counts only D as a correct negative. How is Grade C handled? If A/B is positive and C/D is negative, specificity should include both C and D. Please use consistent definitions for sensitivity, specificity, false-positive rate and FDR, and report their uncertainty. Also explain the 0.20 threshold in the Results and how the simulated mix of true and null effects affects FDR.

**R1-5.** The clumped insomnia-AD estimate has an approximate 95% confidence interval of -0.528 to 0.268, which includes the positive effect of 0.10 discussed in the paper. Power to detect that effect is only 24%, and the East Asian analysis has less than 6% power. These findings do not exclude a smaller causal effect. Please distinguish insufficient evidence from evidence against a claim.

**R1-6.** On PDF p. 12, the authors use removal of 118 chromosome-19 instruments to assess the influence of APOE. Please explicitly state that APOE lies on chromosome 19, so this exclusion removes instruments in the APOE region as well as elsewhere on that chromosome; it is not an APOE-specific exclusion. The remaining unclumped IVW association (β = 0.094, P = 0.003) shows that the nominal signal persists without chromosome-19 instruments, but does not by itself establish the contribution of APOE or explain the attenuation after LD clumping. Please clarify this limitation. If attributing the MR result to APOE, define the region and compare results with and without it using the same LD-handling settings. Explain how this evidence and colocalization support Grade C. Also clarify how the 32 reverse and 47 forward regions were selected and whether they overlap; colocalization alone does not establish causal direction.

**R1-7.** On PDF p. 12, the paper groups the analyses as "three null results (clumped IVW, MRlap, and the MVMR direct effect below)." However, p. 13 states: "The direct effect of insomnia was negative (β = -0.57, P = 0.045), opposite in direction to the original claim that insomnia elevates AD risk." This estimate is nominally significant and points in the opposite direction, so calling all three results null is inconsistent. Please use wording such as "none of the three analyses supported the original positive causal hypothesis" and describe nonsignificant and opposite-direction results separately. Also explain why the forward CAUSE results (P = 0.039 and 0.002) are called borderline and how the disagreement affects scoring. Clarify the CAUSE/MRlap inputs and main settings, the reference to extending an MCMC chain, and any effect-unit conversions.

**R1-8.** The total effect and the effect remaining after adjustment answer different questions. Report conditional instrument strength and how correlated estimates and SNPs were handled. For mediation, clarify the 36-versus-25 protein counts, both path estimates, multiple-testing correction and the calculation of 9% triglyceride mediation. Finding no mediator among the 25 proteins analysed does not rule out mediation through other proteins or pathways.

**R1-9.** Please identify the evidence behind the external-validation scores. The text reports East Asian education-T2D results, while S8 gives education-AD full validation points. A fully worked Grade A example would help explain the framework. For all 12 cases, clarify the reference labels and supporting gate results; Cohen's κ measures rater agreement, not causal accuracy.

**R1-10.** The proposed use in drug-target development is interesting. Please explain how the framework could move from assessing risk factors to assessing specific genes or proteins. For example, evidence for LDL causing coronary disease does not identify the protein a drug should target. A short discussion of target-specific genetic evidence, relevant tissues, inhibition versus activation, safety and druggability would be helpful. Present prediction of drug-development success as a possible application requiring further validation.

## Reviewer 3 (23 Oct 2026)

**R3-1.** In the Abstract, I suggest the authors clarify and harmonize the terminology used for directional/causal claims (e.g., "causal claims", "positive association", "an inverse association", etc.) to ensure consistent messaging.

**R3-2.** In the Abstract, the authors state that "standard MR pipelines often yield precise, statistically significant estimates that do not reflect directed causal effects." Could the authors clarify what is meant by "precise" in this context?

**R3-3.** In the Materials and Equipment section, the authors specify using "ieugwasr v1.1.0: LD clumping against the 1000 Genomes European reference" while also mentioning "East Asian AD...". When analyzing the East Asian AD dataset, did the authors use the European reference panel for LD clumping? If so, please address whether this mismatch introduces linkage disequilibrium mismatch or bias.

**R3-4.** Regarding Gate G2 (robustness), what was the rationale for adopting such an unusually stringent clumping threshold (r2 < 0.001) paired with a very large 10,000-kb window? These parameters deviate significantly from common practice in the field.

**R3-5.** To ensure I understand correctly: does the analytical pipeline take the variables that survive these three distinct corrections, input them into clumped IVW, and then test whether the causal effect retains statistical significance? Please clarify this step in the text.

**R3-6.** Could the authors explain how confounders were selected for inclusion in the Multivariable MR? Additionally, why was the requirement for an F-statistic > 10 evaluated at Gate G4 rather than being established at Gate G1 or Gate G2 during initial instrument selection, because the F-statistic to some extent is correlated with the significance level (p-value)?

**R3-7.** For Gate G6, the text states that "Directional consistency is evaluated in an independent ancestry cohort." Is the statistical power comparable between these ancestry cohorts? Furthermore, given that biological mechanisms or causal architecture may differ across population ancestries, please discuss potential bias introduced by cross-ancestry evaluation.

**R3-8.** Could the authors provide more explicit details on how MR-Egger, Cochran's Q test, MRlap correction, and CAUSE fit into this overarching framework? Were these methods applied to filter/select instrumental variables or used purely as post-estimation sensitivity checks?

**R3-9.** In the simulation framework, how were specific parameter numbers chosen? For example, what guided the choice of 20 and 60 as instrument counts? Additionally, given a mean F-statistic around 36, the tested causal effect sizes (0, 0.08, and 0.15) seem relatively low; please provide justification for these parameter choices.

**R3-10.** Could the authors clarify what is meant by "trans-ethnic re-clumping" and outline the specific algorithmic steps involved?

**R3-11.** The description of Gate G3 requires modification for technical accuracy. While a non-significant result indicates no significant genetic correlation, the authors should refrain from asserting that the relationship "remained unchanged after excluding chromosome 19." Please revise this statement accordingly.

**R3-12.** Please format all tables according to standard scientific formatting rules (e.g., standard three-line tables without vertical rules).

