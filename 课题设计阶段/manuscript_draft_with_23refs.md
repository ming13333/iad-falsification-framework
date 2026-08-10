# A falsification framework for causal claims in polygenic epidemiology: the insomnia–Alzheimer's disease test case

Ming Luo<sup>1,†</sup>, Wangyang Ye<sup>1,†</sup>, Qin Liu<sup>1,*</sup>

<sup>1</sup>Department of Neurosurgery, The Fifth Affiliated Hospital of Wenzhou Medical University (Lishui Central Hospital), Lishui, Zhejiang 323000, China

<sup>†</sup>These authors contributed equally to this work. <sup>*</sup>Correspondence: Qin Liu, lqin5467@gmail.com

---

## Abstract

**Background:** Under extreme polygenicity, larger GWAS sample sizes reduce statistical uncertainty but make systematic bias harder to detect, creating a paradox in which more precisely estimated causal signals may be less credible. Standard Mendelian randomization (MR) pipelines accumulate supporting evidence at every stage, yet lack a systematic procedure for falsifying a directional causal claim. We introduce a six-level falsification framework for causal claims in polygenic epidemiology and apply it to the widely reported insomnia–Alzheimer's disease (AD) association as a challenging test case.

**Methods:** Six ordered gates — association, robustness, genetic architecture, direct effect, biological mediation, and directional external validation — each capable of independently rejecting a directed causal interpretation, were operationalized with MR across twelve trait pairs spanning four disease domains, a 43,200-replicate simulation with known causal parameters, and five East Asian cross-ancestry checks.

**Results:** The positive insomnia→AD effect (β = +0.10, P = 9.3 × 10⁻⁴, unclumped) did not survive LD-clumping (P = 0.52–0.64) or sample-overlap correction (P = 0.43), consistent with APOE-centered locus-specific shared liability rather than directed causation. The framework assigned Grade A to four positive controls (LDL→CAD, education→AD, BMI→T2D, height→CAD), Grade B to a protective signal with mild pleiotropy (education→T2D), Grade C to four pleiotropy-driven or reclassified signals (insomnia→AD, BMI→stroke, HDL→CAD, depression→AD), and Grade D to three null claims (BMI→AD, CRP→CAD, T2D→AD). Simulation-based operating characteristics were sensitivity 0.97 and specificity 1.00; no East Asian cross-ancestry check contradicted a framework-assigned direction.

**Conclusions:** A causal claim should be accepted only after it has survived independent attempts to falsify it. The framework supplies a graded, transparent evidentiary threshold for causal claims in polygenic epidemiology that is applicable beyond MR.

**Keywords:** Mendelian randomization; causal inference; falsification framework; genetic architecture; Alzheimer's disease; insomnia; cross-ancestry replication; drug-target validation

---

## Background

Before P < 5 × 10⁻⁸ became the field-wide GWAS threshold, the early 2000s produced hundreds of gene–disease claims that collapsed in replication [1]. That period was not a failure of the GWAS approach but a correction: the field learned that a reproducible discovery requires instrument-level validation, not just a significant effect estimate. A decade later, -omics epidemiology faces an analogous inflection point — and Mendelian randomization (MR) is its sharpest instance. A decade of comorbidity MR has produced replicated claims of directed causation between traits — insomnia and AD prominent among them [2-5] — yet the simplest instrument-validation step, checking whether the causal estimate survives LD-clumping and sample-overlap correction, is absent from most published workflows [6-9]. When instruments are LD-correlated, the standard inverse-variance weighted (IVW) estimator can return a precisely estimated signal whose precision comes not from a biological effect but from the LD structure of a single genomic region.

The architectural problem goes deeper than missing quality control. Under extreme polygenicity — thousands of variants of small effect influencing both exposure and outcome — more instruments no longer mean better causal estimation. Correlated instruments *inflate* apparent effect strength, and the inflation is greatest where the genetic architecture is most concentrated [9]. Insomnia and AD illustrate this directly: multiple published MRs report a positive insomnia→AD effect [2-5], yet almost none report whether that effect survives the instrument-independence gate. The same dynamic recurs wherever polygenic evidence is aggregated without a rejection procedure — in observational triangulation, in phenome-wide scans, and in multi-omics mediation — making the absence of a falsification step a field-wide vulnerability rather than an MR-specific gap.

But the limitation is more fundamental than a missing quality-control step. **Current causal-inference pipelines in -omics epidemiology are optimized for discovering causality, not for falsifying causal claims.** A conventional MR workflow assembles a significant IVW estimate, confirms it with MR-Egger and MR-PRESSO, and stops. Every stage accumulates supporting evidence; none is designed to reject the claim. What is missing is a systematic procedure for breaking the hypothesis — a set of diagnostic gates that treat a causal claim as provisionally accepted only to the degree that severe attempts to falsify it have failed. Under extreme polygenicity, where any trait pair can yield a nominally significant result, the decisive question is no longer "can we perform the analysis?" but "should we believe this result?" [10-11].

Existing reporting checklists such as STROBE-MR [12] address a related but distinct problem: they specify what information should be reported in every MR study. They do not, however, define how much supporting evidence is sufficient to sustain, downgrade, or reject a causal claim. The present framework supplies this missing layer — an evidentiary threshold, not a reporting standard — that asks whether completed analyses collectively support a causal interpretation at a specified confidence grade. Although developed and validated through MR, the underlying logic — graded falsification gates applied to any body of polygenic evidence — generalizes to other causal-inference settings where correlated evidence can be mistaken for signal.

The falsification hierarchy introduced here arranges these tests into six ordered gates (Fig. 1), applicable to any polygenic causal-inference setting rather than to MR alone. Each gate can independently reject a directional causal claim:

1. **Association** — does a raw MR signal exist at all?
2. **Robustness** — does it survive instrument-independence (LD-clump) and sample-overlap correction?
3. **Genetic architecture** — does the relationship reflect a genome-wide shared polygenic architecture or merely locus-specific sharing?
4. **Direct effect** — does the effect persist after adjusting for confounders and competing exposures?
5. **Biological mediation** — is there a genetically proxied mechanistic pathway?
6. **External validation** — does the conclusion hold under cross-ancestry replication and positive/negative control discrimination?

A high-confidence causal claim requires passage through all six gates; failure at any single gate suffices to falsify a directed causal interpretation. The levels are complementary analytical perspectives on the same GWAS — not independent datasets — so their agreement constitutes analytical triangulation rather than independent replication [10-11]. This reframes causal inference in polygenic epidemiology as a quality-control layer: the goal is to remove artefactual signals before they are published as biology.

The insomnia–AD pair serves as a deliberately challenging test case. Before analysis, we made no prior commitment to causal direction. The robustness gate revealed that the unclumped insomnia→AD signal — consistent with the published literature — is not robust to instrument-independence verification and therefore cannot, by itself, be interpreted as directed causality. Educational attainment's protective effect on AD, a well-established relationship, was evaluated as an internal positive control to show that the framework discriminates rather than uniformly nulls [13-19]. The remaining levels converge on a revised conclusion: insomnia–AD comorbidity is driven by APOE-centered locus-specific shared liability, with educational attainment emerging as a cross-ancestry protective factor — not by a robust directed causal pathway.

---

## Results

### Level 1 — Association: the raw insomnia→AD signal is significant but merely associational

We first established whether a raw MR signal exists between insomnia (ukb-b-3957; UK Biobank, n = 462,341) and AD (ieu-b-2; IGAP Kunkle et al. 2019, ncase = 21,982). Without LD-clumping, the forward (insomnia→AD) IVW estimate was positive and nominally significant (β = +0.104, SE = 0.031, P = 9.3 × 10⁻⁴), replicating the published literature [2-5]. The reverse direction (AD→insomnia) was also nominally significant but tiny in magnitude (β ≈ −0.003 to −0.007) with a highly significant MR-Egger intercept, consistent with broad horizontal pleiotropy rather than genuine directed causality [8,16,20-23].

At this first gate, however, a significant association is not a causal claim. The unclumped estimate draws on 2,462 correlated instruments; its precision reflects instrument count, not necessarily biological signal. Level 1 is therefore treated as a screening gate only: it establishes that a signal exists to be tested, and nothing more.

### Level 2 — Robustness: the signal fails the instrument-independence and overlap gates

We next asked whether the Level-1 signal survives correction for the two dominant MR artefacts — correlated instruments and sample overlap. **After standard LD-clumping** (r² < 0.001, 10,000 kb window), the instrument count dropped from 2,462 to 54 SNPs and the forward IVW estimate reversed to null and non-significant (loose clump β = −0.130, SE = 0.203, P = 0.52; tight clump [r² < 0.001, 5,000 kb] 37 SNPs, β = −0.111, SE = 0.236, P = 0.64) (Fig. 2A). **MRlap** (sample overlap correction) returned a corrected forward estimate indistinguishable from zero and opposite in sign (β = −0.078, SE = 0.098, P = 0.43) [24]. These two independent corrections — one for LD structure, one for sample overlap — both fail to support a directed effect.

A clumped null can reflect either the absence of a genuine effect or the loss of polygenic signal and statistical power that aggressive clumping entails (the clumped forward analysis retains only ~7% power to detect the unclumped effect size; 80% power would require β ≥ 0.57). We verified that the signal collapse was not an artefact of chromosome 19 (which harbours APOE). The insomnia GWAS contributed only **118 chromosome-19 instruments, all clustered at 37.4–37.6 Mb** — distant from the APOE ε4 locus (44–46 Mb), which contributed **zero** insomnia instruments. Removing all 118 chromosome-19 SNPs preserved a positive, significant forward estimate (β = 0.094, SE = 0.032, P = 0.003; ~91% of the unclumped signal), demonstrating that the unclumped→clumped reversal reflects global removal of LD-correlated variants rather than APOE-locus dominance.

**CAUSE** (Bayesian partitioning of causal vs. correlated-pleiotropy components, run on 1,645 independent variants) classified the forward direction as CAUSAL (Kunkle: posterior P = 0.039, ELPD-difference z = 2.07; Bellenguez: P = 0.002, z = 3.05) but simultaneously estimated a very low genome-wide sharing probability (ρ ≈ 0.005) and was **direction-specific**: the reverse direction was classified as PLEIOTROPY_OR_SHARING rather than causal (Kunkle P = 0.082; Bellenguez P = 0.631) [24]. Thus CAUSE indicates a small residual forward component superimposed on low background sharing, not a strong bidirectional causal relationship.

**Steiger directionality testing** was inconclusive: the binary-trait-corrected method (r_from_lor) pointed to AD→insomnia, whereas the quantitative fallback (p→r) pointed in the opposite direction; median per-SNP variance explained was negligible (|r| ≈ 0.002). Steiger was not used to determine direction here.

**Verdict at Level 2:** the insomnia→AD signal does not survive the robustness gate. Three methodologically distinct corrections (clumping, overlap, and — with the caveats above — the low-sharing CAUSE estimate juxtaposed against null genome-wide rg and null multivariable direct effect) converge on rejection of a robust directed effect. This single gate is sufficient, within the framework, to falsify the unclumped literature's directional claim.

### Level 3 — Genetic architecture: shared liability, not a genome-wide shared polygenic background

The next question was whether any comorbidity reflects a genome-spanning shared architecture or locus-specific sharing. LD Score regression yielded a cross-trait genetic correlation indistinguishable from zero (rg = −0.028, SE = 0.050, P = 0.57; 95% CI excludes |rg| > ~0.13), unchanged after removing chromosome 19 (rg = −0.031, SE = 0.049, P = 0.53) [25-26]. At the genome-wide scale, insomnia and AD share no detectable polygenic correlation.

Bayesian colocalization told a locus-specific story (Fig. 2B). In the forward direction, only **1 of 47** tested loci exceeded PP.H4 ≥ 0.80 (rs10838708, chromosome 11; PP.H4 = 0.849; Bellenguez replication 0/49). In the reverse direction, **18 of 32** loci passed (Kunkle), concentrated at the APOE region (PP.H4 > 0.98). Colocalization establishes a *shared causal variant*, not the *direction* of causation; the asymmetry, read together with the null genome-wide rg, indicates shared liability (a common APOE ε4 variant elevating both traits) rather than a unidirectional pathway [16-17,27].

**Verdict at Level 3:** no genome-wide shared polygenic architecture; only APOE-centered locus-specific sharing. This is inconsistent with a pervasive causal relationship and consistent with the Level-2 rejection.

### Level 4 — Direct effect: multivariable adjustment isolates a protective factor, not a causal insomnia pathway

To test whether any effect persists after adjusting for confounders, we performed multivariable MR (MVMR) with insomnia, educational attainment, depression, and LDL-cholesterol as exposures and AD as outcome (exposure selection informed by a minimal confounding diagram; Methods) [28-29]. Educational attainment showed a robust protective effect across all instrument sets (loose clump β = −1.29, P = 0.008; tight clump β = −1.39, P = 0.045; chromosome-19-removed β = −1.28, P = 0.009). Insomnia's direct effect was negative and at most marginally significant (loose β = −0.57, P = 0.045; tight β = −0.53, P = 0.16), consistent with its null-to-negative profile after clumping.

A PheWAS using education instruments confirmed protection against AD (Kunkle β = −0.33, SE = 0.075, P = 1.1 × 10⁻⁵) and Parkinson's disease (Nalls 2019 β = −0.39, SE = 0.086, P = 7.2 × 10⁻⁶), but not multiple sclerosis (β = 0.015, P = 0.90) (Fig. 3). The Bellenguez AD estimate was directionally inconsistent (β = +0.11, P = 0.035) with extreme heterogeneity (Q P = 1.7 × 10⁻¹¹), rendering it unreliable.

**Verdict at Level 4:** the only exposure with a durable direct effect is educational attainment (protective). Insomnia's direct effect collapses to null/negative. This counts against a causal insomnia→AD pathway and supports a protective education→AD effect.

### Level 5 — Biological mediation: no protein mediation; triglycerides partially mediate education's protection

We tested whether genetically proxied mediators transmit the comorbidity (Fig. 4). In the insomnia→protein→AD model, CRP and IL-6 indirect effects were null (CRP β_indirect = −0.001, P = 0.93; IL-6 β_indirect = −0.002, P = 0.80; FDR = 0.91) [30,31]. A curated 36-protein AD-relevant screen (exposure = educational attainment, n = 317 instruments, to maximize power) returned **25 evaluable proteins, 11 excluded for insufficient instruments, and zero FDR < 0.05 hits** (minimum raw P_indirect = 0.111, interleukin-21) [30,32]. An exposure-substitution check confirmed neither CRP nor IL-6 mediated education→AD (P = 0.86 and 0.83, respectively).

In the metabolite dimension, **total triglycerides (Total_TG) significantly mediated education→AD** (indirect β = −0.031, SE = 0.008, P = 5.7 × 10⁻⁵, q = 5.7 × 10⁻⁴; bootstrap 95% CI [−0.047, −0.017], P < 0.001), accounting for ~9% of education's total protective effect. Total cholesterol, DHA, and omega-3 also passed FDR < 0.05 (q = 0.034–0.045) [33,34,35].

**Verdict at Level 5:** the mechanism gate reveals a lipid-mediated, protein-independent architecture. No mechanistic support exists for an insomnia→AD pathway; a plausible mediator exists for the protective education→AD effect.

### Level 6 — Directional external validation: cross-ancestry consistency and control discrimination

The final gate tests generalizability (Fig. 5). For the framework-identified protective signal, we examined directional consistency in East Asian (EAS) cohorts, using Chen/Kim/Lam 2024 EAS educational attainment instruments (GCST90296498; n = 165,232) and BioBank Japan (BBJ) disease outcomes, together with the GARD East Asian AD GWAS (NG00182; n = 6,518, 2,919 cases). **Education→T2D replicated significantly in EAS**: the same 9 EAS education instruments against BBJ type 2 diabetes (bbj-a-77; n = 191,764, 36,614 cases) gave IVW β = −0.145, P = 0.012 (weighted median β = −0.122, P = 0.022; Egger intercept P = 0.819), directionally and substantially concordant with the European analysis (β = −0.634). **T2D→AD remained null in EAS**: 71 position-matched BBJ T2D instruments against GARD EAS AD gave IVW β = +0.006, P = 0.93, matching the European null (β = −0.010, P = 0.71). **Education→Stroke was null in EAS** (BBJ ischemic stroke, bbj-a-129; n = 210,054, 17,671 cases): IVW β = −0.008, P = 0.87 — underpowered with 9 instruments, but directionally consistent with the modest European literature. Education→AD EAS directional consistency (β = −0.029, P = 0.85; 9 instruments) was reported previously [13,36]. **For the study's core pair, a trans-ethnic insomnia→AD check** transferred 40 LD-independent EUR insomnia instruments (r² < 0.001, 10 Mb) into GARD EAS AD; 30 matched by position with allele-flip harmonization and gave a negative, non-significant IVW estimate (β = −0.84, SE = 0.77, P = 0.28; weighted median β = −1.76, P = 0.022; MR-Egger intercept P = 0.61; heterogeneity Q P = 0.005), directionally consistent with the EUR clumped null (β = −0.13, P = 0.52) and providing no evidence of a positive directed effect in an independent ancestry. With 2,919 EAS cases this check is powered only for directional screening (power < 6% at the EUR clumped magnitude) and is reported without grade assignment, mirroring the framework's treatment of underpowered checks elsewhere (Supplementary Note 2). Across all five cross-ancestry checks, no framework-assigned direction was contradicted in EAS (full details in Supplementary Note 2).

The decisive test of any validation framework is whether it can separate true from null claims — assigning high confidence to genuine effects and flagging insufficient evidence [37-38]. This was tested across **twelve trait pairs spanning four disease domains** (Lipid, Neuro, Metabolic, Inflammatory/General) and the full grade spectrum (Supplementary Table s7). Four known or confirmed positive effects received Grade A; one borderline protective received Grade B (Education→T2D, F = 50, IVW β = −0.634, P = 2.1 × 10⁻²⁶ with Egger intercept P = 0.036 and high heterogeneity Q P = 3.2 × 10⁻²⁹ downgrading the L2 gate); four pleiotropy-driven or reclassified pairs received Grade C (insomnia→AD, BMI→stroke, HDL→CAD, depression→AD); three cleanly null claims (CRP→CAD at F = 176; BMI→AD at F = 66; and the new T2D→AD pair at F = 78) received Grade D. The expanded cohort was selected to enrich borderline-ambiguous pairs (Grades B and C), addressing the previously-noted limitation of the original nine-case cohort.

**Key new cases:**

- **Education→T2D (Grade B):** Educational attainment (ieu-a-1239, Lee 2018, n = 766,345) as exposure and Type 2 diabetes (ebi-a-GCST006867, Xue 2018, ~62k cases) as outcome. Clumping at r² < 0.001, 10 Mb yielded 317 independent instruments (F = 50). IVW β = −0.634, P = 2.1 × 10⁻²⁶ (protective, consistent with the established literature [34]); weighted median β = −0.567, P = 5.5 × 10⁻¹⁸ (directionally concordant); MR-Egger intercept P = 0.036 (mild directional signal) and heterogeneity Q P = 3.2 × 10⁻²⁹ (high). The L2 gate is therefore partially passed: clumped IVW remains strongly significant but the Egger intercept suggests non-zero directional pleiotropy. The L6 gate passed on the strength of significant EAS replication (BBJ: β = −0.145, P = 0.012), yielding Grade B (9/12). This case demonstrates the framework handling a well-established positive where mild pleiotropy-induced uncertainty correctly downgrades the grade while cross-ancestry consistency is retained.
- **Depression→AD (Grade C):** Major depression (ieu-b-102, Howard 2019, n = 500k) as exposure and AD Kunkle (ieu-b-2) as outcome. Clumping yielded 50 instruments (F = 37.9). IVW β = −0.254, P = 0.0135 (protective); weighted median β = −0.241, P = 0.059 (borderline non-significant); Egger intercept P = 0.119; heterogeneity Q P = 0.053. The robustness gate is therefore partially passed: clumped IVW is significant but the weighted median fails to reach 5% nominal significance, yielding Grade C (5/12). This case parallels the insomnia→AD study pair — a psychiatric exposure against AD with mixed sensitivity-method agreement — and confirms the framework's consistent treatment of psychiatric-exposure → AD pairs.
- **T2D→AD (Grade D):** Type 2 diabetes (ebi-a-GCST006867) as exposure and AD Kunkle as outcome. Clumping yielded 118 instruments (F = 77.8). IVW β = −0.010, P = 0.714 (precisely null); weighted median β = −0.006, P = 0.891; Egger intercept P = 0.268. Grade D (1/12) — clean null at high power, mirroring the framework's correct rejection of BMI→AD and demonstrating conservative specificity on the contested metabolic-exposure → AD question.

The full twelve-case grading — with per-level scores, F statistics, IVW/WM/Egger estimates, and notes — is reported in Supplementary Table s7 and visualized in Fig. 5.

- **LDL cholesterol→coronary artery disease (textbook positive control):** achieves **Grade A** (high confidence causal). LDL instruments were strong (F = 182, 73 harmonized SNPs after clumping); the IVW estimate was robustly significant (β = +0.388, SE = 0.042, P = 2.0 × 10⁻²⁰), consistent with decades of statin RCTs and MR concordance [39]. MR-Egger (β = +0.400, P = 4.1 × 10⁻⁹) and weighted median (β = +0.343, P = 2.4 × 10⁻¹³) both corroborate. All six levels pass.
- **Educational attainment→AD (internal positive control):** achieves **Grade A** (high confidence protective) across all six gates (PheWAS β = −0.33, P = 1.1 × 10⁻⁵; TG mediation q = 5.7 × 10⁻⁴; EA cross-ancestry directional consistency). Confirms the framework does not manufacture false negatives.
- **BMI→AD (negative control):** body mass index (ieu-a-2, F = 65.6, 71 harmonized SNPs) is widely MR-tested against AD with mixed results; under the full framework, its IVW estimate was precisely null (β = −0.092, SE = 0.092, P = 0.32). MR-Egger (β = −0.151, P = 0.57) and weighted median (β = −0.143, P = 0.22) both agree. Assigned **Grade D** (not supported) — the framework correctly refrains from over-interpreting, demonstrating it does not default to positivity at high power. BMI–AD is a genuinely *contested* relationship; assigning a low evidence grade here demonstrates conservative specificity precisely where MR claims are most consequential.
- **Insomnia→AD (study case):** assigned **Grade C** (shared liability, weak causal evidence) after failing the robustness gate (Level 2).
- **Internal specificity:** 25/25 protein mediators return null while education→AD, LDL→CAD, and the TG mediation all return significant — confirming the framework discriminates rather than uniformly nulling.

The framework assigns evidence grades spanning the full spectrum across the primary validation cases (Supplementary Table s7).

### Framework synthesis

Integrating all six levels, the insomnia→AD pair is classified as **shared liability without independent causal upstream** (Fig. 1c):

- **L1 Association**: unclumped positive signal (+0.10) — screening only.
- **L2 Robustness**: clumped, overlap-corrected, and multivariate estimates converge to null; fails the gate.
- **L3 Architecture**: rg ≈ 0 (P = 0.57); colocalization reverse-dominant and APOE-centered.
- **L4 Direct effect**: education protective (β ≈ −0.33 to −1.3); insomnia direct null/negative.
- **L5 Mediation**: no protein mediation; partial TG mediation of education's protection.
- **L6 Validation**: five EAS cross-ancestry checks, none of which contradicted the assigned directions (Education→T2D significant replication; T2D→AD null concordance; Education→Stroke null; Education→AD and trans-ethnic insomnia→AD directional consistency); full quantitative grading is provided in Supplementary Table s7.

CAUSE returned a nominally causal forward signal (Kunkle P = 0.039; Bellenguez P = 0.002), juxtaposed against very low genome-wide sharing probability (ρ ≈ 0.005) and a sharing-only reverse classification. CAUSE partitions effects rather than negating other methods, and its forward signal — while methodologically real — exists alongside null-or-negative estimates from clumped IVW (P = 0.52–0.64), MRlap (P = 0.43), and MVMR (β ≈ −0.5, P = 0.045–0.16). Given the clumped UVMR's ~7% power and CAUSE's greater effective sensitivity, the residual forward component is compatible with the converging null estimates; it is interpreted as a small unresolved effect, not as a positive causal claim. Steiger directionality testing was inconclusive (conclusion depended on the method used to construct r from binary outcomes; median per-SNP variance explained was negligible) and is reported as a caution against its mechanical application, not as direction-determining evidence.

### Framework operating characteristics: simulation study

To complement the empirical 12-case validation cohort, we quantified the framework's operating characteristics via a simulation study. We generated polygenic two-sample MR summary statistics with **known ground truth** (causal β = 0 / 0.08 / 0.15 per-SD) under a scenario grid varying LD concentration (number of LD blocks 40 / 12 / 5, representing low / medium / high), pleiotropy regime (none / balanced / directional), sample overlap (0 / 0.3), and instrument count (20 / 60), for a total of **43,200 replicates**. Each replicate was scored by all six framework gates (L1 association, L2 clumping + Egger robustness, L3 architecture spread, L4 leave-one-out direct-effect proxy, L5 two-step mediation, L6 independent-sample directional consistency) and assigned Grade A/B/C/D. Mediation signals (L5) were generated only under true causal pathways so that null replicates did not spuriously pass the mediation gate; the L2 disjunctive falsification logic — L1 failure cascading to grade D — was implemented to mirror the manuscript framework.

**Key operating characteristics (marginal over LD, n_iv, n_sim per cell):**

| Scenario | Sens (A/B) at moderate effect (0.15) | Specificity (D) at null | FDR (A/B given null) |
|----------|--------------------------------------|-------------------------|---------------------|
| Ideal (no pleio., no overlap) | **0.97** (Grade A: 0.88) | **1.00** | 0.00 |
| Balanced pleio. | 0.85 | 0.80 | 0.06 |
| Directional pleio. | 0.80 | 0.68 | 0.08–0.18 |
| Directional + 30% overlap | 0.79 | 0.68 | 0.08–0.18 |

**Interpretation.** The framework achieves near-perfect discrimination in the ideal scenario: 97% sensitivity for true moderate effects with 100% specificity at null, yielding zero false discoveries. Sensitivity falls to ~0.5 for weak effects (β = 0.08), reflecting the framework's deliberate conservatism when statistical power is insufficient — the same calibration that protects against false-positive causal claims in real MR. Under directional pleiotropy or sample overlap, sensitivity is mildly reduced and the false-discovery rate among A/B-assigned replicates rises to ~0.08–0.18, confirming that the framework detects pleiotropy- and overlap-driven inflation and downgrades the evidence grade rather than misclassifying it. Full operating-characteristic curves across LD concentration × instrument count are in Supplementary Fig. 5; per-scenario CSV with sensitivity, specificity, and FDR estimates is in Supplementary Table S8.

### Simulation limitations

The simulation abstracts from several real-data complications: LD was modeled as discrete block correlation rather than the full 1000 Genomes LD matrix; the L3 architecture gate used a per-block spread proxy rather than empirical LDSC rg and colocalization; and the L4 conditional effect used a leave-one-out robustness proxy rather than a full multivariable MR. The simulation thus quantifies the framework's behavior under controlled stress tests but does not replace the empirical validation cohort. The empirical cohort remains the primary demonstration; the simulation is a complementary characterization.

---

## Discussion

### Central advance: a validation framework, not another comorbidity MR finding

This paper's contribution is not the specific conclusion about insomnia and AD — that pair is a demonstration — but the **causal-claim validation framework** it introduces. Routine MR asks "is the IVW significant?" and, if MR-Egger and PRESSO do not contradict it, publishes a causal claim. That pipeline produced the insomnia→AD finding at β = +0.10 (P = 9 × 10⁻⁴); it is reproducible, and it survives conventional sensitivity checks. What it does not survive is the single most basic instrument-validation check: LD-clumping reverses the estimate to null and non-significant (P = 0.52–0.64). The original result was correct within the standard workflow; the workflow itself is not designed to falsify its own output.

The six-level framework inverts the logic. Each level tests whether the claim survives a specific failure mode of causal inference under polygenicity: instrument dependence, overlap, locus-limited sharing, confounding, missing mechanism, and poor generalizability. The severity of the tests survived, not the number of methods passed, determines the strength of a causal claim [10-11,37]. The formal rationale for the hierarchy — why six levels, why this order, what information each gate contributes — is detailed in Methods (Framework architecture).

### Why polygenic architecture inflates MR — and why falsification is the remedy

The insomnia→AD example illustrates a general mechanism. Unclumped UVMR recapitulates the published signal (β = +0.104, P = 9.3 × 10⁻⁴), but this precision is an artefact of 2,462 correlated instruments concentrated in a single LD landscape. Clumping, overlap correction, and MVMR each constrain the effect to null or negative — a convergence of complementary methods (instrument dependence, sample overlap, direct-effect adjustment), not independent votes. The apparent comorbidity arises not from a genome-wide causal relationship but from APOE-centered locus-specific shared liability. LD-clump sensitivity analysis should be reported as a default for any MR-based causal claim, particularly in comorbidity pairs where a single genomic region may drive both traits' associations [8-9,20,40].

### Reconciling with the published insomnia–AD MR literature

Our findings do not contradict earlier positive reports; they contextualize them. The unclumped signal we reproduce closely matches published estimates [2-5], confirming the underlying data are correct. The issue is interpretive: the signal exists in unclumped data but reflects LD structure rather than a genome-wide causal relationship. Published studies that did not report clumped-versus-unclumped contrasts may have over-interpreted correlated-instrument inflation as biology [41-44]. We note three self-reinforcing factors: early pipelines (2017–2020) often defaulted to IVW without clump-sensitivity checks; the first positive report may have seeded a citation cascade replicating the same blind spot; and reviewers have not routinely requested instrument-independence reports. The framework presented here provides a constructive template for re-evaluating similarly positioned comorbidity claims.

### Colocalization asymmetry and the limits of Steiger

The reverse-dominant colocalization (18/32 vs. 1/47 loci) is a signature of shared liability: a common APOE ε4 variant elevates both traits, creating apparent bidirectional epidemiology [45-46]. Colocalization establishes a shared causal variant, not direction; triangulation with null rg and null-to-negative forward MR favors shared liability. Steiger directionality testing proved uninformative here — its conclusion flipped with the method used to construct r from binary outcomes — and this is reported as a caution against its mechanical application in prevalence-discrepant comorbidity pairs, not as a limitation of Steiger per se.

### Framework validation and evidence grading

A validation framework is useful only if it both detects true effects and refrains from manufacturing them, across multiple disease domains. Discrimination was tested across 12 cases spanning 4 disease domains, scored against the six-level rubric (Methods — Framework architecture):

| # | Case | Domain | F | IVW P | Key MR finding | Score | Grade |
|---|------|--------|-----|-------|----------------|-------|-------|
| 1 | LDL→CAD | Lipid | 182 | 2.0 × 10⁻²⁰ | Robustly positive; all methods agree | 12 | **A** |
| 2 | Education→AD | Neuro | ~40 | 1.1 × 10⁻⁵ | Protective; mediation confirmed | 12 | **A** |
| 3 | BMI→T2D | Metabolic | 66 | 1.4 × 10⁻³ | Textbook positive; obesity→diabetes | 12 | **A** |
| 4 | Height→CAD | General | 79 | 6.1 × 10⁻⁸ | Genuine protective effect; framework correctly accepts even when not expected | 10 | **A** |
| 5 | Insomnia→AD (study) | Neuro | 38 | 0.52 (clumped) | LD-driven false positive; reclassified | 4 | **C** |
| 6 | BMI→Stroke | Neuro | 66 | 0.018 | IVW significant, WM null (P = 0.30) — pleiotropy-driven | 4 | **C** |
| 7 | HDL→CAD | Lipid | 151 | 8.9 × 10⁻⁴ | IVW significant, MR-Egger null (P = 0.89) — classic MR-corrected false therapeutic target | 4 | **C** |
| 8 | Depression→AD | Neuro | 37.9 | 0.014 | IVW sig (P = 0.014); WM P = 0.059 borderline; Egger int P = 0.119 | 5 | **C** |
| 9 | CRP→CAD | Inflam | 176 | 0.44 | Precisely null at extreme power (F = 176); framework correctly refrains | 2 | **D** |
| 10 | BMI→AD | Metabolic | 66 | 0.32 | Cleanly null; framework rejects a contested relationship | 1 | **D** |
| 11 | T2D→AD | Metabolic | 77.8 | 0.71 | Clean null at high power (F = 78); correctly rejected | 1 | **D** |
| 12 | Education→T2D | Metabolic | 50 | 2.1 × 10⁻²⁶ | Strong protective; Egger int P = 0.036 + high heterogeneity → B; EAS replication IVW −0.145 (P = 0.012) | 9 | **B** |

Four confirmed positive effects received Grade A, including Height→CAD (a genuinely protective relationship that was intended as a negative control candidate — demonstrating the framework is not biased toward null). One borderline protective received Grade B (Education→T2D), where mild pleiotropy correctly downgrades from A. Four cases received Grade C: the LD-driven Insomnia→AD, the pleiotropy-driven BMI→Stroke (IVW P = 0.018 vs. WM P = 0.30), the MR-corrected HDL→CAD (IVW P = 8.9 × 10⁻⁴ vs. MR-Egger P = 0.89), and the new psychiatric-exposure → AD pair Depression→AD (IVW P = 0.014 but WM P = 0.059 borderline). HDL→CAD is particularly informative: it is the most widely cited example of MR overturning a false therapeutic target, and the framework's Grade C assignment is consistent with the cumulative clinical-trial evidence. Three cases received Grade D: BMI→AD, CRP→CAD (null at extreme instrument strength, F = 176), and T2D→AD (null at F = 78). Internal specificity is corroborated by 25/25 null protein mediators coexisting with significant education→AD, LDL→CAD, and TG-mediation effects. Full per-level scoring for all twelve cases is provided in Supplementary Table s7.

The IEU OpenGWAS catalog was systematically searched for candidate negative controls (probing ~120 GWAS IDs across ~50 traits), evaluating each for (i) biological implausibility, (ii) instrument strength F > 50, and (iii) functional summary-statistics extraction. Height→AD was the only candidate passing all three criteria; its IVW was pleiotropy-driven (MR-Egger P = 0.44; heterogeneity P = 5 × 10⁻⁵) and is archived in Supplementary Table S6. The height→CAD result (Grade A) confirms that height is a genuine protective exposure for multiple outcomes, rather than a suitable negative control. The expanded twelve-case cohort spans four disease domains and the full grade spectrum (A: 4, B: 1, C: 4, D: 3), with simulation-based operating characteristics (sensitivity 0.97 / specificity 1.0 in the ideal scenario; FDR ≤ 0.18 under directional pleiotropy) reported in Results and Supplementary Fig. 5.

Inter-rater reliability analysis confirmed that the grading rubric yields reproducible results across independent evaluators. A second rater blinded to the original per-level scores independently applied the same 0–1–2 per-level, 0–12 cumulative rubric to all twelve cases. Grade-level agreement was 10/12 (raw agreement 0.83). Cohen's κ at the grade level was 0.76 (substantial agreement by Landis–Koch criteria); quadratic-weighted κ, which penalises larger disagreements more heavily, was 0.94 (almost perfect). At the individual-gate level (72 items: 6 gates × 12 cases), the per-level κ was 0.89. The two disagreements were both one-grade-adjacent: Height→CAD (Rater 1: Grade A, 10/12; Rater 2: Grade B, 9/12), reflecting a stricter interpretation of the genetic architecture gate (L3), and Education→T2D (Rater 1: Grade B, 9/12; Rater 2: Grade A, 10/12), reflecting a more lenient reading of the direct-effect gate (L4). No case differed by more than one grade, and the three unanimous Grade A (LDL→CAD, Education→AD, BMI→T2D) and three unanimous Grade D (CRP→CAD, BMI→AD, T2D→AD) assignments at the spectrum extremes confirm that the framework cleanly separates high-confidence causal relationships from unsupported claims.

### Implications for comorbidity MR practice

The insomnia→AD recalibration illustrates a broader lesson about the credibility of causal claims in polygenic epidemiology. Phenotypic comorbidity predisposes researchers to causal interpretations; a positive unclumped MR reinforces this; and absent instrument-independence testing, the artefact goes undiscovered. Any causal claim resting on polygenic evidence — MR-based or observational — should clear at least the first two gates (association and robustness) by default; high-confidence claims require passage through all six. The framework extends this minimum into a systematic architecture applicable to other contested pairs — e.g., depression→cardiovascular disease, rheumatoid arthritis→AD, or type 2 diabetes→PD — wherever published MR or single-method observational claims rest on unclumped or un-replicated analyses [1,7].

### Translational implications for drug-target development

The framework also speaks to the genomic-medicine pipeline, in which MR is now routinely used to prioritize drug targets before clinical investment. The grade assignments in this study map onto well-documented translational histories. LDL→CAD received Grade A, consistent with the MR evidence base that anticipated the cardiovascular benefit of statin therapy and PCSK9-targeting approaches [39]. HDL→CAD received Grade C: the unclumped IVW estimate is significant (P = 8.9 × 10⁻⁴) but MR-Egger is null (P = 0.89), and the framework classifies the signal as pleiotropy-driven rather than causal — the verdict ultimately delivered by clinical trials in which torcetrapib raised HDL cholesterol without reducing cardiovascular events [47-48], and by MR analyses showing no causal effect of HDL on myocardial infarction [47]. Applied before trial investment, the robustness and architecture gates would have flagged the fragility of the HDL target on genetic evidence alone, without waiting for a failed trial. The converse risk — falsely rejecting a true protective effect — is equally addressed: education→AD received Grade A, and its triglyceride-mediated protective component (indirect effect −0.031, bootstrap P < 0.001) survived the biological-mediation gate, consistent with the cognitive-reserve literature [19] and positioning education as a modifiable, polygenic-protective exposure of translational relevance for AD prevention. The insomnia→AD recalibration carries a subtler clinical message: sleep disturbance remains a modifiable exposure of public-health importance, but the genetic evidence locates its comorbidity with AD in APOE-centered shared liability rather than a directed causal pathway, so sleep-focused interventions should not be justified by an unverified claim of AD risk reduction. For genomic medicine, a six-gate triage of genetically supported targets — instrument independence, overlap correction, genetic architecture, direct effect, mediation, and ancestry transferability — offers a low-cost, pre-clinical de-risking step complementary to conventional target validation, with ancestry transferability assessed before single-ancestry targets are advanced.

### Beyond MR: a general framework for causal claims in -omics epidemiology

Although operationalized and validated here through Mendelian randomization, the six-level framework is not an MR-specific procedure. Its logic — graded falsification gates applied to a body of polygenic evidence — applies wherever correlated evidence can be mistaken for a causal signal: observational triangulation that pools multiple weak instruments, phenome-wide scans that test thousands of exposure–outcome pairs, and multi-omics mediation that chains protein and metabolite intermediates; the same logic underpins polygenic evidence integration in multi-omics, structural-equation, exposome-wide, and phenome-wide settings [49-57]. Any highly polygenic exposure–outcome pair can be evaluated through the same evidence hierarchy because the framework's logic does not depend on trait biology. The primary determinants of the applicable evidence grade are instrument strength, LD architecture, pleiotropy, and ancestry coverage — not the biological content of the traits themselves. Setting uniform quality-control thresholds at each level (e.g., requiring clumped-versus-unclumped IVW comparison, MRlap overlap correction, and coloc PP.H4 ≥ 0.80) transforms the framework from an MR proof-of-concept into a reusable causal-claim evaluation standard for -omics epidemiology more broadly. A decision-tree visualization (Supplementary Figure 4) encodes these thresholds into a practical flowchart.

### How this changes causal-inference practice

The framework carries specific operational implications that extend beyond MR to anyone publishing a causal claim from -omics data.

For researchers reporting comorbidity MR or observational causal analyses: the minimum expectation should be that every paper reports both clumped and unclumped IVW estimates as a standard sensitivity analysis, analogous to the convention of reporting both fixed-effect and random-effect meta-analyses. This single additional column in a results table allows post hoc re-evaluation of published claims without requiring access to raw data. For reviewers and editors: the six-level scoring rubric provides a transparent standard against which to evaluate submitted causal-inference papers — a Grade C or D assignment does not automatically disqualify a study, but it requires the authors to discuss whether their signal reflects shared liability rather than directed causality. For GWAS consortia, biobanks, and observational epidemiologists: pre-harmonized reference panels for framework-aligned reporting — a common LD reference panel, coloc-ready LD matrices, and a curated set of negative-control outcome GWAS — would reduce the technical burden of adoption and could be integrated into existing summary-statistics deposition standards.

STROBE-MR [12] specifies what should be reported in every MR study; the present framework specifies when the reported evidence is sufficient to sustain a causal claim at a given confidence grade. The two are complementary — a reporting standard and an evidentiary threshold — and together they provide a basis for evaluating causal claims in polygenic epidemiology with the rigor that modern architectures now demand.

### Scope of falsification in the framework

The term "falsification" in this framework refers to the rejection of an independent, directional, genome-wide causal claim — not to the absolute denial of any biological relationship between two traits. Comorbidity by definition involves shared biology; the framework distinguishes whether that shared biology reflects locus-specific pleiotropy (e.g., APOE) or a robust directed causal pathway (e.g., LDL→CAD). A Grade C or D assignment does not mean the two traits are biologically unrelated; it means the available MR evidence does not support a high-confidence directional causal interpretation under the current instrument set and data structure. The cumulative scoring system quantifies the severity of the tests survived, rather than declaring "true" or "false" in absolute terms. The insomnia–AD pair illustrates this: APOE-centered shared liability is well-established, but the claim of a directed insomnia→AD independent causal pathway is not supported by the convergent evidence.

### Limitations

Several limitations remain. First, the framework validation cohort of twelve cases, while spanning four disease domains and the full grade spectrum (A: 4, B: 1, C: 4, D: 3), remains modest in absolute size; a larger cohort specifically enriched for borderline-ambiguous pairs (Grades B and C) would better characterize the framework's decision boundaries. Second, simulation studies characterizing operating characteristics across LD architectures, pleiotropy strengths, and sample overlap scenarios have now been performed (43,200 replicates; Supplementary Fig. 5) and confirm 0.97 sensitivity / 1.00 specificity in the ideal scenario with FDR ≤ 0.18 under directional pleiotropy, but the simulation abstracts from real-data complications (discrete LD blocks rather than full 1000G LD matrices; leave-one-out proxy for L4 multivariable MR; discrete second-sample noise for L6 rather than a true cross-ancestry dataset). A threshold-sensitivity analysis across four configurations (Supplementary Note 1) confirms that no case changes by more than one grade under any scenario. Third, the directional external validation gate (Level 6) covers five cross-ancestry checks — education→AD (EAS GARD), education→T2D (EAS BBJ; significant replication), T2D→AD (EAS GARD; null concordance), education→stroke (EAS BBJ; null), and a trans-ethnic insomnia→AD check (EUR instruments transferred into GARD EAS AD; negative, non-significant) — but these remain directional-screening checks with limited instrument counts (9 for education, 30 for the insomnia→AD trans-ethnic transfer, 71–96 for T2D) rather than formal independent-replication layers with effect-size precision; power was sufficient for directional-consistency testing only (power ≥ 84% at R² ≥ 0.05 for education→AD; < 6% for the insomnia→AD transfer). Depression→AD was not subject to adequately powered cross-ancestry replication within this study, and we document why a formal check is currently infeasible (Supplementary Note 3). The EAS clinical MDD exposure stratum of the largest multi-ancestry MDD GWAS (Meng et al. 2024, Nat Genet; 7,886 cases / 14,412 controls) contains **no genome-wide-significant variants** (min P = 1.9 × 10⁻⁷ across 8.1 M variants), so no EAS depression instruments can be constructed; the multi-ancestry version yields six independent MDD loci, of which only two are present with harmonizable alleles in the sole EAS AD outcome available (GARD, 2,919 cases), precluding a meaningful MR estimate. An exploratory two-instrument direction check is reported for transparency (both point toward a positive AD direction in EAS, within noise), but is not used as evidence for or against the Depression→AD Grade C assignment. This is a power and data-coverage limitation rather than a null result, and should be revisited as larger EAS depression and AD GWAS become available. This gate is therefore a cross-ancestry directional screening check rather than a formal independent-replication layer. Fourth, the mediation gate (Level 5) is inherently constrained by the coverage of the available proteomic and metabolomic GWAS data; absence of detectable mediation does not conclusively disprove the existence of an unmeasured biological pathway. Fifth, CAUSE returned a nominally causal forward signal for insomnia→AD that is methodologically compatible with but not resolved by the converging null estimates from clumped IVW, MRlap, and MVMR; as GWAS sample sizes increase, CAUSE resolution will improve, and this residual signal should be revisited. Sixth, the specificity estimate derives from a single formally computed negative control (BMI→AD), as our systematic search of ~120 GWAS IDs across ~50 candidate exposures in the IEU OpenGWAS catalog found no second candidate simultaneously passing our biological-implausibility, instrument-strength (F > 50), and technical-extraction criteria — height→AD being the only candidate meeting all three, but itself contaminated by pleiotropy (Supplementary Table S6).

Operational thresholds for each gate are detailed in Methods (Framework architecture) and summarized in Supplementary Figure 4.

## Conclusions

The insomnia–AD case demonstrates that a causal claim should be accepted only after it has survived independent attempts to falsify it, not after a single analytical layer has produced a significant estimate. The six-level framework converted a widely replicated positive MR finding into a graded verdict — shared liability rather than directed causation — while correctly retaining high-confidence grades for genuine effects (LDL→CAD, education→AD) and precisely null claims (BMI→AD, CRP→CAD, T2D→AD). Its logic is not MR-specific: any polygenic causal claim, in epidemiology or genomic medicine, can be evaluated through the same falsification gates, and the A/B/C/D rubric provides a transparent standard for drug-target prioritization, reporting, and review. The primary determinants of the applicable grade — instrument strength, LD architecture, pleiotropy, and ancestry coverage — are data properties rather than trait biology, making the framework a reusable evidentiary threshold for causal claims in polygenic epidemiology.

## List of abbreviations

AD: Alzheimer's disease; BMI: body mass index; CAUSE: Causal Analysis Using Summary Effect Estimates; coloc: Bayesian colocalization; CRP: C-reactive protein; EAS: East Asian; FDR: false discovery rate; GWAS: genome-wide association study; HDL: high-density lipoprotein; IL-6: interleukin-6; IVW: inverse-variance weighted; LD: linkage disequilibrium; LDSC: LD Score regression; LDL: low-density lipoprotein; MR: Mendelian randomization; MRlap: MR with sample-overlap correction; MVMR: multivariable Mendelian randomization; PheWAS: phenome-wide association study; pQTL: protein quantitative trait locus; PRESSO: Pleiotropy RESidual Sum and Outlier; rg: genetic correlation; SE: standard error; SNP: single-nucleotide polymorphism; T2D: type 2 diabetes; TG: triglycerides; UKB: UK Biobank; UVMR: univariable Mendelian randomization; WM: weighted median.

---

## Methods

### Study design overview

We designed a six-level causal-claim validation framework (Fig. 1) for evaluating causal claims in polygenic epidemiology, operationalized here through Mendelian randomization under extreme polygenicity. Each level is a falsification gate addressing a progressively stricter question. Although validated on MR cases, the framework is intended as a general causal-inference tool whose logic — graded falsification gates over correlated evidence — extends to observational triangulation and multi-omics settings. The framework was applied to the insomnia–AD pair, with educational attainment and LDL→CAD analyzed as positive controls and BMI→AD as a negative control.

### Framework architecture and theoretical rationale

The framework's six levels correspond to a logical decomposition of the causal-inference problem into six irreducible layers of hypothesis testing. Each level is not merely an additional MR method, but a distinct falsification gate that detects a class of false-positive causal claims that no previous level can resolve. The sequence is non-arbitrary and follows the natural progression of causal evidence from weakest to strongest:

| Level | Gate | Failure mode detected | Unique information | Undetectable by prior levels |
|-------|------|----------------------|-------------------|------------------------------|
| 1 | Association | No signal; null true | Does a raw genetic signal exist? | — |
| 2 | Robustness | LD-inflated false positive; sample overlap | Is the signal robust to instrument (in)dependence? | L1 cannot distinguish LD-driven from biology-driven signal |
| 3 | Genetic architecture | Locus-specific shared liability masquerading as genome-wide causality | Is the association genome-wide (rg) or locus-limited (coloc)? | L2 cannot resolve which genomic regions contribute to the signal |
| 4 | Direct effect | Confounded MR estimate | Does the effect survive multivariate adjustment? | L3 cannot rule out confounding by correlated exposures |
| 5 | Biological mediation | No mechanistic support | Is there a genetically proxied pathway? | L4 cannot establish biological plausibility |
| 6 | External validation | Population-specific artefact; framework itself invalid | Does the conclusion replicate across ancestry and against controls? | L5 cannot verify that the inference generalises |

**Why this order.** Levels 1–2 are statistical prerequisites: a failure at either gate is sufficient to halt the cascade, because downstream inquiries are moot if the underlying signal is artefactual (unclumped) or biased by sample overlap. Level 3 — distinguishing genome-wide architecture from locus-specific sharing — addresses the most common misinterpretation in comorbidity MR and must precede the direct-effect (Level 4) and mechanism (Level 5) gates, because a shared genetic liability (e.g., APOE) cannot be interpreted as a directed causal pathway regardless of downstream mediation or MVMR results. Levels 4 and 5 separate confounding from mechanism. Level 6 provides external anchoring against known positives and negatives. The hierarchy is **cumulative in evidentiary strength** but **disjunctive in falsification**: a single failure suffices to downgrade the evidence grade.

**Quantitative scoring.** To replace a binary pass/fail judgment with a graded evidence assessment, each level is scored 0, 1, or 2: 0 indicates the gate is failed (no evidence of a causal signal at this level); 1 indicates the gate is partially passed (evidence is present but incomplete or qualified); 2 indicates the gate is fully passed (all criteria at this level are met). This ternary scoring follows graded evidence-assessment logic, in which categorical ratings avoid the false precision of continuous weighting schemes and the final grade reflects the weakest surviving link rather than an average. The six-level sum yields a total score of 0–12, which maps to a four-tier evidence grade:

| Total score | Grade | Interpretation | Strategy |
|-------------|-------|---------------|----------|
| 10–12 | **Grade A** (High confidence) | All six levels passed convincingly | Strongest causal claim; suitable for clinical translation |
| 7–9 | **Grade B** (Moderate) | Most levels pass, one or two with reservations | Causal evidence strong but external validation or mechanism incomplete |
| 4–6 | **Grade C** (Weak / shared liability) | Raw association present but robustness or architecture gate failed | Triangulation supports shared liability rather than directed causality |
| 0–3 | **Grade D** (Not supported) | Failed at statistical or robustness gates | No causal claim warranted; do not use for MR-informed decisions |

Applied to the validated cases: LDL→CAD scores 12/12 (all gates fully passed) → Grade A. Educational attainment→AD scores 12/12 (all gates passed; TG mediation supports L5, cross-ancestry directional consistency supports L6) → Grade A. Insomnia→AD scores 4/12 (L1=2: unclumped significant; L2=0: clump reversal; L3=1: rg≈0 with APOE-only coloc asymmetry; L4=1: MVMR direct effect null; L5=0: no protein mediator; L6=0) → Grade C. BMI→AD scores 1/12 (L1=1: significant IVW in unclumped but borderline; L2=0; L3–6=0) → Grade D.

**Pre-specified logic and anti-post-hoc justification.** The six-level hierarchy was defined before analysis of the insomnia–AD pair and was not iteratively adjusted after seeing results. Each level addresses a distinct failure mode of causal inference under polygenicity that no previous level can detect: signal absence (L1), LD/overlap artefacts (L2), locus-limited sharing misinterpreted as genome-wide causality (L3), confounding by correlated exposures (L4), missing mechanistic support (L5), and population-specific or framework-specific validity (L6). The non-arbitrary order follows the natural progression from statistical screening to biological evidence to external generalization. A two-level pipeline (L1+L2) would flag LD-driven false positives but miss shared-liability misinterpretations; a three-level pipeline (L1–L3) would distinguish architecture but miss confounded or non-mechanistic signals; the full six-level pipeline is the only configuration in which all major classes of false causal claims are formally testable. Control-sample selection was systematic (probing ~120 IEU GWAS IDs; see External validation cohort), and the final set of twelve validation cases was finalized before grading.

**Inter-rater reliability.** To assess whether the 0–1–2 per-level scoring rubric yields reproducible grades across independent evaluators, a second rater blinded to the original per-level scores independently applied the same rubric to all twelve validation cases using only the published evidence summaries summarised in Supplementary Table s7. Cohen's κ was computed at the grade level (A/B/C/D) with both unweighted and quadratically weighted variants (the latter penalises gap disagreements—e.g., Grade A vs Grade C—more severely than adjacent disagreements—e.g., Grade A vs Grade B) and at the individual-gate level (0–1–2 across six gates and twelve cases, 72 items).

### Data sources

**Primary GWAS datasets** (all GRCh37 unless noted): [13-17,31,36,58,59-62]

| Trait | GWAS ID / Source | Ancestry | N (N_case) | Instruments after LD-clumping |
|-------|-----------------|----------|-----------|-------------------------------|
| Insomnia | ukb-b-3957 (Ben Elsworth 2018) | EUR | 462,341 | 54 (loose); 37 (tight) |
| AD (primary) | ieu-b-2 (Kunkle/IGAP 2019) | EUR | 63,926 (21,982) | 13 (forward); variable per analysis |
| AD (replication) | ebi-a-GCST90027158 (Bellenguez 2022) | EUR | 487,511 (85,934) | variable per analysis |
| Educational attainment | ieu-a-1239 (Lee 2018; college completion) | EUR | 117,487 | 317 |
| Type 2 diabetes | ebi-a-GCST006867 (Xue 2018) | EUR | ~62k cases | 118 |
| Major depression | ieu-b-102 (Howard 2019) | EUR | 500,199 (170,756) | 50 |
| EA educational attainment | GCST90296498 (Chen/Kim/Lam 2024) | EAS | 165,232 | 100 |
| EA AD | GARD/NG00182 | EAS | 6,518 (2,919) | lifted to GRCh37 |
| EA Type 2 diabetes | bbj-a-77 (BBJ) | EAS | 191,764 (36,614) | 96 |
| EA ischemic stroke | bbj-a-129 (BBJ) | EAS | 210,054 (17,671) | — |

> For the core pair (insomnia→AD), no adequately powered EAS insomnia exposure GWAS exists (largest EAS insomnia case–control, GCST90018649, contains 389 cases); a trans-ethnic check transferring 40 EUR LD-independent insomnia instruments into GARD EAS AD was performed instead (Methods, Level 6; Supplementary Note 2).

**Protein pQTL data**: INTERVAL (Sun et al. 2018; n = 3,301) via IEU OpenGWAS (prot-a-1…2200) [30]. The curated 36-protein screen selected AD-relevant proteins (complement/innate immunity, chemokines/interleukins, cathepsins, YKL-40) with ≥15 instruments [30,32,63-65].

**Metabolite GWAS data**: Nightingale Health metabolomics (Kettunen et al. 2016) via IEU OpenGWAS: Total_C, LDL_C, HDL_C, Total_TG, DHA, Omega_3, Ile, Leu, Val, GlycA [33].

**LD reference panels**: 1000 Genomes Phase 3 European panel (HM3) for clumping; pre-computed LD Scores for LDSC [66].

**External validation cohort**: Positive control: LDL cholesterol (ieu-a-300; Global Lipids 2013, n = 188,577) → coronary artery disease (ieu-a-7; CARDIoGRAMplusC4D 2015, n = 184,305 with 60,801 cases), a textbook causal relationship supported by statin RCTs and MR concordance [39]. Negative control: BMI (ieu-a-2; GIANT/UKB 2015, n = 339,153) → AD (ieu-b-2), tested under the full falsification pipeline (clumped instruments, F = 65.6, two-sample MR).

### Level 2 — Robustness: UVMR with LD-clump sensitivity, MRlap, CAUSE

Bidirectional UVMR used TwoSampleMR (v0.6.8) [6,8-9]. Instruments extracted at P < 5 × 10⁻⁸ and harmonized. Two clump thresholds: loose (r² < 0.001, 10,000 kb) and tight (r² < 0.001, 5,000 kb). **MRlap** (v0.0.3.1) corrected for sample overlap [24]. **CAUSE** (v1.2.2) partitioned effects on 1,645 independent variants [24].

### Level 3 — Genetic architecture: LDSC and colocalization

LDSC (v1.0.1) estimated rg using pre-computed European LD Scores; chromosome-19 removal tested APOE-driven inflation [25]. Colocalization used coloc (v5.2.3); coloc.abf with PP.H4 ≥ 0.80 threshold; ±500 kb windows around exposure lead SNPs; forward and reverse against Kunkle and Bellenguez [16-17,27].

### Level 4 — Direct effect: MVMR and PheWAS

MVMR (MVMR package) jointly modeled insomnia, educational attainment, depression, and LDL-cholesterol against AD [67]. Exposure selection was hypothesis-driven via a minimal confounding diagram: insomnia (primary exposure), educational attainment (a priori protective control), depression (leading shared-pleiotropy confounder), and LDL-cholesterol (principal lipid risk factor / candidate mediator) [28-29]. PheWAS tested education instruments against AD (Kunkle, Bellenguez), PD (Nalls 2019), and MS (IMSGC) [68-69].

### Level 5 — Biological mediation: two-step MR

Protein mediation (G2): insomnia→CRP/IL-6→AD two-step MR; G2b curated 36-protein screen with education as exposure (317 instruments) and Benjamini–Hochberg FDR across 25 evaluable proteins [30,31,70-75] (AD blood-based protein biomarker context: p-tau, GFAP, NfL). Metabolite mediation (C1): educational attainment→10 metabolites→AD; FDR across 10 metabolites [33]. Indirect effect = β₁ × β₂ with delta-method SE; bootstrap 95% CIs (5,000 resamples).

### Level 6 — Directional external validation: cross-ancestry and control discrimination

East Asian (EAS) directional consistency used EAS educational attainment instruments (Chen/Kim/Lam 2024, GCST90296498; n = 165,232; 9 distance-clumped instruments at kb = 10 Mb) as exposure against three EAS outcomes: GARD AD (NG00182; n = 6,518, 2,919 cases; lifted GRCh38→GRCh37 via liftOver), BioBank Japan type 2 diabetes (bbj-a-77; n = 191,764, 36,614 cases), and BioBank Japan ischemic stroke (bbj-a-129; n = 210,054, 17,671 cases). All BBJ outcomes were extracted and harmonized through TwoSampleMR; GARD was matched positionally (chr:pos) with allele-flip harmonization [76]. T2D→AD EAS consistency additionally used BBJ T2D instruments (96 clumped at r² < 0.001, 10 Mb) against GARD EAS AD with position-based matching (71 matched). For the primary study pair, a trans-ethnic directional check used 40 LD-independent EUR insomnia instruments (ukb-b-3957, LD-clumped at r² < 0.001, 10 Mb against the 1000 Genomes Phase 3 EUR reference) transferred into GARD EAS AD by position (hg19) with allele-flip harmonization (30/40 matched); IVW, weighted median, and MR-Egger were computed as in the EA pipeline (code/ea05_transethnic_insomnia_ad.py). No adequately powered EAS insomnia exposure GWAS exists (largest EAS insomnia case–control study, GCST90018649, contains 389 cases), so the EAS-insomnia-instrument design used for education was not possible for the core pair. Power for directional-consistency testing was assessed via mRnd [13,36]. Control discrimination evaluated the framework against two positive controls (LDL→CAD, education→AD), one computed negative control (BMI→AD), and the study case (insomnia→AD), with cross-ancestry checks on the three new validation cases (Education→T2D, T2D→AD) and the previously reported education→AD pair.

### Instrument validity, sensitivity diagnostics, and statistical power

Per-SNP F-statistics (β_exposure/se_exposure)²: forward insomnia→AD mean F = 38.5 (min 29.7), no instrument below F = 10. Cochran's Q for clumped forward IVW: Q = 3,660, df = 2,461, P = 1.3 × 10⁻⁵⁰; MR-PRESSO global distortion non-significant (distributed, not outlier-driven pleiotropy); reverse MR-Egger intercept significant. Leave-one-out (40 clumped instruments): IVW range [−0.238, −0.033] (mean −0.128), zero sign flips. Power (Brion 2013; mRnd): clumped ~7% to detect β = 0.10, requiring β ≥ 0.57 for 80%; unclumped >99% [22-23].

### Simulation operating characteristics

To characterize the framework's sensitivity, specificity, and false-discovery rate (FDR) across controlled stress conditions, we generated polygenic two-sample MR summary statistics with **known ground truth** (causal β ∈ {0, 0.08, 0.15} per-SD units). Instrument effects were drawn from bx ~ N(0, 0.12) per SNP (mean per-SNP F ≈ 36), with correlated LD-block structure (n_blocks ∈ {5, 12, 40}, representing high, medium, and low LD concentration) to capture LD-induced instrument dependence. Outcome effects γ_y = β·bx + pleiotropy_term + noise, with three pleiotropy regimes: **none** (γ_y = β·bx), **balanced** (γ_y = β·bx + u, u ~ N(0, 0.04), mean-zero), and **directional** (γ_y = β·bx + u + 0.03, positive bias). Sample overlap was controlled at ρ ∈ {0, 0.3} by inducing correlated sampling noise. A two-step mediator (X → M → Y) was generated **only when the true effect β > 0**, with mediation strengths a = 0.40 (X → M instrument effect) and b = 0.50 (M → Y), so that null replicates did not spuriously pass the L5 mediation gate. An independent second sample with fresh noise was generated for the L6 directional-consistency check.

Each replicate (n = 43,200 total: 3 LD × 3 pleio × 2 overlap × 3 effect × 2 n_iv × 400 reps) was scored by all six framework gates — L1 unclumped IVW significance; L2 clumped IVW significance with no MR-Egger directional pleiotropy; L3 architecture spread across LD blocks; L4 leave-one-out robustness as direct-effect proxy; L5 two-step mediation (X→M and M→Y both p < 0.05); L6 independent-sample directional consistency — and assigned Grade A/B/C/D by the 0–12 cumulative rubric. **L1 failure cascades to Grade D** (disjunctive falsification), matching the manuscript framework. Operating characteristics were aggregated by scenario: sensitivity = P(grade ∈ {A, B} | true effect > 0), specificity = P(grade = D | null), and FDR = P(effect = 0 | grade ∈ {A, B}) within each scenario (LD × pleio × overlap × n_iv). Implementation: `code/sim_framework_operating_chars.py` (seed 20260804).

### Software and reproducibility

R (v4.5.2) and Python (v3.13). Packages: TwoSampleMR (v0.6.8), coloc (v5.2.3), MRlap (v0.0.3.1), cause (v1.2.2), MVMR (v0.4), ieugwasr (v1.0.0); numpy, scipy, pandas, matplotlib, seaborn. Code, cached inputs, and reproducible analysis scripts have been deposited in a public GitHub repository (https://github.com/ming13333/iad-falsification-framework) and archived via Zenodo https://doi.org/10.5281/zenodo.21858125 upon submission. The six-level framework and the analysis plan were defined a priori before the analyses and are documented in Methods (Framework architecture and theoretical rationale).

### AI assistance in writing

A large language model (the WorkBuddy AI assistant, powered by DeepSeek) was used to assist with drafting and refining the manuscript text for language clarity and structure. All AI-generated or AI-modified text was reviewed, edited, and verified by the authors against primary sources; the authors take full responsibility for the accuracy and integrity of the manuscript. No AI tools were used to generate data, statistical analyses, or figures; all computational results were produced by the authors using standard statistical-genetics software (TwoSampleMR, LDSC, coloc, MVMR) in R and Python. No AI system is listed as an author.

---

## Figure Legends

**Figure 1. A six-level falsification framework for causal claims in polygenic epidemiology.** *Panel a: Six-level evidence hierarchy.* Each level is a gate that can independently reject a directional causal claim: (1) Association, (2) Robustness (instrument-independence and overlap), (3) Genetic architecture (genome-wide vs locus-specific), (4) Direct effect (multivariable adjustment), (5) Biological mediation, (6) External validation (cross-ancestry + positive/negative controls). A high-confidence causal claim requires passage through all six; failure at any single gate suffices to falsify the directed interpretation. *Panel b: Framework versus traditional single-layer causal inference.* The traditional pipeline (left), exemplified by a conventional MR workflow, accumulates supporting evidence within a single analytical layer and declares completion once sensitivity checks such as MR-Egger and PRESSO do not contradict the IVW. The six-level framework (right) inverts the logic: each diagnostic is a falsification gate, and the cumulative output is a quantified evidence grade (A/B/C/D) rather than a binary supported/rejected verdict. *Panel c: Framework synthesis applied to insomnia–AD.* Each layer maps the insomnia–AD evidence to a corresponding analytical dimension; the synthesis row converges on Quadrant III (shared APOE-locus liability; no independent causal upstream).

**Figure 2. Robustness gate — MR forest and colocalization summary.** (A) Bidirectional estimates across methods (unclumped IVW, clumped IVW, MRlap, CAUSE, MVMR) for insomnia–AD. (B) Colocalization PP.H4 for forward (47 loci) and reverse (32 loci) directions, APOE region annotated.

**Figure 3. Direct-effect gate — educational attainment PheWAS.** Forest of education→outcome MR across AD (Kunkle), AD (Bellenguez), PD, and MS, with IVW, weighted median, weighted mode, MR-Egger.

**Figure 4. Mediation gate — protein and metabolite two-step MR.** (A) insomnia→CRP/IL-6→AD; (B) education→CRP/IL-6→AD (exposure substitution); (C) G2b 36-protein screen volcano and top-15 forest; metabolite mediation forest for education→metabolite→AD.

**Figure 5. Validation cohort — quantitative evidence grading.** Twelve evaluated cases scored on the 0–2 per-level, 0–12 cumulative scoring system, spanning four disease domains (A: 4, B: 1, C: 4, D: 3). The full rubric follows the framework architecture detailed in Methods.

## Supplementary Information

**Supplementary Figures**

- **Supplementary Figure 3A**: insomnia → plasma CRP/IL-6 → AD forest
- **Supplementary Figure 3B**: education → CRP/IL-6 → AD (exposure substitution)
- **Supplementary Figure 3C**: G2b 36-protein screen volcano and top-15 forest
- **Supplementary Figure 4**: Decision-tree flowchart for applying the six-level evidence-grading framework to any polygenic exposure–outcome pair. Encodes the practical algorithm: MR IVW significant → LD-clump robust → CAUSE/MRlap consistent → coloc rg architecture → MVMR direct effect → biological mediation → external validation → assign Grade A/B/C/D.
- **Supplementary Figure 5**: Simulation operating characteristics. Panel A: sensitivity vs effect size, by pleiotropy regime. Panel B: specificity and FDR by pleiotropy. Panel C: grade assignment distribution across null / weak / moderate effect × pleiotropy conditions.

**Supplementary Tables**

- **Supplementary Table S1**: Complete colocalization results (129 loci)
- **Supplementary Table S2**: Instrument sensitivity (unclumped vs. clumped, 4 methods)
- **Supplementary Table S3**: Complete MVMR/UVMR results matrix (27 rows)
- **Supplementary Table S4**: Educational attainment PheWAS (4 outcomes × 4 methods)
- **Supplementary Table S5**: STROBE-MR checklist [12]
- **Supplementary Table S6**: Exploratory height→AD analysis: 382 instruments (F = 78.4), IVW β = −0.107 (P = 0.002), MR-Egger β = −0.071 (P = 0.44), WM β = −0.089 (P = 0.063), Cochran Q = 431 (P = 5 × 10⁻⁵). Interpreted as directional pleiotropy; not used as a formal negative control.
- **Supplementary Table s7**: Twelve-case expanded validation cohort (LDL→CAD, Education→AD, BMI→T2D, Height→CAD, Insomnia→AD, BMI→Stroke, HDL→CAD, Depression→AD, Education→T2D, CRP→CAD, BMI→AD, T2D→AD) with full per-level 0–2 scoring, cumulative 0–12 total, F-statistics, IVW/WM/Egger estimates, and domain annotation. Available as CSV and Markdown in the Supplementary materials.
- **Supplementary Table S8**: Simulation operating characteristics across the LD-concentration × pleiotropy × sample-overlap × effect-size scenario grid (43,200 replicates; seed 20260804). Per-scenario CSV with sensitivity, specificity, FDR, and grade distribution; marginal summary by pleiotropy and effect size. Underlies Supplementary Fig. 5.

**Supplementary Notes**

- **Supplementary Note 1**: Threshold-sensitivity analysis of the A/B/C/D grade boundaries. Tests strict (+1), lenient (−1), and extreme-strict configurations; no case changes by more than one grade across any scenario.
- **Supplementary Note 2**: Cross-ancestry (East Asian) reinforcement of Level 6. Five East Asian checks: education→T2D (BBJ; IVW β = −0.145, P = 0.012 — significant replication), T2D→AD (GARD; β = +0.006, P = 0.93 — null concordance), education→stroke (BBJ; β = −0.008, P = 0.87 — underpowered null), education→AD (GARD; β = −0.029, P = 0.85 — directional consistency), and trans-ethnic insomnia→AD (EUR instruments → GARD; β = −0.84, P = 0.28 — negative directional consistency, severely underpowered, not graded). No framework-assigned direction contradicted in EAS.
- **Supplementary Note 3**: EAS depression replication feasibility. Documents why a formal East Asian depression→AD replication is currently infeasible: the EAS clinical-MD stratum of the largest multi-ancestry MDD GWAS (Meng et al. 2024) contains no genome-wide-significant variants, and the sole EAS AD outcome (GARD, 2,919 cases) covers only 2 of 6 multi-ancestry MDD loci; an exploratory two-instrument direction check is reported for transparency and does not affect the Depression→AD grade.

---

## Declarations

### Ethics approval and consent to participate

This study is a secondary analysis of publicly available genome-wide association study (GWAS) summary statistics and involves no new data collection, no human participants, and no personal data. Ethics approval and consent to participate were therefore not required.

### Consent for publication

Not applicable.

### Availability of data and materials

All GWAS summary statistics are publicly available via IEU OpenGWAS (https://gwas.mrcieu.ac.uk/) under the accessions listed in Methods. LDL→CAD (ieu-a-300 and ieu-a-7) and BMI→AD (ieu-a-2 and ieu-b-2) were computed within the IEU platform and are fully reproducible. UKB-PPP pQTL data (Sun et al. 2023, Nature) used for targeted verification are in published Supplementary Tables [32]. GARD/NG00182 East Asian AD GWAS is at NIAGADS (https://www.niagads.org/) [36]. The complete analysis pipeline — including all R/Python scripts (25 standardized modules), harmonized input data, caching layers for zero-API reproduction, and environment specifications — has been deposited in a public GitHub repository (https://github.com/ming13333/iad-falsification-framework) with a frozen Zenodo archive https://doi.org/10.5281/zenodo.21858125 and is freely available upon submission.

### Competing interests

The authors declare no competing interests.

### Funding

This study was not supported by any specific grant from funding agencies in the public, commercial, or not-for-profit sectors.

### Authors' contributions

M.L. and W.Y. contributed equally to this work. M.L. and W.Y. designed the study, performed all bioinformatic and statistical analyses, and drafted the manuscript. Q.L. conceived and supervised the study and provided critical revisions. All authors reviewed and approved the final manuscript.

### Acknowledgements

The authors thank the participants and investigators of the UK Biobank, the International Genomics of Alzheimer's Project (IGAP), the IEU OpenGWAS platform, the Biobank Japan (BBJ) Project, and the NIAGADS database for making GWAS summary statistics publicly available.

## Code Availability

All analysis scripts (R and Python) have been organized into a standardized, versioned codebase (25 R modules; complementary Python modules for figure generation, Steiger analysis, and East Asian replication) with documented environment specifications (renv.lock). Cached harmonized input data for the metabolite mediation module (C1) enable zero-API reproduction. The full repository has been deposited in a public GitHub repository (https://github.com/ming13333/iad-falsification-framework) with a frozen Zenodo archive https://doi.org/10.5281/zenodo.21858125 and is freely available upon submission.



## References

1. Davey Smith G, Ebrahim S. ‘Mendelian randomization’: can genetic epidemiology contribute to understanding environmental determinants of disease?. Int J Epidemiol. 2003;32(1):1–22. 10.1093/ije/dyg070.
2. Grover S, Sharma M. Sleep, Pain, and Neurodegeneration: A Mendelian Randomization Study. Front Neurol. 2022;13:765321. 10.3389/fneur.2022.765321.
3. Guo C, Harshfield EL, Markus HS. Sleep Characteristics and Risk of Stroke and Dementia. Neurology. 2024;102(5):e209141. 10.1212/WNL.0000000000209141.
4. Guo Y, Wang R, Sindi S, Middleton LT, Kivipelto M. Sleep and dementia: Assessing established dementia‐related factors using multivariable Mendelian randomization. Alzheimers Dement. 2026;22(6):e71592. 10.1002/alz.71592.
5. Sambou ML, Zhao X, Hong T, Wang N, Dai J. Associations between sleep-behavioral traits and healthspan: A one-sample Mendelian randomization study based on 388,909 participants of the UK-Biobank. J Affect Disord. 2024;350:854–862. 10.1016/j.jad.2024.01.122.
6. Burgess S, Butterworth A, Thompson SG. Mendelian randomization analysis with multiple genetic variants using summarized data. Genet Epidemiol. 2013;37(7):658–665. 10.1002/gepi.21758.
7. Bowden J, Davey Smith G, Burgess S. Mendelian randomization with invalid instruments: effect estimation and bias detection through Egger regression. Int J Epidemiol. 2015;44(2):512–525. 10.1093/ije/dyv080.
8. Verbanck M, Chen C-Y, Neale B, Do R. Detection of widespread horizontal pleiotropy in causal relationships inferred from Mendelian randomization between complex traits and diseases. Nat Genet. 2018;50(5):693–698. 10.1038/s41588-018-0099-7.
9. Hemani G, Zheng J, Elsworth B, Wade KH, Haberland V, Baird D, et al. The MR-Base platform supports systematic causal inference across the human phenome. Elife. 2018;7:e34408. 10.7554/eLife.34408.
10. Lawlor DA, Tilling K, Davey Smith G. Triangulation in aetiological epidemiology. Int J Epidemiol. 2016;45(6):1866–1886. 10.1093/ije/dyw314.
11. Munafò MR, Davey Smith G. Robust research needs many lines of evidence. Nature. 2018;553(7689):399–401. 10.1038/d41586-018-01023-3.
12. Skrivankova VW, Richmond RC, Woolf BAR, Yarmolinsky J, Davies NM, Swanson SA, et al. Strengthening the Reporting of Observational Studies in Epidemiology Using Mendelian Randomization. JAMA. 2021;326(16):1614–1621. 10.1001/jama.2021.18236.
13. Chen T-T, Kim J, Lam M, Chuang Y-F, Chiu Y-L, Lin S-C, et al. Shared genetic architectures of educational attainment in East Asian and European populations. Nat Hum Behav. 2024;8(3):562–575. 10.1038/s41562-023-01781-9.
14. Sudlow C, Gallacher J, Allen N, Beral V, Burton P, Danesh J, et al. UK Biobank: An Open Access Resource for Identifying the Causes of a Wide Range of Complex Diseases of Middle and Old Age. PLoS Med. 2015;12(3):e1001779. 10.1371/journal.pmed.1001779.
15. Bycroft C, Freeman C, Petkova D, Band G, Elliott LT, Sharp K, et al. The UK Biobank resource with deep phenotyping and genomic data. Nature. 2018;562(7726):203–209. 10.1038/s41586-018-0579-z.
16. Kunkle BW, Grenier-Boley B, Sims R, Bis JC, Damotte V, Naj AC, et al. Genetic meta-analysis of diagnosed Alzheimer’s disease identifies new risk loci and implicates Aβ, tau, immunity and lipid processing. Nat Genet. 2019;51(3):414–430. 10.1038/s41588-019-0358-2.
17. Bellenguez C, Küçükali F, Jansen IE, Kleineidam L, Moreno-Grau S, Amin N, et al. New insights into the genetic etiology of Alzheimer’s disease and related dementias. Nat Genet. 2022;54(4):412–436. 10.1038/s41588-022-01024-z.
18. Lambert J-C, Ibrahim-Verbaas CA, Harold D, Naj AC, Sims R, Bellenguez C, et al. Meta-analysis of 74,046 individuals identifies 11 new susceptibility loci for Alzheimer's disease. Nat Genet. 2013;45(12):1452–1458. 10.1038/ng.2802.
19. Seyedsalehi A, Warrier V, Bethlehem RAI, Perry BI, Burgess S, Murray GK. Educational attainment, structural brain reserve and Alzheimer’s disease: a Mendelian randomization analysis. Brain. 2023;146(5):2059–2074. 10.1093/brain/awac392.
20. Bowden J, Davey Smith G, Haycock PC, Burgess S. Consistent Estimation in Mendelian Randomization with Some Invalid Instruments Using a Weighted Median Estimator. Genet Epidemiol. 2016;40(4):304–314. 10.1002/gepi.21965.
21. Hartwig FP, Davey Smith G, Bowden J. Robust inference in summary data Mendelian randomization via the zero modal pleiotropy assumption. Int J Epidemiol. 2017;46(6):1985–1998. 10.1093/ije/dyx102.
22. Brion M-JA, Shakhbazov K, Visscher PM. Calculating statistical power in Mendelian randomization studies. Int J Epidemiol. 2013;42(5):1497–1501. 10.1093/ije/dyt179.
23. Deng L, Zhang H, Yu K. Power calculation for the general two-sample Mendelian randomization analysis. Genet Epidemiol. 2020;44(3):290–299. 10.1002/gepi.22284.
24. Morrison J, Knoblauch N, Marcus JH, Stephens M, He X. Mendelian randomization accounting for correlated and uncorrelated pleiotropic effects using genome-wide summary statistics. Nat Genet. 2020;52(7):740–747. 10.1038/s41588-020-0631-4.
25. Bulik-Sullivan BK, Loh P-R, Finucane HK, Ripke S, Yang J, Patterson N, et al. LD Score regression distinguishes confounding from polygenicity in genome-wide association studies. Nat Genet. 2015;47(3):291–295. 10.1038/ng.3211.
26. Bulik-Sullivan B, Finucane HK, Anttila V, Gusev A, Day FR, Loh P-R, et al. An atlas of genetic correlations across human diseases and traits. Nat Genet. 2015;47(11):1236–1241. 10.1038/ng.3406.
27. Giambartolomei C, Vukcevic D, Schadt EE, Franke L, Hingorani AD, Wallace C, et al. Bayesian Test for Colocalisation between Pairs of Genetic Association Studies Using Summary Statistics. PLoS Genet. 2014;10(5):e1004383. 10.1371/journal.pgen.1004383.
28. Sanderson E, Davey Smith G, Windmeijer F, Bowden J. An examination of multivariable Mendelian randomization in the single-sample and two-sample summary data settings. Int J Epidemiol. 2019;48(3):713–727. 10.1093/ije/dyy262.
29. Sanderson E. Multivariable Mendelian Randomization and Mediation. Cold Spring Harb Perspect Med. 2021;11(2):a038984. 10.1101/cshperspect.a038984.
30. Sun BB, Maranville JC, Peters JE, Stacey D, Staley JR, Blackshaw J, et al. Genomic atlas of the human plasma proteome. Nature. 2018;558(7708):73–79. 10.1038/s41586-018-0175-2.
31. Ferkingstad E, Sulem P, Atlason BA, Sveinbjornsson G, Magnusson MI, Styrmisdottir EL, et al. Large-scale integration of the plasma proteome with genetics and disease. Nat Genet. 2021;53(12):1712–1721. 10.1038/s41588-021-00978-w.
32. Sun BB, Chiou J, Traylor M, Benner C, Hsu Y-H, Richardson TG, et al. Plasma proteomic associations with genetics and health in the UK Biobank. Nature. 2023;622(7982):329–338. 10.1038/s41586-023-06592-6.
33. Xie Y, Liu S, Wang X, Huang H, Wang M, Qu W, et al. Lipids, Apolipoproteins, Lipid‐Lowering Drugs, and the Risk of Cerebral Small Vessel Disease: A Mendelian Randomization Study. J Am Heart Assoc. 2024;13(16):e032409. 10.1161/JAHA.123.032409.
34. Zhang X, Xie G, Zhao C, Lv Z. Plasma lipid subspecies and Alzheimer’s disease: genetic evidence for risk and protection. QJM. 2026;119(7):542–549. 10.1093/qjmed/hcag006.
35. Sun Y, Meng D, Yu H, Yin G, Zhang X, Yu W, et al. Genetic evidence for a causal relationship between 179 lipid species and cognitive function and alzheimer’s disease: a bidirectional Mendelian randomization study. Eur Arch Psychiatry Clin Neurosci. 2025. 10.1007/s00406-025-02152-3.
36. Kang S, Gim J, Lee J, Gunasekaran TI, Choi KY, Lee JJ, et al. Potential Novel Genes for Late-Onset Alzheimer’s Disease in East-Asian Descent Identified by APOE-Stratified Genome-Wide Association Study. J Alzheimers Dis. 2021;82(4):1451–1460. 10.3233/JAD-210145.
37. Popper KR. The Logic of Scientific Discovery. Routledge Classics ed. London: Routledge; 2002.
38. Sanderson E, Richardson TG, Hemani G, Davey Smith G. The use of negative control outcomes in Mendelian randomization to detect potential population stratification. Int J Epidemiol. 2021;50(4):1350–1361. 10.1093/ije/dyaa288.
39. Allara E, Morani G, Carter P, Gkatzionis A, Zuber V, Foley CN, et al. Genetic Determinants of Lipids and Cardiovascular Disease Outcomes: A Wide-Angled Mendelian Randomization Investigation. Circ Genom Precis Med. 2019;12(12):e002711. 10.1161/circgen.119.002711.
40. Li F-J, Li J-Y, Zhang R-Y, Liu X-J, Lv B-C, Zhang T, et al. PTPRD pleiotropy, genetically driven childbirth timing, and corpus callosum microstructure as potential mechanisms underlying ADHD–RLS comorbidity. Sleep Med. 2025;133:106631. 10.1016/j.sleep.2025.106631.
41. Zhang Y-R, Xu W, Zhang W, Wang H-F, Ou Y-N, Qu Y, et al. Modifiable risk factors for incident dementia and cognitive impairment: An umbrella review of evidence. J Affect Disord. 2022;314:160–167. 10.1016/j.jad.2022.07.008.
42. Cavaillès C, Andrews SJ, Leng Y, Chatterjee A, Daghlas I, Yaffe K. Causal Associations of Sleep Apnea With Alzheimer Disease and Cardiovascular Disease: A Bidirectional Mendelian Randomization Analysis. J Am Heart Assoc. 2024;13(18):e033850. 10.1161/JAHA.123.033850.
43. Li T, Liu M, Zhang P, Li S, Qiu T, Qiu X, et al. Associations between sleep disturbance and cerebrospinal fluid Aβ, and shared proteomic signatures in Alzheimer's disease. Alzheimers Dement. 2026;22(4):e71316. 10.1002/alz.71316.
44. Zhao B, Zhou R, Liu P, Li Q, Yan Y, Du J, et al. FLOT1 and EEF1D: ac4C-related genes bridging Alzheimer’s disease and sleep deprivation. Front Aging Neurosci. 2026;18:1825164. 10.3389/fnagi.2026.1825164.
45. Parhizkar S, Holtzman DM. APOE mediated neuroinflammation and neurodegeneration in Alzheimer's disease. Semin Immunol. 2022;59:101594. 10.1016/j.smim.2022.101594.
46. Inoue Y, Wang H, Heckman MG, Ren Y, White LJ, Lu W, et al. Impact of APOE on cerebrovascular lipid profile in Alzheimer's disease. Acta Neuropathol. 2025;150(1):39. 10.1007/s00401-025-02949-5.
47. Voight BF, Peloso GM, Orho-Melander M, Frikke-Schmidt R, Barbalic M, Jensen MK, et al. Plasma HDL cholesterol and risk of myocardial infarction: a mendelian randomisation study. Lancet. 2012;380(9841):572–580. 10.1016/S0140-6736(12)60312-2.
48. Barter PJ, Caulfield M, Eriksson M, Grundy SM, Kastelein JJ, Komajda M, et al. Effects of torcetrapib in patients at high risk for coronary events. N Engl J Med. 2007;357(21):2109–2122. 10.1056/NEJMoa0706628.
49. Wang F, Wang H, Yuan Y, Han B, Qiu S, Hu Y, et al. Integration of multiple-omics data to reveal the shared genetic architecture of educational attainment, intelligence, cognitive performance, and Alzheimer’s disease. Front Genet. 2023;14:1243879. 10.3389/fgene.2023.1243879.
50. Li Y, Sundquist K, Zhang N, Wang X, Sundquist J, Memon AA. Mitochondrial related genome-wide Mendelian randomization identifies putatively causal genes for multiple cancer types. EBioMedicine. 2023;88:104432. 10.1016/j.ebiom.2022.104432.
51. Wen J, Tian YE, Skampardoni I, Yang Z, Cui Y, Anagnostakis F, et al. The genetic architecture of biological age in nine human organ systems. Nat Aging. 2024;4(9):1290–1307. 10.1038/s43587-024-00662-8.
52. Zhao Y-L, Hao Y-N, Ge Y-J, Zhang Y, Huang L-Y, Fu Y, et al. Variables associated with cognitive function: an exposome-wide and mendelian randomization analysis. Alzheimers Res Ther. 2025;17(1):13. 10.1186/s13195-025-01670-5.
53. Korologou-Linden R, Bhatta L, Brumpton BM, Howe LD, Millard LAC, Kolaric K, et al. The causes and consequences of Alzheimer’s disease: phenome-wide evidence from Mendelian randomization. Nat Commun. 2022;13(1):4726. 10.1038/s41467-022-32183-6.
54. Ye C-J, Kong L-J, Wang Y-Y, Dou C, Zheng J, Xu M, et al. Mendelian randomization evidence for the causal effects of socio-economic inequality on human longevity among Europeans. Nat Hum Behav. 2023;7(8):1357–1370. 10.1038/s41562-023-01646-1.
55. Grotzinger AD, Rhemtulla M, de Vlaming R, Ritchie SJ, Mallard TT, Hill WD, et al. Genomic structural equation modelling provides insights into the multivariate genetic architecture of complex traits. Nat Hum Behav. 2019;3(5):513–525. 10.1038/s41562-019-0566-x.
56. Jung JY, Ahn Y, Park J-W, Jung K, Kim S, Lim S, et al. Polygenic overlap between subjective well-being and psychiatric disorders and cross-ancestry validation. Nat Hum Behav. 2025;9(6):1272–1282. 10.1038/s41562-025-02155-z.
57. Soler Artigas M, Wain LV, Miller S, Kheirallah AK, Huffman JE, Ntalla I, et al. Sixteen new lung function signals identified through 1000 Genomes Project reference panel imputation. Nat Commun. 2015;6(1):8658. 10.1038/ncomms9658.
58. Lee JJ, Wedow R, Okbay A, Kong E, Maghzian O, Zacher M, et al. Gene discovery and polygenic prediction from a genome-wide association study of educational attainment in 1.1 million individuals. Nat Genet. 2018;50(8):1112–1121. 10.1038/s41588-018-0147-3.
59. Okbay A, Wu Y, Wang N, Jayashankar H, Bennett M, Nehzati SM, et al. Polygenic prediction of educational attainment within and between families from genome-wide association analyses in 3 million individuals. Nat Genet. 2022;54(4):437–449. 10.1038/s41588-022-01016-z.
60. Hewitt J, Walters M, Padmanabhan S, Dawson J. Cohort profile of the UK Biobank: diagnosis and characteristics of cerebrovascular disease. BMJ Open. 2016;6(3):e009161. 10.1136/bmjopen-2015-009161.
61. Jansen PR, Watanabe K, Stringer S, Skene N, Bryois J, Hammerschlag AR, et al. Genome-wide analysis of insomnia in 1,331,010 individuals identifies new risk loci and functional pathways. Nat Genet. 2019;51(3):394–403. 10.1038/s41588-018-0333-3.
62. Lane JM, Jones SE, Dashti HS, Wood AR, Aragam KG, van Hees VT, et al. Biological and clinical insights from genetics of insomnia symptoms. Nat Genet. 2019;51(3):387–393. 10.1038/s41588-019-0361-7.
63. Prapiadou S, Živković L, Thorand B, George MJ, van der Laan SW, Malik R, et al. Proteogenomic Data Integration Reveals CXCL10 as a Potentially Downstream Causal Mediator for IL-6 Signaling on Atherosclerosis. Circulation. 2024;149(9):669–683. 10.1161/CIRCULATIONAHA.123.064974.
64. Guo Y, You J, Zhang Y, Liu W-S, Huang Y-Y, Zhang Y-R, et al. Plasma proteomic profiles predict future dementia in healthy adults. Nat Aging. 2024;4(2):247–260. 10.1038/s43587-023-00565-0.
65. Zhang X, Zhao H, Wan M, Man J, Zhang T, Yang X, et al. Associations of 2923 plasma proteins with incident inflammatory bowel disease in a prospective cohort study and genetic analysis. Nat Commun. 2025;16(1):2813. 10.1038/s41467-025-57879-3.
66. Auton A, Abecasis GR, Altshuler DM, Durbin RM, Abecasis GR, Bentley DR, et al. A global reference for human genetic variation. Nature. 2015;526(7571):68–74. 10.1038/nature15393.
67. Burgess S, Thompson SG. Multivariable Mendelian Randomization: The Use of Pleiotropic Genetic Variants to Estimate Causal Effects. Am J Epidemiol. 2015;181(4):251–260. 10.1093/aje/kwu283.
68. Nalls MA, Blauwendraat C, Vallerga CL, Heilbron K, Bandres-Ciga S, Chang D, et al. Identification of novel risk loci, causal insights, and heritable risk for Parkinson's disease: a meta-analysis of genome-wide association studies. Lancet Neurol. 2019;18(12):1091–1102. 10.1016/S1474-4422(19)30320-5.
69. Patsopoulos NA, Baranzini SE, Santaniello A, Shoostari P, Cotsapas C, Wong G, et al. Multiple sclerosis genomic map implicates peripheral immune cells and microglia in susceptibility. Science. 2019;365(6460):eaav7188. 10.1126/science.aav7188.
70. Brickman AM, Manly JJ, Honig LS, Sanchez D, Reyes‐Dumeyer D, Lantigua RA, et al. Plasma p‐tau181, p‐tau217, and other blood‐based Alzheimer's disease biomarkers in a multi‐ethnic, community study. Alzheimers Dement. 2021;17(8):1353–1364. 10.1002/alz.12301.
71. Schindler SE, Petersen KK, Saef B, Tosun D, Shaw LM, Zetterberg H, et al. Head-to-head comparison of leading blood tests for Alzheimer's disease pathology. Alzheimers Dement. 2024;20(11):8074–8096. 10.1002/alz.14315.
72. Pan F, Huang L, Wang Y, Huang Q, Guan Y, Li Y, et al. Plasma P‐tau217, GFAP, and NfL as biomarkers for Alzheimer's disease: role in disease stratification, pathological progression, and cognitive decline. Alzheimers Dement. 2025;21(12):e70987. 10.1002/alz.70987.
73. Wang X, Shi Z, Qiu Y, Sun D, Zhou H. Peripheral GFAP and NfL as early biomarkers for dementia: longitudinal insights from the UK Biobank. BMC Med. 2024;22(1):192. 10.1186/s12916-024-03418-8.
74. Kim KY, Shin KY, Chang K-A. GFAP as a Potential Biomarker for Alzheimer’s Disease: A Systematic Review and Meta-Analysis. Cells. 2023;12(9):1309. 10.3390/cells12091309.
75. Ahmad S, Imtiaz MA, Mishra A, Wang R, Herrera-Rivero M, Bis JC, et al. Genome-wide association study meta-analysis of neurofilament light (NfL) levels in blood reveals novel loci related to neurodegeneration. Commun Biol. 2024;7(1):1103. 10.1038/s42003-024-06804-3.
76. Zheng J, Zhang Y, Rasheed H, Walker V, Sugawara Y, Li J, et al. Trans-ethnic Mendelian-randomization study reveals causal relationships between cardiometabolic factors and chronic kidney disease. Int J Epidemiol. 2022;50(6):1995–2010. 10.1093/ije/dyab203.
