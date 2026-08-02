# 00b 数据核验清单 — 失眠 ↔ AD 共病因果研究（Phase 1）

- **核验人**：孟因之（MR 遗传专家）
- **核验日期**：2026-07-30
- **核验环境**：本机 R 4.5.2（`C:/Program Files/R/R-4.5.2/bin/x64/Rscript`）；`ieugwasr` / `TwoSampleMR` / `coloc` 均已安装且可加载
- **OpenGWAS 连通性**：✅ **本环境可达**（实时 `gwasinfo()` 成功返回三组数据元数据）。故 A、B、C 多数项已"联网实时核验"，而非仅本地推断。
- **上游依据**：`data/raw/数据完整性核验报告.md`（2026-07-21，完整性）、`data/raw/数据预处理报告.md`（2026-07-22，去重/坐标对齐）。本报告在其基础上做 GWAS 身份/样本量/重叠/panel 的**交叉复核**，并修正若干偏差。

---

## 总览结论（先给答案）

| 问题 | 结论 | 评级 |
|---|---|---|
| 锁定的 GWAS 组合（ukb-b-3957 + ieu-b-2 + Bellenguez alt）能否进入 G1？ | **条件性可进入**：身份与样本量均确认；但须先修正 ukb 的 N（905,011→462,341），且 Bellenguez 路径必须上重叠稳健方法 | 已确认 + 2 项"需修正" |
| 重叠程度是否足以要求 MRlap/CAUSE 校正？ | **是，且很强**：ukb↔Bellenguez 重叠 ≈ 87–92%；但 ieu-b-2（Kunkle）路径重叠≈0，可走标准 IVW | 已确认（估算） |
| UKB-PPP 是否覆盖 G2 关键蛋白（GFAP/NfL/CRP/IL-6）？ | **是，全部覆盖**（Olink Explore 3072 面板，文献确认） | 已确认（文献+面板设计） |

---

## A. GWAS ID 与样本量核验

**方法**：实时 `ieugwasr::gwasinfo()` 拉取三组数据元数据；本地 `.clean.tsv.gz` 文件头与 `n` 列抽样交叉核对；与上游预处理报告比对。

### A1. 失眠暴露 — `ukb-b-3957`（Jansen 2019 / UKB 失眠）

| 字段 | 实时 gwasinfo 值 | 本地文件 | 结论 |
|---|---|---|---|
| IEU ID | `ukb-b-3957` ✅ | 文件名一致 | 已确认 |
| trait | "Sleeplessness / insomnia" ✅ | — | 已确认 |
| build | HG19/**GRCh37** ✅ | clean 文件 GRCh37 | 已确认 |
| population | European ✅ | — | 已确认 |
| category | **Categorical Ordered**（有序分类，0–4 失眠评分） | — | 已确认 |
| **sample_size (N)** | **462,341** | clean 文件 `n` 列 = **905,011** ❌ | ⚠️ **不一致，需修正** |
| ncase / ncontrol | NA / NA | ncase、ncontrol 列为空 | 合理（非病例对照） |
| nsnp | 9,851,867 | 去重后 9,837,128 行 | 量级吻合 |
| unit | SD | beta 为该有序评分的 SD 单位 | 已确认 |

**关键判定**：
- **"病例比例"不适用**：`ukb-b-3957` 是 UKB field 3957 的有序分类失眠评分（0–4），属**定量/序数易感性性状**，无病例/对照拆分，故 `ncase/ncontrol = NA`。"病例比例"概念只适用于 AD（见 A2/A3）。失眠暴露 N=462,341 即全部欧洲裔 UKB 参检者。
- ⚠️ **需修正（重要）**：本地 `ukb-b-3957.clean.tsv.gz` 的 `n` 列被注入 **905,011**（上游预处理报告因 gwasinfo 当时 `sample_size` 为空、改用 SE 反推的"有效 N"）。实时 gwasinfo 现返回 **462,341**，且 462k 与 Jansen 2019 UKB 失眠亚样本量（~453–462k）吻合。**905,011 是 2× 高估，须改为 462,341**。对 IVW 点估计无影响（β/se 已正确），但**任何依赖 N 的方法（MRlap/CAUSE 重叠校正、coloc 方差项）都会失真**——必须在进 G1 前修正。

### A2. AD 结局（主）— `ieu-b-2`（Kunkle 2019 / IGAP）

| 字段 | 实时 gwasinfo 值 | 本地文件 | 结论 |
|---|---|---|---|
| IEU ID | `ieu-b-2` ✅ | 文件名一致 | 已确认 |
| trait | "Alzheimer's disease" ✅ | — | 已确认 |
| build | HG19/**GRCh37** ✅ | clean 文件 GRCh37 | 已确认 |
| sample_size (N) | **63,926** | `n`=63,926 ✅ | 已确认 |
| ncase / ncontrol | 21,982 / **41,944** | 21,982 / 41,944 ✅ | 已确认 |
| year / pmid | 2019 / 30820047 | — | 已确认 |
| 病例比例 | 21,982 / 63,926 = **34.4%** | — | 已确认 |

**关键判定**：样本量与本地文件完全一致。任务描述中"41,938 controls"为笔误，**实际为 41,944**（与 gwasinfo 及本地文件一致）。**Kunkle 2019 早于 UKB 纳入 AD GWAS，其队列（ADGC/CHARGE/IGAP）基本不含 UKB 个体 → 与 ukb-b-3957 重叠≈0**（见 B）。这是走标准 IVW 的"干净"路径。

### A3. AD 结局（备选/复制）— `ebi-a-GCST90027158`（Bellenguez 2022）

| 字段 | 实时 gwasinfo 值 | 本地文件（GRCh38 主 / GRCh37 dedup） | 结论 |
|---|---|---|---|
| IEU ID | `ebi-a-GCST90027158` ✅ | 一致 | 已确认 |
| trait | "Alzheimer's disease" ✅ | — | 已确认 |
| **build** | gwasinfo 标 **HG19/GRCh37**（IEU 已调和） | 本地 GWAS-Catalog 下载 **GRCh38**；已制备 GRCh37 dedup 版 | ⚠️ 见注 |
| sample_size (N) | **487,511** | 行内 `n_cases+n_controls`=85,934+401,577=**487,511** ✅ | 已确认 |
| ncase / ncontrol（gwasinfo） | 39,106 / 46,828 | — | ⚠️ **字段错位**（见下） |
| n_cases / n_controls（本地 TSV） | — | **85,934 / 401,577** ✅ | 已确认 |
| year / pmid | 2022 / 35379992 | — | 已确认 |

**关键判定**：
- **样本量确认**：总 N=487,511 与 gwasinfo `sample_size` 完全一致；本地文件逐位点 `n_cases=85,934`（= 39,106 临床诊断 AD + 46,828 proxy-AD）/ `n_controls=401,577`，与 Bellenguez 2022 原文设计一致。
- ⚠️ **gwasinfo 的 ncase/ncontrol 字段错位**：gwasinfo 返回 `ncase=39,106, ncontrol=46,828`，但 46,828 实为 **proxy-AD 病例**（非对照）。**权威值以本地 TSV 的 n_cases=85,934 / n_controls=401,577 为准**，勿用 gwasinfo 的 ncase/ncontrol。
- **build 注记**：gwasinfo 将 Bellenguez 标为 GRCh37，系 OpenGWAS 调和存储惯例；原始 GWAS-Catalog 释放为 **GRCh38**（上游预处理报告 meta.yaml 已确认）。本地已同时制备 GRCh38（全量 21,070,466 行）与 GRCh37 dedup（10,610,198 行）两版，坐标对齐无碍。G1 若经 OpenGWAS API 拉取则自动 GRCh37，与本地 GRCh37 版一致。
- **病例比例**：含 proxy 的总病例率 85,934/487,511 = **17.6%**；仅临床诊断 AD 为 39,106/487,511 = **8.0%**。

### A 项评级
**已确认**（身份/坐标/样本量均经实时 gwasinfo + 本地文件双重核对）；**2 项"需修正/需关注"**：(1) ukb 的 N 列 905,011→462,341；(2) Bellenguez 勿用 gwasinfo 错位的 ncase/ncontrol，用本地 TSV 值。

---

## B. Jansen（ukb-b-3957）↔ Bellenguez（ebi-a-GCST90027158）的 UKB 样本重叠

**结论：重叠极大（≈87–92%），必然违反标准两样本 MR 的"无样本重叠"假设 → Bellenguez 路径必须上 MRlap / CAUSE / MR-RAPS 等重叠稳健方法。**

### 估算方法与数据来源
- `ukb-b-3957`（失眠）本质是 **全部欧洲裔 UKB 参检者**（N=462,341），失眠评分为 UKB 基础问卷字段，覆盖几乎所有 UKB 个体。
- Bellenguez 2022 设计（原文 Stage I）：39,106 临床诊断 AD + 46,828 **proxy-AD（基于 UKB 父母痴呆问卷）** + 401,577 对照，总 487,511。其中：
  - **46,828 proxy-AD 病例 100% 来自 UKB**；
  - 401,577 对照中，EADB（15 个欧洲国家）贡献 22,244 非 UKB 对照，其余 **≈379,000 对照来自 UKB**；
  - 临床诊断 AD 病例（39,106）来自 EADB/ADGC/CHARGE 等临床队列，**非 UKB**。
- 因此 Bellenguez 的 UKB 成分 ≈ 46,828（proxy 病例）+ 379,000（UKB 对照）≈ **426,000** 个体。

### 重叠比例
```
重叠个体数  ≈ 426,000（既在 ukb-b-3957，又在 Bellenguez 的 UKB 子集）
重叠/失眠N  = 426,000 / 462,341 ≈ 92.2%
重叠/BellenguezN = 426,000 / 487,511 ≈ 87.4%
```
- **保守下界**：即便仅计 UKB proxy 病例 + 部分 UKB 对照（如 300k），重叠仍 > 65%。结论（重叠远超阈值）稳健。
- **精确值待精核**：建议从 Bellenguez 2022 **Supplementary Table 2**（各队列样本量）取 UKB 对照确切数，以收紧 426,000 的估计；但无论取何值，重叠均 > 60%，足以要求校正。

### 与 ieu-b-2（Kunkle）路径的对比（重要设计点）
- **ukb-b-3957 ↔ ieu-b-2**：Kunkle 2019 不含 UKB → 重叠 ≈ **0** → 标准 IVW / Egger / 加权中位数 可直接使用，无需重叠校正。
- **ukb-b-3957 ↔ Bellenguez**：重叠 ≈ 87–92% → **必须重叠稳健**：优先 **MRlap**（需暴露/结局 N 与近似遗传相关）或 **CAUSE**（区分因果 vs 混杂/水平多效性），并以 **MR-RAPS**（稳健 SE）作敏感性。

### B 项评级
**已估算（文献+设计推导）**，方向明确 → **需关注/必须校正**。重叠量级不因精确 UKB 数而动摇，故"是否需 MRlap/CAUSE"的答案为**强烈肯定（是）**。

---

## C. UKB-PPP panel 是否覆盖 G2 关键蛋白

**结论：GFAP、NfL、CRP、IL-6 全部在 UKB-PPP（Olink Explore 3072）面板内 → G2 四候选均可测。**

**面板事实**（Sun et al. Nature 2022/2023；UKB-PPP = Olink Explore 3072 PEA，54,219 UKB 参检者，2,923 独特蛋白，分 4 子面板：inflammation / oncology / cardiometabolic / neurology）：

| 蛋白 | 基因 | 子面板 | 覆盖 | 证据 |
|---|---|---|---|---|
| **CRP**（C 反应蛋白） | *CRP* | inflammation | ✅ 命中 | Olink 炎症面板标配；UKB-PPP 炎症网络分析常规包含 |
| **IL-6**（白细胞介素-6） | *IL6* | inflammation | ✅ 命中 | Olink 炎症面板标配细胞因子 |
| **GFAP**（胶质纤维酸性蛋白） | *GFAP* | neurology | ✅ 命中 | Buonocore & Fratto (J Neurol 2025) 明确以 **Olink Explore 3072** 在 UKB 测 GFAP；Wang et al. (BMC Med 2024)、Olink UKB-PPP 神经疾病综述均报告 UKB-PPP 内 GFAP |
| **NfL**（神经丝轻链） | *NEFL* | neurology | ✅ 命中 | 同上，Buonocore & Fratto (2025) 以 Olink Explore 3072 在 UKB 测 NfL；Wang et al. (2024) 以 Olink 在 UKB 测 NfL |

**方法说明**：本地无 UKB-PPP 蛋白清单文件（G2 脚本 `02_protein_mediation.R` 依赖的 `ukbppp_protein_gwas_index.csv` 尚未生成）。上述结论基于**已发表、使用完全相同 Olink Explore 3072 面板的 UKB-PPP 研究**，证据强度高；仍建议 G2 实际运行时对照本地 2,923 蛋白索引表逐条核对 Olink target ID（如 GFAP 的精确 target 名、NEFL）。

### ⚠️ G2 两步中介的"双重样本重叠"隐含风险（来自 02_protein_mediation.R §3 注释）
- Step1（失眠→蛋白）：暴露=ukb-b-3957（UKB），蛋白 pQTL=UKB-PPP（UKB）→ **重叠**；
- Step2（蛋白→AD）：蛋白 pQTL=UKB-PPP（UKB），AD=Bellenguez（含 UKB）→ **重叠**。
- 两步共用 UKB → delta 法 SE **低估**、P 值偏小、FDR 假阳性膨胀。
- **设计建议（缓解）**：
  1. **Step2 改用 ieu-b-2（Kunkle，无 UKB 重叠）作 AD 结局** → 直接消除 Step2 重叠（最优、零成本）；
  2. Step1 重叠用 **MRlap / bootstrap（R=1000）** 校正 SE；或换用非 UKB 失眠 GWAS（如 Jansen 2019 全 meta ~1.3M）降低 UKB 占比；
  3. 蛋白 pQTL 若有非重叠源（SCALLOP/AGA）作敏感性复制。

### C 项评级
**已确认（文献 + 面板设计）**；本地逐 target 复核留待 G2 运行时。GFAP/NfL 的覆盖是 G2 能落地机制分析的前提，已满足。

---

## D. 本地 clean 文件完整性复核

**方法**：`ls -la` 确认存在与大小；`zcat | head` 确认表头与字段；`zcat | head -100000 | wc -l` 抽样确认无截断/流式正常；`n` 列抽查；行数引用上游预处理报告（已逐 SNP 去重验证）。

| 文件 | 大小 | 表头（关键列） | 抽样流式 | 数据行数（去重后） | 结论 |
|---|---|---|---|---|---|
| `ukb-b-3957/ukb-b-3957.clean.tsv.gz` | 196 MB | `SNP CHR BP A1 A2 beta se p n ncase ncontrol` | 100k 行正常 | 9,837,128 | ✅ 存在/非截断 |
| `ieu-b-2/ieu-b-2.clean.tsv.gz` | 186 MB | 同上 | 100k 行正常 | 10,444,926 | ✅ 存在/非截断 |
| `ebi-a-GCST90027158/GCST90027158_buildGRCh37.dedup.tsv.gz` | 188 MB | `SNP CHR BP A1 A2 beta se p n_cases n_controls` | 100k 行正常 | 10,610,198 | ✅ 存在/非截断 |
| `ebi-a-GCST90027158/GCST90027158_buildGRCh38.dedup.tsv.gz` | 399 MB | 同上 | 100k 行正常 | 21,070,466 | ✅ 存在/非截断 |

> 任务描述假定四文件直接位于 `data/raw/` 下；实际位于 `data/raw/` 的对应子目录（`ukb-b-3957/`、`ieu-b-2/`、`ebi-a-GCST90027158/`）。路径已核对，文件齐备。

**行数合理性**：与上游预处理报告完全吻合（9.8M / 10.4M / 10.6M / 21M），量级合理，无空文件/截断。

**D 项需注意的细节（非阻断，供 G1/G2 脚本适配）**：
1. ⚠️ **ukb 的 `n`=905,011 错误**（见 A1），进入任何 N 依赖分析前须改 462,341。
2. ⚠️ **列名不一致**：ukb/ieu 用 `n/ncase/ncontrol`，Bellenguez 用 `n_cases/n_controls`。若 G1 脚本显式读 `n` 列，需兼容两种命名；MR 核心列（SNP/beta/se/p/allele）不受影响。
3. ⚠️ **ukb 用 UKB 风格 ID**（`10_100744250_C_T`）而非 rsID，而 ieu/ Bellenguez 用 rsID → 双向 MR / coloc 须按 **CHR:BP:A1:A2** 协调（文件均含 CHR/BP，可行；上游已提示此点）。

### D 项评级
**已确认**（四文件齐备、表头正确、流式无截断、行数与上游一致）。

---

## 最终裁决（回答任务三个核心问题）

1. **当前锁定的 GWAS 组合（ukb-b-3957 + ieu-b-2 + Bellenguez alt）是否可安全进入 G1？**
   → **条件性可进入（GO，附 2 项强制修正）**：
   - ✅ 三者身份、坐标（GRCh37 互通）、样本量均经实时 gwasinfo + 本地文件双重确认；
   - 🔧 **修正 1**：将 `ukb-b-3957.clean.tsv.gz` 的 `n` 由 905,011 改为 462,341（进 G1 前必做）；
   - 🔧 **修正 2**：Bellenguez 路径明确使用重叠稳健方法（MRlap/CAUSE/MR-RAPS）；ieu-b-2 路径走标准 IVW（无重叠）。

2. **重叠程度是否足以要求 MRlap/CAUSE 校正？（预期：是）**
   → **是，且很强**。ukb↔Bellenguez 重叠 ≈ 87–92%（~426k 共享 UKB 个体）；ukb↔ieu-b-2 重叠≈0。故 **G1 双 AD 源应分而治之**：Kunkle 走标准 IVW（干净参照），Bellenguez 走重叠稳健（主敏感性）。

3. **UKB-PPP 是否覆盖 G2 所需关键蛋白？**
   → **是**。GFAP、NfL、CRP、IL-6 均在 Olink Explore 3072 面板内（文献确认），G2 四候选均可测。另须注意 G2 两步中介的"双重 UKB 重叠"会使 delta 法 SE 低估——建议 Step2 改用 ieu-b-2 作 AD 结局以消除该重叠。

---

## 待办清单（交接主理人/下游）

- [ ] **修正 ukb N**：`ukb-b-3957.clean.tsv.gz` 全行 `n` 列 905,011 → 462,341（脚本 sed/awk 或重生成）。
- [ ] **G1 设计落地**：Kunkle(ieu-b-2) 标准 IVW + Egger + 加权中位数 + MR-PRESSO + 留一 + Steiger；Bellenguez 增加 MRlap/CAUSE + MR-RAPS 敏感性；共定位 coloc（PP.H4>0.8）。
- [ ] **G2 准备**：生成 `ukbppp_protein_gwas_index.csv`（2,923 蛋白 → 本地 pQTL 文件或 IEU ID，含 Olink target、n_samples）；Step2 优先用 ieu-b-2 消重叠；Step1 用 MRlap/bootstrap 校正。
- [ ] **精确重叠数**（可选精修）：从 Bellenguez 2022 Suppl Table 2 取 UKB 对照确切 N，收紧 426,000 估计（不影响"需校正"结论）。
- [ ] **列名兼容**：G1/G2 脚本兼容 `n/ncase/ncontrol` 与 `n_cases/n_controls`；失眠暴露按 CHR:BP:A1:A2 协调。

---
*复现：实时元数据核验见 `C:/Temp/iad_g1/00b_verify.R`（本环境 OpenGWAS 可达，可直接 `Rscript` 重跑）。*
