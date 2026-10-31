# 审稿应答 · 第 2 轮定向精读（自包含投喂件）

> 用途：把外部模型在第 1 轮点名要看、且**只有看到原文才能判断**的 12 个文段，按行号从稿件实时切下来，做成一份可直接粘贴的单文件。
> 源文件：`课题设计阶段/manuscript_Frontiers_Methods_v2_humanized.md`（296 行）；本文件由 `reviews/make_round2_excerpt.py` 生成，**改稿后必须重跑**，否则行号漂移。
> 摘录正文共 33827 字符 ≈ 9,396 tokens；12 段。

---

## 一、怎么用

| 场景 | 做法 |
|---|---|
| 外部模型**不能**读文件（网页版） | 把「二、提示词」+「三、摘录」**整份**粘贴给它 |
| 外部模型**能**读文件（同机 agent） | 只发「二、提示词」；它自己按行号读 `课题设计阶段/manuscript_Frontiers_Methods_v2_humanized.md` |

两种方式等价：摘录内容与它自己读到的完全一致（逐字切片，未做任何删改或改写）。

---

## 二、提示词（原样复制）

```text
只读这一份文件的指定行区间，读完即停：
C:/D/workbuddy/科研/共病分析/课题设计阶段/manuscript_Frontiers_Methods_v2_humanized.md
- L11–L18（Abstract）｜判断目标：判断因果术语是否前后一致；此处 "precise" 指什么
- L30–L52（Materials and Equipment）｜判断目标：判断 LD 参考面板、EAS 数据与软件版本描述是否足以回应 R3#3
- L59–L78（The six gates + Grading rubric）｜判断目标：判断六门定义、部分计分、Grade C 与 decisive failure 规则是否自洽
- L79–L90（Step-by-step execution protocol）｜判断目标：判断 Egger/Q/MRlap/CAUSE 是筛 IV 还是敏感性检查
- L91–L95（Simulation-based validation: design and DGP）｜判断目标：判断 DGP 正文与 R1#2 所指代码差异的精确落点
- L98–L103（Operating characteristics（结果段））｜判断目标：判断 sens/spec/FDR/0.20 阈值的定义与呈现
- L104–L121（Example of application: insomnia–AD）｜判断目标：判断 null、反向显著、CAUSE、APOE/chr19 表述
- L122–L130（Precision, limits of detection, pitfalls）｜判断目标：判断检测下限与排障段是否已承认低功效边界
- L131–L146（Discussion）｜判断目标：判断药物靶点外推、Limitations 与结论口径是否过强
- L210–L221（Figure legends）｜判断目标：判断图注是否与评分规则、12 例验证、APOE 叙述冲突
- L222–L235（Table 1（含表题））｜判断目标：判断 Table 1 是否确有"仅 0/2 分"脚注及需怎样改
- L237–L251（Table 2（含表题））｜判断目标：判断 Table 2 是否需重算 C/D 特异度、CI 与 FDR 不确定性

禁止：读该文件的其余部分、读任何其他文件、列目录、搜索。

硬红线（本包已内嵌，不必重读）：数字只引用不重算；不得把"证据不足"写成"证据反对"；缺数据只写缺数据、不得建议补做不可得分析；禁引 PhenoScanner；不跨 estimand 排名；
禁用 novel / first / best / optimal / solution / breakthrough；固定术语 six-gate falsification framework / G1–G6 / Grade A–D / locus-driven confounding；
不虚构作者决定；不得建议删除对冲措辞（bounded by / cannot be ruled out / Limitations 各条）；已投稿版本不动，只给改法不给全文。

## 已核实事实（作者方已完成核查，直接引用，不要重新推测、不要推翻、不要写成"可能/似乎"）

F1 评分制式冲突（R1#1 的根因，已实测）。模拟代码 `code/sim_framework_operating_chars.py` 实际用 **0/1/2 三档**（pass=2 / partial=1 / fail=0）；正文与 Table 1 只写 **0/2 两档**。R1#1 追问的"1 分"与 education-T2D 的"9 分"同出于此，不是 Supplementary Table S8 抄错。
F2 六门在 43,200 条模拟里实际只有 3–4 个自由度（已逐条统计）：G3 取值仅 {0,2}（恒得 2，因 clumping 每块必留一个 SNP）；G4 与 G2 完全共线（G2>0 ⟺ G4>0，43,200 条零例外）；G5 的 1 分全库仅出现 10 次。→ 任何"六门独立累积、分数随效应量单调"的线性表述都不成立。
F3 "G2 失败仍可评 A 级"：按正文 0/2 规则**可达**（其余五门满分 = 10 = Grade A 下界）；按实际代码**不可达**（G2=0 时 43,200 条最高分 8.0）。因此该条答案取决于制式选择，两种都能自洽，混用必被再问一轮。
F4 模拟 DGP 未生成任何 LD 相关结构：`bx = rng.normal(0, 0.12, n_iv)` 各 SNP 独立抽样，`block` 仅作聚类索引。→ 改法中禁止出现"模拟刻画了 LD 相关工具 / 相关工具导致虚假精度"一类断言（代码里不存在此机制）。此点审稿人未点名，回应信不主动展开。
F5 Zenodo 归档已逐字节核对（记录 21858125 的 md5 与下载值一致）。稿件六处引用的 DOI 21858125 = **v1.0.0（2026-08-09）**；归档内模拟脚本逐字节等于 git `b983865`（08-06），而投稿版为 `3225fea`（09-02），两者差一次**按效应量单算敏感度**的聚合修正。后果（同一份 `sim_replicates.csv` 两套聚合实测）：S9 逐格敏感度与归档逻辑 **0/72** 一致、与投稿逻辑 **72/72** 一致；Fig 2 A 面板归档逻辑 0.738→0.738（变平）、投稿逻辑 0.500→0.976；**Table 2 与全部实证结果不受影响**。另有 **v1.1.0（记录 22064685，2026-08-23）未被稿件引用**；概念 DOI 为 21858124。
F6 R1#2 说"CAUSE / MRlap 缺失"的准确范围：CAUSE（`code/r_analysis/01c_cause_patched.R`，含 loo≥2.6 的 monkey-patch）与 MRlap（`01b_overlap_correction.R`）以及 MVMR、LDSC 等 9 个经验分析 R 脚本**都在归档内**，剥离注释后纯代码相似度 0.83–0.98，差异只有 `C:/Temp/iad_g1/…`→`./output/…` 与中文提示串被英译。→ 缺失发生在 **43,200 条模拟网格内**（模拟只做 IVW 类判定），不是归档里没有实现。此区分必须写清。
F7 其他已核实小项：稿件四处写 `renv.lockfile`，归档内实际文件名为 `renv.lock`；`S7_iv_annotation_confounder.csv` 有文件但无生成脚本。

## 输出

两张表，不要导言、不要复述稿件、不要写修改后的完整段落：

**表 1 —— 逐条应答方案**（上限 22 行，按 P0→P2）
`编号 | 处置结论（照改 / 需补分析 / 需重跑数值 / 据理反驳 / 仅格式） | 落点（行号 + 章节 + 关键词） | 具体改法（≤40 字，动词开头） | 需补的数字或表（无则填"—"） | 主要风险（≤15 字）`

**表 2 —— 我方说满的地方**（上限 8 行）
即你在正文里读到的**过度断言**：把"未能检出"说成"已排除"、把"框架提供分诊"说成"解决可信性"、把工具数当作独立证据量、把未建模变异写成偏倚下界一类。
`行号 + 原句片段（≤12 词） | 问题类型 | 建议替换文本（给出可直接替换的英文句子） | 理由（≤20 字）`

补充要求（合计不超过 10 行）：
1. 凡表中出现"需补分析 / 需重跑数值"的行，用一句话说明**能否在不重跑前提下降级为文字回应**（能 / 不能 + 半句理由）。
2. 对 R1#1 / R1#2 / R1#4 三行，必须给出**制式裁定**：明确选「甲 = 正式采用 0/1/2 三档」还是「乙 = 回退全 0/2 并加决定性失败规则」，并列出该选择的连带改动清单（Table 1、S8、模拟脚本、κ、Table 2 中哪些要动）。二选一，不要"两种都可以"。
3. 若你认为 F2 使"六门加性评分"本身难以辩护，直说，并给出最小可行修补（不要求重跑）。
```

> 上表中 12 个区间**不是**模型原话的等号复制：表 1/表 2 两处已把**表题行**（L222、L237）并入，否则切片里看不到 "Table 1." / "Table 2." 的编号。其余 10 段与模型自述的区间逐行一致。

---

## 三、逐段摘录（12 段，逐字）

每段上方是坐标与该段的判断目标；正文未做任何省略、未加批注。

### 段 1 ｜ L11–L18 ｜ Abstract

**对应意见**：R3#1、R3#2 ｜ **判断目标**：判断因果术语是否前后一致；此处 "precise" 指什么

````text
## Abstract

Mendelian randomization (MR) uses germline variants as instrumental variables to estimate causal relationships, relying on relevance, independence, and exclusion-restriction assumptions. When a single locus of large effect, such as *APOE* in Alzheimer's disease (AD), dominates trait genetic architecture, standard MR pipelines often yield precise, statistically significant estimates that do not reflect directed causal effects. This failure mode is termed locus-driven confounding. Here, we present a six-gate falsification framework that tests causal claims using six criteria: association screening, robustness, genetic architecture, direct effect, biological mediation, and external validation. Evidence across these gates is aggregated into an *a priori* grade (A–D) ranging from 0 to 12 points. To define its operating characteristics, we benchmarked 43,200 simulated two-sample MR scenarios covering variations in linkage disequilibrium (LD) concentration, pleiotropy regimes, sample overlap, effect sizes, and instrument counts, evaluating each replicate across all gates. Under the null hypothesis without pleiotropy, the framework demonstrated 100% specificity with zero false discoveries. In the presence of balanced pleiotropy, marginal specificity was $\approx 0.80$, corresponding to a marginal false discovery rate (FDR) of $\approx 0.08$ (scenario range 0.04–0.13). Sensitivity reached 0.97 at the highest effect size grid in the absence of pleiotropy, and assigned grades showed a monotonic relationship with effect size.

We evaluated the framework on the association between insomnia and AD as an empirical benchmark. A previously reported unclumped positive association ($\beta$ = +0.10, $P$ = $9.3 \times 10^{-4}$) was reclassified as shared liability driven by the *APOE* locus (Grade C). The association attenuated to the null after LD clumping ($\beta$ = $-0.13$, $P$ = 0.52), genome-wide genetic correlation was negligible ($r_g$ = $-0.028$, $P$ = 0.57), colocalization was consistent with reverse-direction variant sharing, and no protein mediators were identified. In contrast, educational attainment maintained an inverse association with AD ($\beta$ = $-0.33$, $P$ = $1.1 \times 10^{-5}$). The pipeline is fully reproducible via `renv.lockfile` (R 4.5.2) and archived on Zenodo (DOI 10.5281/zenodo.21858125), offering a standardizable protocol for graded causal inference in polygenic epidemiology.

**Keywords:** Alzheimer's disease; APOE; benchmarking; causal inference; falsification framework; locus-driven confounding; Mendelian randomization; operating characteristics
````

### 段 2 ｜ L30–L52 ｜ Materials and Equipment

**对应意见**：R3#3、R3#4（间接） ｜ **判断目标**：判断 LD 参考面板、EAS 数据与软件版本描述是否足以回应 R3#3

````text
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
````

### 段 3 ｜ L59–L78 ｜ The six gates + Grading rubric

**对应意见**：R1#1、R1#4、R3#4、R3#6、R3#8 ｜ **判断目标**：判断六门定义、部分计分、Grade C 与 decisive failure 规则是否自洽

````text
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
````

### 段 4 ｜ L79–L90 ｜ Step-by-step execution protocol

**对应意见**：R3#5、R3#8、R1#2（对照） ｜ **判断目标**：判断 Egger/Q/MRlap/CAUSE 是筛 IV 还是敏感性检查

````text
### Step-by-step execution protocol

The pipeline processes gates in a sequential workflow (Table 4). Intermediate outputs are saved at designated pause points to allow downstream re-analysis without repeating prior calculations.

1. **Harmonization** ($\approx 1.5\text{ h}$). Extract instruments at $P < 5 \times 10^{-8}$; harmonize alleles and strand orientation against the LD reference; align exposure and outcome summary statistics. *Pause point 1:* save harmonized unclumped instrument set.
2. **Gate G1** ($15\text{--}30\text{ min}$). Run unclumped IVW using the full instrument set.
3. **Gate G2** ($2\text{--}4\text{ h}$, includes CAUSE MCMC fitting). Perform LD clumping at $r^2 < 0.001$ within $10,000\text{ kb}$; re-estimate IVW on clumped instruments; run MR-Egger and Cochran $Q$ tests; calculate MRlap corrections using the cross-trait LDSC intercept; fit CAUSE models. *Pause point 2:* save clumped instrument set, MRlap output, and CAUSE posteriors.
4. **Gate G3** ($1\text{--}2\text{ h}$). Munge summary statistics; compute $r_g$ via LDSC; perform per-locus colocalization across independent loci with $PP.H4 \ge 0.80$. *Pause point 3:* save LDSC log files and colocalization matrices.
5. **Gate G4** ($30\text{--}45\text{ min}$). Fit multivariable MR models including specified confounders; calculate conditional $F$-statistics. *Pause point 4:* export multivariable MR coefficients and conditional $F$-statistics.
6. **Gate G5** ($3\text{--}6\text{ h}$, includes bootstrap). Execute two-step MR across the mediator panel; apply Benjamini–Hochberg FDR adjustments; derive $10,000$-replicate bootstrap confidence intervals for indirect effects. *Pause point 5:* save FDR-adjusted mediation tables.
7. **Gate G6** ($1\text{--}2\text{ h}$). Conduct cross-ancestry replication using ancestry-matched LD clumping; calculate validation-cohort grades. *End:* sum the $0\text{--}12$ score and map the total to grades A–D.
````

### 段 5 ｜ L91–L95 ｜ Simulation-based validation: design and DGP

**对应意见**：R1#2、R3#9 ｜ **判断目标**：判断 DGP 正文与 R1#2 所指代码差异的精确落点

````text
### Simulation-based validation: design and data-generating process

Because the framework is prescriptive, its operating characteristics require quantitative evaluation prior to empirical deployment. We generated polygenic two-sample MR summary statistics under known ground truth, varying: causal effect size $\beta \in \{0, 0.08, 0.15\}$ per standard deviation; LD structure ($5$, $12$, or $40$ blocks); pleiotropy mode (none, balanced, directional); sample overlap ($0%$ or $30%$); and instrument count ($20$ or $60$). Instrument effects were sampled with mean per-variant $F \approx 36$. Each parameter combination was replicated $400$ times ($3 \times 3 \times 3 \times 2 \times 2 \times 400 = 43,200$ total iterations). Every replicate was evaluated through all six gates and assigned a grade using the $0\text{--}12$ rubric. Empirical FDR was computed across the full effect-size mixture (one-third null and two-thirds non-null replicates per parameter cell), reflecting the framework's intended usage in which null and candidate claims are evaluated together.

The full data-generating process is defined in the archived code repository (Zenodo DOI: 10.5281/zenodo.21858125). Key features include LD blocks simulated from block-diagonal correlation matrices, balanced pleiotropy represented as independent, symmetric effects on the outcome, directional pleiotropy modeled as a systematic bias aligned with the exposure effect, and sample overlap induced by introducing correlated residual noise between exposure and outcome samples. Evaluated metrics include specificity ($1 - \text{Type I error}$), sensitivity (power), empirical FDR, and monotonicity of grade calibration across effect sizes.
````

### 段 6 ｜ L98–L103 ｜ Operating characteristics（结果段）

**对应意见**：R1#4 ｜ **判断目标**：判断 sens/spec/FDR/0.20 阈值的定义与呈现

````text
### Operating characteristics of the framework (43,200-simulation benchmark)

At the null ($\beta = 0$), the framework achieved 100% specificity and a zero false discovery rate ($\text{FDR} = 0$) in the absence of pleiotropy, confirming Type I error control in the ideal parameter space. Under balanced pleiotropy, marginal specificity was 0.80 (scenario range 0.77–0.84) with a marginal FDR of 0.08 (scenario range 0.04–0.13). Directional pleiotropy increased the marginal FDR to 0.13 (scenario range 0.08–0.18), which remained below the nominal 0.20 decision threshold. For the largest effect size tested ($\beta = 0.15$), marginal sensitivity reached 0.97 (scenario range 0.95–1.00) without pleiotropy, declining to approximately 0.85 under balanced pleiotropy and 0.80 under directional pleiotropy. At $\beta = 0.08$, sensitivity dropped to approximately 0.5 across all regimes, reflecting lower power to detect modest effects. Grade assignment scaled monotonically with effect size. Without pleiotropy, marginal Grade A frequency increased from 0 at the null to 0.88 at $\beta = 0.15$ (scenario range 0.62–1.00), falling to 0.72 under balanced pleiotropy (scenario range 0.51–0.95) and 0.67 under directional pleiotropy. Under null conditions without pleiotropy, 100% of replicates received Grade D, compared with 0.80 under balanced pleiotropy and 0.68 under directional pleiotropy. No null replicate received Grade A in the absence of pleiotropy, whereas 6% under balanced pleiotropy and 5% under directional pleiotropy were assigned Grade A. Complete operating characteristics are provided in Supplementary Table S9, Table 2, and Figure 2.

**Interpretation for users.** A grade of A–B indicates that the claim aligns with a directed causal effect at the framework's measured sensitivity for the tested effect size. A grade of C–D indicates that the claim is falsified or supported exclusively by shared-liability evidence. Borderline assignments (B/C) represent provisional findings requiring further empirical validation.
````

### 段 7 ｜ L104–L121 ｜ Example of application: insomnia–AD

**对应意见**：R1#5、R1#6、R1#7、R3#7、R3#11 ｜ **判断目标**：判断 null、反向显著、CAUSE、APOE/chr19 表述

````text
### Example of application: the insomnia–AD proof-of-concept

**Data.** Insomnia: ukb-b-3957 ($n = 462,341$, continuous trait; cf. Jansen et al., 2019; Lane et al., 2019). Alzheimer's disease (AD): ieu-b-2 (Kunkle et al., 2019; 21,982 cases, 41,944 controls) as the primary outcome, with ebi-a-GCST90027158 (Bellenguez et al., 2022; 85,934 cases, 401,577 controls) as a sensitivity outcome. Educational attainment: ieu-a-1239 ($n = 766,345$). Protein pQTLs from the INTERVAL panel (Sun et al., 2018; $n = 3,301$) and NMR metabolites from Kettunen et al. (2016). East Asian sensitivity evaluations incorporated GARD AD (NG00182; $n = 6,518$) and BioBank Japan summary statistics (Koyama et al., 2020; Kang et al., 2021). All datasets were harmonized on GRCh37.

**G1: association.** Unclumped inverse-variance weighted (IVW) analysis yielded $\beta = +0.104$ ($\text{SE} = 0.031$, $P = 9.3 \times 10^{-4}$; 2,462 instruments), reproducing the published positive association (Figure 3A).

**G2: robustness.** LD clumping ($r^2 < 0.001$, 10,000 kb window) reduced the instrument set to 54 variants and attenuated the estimate to the null ($\beta = -0.130$, $\text{SE} = 0.203$, $P = 0.52$). A narrower window (5,000 kb; 37 instruments) produced consistent results ($\beta = -0.111$, $P = 0.64$). Correcting for sample overlap via MRlap sustained the null ($\beta = -0.078$, $P = 0.43$). CAUSE fitting on the clumped instrument sets retained a boundary forward CAUSAL classification in both AD sources (Kunkle: causal $P = 0.039$; Bellenguez: causal $P = 0.002$), whereas both reverse analyses were classified as pleiotropy or sharing ($P = 0.08$ and $P = 0.63$). The Bellenguez classification must be interpreted cautiously, because that AD source showed extreme heterogeneity in related analyses (Cochran $Q$ $P = 1.7 \times 10^{-11}$; Supplementary Table S4), rendering its estimates unreliable. CAUSE therefore constitutes a single method-level disagreement against three null results (clumped IVW, MRlap, and the MVMR direct effect below); we report this disagreement explicitly rather than treating the boundary CAUSAL label as evidence for a directed effect. This signal attenuation was not driven by the *APOE* locus, as excluding 118 chromosome-19 instruments retained the unclumped association ($\beta = 0.094$, $P = 0.003$). These two observations operate at different levels: the unclumped precision reflects genome-wide instrument correlation, whereas the colocalization signal localizes to the *APOE* region; the former concerns instrument redundancy, the latter locus-specific shared liability, and they are not contradictory. Statistical power at the achieved instrument strength ($R^2 = 0.0022$ across 44 window-clumped loci; mean $F = 44.3$, minimum $F = 29.8$) was 24% for $\beta = 0.10$. Achieving 80% power required $\beta \ge 0.226$ ($\text{OR} \ge 1.25$ per standard deviation of insomnia liability; mRnd binary-outcome approximation with outcome GWAS sample size $n = 63,926$; Brion et al., 2013; Deng et al., 2020; Supplementary power tables). For transparency, the instrument count chain is: 2,462 unclumped instruments (Gate G1) $\rightarrow$ 54 LD-independent instruments after clumping ($r^2 < 0.001$, 10,000 kb) $\rightarrow$ 44 window-clumped loci (1-Mb window) retained for power estimation and confounder screening $\rightarrow$ 38 after removing six confounder-associated variants $\rightarrow$ 33 harmonized instruments. The 54-versus-40 discrepancy with the cross-ancestry step (Gate G6 below) reflects LD reference-panel updates between the primary European clumping (54 instruments) and the trans-ethnic re-clumping of the same instrument set against the updated panel (40 instruments), which we disclose for reproducibility. An instrument–confounder screen (GWAS Catalog IV-PheWAS across all 44 independent loci; a priori domains: smoking, alcohol, education/cognition, adiposity, depression/anxiety/neuroticism) identified six variants with documented associations in these domains, matching a negative-control framework (Sanderson et al., 2021b). Removing these variants maintained the null ($\beta = -0.106$, $\text{SE} = 0.252$, $P = 0.67$; 33 harmonized instruments; Supplementary Table S7). Heterogeneity diagnostics reflected this instrument-correlation pattern: on the unclumped set, Cochran's $Q$ was extreme ($Q = 3.66 \times 10^{3}$, $P = 1.25 \times 10^{-50}$), consistent with precision inflation from correlated instruments, whereas MR-Egger and the weighted-median/mode estimators were not separately reported for the clumped subsets (Supplementary Table S2).

**G3: genetic architecture.** Cross-trait LD Score regression (LDSC) yielded $r_g = -0.028$ ($\text{SE} = 0.050$, $P = 0.57$), which remained unchanged after excluding chromosome 19 ($r_g = -0.031$, $P = 0.53$), indicating no genome-wide shared polygenic architecture. Colocalization analysis identified strong support ($\text{PP.H4} \ge 0.80$) for 18 of 32 loci in the reverse direction, concentrated in the *APOE* region ($\text{PP.H4} > 0.98$), compared with 1 of 47 loci in the forward direction (Figure 3B). This asymmetry indicates locus-specific, *APOE*-centered genetic sharing (Supplementary Table S1; Figure 4).

**G4: direct effect.** Multivariable MR (MVMR) incorporating insomnia, education, depression, and LDL cholesterol revealed a protective direct effect for educational attainment ($\beta = -1.29$, $P = 0.008$, loose clump). The direct effect of insomnia was negative ($\beta = -0.57$, $P = 0.045$), opposite in direction to the original claim that insomnia elevates AD risk, further supporting falsification rather than a protective interpretation given the low power of this direct-effect model. Educational attainment PheWAS confirmed protective associations against AD ($\beta = -0.33$, $P = 1.1 \times 10^{-5}$; cf. Seyedsalehi et al., 2023) and Parkinson's disease ($\beta = -0.39$, $P = 7.2 \times 10^{-6}$; Nalls et al., 2019), but not multiple sclerosis ($\beta = +0.015$, $P = 0.90$; Patsopoulos et al., 2019).

**G5: biological mediation.** Protein mediation was absent along the insomnia $\rightarrow$ protein $\rightarrow$ AD pathway, as CRP and IL-6 indirect effects were null (overall $\text{FDR} = 0.91$). Screening 36 AD-relevant candidate proteins (25 evaluable) yielded no associations at $\text{FDR} < 0.05$. In the metabolite domain, circulating triglycerides mediated the protective effect of education (indirect $\beta = -0.031$, $\text{SE} = 0.008$, $q = 5.7 \times 10^{-4}$; bootstrap 95% CI $[-0.047, -0.017]$), accounting for 9% of the total educational effect.

**G6: external validation.** Directional consistency was maintained across East Asian cohorts for established directions. Education associated inversely with T2D risk using East Asian education instruments ($\beta = -0.145$, $P = 0.012$; cf. Chen et al., 2024), whereas the T2D $\rightarrow$ AD pathway remained null ($\beta = +0.006$, $P = 0.93$). Trans-ethnic evaluation (cf. Zheng et al., 2021) using 40 LD-independent European instruments in GARD East Asian AD summary statistics produced a negative IVW estimate ($\beta = -0.84$, $P = 0.28$), aligning with the European clumped null. Because statistical power was low ($<6%$), this step serves only for directional screening and contributes no scoring points (Supplementary Note 2). Across the 12-case validation cohort, the framework assigned Grade A to positive controls (LDL–CAD, education–AD), Grade B/C to reclassified or borderline traits (education–T2D, insomnia–AD), and Grade D to true nulls (BMI–AD, T2D–AD), yielding an inter-rater agreement of $\kappa = 0.76\text{--}0.94$ (Supplementary Table S8; Figure 5). A formal East Asian replication of the depression–AD case was not feasible with currently accessible data (Supplementary Note 1).

**Integrated verdict.** The cumulative 0–12 score maps to **Grade C: shared APOE-locus liability, no independent causal upstream.** This application shows how the framework re-evaluates a previously reported Mendelian randomization signal, yielding a graded verdict that accounts for pleiotropic confounding.
````

### 段 8 ｜ L122–L130 ｜ Precision, limits of detection, pitfalls

**对应意见**：R1#5 ｜ **判断目标**：判断检测下限与排障段是否已承认低功效边界

````text
### Precision, limits of detection, pitfalls, and troubleshooting

The benchmarked operating characteristics above define the precision of the framework. Limits of detection depend on statistical power. At instrument strengths typical of insomnia liability ($R^2 \approx 0.0022$), the procedure detects medium-to-large causal effects ($80%$ power at $\text{OR} \ge 1.25$ per standard deviation) but cannot exclude smaller effects. Consequently, cross-ancestry checks provide directional screening rather than definitive exclusion. Key methodological pitfalls and corrective actions are outlined in Table 5. Principal operational challenges include:

1. **MRlap covariance non-positive-definiteness under substantial sample overlap and weak instruments:** Prune variant sets to per-SNP $F > 20$ and inspect the cross-trait LDSC intercept.
2. **CAUSE non-convergence with sparse variant panels:** Relax pre-pruning thresholds to $r^2 < 0.05$ or extend the MCMC sampling chain.
3. **Colocalization power loss from incomplete regional coverage:** Impute regional summary statistics using the 1000 Genomes reference panel.
4. **Conditional $F$-statistics $< 10$ in MVMR due to collinearity:** Restrict instruments to variants associated exclusively with the targeted exposure.
5. **Cross-ancestry inflation driven by LD mismatch:** Re-clump summary statistics using an ancestry-matched reference panel.
````

### 段 9 ｜ L131–L146 ｜ Discussion

**对应意见**：R1#3、R1#10、R3#11 ｜ **判断目标**：判断药物靶点外推、Limitations 与结论口径是否过强

````text
## Discussion

The insomnia–AD findings demonstrate how a replicated Mendelian randomization (MR) signal can arise as an artifact of locus-driven confounding. They also show how a sequence of falsification gates translates that signal into a graded verdict with quantified statistical properties. Methodologically, the framework operationalizes six common MR failure modes as distinct gates, assigns evidence grades by fixed rules rather than subjective judgment, and reports operating characteristics derived from 43,200 simulated replicates. This calibration allows performance to be evaluated through measured Type I error and statistical power rather than asserted confidence.

The APOE result reflects a broader pattern in complex-trait genetics: when a single locus dominates genetic variance, genome-wide genetic correlation ($r_g$) and clumped MR can be null even while standard MR yields a positive signal. Analyses that omit clumping, sample-overlap correction, and architectural assessment remain susceptible to this artifact. Benchmarking established specific operating parameters for the framework: a specificity of 1.00 under the null without pleiotropy, a marginal false discovery rate (FDR) of approximately 0.08 under balanced pleiotropy, and sensitivity of 0.97 at the upper effect grid in the absence of pleiotropy. The monotonic grade calibration indicates that intermediate grades (B/C) reflect claims with provisional evidence.

**Complementarity with reporting standards.** While STROBE-MR defines reporting requirements, this framework evaluates whether reported evidence supports a causal claim at a specific grade. The combined approach targets two persistent challenges in polygenic epidemiology: incomplete pipeline reporting and over-confident evidence interpretation.

**Generalizability of the template.** Although insomnia–AD was chosen as a case study due to the extreme locus concentration at APOE, the framework functions independently of the underlying biological locus. It applies directly to other complex-trait pairs, including psychiatric exposures and cardiometabolic outcomes where pleiotropic instruments and sample overlap frequently occur. The codebase, simulation grid, and grading rubric are implemented in R 4.5.2 via `renv.lockfile` and archived for reuse (Zenodo DOI 10.5281/zenodo.21858125). Investigators can apply the same gate sequence to pre-specified hypotheses using harmonized summary statistics and a suitable LD reference without individual-level data.

**Implications for drug-target prioritization.** Distinguishing directed causation from locus-driven shared liability directly informs translational decisions. Causal claims that pass all six gates, such as LDL-cholesterol and coronary artery disease (Grade A; Allara et al., 2019), align with drug targets whose efficacy was confirmed in clinical trials. Conversely, claims that fail robustness gates despite replication, such as HDL-raising therapies, correspond to target interventions that failed in trials. The framework offers a preclinical triage system: Grade A–B signals warrant target investment, whereas Grade C–D signals indicate shared liability or confounding and are insufficient to justify interventional drug development.

**Limitations.** Several methodological boundaries apply. First, the framework was evaluated on 12 trait pairs enriched for borderline grades, requiring larger validation sets. Second, while the simulation grid covers 43,200 replicates, it does not encompass all genetic architectures; directional pleiotropy at the magnitude of APOE was not fully parameterized. Third, the primary case study achieved 80% power only for medium-to-large effects ($OR \ge 1.25$ per SD of insomnia liability), meaning small causal effects cannot be ruled out, and the trans-ethnic evaluation serves strictly as a directional screen. Fourth, the grade-boundary cutoffs (10–12, 7–9, 4–6, 0–3) are pre-specified but arbitrary. In the validation cohort, two of 12 cases fell within one point of a boundary (Height–CAD at 10, the lower bound of Grade A; Education–T2D at 9, the upper bound of Grade B); shifting a boundary by one point would move Height–CAD from A to B, so adjacent-grade assignments at the boundaries should be interpreted as provisional. Fifth, Steiger directional tests could not establish a reliable direction (the inferred direction flipped with the choice of $r$ construction; median $|r| \approx 0.002$), so directionality was not scored in this application and should be interpreted with caution. Finally, upstream summary-statistic quality and build harmonization remain critical prerequisites, as upstream errors alter downstream gate decisions.

**Conclusions.** A six-gate falsification framework with quantified operating characteristics reclassifies locus-driven MR artifacts into graded causal verdicts. In the insomnia–AD case study, the framework identifies a replicated MR signal as shared APOE-locus liability, offering a calibrated template for causal inference across polygenic traits.
````

### 段 10 ｜ L210–L221 ｜ Figure legends

**对应意见**：R1#6、R1#9 ｜ **判断目标**：判断图注是否与评分规则、12 例验证、APOE 叙述冲突

````text
## Figure legends

**Figure 1.** The six-gate falsification framework. (**A**) Six falsification gates, each operationalizing one failure mode of MR inference; cumulative 0–12 scores assign grades A–D. (**B**) Comparison with the traditional one-shot MR pipeline.

**Figure 2.** Simulation operating characteristics across 43,200 replicates. Sensitivity, specificity, and FDR by pleiotropy regime, LD concentration, and effect size; grade calibration by effect size.

**Figure 3.** Case study MR results (insomnia–AD). (A) Key MR estimates showing clump reversal and education protection; (B) colocalization asymmetry (reverse-dominated, 18/32 reverse vs. 1/47 forward).

**Figure 4.** APOE-locus shared liability: genome-wide $r_g$, chromosome-19 removal, and locus-specific colocalization.

**Figure 5.** Validation cohort grades (12 cases) and cross-ancestry directional consistency.
````

### 段 11 ｜ L222–L235 ｜ Table 1（含表题）

**对应意见**：R1#1 ｜ **判断目标**：判断 Table 1 是否确有"仅 0/2 分"脚注及需怎样改

````text
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
````

### 段 12 ｜ L237–L251 ｜ Table 2（含表题）

**对应意见**：R1#1、R1#4 ｜ **判断目标**：判断 Table 2 是否需重算 C/D 特异度、CI 与 FDR 不确定性

````text
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
````

---

## 四、摘录**没有**包含哪里（诚实标注）

| 行区间 | 内容 | 为什么没切 |
|---|---|---|
| L1–L10 | 标题 / 作者 / 单位 | 第 1 轮未点名；若你需要，直接说区间，不给也会被告知 |
| L19–L29 | Introduction | 第 1 轮未点名；若你需要，直接说区间，不给也会被告知 |
| L147–L164 | Declarations（数据、伦理、贡献、基金、COI、AI 声明） | 第 1 轮未点名；若你需要，直接说区间，不给也会被告知 |
| L165–L209 | References（42 条） | 第 1 轮未点名；若你需要，直接说区间，不给也会被告知 |
| L254–L293 | Table 3 数据清单、Table 4 执行步骤、Table 5 排障 | 第 1 轮未点名；若你需要，直接说区间，不给也会被告知 |

> 若模型判断某条意见必须看上述某段，请在输出里用 `L起–L止` 单独提出，不要基于缺失内容猜测。
