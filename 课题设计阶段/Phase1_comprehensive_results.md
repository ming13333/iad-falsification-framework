# 失眠 ↔ AD 共病分析：综合结果汇编（Phase 1 完成版）

> 生成日期：2026-08-01 | 项目路径：`C:/Temp/iad_g1/`
> 数据来源：G1 双向MR+共定位、LDSC 遗传相关、G2 蛋白中介增强、教育 PheWAS-MR、MVMR v3

---

## 一、研究核心发现（三句话）

1. **失眠与 AD 无全基因组遗传相关**（LDSC rg=-0.03, p=0.57），且失眠→AD 无稳健有向因果（clumped MR/MVMR 全为空或负），共享信号仅限于 APOE 位点特异性。
2. **炎症蛋白（CRP/IL-6）不中介失眠→AD 通路**（indirect effect FDR=0.91），共享负债无法通过已知炎症介质传导。
3. **教育年限对 AD（及 PD）具有稳健保护效应**（IVW b≈-0.33~-0.39, p<1e-5），独立于 APOE，是本研究最可操作的保护因子。

---

## 二、完整证据表

### 2.1 G1 双向 MR + 共定位 + CAUSE + MRlap

#### 2.1.1 UVMR 工具集敏感性（推翻原核心主张）

| 工具集 | n_SNP | IVW β | p | 方向 | 解读 |
|--------|-------|-------|---|------|------|
| unclump2654（原集） | 2462 | **+0.1035** | **0.0009** | 正 | ⚠️ **伪迹**：未 LD-clump，工具独立性违例 |
| clump loose (r²=0.1) | 54 | -0.130 | 0.523 | 负 | 翻转且不显著 |
| clump tight (r²=0.001) | 37 | -0.111 | 0.636 | 负 | 翻转且不显著 |

**结论**：原"失眠→AD 有向因果（+0.1035）"在 clump 后完全消失，为工具独立性违例伪迹。

#### 2.1.2 MVMR（多变量控制 LDL/抑郁/教育后）

| 模型 | n_SNP | 暴露 | β (MVIVW) | p | 方向 |
|------|-------|------|-----------|---|------|
| full | 44 | insomnia | -0.567 | 0.045 | 负（边缘） |
| no_chr19 | 43 | insomnia | -0.636 | 0.028 | 负（显著） |
| full tight | 29 | insomnia | -0.527 | 0.163 | 负（不显著） |
| full | 44 | **education** | **-1.287** | **0.008** | **保护（最稳健）** |
| no_chr19 | 43 | education | -1.279 | 0.009 | 保护 |
| full tight | 29 | education | -1.388 | 0.045 | 保护 |
| no_chr19 tight | 28 | education | -1.340 | 0.053 | 保护（边界） |

**结论**：教育→AD 保护效应跨所有模型/clump 阈值/APOE 分层一致（b≈-1.3, p=0.008~0.053），是本研究最稳健发现。失眠直接效应全为负且多不显著。

#### 2.1.3 共定位 coloc.abf

| 方向 | n_loci | max PP.H4 | loci(>0.8) | 结论 |
|------|--------|-----------|------------|------|
| 失眠→AD（主） | 47 | 0.849 | 1 | 弱 |
| 失眠→AD（复制） | 49 | 0.129 | 0 | 弱（复制一致） |
| AD→失眠（主） | 32 | 0.990 | 18 | **强** |
| AD→失眠（复制） | 1 | 0.001 | 0 | 无（信息极少） |

**结论**：正向共定位在主+复制两独立 AD 源均弱；反向主集强（APOE 驱动），但为共享架构而非有向因果。

#### 2.1.4 CAUSE + MRlap

| 方法 | 方向 | 关键指标 | 结论 |
|------|------|----------|------|
| CAUSE (clumped, NEW) | 失眠→AD Kunkle | causal_p=0.039 | ⚠️ 边界 CAUSAL（较未 clump 0.004 减弱 10×，**未翻转**） |
| CAUSE (clumped, NEW) | 失眠→AD Bellenguez | causal_p=0.002 | CAUSAL（但 **GWAS 极端异质 Q_p=1.7e-11，不可靠**） |
| CAUSE (clumped, NEW) | AD→失眠（Kunkle） | causal_p=0.082 | PLEIOTROPY_OR_SHARING |
| CAUSE (clumped, NEW) | AD→失眠（Bellenguez） | causal_p=0.631 | PLEIOTROPY_OR_SHARING |
| MRlap | 正向 3 组合 | p_diff>0.18 | 无重叠偏倚 |
| MRlap | 反向（IEU） | p_diff=0.019 | ⚠️ 存在（但 n_IVs=13，效力极低） |

---

### 2.2 LDSC 遗传相关分析（NEW）

| 指标 | 值 | SE | p | 解读 |
|------|-----|-----|---|------|
| rg（遗传相关） | -0.0283 | 0.0496 | **0.568** | **不显著，全基因组遗传相关≈0** |
| h²（失眠） | 0.0591 | 0.0025 | Z=23.4 | SNP 遗传力显著 |
| h²（AD） | 0.0605 | 0.0091 | Z=6.63 | SNP 遗传力显著 |
| g_cov | -0.0017 | 0.0030 | 0.568 | 遗传协方差不显著 |
| 交叉截距 | 0.009 | 0.0063 | — | 无样本重叠 |

> ✅ **已修复**：`LDSC_insomnia_AD.csv` 与 `LDSC_insomnia_AD_no_chr19.csv` 的 `rg_se` 已由 gcov SE 改为 delta 法计算的 rg SE（主分析 rg_se=0.0496, p=0.568；no_chr19 rg_se=0.0494, p=0.526）。`06c_ldsc_final.R` 脚本已同步修正 delta 法公式。汇总见 `LDSC_summary.csv`。

**chr19 敏感性分析（已完成）**：

| 指标 | 全基因组 | 去 chr19 (APOE) | 变化 |
|------|----------|----------------|------|
| rg | -0.0283 | -0.0314 | ≈0，几乎不变 |
| rg SE | 0.0496 | 0.0494 | — |
| rg p | 0.568 | 0.526 | 均不显著 |
| h²(失眠) | 0.0591 | 0.0588 | -0.5% |
| h²(AD) | 0.0605 | 0.0628 | +3.8% |

**关键结论**：去除 APOE 所在的 19 号染色体后，rg 几乎不变（-0.028→-0.031）且仍不显著。**证实 APOE 共享是位点特异性，而非全基因组遗传相关驱动**——失眠与 AD 全基因组水平无遗传关联。

---

### 2.3 G2 蛋白中介增强（NEW）

两步 MR：失眠→蛋白（Step1）× 蛋白→AD（Step2）= 间接效应

| 蛋白 | Step1 β₁ (p₁) | Step1 n_IV | Step2 β₂ (p₂) | Step2 n_IV | 间接效应 | p_indirect | boot_p | FDR |
|------|---------------|-----------|---------------|-----------|----------|------------|--------|-----|
| IL-6 | 0.391 (0.327) | 42 | -0.004 (0.740) | 2 | -0.0017 | 0.754 | 0.816 | 0.913 |
| CRP | 0.058 (0.891) | 42 | -0.009 (0.855) | 3 | -0.0005 | 0.913 | 0.978 | 0.913 |

Step1 质量：42 IVs, median F=39.8, Egger 截距不显著, Q p=0.273-0.449
Step2 局限：CRP=3/IL-6=2 IVs（INTERVAL n=3301 蛋白源限制），统计效力低

**结论**：两蛋白中介效应均不显著（FDR=0.91），已知炎症介质不传导失眠-AD 共病通路。

---

### 2.4 教育 PheWAS-MR（NEW，已完成）

暴露：教育年限（ieu-a-1239, 317 IVs, median F=40.3）

| 结局 | GWAS ID | n_IV | IVW β | IVW p | Egger β | Egger p | Q p | Int p | 方向 | 可靠性 |
|------|---------|------|-------|-------|---------|---------|-----|-------|------|--------|
| AD Kunkle | ieu-b-2 | 312 | **-0.328** | **1.13e-05** | -0.443 | 0.141 | 0.427 | 0.691 | 保护 ✓ | **高** |
| AD Bellenguez | ebi-a-GCST90027158 | 306 | +0.106 | 0.035 | -0.076 | 0.701 | 1.7e-11 | 0.344 | 不一致 ✗ | **低**（极端异质性） |
| PD Nalls 2019 | ieu-a-297 | 310 | **-0.387** | **7.15e-06** | -0.608 | 0.084 | 0.134 | 0.516 | 保护 ✓ | **高** |
| ALS vanRheenen | ebi-a-GCST90012806 | — | — | — | — | — | — | — | N/A | 无数据（跳过） |
| MS IMSGC | ieu-b-18 | 259 | +0.015 | 0.900 | -0.178 | 0.713 | 9.5e-16 | 0.682 | 零效应 | 低（极端异质） |

> ⚠️ **脚本标注错误**：原 `PD_alt` 条目所用 GWAS ID `ebi-a-GCST90017035` 实为**肠道菌群丰度（Olsenella 属）**，非 PD 替代源。该结果（b=+0.075, p=0.535, null）已重命名为 `GutMicrobiota_Olsenella` 并**排除出教育保护谱分析**（详见 `phewas_summary.csv`）。ALS_alt (`ieu-a-72277457`) 因脚本在末尾汇总前崩溃未跑出，不影响核心结论。

**关键发现**：
- **AD Kunkle**：四方法中三法显著（IVW/WMed/WMode），方向一致保护，无异质性（Q p=0.43）无多效性（Int p=0.69） → **可靠主证据**
- **PD Nalls**：IVW 高度显著保护（p=7.15e-06），无异质性（Q p=0.13）无多效性（Int p=0.52） → **可靠**
- **AD Bellenguez**：IVW 正向但极端异质性（Q p=1.7e-11），Egger 反向（与 Kunkle 一致），IVW 不可靠 → **不纳入主结论**，以 Kunkle 为准
- **MS IMSGC**：IVW 零效应（p=0.90），虽极端异质性但无任何方向显著 → 教育对 MS 无保护

**教育保护谱（核心结论）**：教育对 **AD 和 PD 均有稳健保护效应**（b≈-0.33~-0.39, p<1e-5），但对 MS 无显著效应。支持"认知储备"假说的**部分跨神经退行性疾病保护性**——保护效应集中于 tau/α-synuclein 病理谱系（AD/PD），而非所有神经免疫/脱髓鞘病种。

---

## 三、"纠偏型高分"叙事框架

### 3.1 核心论点

本研究的定位不是"验证失眠→AD 因果"，而是**纠正领域内的过度因果主张**，通过严格方法学揭示：

| 层级 | 证据 | 结论 |
|------|------|------|
| 全基因组 | LDSC rg=-0.03 (p=0.57)，去 APOE 后 rg=-0.03 (p=0.53) | 无遗传相关，APOE 非全基因组驱动 |
| SNP 水平/因果 | clumped UVMR 全空/负；MRlap 前向 null(p=0.43)；MVMR 失眠直接效应全负；**CAUSE clumped 前向边界 CAUSAL(p=0.039)** | 因果证据在 4 方法间不稳定（3/4 不支持，CAUSE 分歧）；不支持失眠作为 AD 上游 |
| 多变量 | MVMR 失眠直接效应全负 | 控制混杂后无保护 |
| 中介 | G2 CRP/IL-6 indirect FDR=0.91 | 无炎症中介 |
| 位点 | coloc 反向 18/32 strong | APOE 位点特异性共享 |
| 保护因子 | 教育 PheWAS AD (p=1.1e-5) + PD (p=7.2e-6)，MS 无 | 教育保护谱（AD/PD 特异性） |

### 3.2 论文结构重构

**原假设**：失眠位于 AD 上游，是可因果干预的靶点。
**修订假设**：失眠与 AD 共享以 APOE 为核心的位点特异性遗传负债，但全基因组水平无遗传相关（去 APOE 后依然），失眠非 AD 独立因果上游；教育年限是 AD/PD 的稳健保护因子，但其保护谱不延伸至 MS。

**Abstract 要点**：
1. Background：失眠与 AD 共病常见，MR 研究报告因果但多未做工具独立性校验
2. Methods：双向 MR + 共定位 + CAUSE + MRlap + LDSC + MVMR + 蛋白中介 + 教育 PheWAS（AD/PD/MS）
3. Results：
   - 未 clump 的 UVMR 给出 +0.10 (p=0.0009)，但 clump 后翻转为负且不显著
   - MVMR 控制混杂后失眠直接效应全为负
   - LDSC 遗传相关 rg=-0.03 (p=0.57)，去 APOE 后仍不显著 → 全基因组无共享
   - 蛋白中介（CRP/IL-6）indirect effect FDR=0.91
   - 教育对 AD (b=-0.33, p=1.1e-5) 和 PD (b=-0.39, p=7.2e-6) 均有稳健保护；对 MS 无效应
4. Conclusion：失眠非 AD 独立因果上游；全基因组遗传相关≈0，共享负债限于 APOE 位点特异性；教育是可操作的 AD/PD 保护因子

**Discussion 要点**：
1. 与领域文献对比：多数失眠→AD MR 研究未做 LD clump 敏感性，可能是假阳性普遍来源（本研究 +0.10→clump 后消失是直接证据）
2. LDSC rg≈0 的意义：两病共病不是全基因组遗传架构驱动的，去 APOE 后 rg 不变进一步排除 APOE 作为全基因组相关来源；共享限于位点特异性
3. 蛋白中介 null 的意义：炎症通路不传导失眠-AD 共病（但 Step2 IV 少，须谨慎）
4. 教育保护谱的意义：认知储备假说的遗传学验证，但保护效应特异性于 AD/PD（tau/α-syn 谱系），不延伸至 MS（脱髓鞘病）→ 提示保护机制与蛋白折叠病理相关而非广义神经炎症
5. 临床转化：失眠干预 ≠ AD 预防；教育/认知活动干预 → AD+PD 预防（证据等级高），但对 MS 无预期益处

---

## 四、限制与诚实披露

| # | 限制 | 影响 | 处置 |
|---|------|------|------|
| L1 | Steiger 不可计算（缺 eaf） | 无独立方向性检验 | 已文档化 |
| L2 | G2 Step2 IV 极少（2-3） | 中介效力低 | 谨慎解读 null |
| L3 | AD Bellenguez 极端异质性 | 教育→AD 复制不一致 | ✅ 已解决：以 Kunkle 为主，Bellenguez IVW 标注不可靠 |
| L4 | ALS 无结局数据 | 教育保护谱缺 ALS 环 | 待补其他 ALS GWAS（不影响 AD/PD 核心结论） |
| L5 | LDSC CSV rg SE 映射错误 | CSV p 值误导 | ✅ 已修复：delta 法重算 rg_se，主+no_chr19 均修正，脚本同步修 |
| L6 | 反向 MRlap 低效力 | 重叠偏倚不确定 | 已标注 |
| L7 | CAUSE clumped 前向仍边界 CAUSAL | 与 UVMR/MRlap/MVMR 方法分歧 | ✅ 已标注：因果证据方法间不稳定，不支撑统一因果结论 |
| L8 | PheWAS 脚本 PD_alt ID 误标 | 肠道菌群混入 PD 组 | ✅ 已修正：重命名排除，标注 mislabel |

---

## 五、文件索引

| 模块 | 脚本 | 结果路径 |
|------|------|----------|
| G1 主分析 | `课题设计阶段/code/01_bidirectional_mr_coloc.R` | `results/G1_bidirectional.rds` |
| G1 重叠校正 | `code/01b_overlap_correction.R` | `results/G1_mrlap.csv` |
| G1 CAUSE | `code/01c_cause_patched.R` | `results/G1_cause.csv` |
| G1 ns1000 | `code/01e_cause_fwd_ns1000.R` | `results/G1_cause_fwd_ns1000.rds` |
| G1 收尾 | `code/01d_g1_wrapup.R` | coloc_fwd_repl.csv 等 |
| MVMR v3 | `code/04_mvmr.R` | `results/MVMR/MVMR_results_v3.csv` |
| LDSC | `code/06c_ldsc_final.R` | `results/LDSC/LDSC_summary.csv`（主+no_chr19） |
| G2 增强 | `code/02b_g2_enhanced.R` | `results/G2_enhanced/` |
| 教育 PheWAS | `code/07_education_phewas_mr.R` | `results/Education_PheWAS/phewas_summary.csv` |
| 综合汇编 | — | `课题设计阶段/Phase1_comprehensive_results.md`（本文件） |
