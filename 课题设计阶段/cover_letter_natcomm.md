# Cover Letter — Nature Communications

**Date:** August 5, 2026

**To:** The Editor-in-Chief, *Nature Communications*

**Re:** Submission of "A falsification framework for causal claims in polygenic epidemiology: the insomnia–Alzheimer's disease test case"

---

Dear Editor-in-Chief,

We are pleased to submit our manuscript "A falsification framework for causal claims in polygenic epidemiology: the insomnia–Alzheimer's disease test case" for consideration as an Article in *Nature Communications*.

Mendelian randomization has become the standard way to turn genetic associations into causal claims, yet most pipelines are built to accumulate evidence, not to reject it. A typical workflow assembles a significant inverse-variance-weighted estimate, checks heterogeneity, and stops. Nothing in that sequence is designed to fail. The difficulty is greatest under extreme polygenicity, where thousands of correlated instruments inflate an apparent effect precisely in the genomic regions where liability is most concentrated. Reporting guidelines such as STROBE-MR tell authors what to disclose, but they do not say when the disclosed evidence is enough to stand behind a directional claim. Our framework supplies that missing step.

The manuscript contributes in three ways. First, it makes falsification, rather than discovery, the operational logic of causal-claim validation. Six ordered gates (association, robustness, genetic architecture, direct effect, biological mediation, and external validation) each test a distinct false-positive mechanism, and any one of them can downgrade a claim. The output is a graded verdict from A to D, not a binary supported-or-rejected label. Second, the framework overturns a result that has already survived every standard check. The insomnia–AD association yields a positive MR effect (β = +0.10, P = 9.3 × 10⁻⁴; 2,462 correlated instruments) that holds under MR-Egger and MR-PRESSO. After LD-clumping, the estimate collapses (P = 0.52–0.64); sample-overlap correction agrees (MRlap P = 0.43); and multivariable adjustment points the other way (β ≈ −0.5, P = 0.045–0.16). Three independent corrections converge on rejection. The estimate was never wrong within its pipeline. The pipeline simply has no procedure to falsify its own output. Third, the framework discriminates across the full evidence spectrum using both empirical and simulated ground truth. Twelve trait pairs spanning four disease domains receive Grade A (LDL→CAD, education→AD, BMI→T2D, height→CAD), Grade B (education→T2D, with mild pleiotropy), Grade C (insomnia→AD, BMI→stroke, HDL→CAD, depression→AD), and Grade D (BMI→AD, CRP→CAD, T2D→AD). A 43,200-replicate simulation with known causal parameters gives sensitivity of 0.97 and specificity of 1.00, with FDR no higher than 0.18 under directional pleiotropy. Four East-Asian replication checks did not contradict any framework-assigned direction.

The framework cannot prove a causal effect; it can only raise or lower confidence in one. Its practical value is the default we hope the field will adopt: every MR-based report should present both clumped and unclumped IVW estimates as a routine sensitivity analysis, much as meta-analyses now report both fixed- and random-effect models. For reviewers, the A/B/C/D rubric offers a transparent basis for judging whether a signal reflects directed causality or shared liability. We present the insomnia–AD result as a worked example. The contribution is the framework, not the specific comorbidity conclusion.

*Nature Communications* is the right venue because this is a methodological advance with reach across neurodegeneration, cardiometabolic disease, psychiatry, and anthropometric traits, rather than a finding tied to one disease. It extends STROBE-MR instead of competing with it, filling the evidentiary-threshold layer the guideline leaves open. The timing is relevant: as GWAS sample sizes reach into the millions and MR publications multiply, the need for procedures that separate precisely estimated signals from meaningful ones is immediate.

The manuscript is not under consideration elsewhere. All authors have approved submission and declare no competing interests. All GWAS summary statistics are publicly available, and the full analysis pipeline (25 R and Python modules, cached harmonized inputs, environment specifications) will be released in a public repository with a Zenodo archive on acceptance. The manuscript was prepared with AI-assisted writing support (a large language model used for language drafting and refinement); all content was verified by the authors.

Yours sincerely,

Qin Liu, on behalf of all authors
Department of Neurosurgery, The Fifth Affiliated Hospital of Wenzhou Medical University (Lishui Central Hospital), Lishui, Zhejiang, 323000
Email: lqin5467@gmail.com
