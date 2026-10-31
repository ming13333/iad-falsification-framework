# 待改清单：Frontiers 回信与正文一致性（2026-10-30）

来源：三份外审报告的并集（A / B / C），逐条回源核验后去重、纠错、补全。
核验对象：
- 正文 `课题设计阶段/manuscript_Frontiers_Methods_v2_humanized.md`（307 行）
- 回信 `reviews/Response_to_Reviewers_Frontiers.md`（L1–L331）
- 补充表 `manuscript/supplementary/S8_twelve_case_validation.csv`
- 归档实测 `results/ea_mr/ea_transethnic_insomnia_ad_report.txt`

---

## ✅ 执行完成（2026-10-31 16:05）

16 条全部改完：M0–M7（P0）、W1–W5（P1）、D2–D4（P2）。逐条改法与原文见下文各条；下方为汇总。

| 组 | 条 | 改动要点 |
|---|---|---|
| P0 | M0 | Methods L67/L91/L289 阈值更正为 `r²<0.1`（方案 A），回信 R3-4 重写为先认错再论证 |
| P0 | M1/M2 | L116 首句与 count chain 的 54 变异档归 r²<0.1，补 tight 档 SE 0.236 |
| P0 | M3 | 删 L116 的 APOE 结论句，改为"不归因于 19 号染色体单独"并指向 G3 |
| P0 | M4 | 回信 `above` → `below`（P=0.039 < 0.05） |
| P0 | M5 | 回信 SE 倍率不再称"方差低估"，改为 SE 增大 6.5–7.5 倍（方差差 42–56 倍） |
| P0 | M6 | L153 "pass all six gates" → "Grade A under the current rubric"；"warrant target investment" → "prioritize trait-level hypotheses for target-specific follow-up" |
| P0 | M7 | 回信 G3 规则 `or` → `neither … nor`，并注明仅缺 coloc 记 1 分 |
| P1 | W1 | "restores the sampling variance" → "clumping changed both the instrument set and the reported SE；比值本身不能识别抽样方差"（正文+回信） |
| P1 | W2 | "低效能向零偏倚、不反转符号" → "低效能降分辨率、单次符号反转本身证据弱"（正文+回信） |
| P1 | W3 | 删除"不影响 null 符号"的保证，改为"可影响符号，故仅作方向筛查不计分"（正文×2+回信） |
| P1 | W4 | 网格 {0,0.08,0.15} 全部在 0.226 之下 → "every grid point lies below that boundary；采样的是低效能区"（正文+回信） |
| P1 | W5 | R1-2 (iv) 拆为两层：无 LD 协方差成立、相关残差确实生成（对照代码公式）；开场"correct in every particular"收紧；正文 L101 补层间区分 |
| P2 | D2 | Wilson 区间范围限定为 sensitivity + 两种 specificity；P(A) 与 FDR 的口径说明 |
| P2 | D3 | 补"40 提取 → 30 位置匹配后入模" |
| P2 | D4 | L106 的 0.80 标注为 D-only 口径 |

**收尾校验（附录 B 全绿）**

| 检查 | 结果 |
|---|---|
| 残留错标 `r²<0.001$, 10,000 kb window) reduced` | 无输出 |
| `r²<0.1$, 10,000 kb` 出现次数 | 2（同在 L116） |
| `immediately above the 0.05` / `understatement of sampling variance` | 均无输出 |
| `pass all six gates` / `warrant target investment` | 无输出 |
| `every proportion` / `Every proportion in Table 2` | 无输出 |
| W/D 系列残留（5 组关键词） | 正文 0 / 回信 0 |
| `ea_transethnic_insomnia_ad_harm.tsv` 行数 | 31（表头 + 30） |
| `audit_response_letter.py` | OK，22/22；20 full + 2 in part + 0 declined；正文 5,379 词 |
| 正文 docx | 162 段 / 5 表；15 处关键句全部命中 |
| 回信 docx | 149 段 / 2 表 / 8,422 词；7 处关键句全部命中 |

> `grep -c` 按**行**计数，L116 同时含首句与 count chain 两处，故显示 1；按出现次数为 2。

---

---

## 关于条数：口头 13 → 首次落盘 16 → **定稿 15**（撤回 1 条）

上轮口述 13 条是**凭记忆合并**得来的；落盘时脚本枚举全集后为 16 条；随后核查 S8 的 `.md` 载体，再撤回 1 条。差异如下：

| 变化 | 原因 |
|---|---|
| +1 | R1-1 的 G3 计分规则矛盾（B 的首条发现）在口述时被并入"硬错"未单列 |
| +1 | L116 的同一处错标出现两次（首句 + instrument count chain），口述只算一次 |
| +1 | 正文 L106 的 specificity 口径（B 的 R1-4 附加项）未计入 |
| −1 | **撤回**：S8 的 30 IV 与正文 40 IV 不是矛盾，见 D3 |
| −1 | **撤回 D1**：S8 的 7 条脚注与 reproducibility 段落**确实存在**，在 `.md` 载体里，见 D1 |

> 两次撤回同源：都因只查了 CS 一个载体就下判断。D3 是只比对两处文本、没查生成该数字的报告；D1 是只 grep 了 CSV、没查 `.md`。凡"承诺是否兑现 / 两处数值是否冲突"，须枚举该对象的全部载体与上游日志。

---

## 优先级总表

| ID | 级 | 位置 | 一句话 | 来源 |
|---|---|---|---|---|
| ~~M0~~ ✅ | P0 | 正文 Methods L67 / L91 / L289 ＋ 回信 R3-4 | **已按方案 A 改完**：54 变异 / β=−0.130 实为 `r²<0.1`（`04_mvmr.R:28` 实锤），Methods 三处与回信 R3-4 已同步更正 | 本清单（代码实锤） |
| ~~M1~~ ✅ | P0 | 正文 L116 首句 | **已改**：`r²<0.001`→`r²<0.1`，补齐 tight 档 SE 0.236 | C |
| ~~M2~~ ✅ | P0 | 正文 L116 count chain | **已改**：同上 | 本清单 |
| ~~M3~~ ✅ | P0 | 正文 L116 vs L120 | L116 据染色体剔除作 APOE 结论，L120 明令不得作此结论 | C |
| ~~M4~~ ✅ | P0 | 回信 L156 | `P = 0.039` 写成"位于 0.05 之上" | A/B/C |
| ~~M5~~ ✅ | P0 | 回信 L220 | SE 倍率（6.5–7.5）被称"抽样方差低估倍数"（应为 43–56） | B/C |
| ~~M6~~ ✅ | P0 | 正文 L153 | 称 LDL–CAD"通过全部六门"并"足以支持靶点投资"，S8 其 G6 = 0 | A/B/C |
| ~~M7~~ ✅ | P0 | 回信 L64 | G3 规则写"LDSC **或** colocalization 不可运行即 0 分"，正文与 Table 1 为"两者均" | B/C |
| ~~W1~~ ✅ | P1 | 回信 L94 + 正文 L118 | "restores the sampling variance" 归因过强（工具集同时改变） | A/B/C |
| ~~W2~~ ✅ | P1 | 回信 L124 + 正文 L134 | "does not reverse its sign" 为绝对统计论断 | A/B/C |
| ~~W3~~ ✅ | P1 | 回信 L230 + 正文 L79/L126 | "不影响 null 的符号" / "不能产生同向虚假估计" 无保证 | A/B/C |
| ~~W4~~ ✅ | P1 | 回信 L282 + 正文 L99 | 网格 {0, 0.08, 0.15} 全在 0.226 之下，不能称 brackets | B/C |
| ~~W5~~ ✅ | P1 | 回信 L78 | (iv) 项过度认错：代码**确实**生成相关残差 | 本清单（代码实锤） |
| ~~D1~~ | — | 回信 L192 / L316 | **已撤回**：脚注 1–7 与 reproducibility 段落存在，在 `S8_..md` 里 | — |
| ~~D2~~ ✅ | P2 | 回信 L15 / L108 | 称"每一个比例"都有 Wilson 区间，实际仅 sens + 两种 spec | A/B/C |
| ~~D3~~ ✅ | P2 | 正文 L116 vs S8 | 40 与 30 是"提取 / harmonise 后"，不是矛盾，但**未说明** | A（判定需修正） |
| ~~D4~~ ✅ | P2 | 正文 L106 | specificity 0.80 未标 D-only 还是 C/D 口径 | B |

---

## P0 · 必须先改（审稿人会直接指出"没改"）

### M0 · 主分析的 clumping 阈值：Methods 声明与实际运行不一致（新发现，最高优先）

改 M1/M2 时发现，问题不止"正文某一处标错"，而是 **Methods 声明的阈值与产生主结果的阈值不是同一个**。

**逐字证据链**

| 来源 | 内容 | 指向 |
|---|---|---|
| `code/r_analysis/04_mvmr.R:28` | `THRESH <- list(p1 = 5e-8, clump_kb = 10000, r2_tight = 0.001, r2_loose = 0.1)` | 两档的真实参数 |
| `manuscript/supplementary/S2` 行名 | `clump_loose` = 54 IV / β=−0.130 / SE=0.203；`clump_tight(42)` = 37 IV / β=−0.111 / SE=0.236 | 54 属 loose |
| `code/make_figures.py:90` | `("Clumped UVMR (r2=0.1)", -0.130, ...)`；下一行 `("Clumped UVMR (r2=0.001)", -0.111, ...)` | 图注已正确区分 |
| `results/ea_mr/ea_transethnic_insomnia_ad_report.txt:17` | `EUR clumped (54 IVs, loose): beta = -0.130, p = 0.52  [manuscript Level 2]` | 明写 loose |
| 正文 L67 / L91 / L289（Methods） | `LD clumping ($r^2 < 0.001$, 10,000-kb window, 1000 Genomes EUR reference)` | 声明 0.001 |
| 回信 R3-4（L240） | "They are the TwoSampleMR/IEU defaults (r² < 0.001, 10,000 kb), adopted as the field's most conservative" | 声明 0.001 |

**矛盾**：正文 Level 2（G2）唯一报出的数值是 54 变异 / β=−0.130 / SE=0.203，那是 `r²<0.1` 的结果；而 Methods 三处与回信 R3-4 都说主分析用 `r²<0.001`。**投稿版即如此，审稿人未察觉**（R3-4 的提问正是基于"你们用 0.001"这个前提）。

**两条互斥的修法，须先定方向**

- **方案 A（改 Methods 向 0.1）**：L67 / L91 / L289 的 `r²<0.001` 改为 `r²<0.1`，并把 0.001 档写成本文额外报告的更严档。
  - 不动摘要、Table 2、Fig 2A、回信数值 → 与所有已报数值零冲突，改动面最小。
  - 代价：回信 R3-4 须重写——不能再以"我们采用最保守设置"作辩护，改为"主分析用 IEU 常用设置之一（r²<0.1），并额外报告更严档；**结论在最宽松档已翻转**，因此不依赖严格设置"。（此论证实际更强。）
- **方案 B（改 Results 向 0.001）**：L116 主叙述改为 37 变异 / β=−0.111 / SE=0.236，54/−0.130 降级为 loose 敏感性。
  - 保留 Methods 与 R3-4 现有措辞。
  - 代价：摘要、Table 2、Fig 2A、回信所有引用 −0.130 / P=0.52 之处须同步改（约 10 余处），且 "54-versus-40 discrepancy" 段须重写为 37-versus-40。

> **✅ 已按方案 A 执行（2026-10-31 11:10）**，改动如下：
>
> | 位置 | 改法 |
> |---|---|
> | 正文 L67（Methods, G2） | 主句改 `$r^2 < 0.1$`，括注 `a stricter $r^2 < 0.001$ tier is reported alongside in Supplementary Table S11` |
> | 正文 L91（流程步骤 3） | `Perform LD clumping at $r^2 < 0.1$ within $10,000\text{ kb}$, and repeat at the stricter $r^2 < 0.001$ tier` |
> | 正文 L289（流程表第 3 行） | 同 L91（与 L91 用 replace_all 一次改两处，保证逐字一致） |
> | 回信 R3-4 正文 | 重写为两段：先承认投稿版 Methods 把主档误写为 0.001（并点出归档管线的 `r2_loose = 0.1`/`r2_tight = 0.001`），再论证"更正后审稿人前提不再成立、结论在最宽松档已翻转" |
> | 回信 R3-4 标题 | 加 `*(Methods corrected in revision)*` |
> | 回信 R3-4 Changes | 明写 `clumping threshold **corrected** to r² < 0.1` |
> | 回信处置表 R3-4 行 | 处置改 `Accepted in part; Methods corrected`，位置补 `(threshold corrected to r² < 0.1)` |
> | 回信 Summary 第 6 条 | 加一句"该意见促我们发现并更正了 Methods 的描述错误" |
>
> **未改**：摘要（不含阈值，只有 `β=−0.13, P=0.52`，数值未变）、Table 2（不含阈值）、Fig 2A（本就同画两档 `r2=0.1` / `r2=0.001`）。
>
> **连带修正（A 案暴露的新问题）**：正文 L116 原称 54 与跨族裔 40 的差异"仅源于 LD 参考面板更新"。实测跨族裔用 `r²<0.001`（`code/ea05_transethnic_insomnia_ad.py:7` 与报告 L3），主分析用 `r²<0.1`，**阈值与面板同时变**。已改为"two sources"，并明确两步不可 like-for-like 比较、跨族裔只作低效能方向筛查。同时修正 `ea05` 脚本 L155 的同一错误表述（仅影响将来重跑，已归档的 `results/ea_mr/` 输出保持 v1.2.1 原样未动）。
>
> **验证**：`54 → 44（1-Mb 窗）→ 38 → 33` 链条与 `S7_iv_annotation_confounder.csv` 实测吻合（44 行、6 excluded、38 retained）；正文 md 段落词数 10,987 → 11,056（+69）；正文 docx 重导 162 段/5 表；回信 docx 重导 149 段/2 表/8,251 词；`audit_response_letter.py` 复跑全绿（22/22 覆盖、20 full + 2 in part + 0 declined、5,218 词）。

---

### M1 · 正文 L116 首句：阈值归属错 ✅ 已改（2026-10-30 23:05）

**原文**
> **G2: robustness.** LD clumping ($r^2 < 0.001$, 10,000 kb window) reduced the instrument set to 54 variants and attenuated the estimate to the null ($\beta = -0.130$, $\text{SE} = 0.203$, $P = 0.52$). A narrower window (5,000 kb; 37 instruments) produced consistent results ($\beta = -0.111$, $P = 0.64$).

**问题**：54 变异 / SE 0.203 对应 `r²<0.1`，不是 `r²<0.001`。依据三处一致：正文 L118（`SE widened 6.5-fold at r²<0.1 (SE = 0.203, 54 variants)`，且 0.031→0.203 恰为 6.5 倍，数学自洽）、回信 L240、Table S11。

**替换**
> **G2: robustness.** LD clumping ($r^2 < 0.1$, 10,000 kb window) reduced the instrument set to 54 variants and attenuated the estimate to the null ($\beta = -0.130$, $\text{SE} = 0.203$, $P = 0.52$). Tightening the threshold to $r^2 < 0.001$ left 37 variants with a consistent null estimate ($\beta = -0.111$, $\text{SE} = 0.236$, $P = 0.64$), and narrowing the window to 5,000 kb gave the same result.

**连带**：替换后须删除紧随的原句 `A narrower window (5,000 kb; 37 instruments) produced consistent results...`，否则重复。

**验证**：`grep -n "r\^2 < 0.001\$, 10,000 kb window) reduced" 课题设计阶段/manuscript_Frontiers_Methods_v2_humanized.md` 应无输出。

**✅ 实际改法（与上方替换句略有出入，取更精确版）**

> **G2: robustness.** LD clumping ($r^2 < 0.1$, 10,000 kb window) reduced the instrument set to 54 variants and attenuated the estimate to the null ($\beta = -0.130$, $\text{SE} = 0.203$, $P = 0.52$). Tightening to $r^2 < 0.001$ at the same window left 37 harmonised variants with a consistent null estimate ($\beta = -0.111$, $\text{SE} = 0.236$, $P = 0.64$), and a 5,000-kb window at that threshold gave the same estimate.

与清单原替换句的差异及理由：原句写 "left 37 variants"，但 S11 注（1）与回信 L240 均明确 `r²<0.001 / 10,000 kb` 先留 **42 loci**，**harmonise 后**才是 37 变异；故改为 "left 37 harmonised variants"，既不虚报也不把 42 与同段的 "44 window-clumped loci（1-Mb 窗）"混淆。原句把 5,000 kb 说成"产生 37 变异"的那一笔，改为"在该阈值下 5,000-kb 窗给出相同估计"，与回信 L240 的三档表述一致。

---

### M2 · 正文 L116 instrument count chain：同一错标第二次出现 ✅ 已改（2026-10-30 23:05）

**原文**
> The instrument count chain is: 2,462 unclumped instruments (Gate G1) $\rightarrow$ 54 LD-independent instruments after clumping ($r^2 < 0.001$, 10,000 kb) $\rightarrow$ 44 window-clumped loci

**问题**：C 的修法只改首句，此处的 `r²<0.001` 未动，改完 M1 后正文仍自相矛盾。三份审计均未覆盖。

**替换**
> 54 LD-independent instruments after clumping ($r^2 < 0.1$, 10,000 kb)

**✅ 已按此执行**。连同 M1，全文 `r²<0.001` 附近不再出现 54 的误归属（剩余 L67 / L91 / L289 是 M0 的 Methods 声明，L118 是正确的三档对照句）。

---

### M3 · 正文 L116 与 L120 的 APOE 结论冲突

**原文（L116 末）**
> This signal attenuation was not driven by the *APOE* locus, as excluding 118 chromosome-19 instruments retained the unclumped association ($\beta = 0.094$, $P = 0.003$).

**原文（L120）**
> That exclusion removes the whole of chromosome 19 rather than the *APOE* region specifically, because *APOE* lies at 19q13.32 and cannot be isolated by chromosome-level filtering; we therefore make no *APOE*-specific claim from it.

**问题**：L116 正是据该剔除作出 APOE 特异性结论，L120 又明令不作此结论。属硬矛盾，且是 C 判 R1-6 为 MISMATCH 的唯一依据。

**替换**：删结论、留事实、指向 L120。
> Excluding 118 chromosome-19 instruments retained the unclumped association ($\beta = 0.094$, $P = 0.003$); as set out under G3, this removes the whole chromosome rather than the *APOE* region and supports no *APOE*-specific claim.

> 注：C 建议的写法与 L120 近乎逐字重复，此处改为删句 + 指向，避免同一节内重复解释。

---

### M4 · 回信 L156：`above` 应为 `below`

**原文**
> The Kunkle classification (P = 0.039) sits immediately above the 0.05 boundary

**问题**：0.039 < 0.05。错的是方位词，不是 P 值。正文 L116 只写 `boundary forward CAUSAL classification`，未复述 `above`，故只改回信。

**替换**
> The Kunkle classification (P = 0.039) sits immediately below the 0.05 boundary

---

### M5 · 回信 L220：把 SE 倍率当成方差倍率

**原文**
> clumping widens the same estimate's SE to 0.203–0.236 — a 6.5- to 7.5-fold understatement of sampling variance

**问题**：SE 由 0.031 增至 0.203（6.55 倍）/ 0.236（7.61 倍）。方差倍率为其平方：**43–58 倍**。正文 L118 说的是 `widened 6.5-fold`（对 SE），口径正确；错在回信换成 "sampling variance"。

**替换**
> clumping widens the same estimate's SE from 0.031 to 0.203–0.236 — a 6.5- to 7.5-fold increase in the reported standard error

---

### M6 · 正文 L153：与 S8 评分不符的转化表述

**原文 1**
> Causal claims that pass all six gates, such as LDL-cholesterol and coronary artery disease (Grade A; Allara et al., 2019), align with drug targets whose efficacy was confirmed in clinical trials.

**原文 2**
> The framework offers a preclinical triage system: Grade A–B signals warrant target investment, whereas Grade C–D signals indicate shared liability or confounding

**问题**：S8 该案 `L1–L6 = 2,2,2,2,2,0`，G6 = 0，**五门而非六门**。同段的限制句（"待前瞻检验的假设"）不能抵消这两句更强的主张。

**替换 1**
> Causal claims graded A under the rubric—LDL-cholesterol and coronary artery disease, for instance (10 of 12 points; Allara et al., 2019; G6 = 0, so it passes five of six gates)—align with drug targets whose efficacy was confirmed in clinical trials.

**替换 2**
> Grade A–B signals prioritise trait-level hypotheses for target-specific follow-up, whereas Grade C–D signals indicate shared liability or confounding

---

### M7 · 回信 L64：G3 计分规则与正文/Table 1 不符

**原文**
> fewer than three independent instruments (G2), LDSC or colocalization not runnable (G3), conditional F ≤ 10 or no estimable model (G4)

**问题**：正文 L71 与 Table 1（L242）均为 `0 for architectural evidence contradicting the claim, or where **neither** LDSC nor colocalization could be run`，且 `colocalization was not performed` 计 **1** 分。回信写成"或"，与 2 处正文冲突（2:1，改回信）。

**替换**
> fewer than three independent instruments (G2); at G3, 0 only where neither LDSC nor colocalization could be run, with colocalization absent but $r_g$ direction-consistent scoring 1 as in Table 1; conditional F ≤ 10 or no estimable model (G4)

---

## P1 · 措辞越界（数值不动，只收紧论断）

### W1 · R1-3：SE 增大不能单独证明"恢复方差"

**位置**：回信 L94、正文 L118

**原文（正文 L118）**
> LD correction thus does not merely attenuate a coefficient; it restores the sampling variance that instrument redundancy had suppressed, and this restoration is what dissolves the claim at Gate G2.

**替换**
> LD correction thus does not merely attenuate a coefficient; it widens the reported standard error from 0.031 to 0.203–0.236, and this widening is what dissolves the claim at Gate G2. The widening cannot be attributed to instrument redundancy alone, because the instrument set changed at the same time.

**原文（回信 L94 后半）**
> it does not merely attenuate the coefficient, it restores the sampling variance that instrument redundancy had suppressed, and the apparent significance of the unclumped estimate (P = 9.3 × 10⁻⁴) does not survive that restoration.

**替换**
> it does not merely attenuate the coefficient: the reported standard error widens from 0.031 to 0.203–0.236, and the apparent significance of the unclumped estimate (P = 9.3 × 10⁻⁴) does not survive that widening. Because the instrument set changed at the same time, the ratio does not by itself identify the sampling variance of the original set.

---

### W2 · R1-5："不反转符号"是绝对论断

**位置**：回信 L124、正文 L134

**原文（两处同句）**
> Underpowering attenuates an estimate towards zero, it does not reverse its sign, and it does not produce locus-specific colocalization concentrated in the opposite direction.

**替换**
> Underpowering attenuates an estimate towards zero on average, but an imprecise estimate can take either sign, so a single reversal is weak evidence on its own; what underpowering does not produce is locus-specific colocalization concentrated in the opposite direction.

---

### W3 · R3-3：跨族裔偏差不保证不动符号

**位置**：回信 L230、正文 L79、正文 L126

**原文（正文 L126）**
> Both affect precision and the magnitude of the point estimate rather than the sign of a null result, which is why the step is read only for directional concordance, and why the framework assigns it no points at the power achieved here.

**替换**
> Both affect precision and the magnitude of the point estimate, and may affect its sign as well; the step is therefore read only for directional concordance and receives no points at the power achieved here.

**原文（正文 L79）**
> it cannot create a spurious estimate in the claimed direction when the sign is concordant

**替换**
> it can bias the estimate in either direction, which is why the step is treated only as a directional screen and scores no points

**原文（回信 L230）**：同 L126 句，按同一替换。

---

### W4 · R3-9：网格并未跨越 0.226 阈值

**位置**：回信 L282、正文 L99

**原文（正文 L99）**
> 0.15 sits just below the 0.226 threshold at which the worked example reaches 80% power, so the grid brackets the boundary between detectable and undetectable claims.

**替换**
> 0.15 sits just below the 0.226 threshold at which the worked example reaches 80% power; the grid therefore stops short of that threshold, and we do not claim that it brackets the boundary between detectable and undetectable claims.

**原文（回信 L282）**：同句，按同一替换。

---

### W5 · 回信 L78 (iv)：过度认错，代码实为正确

**位置**：回信 L78

**原文**
> (iv) No LD covariance and no correlated exposure–outcome errors are generated; instrument effects are drawn independently, so the simulation contains no inter-instrument LD at all.

**实证**：`code/sim_framework_operating_chars.py:L108-L109`

```python
if overlap > 0:
    e_y = overlap * e_x + np.sqrt(1 - overlap ** 2) * e_y
```

即**样本重叠正是通过相关残差噪声实现的**。正文 L101（`sample overlap induced by introducing correlated residual noise between exposure and outcome samples`）是**正确的**，不该改。审稿人此项指控只对了一半（无 LD covariance 成立，无 correlated residuals 不成立）。

**替换**
> (iv) No inter-instrument LD covariance is generated, because instrument effects are drawn independently; sample overlap is instead induced by adding a correlated residual to the outcome error, so the simulation does contain correlated exposure–outcome residuals even though it contains no LD.

**连带（必须同时改）**：R1-2 开头 `accepted in full. ... it is correct in every particular` 需降为"五项成立、一项更正"，否则同段自相矛盾。建议：
> **Response: accepted in part — five of the six items are correct as stated and are addressed below; the sixth (correlated exposure–outcome errors) is corrected here rather than conceded.**

> 风险提示：此改会削弱"全盘认错"的姿态。若不愿动，替代方案是保留认错但在 L78 加脚注指向 L101 与代码行号——不推荐，因为审稿人一旦复核代码，会被视为明知不改。

---

## P2 · 承诺与口径（不致命，但被核对就会暴露）

### ~~D1~~ · 已撤回：S8 的脚注与 reproducibility 段落确实存在

**原判断**：回信 L192 承诺 `footnotes 5–7, revised reproducibility paragraph`、L316 承诺 `footnotes 1–7`，而 `S8_twelve_case_validation.csv` 中 `grep -ci "footnote\|reproducib"` = 0 → 判为承诺未兑现。

**撤回依据**：S8 有三种载体，脚注在 `.md` 里。

| 载体 | 内容 | 脚注 |
|---|---|---|
| `S8_twelve_case_validation.md`（7,489 B） | 表格 + `**Scoring reproducibility.**` 段 + `**Footnotes.**` 段 | **1–7 条全在**（门定义、G1 cascade、Egger P 语义、n instruments、G6 计分、decisive failure、与投稿版差异） |
| `S8_twelve_case_validation.csv`（2,634 B） | 纯数据，24 列 | 否（CSV 不承载脚注，属正常） |
| `Supplementary_Tables.xlsx` 的 S8 sheet | 渲染版 | 否 |

**结论**：回信的两处承诺均已兑现，A 的 R1-9 判 MISMATCH 因此不成立。**不改任何文件。**

**教训**：判断"承诺是否兑现"必须枚举该表的全部交付载体（md / csv / xlsx / docx），CSV 无脚注是设计而非缺陷。

---

### D2 · Wilson 区间的覆盖范围

**位置**：回信 L15、L108

**原文（L15）**
> all proportions carry 95% Wilson intervals

**原文（L108）**
> Every proportion in Table 2 now carries a 95% Wilson score interval computed on the pooled 4,800 replicates per row

**实际**：Table 2 中敏感度与两种特异度有区间；`P(Grade A)` 无区间；FDR 列是 12 个参数格的范围（min–max），不是区间估计。

**替换（L15）**
> sensitivity and both specificity columns carry 95% Wilson intervals

**替换（L108）**
> Sensitivity and both specificity columns in Table 2 now carry 95% Wilson score intervals computed on the pooled 4,800 replicates per row (for example, balanced specificity C/D = 0.882, 95% CI 0.873–0.891); P(Grade A) carries none, and FDR is reported as the range across the twelve parameter cells.

---

### D3 · 40 与 30 不是矛盾（**撤回 A 的判定**）

**位置**：正文 L116 vs S8 `G6_evidence`

**实测**：`results/ea_mr/ea_transethnic_insomnia_ad_report.txt`

```
Exposure: Insomnia ukb-b-3957 ... 40 LD-independent instruments at r2<0.001, 10 Mb
Harmonized: 30/40 instruments matched positionally; strand-aligned; 30 retained
Instrument count (n=30) differs from primary EUR analysis (n=54) due to LD reference panel update
```

**结论**：40 = 提取到的 LD 独立工具；30 = harmonise 后位置匹配成功并保留的工具。**两者都对**，A 判 MISMATCH 并建议"统一为 40 IV"是错的——若照改，S8 会与 MR 实际入模数（30）不符。

**唯一缺陷**：正文只写 40，未交代 40→30 的损耗。

**建议**：正文 L116 该句补半句
> $\rightarrow$ 40 harmonised trans-ethnic instruments, of which 30 matched positionally and entered the MR

**验证**：`grep -c "^" results/ea_mr/ea_transethnic_insomnia_ad_harm.tsv` = 31（表头 + 30 行），与 report 的 30 retained 一致。

**附带待核**：S8 的 `IVW_beta = −0.128` 与正文 `−0.130` 差 0.002。report 仅记录 EUR clumped `beta = −0.130`。需确认 −0.128 出自哪次运行；若属不同 reference panel 的复算，加注说明即可，不必统一。

---

### D4 · specificity 0.80 未标口径

**位置**：正文 L106

**原文**
> Under balanced pleiotropy, marginal specificity was 0.80 (scenario range 0.77–0.84) with a marginal FDR of 0.10 (scenario range 0.06–0.15).

**问题**：R1-4 已确立双口径（D-only 与 C+D），Table 2 两种都报。此处 0.80 是 D-only，C+D 为 0.88，但正文未标，读者会与 Table 2 的 0.88 冲突。

**替换**
> Under balanced pleiotropy, marginal specificity was 0.80 under the Grade D-only convention (0.88 under Grade C+D; scenario range 0.77–0.84 for D-only) with a marginal FDR of 0.10 (scenario range 0.06–0.15).

---

## 附录 A · 补充表版本隔离（**已于 2026-10-30 22:36 执行完毕**）

### A-1 实际状态：不是"两套"，是"三目录、两状态"

| 目录 | 工作簿 | sheets | S8 列 | S8 分数（LDL/EDU/BMI/Height/INS） | 判定 |
|---|---|---|---|---|---|
| `manuscript/supplementary/` | `Supplementary_Tables.xlsx` | **12** | 24 | **10/10/10/8/4**（封顶后） | ✅ 唯一权威 |
| `课题设计阶段/Supplementary_final/` | 原 xlsx（Sep 2） | 9 | 17 | 12/12/12/10/4 | 🔴 旧制；**但同目录的 CSV/MD 全是新版** |
| `课题设计阶段/Supplementary/` | `Supplementary_Tables.xlsx` | 9 | 17 | 12/12/12/10/4 | 🔴 全面旧版 |

`Supplementary_final/` 是**混合态**：S8/S9/S10/S11 的 CSV+MD 与权威版逐字节相同，唯独 `Supplementary_Tables.xlsx` 从未重建（停留在 Sep 2）。这种"同目录一半新一半旧"比整目录旧版更危险——只看目录名会以为一致。

### A-2 已执行的处置

1. **7 个旧制文件加 `_SUPERSEDED_<日期>` 后缀**（原文件全部保留，仅改名）：
   - `课题设计阶段/Supplementary/Supplementary_Tables.xlsx` → `..._SUPERSEDED_20260902.xlsx`
   - `课题设计阶段/Supplementary_final/Supplementary_Tables.xlsx` → `..._SUPERSEDED_20260902.xlsx`
   - `课题设计阶段/Supplementary/S8_twelve_case_validation.csv` → `..._SUPERSEDED_20260804.csv`
   - `课题设计阶段/Supplementary/S8_twelve_case_validation.md` → `..._SUPERSEDED_20260810.md`
   - `课题设计阶段/Supplementary/S9_simulation_operating.csv` / `.md` / `_marginal.csv` → `..._SUPERSEDED_20260902.*`
2. **`Supplementary_final/Supplementary_Tables.xlsx` 用权威版覆盖**：MD5 `2436d374408eb668572e8354985b2b20`，与 `manuscript/supplementary/` 逐字节一致，12 sheet。
3. **写两份声明**：
   - `manuscript/supplementary/_AUTHORITATIVE.md`（唯一来源、判据表、S8 三载体分工）
   - `课题设计阶段/Supplementary/_SUPERSEDED_README.md`（禁用清单、哪些文件属独有不得动）
4. **不动目录结构**：`reviews/` 下 20+ 处文档引用 `Supplementary_final/` 路径，移动目录会断引用；只改名不动位置。

### A-3 未动的东西（有意保留）

| 文件 | 原因 |
|---|---|
| `课题设计阶段/Supplementary/` 下 9 个 ONLY-HERE 文件（G2b 审计、Pvalue_decision_table、S7_dual_track、S7b_gwascatalog、power_calc_EUR、pruned_mr_sensitivity、Supplementary0805.docx、两个 Note） | 权威目录无对应物，属独有历史材料 |
| `Supplementary_final/Supplementary_Notes.docx`（42 KB） | 同上，两份 Note 的合并渲染版 |
| `Supplementary_final/` 的 S8/S9/S10/S11 CSV+MD | 与权威版 MD5 相同，已是新版 |

### A-4 执行后校验

```
python code/build_supplementary_workbook.py --check   →  workbook OK
md5sum manuscript/supplementary/Supplementary_Tables.xlsx
      Supplementary_final/Supplementary_Tables.xlsx   →  两者同为 2436d374...
ls 课题设计阶段/Supplementary/ | grep superseded       →  6 个 + README
脚本引用检查：make_review_packet.py 依赖的
  Supplementary_final/S8_...csv、S9_.._marginal.csv   →  未改名，引用完好
```

---

## 附录 B · 改完后的验证清单

按顺序跑，全绿才算改完：

```bash
# 1) 阈值归属只出现在正确位置
grep -n "r\^2 < 0.001\$, 10,000 kb window) reduced" 课题设计阶段/manuscript_Frontiers_Methods_v2_humanized.md   # 期望：无输出
grep -c "r\^2 < 0.1\$, 10,000 kb" 课题设计阶段/manuscript_Frontiers_Methods_v2_humanized.md                    # 期望：≥2

# 2) above/below 与方差口径
grep -n "immediately above the 0.05" reviews/Response_to_Reviewers_Frontiers.md        # 期望：无输出
grep -n "understatement of sampling variance" reviews/Response_to_Reviewers_Frontiers.md # 期望：无输出

# 3) 六门表述
grep -n "pass all six gates\|warrant target investment" 课题设计阶段/manuscript_Frontiers_Methods_v2_humanized.md  # 期望：无输出

# 4) Wilson 承诺
grep -n "every proportion\|Every proportion in Table 2" reviews/Response_to_Reviewers_Frontiers.md  # 期望：无输出

# 5) S8 与正文的 IV 数口径
grep -c "^" results/ea_mr/ea_transethnic_insomnia_ad_harm.tsv   # 期望：31

# 6) 回信结构完整性（22 条覆盖 / 表态 / Changes）
python code/audit_response_letter.py      # 期望：OK every comment is quoted, answered, dispositioned and located

# 7) 回信 docx 重导（先确认无预览占用）
python -c "open('reviews/Response_to_Reviewers_Frontiers.docx','r+b').close(); print('free')"
python code/md_to_docx_response.py --in reviews/Response_to_Reviewers_Frontiers.md --out reviews/Response_to_Reviewers_Frontiers.docx
```

改完后回信字数会上升约 120–150 词（W5 的降级句 + M7 的 G3 从句 + D2 的补充），`audit_response_letter.py` 的字数统计会随之变化，属预期。
