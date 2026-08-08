# Cover Letter — Genome Medicine

**Date:** August 8, 2026

**To:** Rabia Begum, PhD, Chief Editor, *Genome Medicine*

**Re:** Submission of "A falsification framework for causal claims in polygenic epidemiology: the insomnia–Alzheimer's disease test case" (Research article)

---

Dear Dr Begum,

We are pleased to submit our manuscript "A falsification framework for causal claims in polygenic epidemiology: the insomnia–Alzheimer's disease test case" for consideration as a Research article in *Genome Medicine*.

Mendelian randomization (MR) has become the standard route from genetic association to causal claim, and it now sits at the front of the genomic-medicine pipeline — prioritizing drug targets, informing therapeutic windows, and annotating disease mechanisms. Yet most MR pipelines are built to accumulate evidence, not to reject it: a typical workflow assembles a significant inverse-variance-weighted estimate, checks heterogeneity, and stops. Nothing in that sequence is designed to fail. The difficulty is greatest under extreme polygenicity, where thousands of correlated instruments inflate an apparent effect precisely in the genomic regions where liability is most concentrated. Reporting guidelines such as STROBE-MR tell authors what to disclose, but they do not say when the disclosed evidence is enough to stand behind a directional claim that will influence target selection or clinical reasoning. Our framework supplies that missing step — an evidentiary threshold rather than a reporting standard.

The manuscript contributes in three ways. **First**, it makes falsification, rather than discovery, the operational logic of causal-claim validation. Six ordered gates (association, robustness, genetic architecture, direct effect, biological mediation, and directional external validation) each test a distinct false-positive mechanism, and any single one can downgrade a claim. The output is a graded verdict from A to D, not a binary supported-or-rejected label. **Second**, the framework overturns a result that has already survived every standard check. The insomnia→AD association yields a positive MR effect (β = +0.10, P = 9.3 × 10⁻⁴; 2,462 correlated instruments) that holds under MR-Egger and MR-PRESSO. After LD-clumping, the estimate collapses (P = 0.52–0.64); sample-overlap correction agrees (MRlap P = 0.43); and multivariable adjustment points the other way. Three independent corrections converge on rejection — evidence that the estimate was never wrong within its pipeline, but that the pipeline has no procedure to falsify its own output. The recalibrated interpretation is APOE-centered shared liability rather than a directed causal pathway, a distinction with direct implications for how sleep and AD comorbidity is framed in genomic medicine. **Third**, the framework discriminates across the full evidence spectrum using both empirical and simulated ground truth. Twelve trait pairs spanning four disease domains receive Grade A (LDL→CAD, education→AD, BMI→T2D, height→CAD), Grade B (education→T2D, with mild pleiotropy), Grade C (insomnia→AD, BMI→stroke, HDL→CAD, depression→AD), and Grade D (BMI→AD, CRP→CAD, T2D→AD). A 43,200-replicate simulation with known causal parameters gives sensitivity 0.97 and specificity 1.00, with FDR no higher than 0.18 under directional pleiotropy. Five East Asian cross-ancestry checks — including a trans-ethnic insomnia→AD transfer into the GARD East Asian AD cohort — contradicted no framework-assigned direction.

We believe *Genome Medicine* is the right venue for three reasons specific to its remit. First, the journal's emphasis on multi-ancestry and cross-ancestry evidence is precisely where the framework is weakest by default and where we have invested: the insomnia–AD core pair now includes a trans-ethnic check, and the protective education signal replicates directionally in East Asian cohorts. Second, the framework's immediate translational relevance — grading genetically supported targets before clinical investment, as illustrated by LDL→CAD (Grade A) versus HDL→CAD (Grade C, mirroring the torcetrapib history) — speaks directly to the journal's target-validation and precision-medicine readership. Third, the test case is a neurogenomics problem: AD genetics, APOE-centered architecture, and a modifiable exposure (sleep) are central to the journal's disease focus.

The framework cannot prove a causal effect; it can only raise or lower confidence in one. Its practical value is the default we hope the field will adopt: every MR-based report should present both clumped and unclumped IVW estimates as routine sensitivity analysis, much as meta-analyses now report both fixed- and random-effect models. For reviewers and editors, the A/B/C/D rubric offers a transparent standard for judging whether a signal reflects directed causality or shared liability. We present the insomnia–AD result as a worked example; the contribution is the framework, not the specific comorbidity conclusion.

The manuscript is not under consideration elsewhere. All authors have approved submission and declare no competing interests. All GWAS summary statistics are publicly available, and the full analysis pipeline (R and Python modules, cached harmonized inputs, environment specifications) will be released in a public repository with a Zenodo archive on acceptance. This is a secondary analysis of publicly available summary-level data; no ethics approval was required. The manuscript was prepared with AI-assisted writing support (a large language model used for language drafting and refinement); all content was verified by the authors.

We thank you for considering this work.

Yours sincerely,

Qin Liu, on behalf of all authors (Ming Luo, Wangyang Ye, Qin Liu)
Department of Neurosurgery, The Fifth Affiliated Hospital of Wenzhou Medical University (Lishui Central Hospital), Lishui, Zhejiang, 323000
Email: lqin5467@gmail.com
