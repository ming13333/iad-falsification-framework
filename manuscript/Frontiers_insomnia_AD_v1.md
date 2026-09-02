# A six-gate falsification framework for correcting locus-driven confounding in Mendelian randomization: architecture, 43,200-simulation validation, and application to complex traits

**Qin Liu^1,†, Wangyang Ye^1,†, Ming Luo^1,\*^**

^1^Department of Neurosurgery, The Fifth Affiliated Hospital of Wenzhou Medical University (Lishui Central Hospital), Lishui, Zhejiang 323000, China

†These authors contributed equally to this work.

\*Correspondence: Ming Luo, lm962272@gmail.com

## Abstract

Mendelian randomization (MR) uses germline variants as instrumental variables to estimate causal relationships, relying on relevance, independence, and exclusion-restriction assumptions. When a single locus of large effect, such as *APOE* in Alzheimer's disease (AD), dominates trait genetic architecture, standard MR pipelines often yield precise, statistically significant estimates that do not reflect directed causal effects. This failure mode is termed locus-driven confounding. Here, we present a six-gate falsification framework that tests causal claims using six criteria: association screening, robustness, genetic architecture, direct effect, biological mediation, and external validation. Evidence across these gates is aggregated into an *a priori* grade (A–D) ranging from 0 to 12 points. To define its operating characteristics, we benchmarked 43,200 simulated two-sample MR scenarios covering variations in linkage disequilibrium (LD) concentration, pleiotropy regimes, sample overlap, effect sizes, and instrument counts, evaluating each replicate across all gates. Under the null hypothesis without pleiotropy, the framework demonstrated 100% specificity with zero false discoveries. In the presence of balanced pleiotropy, marginal specificity was $\approx 0.80$, corresponding to a marginal false discovery rate (FDR) of $\approx 0.08$ (scenario range 0.04–0.13). Sensitivity reached 0.97 at the highest effect size grid in the absence of pleiotropy, and assigned grades showed a monotonic relationship with effect size.

We evaluated the framework on the association between insomnia and AD as an empirical benchmark. A previously reported unclumped positive association ($\beta$ = +0.10, $P$ = $9.3 \times 10^{-4}$) was reclassified as shared liability driven by the *APOE* locus (Grade C). The association attenuated to the null after LD clumping ($\beta$ = $-0.13$, $P$ = 0.52), genome-wide genetic correlation was negligible ($r_g$ = $-0.028$, $P$ = 0.57), colocalization was consistent with reverse-direction variant sharing, and no protein mediators were identified. In contrast, educational attainment maintained an inverse association with AD ($\beta$ = $-0.33$, $P$ = $1.1 \times 10^{-5}$). The pipeline is fully reproducible via `renv.lockfile` (R 4.5.2) and archived on Zenodo (DOI 10.5281/zenodo.21858125), offering a standardizable protocol for graded causal inference in polygenic epidemiology.

**Keywords:** Alzheimer's disease; APOE; benchmarking; causal inference; falsification framework; locus-driven confounding; Mendelian randomization; operating characteristics

## Introduction

Mendelian randomization uses germline genetic variants as instruments to estimate the causal effect of an exposure on an outcome under three core assumptions: relevance (the variant associates with the exposure), independence (no confounding of the variant–outcome association), and exclusion restriction (the variant affects the outcome exclusively through the exposure) (Davey Smith and Ebrahim, 2003; Burgess et al., 2013). Violations of these assumptions at strong-effect loci can cause standard two-sample MR pipelines (Figure 1B) to yield precise, statistically significant estimates that misrepresent directed causal effects. Alzheimer's disease (AD) exemplifies this vulnerability: the APOE ε4 allele accounts for a substantial fraction of disease heritability, exposing any MR analysis involving AD as an exposure or outcome to locus-driven confounding (Lambert et al., 2013).

This failure mode emerges when polygenic MR instruments are aggregated from genome-wide significant variants and a single locus contributes disproportionately to instrument strength. Under extreme locus concentration, such as APOE in AD, the aggregated instrument behaves like a single-variant experiment. This regime produces four systematic distortions: (i) unclumped inverse-variance weighted (IVW) estimates derive artificial precision from thousands of correlated variants, causing statistical significance to reflect instrument count rather than biological signal; (ii) linkage disequilibrium (LD) clumping can invert the direction of effect because the clumped estimate becomes dominated by the strongest independent variant, whose underlying biology may lie outside the exposure's causal pathway; (iii) genome-wide genetic correlation can remain null while locus-specific sharing is strong, as shared liability is confined to the dominant region; and (iv) standard pleiotropy diagnostics lose power because the horizontal pleiotropy is concentrated rather than diffuse (Verbanck et al., 2018). Published insomnia–AD MR studies illustrate these vulnerabilities. Previous analyses differ in instrument pruning, sample-overlap correction, genetic-architecture assessment, and mediation testing, which are the specific analytical choices where locus-driven confounding manifests. Nevertheless, a positive insomnia–AD effect is repeatedly reported and cited as evidence that sleep disturbance elevates AD risk.

Addressing this problem requires a structured decision procedure rather than ad hoc sensitivity analyses. Specifically, causal evaluation benefits from a framework that evaluates directional causal claims through a fixed sequence of falsification gates (Popper, 1959), integrates multiple lines of evidence (Munafò and Davey Smith, 2018), assigns evidence grades based on cumulative outcomes, and undergoes benchmarking under controlled conditions prior to empirical application (Lawlor et al., 2016). The six-gate falsification framework fills this gap. The framework (i) operationalizes six failure modes of MR inference as sequential gates (association screening, robustness, genetic architecture, direct effect, biological mediation, and external validation); (ii) converts cumulative gate performance into an evidence grade (A–D) using a pre-specified 0–12 rubric; and (iii) is benchmarked using a 43,200-replicate simulation grid that quantifies Type I error control, specificity under pleiotropy, power, and grade calibration.

Two structural properties distinguish this framework from reporting checklists. First, it quantifies the evidence required to sustain a causal claim. Grades are assigned via a deterministic rule using fixed threshold policies (instrument extraction P < 5×10⁻⁸; per-SNP F > 10; Benjamini–Hochberg FDR for multi-mediator screens; nominal P < 0.05 elsewhere). Second, its operating characteristics are empirically quantified via simulation rather than assumed. An A–B grade indicates consistency with a directed causal effect under the framework's measured operating parameters, whereas a C–D grade denotes insufficient or falsified evidence. The framework complements reporting standards such as STROBE-MR (Skrivankova et al., 2021): while reporting guidelines define required study documentation, this framework defines when reported evidence supports a causal claim at a specified confidence level.

We benchmark the framework under controlled stress parameters, crossing null, balanced, and directional pleiotropy with LD concentration, sample overlap, effect size, and instrument count. We then apply it to the insomnia–AD axis as a proof-of-concept for a trait pair with a reported positive MR signal and a known dominant locus (APOE) in the outcome architecture. This insomnia–AD application serves to evaluate the framework's diagnostic utility, not to assert an independent epidemiological claim. The complete pipeline, simulation grid, grading rubric, and derived results are reproducible via the project renv.lockfile (R 4.5.2) and archived for reuse (Zenodo DOI 10.5281/zenodo.21858125; GitHub ming13333/iad-falsification-framework).
## Materials and Equipment

The framework is implemented as an open-source R/Python pipeline. All analyses use publicly available GWAS summary statistics, requiring no individual-level data.

**Software environment.** Analyses run in a reproducible computational environment managed via the project `renv.lockfile` under R 4.5.2 and Python ≥ 3.10 on Linux or Windows workstations (≥ 8 cores and 32 GB RAM recommended for simulation and LD score regression).

**Core R packages and roles.**
- `TwoSampleMR` v0.7.9 (Hemani et al., 2018): instrument extraction, harmonization, IVW, MR-Egger, and weighted median estimation (Bowden et al., 2015, 2016).
- `MendelianRandomization` v0.10.0: multivariable MR (MVMR) with conditional F statistics.
- `MRlap` (Mounier and Kutalik, 2023): sample-overlap correction using cross-trait LDSC intercepts.
- `CAUSE` v1.2.0 (Morrison et al., 2020): correlated-pleiotropy model fitting ($q$ and $\gamma$ estimates).
- `coloc` (Giambartolomei et al., 2014): Bayesian colocalization (PPH4).
- `GenomicSEM` v0.0.5 (Grotzinger et al., 2019) and LDSC (Bulik-Sullivan et al., 2015a): genome-wide genetic correlation ($r_g$).
- `ieugwasr` v1.1.0: LD clumping against the 1000 Genomes European reference.
- Additional data manipulation and Bayesian diagnostic utilities: `data.table` v1.18.4, `dplyr` v1.2.1, and `loo` v2.10.0.

**Python components.** The simulation data-generating process and gate-scoring engine are implemented in Python using NumPy and SciPy (`pyreadr` v0.5.6; see archived code), alongside VEP REST-based variant annotation.

**Input data requirements.** Pipeline execution requires two harmonized, same-build (GRCh37) GWAS summary-statistics files per trait pair. Each file must contain the effect allele, other allele, effect size, standard error (or OR and CI), $P$-value, total sample size, and case–control counts where applicable. LD reference panels must match the genomic build of the input GWAS.

**Public data repositories.** Proof-of-concept applications utilize public summary statistics (obtained from IEU OpenGWAS unless noted): insomnia, ukb-b-3957 (UK Biobank; Sudlow et al., 2015, $n = 462,341$); AD, ieu-b-2 (Kunkle et al., 2019; 21,982 cases, 41,944 controls) and ebi-a-GCST90027158 (Bellenguez et al., 2022; 85,934 cases, 401,577 controls); educational attainment, ieu-a-1239 (Lee et al., 2018; $n = 766,345$); and East Asian AD, GARD NG00182 ($n = 6,518$; 2,919 cases) alongside BioBank Japan outcomes (Table 3).

**Archived framework.** Simulation outputs, executable pipeline scripts, and the grading rubric are archived at Zenodo (DOI 10.5281/zenodo.21858125). Source code and documentation are hosted on GitHub (ming13333/iad-falsification-framework).
## Methods

### Objectives and validation of the method

The framework converts a directional Mendelian randomization (MR) claim into a graded verdict with a calibrated numerical basis. Methodological validation comprises two parts. First, a simulation-based assessment evaluates the full gate-scoring procedure under known ground truth (see the simulation-based validation below) to establish operating characteristics prior to application. Second, an empirical evaluation uses the insomnia–Alzheimer's disease trait pair (see the proof-of-concept application) to evaluate performance on a recognized edge case. Threshold policies are established before execution of either evaluation and remain fixed throughout.

### The six gates

Each gate operationalizes a distinct failure mode of MR inference (Figure 1, Table 1). All gates evaluate identical harmonized summary statistics unless explicitly indicated.

**Gate G1 (association, screening).** An unclumped inverse-variance weighted (IVW) estimate tests for initial signal presence. Because unclumped estimation uses correlated instruments, precision reflects instrument count rather than biological signal. Gate G1 therefore uses a liberal threshold ($P < 0.05$) to identify candidates for falsification rather than to establish a causal verdict. Score: 2 if the unclumped IVW estimate is nominally significant in the claimed direction, 0 otherwise.

**Gate G2 (robustness).** The primary signal must survive three distinct corrections: (i) linkage disequilibrium (LD) clumping ($r^2 < 0.001$, 10,000-kb window, 1000 Genomes EUR reference; Auton et al., 2015), (ii) sample-overlap correction via MRlap using the cross-trait LD score regression (LDSC) intercept, and (iii) correlated-pleiotropy partitioning via CAUSE. A directional reversal, shifting from positive to null or negative following clumping, falsifies the claim regardless of the unclumped result. Robust estimation complements clumped IVW. MR-Egger regression tests for directional pleiotropy (Bowden et al., 2015), the weighted median remains consistent when up to half of the instruments are invalid (Bowden et al., 2016), and the mode-based estimator provides a further consistency check (Hartwig et al., 2017). Score: 2 only if the clumped IVW estimate remains significant in the claimed direction, without a directional MR-Egger intercept ($P \ge 0.05$) or excessive heterogeneity (Cochran $Q$ test $P \ge 0.05$); 0 otherwise.

**Gate G3 (genetic architecture).** LDSC tests genome-wide genetic correlation ($r_g$; Bulik-Sullivan et al., 2015a), interpreted against the cross-trait atlas of genetic correlations (Bulik-Sullivan et al., 2015b). Bayesian colocalization (`coloc`, $PP.H4 \ge 0.80$) evaluates locus-specific variant sharing. Shared liability restricted to a single region without genome-wide correlation indicates locus-driven confounding rather than a systemic causal pathway. Score: 2 for an $r_g$ estimate consistent in direction with the claim (or null) alongside locus-specific sharing at the expected region; 0 for architectural evidence contradicting the claim.

**Gate G4 (direct effect).** Multivariable MR (Burgess and Thompson, 2015; Sanderson et al., 2019) estimates the direct effect of the exposure conditional on specified confounders (education, depression, and cardiometabolic traits), requiring a conditional $F$-statistic $> 10$ for instrument strength. Score: 2 for a significant direct effect in the claimed direction with conditional $F > 10$; 0 otherwise.

**Gate G5 (biological mediation).** Two-step MR (Sanderson, 2021a) tests genetically proxied mediators along the exposure$\rightarrow$mediator$\rightarrow$outcome path, applying Benjamini–Hochberg false discovery rate (FDR) control across the mediator panel and bootstrap confidence intervals for indirect effects. Score: 2 for a significant FDR-corrected indirect effect consistent with the claim; 0 otherwise.

**Gate G6 (external validation).** Directional consistency is evaluated in an independent ancestry cohort and, where feasible, a multi-domain validation cohort across the full grade spectrum. Underpowered tests (achieved power $< 80%$) serve as directional screening only and assign no points. Score: 2 for cross-ancestry directional consistency in the claimed direction; 0 otherwise.

### Grading rubric

Cumulative scores range from 0 to 12 points, with G1–G6 each contributing 0–2 points. Grade A (10–12 points) indicates resistance to falsification, Grade B (7–9 points) indicates support with caveats, Grade C (4–6 points) indicates weak evidence or shared liability, and Grade D (0–3 points) indicates lack of support. The complete grading scheme, including the rationale for liberal screening thresholds and Bayesian posterior limits, is provided in Table 1 and the gate definitions above. In the validation cohort, two independent raters scored all six gates for each of the 12 trait pairs (72 gate-level items) following the pre-specified rubric; disagreements were resolved by consensus, and grade-level agreement was quantified by Cohen's κ (Supplementary Table S8).

### Step-by-step execution protocol

The pipeline processes gates in a sequential workflow (Table 4). Intermediate outputs are saved at designated pause points to allow downstream re-analysis without repeating prior calculations.

1. **Harmonization** ($\approx 1.5\text{ h}$). Extract instruments at $P < 5 \times 10^{-8}$; harmonize alleles and strand orientation against the LD reference; align exposure and outcome summary statistics. *Pause point 1:* save harmonized unclumped instrument set.
2. **Gate G1** ($15\text{--}30\text{ min}$). Run unclumped IVW using the full instrument set.
3. **Gate G2** ($2\text{--}4\text{ h}$, includes CAUSE MCMC fitting). Perform LD clumping at $r^2 < 0.001$ within $10,000\text{ kb}$; re-estimate IVW on clumped instruments; run MR-Egger and Cochran $Q$ tests; calculate MRlap corrections using the cross-trait LDSC intercept; fit CAUSE models. *Pause point 2:* save clumped instrument set, MRlap output, and CAUSE posteriors.
4. **Gate G3** ($1\text{--}2\text{ h}$). Munge summary statistics; compute $r_g$ via LDSC; perform per-locus colocalization across independent loci with $PP.H4 \ge 0.80$. *Pause point 3:* save LDSC log files and colocalization matrices.
5. **Gate G4** ($30\text{--}45\text{ min}$). Fit multivariable MR models including specified confounders; calculate conditional $F$-statistics. *Pause point 4:* export multivariable MR coefficients and conditional $F$-statistics.
6. **Gate G5** ($3\text{--}6\text{ h}$, includes bootstrap). Execute two-step MR across the mediator panel; apply Benjamini–Hochberg FDR adjustments; derive $10,000$-replicate bootstrap confidence intervals for indirect effects. *Pause point 5:* save FDR-adjusted mediation tables.
7. **Gate G6** ($1\text{--}2\text{ h}$). Conduct cross-ancestry replication using ancestry-matched LD clumping; calculate validation-cohort grades. *End:* sum the $0\text{--}12$ score and map the total to grades A–D.

### Simulation-based validation: design and data-generating process

Because the framework is prescriptive, its operating characteristics require quantitative evaluation prior to empirical deployment. We generated polygenic two-sample MR summary statistics under known ground truth, varying: causal effect size $\beta \in \{0, 0.08, 0.15\}$ per standard deviation; LD structure ($5$, $12$, or $40$ blocks); pleiotropy mode (none, balanced, directional); sample overlap ($0%$ or $30%$); and instrument count ($20$ or $60$). Instrument effects were sampled with mean per-variant $F \approx 36$. Each parameter combination was replicated $400$ times ($3 \times 3 \times 3 \times 2 \times 2 \times 400 = 43,200$ total iterations). Every replicate was evaluated through all six gates and assigned a grade using the $0\text{--}12$ rubric. Empirical FDR was computed across the full effect-size mixture (one-third null and two-thirds non-null replicates per parameter cell), reflecting the framework's intended usage in which null and candidate claims are evaluated together.

The full data-generating process is defined in the archived code repository (Zenodo DOI: 10.5281/zenodo.21858125). Key features include LD blocks simulated from block-diagonal correlation matrices, balanced pleiotropy represented as independent, symmetric effects on the outcome, directional pleiotropy modeled as a systematic bias aligned with the exposure effect, and sample overlap induced by introducing correlated residual noise between exposure and outcome samples. Evaluated metrics include specificity ($1 - \text{Type I error}$), sensitivity (power), empirical FDR, and monotonicity of grade calibration across effect sizes.
## Results

### Operating characteristics of the framework (43,200-simulation benchmark)

At the null ($\beta = 0$), the framework achieved 100% specificity and a zero false discovery rate ($\text{FDR} = 0$) in the absence of pleiotropy, confirming Type I error control in the ideal parameter space. Under balanced pleiotropy, marginal specificity was 0.80 (scenario range 0.77–0.84) with a marginal FDR of 0.08 (scenario range 0.04–0.13). Directional pleiotropy increased the marginal FDR to 0.13 (scenario range 0.08–0.18), which remained below the nominal 0.20 decision threshold. For the largest effect size tested ($\beta = 0.15$), marginal sensitivity reached 0.97 (scenario range 0.95–1.00) without pleiotropy, declining to approximately 0.85 under balanced pleiotropy and 0.80 under directional pleiotropy. At $\beta = 0.08$, sensitivity dropped to approximately 0.5 across all regimes, reflecting lower power to detect modest effects. Grade assignment scaled monotonically with effect size. Without pleiotropy, marginal Grade A frequency increased from 0 at the null to 0.88 at $\beta = 0.15$ (scenario range 0.62–1.00), falling to 0.72 under balanced pleiotropy (scenario range 0.51–0.95) and 0.67 under directional pleiotropy. Under null conditions without pleiotropy, 100% of replicates received Grade D, compared with 0.80 under balanced pleiotropy and 0.68 under directional pleiotropy. No null replicate received Grade A in the absence of pleiotropy, whereas 6% under balanced pleiotropy and 5% under directional pleiotropy were assigned Grade A. Complete operating characteristics are provided in Supplementary Table S9, Table 2, and Figure 2.

**Interpretation for users.** A grade of A–B indicates that the claim aligns with a directed causal effect at the framework's measured sensitivity for the tested effect size. A grade of C–D indicates that the claim is falsified or supported exclusively by shared-liability evidence. Borderline assignments (B/C) represent provisional findings requiring further empirical validation.

### Example of application: the insomnia–AD proof-of-concept

**Data.** Insomnia: ukb-b-3957 ($n = 462,341$, continuous trait; cf. Jansen et al., 2019; Lane et al., 2019). Alzheimer's disease (AD): ieu-b-2 (Kunkle et al., 2019; 21,982 cases, 41,944 controls) as the primary outcome, with ebi-a-GCST90027158 (Bellenguez et al., 2022; 85,934 cases, 401,577 controls) as a sensitivity outcome. Educational attainment: ieu-a-1239 ($n = 766,345$). Protein pQTLs from the INTERVAL panel (Sun et al., 2018; $n = 3,301$) and NMR metabolites from Kettunen et al. (2016). East Asian sensitivity evaluations incorporated GARD AD (NG00182; $n = 6,518$) and BioBank Japan summary statistics (Koyama et al., 2020; Kang et al., 2021). All datasets were harmonized on GRCh37.

**G1: association.** Unclumped inverse-variance weighted (IVW) analysis yielded $\beta = +0.104$ ($\text{SE} = 0.031$, $P = 9.3 \times 10^{-4}$; 2,462 instruments), reproducing the published positive association (Figure 3A).

**G2: robustness.** LD clumping ($r^2 < 0.001$, 10,000 kb window) reduced the instrument set to 54 variants and attenuated the estimate to the null ($\beta = -0.130$, $\text{SE} = 0.203$, $P = 0.52$). A narrower window (5,000 kb; 37 instruments) produced consistent results ($\beta = -0.111$, $P = 0.64$). Correcting for sample overlap via MRlap sustained the null ($\beta = -0.078$, $P = 0.43$). CAUSE fitting on the clumped instrument sets retained a boundary forward CAUSAL classification in both AD sources (Kunkle: causal $P = 0.039$; Bellenguez: causal $P = 0.002$), whereas both reverse analyses were classified as pleiotropy or sharing ($P = 0.08$ and $P = 0.63$). The Bellenguez classification must be interpreted cautiously, because that AD source showed extreme heterogeneity in related analyses (Cochran $Q$ $P = 1.7 \times 10^{-11}$; Supplementary Table S4), rendering its estimates unreliable. CAUSE therefore constitutes a single method-level disagreement against three null results (clumped IVW, MRlap, and the MVMR direct effect below); we report this disagreement explicitly rather than treating the boundary CAUSAL label as evidence for a directed effect. This signal attenuation was not driven by the *APOE* locus, as excluding 118 chromosome-19 instruments retained the unclumped association ($\beta = 0.094$, $P = 0.003$). These two observations operate at different levels: the unclumped precision reflects genome-wide instrument correlation, whereas the colocalization signal localizes to the *APOE* region; the former concerns instrument redundancy, the latter locus-specific shared liability, and they are not contradictory. Statistical power at the achieved instrument strength ($R^2 = 0.0022$ across 44 window-clumped loci; mean $F = 44.3$, minimum $F = 29.8$) was 24% for $\beta = 0.10$. Achieving 80% power required $\beta \ge 0.226$ ($\text{OR} \ge 1.25$ per standard deviation of insomnia liability; mRnd binary-outcome approximation with outcome GWAS sample size $n = 63,926$; Brion et al., 2013; Deng et al., 2020; Supplementary power tables). For transparency, the instrument count chain is: 2,462 unclumped instruments (Gate G1) $\rightarrow$ 54 LD-independent instruments after clumping ($r^2 < 0.001$, 10,000 kb) $\rightarrow$ 44 window-clumped loci (1-Mb window) retained for power estimation and confounder screening $\rightarrow$ 38 after removing six confounder-associated variants $\rightarrow$ 33 harmonized instruments. The 54-versus-40 discrepancy with the cross-ancestry step (Gate G6 below) reflects LD reference-panel updates between the primary European clumping (54 instruments) and the trans-ethnic re-clumping of the same instrument set against the updated panel (40 instruments), which we disclose for reproducibility. An instrument–confounder screen (GWAS Catalog IV-PheWAS across all 44 independent loci; a priori domains: smoking, alcohol, education/cognition, adiposity, depression/anxiety/neuroticism) identified six variants with documented associations in these domains, matching a negative-control framework (Sanderson et al., 2021b). Removing these variants maintained the null ($\beta = -0.106$, $\text{SE} = 0.252$, $P = 0.67$; 33 harmonized instruments; Supplementary Table S7). Heterogeneity diagnostics reflected this instrument-correlation pattern: on the unclumped set, Cochran's $Q$ was extreme ($Q = 3.66 \times 10^{3}$, $P = 1.25 \times 10^{-50}$), consistent with precision inflation from correlated instruments, whereas MR-Egger and the weighted-median/mode estimators were not separately reported for the clumped subsets (Supplementary Table S2).

**G3: genetic architecture.** Cross-trait LD Score regression (LDSC) yielded $r_g = -0.028$ ($\text{SE} = 0.050$, $P = 0.57$), which remained unchanged after excluding chromosome 19 ($r_g = -0.031$, $P = 0.53$), indicating no genome-wide shared polygenic architecture. Colocalization analysis identified strong support ($\text{PP.H4} \ge 0.80$) for 18 of 32 loci in the reverse direction, concentrated in the *APOE* region ($\text{PP.H4} > 0.98$), compared with 1 of 47 loci in the forward direction (Figure 3B). This asymmetry indicates locus-specific, *APOE*-centered genetic sharing (Supplementary Table S1; Figure 4).

**G4: direct effect.** Multivariable MR (MVMR) incorporating insomnia, education, depression, and LDL cholesterol revealed a protective direct effect for educational attainment ($\beta = -1.29$, $P = 0.008$, loose clump). The direct effect of insomnia was negative ($\beta = -0.57$, $P = 0.045$), opposite in direction to the original claim that insomnia elevates AD risk, further supporting falsification rather than a protective interpretation given the low power of this direct-effect model. Educational attainment PheWAS confirmed protective associations against AD ($\beta = -0.33$, $P = 1.1 \times 10^{-5}$; cf. Seyedsalehi et al., 2023) and Parkinson's disease ($\beta = -0.39$, $P = 7.2 \times 10^{-6}$; Nalls et al., 2019), but not multiple sclerosis ($\beta = +0.015$, $P = 0.90$; Patsopoulos et al., 2019).

**G5: biological mediation.** Protein mediation was absent along the insomnia $\rightarrow$ protein $\rightarrow$ AD pathway, as CRP and IL-6 indirect effects were null (overall $\text{FDR} = 0.91$). Screening 36 AD-relevant candidate proteins (25 evaluable) yielded no associations at $\text{FDR} < 0.05$. In the metabolite domain, circulating triglycerides mediated the protective effect of education (indirect $\beta = -0.031$, $\text{SE} = 0.008$, $q = 5.7 \times 10^{-4}$; bootstrap 95% CI $[-0.047, -0.017]$), accounting for 9% of the total educational effect.

**G6: external validation.** Directional consistency was maintained across East Asian cohorts for established directions. Education associated inversely with T2D risk using East Asian education instruments ($\beta = -0.145$, $P = 0.012$; cf. Chen et al., 2024), whereas the T2D $\rightarrow$ AD pathway remained null ($\beta = +0.006$, $P = 0.93$). Trans-ethnic evaluation (cf. Zheng et al., 2021) using 40 LD-independent European instruments in GARD East Asian AD summary statistics produced a negative IVW estimate ($\beta = -0.84$, $P = 0.28$), aligning with the European clumped null. Because statistical power was low ($<6%$), this step serves only for directional screening and contributes no scoring points (Supplementary Note 2). Across the 12-case validation cohort, the framework assigned Grade A to positive controls (LDL–CAD, education–AD), Grade B/C to reclassified or borderline traits (education–T2D, insomnia–AD), and Grade D to true nulls (BMI–AD, T2D–AD), yielding an inter-rater agreement of $\kappa = 0.76\text{--}0.94$ (Supplementary Table S8; Figure 5). A formal East Asian replication of the depression–AD case was not feasible with currently accessible data (Supplementary Note 1).

**Integrated verdict.** The cumulative 0–12 score maps to **Grade C: shared APOE-locus liability, no independent causal upstream.** This application shows how the framework re-evaluates a previously reported Mendelian randomization signal, yielding a graded verdict that accounts for pleiotropic confounding.

### Precision, limits of detection, pitfalls, and troubleshooting

The benchmarked operating characteristics above define the precision of the framework. Limits of detection depend on statistical power. At instrument strengths typical of insomnia liability ($R^2 \approx 0.0022$), the procedure detects medium-to-large causal effects ($80%$ power at $\text{OR} \ge 1.25$ per standard deviation) but cannot exclude smaller effects. Consequently, cross-ancestry checks provide directional screening rather than definitive exclusion. Key methodological pitfalls and corrective actions are outlined in Table 5. Principal operational challenges include:

1. **MRlap covariance non-positive-definiteness under substantial sample overlap and weak instruments:** Prune variant sets to per-SNP $F > 20$ and inspect the cross-trait LDSC intercept.
2. **CAUSE non-convergence with sparse variant panels:** Relax pre-pruning thresholds to $r^2 < 0.05$ or extend the MCMC sampling chain.
3. **Colocalization power loss from incomplete regional coverage:** Impute regional summary statistics using the 1000 Genomes reference panel.
4. **Conditional $F$-statistics $< 10$ in MVMR due to collinearity:** Restrict instruments to variants associated exclusively with the targeted exposure.
5. **Cross-ancestry inflation driven by LD mismatch:** Re-clump summary statistics using an ancestry-matched reference panel.
## Discussion

The insomnia–AD findings demonstrate how a replicated Mendelian randomization (MR) signal can arise as an artifact of locus-driven confounding. They also show how a sequence of falsification gates translates that signal into a graded verdict with quantified statistical properties. Methodologically, the framework operationalizes six common MR failure modes as distinct gates, assigns evidence grades by fixed rules rather than subjective judgment, and reports operating characteristics derived from 43,200 simulated replicates. This calibration allows performance to be evaluated through measured Type I error and statistical power rather than asserted confidence.

The APOE result reflects a broader pattern in complex-trait genetics: when a single locus dominates genetic variance, genome-wide genetic correlation ($r_g$) and clumped MR can be null even while standard MR yields a positive signal. Analyses that omit clumping, sample-overlap correction, and architectural assessment remain susceptible to this artifact. Benchmarking established specific operating parameters for the framework: a specificity of 1.00 under the null without pleiotropy, a marginal false discovery rate (FDR) of approximately 0.08 under balanced pleiotropy, and sensitivity of 0.97 at the upper effect grid in the absence of pleiotropy. The monotonic grade calibration indicates that intermediate grades (B/C) reflect claims with provisional evidence.

**Complementarity with reporting standards.** While STROBE-MR defines reporting requirements, this framework evaluates whether reported evidence supports a causal claim at a specific grade. The combined approach targets two persistent challenges in polygenic epidemiology: incomplete pipeline reporting and over-confident evidence interpretation.

**Generalizability of the template.** Although insomnia–AD was chosen as a case study due to the extreme locus concentration at APOE, the framework functions independently of the underlying biological locus. It applies directly to other complex-trait pairs, including psychiatric exposures and cardiometabolic outcomes where pleiotropic instruments and sample overlap frequently occur. The codebase, simulation grid, and grading rubric are implemented in R 4.5.2 via `renv.lockfile` and archived for reuse (Zenodo DOI 10.5281/zenodo.21858125). Investigators can apply the same gate sequence to pre-specified hypotheses using harmonized summary statistics and a suitable LD reference without individual-level data.

**Implications for drug-target prioritization.** Distinguishing directed causation from locus-driven shared liability directly informs translational decisions. Causal claims that pass all six gates, such as LDL-cholesterol and coronary artery disease (Grade A; Allara et al., 2019), align with drug targets whose efficacy was confirmed in clinical trials. Conversely, claims that fail robustness gates despite replication, such as HDL-raising therapies, correspond to target interventions that failed in trials. The framework offers a preclinical triage system: Grade A–B signals warrant target investment, whereas Grade C–D signals indicate shared liability or confounding and are insufficient to justify interventional drug development.

**Limitations.** Several methodological boundaries apply. First, the framework was evaluated on 12 trait pairs enriched for borderline grades, requiring larger validation sets. Second, while the simulation grid covers 43,200 replicates, it does not encompass all genetic architectures; directional pleiotropy at the magnitude of APOE was not fully parameterized. Third, the primary case study achieved 80% power only for medium-to-large effects ($OR \ge 1.25$ per SD of insomnia liability), meaning small causal effects cannot be ruled out, and the trans-ethnic evaluation serves strictly as a directional screen. Fourth, the grade-boundary cutoffs (10–12, 7–9, 4–6, 0–3) are pre-specified but arbitrary. In the validation cohort, two of 12 cases fell within one point of a boundary (Height–CAD at 10, the lower bound of Grade A; Education–T2D at 9, the upper bound of Grade B); shifting a boundary by one point would move Height–CAD from A to B, so adjacent-grade assignments at the boundaries should be interpreted as provisional. Fifth, Steiger directional tests could not establish a reliable direction (the inferred direction flipped with the choice of $r$ construction; median $|r| \approx 0.002$), so directionality was not scored in this application and should be interpreted with caution. Finally, upstream summary-statistic quality and build harmonization remain critical prerequisites, as upstream errors alter downstream gate decisions.

**Conclusions.** A six-gate falsification framework with quantified operating characteristics reclassifies locus-driven MR artifacts into graded causal verdicts. In the insomnia–AD case study, the framework identifies a replicated MR signal as shared APOE-locus liability, offering a calibrated template for causal inference across polygenic traits.

## Declarations

**Data availability statement.** All GWAS summary statistics used in this study are publicly available via IEU OpenGWAS under the accessions listed in the Materials and Equipment section. Derived results, simulation scripts, and analysis code are archived on Zenodo (DOI 10.5281/zenodo.21858125); source code is maintained at GitHub (ming13333/iad-falsification-framework).

**Ethics statement.** This study is a secondary analysis of publicly available GWAS summary statistics. No individual-level data were used and no new data were collected; therefore, no ethics approval was required. The study was conducted in accordance with the Declaration of Helsinki.

**Author contributions.** QL and WY designed the framework and performed the analyses (equal contribution); ML supervised the study and revised the manuscript. All authors contributed to conceptualization, methodology, software, validation, formal analysis, and writing, and approved the submitted version.

**Funding.** This research received no specific grant from any funding agency in the public, commercial, or not-for-profit sectors.

**Conflict of interest.** The authors declare that the research was conducted in the absence of any commercial or financial relationships that could be construed as a potential conflict of interest.

**Use of AI.** Large language models (GLM and DeepSeek, accessed through the WorkBuddy agent environment) assisted with drafting and language editing; all generated text was reviewed and verified by the authors, who take full responsibility for the content. No AI tool was used to analyse data or generate results.

**Supplementary material.** The Supplementary Material for this article comprises Supplementary Tables S1–S9 and Supplementary Notes 1–2, submitted as separate files with this manuscript.

---

## References

Allara, E., Morani, G., Carter, P., Gkatzionis, A., Zuber, V., Foley, C. N., et al. (2019). Genetic Determinants of Lipids and Cardiovascular Disease Outcomes: A Wide-Angled Mendelian Randomization Investigation. Circ. Genom. Precis. Med. 12(12), e002711. doi: 10.1161/circgen.119.002711
Auton, A., Abecasis, G. R., Altshuler, D. M., Durbin, R. M., Bentley, D. R., Chakravarti, A., et al. (2015). A global reference for human genetic variation. Nature 526(7571), 68–74. doi: 10.1038/nature15393
Bellenguez, C., Küçükali, F., Jansen, I. E., Kleineidam, L., Moreno-Grau, S., Amin, N., et al. (2022). New insights into the genetic etiology of Alzheimer’s disease and related dementias. Nat. Genet. 54(4), 412–436. doi: 10.1038/s41588-022-01024-z
Bowden, J., Davey Smith, G., and Burgess, S. (2015). Mendelian randomization with invalid instruments: effect estimation and bias detection through Egger regression. Int. J. Epidemiol. 44(2), 512–25. doi: 10.1093/ije/dyv080
Bowden, J., Davey Smith, G., Haycock, P. C., and Burgess, S. (2016). Consistent Estimation in Mendelian Randomization with Some Invalid Instruments Using a Weighted Median Estimator. Genet. Epidemiol. 40(4), 304–14. doi: 10.1002/gepi.21965
Brion, M. J. A., Shakhbazov, K., and Visscher, P. M. (2013). Calculating statistical power in Mendelian randomization studies. Int. J. Epidemiol. 42(5), 1497–501. doi: 10.1093/ije/dyt179
Bulik-Sullivan, B. K., Loh, P. R., Finucane, H. K., Ripke, S., Yang, J., Patterson, N., et al. (2015a). LD Score regression distinguishes confounding from polygenicity in genome-wide association studies. Nat. Genet. 47(3), 291–5. doi: 10.1038/ng.3211
Bulik-Sullivan, B., Finucane, H. K., Anttila, V., Gusev, A., Day, F. R., Loh, P. R., et al. (2015b). An atlas of genetic correlations across human diseases and traits. Nat. Genet. 47(11), 1236–41. doi: 10.1038/ng.3406
Burgess, S., Butterworth, A., and Thompson, S. G. (2013). Mendelian Randomization Analysis With Multiple Genetic Variants Using Summarized Data. Genet. Epidemiol. 37(7), 658–65. doi: 10.1002/gepi.21758
Burgess, S., and Thompson, S. G. (2015). Multivariable Mendelian Randomization: The Use of Pleiotropic Genetic Variants to Estimate Causal Effects. Am. J. Epidemiol. 181(4), 251–60. doi: 10.1093/aje/kwu283
Chen, T. T., Kim, J., Lam, M., Chuang, Y. F., Chiu, Y. L., Lin, S. C., et al. (2024). Shared genetic architectures of educational attainment in East Asian and European populations. Nat. Hum. Behav. 8(3), 562–575. doi: 10.1038/s41562-023-01781-9
Davey Smith, G., and Ebrahim, S. (2003). ‘Mendelian randomization’: can genetic epidemiology contribute to understanding environmental determinants of disease?. Int. J. Epidemiol. 32(1), 1–22. doi: 10.1093/ije/dyg070
Deng, L., Zhang, H., and Yu, K. (2020). Power calculation for the general two-sample Mendelian randomization analysis. Genet. Epidemiol. 44(3), 290–299. doi: 10.1002/gepi.22284
Giambartolomei, C., Vukcevic, D., Schadt, E. E., Franke, L., Hingorani, A. D., Wallace, C., et al. (2014). Bayesian Test for Colocalisation between Pairs of Genetic Association Studies Using Summary Statistics. PLoS Genet. 10(5), e1004383. doi: 10.1371/journal.pgen.1004383
Grotzinger, A. D., Rhemtulla, M., de Vlaming, R., Ritchie, S. J., Mallard, T. T., Hill, W. D., et al. (2019). Genomic structural equation modelling provides insights into the multivariate genetic architecture of complex traits. Nat. Hum. Behav. 3(5), 513–525. doi: 10.1038/s41562-019-0566-x
Hartwig, F. P., Davey Smith, G., and Bowden, J. (2017). Robust inference in summary data Mendelian randomization via the zero modal pleiotropy assumption. Int. J. Epidemiol. 46(6), 1985–1998. doi: 10.1093/ije/dyx102
Hemani, G., Zheng, J., Elsworth, B., Wade, K. H., Haberland, V., Baird, D., et al. (2018). The MR-Base platform supports systematic causal inference across the human phenome. Elife 7, e34408. doi: 10.7554/eLife.34408
Jansen, P. R., Watanabe, K., Stringer, S., Skene, N., Bryois, J., Hammerschlag, A. R., et al. (2019). Genome-wide analysis of insomnia in 1,331,010 individuals identifies new risk loci and functional pathways. Nat. Genet. 51(3), 394–403. doi: 10.1038/s41588-018-0333-3
Kang, S., Gim, J., Lee, J., Gunasekaran, T. I., Choi, K. Y., Lee, J. J., et al. (2021). Potential Novel Genes for Late-Onset Alzheimer’s Disease in East-Asian Descent Identified by APOE-Stratified Genome-Wide Association Study. J. Alzheimers Dis. 82(4), 1451–1460. doi: 10.3233/JAD-210145
Kettunen, J., Demirkan, A., Würtz, P., Draisma, H. H. M., Haller, T., Rawal, R., et al. (2016). Genome-wide study for circulating metabolites identifies 62 loci and reveals novel systemic effects of LPA. Nat. Commun. 7, 11122. doi: 10.1038/ncomms11122
Koyama, S., Ito, K., Terao, C., Akiyama, M., Horikoshi, M., Momozawa, Y., et al. (2020). Population-specific and trans-ancestry genome-wide analyses identify distinct and shared genetic risk loci for coronary artery disease. Nat. Genet. 52(11), 1169–1177. doi: 10.1038/s41588-020-0705-3
Kunkle, B. W., Grenier-Boley, B., Sims, R., Bis, J. C., Damotte, V., Naj, A. C., et al. (2019). Genetic meta-analysis of diagnosed Alzheimer’s disease identifies new risk loci and implicates Aβ, tau, immunity and lipid processing. Nat. Genet. 51(3), 414–430. doi: 10.1038/s41588-019-0358-2
Lambert, J. C., Ibrahim-Verbaas, C. A., Harold, D., Naj, A. C., Sims, R., Bellenguez, C., et al. (2013). Meta-analysis of 74,046 individuals identifies 11 new susceptibility loci for Alzheimer's disease. Nat. Genet. 45(12), 1452–8. doi: 10.1038/ng.2802
Lane, J. M., Jones, S. E., Dashti, H. S., Wood, A. R., Aragam, K. G., van Hees, V. T., et al. (2019). Biological and clinical insights from genetics of insomnia symptoms. Nat. Genet. 51(3), 387–393. doi: 10.1038/s41588-019-0361-7
Lawlor, D. A., Tilling, K., and Davey Smith, G. (2016). Triangulation in aetiological epidemiology. Int. J. Epidemiol. 45(6), 1866–1886. doi: 10.1093/ije/dyw314
Lee, J. J., Wedow, R., Okbay, A., Kong, E., Maghzian, O., Zacher, M., et al. (2018). Gene discovery and polygenic prediction from a genome-wide association study of educational attainment in 1.1 million individuals. Nat. Genet. 50(8), 1112–1121. doi: 10.1038/s41588-018-0147-3
Morrison, J., Knoblauch, N., Marcus, J. H., Stephens, M., and He, X. (2020). Mendelian randomization accounting for correlated and uncorrelated pleiotropic effects using genome-wide summary statistics. Nat. Genet. 52(7), 740–747. doi: 10.1038/s41588-020-0631-4
Mounier, N., and Kutalik, Z. (2023). Bias correction for inverse variance weighting Mendelian randomization. Genet. Epidemiol. 47(4), 314–331. doi: 10.1002/gepi.22522
Munafò, M. R., and Davey Smith, G. (2018). Robust research needs many lines of evidence. Nature 553(7689), 399–401. doi: 10.1038/d41586-018-01023-3
Nalls, M. A., Blauwendraat, C., Vallerga, C. L., Heilbron, K., Bandres-Ciga, S., Chang, D., et al. (2019). Identification of novel risk loci, causal insights, and heritable risk for Parkinson's disease: a meta-analysis of genome-wide association studies. Lancet Neurol. 18(12), 1091–1102. doi: 10.1016/S1474-4422(19)30320-5
Patsopoulos, N. A., Baranzini, S. E., Santaniello, A., Shoostari, P., Cotsapas, C., Wong, G., et al. (2019). Multiple sclerosis genomic map implicates peripheral immune cells and microglia in susceptibility. Science 365(6460), eaav7188. doi: 10.1126/science.aav7188
Popper, K. (1959). The Logic of Scientific Discovery. London: Hutchinson. doi: 10.4324/9780203994627
Sanderson, E., Davey Smith, G., Windmeijer, F., and Bowden, J. (2019). An examination of multivariable Mendelian randomization in the single-sample and two-sample summary data settings. Int. J. Epidemiol. 48(3), 713–727. doi: 10.1093/ije/dyy262
Sanderson, E. (2021a). Multivariable Mendelian Randomization and Mediation. Cold Spring Harb. Perspect. Med. 11(2), a038984. doi: 10.1101/cshperspect.a038984
Sanderson, E., Richardson, T. G., Hemani, G., and Davey Smith, G. (2021b). The use of negative control outcomes in Mendelian randomization to detect potential population stratification. Int. J. Epidemiol. 50(4), 1350–1361. doi: 10.1093/ije/dyaa288
Seyedsalehi, A., Warrier, V., Bethlehem, R. A. I., Perry, B. I., Burgess, S., and Murray, G. K. (2023). Educational attainment, structural brain reserve and Alzheimer’s disease: a Mendelian randomization analysis. Brain 146(5), 2059–2074. doi: 10.1093/brain/awac392
Skrivankova, V. W., Richmond, R. C., Woolf, B. A. R., Yarmolinsky, J., Davies, N. M., Swanson, S. A., et al. (2021). Strengthening the Reporting of Observational Studies in Epidemiology Using Mendelian Randomization: The STROBE-MR Statement. JAMA 326(16), 1614–1621. doi: 10.1001/jama.2021.18236
Sudlow, C., Gallacher, J., Allen, N., Beral, V., Burton, P., Danesh, J., et al. (2015). UK Biobank: An Open Access Resource for Identifying the Causes of a Wide Range of Complex Diseases of Middle and Old Age. PLoS Med. 12(3), e1001779. doi: 10.1371/journal.pmed.1001779
Suhre, K., Arnold, M., Bhagwat, A. M., Cotton, R. J., Engelke, R., Raffler, J., et al. (2017). Connecting genetic risk to disease end points through the human blood plasma proteome. Nat. Commun. 8, 14357. doi: 10.1038/ncomms14357
Sun, B. B., Maranville, J. C., Peters, J. E., Stacey, D., Staley, J. R., Blackshaw, J., et al. (2018). Genomic atlas of the human plasma proteome. Nature 558(7708), 73–79. doi: 10.1038/s41586-018-0175-2
Verbanck, M., Chen, C. Y., Neale, B., and Do, R. (2018). Detection of widespread horizontal pleiotropy in causal relationships inferred from Mendelian randomization between complex traits and diseases. Nat. Genet. 50(5), 693–698. doi: 10.1038/s41588-018-0099-7
Zheng, J., Zhang, Y., Rasheed, H., Walker, V., Sugawara, Y., Li, J., et al. (2021). Trans-ethnic Mendelian-randomization study reveals causal relationships between cardiometabolic factors and chronic kidney disease. Int. J. Epidemiol. 50(6), 1995–2010. doi: 10.1093/ije/dyab203

## Figure legends

**Figure 1.** The six-gate falsification framework. (**A**) Six falsification gates, each operationalizing one failure mode of MR inference; cumulative 0–12 scores assign grades A–D. (**B**) Comparison with the traditional one-shot MR pipeline.

**Figure 2.** Simulation operating characteristics across 43,200 replicates. Sensitivity, specificity, and FDR by pleiotropy regime, LD concentration, and effect size; grade calibration by effect size.

**Figure 3.** Case study MR results (insomnia–AD). (A) Key MR estimates showing clump reversal and education protection; (B) colocalization asymmetry (reverse-dominated, 18/32 reverse vs. 1/47 forward).

**Figure 4.** APOE-locus shared liability: genome-wide $r_g$, chromosome-19 removal, and locus-specific colocalization.

**Figure 5.** Validation cohort grades (12 cases) and cross-ancestry directional consistency.

## Tables

**Table 1.** Gate decision matrix for the six-gate falsification framework. See "The six gates" section for detailed definitions and scoring rules.

| Gate | Failure mode | Method | Pass criterion (score = 2; otherwise 0) |
|------|--------------|--------|------------------------------------------|
| G1 | Association / screening | Unclumped IVW; liberal screen at $P < 0.05$ | Unclumped IVW nominally significant in the claimed direction |
| G2 | Robustness to LD / overlap / pleiotropy | LD clump ($r^2 < 0.001$) + MRlap + CAUSE; directional reversal $\Rightarrow$ falsified | Clumped IVW significant; no Egger intercept or $Q$ heterogeneity ($P \ge 0.05$) |
| G3 | Genetic architecture | LDSC $r_g$ + coloc (PP.H4 $\ge 0.80$) | $r_g$ direction-consistent (or null) with locus-specific sharing |
| G4 | Direct effect | MVMR vs. education, depression, cardiometabolic; conditional $F > 10$ | Significant direct effect in claimed direction ($F > 10$) |
| G5 | Biological mediation | Two-step MR; Benjamini–Hochberg FDR + bootstrap CI | FDR-corrected indirect effect consistent with the claim |
| G6 | External validation | Cross-ancestry replication (power $\ge 80\%$ scores) | Cross-ancestry directional consistency in claimed direction |

*All gates apply fixed a priori thresholds and contribute 0 or 2 points (maximum 12). IVW, inverse-variance weighted; LD, linkage disequilibrium; MRlap, sample-overlap-corrected MR; CAUSE, correlated-pleiotropy MR; LDSC, linkage-disequilibrium score regression; MVMR, multivariable MR; FDR, false discovery rate. Underpowered validations (achieved power < 80%) inform direction only and assign no points.* |

**Table 2.** Simulation operating characteristics of the six-gate framework (43,200 replicates; seed 20260804).

| Pleiotropy regime | Effect size (β per SD) | Sensitivity (Grade A/B) | Specificity (Grade D) | P(Grade A) | Empirical FDR |
|---|---|---|---|---|---|
| None | 0.00 | — | 1.000 | 0.000 | 0.000 |
| None | 0.08 | 0.506 | — | 0.213 | 0.000 |
| None | 0.15 | 0.973 | — | 0.875 | 0.000 |
| Balanced | 0.00 | — | 0.796 | 0.061 | 0.042–0.125 |
| Balanced | 0.08 | 0.527 | — | 0.354 | 0.042–0.125 |
| Balanced | 0.15 | 0.847 | — | 0.717 | 0.042–0.125 |
| Directional | 0.00 | — | 0.679 | 0.046 | 0.081–0.183 |
| Directional | 0.08 | 0.545 | — | 0.367 | 0.081–0.183 |
| Directional | 0.15 | 0.804 | — | 0.667 | 0.081–0.183 |

Values are marginal across LD concentration (5/12/40 blocks), sample overlap (0%/30%), and instrument count (20/60); 400 replicates per parameter cell. Sensitivity is the proportion of replicates graded A or B; specificity the proportion graded D at β = 0; FDR is the empirical false-discovery proportion among positive calls, computed across the full effect-size mixture (one-third null, two-thirds non-null replicates) and reported as the range across the parameter grid. Full operating characteristics by parameter cell are given in Supplementary Table S9.


**Table 3.** Data inventory: publicly available GWAS summary statistics used in this study.

| Trait / role | Accession | Source | Sample size | Ancestry |
|---|---|---|---|---|
| Insomnia (continuous), exposure | ukb-b-3957 | UK Biobank | 462,341 | European |
| Alzheimer's disease (primary outcome) | ieu-b-2 | Kunkle et al. (2019), IGAP | 21,982 cases / 41,944 controls | European |
| Alzheimer's disease (sensitivity outcome) | ebi-a-GCST90027158 | Bellenguez et al. (2022) | 85,934 cases / 401,577 controls | European |
| Educational attainment (mediator/confounder) | ieu-a-1239 | Lee et al. (2018) | 766,345 | European |
| Alzheimer's disease (East Asian) | NG00182 | GARD | 6,518 (2,919 cases) | East Asian |
| CRP / IL-6 / NfL pQTLs | prot-a-670 / prot-a-1540 / prot-a-2027 | Sun et al. (2018), INTERVAL | 3,301 | European |
| GFAP pQTL | prot-c-3034_1_2 | Suhre et al. (2017), KORA | 1,000 | European |
| Triglycerides (NMR) | met-d-Total_TG | Kettunen et al. (2016), Nightingale platform | 24,925 | European |
| Supplementary outcomes (East Asian) | — | BioBank Japan | — | East Asian |

All summary statistics were harmonized on build GRCh37. The 36 AD-relevant candidate pQTLs screened in Gate G5 derive from the INTERVAL panel above (25 evaluable after instrument quality filtering).


**Table 4.** Step-by-step execution protocol with estimated timings and pause points. See "Step-by-step execution protocol" section for detailed procedures.

| Step | Gate / stage | Procedure | Estimated time | Pause point |
|------|--------------|-----------|----------------|-------------|
| 1 | Harmonization | Extract instruments at $P < 5 \times 10^{-8}$; harmonize alleles and strand orientation against the LD reference; align exposure and outcome summary statistics. | $\approx 1.5\text{ h}$ | Pause point 1 |
| 2 | Gate G1 | Run unclumped IVW using the full instrument set. | $15\text{--}30\text{ min}$ | — |
| 3 | Gate G2 | Perform LD clumping at $r^2 < 0.001$ within $10,000\text{ kb}$; re-estimate IVW on clumped instruments; run MR-Egger and Cochran $Q$ tests; calculate MRlap corrections using the cross-trait LDSC intercept; fit CAUSE models. | $2\text{--}4\text{ h}$, includes CAUSE MCMC fitting | Pause point 2 |
| 4 | Gate G3 | Munge summary statistics; compute $r_g$ via LDSC; perform per-locus colocalization across independent loci with $PP.H4 \ge 0.80$. | $1\text{--}2\text{ h}$ | Pause point 3 |
| 5 | Gate G4 | Fit multivariable MR models including specified confounders; calculate conditional $F$-statistics. | $30\text{--}45\text{ min}$ | Pause point 4 |
| 6 | Gate G5 | Execute two-step MR across the mediator panel; apply Benjamini–Hochberg FDR adjustments; derive $10,000$-replicate bootstrap confidence intervals for indirect effects. | $3\text{--}6\text{ h}$, includes bootstrap | Pause point 5 |
| 7 | Gate G6 | Conduct cross-ancestry replication using ancestry-matched LD clumping; calculate validation-cohort grades. *End:* sum the $0\text{--}12$ score and map the total to grades A–D. | $1\text{--}2\text{ h}$ | — |

**Table 5.** Troubleshooting guide: common pitfalls, causes, and remedies across the six gates.

| Issue | Remedy |
|-------|--------|
| MRlap covariance non-positive-definiteness under substantial sample overlap and weak instruments | Prune variant sets to per-SNP $F > 20$ and inspect the cross-trait LDSC intercept. |
| CAUSE non-convergence with sparse variant panels | Relax pre-pruning thresholds to $r^2 < 0.05$ or extend the MCMC sampling chain. |
| Colocalization power loss from incomplete regional coverage | Impute regional summary statistics using the 1000 Genomes reference panel. |
| Conditional $F$-statistics $< 10$ in MVMR due to collinearity | Restrict instruments to variants associated exclusively with the targeted exposure. |
| Cross-ancestry inflation driven by LD mismatch | Re-clump summary statistics using an ancestry-matched reference panel. |

*Display items: 5 figures + 5 tables = 10 (within the Frontiers Methods limit of 15).*

---
