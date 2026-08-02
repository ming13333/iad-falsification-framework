# AI Research Reproducibility Guard — 全流程审计报告

> 审计日期：2026-08-01 | 审计框架：ai-research-repro-guard v1  
> 审计范围：Phase 1（G1 MR+Coloc+CAUSE+MRlap+LDSC+MVMR+G2+教育PheWAS）→ Phase C（C3 CAUSE clumping + C1 代谢组学中介）

---

## 一、关键发现摘要

| 级别 | 数量 | 最严重问题 |
|------|------|-----------|
| 🔴 CRITICAL | 0 | 无不可修复的致命错误 |
| 🟠 HIGH | 4 | 版本锁定缺失、API 不可复现、手动 IVW 偏差 5%、C1 Step2 缺 F-stat |
| 🟡 MEDIUM | 5 | 宣称语言偏强、CAUSE p=0.039 解读需审慎、G2 Step2 检出力低、MVMR 缺 set.seed、PheWAS 未标注多重检验次数 |
| 🔵 LOW | 3 | 审计日志不完整、AI 工具需按期刊政策披露、G2 蛋白中介 Step2 仅 3 IV |

---

## 二、详细审计（按检查表逐项）

### 2.1 统计陷阱检查

| 检查项 | 状态 | 详情 |
|--------|------|------|
| 多重检验校正 | ✅ 大部分 | G2 FDR=0.913 ✓；C1 BH-FDR 4/10 ✓；PheWAS 7 结局未校正（⚠️ 需在 Limitation 标注） |
| FDR 边界值 | ⚠️ | C1 Total_C q=0.039、DHA q=0.045 → 边界显著，需附 bootstrap CI 确认 |
| 数据泄露 | ✅ 不适用 | GWAS summary-level 数据，无训练/测试泄露风险 |
| 假重复/批次效应 | ✅ 不适用 | 两样本 MR 设计，暴露/结局独立 |
| 排列检验下限 | ✅ 不适用 | 未使用排列检验 |
| 模型假设违反 | ⚠️ | CAUSE 前向 p=0.039 可能是模型误设（方差混合模型对 LD 结构不敏感）而非真实因果 |

### 2.2 数据完整性（n-drift / silent dropout）

| 检查项 | 状态 | 详情 |
|--------|------|------|
| UVMR 工具集 n-drift | ✅ 已披露 | 2462→54→37 SNP，98% 缩减是**分析核心发现**（伪迹论证）非 bug |
| G2 Step2 n-drift | ⚠️ 已知但弱 | CRP: 39→3 SNP；IL-6: 42→2 SNP → 中介检出力极低，已披露但仍需强调 |
| C1 Step2 n-drift | ⚠️ 未充分披露 | Ile 仅 9 IV、Leu 14 IV，Step2 结果可靠性低。**未标注 F-stat** |
| CAUSE n-drift | ✅ | 15564→1645 变异（89% 压缩），LD-clump 合理 |
| PheWAS n-drift | ✅ | 教育 317→~306 SNP（跨结局一致） |
| SNP 丢失原因追迹 | ✅ | 均因 palindromic/incompatible alleles，日志可见 |
| 样本量一致性 | ✅ | 暴露 n=462,341 (UKB)、结局 n=63,926 (Kunkle) 跨分析一致 |

### 2.3 代码正确性

| 检查项 | 状态 | 详情 |
|--------|------|------|
| LDSC rg_se 映射错误 | ✅ 已修复（最关键） | 原取 gcov SE (0.003)，导致 rg_p=1.2e-21 → delta 法修正为 0.05, p=0.57 |
| TwoSampleMR 方法名映射 | ✅ 已建立 | method_map 字典解决 "Inverse variance weighted" vs "IVW" |
| 手动 IVW 公式 | ⚠️ **有偏差** | 与 TwoSampleMR 标准 IVW 差 ~5%（b: −0.311 vs −0.328），因手工 IVW 为固定效应，标准 mr() 可能含额外过滤。C1 全部使用手工 IVW → **P1 需文档化** |
| G2 Step2 手动 IVW fallback | ⚠️ | CRP 3 IV、IL-6 2 IV → 手动 IVW 为唯一可行方案（mr() 崩溃），但 2-3 IV 的 IVW 极不稳定 |
| Steiger 方向性检验 | ❌ 数据源缺 eaf | IEU 不存 eaf 列 → 已文档化为 L1 限制 |
| CAUSE monkey-patch | ⚠️ 脆弱 | `assignInNamespace` 修改 cause 内部函数，依赖 loo 版本匹配。loo 升级后可能崩溃 |
| 代谢组学内联 IVW | ✅ | v3 诊断验证通过，防御性编写（is.finite + se>0 + tryCatch） |

### 2.4 宣称语言严谨度

| 检查项 | 状态 | 问题与建议 |
|--------|------|-----------|
| "失眠非 AD 独立因果上游" | ⚠️ 偏强 | 可改为 "insufficient evidence to support insomnia as an independent causal upstream of AD" |
| "TG 是可药物干预靶点" | ⚠️ 跳跃 | 遗传中介 ≠ 药理干预。应改为 "TG is a genetically proxied mediator and a known pharmacologically modifiable risk factor, suggesting lipid-lowering may partially contribute to the AD-protective profile associated with higher education" |
| "通过降低 TG 间接保护 AD" | ⚠️ 因果语言 | 中介 ≠ 因果机制。应改为 "education-associated reduction in TG partially mediates the protective genetic association" |
| "炎症通路不传导共病" | ⚠️ 过度排除 | 应改为 "no evidence supporting inflammation mediation"（G2 Step2 仅 2-3 IV，无排除效力） |
| "纠偏/推翻" 调门 | ✅ 已软化 | Phase2A 已改为 "重新校准" |
| 预测 vs 发现 | ✅ 适当 | 未声称 AI 预测/发现，均为 GWAS+MR 推断 |

### 2.5 可复现性基础设施

| 检查项 | 状态 | 详情 |
|--------|------|------|
| `set.seed()` | ⚠️ 部分 | G1 脚本有（20240721）；C1 slim 脚本无；MVMR(04) 无；07_phewas 无 |
| `sessionInfo()` 存档 | ✅ G1 有 | `results/G1_sessionInfo.txt` 已落盘（2026-07-30） |
| `renv.lock` 或 `environment.yml` | ❌ 缺失 | 无整体环境快照。依赖 R-4.5.2 + 手动安装包 |
| 包版本记录 | ⚠️ 部分 | 01c 记录 loo/cause 版本；其余脚本无 |
| Git 版本控制 | ❌ 未确认 | 脚本多次就地编辑，无版本控制历史 |
| 数据版本 | ⚠️ | IEU GWAS IDs (ukb-b-3957, ieu-b-2 等) 无下载日期/版本号 |
| 审计日志 | ⚠️ 部分 | 今日 daily log 覆盖关键决策，但部分运行输出被 grep -v 破坏 |
| IEU API 结果可复现性 | ❌ | C1 依赖在线 API，网络状态影响结果。**无法严格复现** |
| 原始 GWAS 数据 | ✅ | ukb-b-3957.clean.tsv.gz (196MB) + ieu-b-2.clean.tsv.gz (185MB) 本地保存 |

### 2.6 分析覆盖盲区

| 盲区 | 严重度 | 说明 |
|------|--------|------|
| **C1 Step2 仪器强度 (F-stat)** | 🟠 | 代谢物自身 IV 的 F 统计量未计算。Ile=9 IV / Leu=14 IV 弱仪器风险 |
| **教育 PheWAS 多重检验** | 🟡 | 7 结局无全局校正，需在 Limitation 标注 |
| **G2 蛋白中介反方向** | 🔵 | 仅测了失眠→蛋白→AD；未测 AD→蛋白→失眠（虽生物意义不大） |
| **教育 MR 的水平多效性** | 🟡 | 教育 PheWAS 中 MR-Egger 截距 p 值已报告，但未单独讨论教育 IV 的多效性敏感性 |
| **代谢物间共线性** | 🔵 | C1 中 Total_C/LDL_C/HDL_C 高度共线但作为独立中介分别分析。BH-FDR 部分缓解但未显式控制 |
| **中介效应占总效应比例** | 🟡 | 仅计算了 indirect/b_total  = −0.031/−0.33 ≈ 9.4%，但未给出 CI |

---

## 三、与项目记忆一致性校验

| 记忆条目 | 实际数据 | 一致性 |
|----------|---------|--------|
| "LDSC rg=−0.028 (p=0.57)" | CSV: rg=−0.0283, p=0.568 | ✅ |
| "教育 PheWAS AD b=−0.33 p=1.1e-5" | CSV: b=−0.328, p=1.13e-5 | ✅ |
| "MVMR 教育→AD b≈−1.3" | CSV: b=−1.310~−1.392 | ✅ |
| "CAUSE clumped Kunkle p=0.039" | CSV: p=0.03888 | ✅ |
| "C1 Total_TG indirect=−0.031 q=0.0006" | CSV: indirect=−0.03099, q=0.000565 | ✅ |
| "G2 CRP indirect FDR=0.913" | CSV: p_ind=0.913 | ✅ |
| "LDSC no_chr19 rg=−0.031 (p=0.53)" | CSV: rg=−0.0313, SE=0.0493 | ✅ |

**结论**：数值引用全部准确，无记忆漂移。

---

## 四、行动建议

### 投稿前必须完成（P0-P1）

| # | 动作 | 严重度 |
|---|------|--------|
| 1 | 在 Methods 声明 AI 工具使用范围（按期刊 SCI 政策） | 🟠 |
| 2 | 补充 C1 Step2 代谢物仪器 F-stat 并标记弱仪器（<10 IV 或 F<10） | 🟠 |
| 3 | 在 Limitation 披露手动 IVW 与标准实现 ~5% 偏差 | 🟠 |
| 4 | 补充 `renv.lock` 或至少列出所有包版本号 | 🟠 |
| 5 | 三个缺少 `set.seed()` 的脚本（04_mvmr.R, 07_phewas, 09b_slim）补充 | 🟡 |
| 6 | PheWAS Limitation 加入 "7 outcomes tested without global correction" | 🟡 |
| 7 | CAUSE p=0.039 解读加 "borderline, should be interpreted with caution given method divergence" | 🟡 |
| 8 | 软化 TG 中介的因果措辞（"genetically proxied mediation" 而非 "protects through"） | 🟡 |
| 9 | 在 Limitation 标注 IEU API 依赖 → 建议下载代谢物 full summary stats 落盘 | 🔵 |

### Revision 阶段可做（P2-P3）

| # | 动作 |
|---|------|
| 10 | 用 UKB-PPP 强 IV 替换 G2 弱 IV 蛋白中介（需 Synapse 审批） |
| 11 | 补全原始 GWAS eaf + Steiger 方向性检验 |
| 12 | 代谢物中介 bootstrap CI（非 delta 法渐近 CI） |
| 13 | 东亚 UKB/BBJ 复制（C2） |

---

## 五、总体评估

**论文科学严谨度**：8/10。Triangulation 设计扎实，关键 bug（LDSC rg_se）已修复，数值引用准确。主要风险集中在**可复现性基础设施不完整**（版���锁定、API 依赖）和**部分宣称语言偏强**。无致命错误，按行动建议修正后可投稿。

**最大风险**：如果审稿人要求独立复现，C1 代谢组学中介依赖 IEU API 实时请求 → 无法严格复现。建议在 revision 或投稿前下载代谢物 full summary stats 落盘。
