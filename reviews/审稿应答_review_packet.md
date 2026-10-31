# review_packet.md — 审稿应答投喂包（Reviewer 1 + Reviewer 3）

> **用途**：把「稿件 + 两位审稿人的 22 条意见 + 作者方初判」压成一个自包含投喂包，交给另一个模型
> 制定**应答与改稿方案**（不是让它在没读稿的情况下凭空点评）。
> **生成**：2026-10-27 17:14 ｜ **期刊**：Frontiers in Genetics（Methods / Computational Genomics）
> **稿件**：`C:/D/workbuddy/科研/共病分析/课题设计阶段/manuscript_Frontiers_Methods_v2_humanized.md`（296 行，55,953 字符，≈13,988 tokens）
> **⚠️ 本包的文件名不叫 `review_packet.md`**（中文名 `审稿应答_review_packet.md`），提示词里用的是绝对路径，勿改名。

---

## 0. 怎么用（先读这一节）

### 模式 A —— 模型有文件读取工具（同会话 / 同机器）
只给它**本文件的绝对路径** + 第 2 节提示词。**不要粘贴正文**：它继承工作区，按需读。
成本 ≈ 1k 指令 + 按需读 30–50% 稿件。

### 模式 B —— 外部模型（网页版，无文件能力）
把本文件**整包粘贴**。本包已自包含：22 条审稿意见逐字、稿件骨架（含行号）、关键数值卡、作者初判。
不需再粘正文即可完成第 1 轮。

### 模式 C —— 不想让它碰稿件（最省）
只投本包。第 1 轮的全部产出（分级处置表 + 两张清单）只依赖包内信息。

### 铁律
**第 1 轮禁止读稿件正文。** 先要计划 / 先出处置表 → 作者挑行区间 → 第 2 轮只读那些区间。
理由：正文 ≈13,988 tokens，一轮全读会把本包省下来的全花光，且读得越多越容易"重写一遍"而不是"给方案"。

---

## 1. 投喂清单与 token 预算

| 文件 | 体积 | ≈tokens | 第 1 轮 | 第 2 轮 | 备注 |
|---|---|---|---|---|---|
| `reviews/审稿应答_review_packet.md`（本文件） | 31.8 KB | — | **必读** | 复用 | 含 22 条意见逐字 + 作者初判 + 数值卡 |
| `课题设计阶段/manuscript_Frontiers_Methods_v2_humanized.md` | 54.9 KB | ≈13,988 | **禁读** | 仅读指定行区间 | `.md` 源，勿投 `.docx` |
| `reviews/作者初判_审稿意见分析.md` | 6.7 KB | — | 不必（已内联为 §6.3） | — | 单独投喂＝重复付费 |
| `审稿人意见.docx` | 9.2 KB | — | **禁投** | — | 已逐字内联为 §6.1–6.2；docx 解析慢且带 XML 噪声 |
| `课题设计阶段/Supplementary_final/S8_twelve_case_validation.csv` | 小 | — | 不必（已渲染为 §5 表 C） | 需要时 | 12 例逐门分值 |
| `课题设计阶段/Supplementary_final/S9_simulation_operating*.csv` | 中 | ≈2k | 不必 | 按需 | 模拟全表（Table 2 是它的边际汇总） |
| 图件（Fig1–5 的 PNG/SVG/TIFF） | 1–2k/张 | — | **禁投** | 需要时单张 | 判图先读图注（L210–L221） |
| `References` 段（L165–L209） | ≈1.5k | — | **禁投** | 按需 | 评审价值最低的一段 |

**三条规矩**：一次交付胜过多次小交付 ｜ 只投 `.md` ｜ 数值从 CSV 来，不靠图片。

---

## 2. 提示词

- **第 1 轮**（锁定形态）：`reviews/审稿应答_prompt_round1.md` —— 直接复制粘贴发送。
- **第 2 轮**：`reviews/审稿应答_prompt_round2.md` —— 把第 1 轮返回的行区间填进 `{{RANGES}}` 再发。

> **对 skill 模板 C 的有意偏离**（记录下来，避免下次被"修正"回去）：
> 模板 C 第 1 轮只输出两张清单。本包**额外增加一张 22 行的分级处置表**放在最前，
> 因为本次任务本质是"分配改稿工作量"，属于 skill 中"混合模式（方向咨询 + 稿件评审）"的许可形态。
> **模板 C 的核心纪律一字未改**：只读本包、禁止点名正文、读完即停、等作者确认。

---

## 3. 硬红线（违反任一条即返工）

1. **数字只引用，不重算、不改写。** 一切统计量以 §5 数值卡为准；发现疑似不一致，标 `to verify` 并指出位置，**不得自行改数**。
2. **不得把"证据不足"写成"证据反对"。** 功效不足（24% / <6%）的零结果只能表述为"未能检出"，不能表述为"已排除"——这正是 R1#5 的核心指控。
3. **缺数据就写缺数据。** 个体级 UKB 数据、大样本东亚失眠 GWAS、LIVE OpenGWAS 拉取在本项目中**不可得**（出口封锁 + 样本量不足）。不得建议"补做"这类分析，也不得用占位数字充数；只能建议在 Limitations 中强化披露。
4. **禁引 PhenoScanner。** 工具已停服且本机出口封锁。IV 多效性 / 变异注释只能走 GWAS Catalog、VEP，或 MR 自身诊断（Egger / LOO / Steiger / Cochran Q）。
5. **不跨 estimand 排名。** 未 clump IVW 与 clump 后 IVW 不是同一估计目标；MVMR 直接效应与 UVMR 总效应该分开陈述，不能并列排序或互相"佐证"。
6. **禁用词**：novel / first / best / optimal / solution / breakthrough / "首个" / "最优"。不得声称框架"解决了"MR 的可信性问题——只能说"提供一种可量化的分诊程序"。
7. **固定术语，不得替换**：`six-gate falsification framework`、门名 `G1–G6`、`Grade A–D`、`locus-driven confounding`、`shared liability`。不得改成 pipeline / score / tool / shared confounding。
8. **不虚构作者决定。** 利益冲突、基金、作者贡献、AI 使用声明只能指向投稿系统表单，不得代拟。
9. **不得建议删除对冲措辞**（`bounded by` / `cannot be ruled out` / `should be interpreted with caution` / Limitations 各条）。它们承载统计诚实性，不是冗余。
10. **已投稿版本不动。** 所有建议必须落成"改哪一节、怎么改"，由作者决定是否动稿；不得直接产出"修改后的全文"。

---

## 4. 稿件骨架（行号由脚本从磁盘实时计算）

> 行号对应 `C:/D/workbuddy/科研/共病分析/课题设计阶段/manuscript_Frontiers_Methods_v2_humanized.md`（296 行）。**任何编辑都会使行号失效**——改稿后须重跑 `reviews/make_review_packet.py`。

| 章节 | 行区间 | 一句话内容 |
|---|---|---|
| A six-gate falsification framework for correcting locus-driven confounding in Mendelian randomization: architecture, 43,200-simulation validation, and application to complex traits | L1–L10 | 标题行 + 作者 + 单位 + 通讯（行 1–9） |
| Abstract | L11–L18 | 背景 → 六门 → 43,200 模拟操作特征 → 失眠-AD 判 Grade C；约 305 词 |
| Introduction | L19–L29 | MR 三假设失效路径；locus-driven confounding 的四种畸变；框架定位（与 STROBE-MR 互补） |
| Materials and Equipment | L30–L52 | 软件与版本清单（`ieugwasr` v1.1.0 + 1000G **EUR** 面板）、输入要求、数据 accession（Table 3） |
| Methods | L53–L54 | 方法总纲 |
| Objectives and validation of the method | L55–L58 | 两部分验证：模拟（已知真值）+ 实证（失眠-AD 边界案例）；阈值预注册且固定 |
| The six gates | L59–L74 | G1–G6 逐门定义与计分。**R1#1/#4、R3#4/#6/#8 的主战场** |
| Grading rubric | L75–L78 | 0–12 → A(10–12)/B(7–9)/C(4–6)/D(0–3)；双人评分 72 items，Cohen's κ |
| Step-by-step execution protocol | L79–L90 | 7 步 + 5 个 pause point + 工时估计（含 CAUSE MCMC） |
| Simulation-based validation: design and data-generating process | L91–L95 | 网格 3 效应量 × 3 LD 浓度 × 3 多效性 × 2 overlap × 2 工具数 × 400 = 43,200；DGP 仅一段**定性**描述。**R1#2 的核心地带** |
| Results | L96–L97 | 结果总纲 |
| Operating characteristics of the framework (43,200-simulation benchmark) | L98–L103 | Table 2 数值；Grade A 频率 0→0.88；FDR 0.20 决策阈；单调校准 |
| Example of application: the insomnia–AD proof-of-concept | L104–L121 | G1–G6 逐门实证 + 工具数链条 2,462→54→44→38→33 + 功效 24%。**R1#5/#6/#7、R3#11 的主战场** |
| Precision, limits of detection, pitfalls, and troubleshooting | L122–L130 | 检测下限（OR ≥ 1.25/SD）与 5 条排障（Table 5） |
| Discussion | L131–L146 | APOE 模式普适性；与 STROBE-MR 互补；药物靶点转化；Limitations 六条；结论 |
| Declarations | L147–L164 | 数据/伦理/贡献/基金/COI/AI 使用声明 |
| References | L165–L209 | 42 条，全含 DOI（投喂时应丢弃） |
| Figure legends | L210–L221 | Fig1 框架 a/b；Fig2 43,200 操作特征；Fig3 案例 MR + coloc 不对称；Fig4 APOE 共享负债；Fig5 12 例分级 + 跨祖先 |
| Tables | L222–L296 | Table 1 门判定矩阵；Table 2 模拟操作特征；Table 3 数据清单；Table 4 执行步骤；Table 5 排障 |

---

## 5. 关键数值卡

> 这些数字是本次应答的载荷事实。**引用可以，重算禁止**。

### 表 A — 模拟操作特征（43,200 replicates，seed 20260804）

网格：效应量 β ∈ {0, 0.08, 0.15} × LD 浓度 {5, 12, 40 blocks} × 多效性 {none, balanced, directional} × 样本重叠 {0%, 30%} × 工具数 {20, 60} × 400 reps = **43,200**。平均每变异 F ≈ 36。

| 多效性 | β | 敏感度（Grade A/B） | 特异度（Grade D） | P(Grade A) | 经验 FDR |
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

要点：`β=0.08` 时敏感度仅 ≈0.5（**中-小效应检不出**）；FDR 全部低于 0.20 决策阈；null + 无多效时 100% Grade D、0% Grade A。

### 表 B — 失眠-AD 证据链（Grade C）

| 门 | 结果 | 值 |
|---|---|---|
| G1 未 clump | 正向、伪精确 | β=+0.104（SE 0.031，P=9.3×10⁻⁴），**2,462** 个工具 |
| G2 clump 后 | 翻转为 null | **54** 个工具，β=−0.130（SE 0.203，P=0.52）；**95%CI ≈ [−0.528, 0.268]** |
| G2 替代窗口 | 一致 | 5,000 kb → 37 工具，β=−0.111，P=0.64 |
| G2 MRlap | 仍 null | β=−0.078，P=0.43 |
| G2 CAUSE | **唯一分歧** | 前向 Kunkle P=0.039；Bellenguez P=0.002（但该数据源 Cochran Q P=1.7×10⁻¹¹，不可靠）；反向 P=0.08 / 0.63 |
| 工具数链条 | 已披露 | 2,462 →（clump）54 →（1 Mb 窗口）44 →（去 6 个混杂相关变异）38 →（harmonize）33 |
| 功效 | 关键限制 | R²=0.0022，mean F=44.3，min F=29.8；对 β=0.10 的功效**仅 24%**；80% 功效需 β ≥ 0.226（OR ≥ 1.25/SD）；AD 样本 n=63,926 |
| 19 号染色体 | 非 APOE 特异 | 剔除 **118** 个 chr19 工具后仍未 clump 显著：β=0.094，P=0.003 |
| G3 LDSC | rg≈0 | r_g=−0.028（SE 0.050，P=0.57）；去 chr19 后 −0.031（P=0.53） |
| G3 coloc | 反向为主 | 反向 **18/32**（APOE 区 PP.H4 > 0.98）vs 前向 **1/47** |
| G4 MVMR | 教育保护 / 失眠直接效应为负 | 教育 β=−1.29，P=0.008；失眠 β=−0.57，P=0.045（**方向与原始主张相反**，且该模型功效低） |
| G4 PheWAS | 教育 | AD −0.33（P=1.1×10⁻⁵）；PD −0.39（P=7.2×10⁻⁶）；MS +0.015（P=0.90） |
| G5 蛋白中介 | 全 null | CRP/IL-6 overall FDR=0.91；36 靶向 → **25 可评估**，FDR<0.05 命中 **0** |
| G5 代谢中介 | 教育保护部分由 TG 中介 | indirect β=−0.031（SE 0.008，q=5.7×10⁻⁴），占总效应 **9%** |
| G6 跨祖先 | 仅方向筛选 | 东亚 insomnia→AD β=−0.84，P=0.28（**power <6%**，**40** 个 EUR 独立工具，计 0 分）；EAS 教育→T2D β=−0.145，P=0.012；T2D→AD +0.006，P=0.93 |
| Steiger | 无法定方向 | 方向随 r 构建方式翻转，中位 \|r\|≈0.002 → 未计分 |

### 表 C — 12 例验证队列逐门分值（来自 `S8_twelve_case_validation.csv`，12 例）

| Case | L1 | L2 | L3 | L4 | L5 | L6 | Score | Grade | 备注 |
|---|---|---|---|---|---|---|---|---|---|
| LDL→CAD | 2 | 2 | 2 | 2 | 2 | 2 | 12 | A | Textbook positive; statin RCT + MR concordance |
| Education→AD | 2 | 2 | 2 | 2 | 2 | 2 | 12 | A | TG mediation q=5.7e-04; EA consistency |
| BMI→T2D | 2 | 2 | 2 | 2 | 2 | 2 | 12 | A | Classic obesity→diabetes |
| Height→CAD | 2 | 2 | 2 | 1 | 1 | 2 | 10 | A | Genuine protective; framework correctly accepts |
| Insomnia→AD | 2 | 0 | 1 | 1 | 0 | 0 | 4 | C | LD false positive; reclassified |
| BMI→Stroke | 2 | 1 | 1 | 1 | 0 | 0 | 5 | C | IVW sig but WM null; pleiotropy |
| HDL→CAD | 2 | 1 | 1 | 1 | 0 | 1 | 6 | C | IVW sig but Egger null; MR corrective |
| CRP→CAD | 1 | 0 | 0 | 0 | 0 | 0 | 1 | D | Clean null at extreme power F=176 |
| BMI→AD | 1 | 0 | 0 | 0 | 0 | 0 | 1 | D | Contested; framework correctly rejects |
| Education→T2D | 2 | 1 | 2 | 1 | 1 | 2 | 9 | B | Strong protective; Egger int p=0.036 + high hetero -> B; EAS rep IVW -0.145 (p=0.012) |
| Depression→AD | 2 | 1 | 1 | 1 | 0 | 0 | 5 | C | Protective borderline; WM p=0.059 not sig -> robustness partial |
| T2D→AD | 1 | 0 | 0 | 0 | 0 | 0 | 1 | D | Clean null at high power F=78; contested -> correctly rejected |

> **注意**：本表列头为 `L1–L6`（S8 原样），正文用 `G1–G6`；且表中**出现 1 分**，而 Table 1 脚注写"仅 0 或 2 分"。
> 两处均已在 §6.3 的 K1/K2 登记为待裁定事项——**不要当作新发现重复报告**。

### 表 D — 稿件规格

| 项 | 值 |
|---|---|
| 正文字数（Abstract → References 之前） | 4,520 words |
| 全文字数（含参考文献/图注/表格） | 6,628 words |
| Frontiers Methods (A-type) 上限 | 12,000 words → **余量充裕，不必"以删换增"** |
| Display items | 5 图 + 5 表 = 10（上限 15） |
| 参考文献 | 42 条，全含 DOI |
| 补充材料 | S1–S9 + Note 1–2 + STROBE-MR 清单 |

---

## 6. 审稿意见（逐字）与作者初判

### 6.1–6.2 审稿意见原文

> 以下为 `审稿人意见.docx` 的**逐字**文本，仅做编号切分，未改一字。
> **Reviewer 2 缺失**——docx 内只有 Reviewer 1（2026-10-22）与 Reviewer 3（2026-10-23），编号不连续。
> 也**没有 Editor 决定信**；唯一的总评是 R1 末句 "I recommend major revision"。

#### Reviewer 1 —— 逐字原文（10 条）


**R1#1**

> The scoring rules differ across the text, Table 1, Figure 1 and Table S8: some allow only 0 or 2 points, while others also use 1 point. The education-T2D score of 9 therefore needs explanation. Also, failure at G2 could still produce Grade A under the additive rule. Please provide one consistent scoring table covering partial scores, decisive failures, conflicting results and unavailable or underpowered analyses.


**R1#2**

> The simulation script in the cited Zenodo archive differs from the described workflow. G3 uses block coverage and G4 uses leave-one-out variation instead of LDSC/colocalization and MVMR; CAUSE/MRlap and the G6 power check are absent. The code also does not generate the described LD covariance or correlated exposure-outcome errors, and adds outcome noise with SD 0.01 while supplying SE 0.03. Mediator values depend on the true effect but do not generate the outcome. Please confirm the code version used and describe the actual simulation procedure in the Methods, explaining these differences. If they affect the performance results, please update those results.


**R1#3**

> What does the full framework add beyond routine LD handling and robustness checks? Please compare correctly LD-adjusted IVW, a conventional MR workflow with specified robustness analyses, and the complete six-gate framework on the same simulated datasets. State the rules for each approach and compare both false positives and missed true effects. Adding gates sequentially or removing one at a time would also help show the contribution of each gate.


**R1#4**

> Sensitivity treats A/B as positive, but specificity counts only D as a correct negative. How is Grade C handled? If A/B is positive and C/D is negative, specificity should include both C and D. Please use consistent definitions for sensitivity, specificity, false-positive rate and FDR, and report their uncertainty. Also explain the 0.20 threshold in the Results and how the simulated mix of true and null effects affects FDR.


**R1#5**

> The clumped insomnia-AD estimate has an approximate 95% confidence interval of -0.528 to 0.268, which includes the positive effect of 0.10 discussed in the paper. Power to detect that effect is only 24%, and the East Asian analysis has less than 6% power. These findings do not exclude a smaller causal effect. Please distinguish insufficient evidence from evidence against a claim.


**R1#6**

> On PDF p. 12, the authors use removal of 118 chromosome-19 instruments to assess the influence of APOE. Please explicitly state that APOE lies on chromosome 19, so this exclusion removes instruments in the APOE region as well as elsewhere on that chromosome; it is not an APOE-specific exclusion. The remaining unclumped IVW association (β = 0.094, P = 0.003) shows that the nominal signal persists without chromosome-19 instruments, but does not by itself establish the contribution of APOE or explain the attenuation after LD clumping. Please clarify this limitation. If attributing the MR result to APOE, define the region and compare results with and without it using the same LD-handling settings. Explain how this evidence and colocalization support Grade C. Also clarify how the 32 reverse and 47 forward regions were selected and whether they overlap; colocalization alone does not establish causal direction.


**R1#7**

> On PDF p. 12, the paper groups the analyses as "three null results (clumped IVW, MRlap, and the MVMR direct effect below)." However, p. 13 states: "The direct effect of insomnia was negative (β = -0.57, P = 0.045), opposite in direction to the original claim that insomnia elevates AD risk." This estimate is nominally significant and points in the opposite direction, so calling all three results null is inconsistent. Please use wording such as "none of the three analyses supported the original positive causal hypothesis" and describe nonsignificant and opposite-direction results separately. Also explain why the forward CAUSE results (P = 0.039 and 0.002) are called borderline and how the disagreement affects scoring. Clarify the CAUSE/MRlap inputs and main settings, the reference to extending an MCMC chain, and any effect-unit conversions.


**R1#8**

> The total effect and the effect remaining after adjustment answer different questions. Report conditional instrument strength and how correlated estimates and SNPs were handled. For mediation, clarify the 36-versus-25 protein counts, both path estimates, multiple-testing correction and the calculation of 9% triglyceride mediation. Finding no mediator among the 25 proteins analysed does not rule out mediation through other proteins or pathways.


**R1#9**

> Please identify the evidence behind the external-validation scores. The text reports East Asian education-T2D results, while S8 gives education-AD full validation points. A fully worked Grade A example would help explain the framework. For all 12 cases, clarify the reference labels and supporting gate results; Cohen's κ measures rater agreement, not causal accuracy.


**R1#10**

> The proposed use in drug-target development is interesting. Please explain how the framework could move from assessing risk factors to assessing specific genes or proteins. For example, evidence for LDL causing coronary disease does not identify the protein a drug should target. A short discussion of target-specific genetic evidence, relevant tissues, inhibition versus activation, safety and druggability would be helpful. Present prediction of drug-development success as a possible application requiring further validation.


#### Reviewer 3 —— 逐字原文（12 条）


**R3#1**

> In the Abstract, I suggest the authors clarify and harmonize the terminology used for directional/causal claims (e.g., "causal claims", "positive association", "an inverse association", etc.) to ensure consistent messaging.


**R3#2**

> In the Abstract, the authors state that "standard MR pipelines often yield precise, statistically significant estimates that do not reflect directed causal effects." Could the authors clarify what is meant by "precise" in this context?


**R3#3**

> In the Materials and Equipment section, the authors specify using "ieugwasr v1.1.0: LD clumping against the 1000 Genomes European reference" while also mentioning "East Asian AD...". When analyzing the East Asian AD dataset, did the authors use the European reference panel for LD clumping? If so, please address whether this mismatch introduces linkage disequilibrium mismatch or bias.


**R3#4**

> Regarding Gate G2 (robustness), what was the rationale for adopting such an unusually stringent clumping threshold (r2 < 0.001) paired with a very large 10,000-kb window? These parameters deviate significantly from common practice in the field.


**R3#5**

> To ensure I understand correctly: does the analytical pipeline take the variables that survive these three distinct corrections, input them into clumped IVW, and then test whether the causal effect retains statistical significance? Please clarify this step in the text.


**R3#6**

> Could the authors explain how confounders were selected for inclusion in the Multivariable MR? Additionally, why was the requirement for an F-statistic > 10 evaluated at Gate G4 rather than being established at Gate G1 or Gate G2 during initial instrument selection, because the F-statistic to some extent is correlated with the significance level (p-value)?


**R3#7**

> For Gate G6, the text states that "Directional consistency is evaluated in an independent ancestry cohort." Is the statistical power comparable between these ancestry cohorts? Furthermore, given that biological mechanisms or causal architecture may differ across population ancestries, please discuss potential bias introduced by cross-ancestry evaluation.


**R3#8**

> Could the authors provide more explicit details on how MR-Egger, Cochran's Q test, MRlap correction, and CAUSE fit into this overarching framework? Were these methods applied to filter/select instrumental variables or used purely as post-estimation sensitivity checks?


**R3#9**

> In the simulation framework, how were specific parameter numbers chosen? For example, what guided the choice of 20 and 60 as instrument counts? Additionally, given a mean F-statistic around 36, the tested causal effect sizes (0, 0.08, and 0.15) seem relatively low; please provide justification for these parameter choices.


**R3#10**

> Could the authors clarify what is meant by "trans-ethnic re-clumping" and outline the specific algorithmic steps involved?


**R3#11**

> The description of Gate G3 requires modification for technical accuracy. While a non-significant result indicates no significant genetic correlation, the authors should refrain from asserting that the relationship "remained unchanged after excluding chromosome 19." Please revise this statement accordingly.


**R3#12**

> Please format all tables according to standard scientific formatting rules (e.g., standard three-line tables without vertical rules).


---

### 6.3 作者初判：重叠与优先级


> 本文档是**作者方（本机 AI 助手）**在 2026-10-27 对 `审稿人意见.docx` 的初步拆解，
> 供外部模型接手时作为「已知项」——**请勿把这些当作你自己的新发现重复输出**。
> 你可以**反驳**其中任一判断，但需给出理由。

---

#### A. 意见总量与定性

| 项 | 结论 |
|---|---|
| 意见总量 | **22 条**（Reviewer 1 十条 + Reviewer 3 十二条） |
| Reviewer 2 | **缺失**。docx 内只有 Reviewer 1（2026-10-22）与 Reviewer 3（2026-10-23），编号不连续 |
| Editor 决定信 | 包内无。仅有 R1 总评末句 "I recommend major revision" |
| R1 画像 | 方法学审计型。聚焦**评分体系自洽性、模拟代码与描述一致性、框架增量价值、统计定义、因果解释口径** |
| R3 画像 | 透明性与技术准确性型。多为 *please clarify*，聚焦**术语统一、参数依据、流程叙述、跨祖先偏倚、表格格式** |

---

#### B. 重叠矩阵（7 个共同主题簇，覆盖 **18 条**意见）

| 簇 | 主题 | Reviewer 1 | Reviewer 3 | 强度 |
|---|---|---|---|---|
| ① | **G2 clumping 参数 → IV 剩多少 → 功效 → 「证据不足 vs 证据反对」** | #4、#5、#6 | #4 | 🔴 强（同一因果链被两人从两端夹住） |
| ② | **LD 参考面板与 LD 处理正确性** | #3、#6 | #3、#4、#10 | 🔴 强 |
| ③ | **19 号染色体 / APOE / 遗传相关的表述** | #6 | #11 | 🔴 强（几乎同一句话） |
| ④ | **G6 跨祖先：功效可比性与解释** | #5 | #3、#7 | 🟡 中 |
| ⑤ | **各方法在流程中的定位与叙述** | #7、#8 | #5、#6、#8 | 🟡 中 |
| ⑥ | **断言强度与措辞一致性** | #5、#7、#10 | #1、#11 | 🟡 中 |
| ⑦ | **模拟设计与参数依据** | #2、#3 | #9 | 🟡 中（R3 要依据、R1 要重跑，动作可合并） |

**统计口径**（22 = 18 重叠 + 4 独有）

- 参与重叠：R1 的 #2/#3/#4/#5/#6/#7/#8/#10（8 条）+ R3 的 #1/#3/#4/#5/#6/#7/#8/#9/#10/#11（10 条）。
- **完全独有 4 条**：
  - **R1#1** 统一评分表（含"G2 失败仍可 A 级"的逻辑漏洞）—— 与簇⑤⑥ 相邻但不属于其中任何一簇，它是评分制式本身的问题；
  - **R1#9** 外部验证分数的证据来源 + κ 被当作因果准确性；
  - **R3#2** Abstract 中 "precise" 一词的所指；
  - **R3#12** 三线表格式。
- ⚠️ 上一轮口头汇报曾称"独有 10 条""重叠覆盖 12 条"——**该计数有误**，以本表为准。错因：把已归入簇⑤⑥⑦的条目同时计成了独有。


---

#### C. 优先级分组（P0 立论级 / P1 需定量回应 / P2 澄清格式）

| 级别 | 条目 | 数量 | 判据 |
|---|---|---|---|
| **P0** | R1#1、R1#2、R1#3、R1#4 | 4 | 靠改写文字**无法**回应，必须补分析、重跑或改评分体系；不解决则框架立论不成立 |
| **P1** | R1#5、R1#6、R1#7、R1#8、R1#9、R3#3、R3#4、R3#6、R3#7、R3#9 | 10 | 需要一个具体数字、一张补充表或一段方法学论证才能结案 |
| **P2** | R1#10、R3#1、R3#2、R3#5、R3#8、R3#10、R3#11、R3#12 | 8 | 澄清、统一术语、补一句流程说明、改表格样式，可批量处理 |

---

#### D. 作者方的三条判断（允许反驳）

1. **R1#2 是本次最危险的一条**，且性质不是"解释不清"而是**可复现性**：审稿人已逐项点名 Zenodo 归档代码与 Methods 描述的四类偏差（G3/G4 实现替代、CAUSE/MRlap 与 G6 功效检查缺失、未生成所述 LD 协方差与相关误差、结局噪声 SD 0.01 配 SE 0.03、中介变量不生成结局）。任何"已在 Methods 说明"式回应都不成立，必须**核对代码版本并给出实际 DGP**。
2. **簇①+②+③ 是同一根链条，必须打包回应**：LD 面板 → clump 参数（r²<0.001、10 Mb）→ IV 只剩 54 个 → 功效 24% → CI [−0.528, 0.268] 含 +0.10 → 无法排除小效应 → 却把结论写成 Grade C 的否定性判定。两位审稿人不约而同落在这一点，说明这是全稿最脆弱的解释链。
3. **R3#4 不能只答"更保守"**。clump 阈值远超领域常规，需给出**可验证的依据**（如：与 APOE 位点 LD 跨度匹配、与替代阈值下的结果一致性），否则等于承认参数是任选的。

---

#### E. 作者自查新增的 4 处内部不一致（审稿人**未**提出，但请勿当作新发现重复报告）

> 以下由本机对稿件与 `Supplementary_final/S8_twelve_case_validation.csv` 的交叉核对得出，
> 已登记为"待作者裁定"，**不属于外部模型的新发现**。若要讨论，请围绕"如何修正"而非"是否存在"。

| 编号 | 现象 | 证据位置 |
|---|---|---|
| K1 | **评分制式自相矛盾**：Table 1 脚注写 "All gates … contribute 0 or 2 points (maximum 12)"，但 S8 实际使用 1 分（Education→T2D = 2,1,2,1,1,2 = 9；Height→CAD 含两个 1；CRP→CAD 的 L1=1）。这正是 R1#1 追问 9 分的来源 | 正文 L235 vs `S8_twelve_case_validation.csv` |
| K2 | **门名不一致**：S8 列头为 `L1–L6`，正文与 Table 1 用 `G1–G6` | 同上 |
| K3 | **12 例叙述覆盖不全**：正文 L118 仅点名 4 例（LDL–CAD、Education–AD 为 A；Education–T2D、Insomnia–AD 为 B/C；BMI–AD、T2D–AD 为 D），遗漏 BMI–T2D（12/A）、Height–CAD（10/A）、BMI–Stroke（5/C）、HDL–CAD（6/C）、Depression–AD（5/C）、CRP–CAD（1/D） | 正文 L118 vs S8 |
| K4 | **S8 中若干 G6 计分 2 分缺乏可核查的跨祖先前置**（如 BMI–T2D 的 L6=2、Education–AD 的 L6=2），与正文 L118 只报告 education→T2D 与 insomnia→AD 的跨祖先结果不匹配 → **待核**，非定论 | 同上 |

---

#### F. 内部已知软肋（已披露 / 不可补数据，勿建议"补做"）

1. **G4 多状态时序**缺 UKB 个体级长表 → 未执行，Limitations 已披露。
2. **失眠→AD 东亚复制**缺大样本 EAS 失眠 GWAS（GCST90018649 仅 389 例）→ 降级为方向性筛选，Note 1 已写明不可行。
3. **Steiger 方向检验**无法定方向（推断方向随 r 构建方式翻转，中位 |r| ≈ 0.002）→ 未计分，已披露。
4. **54 vs 40 工具数差异**（LD 参考面板更新所致）→ 正文 L110 已主动披露。
5. **Grade 阈值（10–12/7–9/4–6/0–3）为预设但任意** → Limitations 已披露，并列出 2 例贴边界。
6. **36 靶向蛋白 → 25 可评估**（11 个仪器不足被排除）→ 正文 L116、Table 3 已披露。
7. **主案例仅对中-大效应有 80% 功效**（OR ≥ 1.25/SD）→ 正文 L110、L124、Limitations 已三处披露。

> 对上述 7 条，**不要**建议"补充个体级数据""换更大 EAS 样本""改用 Steiger 定性"——本机出口封锁与大样本可得性已排除这些路径（见 §硬红线 3）。


---

### 6.4 本包**不含**什么（诚实标注）

| 未包含 | 后果 |
|---|---|
| 稿件 `.docx` 与 PDF 版式（只有 `.md` 源） | 无法判断"PDF p. 12"这类**页码定位**；行号以 `.md` 为准，需自行换算 |
| 图件 Fig1–5 的实际像素内容 | 无法核实 R1#1 所说"Figure 1 的评分规则"具体如何画、R1#9 的图注对应关系 |
| `S1–S9` 全表、`Note 1–2`、STROBE-MR 清单 | 无法核实 S 表编号是否与正文引用一致（如 R1#8 的 36 vs 25、R1#9 的 S8 标签） |
| Zenodo 归档代码（DOI 10.5281/zenodo.21858125）与 GitHub 仓库 | **无法独立核对 R1#2**（代码与 Methods 描述不一致）。该条只能由作者方自查后转述，或明确标 `to verify` |
| Editor 决定信 / 审稿人评分卡 | 无法判断本轮是 major revision 还是 reject-and-resubmit |
| 前 5 次 desk reject 的编辑原话 | 与本轮无关，但影响"是否值得继续投综合刊"的判断 |

---

## 7. 深读索引

| 想看什么 | 读什么 |
|---|---|
| Abstract 全文 | `C:/D/workbuddy/科研/共病分析/课题设计阶段/manuscript_Frontiers_Methods_v2_humanized.md` L11–L18 |
| 六门定义（R1#1/#4、R3#4/#6/#8 主战场） | 同文件 L59–L74 |
| 评分 rubric（Grade C 归类争议） | 同文件 L75–L78 |
| 模拟 DGP 描述（R1#2 核心） | 同文件 L91–L95 |
| 模拟结果叙述 + 0.20 阈值 | 同文件 L98–L103 |
| 失眠-AD 逐门实证（R1#5/#6/#7、R3#11 主战场） | 同文件 L104–L121 |
| 检测下限与排障 | 同文件 L122–L130 |
| Limitations 六条（勿建议删除） | 同文件 L143 |
| 图注 | 同文件 L210–L221 |
| Table 1 门判定矩阵 | 同文件 L226–L235 |
| Table 2 模拟操作特征 | 同文件 L239–L251 |
| 12 例逐门分值 | `课题设计阶段/Supplementary_final/S8_twelve_case_validation.csv` |
| 模拟全表 | `课题设计阶段/Supplementary_final/S9_simulation_operating.csv` |
| 项目规则 | `RULES.md` |
| 本包生成脚本（改稿后重跑） | `reviews/make_review_packet.py` |

---

*本包含索引、骨架、数值卡与 22 条意见逐字；正文按需按行区间投喂，勿在第一轮整体读取。*
