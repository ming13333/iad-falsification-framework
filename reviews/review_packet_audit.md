# review_packet_audit.md — 修订答复第三方复核投喂包

> **用途**：交给一个**有文件读取工具**的模型，复核本次 Frontiers 大修的答复是否站得住。
> **不是**改写任务：不要重写回信、不要润色正文、不要提新的论证思路。
> **生成**：`code/make_review_packet.py` 从磁盘实时渲染，行区间与字数每次重算。改动任一方后请重跑。
> **版本**：audit-2026-10-30 ｜ 回信 333 行 / 8,670 词（≈12k tok）｜ 正文 307 行 / 11,172 词（≈15k tok）

---

## 0. 怎么用（先读这一节）

**模式 A（本包假定）**：模型能读本地文件。**不要粘贴正文**，给路径 + 提示词即可。

**铁律**：第 1 轮只读本包一个文件，读完即停。模型先给出「必须看原文才能核的条目」，
由作者确认行区间后，第 2 轮才定向读。第 1 轮就去读回信或正文 = 白烧预算。

**为什么第 2 轮允许整份读回信**：回信是审计对象本身，22 条必须逐条核，抽样等于放弃任务。
这是对「不要整篇读」规则的**有意例外**；正文仍按行区间切。

**为什么本包比常规投喂包厚**：常规包为「提修改意见」而建，只需骨架 + 数字卡。
本包为「核账」而建，必须携带 §7 的已知未决项与 §9 的判定口径，否则外审会把已声明的东西当新发现，
或把主动降级当成需要「修正」的错误。

---

## 1. 投喂清单与预算

| 文件（相对工作区根） | 体量 | 估 token | 第 1 轮 | 第 2 轮 |
|---|---|---|---|---|
| `reviews/review_packet_audit.md`（本包） | 19.5 KB | ≈6k | **只读这个** | 不再读 |
| `reviews/Response_to_Reviewers_Frontiers.md` | 58 KB | ≈12k | 禁读 | **整份** |
| `课题设计阶段/manuscript_Frontiers_Methods_v2_humanized.md` | 84 KB | ≈15k | 禁读 | 按 §8 行区间 |
| `manuscript/supplementary/S8_twelve_case_validation.csv` | 2.6 KB | ≈2k | 禁读 | **必读** |
| `manuscript/supplementary/S9_simulation_operating_marginal.csv` / `S11` / `S12` | 7.7 KB | ≈3k | 禁读 | 按需 |
| `results/simulation/S14_table2_cap_audit.csv` | 0.6 KB | ≈0.5k | 禁读 | 按需 |
| `.docx` / 图 / references 段 | — | — | 不要 | 不要 |

**总成本**：第 1 轮 ≈6k，第 2 轮 ≈22k。**单次交付优于多轮**，不要分批发。

---

## 2. 提示词

- 第 1 轮：`reviews/handoff_prompt_round1.md`（路径已填，可直接拷）
- 第 2 轮：`reviews/handoff_prompt_round2.md`（含行区间占位，等第 1 轮回答后填）

---

## 3. 硬约束（违反任一条即返工）

1. **不得改动任何数值。** 有疑点写 `to verify`，不要自行算出「应该是多少」。
2. **不得把「我没找到」当成「作者写错了」。** 区分 `找到且一致` / `找到但不一致` / `档案中无此数`。
3. **不得把 §7 已声明的缺口当作新发现。** 逐条读过再说话。
4. **不得建议把已收紧的措辞放宽。** 本稿多处主动降级（六门→四信号、验证→基准、A→B、
   撤 G6 分），改回去是本轮最严重的错误。
5. **不得引入 `novel` / `first` / `best` / `optimal` / `solution`。**
6. **不得改标题。** 两处改动各有理由（见回信 R1-2）；`six-gate` 保留是因为框架本身是六门，
   被收窄的是基准覆盖的信号数，不是门的数量。
7. **不得重排投稿策略、选刊或作者信息。** 不在本轮范围。
8. **不评价「是否仍够格发表」。** 作者有意排除，见 §9 末。

---

## 4. 正文骨架

| 章节 | 行区间 | 一句话 |
|---|---|---|
| A six-gate falsification framework for diagnosing locus-driven confounding ... | L1-L10 | Title (revised: diagnosing / benchmark of its scoring rule) |
| Abstract | L11-L18 | Abstract; claim narrowed to the scoring rule |
| Introduction | L19-L29 | Framing: locus-driven confounding; why six gates |
| Materials and Equipment | L30-L52 | Data inventory and software |
| Methods | L53-L54 | Methods head |
| Objectives and validation of the method | L55-L60 | What the framework claims to validate |
| The six gates | L61-L80 | G1-G6 definitions |
| Grading rubric | L81-L84 | 0/1/2 tiers, binary gates, decisive-failure cap |
| Step-by-step execution protocol | L85-L96 | Seven-step protocol with pause points |
| Simulation-based validation: design and data-generating process | L97-L101 | Design and data-generating process - rewritten in revision |
| Results | L102-L103 | Results head |
| Operating characteristics of the scoring rule (43,200-simulation benchmark) | L104-L109 | Table 2 territory; post-cap numbers |
| Example of application: the insomnia–AD proof-of-concept | L110-L129 | The insomnia-AD case; Grade C |
| Precision, limits of detection, pitfalls, and troubleshooting | L130-L142 | LD correction, power, pitfalls |
| Discussion | L143-L158 | Includes drug-target translation paragraph |
| Declarations | L159-L176 | Ethics, data availability, competing interests |
| References | L177-L221 | Reference list (drop when feeding) |
| Figure legends | L222-L233 | Figure 1-5 legends |
| Tables | L234-L308 | Tables 1-5, including the two-layer gate specification |

---

## 5. 回信骨架（22 条，审计对象）

| 编号 | 行区间 | 主题 |
|---|---|---|
| Summary | L9-L18 | seven headline changes |
| Table R1 | L19-L49 | disposition table, 22 rows |
| Reviewer 1 | L50-L51 |  |
| R1-1 | L52-L69 | scoring rules, partial credit, decisive failures |
| R1-2 | L70-L85 | archived simulation code vs described workflow |
| R1-3 | L86-L99 | what the framework adds beyond routine LD handling |
| R1-4 | L100-L117 | operating-characteristic definitions, 0.20 threshold |
| R1-5 | L118-L129 | insufficient evidence is not evidence against |
| R1-6 | L130-L145 | chromosome 19 is not the APOE region |
| R1-7 | L146-L161 | three nulls vs a negative direct effect; CAUSE inputs |
| R1-8 | L162-L177 | conditional instrument strength; mediation details |
| R1-9 | L178-L193 | evidence behind the external-validation scores; kappa |
| R1-10 | L194-L205 | risk factors to drug targets |
| Reviewer 3 | L206-L207 |  |
| R3-1 | L208-L215 | terminology for directional and causal claims |
| R3-2 | L216-L223 | what 'precise' means |
| R3-3 | L224-L233 | European LD panel on East Asian data |
| R3-4 | L234-L245 | rationale for r2 < 0.001 with a 10,000-kb window |
| R3-5 | L246-L253 | do corrections feed into clumped IVW |
| R3-6 | L254-L263 | confounder choice; why F > 10 sits at G4 |
| R3-7 | L264-L271 | power comparability across ancestries |
| R3-8 | L272-L279 | where Egger, Q, MRlap and CAUSE sit |
| R3-9 | L280-L287 | choice of simulation parameter values |
| R3-10 | L288-L295 | what trans-ethnic re-clumping is |
| R3-11 | L296-L303 | do not say r_g 'remained unchanged' |
| R3-12 | L304-L313 | three-line tables without vertical rules |
| Note | L314-L334 | supplementary material inventory |

注意：`Summary`（L9–L18）与 `Table R1`（L19–L49）都在 R1-1 之前，是总览；
`Note`（L312–末）是补充材料清单。这三段不属于 22 条中的任何一条。

---

## 6. 关键数字卡

> 全部由脚本从归档 CSV 直读，未手工誊写。回信里的每个数字都应能在下面或 S8/S10/S11/S12 找到出处；
> 找不到 = `档案中无此数`，按硬约束 2 处理，不要判成错。

### 6.1 Table 2 — 操作特征（43,200 次重复，seed 20260804，**已施加决定性失败封顶**）

| 多效性 | 效应 β | 敏感度 A/B | 特异度 D-only | 特异度 C/D | P(A) |
|---|---|---|---|---|---|
| none | 0.0 | - | 1.000 (0.999-1.000) | 1.000 (0.999-1.000) | 0.000 |
| none | 0.08 | 0.216 (0.204-0.228) | - | - | 0.213 |
| none | 0.15 | 0.878 (0.869-0.887) | - | - | 0.875 |
| balanced | 0.0 | - | 0.796 (0.785-0.807) | 0.882 (0.873-0.891) | 0.061 |
| balanced | 0.08 | 0.376 (0.362-0.389) | - | - | 0.354 |
| balanced | 0.15 | 0.724 (0.711-0.736) | - | - | 0.717 |
| directional | 0.0 | - | 0.679 (0.666-0.692) | 0.809 (0.798-0.820) | 0.046 |
| directional | 0.08 | 0.408 (0.394-0.422) | - | - | 0.367 |
| directional | 0.15 | 0.691 (0.678-0.704) | - | - | 0.667 |

每行 = 12 个参数格等权均值，每格 400 次重复 × 3 个效应档；括号内为 4,800 次重复上的 95% Wilson 区间。

### 6.2 S8 — 十二案评分（v1 = 投稿版）

| 案例 | G1-G6 | 分数 | 等级 | 投稿版分数 | 投稿版等级 | Δ | 跨级? |
|---|---|---|---|---|---|---|---|
| LDL→CAD | 222220 | 10 | A | 12 | A | -2 |  |
| Education→AD | 222220 | 10 | A | 12 | A | -2 |  |
| BMI→T2D | 222220 | 10 | A | 12 | A | -2 |  |
| Height→CAD | 222110 | 8 | B | 10 | A | -2 | **yes** |
| Insomnia→AD | 201100 | 4 | C | 4 | C | 0 |  |
| BMI→Stroke | 211100 | 5 | C | 5 | C | 0 |  |
| HDL→CAD | 211100 | 5 | C | 6 | C | -1 |  |
| CRP→CAD | 000000 | 0 | D | 1 | D | -1 |  |
| BMI→AD | 000000 | 0 | D | 1 | D | -1 |  |
| Education→T2D | 212112 | 9 | B | 9 | B | 0 |  |
| Depression→AD | 211100 | 5 | C | 5 | C | 0 |  |
| T2D→AD | 000000 | 0 | D | 1 | D | -1 |  |

**Δ≠0 共 8 例，跨级 1 例（Height→CAD，A→B）。** 回信 Summary 第 6 条声称「every score that moved」
并称列全 8 例 —— 请逐一核对上表 Δ≠0 的行是否都在该条里被指名。

### 6.3 S11 — 三档工具（失眠→AD）

| 档位 | clumping | n IV | β | SE | SE 膨胀 | 方向 | G2 |
|---|---|---|---|---|---|---|---|
| Unclumped | None (genome-wide significant only) | 2462 | 0.104 | 0.031 | 1.00 | positive | Pass |
| Loose | r2 < 0.1, 10,000 kb | 54 | -0.130 | 0.203 | 6.50 | negative | Fail |
| Tight | r2 < 0.001, 10,000 kb | 37 | -0.111 | 0.236 | 7.54 | negative | Fail |

### 6.4 封顶前后（S14）

| regime | 指标 | 未封顶 | 已封顶 | Δ |
|---|---|---|---|---|
| none | spec_D | 1.0 | 1.0 | 0.0 |
| none | spec_CD | 1.0 | 1.0 | 0.0 |
| none | fdr | 0.0 | 0.0 | 0 |
| none | sens_015 | 0.9727 | 0.8781 | -0.0946 |
| none | sens_008 | 0.5062 | 0.2158 | -0.2904 |
| none | p_A | 0.3628 | 0.3628 | 0.0 |
| balanced | spec_D | 0.7963 | 0.7963 | 0.0 |
| balanced | spec_CD | 0.8821 | 0.8821 | 0.0 |
| balanced | fdr | 0.0828 | 0.1001 | 0.0173 |
| balanced | sens_015 | 0.8473 | 0.724 | -0.1233 |
| balanced | sens_008 | 0.5267 | 0.3756 | -0.1511 |
| balanced | p_A | 0.3772 | 0.3772 | 0.0 |
| directional | spec_D | 0.6794 | 0.6794 | 0.0 |
| directional | spec_CD | 0.8094 | 0.8094 | 0.0 |
| directional | fdr | 0.1275 | 0.1512 | 0.0237 |
| directional | sens_015 | 0.804 | 0.6915 | -0.1125 |
| directional | sens_008 | 0.545 | 0.4079 | -0.1371 |
| directional | p_A | 0.3601 | 0.3601 | 0.0 |

**特异度与 P(Grade A) 的 Δ 全为 0** —— 这是回信「特异度不变」的依据。

### 6.5 FDR 对真零比例的依赖

| 多效性 | π(null) | FDR | >0.20? |
|---|---|---|---|
| none | 0.3333 | 0.0 |  |
| none | 0.5 | 0.0 |  |
| none | 0.6667 | 0.0 |  |
| balanced | 0.3333 | 0.0969 |  |
| balanced | 0.5 | 0.1766 |  |
| balanced | 0.6667 | 0.3002 | **YES** |
| directional | 0.3333 | 0.1478 |  |
| directional | 0.5 | 0.2575 | **YES** |
| directional | 0.6667 | 0.4095 | **YES** |

> ⚠️ **两种口径并存，见 §7 第 11 条。** 本表用「4,800 次合并」口径（balanced/1-3 = **0.0969**）；
> Table 2 与 S14 用「12 格等权平均」口径（**0.1001**）。回信正文的 0.100 属后者，
> 重加权讨论里的 0.18/0.26 属前者。差额 0.003 来自加权方式，**不是算错**。

### 6.6 其它被引用的数

- 留一门消融（S10，72 行）：移除单门后改变等级的案例数 —— G1 7/12, G2 3/12, G3 4/12, G4 4/12, G5 3/12
- 敏感度重算：β=0.15 无多效性 **0.878**（投稿 0.973）；平衡 **0.724**（0.847）；方向性 **0.691**（0.804）
- 改判重复数：**4,363 / 43,200 = 10.1%**，全部 B→C，且全部为真实非零效应
- 阈值扰动：`A≥11` 三例 A→B；`C≥5` 主案 C→D（仍负）；**极性翻转 0 例**
- 220 种单调四段划分：主案极性保持 89.3%，三个 A 级案例 100%
- 教育→AD 东亚复制：β = −0.029，P = 0.85，实际效能 ≥84%
- 教育→TG β=−0.183（P=2.5e-22）；TG→AD β=+0.169（P=9.7e-6）；indirect −0.031（q=5.7e-4）；中介比 9.5%
- κ 复现性：11/12 等级，κ=0.89（95% CI 0.64–1.00），加权 κ=0.97，逐门 72 项 κ=0.91
- 归档 DOI `10.5281/zenodo.23733172`（v1.2.1）；旧 `10.5281/zenodo.21858125` 仅作历史叙述

---

## 7. 已知未决项（**先读这一节，再开口**）

> 以下各项作者已内部识别并在回信或正文中声明。**不要当作新发现重报。**
> 若你认为某项其实仍不成立、或不构成充分披露，请直接反驳并说明理由 —— 这是允许的。
> 但重复报告同一事实而不给新论据，属于浪费行数。

**1. 模拟无法回答 LD 校正问题**

基准独立抽取工具效应，数据中没有工具间 LD，三臂对比（校正/常规/六门）在那里是同一个估计量。回信 R1-3 已声明为部分接受，并改用 S10 消融与 S11 三档替代。**不要建议补做三臂模拟**——那等于替换模拟，不是修订。

**2. 条件 F 统计量从未提取**

归档的 MVIVW 拟合对象未提供条件 F 槽位，28 个模型行该列全为 NA；协调后的多变量输入矩阵未保留，上游 API 在本方环境不可达。已在方法学与局限中声明为**报告缺口**。不要建议「补算条件 F」。

**3. APOE 区域剔除后的对照未做**

审稿人建议「同 clumping 设置有/无 APOE 区域的对照」，但 clumped 集仅 54 个变异，剔除后不足以稳定估计。已如实说明未做，而非呈现一个效能不足的对比。

**4. 10,000 kb 无法从原理推导**

r²<0.001 + 10,000 kb 是 TwoSampleMR/IEU 默认值，作为最保守通行设置采用。已用三档证明结论不依赖它（最宽松档即已反转），但**不能**从第一原理论证 10,000 优于 5,000。两条都已报告。

**5. 跨族裔使用欧洲 LD 面板**

当时无东亚 LD 参考面板。已写明后果（残余 LD 低估 SE、频率差异移动点估计），且该步只读方向、在效能 <6% 时不计分。

**6. G3 由 G1 决定、G4 与 G2 99.1% 吻合**

基准中 G1>0 的重复 100% 得 G3=2；G4 与 G2 在 99.1% 的重复中一致。因此基准实际评估**四门信号**（G1/G2/G5/G6）到 0–12 的映射。已写入 Table 1 与 Table 2 脚注、方法学、回信 R1-2。

**7. 决定性失败封顶在本队列不 binding**

12 案中唯一 G2 失败者是失眠→AD，总分 4，封顶 6 不触发。S12.3 已明说：封顶位置来自「C 级上界」的定义，不是这些数据推出来的。

**8. `Supplementary_Tables.xlsx` 无三线边框**

三线表只在正文 docx 实现；工作簿由 CSV 生成，与归档 v1.2.1 逐字节一致。builder 有 `--rules` 开关，**默认关闭**以保持与已发布物一致。回信 R3-12 已如实描述。不要建议改默认值。

**9. 归档快照的 README 含 `<DOI-TODO>`**

DOI 在快照之后才铸造，属「先打包后铸造」的固有代价；回填已在 main 分支完成。不要当作错误。

**10. 旧 DOI 落在旧 concept 下**

`21858125`(v1.0.0)/`22064685`(v1.1.0) 属 concept `21858124`，与当前仓库链接已 detach；新记录 concept 为 `23732880`。README 与 `.zenodo.json` 已如实写明「被取代、非本记录版本」。

**11. FDR 存在两种口径，数值差 0.003**

**这是定义差异，不是计算错误，也不是笔误。** Table 2 / S14 用「12 个参数格等权平均」得 0.1001；`fdr_null_fraction_sensitivity.csv` 用「4,800 次重复合并」得 0.0969。同一 regime 的格间 null 判定率不同，平均不等于合并。回信正文的 0.100 用前者，重加权讨论的 0.18/0.26 用后者。**不要把它报成 MISMATCH**，但可以指出正文未声明口径。

### 7b. 本轮已修（勿当遗漏重报，**更勿改回**）

- **Summary 第 6 条原漏两个 A 级案例**：原只写 Education→AD 12→10，漏了 LDL→CAD 与 BMI→T2D（同为 12→10）。S8 的 `delta` 非零行共 8 个，现全部指名，并加「eight of the twelve moved」计数。**已于 2026-10-30 修，勿当作遗漏重报。**
- **R1-9 把 LDL→CAD 的投稿版分数写成 `10/10`**：S8 的 `score_v1` 为 **12**（原 G6 给 2 分）。已改为「12 points in the submitted version … 10 now」。**已于 2026-10-30 修，勿改回。**

---

## 8. 深读索引（第 2 轮用；按审计路径组织）

| 要核什么 | 读哪里 |
|---|---|
| 22 条答复全文 | `reviews/Response_to_Reviewers_Frontiers.md` L1–L333（整份） |
| 评分规则与门的定义 | `课题设计阶段/manuscript_Frontiers_Methods_v2_humanized.md` Methods「The six gates」「Grading rubric」 |
| Table 1 两层表 + 封顶脚注 | `课题设计阶段/manuscript_Frontiers_Methods_v2_humanized.md` Tables 段 |
| Table 2 + 脚注（四信号声明） | `课题设计阶段/manuscript_Frontiers_Methods_v2_humanized.md` Tables 段 |
| 模拟设计与退化 | `课题设计阶段/manuscript_Frontiers_Methods_v2_humanized.md` Methods「Simulation-based validation」 |
| LD 校正的实证 | `课题设计阶段/manuscript_Frontiers_Methods_v2_humanized.md` Results「Precision, limits of detection…」 |
| 失眠→AD 主案 | `课题设计阶段/manuscript_Frontiers_Methods_v2_humanized.md` Results「Example of application」 |
| 十二案逐门证据 + G6 evidence | `manuscript/supplementary/S8_twelve_case_validation.csv` |
| 阈值稳健性四项 | `manuscript/supplementary/S12_threshold_robustness.md`（S12.1–S12.5） |
| 留一门消融 | `manuscript/supplementary/S10_gate_ablation.csv` |
| 封顶前后 | `results/simulation/S14_table2_cap_audit.csv` |
| 规则唯一真源 | `results/validation/rubric_spec_v3.csv` |

---

## 9. 审计契约（第 2 轮输出格式，固定）

**三张表，(A) 必须先出，行数为硬限。**

**表 A — 逐条核账**（22 行，一条不漏）

| 列 | 内容 |
|---|---|
| # | R1-1 … R3-12 |
| 回信声称 | 该条 Response 里最容易被核的一个具体断言；含数字则照抄 |
| 核账位置 | 文件 + 行区间 |
| 实际 | 你在该位置读到的原值；没有就写 `NOT FOUND` |
| 判定 | `PASS` / `MISMATCH` / `NOT IN ARCHIVE` / `OVERCLAIM` |
| 一句话 | 仅当判定非 PASS 时填 |

判定口径：

- `PASS` = 回信断言与证据一致
- `MISMATCH` = 两处写的不是同一个数、或不是同一件事
- `NOT IN ARCHIVE` = 回信提到的数字档案里查不到（**不等于错**，可能是档案缺）
- `OVERCLAIM` = 数字对，但措辞比证据强（如把「未检出」说成「排除」）

**表 B — 只说未改 / 说满**（≤8 行）

| 列 | 内容 |
|---|---|
| 编号 | 回信条目 |
| 问题类型 | `口头接受但正文无对应改动` / `改动幅度小于承诺` / `措辞强于证据` / `回避了意见的核心` |
| 证据 | 回信行 + 正文行 |
| 建议 | 具体到「加哪一句」「改哪个词」；不要写「建议加强论述」 |

**表 C — 修订新引入的错误**（≤8 行）

| 列 | 内容 |
|---|---|
| 位置 | 文件 + 行 |
| 错误类型 | `内部矛盾` / `数字串台` / `新旧表述并存` / `表格与正文不一致` / `失效引用` |
| 说明 | 哪两处矛盾，各写了什么 |
| 修法 | 直接给替换文字（英文原文） |

**最后一行**：`COVERAGE: xx/22 PASS, yy MISMATCH, zz NOT IN ARCHIVE, ww OVERCLAIM`

**不要写导言、不要复述回信、不要写总结段。三张表之后即停。**

**明确不要求你回答**：这篇文章是否仍够格发表、贡献是否被削空、该投哪本刊。
这是作者的决定，不在本轮范围。

---

*本包含索引、骨架、数字卡、已知未决项与审计契约，不含正文。正文按 §8 行区间定向读取。*
