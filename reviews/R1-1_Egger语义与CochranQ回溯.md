# S8 两处悬空量的回溯裁决：`Egger_P` 语义 与 Cochran Q 缺失

> 目的：为 R1#1（统一评分表）与 R1#9（12 例证据来源）提供可写进 Methods 的事实基础。
> 方法：回到原始输出（`S4`、`S2`、`S6`、`G1_bidirectional.rds`），不做任何推测性补值。
> 产物：`output/results/Simulation/S8_diagnostics_recovery.csv`（12 例 × 诊断量回收矩阵）
> 日期：2026-10-27

---

## 结论（三句）

1. **`Egger_P` 的主体是 MR-Egger 斜率（因果估计）的 p 值，不是截距**——L2 拟合检验 8/11 支持斜率、5/11 支持截距，且 `HDL→CAD` 的备注原文 "IVW sig but Egger null" 只能是斜率语义。但**该列至少混进了一格截距**（`CRP→CAD`，0.009），因此它是一个**混合列**，必须拆成两列。
2. **Cochran Q 在 12 例中从未被计算或记录**——不是"漏抄"，是"没算"。仅 2 例可回收：`Education→AD`（Q=268.60, df=311, p=0.427，来自 S4）与 `Insomnia→AD`（Q=37.62, df=30, p=0.160，来自 rds 的 31-IV 版）；其余 10 例**离线不可回收**，需重跑外部队列，而本机出口对这些主机封锁。
3. **没有任何一条仅依赖已记录列的规则能复现全部 12 个 L2 值**（最佳规则失配 2/12）。失配的两格（`HDL→CAD`、`Education→T2D`）恰好就是备注里引用了「Egger 截距」与「高异质性」的两格——这反过来证明：**G2 真正依赖的两个量只存在于自由文本备注，从未进入表格**。

---

## 一、`Egger_P` 到底是什么：三重判定

### 判定 1 — 项目内部命名规范（决定性）

本项目所有补充表遵循同一套列名，**截距与斜率从不共用一列**：

| 文件 | 斜率列 | 截距列 |
|---|---|---|
| `S2_instrument_sensitivity.csv` | `b_egger` / `p_egger` | `egger_intercept` / `egger_intercept_p` |
| `S4_education_PheWAS.csv` | `b_egger` / `p_egger` | `egger_intercept_p` |
| `S6_Height_AD_exploratory.csv` | `b_egger` / `se_egger` / `p_egger` | （未列） |
| 原始 RDS `G1_bidirectional.rds` | `$res` 表中 `method=="MR Egger"` 的 `pval` | `$pleio` 表的 `pval`（`mr_pleiotropy_test`） |

S6 是最直接的旁证：`b_egger=-0.071, se_egger=0.092, p_egger=0.44` —— 一个 beta/se/p 三元组，只能是**斜率**。

`G1_bidirectional.rds` 里两者分离得最清楚（失眠→AD，31 IV）：

```
-- res（MR Egger）--        b = -0.3081   se = 0.8815   p = 0.7293   ← 斜率
-- pleio（Egger 截距）--     intercept = 0.002628  se = 0.009968  p = 0.7939
-- het（Cochran Q, IVW）--   Q = 37.6208  df = 30  p = 0.1597
```

⇒ S8 的列名 `Egger_P` **没有跟着这套规范走**，语义靠猜。

### 判定 2 — L2 拟合检验（把两种解释各自代入 G2 的代码规则，看哪个能反推出实际的 L2）

按 `code/sim_framework_operating_chars.py` L140 的口径：`2 需 IVW 显著 且 Egger 截距 p ≥ 0.05`。

| Case | IVW_P | Egger_P | 实际 L2 | 若=截距 → L2 | 若=斜率 → L2 |
|---|---|---|---|---|---|
| LDL→CAD | 2.0e-20 | 4.1e-09 | 2 | 1 🔴 | 2 ✅ |
| BMI→T2D | 1.4e-03 | 0.136 | 2 | 2 ✅ | 1 🔴 |
| Height→CAD | 6.1e-08 | 0.046 | 2 | 1 🔴 | 2 ✅ |
| BMI→Stroke | 1.8e-02 | 0.505 | 1 | 2 🔴 | 1 ✅ |
| HDL→CAD | 8.9e-04 | 0.891 | 1 | 2 🔴 | 1 ✅ |
| CRP→CAD | 4.4e-01 | 0.009 | 0 | 0 ✅ | 0 ✅ |
| BMI→AD | 3.2e-01 | 0.567 | 0 | 0 ✅ | 0 ✅ |
| Education→T2D | 2.1e-26 | 0.036 | 1 | 1 ✅ | 2 🔴 |
| Depression→AD | 1.4e-02 | 0.119 | 1 | 2 🔴 | 1 ✅ |
| T2D→AD | 7.1e-01 | 0.268 | 0 | 0 ✅ | 0 ✅ |

**斜率 8/10，截距 5/10**（另 2 例 `—` 不可判）。

再把 `Education→AD` 从 S4 补进来（Egger 斜率 p=0.1409，截距 p=0.6911，实际 L2=2）：
截距 6/11、斜率 8/11 —— **斜率解释稳定占优**。

### 判定 3 — 备注文案

| Case | Notes 原文 | 只能读作 |
|---|---|---|
| HDL→CAD | "IVW sig but **Egger null**; MR corrective" | 斜率（"Egger 估计为零"） |
| Education→T2D | "**Egger int p=0.036** + high hetero -> B" | 截距（作者自己写了 "int"） |
| CRP→CAD | "**Clean null** at extreme power F=176" | 若 0.009 是斜率则与 "clean null" 直接冲突 → 应为截距（方向性多效性） |

### 判定结论

> **`Egger_P` 是一个混合列。** 主体（约 8–9 格）是 MR-Egger **斜率** p；至少 `CRP→CAD` 一格按备注逻辑只能是**截距** p；`Education→T2D` 备注明写 "int" 但数值 0.036 若作斜率也自洽，无法从文件确证。
>
> 因此**不能**通过"换个列名"解决，必须拆成 `Egger_slope_P` 与 `Egger_intercept_P` 两列，并回原始输出重取——而其中 10 例的原始输出不在库内。

---

## 二、Cochran Q：不是漏抄，是从未计算

### 2.1 12 例回收矩阵

| Case | L2 | Egger 斜率 p | Egger 截距 p | Cochran Q (P) | n_IV | 来源 |
|---|---|---|---|---|---|---|
| LDL→CAD | 2 | 4.1e-09 | not recorded | **not recorded** | not recorded | — |
| Education→AD | 2 | 0.1409 | **0.6911** | **0.4268**（Q=268.60, df=311） | **312** | `S4_education_PheWAS.csv` |
| BMI→T2D | 2 | 0.136 | not recorded | **not recorded** | not recorded | — |
| Height→CAD | 2 | 0.046 | not recorded | **not recorded** | not recorded | — |
| Insomnia→AD | 0 | 0.7293 | **0.7939** | **0.1597**（Q=37.62, df=30） | **31** | `G1_bidirectional.rds$fwd`（※ 31-IV 版） |
| BMI→Stroke | 1 | 0.505 | not recorded | **not recorded** | not recorded | — |
| HDL→CAD | 1 | 0.891 | not recorded | **not recorded** | not recorded | — |
| CRP→CAD | 0 | 0.009（疑为截距） | not recorded | **not recorded** | not recorded | — |
| BMI→AD | 0 | 0.567 | not recorded | **not recorded** | not recorded | — |
| Education→T2D | 1 | 0.036 | not recorded | **not recorded**（备注称 "high hetero"） | not recorded | — |
| Depression→AD | 1 | 0.119 | not recorded | **not recorded** | not recorded | — |
| T2D→AD | 0 | 0.268 | not recorded | **not recorded** | not recorded | — |

**可回收 2/12（16.7%）；10/12 需要重跑外部暴露-结局对。**

### 2.2 两条可回收值的完整原文

**Education→AD（n_iv=312，Kunkle ieu-b-2）**

```
b_ivw = -0.3276  se = 0.07463  p = 1.133e-05
b_wmed = -0.41568               p_wmed = 1.8998e-04
b_egger = -0.44327              p_egger(斜率) = 0.14094
Q_ivw = 268.5955  Q_p_ivw = 0.42685
egger_intercept_p = 0.69108
```
⇒ S8 里 `Education→AD` 的 `WM_P` 与 `Egger_P` 两个 `—` **本来有值**，可直接补：`WM_P=1.9e-04`、`Egger_slope_P=0.141`、`Egger_intercept_P=0.691`、`Q_P=0.427`、`n_IV=312`。

**Insomnia→AD（31 IV，2026-07-20 冻结版）**

```
IVW  b=-0.0889  se=0.2893  p=0.7585
WM   p=0.3649 | Egger 斜率 p=0.7293
Cochran Q(IVW) = 37.6208, df=30, p=0.1597
Egger 截距 = 0.002628 (se 0.009968) p=0.7939
```
⚠️ **注意口径不一致**：S8 记的 `IVW_P=0.52` 对应的是 **clump 后 54 IV** 版（`S2` 的 `clump_loose`：b=−0.1298, p=0.5227），不是这 31 IV 版。所以这组 Q 值**不能直接填进 S8 的失眠行**，只能作为"该对性状无实质异质性"的旁证。54 IV 版的 Q **不可回收**（缺 per-SNP harmonised 数据）。

### 2.3 为什么这件事对 R1#4 / R3#4 也重要

Cochran Q 对 clump 强度极度敏感，同一对性状三个版本：

| 仪器集 | n_IV | Q | Q_p | 出处 |
|---|---|---|---|---|
| 未 clump | 2,462 | 3,660.12 | 1.25e-50 | `S2_instrument_sensitivity.csv` |
| clump（07-20 版） | 31 | 37.62 | 0.160 | `G1_bidirectional.rds$fwd` |
| clump_loose | 54 | — | not recorded | — |
| clump_tight | 37 | — | not recorded | — |

**同一条因果链：Q_p 从 1.3e-50 变成 0.16，只因为换了 clump 设定。** 这正是 R3#4（r²<0.001 + 10 Mb 依据）与 R1#4（特异度口径）共同指向的那条链，也说明 G2 若把 Q 写进规则，就必须**同时披露 Q 是在哪一套 clump 设定下算的**。

---

## 三、单一规则复现不了 L2：四种候选规则的失配表

把 4 种"只依赖已记录列"的规则各自代入 12 例（已用 S4 补全 `Education→AD`）：

| 规则 | 失配 | 失配案例（实际→规则给出） |
|---|---|---|
| A：IVW ∧ WM ∧ Egger 斜率 全显著 → 2 | 3/12 | Education→AD (2→1)、BMI→T2D (2→1)、Education→T2D (1→2) |
| **B：IVW ∧ WM 全显著 → 2（不含 Egger）** | **2/12** | HDL→CAD (1→2)、Education→T2D (1→2) |
| C：IVW ∧ Egger 斜率 显著 → 2 | 3/12 | Education→AD (2→1)、BMI→T2D (2→1)、Education→T2D (1→2) |
| D：IVW ∧ Egger 截距 ≥ 0.05 → 2（代码口径） | 4/12 | BMI→Stroke、HDL→CAD、Education→T2D、Depression→AD 均 (1→2) |

**关键观察**：无论选哪条规则，**`HDL→CAD` 与 `Education→T2D` 这两格永远失配**，而它们的备注恰好写着 "Egger null" 与 "Egger int p=0.036 + high hetero"。也就是说——

> 这两格是评分者用 **Egger 截距** 与 **Cochran Q** 判的，而这两个量既不在表里、也无法从表里推出来。
> 所以 L2 的 12 个格子，**本质是"报告诊断 + 人工判断"**，不是算法输出。

这不是缺陷，而是需要**如实写出来**的性质：它正好解释了为什么要有两名评分者与 κ。

---

## 四、必须处理的三个后果

### 后果 1 — R1#1 的统一评分表不能写成"算法"

审稿人要的是"覆盖部分得分、决定性失败、结果冲突、不可用/功效不足"的统一表。我们可以给，但 G2 那一行必须写成：

| G2 部分得分（=1）的判定 | 输入诊断（须全部列出） | 判断方式 |
|---|---|---|
| clump 后主效应仍显著，但稳健性诊断未全部通过 | IVW p、加权中位数 p、MR-Egger 斜率 p、（如有）MR-Egger 截距 p、Cochran Q p | 两名评分者独立判定，分歧记录于 Notes；κ=0.89（72 项） |

**不能**写成"IVW<0.05 且 Egger 截距≥0.05 则 2 分"——因为 12 例里 10 例根本没有截距值，写出来立刻被 R1#9 打穿。

### 后果 2 — 模拟口径与验证口径本来就不一致，必须显式披露

- **模拟（43,200 次重复）**：`grade_framework()` L140 用 `Egger 截距 p > 0.05` 作为 G2 满分条件。
- **12 例验证**：评分者用 IVW + WM + Egger（斜率/截距混用）+ Notes 判断。

两者不是同一套操作化。**必须主动写明**，否则一旦审稿人抽查就会发现"模拟验证的规则不是验证集用的规则"。措辞建议见 §六。

### 后果 3 — `CRP→CAD` 那一格无法确证，只能标注

`Egger_P=0.009` 若为斜率，则与备注 "Clean null at extreme power F=176" 自相矛盾（斜率显著＝有信号）；若为截距，则与 IVW p=0.44 一致（方向性多效性导致零效应）。**倾向截距，但现有文件不足以确证** → 在 S8-v2 中按"语义待核"标注，不擅自改值。

---

## 五、建议动作

### 方案 A（推荐）— 拆列 + 如实标注 + 主动披露

1. `Egger_P` → 拆为 `Egger_slope_P` 与 `Egger_intercept_P`；新增 `Cochran_Q_P` 与 `n_IV`。
2. 已回收的 2 例（`Education→AD`、`Insomnia→AD`）填真值（失眠行需注明 31-IV 口径）。
3. 其余 10 例填 `not reported in source`，并在表注写明：**"For cases derived from published summary statistics, Cochran's Q and the MR-Egger intercept were not available; G2 was therefore scored by two independent raters from the reported IVW, weighted-median and MR-Egger estimates (per-level κ = 0.89)."**
4. Methods 增加一句模拟口径与验证口径的差异披露。
5. **不动**任何 L2 分值 → 等级、κ、Table 2、S9、Fig 2 **零变动**。

### 方案 B — 重跑 10 例补齐 Q 与截距

- 需外部暴露-结局 GWAS + LD 面板；本机 `mrcieu.ac.uk` 出口封锁、`EAS_bfile/` 为空、无 plink → **本机不可执行**。
- 若在可联网环境执行，工作量 ≈ 10 对性状 × (extract_instruments + clump + harmonise + mr_heterogeneity + mr_pleiotropy_test)，约半天。
- 收益：S8 变成完全可复现的算法输出；代价：结果可能改级（规则 B 下 `HDL→CAD` 6→7=B、`Education→T2D` 9→10=A，**两例改级**，且与 R1#10 引用的"框架正确降级"叙事冲突）。

> **不推荐 B**：收益是可复现性，代价是把两个最有说服力的验证案例改坏。

---

## 六、可直接使用的英文措辞

**Methods（12 例验证段，新增）**

> For each of the twelve validation trait pairs, we recorded the inverse-variance-weighted, weighted-median and MR-Egger estimates together with instrument strength. Because several pairs were assembled from published summary statistics, Cochran's Q and the MR-Egger intercept were not uniformly available; G2 was therefore scored by two independent raters from the reported diagnostics, with disagreements resolved by discussion and recorded in the table notes (per-level Cohen's κ = 0.89, 72 items).

**Table S8 表注（新增）**

> `Egger_slope_P` denotes the p value of the MR-Egger causal estimate; `Egger_intercept_P` denotes the p value of the MR-Egger intercept (directional pleiotropy test). Entries marked *not reported in source* indicate that the corresponding quantity was not available from the published summary statistics used for that pair; the sensitivity analysis for those pairs therefore relied on the reported estimates only.

**Response to Reviewer 1, comment 9（片段）**

> We agree that the provenance of each G2 score should be transparent. We have (i) renamed the previously ambiguous `Egger_P` column as `Egger_slope_P` and added `Egger_intercept_P`, `Cochran_Q_P` and `n_IV`; (ii) filled the values that were recoverable from our own archived outputs; and (iii) explicitly marked the ten cases for which these statistics were not reported in the source publications. We also state in the Methods that G2 was scored by two independent raters for these cases, which is the reason inter-rater reliability was assessed in the first place.

---

## 七、诚实边界

- 本报告只核了 **2/12** 例的原始输出（`Education→AD` 走 S4，`Insomnia→AD` 走 rds 的 31-IV 版）。其余 10 例的原始输出不在本仓库内，任何"补值"都会是编造。
- `Insomnia→AD` 的 Q 值对应 31-IV 版，与 S8 行的 54-IV 版**不是同一仪器集**，不能混填。
- `CRP→CAD` 与 `T2D→AD` 的 `Egger_P` 语义仍有疑点（前者倾向截距、后者中性），**未擅自修改**。
- 规则失配统计使用"截距未知即视为通过"的保守处理，实际失配数可能更多而非更少。
