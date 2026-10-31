# Step 0 数字溯源报告（2026-10-27）

> 触发：D1 已裁定「接受"模拟=代理实现、结论收窄"」；D2 按「许可范围内充分披露 AI 使用」。
> 本报告只做溯源与核对，**不改任何稿件数字**；改动清单在 §四，等你确认后进 Step 3。
> 复现环境：Python 3.13.14 / pandas 2.2.3 / numpy 2.1.3 / sklearn 1.9.0（与投稿时一致）。

---

## 摘要（五条）

1. **marginal FDR 完全可复现**，口径 = 12 个参数格 cell-level FDR 的**等权均值**：balanced 0.0828→0.08、directional 0.1275→0.13；两组 range（0.042–0.125、0.081–0.183）与稿件**逐位一致**。⇒ 不需要改数字。
2. **但该统计量在主脚本里没有输出列**（`sim_framework_operating_chars.py` 的 marginal 聚合只写 sens/spec/p_gradeA–D）。已补 `code/sim_marginal_fdr.py`，产出 `sim_marginal_fdr.csv` + `sim_cell_fdr.csv`，把这条链补成可复现。
3. **正文两处 range 端点与它自己的 S9 矛盾**：sens@0.15（none）正文写 0.95–1.00，S9 最小 0.9250；P(A)@0.15（none）正文写 0.62，S9 最小 0.610。⇒ 要改两处数字（不影响任何结论）。
4. **G6 的 12 格里只有 2 格有据可查**（Education→T2D、Education→AD）。LDL→CAD、BMI→T2D、Height→CAD、HDL→CAD 四格在库内**没有任何外部验证记录**。严格按规则应归零，其中 **Height→CAD 会由 A 降为 B**（唯一改级）。
5. 🔴 **κ 的"第二位评分者"在仓库里不存在独立证据**：`code/interrater_reliability.py` 里 Rater 2 是硬编码数组，注释自承 "Deliberately stricter"，无评分人身份、无时间戳、无独立评分表。这一条只能由作者本人确认。

---

## 一、marginal FDR 溯源

### 1.1 三种口径全部算过

| pleio | pooled（全部 12 格合并） | **cell-mean（12 格等权均值）** | cell range | 稿件 | 判定 |
|---|---|---|---|---|---|
| none | 0.0000 | 0.0000 | 0.000–0.000 | 0.00 | ✅ |
| balanced | 0.0787 | **0.0828** | 0.0420–0.1255 | 0.08（0.042–0.125） | ✅ 与 cell-mean 一致 |
| directional | 0.1240 | **0.1275** | 0.0812–0.1828 | 0.13（0.081–0.183） | ✅ 与 cell-mean 一致 |

**判定**：稿件采用的是 **cell-mean**。若改用 pooled，directional 会是 0.124→0.12，与稿件 0.13 不符。二者差 0.004–0.006，不影响任何阈值判断，但**必须在 Methods 写死定义**，否则下一轮会被问"marginal 是哪种 marginal"。

### 1.2 其余边际量与 Table 2 逐位核对（12 格均值 vs 已发表）

| 量 | none | balanced | directional | 判定 |
|---|---|---|---|---|
| specificity（Grade D @β=0） | 1.0000 | 0.7963 | 0.6794 | ✅ 与 Table 2 的 1.000/0.796/0.679 一致 |
| sensitivity @β=0.08 | 0.5062 | 0.5267 | 0.5450 | ✅ 0.506/0.527/0.545 |
| sensitivity @β=0.15 | 0.9727 | 0.8473 | 0.8040 | ✅ 0.973/0.847/0.804 |
| P(Grade A) @null | 0.0000 | 0.0615 | 0.0462 | ✅ 0.000/0.061/0.046 |
| P(Grade A) @β=0.15 | 0.8754 | 0.7167 | 0.6673 | ✅ 0.875/0.717/0.667 |

⇒ **Table 2 与其正文叙述同源、可复现**；Table 2 与 S9 亦同源（S9 的 cell 值逐格等于 `sim_replicates.csv` 重算值）。

### 1.3 两处 range 端点错误（正文 vs 自己的 S9）

| 正文位置 | 现文 | S9 实测 | 应改为 |
|---|---|---|---|
| L100 `At the largest effect size … marginal sensitivity reached 0.97 (scenario range 0.95–1.00)` | 0.95–1.00 | **0.9250**–1.0000（最低格 = n_iv 20 / ld high / overlap 0.3） | **0.93–1.00** |
| L100 `marginal Grade A frequency … 0.88 at β = 0.15 (scenario range 0.62–1.00)` | 0.62–1.00 | **0.610**–1.000（最低格 = n_iv 20 / ld high / overlap 0） | **0.61–1.00** |

其余 range 全部正确：spec（balanced）0.770–0.835→0.77–0.84 ✅；P(A)@0.15（balanced）0.505–0.950→0.51–0.95 ✅；P(A)@0.15（directional）0.475–0.878（正文未给 range）✅。

### 1.4 新增产物

- `code/sim_marginal_fdr.py` —— 从 `sim_replicates.csv` 一次算出 cell/pooled/cell-mean 三种 FDR 与全部边际量，并与稿件值逐项比对打 `OK/DIFF`。
- `output/results/Simulation/sim_cell_fdr.csv`（12 格 × 9 列）
- `output/results/Simulation/sim_marginal_fdr.csv`（3 行 × 22 列，含 `pub_*` 对照列）

---

## 二、G6 跨祖先证据清点

### 2.1 逐例核对（依据 `Supplementary_Note_2_EAS_validation.md` + `data/raw/` 实盘）

| Case | S8 的 L6 | 库内记录的外部验证 | 可否支撑 2 分 |
|---|---|---|---|
| LDL→CAD | 2 | **无**（无任何跨祖先或独立队列分析） | 🔴 否 |
| Education→AD | 2 | EAS GARD：β=−0.029, P=0.85；Note 2 称 power ≥84% @ R²≥0.05 | 🟡 可，但须在表注写死 power 前提 |
| BMI→T2D | 2 | **无** | 🔴 否 |
| Height→CAD | 2 | **无** | 🔴 否 |
| Insomnia→AD | 0 | trans-ethnic 30 IV，power<6% → 不计分 | ✅ 一致 |
| BMI→Stroke | 0 | 无（但为 0，不影响） | ✅ |
| HDL→CAD | 1 | **无**；且二元规则下不存在 1 分档（Rater 2 亦给 0） | 🔴 否 |
| CRP→CAD | 0 | 无 | ✅ |
| BMI→AD | 0 | 无 | ✅ |
| Education→T2D | 2 | EAS BBJ：β=−0.145, P=0.012, F=35.5, WM 同向 | ✅ 有据 |
| Depression→AD | 0 | EAS 26 IV，underpowered | ✅ 一致 |
| T2D→AD | 0 | EAS GARD：β=+0.006, P=0.93（null 一致） | ✅ 一致（按规则仍 0） |

### 2.2 严格归零后的连锁后果

| Case | 原分/级 | 新分/级 | 说明 |
|---|---|---|---|
| LDL→CAD | 12 A | 10 A | 等级不变 |
| BMI→T2D | 12 A | 10 A | 等级不变 |
| Height→CAD | 10 A | **8 B** | 🔴 **唯一改级** |
| HDL→CAD | 6 C | 5 C | 等级不变 |
| 其余 8 例 | — | — | 不变 |

改级后 12 例分布：A 4→3、B 1→2、C 4、D 3。**Figure 5、Table S8、κ 输入、Results L118 的枚举句都要同步**。

### 2.3 顺带发现的文本/表不一致

正文 L118 写 "assigned Grade A to positive controls (**LDL–CAD, education–AD**)"，只列 2 例 A；而 S8 实有 **4 例 A**（另含 BMI→T2D、Height→CAD）。R1#9 要逐例透明度，这处必须改。

---

## 三、可回收数据盘点（决定 "not reported in source" 是否成立）

`data/` 实盘（3.1 GB）内容：

| 路径 | 内容 |
|---|---|
| `data/raw/ukb-b-3957` | 失眠 GWAS（EUR） |
| `data/raw/ieu-b-2` | AD GWAS（Kunkle） |
| `data/raw/ebi-a-GCST90027158` | AD 敏感性 GWAS（Bellenguez） |
| `data/raw/c1_cache` | 教育 / 代谢物两步中介的 harmonised 缓存（edu、DHA、GlycA…） |
| `data/processed` | GARD EAS AD（hg19）、EA 教育仪器与 harmonised |
| `raw/`（1.5 GB） | 上述三个 GWAS 的旧副本 |

**结论**：12 例中的 LDL、BMI、HDL、CRP、身高、T2D、卒中、抑郁、教育→T2D 等 **GWAS 从未在本地存在**，因此其 Cochran Q / Egger 截距**客观上不可回收**——"not reported in source" 成立，且原因应写明：**12 例是对已发表汇总统计的再评分（re-scoring of published summary statistics），不是本项目重新跑的分析**。这一句同时能挡掉"为什么你们自己的表里会有 not reported"的追问。

---

## 四、κ 的来源问题（最高优先级，须作者裁定）

`code/interrater_reliability.py` 的实际情况：

- L28–43 `r1_per_level`：Rater 1 的 72 个分值，硬编码。
- L53–66 `r2_per_level`：Rater 2 的 72 个分值，**同样是硬编码**，注释写着 *"Deliberately stricter on L3/L5/L6"*、*"L6: requires formal cross-ancestry check, not RCT/literature"*。
- 仓库内**没有**第二评分者的身份、评分日期、独立评分表或盲法记录。

复跑结果（与稿件一致）：grade κ = 0.7647、quadratic κ = 0.9412、per-level κ = 0.8941、raw agreement 10/12。

**问题**：正文 L77 写 "two independent raters scored all six gates … disagreements were resolved by consensus"，Results 报 κ=0.76–0.94。若第二位评分者并非独立人类，这处表述与事实不符；而 R1#9 恰恰在质疑 κ 的含义（"评分者一致性 ≠ 因果准确性"）。

三条可选处理（需你选）：

| 方案 | 做法 | 代价 |
|---|---|---|
| **K-a（推荐，若确无第二人）** | 改写为"primary scoring + 一次盲法复评（stricter reading）"，κ 改称 *scoring reproducibility*，不再称 inter-rater；保留 0.76/0.94 数值 | 需改 L77、L118、Table S8 表注、Figure 5 图注；R1#9 的"独立性"追问仍在，但至少表述真实 |
| K-b（若有真实第二人） | 补存评分表、身份与日期，声明归档；正文不动 | 需你提供证据 |
| K-c | 删除 κ 与"two raters"表述，只报逐例评分 | 失去一致性证据；R1#9 会问"为何不做" |

---

## 五、其他（次要但需一并修）

| # | 问题 | 处理 |
|---|---|---|
| 1 | 无 `requirements.txt` / `environment.yml`；稿件 L15 却称 "fully reproducible via `renv.lockfile`" | 补 Python 依赖锁定（numpy 2.1.3 / pandas 2.2.3 / sklearn 1.9.0 / Python 3.13.14）+ `renv.lockfile`→`renv.lock` |
| 2 | `sim_marginal.csv`（归档输出）无 FDR 列 | 归档 v1.2.0 内加入新脚本与新 csv，Methods 注明 marginal = 12 格等权均值 |
| 3 | Table 2 脚注只说 "reported as the range across the parameter grid"，未说 range 是 cell 级 | 表注补一句 "range = min–max across the 12 parameter cells" |

---

## 六、待你裁定（3 项）

| # | 事项 | 我的建议 |
|---|---|---|
| **A** | G6 四格是否按规则归零（代价：Height→CAD A→B，Fig 5 / S8 / κ 全部联动） | **归零**。R1#9 要"逐例证据"，无据保留比降一级更危险；而且"不可评估即 0 分"正是框架自己写定的规则 |
| **B** | κ 表述走 K-a / K-b / K-c | **K-a**（前提：确无独立第二人） |
| **C** | 两处 range 端点（0.95→0.93、0.62→0.61） | **照改**，纯转录错误，不影响结论 |

裁定 A/B/C 后进入 Step 1（两层 Table 1 + `rubric_spec_v3.csv`）与 Step 2（S8-v3 + 消融表）。
