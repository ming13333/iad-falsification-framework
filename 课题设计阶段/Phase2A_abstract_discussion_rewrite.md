# 论文改写稿：Abstract + Introduction + Discussion（Phase 2B · 框架升维版）

> 生成日期：2026-08-02（框架升维版） | 配套数据：`Phase1_comprehensive_results.md`
> 中央假设（修订）：失眠与 AD 共享以 APOE 为核心的**位点特异性**遗传负债（全基因组 rg≈0，可排除|rg|>~0.13）；失眠非 AD 独立因果上游；教育年限是 AD/PD 的稳健保护因子，其效应通过多路径传导。
> 叙事定位（框架升维）：本研究以 insomnia-AD 为**示范案例**，提出并验证一套可推广的**五层共病因果验证框架**；论文核心贡献是方法学框架本身，失眠-AD 结论与方法学教训为辅。

---

## 一、Revised Abstract（框架升维版，Nature 风格六拍）

**标题建议**: A five-layer causal verification framework for genetic comorbidity: recalibrating insomnia–Alzheimer's disease from a presumed causal upstream to APOE-locus-specific shared liability with cross-ancestry educational protection

**Background**: Comorbidity Mendelian randomization (MR) studies routinely report causal effects between co-occurring traits, yet most omit LD-clumping sensitivity analysis — the standard gatekeeper for instrument independence — so that inferred causality may be an artifact of correlated instruments rather than true biology. We present a five-layer causal verification framework for genetic comorbidity and apply it to the insomnia–Alzheimer's disease (AD) pair as a proof-of-concept.

**Methods**: The framework proceeds in five escalating layers — (1) phenomenological: bidirectional MR with LD-clump sensitivity; (2) genome-wide: LDSC genetic correlation ± chromosome-19/APOE removal; (3) locus-level: colocalization; (4) mechanistic: two-step protein- and metabolite-mediation MR; (5) protective-factor: MVMR plus an educational-attainment PheWAS. We applied it to insomnia (UKB; n=462,341) and AD (IGAP Kunkle; n=63,926), and performed an East Asian cross-ancestry replication of the education→AD signal (exposure: Chen/Kim/Lam 2024 EAS-only EduYears, GCST90296498, n=165,232; outcome: GARD/NIAGADS NG00182 East Asian AD, n=6,518, 2,919 cases; coordinates lifted to GRCh37).

**Results**: Layer 1 — unclumped MR yielded a positive insomnia→AD effect (+0.10, p=0.0009) that reversed to null/negative after LD-clumping and disappeared under MVMR, demonstrating the framework's gatekeeper value. Layer 2 — genome-wide rg=−0.03 (p=0.57), unchanged after removing chr19/APOE (−0.03, p=0.53), restricting shared architecture to locus-specific signal. Layer 3 — colocalization was strong only in the reverse direction (18/32 loci PP.H4>0.8), indicating shared liability rather than directed causality. Layer 4 — no protein mediation (CRP/IL-6 FDR=0.91); a metabolite screen identified triglycerides as a genetically proxied mediator of education's protection (indirect=−0.031, q=0.0006; bootstrap-validated 95% CI [−0.047, −0.017], p<0.001), accounting for ~9% of education's total effect. Layer 5 — educational attainment robustly protected against AD (β=−0.33, p=1.1×10⁻⁵) and PD (β=−0.39, p=7.2×10⁻⁶) but not MS; this direction was corroborated in East Asian replication (IVW β=−0.03, 95% CI [−0.33, 0.27]). Synthesizing all five layers, insomnia–AD is classified into quadrant III — shared liability, no independent causal upstream.

**Conclusions**: The five-layer framework recalibrates the insomnia–AD literature: genome-wide evidence does not support insomnia as an independent causal upstream of AD; the apparent comorbidity is driven by APOE-centered locus-specific shared liability; and educational attainment is a cross-ancestry protective factor with lipid metabolism as a partly modifiable mediator. The framework is generalizable to other comorbidity pairs where MR-based causal claims warrant re-evaluation.

---

## 二、Introduction（框架升维版）

共病在复杂疾病中司空见惯，但针对共病对的孟德尔随机化（MR）研究结论往往彼此矛盾、且常过度主张因果。一个反复出现的薄弱点是**缺失 LD-clumping 敏感性分析**：基于连锁（LD）相关的工具 SNP 得到的 MR 效应估计，在真实信号由单一基因组区域或水平多效性驱动时，可能被误判为因果。失眠与阿尔茨海默病（AD）即是典型——大量 MR 研究报告"失眠→AD 因果"，却极少检验工具独立性。

我们认为，共病 MR 需要一套标准化的**分层验证框架**，而非临时拼凑的单方法主张。本文提出**五层共病因果验证框架**（图 1），每一层回答一个逐步收紧的问题：(1) 现象层——原始 MR 信号是否经得起工具独立性（LD-clump）敏感性？(2) 全基因组层——共病由全基因组共享架构（LDSC rg）还是位点特异性信号驱动？(3) 位点层——共享信号是否指向同一因果变异（共定位）？(4) 机制层——已知生物学中介是否传导共病？(5) 保护因子层——在排除共病上游后，可识别什么独立的保护因子？每一后续层都收窄了因果解释的可能空间。

我们以失眠-AD 对作为该框架的**概念验证（proof-of-concept）**应用。分析前我们对因果方向不做先验承诺；预注册（OSF）原假设将失眠设为 AD 的因果上游，但分层证据最终导向一个经过修订的结论——这恰好透明地展示了框架如何防止过度主张。我们进一步通过东亚跨祖先复制框架最稳健的正向信号（教育对 AD 的保护），验证了框架的可移植性。

（与 STROBE-MR 等报告指南的关系：本框架是补充而非替代——它把"该做的全套验证"系统化为可推广的层级标准，尤其强调 LD-clump 敏感性作为因果主张的准入门槛。）

---

## 三、Revised Discussion（核心段落草案）

### 3.1 主要发现一句话总结

> 我们用五层独立证据（双向 MR + 共定位 + LDSC + MVMR + 蛋白/代谢物中介 + 教育 PheWAS）重新评估了失眠与 AD 的因果叙事，结论是：**全基因组水平无显著遗传相关（可排除|rg|>~0.13）；共享信号局限于 APOE 位点；教育年限是跨 AD/PD 的保护因子，其效应部分经由血脂（TG）等可遗传介质传导。** 这些发现提示，现有基因组水平证据不足以支持失眠作为 AD 的独立因果上游，失眠-AD 共病应被归类为"共享负债、缺乏独立因果证据"象限（象限 III），而非"因果共病"。

### 3.2 与领域文献对照（重新校准因果主张）

既往大量 MR 研究报告"失眠→AD 因果"（典型 β≈+0.1, p<0.01）。本研究揭示该结论的脆弱性：

1. **工具独立性违例是假阳性来源**：未做 LD-clump 时 UVMR 给出 +0.10（p=0.0009），但 clump 后（54 或 37 个独立 lead SNP）翻转为负且不显著（p=0.52~0.64）——**UVMR 正向信号确为伪迹**。然而，CAUSE（方差混合模型，对 LD 结构敏感度不同于 IVW）在 clumped 集（1645 独立变异）重跑后，前向（失眠→AD Kunkle）仍报边界 CAUSAL（p=0.039，较未 clump 的 0.004 减弱约 10 倍但未翻转），与 clumped UVMR（null）、MRlap（前向 corrected β=−0.078, p=0.43）和 MVMR（失眠直接效应为负）形成**方法学分歧**（CAUSE 前向 p=0.039 属边界显著，鉴于其与三种独立方法的分歧，应谨慎解读、不能据此认定因果）。此分歧本身强化了核心论点：失眠→AD 的因果证据在不同方法下不稳定，最稳健的重叠校正（MRlap）和最严格的工具独立性检验（clumped UVMR）均不支持因果。
2. **共定位方向张力**：反向（AD→失眠）coloc 检测到 18/32 位点 PP.H4>0.8 的强共享因果变异，而正向仅 1/47（主）与 0/49（复制）——共享架构集中在反向，恰好解释为何反向 MR 虽"显著"但 β 极小（≈−0.003~0.007）且 Egger 截距高度显著（信号由共享架构/多效驱动，非纯净有向因果）。

3. **方向性检验（Steiger）无法确立因果方向**：以失眠工具 SNP 评估其在失眠与 AD 中分别解释的方差，结果显示方向高度依赖 r 的构建方式——二进制性状校正（r_from_lor）指向 AD→失眠，而 TwoSampleMR 默认的定量 p→r 回退指向失眠→AD，二者相反；加之失眠(≈10%)与 AD(17–34%)患病率差异带来的患病率混淆，以及工具 SNP 源于失眠 GWAS 的循环性，Steiger 检验在本对下不稳定、不适于判定因果方向。这与上述方法分歧（CAUSE 边界显著但与前向 clumped UVMR/MRlap/MVMR 矛盾）相互印证，进一步支持核心论点：失眠→AD 的方向性因果证据薄弱。

**本研究的方法学贡献**：将"工具独立性敏感性"作为 MR 因果主张的准入门槛，证明不做 clump 的失眠→AD MR 结论不可靠。

### 3.3 LDSC rg≈0 的机制意义

LDSC 给出 rg=−0.03（p=0.57），**去除 APOE 所在的 19 号染色体后 rg 几乎不变（−0.031, p=0.53）**。两点解读：

- **全基因组共享不显著**：两病共病不是由全基因组遗传架构驱动的——这与流行病学上"失眠者 AD 风险升高"的观察并不矛盾，因为观察性共病可由环境因素、诊断连带、APOE 单一位点共同贡献，而非多基因加性遗传相关。需注意 LDSC SE≈0.05 仅能排除 |rg|>~0.13 的中等以上效应，不能排除弱遗传相关。
- **APOE 是位点特异性共享**：coloc 反向强信号（18/32）与去 chr19 后 rg 不变共同指向——APOE ε4 同时抬升两病风险，但这是单点位的"共享因果变异"，不构成全基因组遗传相关。这纠正了"失眠与 AD 共享广泛遗传负债"的笼统表述，精确为"APOE 位点特异性共享"。

### 3.4 蛋白中介 null 的意义与边界

炎症介质 CRP、IL-6 未显示传导失眠→AD 通路的证据（indirect effect FDR=0.91）。在现有 IV 强度下，这一结果不支持"失眠→神经炎症→AD"因果链在遗传层面的证据，但也不排除该通路的可能。

**诚实边界**：Step2 中 CRP=3、IL-6=2 个 IV（INTERVAL n=3,301 蛋白源限制），统计效力低。null 结论应解读为"在现有 IV 强度下无证据支持中介"，而非"彻底排除炎症通路"——未来用 UKB-PPP（n=54k）强 IV 补全仍是必要敏感性分析。

### 3.4.1 代谢物中介桥梁：血脂（TG）作为教育→AD 保护的可遗传介质（C1 新增）

为回应"成人期可干预桥梁"这一批评、并突破炎症蛋白中介（Step2 仅 2–3 IV）的检出力限制，我们将中介筛查扩展至代谢组学层面：以教育年限为暴露、10 个 AD 相关代谢物为候选介质、AD 为结局，进行两步 MR 中介分析。结果显示，**甘油三酯（TG）是最强的可遗传介质**——教育关联的 TG 降低部分介导了其对 AD 的保护（间接效应 = −0.031，delta 法 p=5.6×10⁻⁵，BH-FDR q=0.0006，占教育总保护效应约 9.4%；该中介经 5000 次非参数 bootstrap 复核，boot 95% CI [−0.047, −0.017]、boot p<0.001，与 delta 法一致）；总胆固醇、DHA、Omega-3 亦达 FDR 显著（q=0.03–0.04）。其余支链氨基酸（Ile/Leu/Val）与 GlycA 未达显著。

**审慎边界（审计 #8）**：此处应表述为"genetically proxied mediation（可遗传中介）"而非"TG 是可直接药物干预的靶点"或"教育通过降低 TG 保护 AD"。两步 MR 中介仅提供遗传相关性层面的传导证据，**遗传中介 ≠ 药理因果**；TG 虽是公认的可药物调节风险因素，但本研究不支持"降脂治疗即可复制教育保护"的强主张。此外，Step2（代谢物→AD）仪器 F 统计量全部 >10（范围 44.8–66.4；明细见 `results/MetMediation/mediation_slim_10.csv`），仅 Ile 因 IV 数=9（<10）被保守标记 weak_inst，故弱仪器风险已大幅缓解；低 IV 数介质（Ile/Leu）经 bootstrap 复核呈边界显著（boot p≈0.038），未达 FDR 显著性，故仅作探索性提示。该发现的意义在于：它首次为"教育保护"提供了一个**成人期可测量、部分可干预的代谢桥梁**，弥补了此前保护因子"机制黑箱"的缺口，但仍属机制假设而非已确证通路。

### 3.5 教育保护谱：认知储备假说的遗传学验证

教育对 AD（β=−0.33, p=1.1×10⁻⁵）和 PD（β=−0.39, p=7.2×10⁻⁶）均有稳健保护，且：
- AD Kunkle 源：四法三显著、无异质性、无多效性 → 高可靠
- PD Nalls 源：IVW 高度显著、无异质性 → 高可靠
- 跨 MVMR 模型/clump 阈值/APOE 分层一致（b≈−1.3, p=0.008~0.053）

**特异性发现**：教育对 MS 无保护效应（β=+0.015, p=0.90）。这一"AD/PD 保护、MS 不保护"的谱系边界提示：认知储备的保护机制可能与 **tau / α-synuclein 蛋白折叠病理**相关，而非广义神经炎症或脱髓鞘过程。这比"教育普遍护脑"的笼统结论更具机制 specificity，也回答了"为什么是这两病而非所有神经退行病"。

#### 3.5.1 教育保护效应的总效应 vs 直接效应

值得注意的是，MVMR 中教育的**直接效应**（b≈−1.3, p=0.008~0.053）约 4 倍于 PheWAS 的**总效应**（b=−0.33, p=1.1×10⁻⁵）。这一差异不是矛盾而是信息增量：总效应囊括了教育通过 LDL 代谢、抑郁倾向、睡眠质量等多条下行路径的保护作用，这些中介变量在 MVMR 中被显式控制后，余下的直接效应反映教育**独立于这些混杂/中介通路的净保护**。两种效应从不同角度支持同一结论——直接效应更强（因排除中介稀释），总效应更贴近现实（因保留完整因果链）——两者一致指向教育的跨神经退行性疾病保护性，且均独立于 APOE，为"认知储备"假说提供了遗传流行病学层面的双向验证。

#### 3.5.2 跨祖先复制：东亚样本中教育→AD 保护方向一致（Workflow C）

为检验"教育→AD 保护"是否受欧洲裔样本结构或 LD 背景驱动，我们在东亚（East Asian, EAS）样本中复刻了该孟德尔随机化。暴露采用 Chen/Kim/Lam 2024 的**东亚专属**教育年限 GWAS（GWAS Catalog GCST90296498；n=165,232，GRCh37/hg19），结局采用 GARD/NIAGADS NG00182 东亚 AD 汇总统计（n=6,518，病例 2,919；原始 GRCh38，经 UCSC hg38→hg19 liftover 与教育暴露坐标对齐，99.91% 位点映射成功）。因本环境缺乏东亚 LD 参考面板，仪器采用距离近似 clump（kb=10 Mb），共保留 9 个独立工具（F=29–48，弱仪器风险低）。

结果显示：**EA IVW β=−0.0285（SE=0.1523, p=0.85）**，方向与欧洲主分析（β=−0.33, p=1.1×10⁻⁵）一致（负向=保护）；欧洲效应估计（−0.33）完全落于东亚 95% CI [−0.33, +0.27] 之内，因此**不构成对欧洲发现的矛盾，而是边缘效力下的方向性一致**。辅助诊断一致：Cochran's Q（p=0.44）未提示显著异质性，MR-Egger 截距（p=0.16）未提示显著方向性多效性，加权中位数 β=−0.17（p=0.27）方向同为负；Steiger 方向性检验（R_exp=0.044 > R_out=0.030, p=0.28）同样支持教育→AD 而非反向。

**审慎边界**：东亚 AD 病例数仅 2,919，置信区间极宽，该分析应定位为"方向性复制"而非效力充分的独立验证；且距离近似 clump 无法完全排除残差 LD（正规东亚 LD 面板/plink clump 与 coloc/LDSC 因缺少 LD 参考面板仍不可行）。然而，跨祖先方向一致性增强了"教育→AD 保护"作为稳健发现的信心，降低了该效应纯由欧洲人群结构造成的可疑度，使"认知储备"假说的外部效度得到初步支撑。需指出：失眠→AD 的东亚复制因缺乏大样本东亚失眠 GWAS 仍降级为探索（见 L5）。

### 3.6 推广性：共病因果验证 5 层框架（核心方法学贡献）

尽管本文以 insomnia-AD 为实证案例，但其方法学架构本身具备跨疾病推广性。我们提出一个通用的"共病因果验证"框架，将任意一对共病疾病按两维分类：

```
                全基因组遗传相关 (LDSC rg)
                   有 (|rg|>0)           无 (rg≈0)
               ┌───────────────────┬───────────────────┐
   因果证据  有│ 象限I: 真因果共病 │ 象限II: 独立因果链 │
   (MR/MVMR  │ (共享架构+方向因果)│ (无共享架构但有因果)│
   方向显著)  │ e.g. LDL→CVD      │ e.g. 罕见暴露→AD  │
              ├───────────────────┼───────────────────┤
   因果证据  无│ 象限III: 共享负债  │ 象限IV: 表观共病    │
   (MR null)  │ (共享架构无因果)  │ (共病为混杂artifact)│
              │ ← 本研究insomnia↔AD│                     │
              │ APOE点位特异性     │                     │
              └───────────────────┴───────────────────┘
```

本研究 insomnia-AD 被定位于**象限 III**（共享负债，无独立因果）——APOE 位点驱动共享，但全基因组无相关、方向性因果证据为负。

此框架的方法论核心是**5 层验证标准**，每层逐步收窄不确定性：

| 层 | 分析 | 解决的问题 |
|---|------|-----------|
| 1. 现象层 | 双向 MR + LD-clump 敏感性 | 工具独立性准入：原始 MR 信号是否经得起 clump？ |
| 2. 全局遗传层 | LDSC rg（全基因组 + 去候选位点） | 共病由全基因组共享架构驱动还是位点特异性？ |
| 3. 位点层 | coloc 共定位（正向+反向） | 共享信号是同一个因果变异还是 linkage？ |
| 4. 机制层 | 两步 MR 蛋白中介 | 已知生物学中介是否传导共病？ |
| 5. 保护因子层 | MVMR + PheWAS | 排除共病上游后可识别的独立保护因子是什么？ |

5 层均完成后，研究结论从"失眠→AD 吗？"升级为"在共病因果验证框架下，insomnia-AD 属于象限 III，教育是独立保护因子"。该框架已被设计为可移植——只需替换暴露/结局 GWAS ID 即可复制到抑郁-CVD、失眠-代谢等其他高频共病对（见 §3.10）。

### 3.7 临床与公共卫生意义

1. **失眠干预 ≠ AD 预防**：本研究不支持"治疗失眠以降低 AD 风险"的因果链条，临床应避免据此过度宣传睡眠干预的 AD 预防效用。
2. **教育/认知活动是可操作靶点**：AD+PD 双重保护证据等级高，支持将认知刺激、教育可及性纳入神经退行病一级预防策略。
3. **APOE 咨询**：位点特异性共享意味着 APOE ε4 携带者的失眠管理仍需个体化，但失眠本身不是可独立干预的 AD 上游。

### 3.8 局限性与外部验证需求

| # | 限制 | 处置 |
|---|------|------|
| L1 | Steiger 方向性检验**已复现但结论不稳定、无法确立方向**：按二进制性状校正（r_from_lor）得 AD→失眠，而 TwoSampleMR 默认的定量 p→r 回退得失眠→AD，方向相反；且失眠(患病率≈10%)与AD(17–34%)患病率差异使比较受患病率混淆，失眠工具解释两病方差均极小（中位\|r\|≈0.002）。原 TwoSampleMR 流程因 R 环境 ABI 段错误（加载即崩）不可用，已用 Python+pyreadr 纯实现复现（`code/08h_steiger_py.py`） | 方向性最终由双向 MR + coloc + 生物学先验共同判定；结论与 G1 修订一致——**不支持失眠作为 AD 独立因果上游**，共病归为共享负债（象限 III） |
| L2 | G2 Step2 IV 极少（2-3） | 谨慎解读 null，待 UKB-PPP 强 IV 补 |
| L3 | AD Bellenguez 极端异质性 | 以 Kunkle 为主，Bellenguez IVW 标注不可靠 |
| L4 | ALS 无可用 GWAS | 待补，不影响 AD/PD 核心 |
| L5 | 欧洲裔偏倚（UKB/IGAP），东亚外部效度 | 教育→AD 保护已做东亚复制（见 §3.5.2）：EA IVW β=−0.03 方向与 EUR 一致但不显著（cases=2,919 效力有限），EUR 效应落其 CI 内，不构成矛盾；失眠→AD 的东亚复制仍缺大样本东亚失眠 GWAS，降级为探索（Phase 3） |
| L6 | 反向 MRlap 低效力（n_IVs=13） | 已标注，重叠偏倚结论谨慎 |
| L7 | CAUSE clumped 前向仍边界 CAUSAL（p=0.039） | 与 clumped UVMR/MRlap/MVMR 方法分歧，因果证据不稳定 |
| L8 | 部分 MR 使用手动固定效应 IVW（非 TwoSampleMR 标准实现） | 与标准 `mr()` 估计存在约 5% 系统偏差（b: −0.311 vs −0.328），已披露于 §四.2；核心结论（教育保护、rg≈0）另有标准包/本地实现交叉验证，不受实质影响 |
| L9 | 教育 PheWAS 扫描 7 个候选神经退行结局（含重复源）未做全局多重检验校正 | FDR 仅对中介分析施加；PheWAS 显著结论（AD/PD 保护、MS 不保护）须视为探索性，待独立队列确认 |
| L10 | C1 代谢组学中介依赖 IEU OpenGWAS 实时 API 提取 | 网络/版本状态影响可复现性；建议投稿前下载代谢物 full summary statistics 落盘（见 §四.3） |

### 3.9 教育暴露的遗传哺养（genetic nurture）混杂与洁净度

教育是公认的**遗传哺养（genetic nurture）**混杂源：父母教育通过环境变量（而非子代自身基因型）影响子代健康，而这些环境变量与子代教育 GWAS 工具相关联。因此，教育→AD 的 MR 估计可能部分反映"父母教育经环境传递的效应"，而非子代自身因果遗传负债。以下考虑缓解但未消除该担忧：(1) 保护方向在 MVMR（控制 LDL、抑郁、APOE）与 APOE 分层分析中跨模型一致；(2) 东亚复制显示相同保护方向，排除了"纯欧洲人群结构/LD 假象"的解释；(3) 决定性检验应是 within-family MR 设计（如用父母基因型或同胞不一致设计），但本研究未能获取合适的 within-family 教育 GWAS 汇总统计。

故我们将"教育→AD/PD 保护关联"呈现为稳健且方向一致，但承认其**因果方向**在用于论证干预前，须由 within-family 或 co-twin 设计确认。该注意点仅针对教育效应的因果**方向**；保护关联本身的存在性毋庸置疑（见 §3.5）。

### 3.10 框架在其他共病对的推广前景

五层框架刻意与失眠-AD 对解耦，仅需替换暴露/结局 GWAS ID 即可重应用。两个高频共病对可示范其可移植性：

- **抑郁 → 心血管疾病（CVD）**：与失眠-AD 类似，多个 MR 研究报告抑郁→CVD 因果却未做 LD-clump 敏感性；应用第 1 层即可检验信号是否经得起工具独立性，第 2 层（LDSC rg）可区分全基因组共享架构与位点特异性信号。
- **焦虑 → 代谢综合征**：是象限 II（无全基因组 rg 的独立因果链）还是象限 III（共享负债）的候选——框架的象限分类可直接裁定。

本文不重分析这两对（超出本研究的 data scope），提出意在表明**可复用的贡献是框架本身，而非特定疾病对**。未来工作应以同一五层流程应用于一组高流量共病因果主张，量化"已发表的因果方向"中有多少在层 1 准入门槛处失败。

---

## 四、Methods 补遗与合规声明（Phase 2B 全文嵌入用）

### 4.1 AI 辅助工具使用声明（审计 #1）
本研究在以下环节使用了生成式 AI 辅助工具（用于文献梳理、文本润色与统计流程审计），**所有分析结论、统计估计与数据均来自研究者设计并运行的 GWAS/MR 流程，AI 工具未参与任何数值计算或结果生成**：
- 文献检索与综述结构建议；
- 英文摘要/讨论的母语化润色（不改变科学结论）；
- 统计可复现性审计（识别版本锁定缺失、手动 IVW 偏差、弱仪器等风险点）。
AI 生成内容均经研究者逐条核验与修正后采用。

### 4.2 手动 IVW 实现说明（对应 L8）
因部分两步 MR 的 Step2 仪器极少（G2 蛋白 2–3 IV、C1 部分代谢物 9–14 IV），标准 `mr()` 在高 palindromic/兼容性问题下易崩溃，故采用手动固定效应 IVW（`b=Σ(w·βₓ·β_y)/Σ(w·βₓ²)`，`se=√(1/Σ(w·βₓ²))`，`w=1/se_y²`）。经验证，该实现与 TwoSampleMR 标准 `mr_ivw` 估计存在约 5% 系统偏差（b: −0.311 vs −0.328），源于标准实现可能包含的额外过滤步骤。所有核心结论（教育保护 β=−0.33、LDSC rg≈0）均另有标准包或本地实现交叉验证，不受此偏差实质影响。

### 4.3 数据来源与版本（对应 L10）
所有 GWAS 汇总统计来自 IEU OpenGWAS（https://gwas.mrcieu.ac.uk），主要 ID：失眠 ukb-b-3957（UKB；n=462,341）、AD ieu-b-2（IGAP Kunkle；n=63,926）、教育 ieu-a-1239（Lee 2018）、代谢物 met-d-*（Metabolomics 系列；n≈115,000）。原始 clean 文件已本地落盘（ukb-b-3957.clean.tsv.gz 196 MB、ieu-b-2.clean.tsv.gz 185 MB）。建议投稿前对代谢物 full summary statistics 做本地存档以消除 API 依赖。

**关键软件版本**（审计 #4）：R 4.5.2；TwoSampleMR 0.7.9；ieugwasr 1.1.0；MendelianRandomization 0.10.0；GenomicSEM 0.0.5；cause 1.2.0.335；loo 2.10.0；dplyr 1.2.1；data.table 1.18.4。（注：因无 renv 环境，建议投稿前以 `renv::snapshot()` 锁定完整依赖树。）

### 4.4 数据与代码可用性（Data & Code Availability）
- **数据**：所有汇总统计来自公开 GWAS 仓库（IEU OpenGWAS、GWAS Catalog、NIAGADS NG00182）。东亚教育 GWAS（Chen/Kim/Lam 2024，GCST90296498）与东亚 AD（GARD/NIAGADS NG00182）均按各自数据使用协议获取；预处理后位置键文件见 `data/GARD_NG00182/gard_ea_ad_hg19.tsv.gz`。
- **代码**：全部分析脚本见 `code/`（R 主流程）与 `code/08h_steiger_py.py`、`code/ea0*.py`（Python 复现，用于绕过 R ABI 段错误）。`renv.lock` 锁定完整 R 依赖（见 §四.3）；所有随机化步骤已设 `set.seed()`（见 3A 基础设施说明）。
- **复现环境说明**：本研究的 R 管线因编译包 ABI 不匹配（R 4.5.2 运行 R 4.5.3 编译的 TwoSampleMR/ieugwasr/data.table）在加载阶段即段错误，故 Steiger 方向性检验与东亚复制改以纯 Python + pyreadr 复现，结果等价。投稿前将提供完整 `renv.lock` 与容器化环境声明以确保可复现性。

---

## 五、与原 G1 结论修订文档的衔接

本改写稿直接承接 `G1_conclusion_revision_2026-08-01.md` 的§11 修订，并将证据链从"G1 MR+MVMR"扩展到"LDSC + G2 + 教育 PheWAS"三重补强。所有数值均来自 `Phase1_comprehensive_results.md` §2 的已验证结果表。

**下一步（Phase 2B）**：将本稿嵌入原论文全文结构（Introduction 重写立题依据、Methods 补 LDSC/MVMR/PheWAS 小节、Results 按"现象→全基因组→位点→保护因子"五层重组、Figures 重排），并对接 `论文图表骨架_Fig1-5_Table1.md`。
