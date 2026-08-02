# OSF 预注册计划 · 失眠 ↔ 阿尔茨海默病 共病 MR 研究

> **目的**：在跑数前于 OSF（Open Science Framework）锁定研究设计，防止 p-hacking / 选择性报告质疑，并作为投稿时的"预注册证明"。
> **对应文件**：`失眠-AD_三法整合设计.md` §八；`项目交接手册.md` §9-3。
> **状态**：本文件为可粘贴 OSF 的终稿。复制到 OSF 后锁定（freeze），此后不得修改分析设计。

---

## 0. 注册元数据（OSF 填写用）

| 字段 | 内容 |
|------|------|
| **OSF 项目类型** | Preregistration（非 OSF Project；Preregistration 专门用于跑数前锁定设计） |
| **注册标题** | Insomnia and Alzheimer's Disease: Causal Direction, Temporal Ordering, and Plasma Protein Mediation — A Triangulation Study Using Bidirectional MR, Colocalization, Two-Step Mediation, and Multistate Models |
| **注册人 / 通讯作者** | `[AUTHOR_NAME]`（占位，注册时填写） |
| **共同作者** | `[COAUTHORS]`（占位，注册时填写） |
| **机构** | `[INSTITUTION]`（占位） |
| **注册时间戳** | `[YYYY-MM-DD HH:MM:SS TZ]`（占位，OSF 自动生成；此处手动填写以备审计） |
| **OSF DOI** | `[DOI: 10.17605/OSF.IO/XXXXX]`（占位，OSF 锁定后自动分配，回填此处） |
| **OSF 项目链接** | `https://osf.io/XXXXX`（占位，注册后回填） |
| **关联数据仓库** | UKB 申请号 `[UKB_APPLICATION_ID]`（占位）；GWAS 汇总统计来源见 §3 |
| **关联代码仓库** | `code/00_config.R` ~ `code/03_multistate_onset.R`（已冻结版本） |
| **预注册协议** | 本文件全部章节 §1–§11，锁定后不可更改 |

> ⚠️ **锁定纪律**：OSF Preregistration 冻结后，若需修改任何分析设计（暴露/结局定义、协变量、方法顺序、敏感性清单、阈值），必须在 OSF 上发布修订说明（Revision Note）并记录修改原因。未声明的设计变更将被视为 p-hacking。

---

## 1. 研究问题（Research Question）

失眠与阿尔茨海默病（AD）之间的**因果方向、时序与血浆蛋白机制**是什么？
具体拆解：

- **方向（G1）**：失眠是否因果地增加 AD 风险（失眠→AD）？反向（AD→失眠）是否成立？
- **机制（G2）**：哪些血浆蛋白介导"失眠→AD"的因果路径？
- **时序与预后（G4）**：在真实人群中，失眠先发还是 AD 先发？失眠先发的共病者预后是否更差？
- **可推广性（G3，并行）**：上述 G1/G2 结论在东亚/华裔/日裔等非欧裔人群中是否复制？

---

## 2. 核心假设与三角验证逻辑

**三角验证（triangulation）**：G1（遗传方向）+ G2（分子机制）+ G4（临床时序）三独立证据源是否一致收敛。

**操作化判定标准**：
- **一致收敛（Concordant）** ⇒ 定义为以下三条同时成立：
  1. G1 正向 MR IVW P < 0.05 且反向 MR IVW P ≥ 0.05（方向=失眠→AD）；
  2. G2 至少 1 个蛋白间接效应 FDR < 0.05 且 coloc PP.H4 > 0.80（机制=该蛋白介导）；
  3. G4 经失眠先发路径（S0→S1→S3）的累积概率显著高于 AD 先发路径（S0→S2→S3），且分层生存 HR 的 95% CI 不跨 1（时序=失眠在前且预后更差）。
- **不一致（Discordant）** ⇒ 上述三条中至少一条不满足。不一致≠失败，而是纠偏型结论：失眠可能为 AD 临床前标记而非前因。

**不做**：不声称"治疗失眠可预防痴呆"——需干预研究验证，本设计仅提供因果与机制证据。

---

## 3. 暴露与结局定义（锁定）

| 角色 | 定义 | 数据来源（候选 ID，待 `00b_verify_gwas.R` 联网核验） |
|------|------|----------|
| 暴露（G1 正向 / G2） | 失眠（遗传工具：BenElsworth 2018 UKB 失眠 GWAS） | `ukb-b-3957`（EUR n=462,341，42 clumped IVs；原候选 ieu-a-1096=儿童肥胖、Jansen 2019 1.33M 不在仓库，已废弃） |
| 结局（G1 正向 / G2 step2） | AD（遗传工具：主对 Kunkle/IGAP；复制 Bellenguez 2022） | 主对 `ieu-b-2`（Kunkle 2019, ncase=21,982，非 UKB，与 ukb-b-3957 无重叠）；复制 `ebi-a-GCST90027158`（Bellenguez 2022, ncase=39,106） |
| 中介（G2） | 血浆蛋白 pQTL（~2,923，UKB-PPP / Olink） | UKB-PPP 发布源 / IEU |
| 个体级（G4） | 失眠/AD 发病时间、协变量、死亡 | UKB 申请字段（2245/2255、ICD-10 G47.0/F00/G30、死亡登记、APOE ε4） |
| 复制（G3，并行） | 东亚子集 / CHARLS / BBJ | 跨祖先（见 `G3跨祖先复制方案.md`） |

**GWAS ID 核验与回退策略（锁定）**：
1. 跑数前必须先运行 `00b_verify_gwas.R`，联网核验候选 ID 的样本量、人群、instrument 数。
2. 核验通过后写入 `code/gwas_ids_resolved.json`，`00_config.R` 优先读取该文件。
3. 若 `ukb-b-3957`（BenElsworth 2018 失眠）核验失败 → 回退至 Hammerschlag 2017 (ebi-a-GCST004695, 1 IV, 弱) 或 Mbatchou 2021 (ebi-a-GCST90013934) 重新核验；原 Jansen 2019 1.33M 已确认不在 OpenGWAS 仓库，不可作为回退。
4. 若 AD ID 无法在 IEU 解析 → 回退至 GWAS Catalog `GCST90012871`（Bellenguez 2022）或 Kunkle 2019（IGAP stage 1）。
5. 上述回退选择必须在 Results / Methods 中明确记录使用了哪个 ID 及原因。

---

## 4. 分析设计与顺序（锁定）

1. **G1 双向 MR + 共定位**（`01_bidirectional_mr_coloc.R`）
   - 正向：失眠→AD；反向：AD→失眠。
   - 主方法 IVW；敏感性：MR-Egger、加权中位数、加权众数、MR-PRESSO、留一法。
   - 报告 Cochran Q 异质性、Egger 截距。
   - Steiger 方向性过滤（排除因果方向颠倒）。
   - 共定位 `coloc`（失眠位点 ↔ AD GWAS，PP.H4 > 0.80 判显著）。
2. **G2 血浆蛋白两步中介**（`02_protein_mediation.R`）
   - Step1 失眠→蛋白 pQTL（b1）；Step2 蛋白→AD（b2）；间接效应 ≈ b1×b2。
   - 间接效应 SE 用 delta 法，P 值正态近似；~2,923 蛋白做 FDR 校正（Benjamini-Hochberg，< 0.05）。
   - top 候选蛋白用 `coloc` 复核（蛋白 pQTL ↔ AD 共享变异）。
   - 反向（AD→蛋白→失眠）证伪。
3. **G4 多状态发病顺序**（`03_multistate_onset.R`）
   - 状态：S0 健康｜S1 仅失眠｜S2 仅 AD｜S3 共病｜+ 死亡（吸收）。
   - 连续时间多状态 Markov 模型（`msm` 包）；年龄作时间尺度（左截断）。
   - 核心对比：经 `1→3`（失眠先发）vs `2→3`（AD 先发）到达 S3 的累积概率；到达 S3 后按进入路径分层的全因死亡生存（左截断 Cox 模型）。
4. **G3 跨祖先复制**（并行，见独立方案 `G3跨祖先复制方案.md`）：CHARLS / BBJ / 东亚 UKB 子集复制 G1/G2。

**分析顺序锁定理由**：G1 定方向 → G2 落机制 → G4 给时序，三者互为补丁。顺序不可互换（G2 依赖 G1 确认方向后才有意义；G4 时序验证依赖 G1 排除反向因果）。

---

## 5. 协变量（锁定，G4 多状态模型）

| 协变量 | 定义 | 编码 | 纳入理由 |
|--------|------|------|----------|
| age0 | 基线年龄 | 连续(年) | 时间常数协变量, 影响所有转移强度 |
| sex | 生物性别 | 0=女, 1=男 | 失眠与 AD 均有性别差异 |
| education | 教育年限或最高学历等级 | 连续或有序分类 | 认知储备, AD 保护因素 |
| depression | 抑郁状态 | 0=无, 1=有(或 PHQ-4 ≥ 2) | 关键混杂: 失眠↔抑郁↔AD 三角 |
| apoe_e4 | APOE ε4 携带数 | 0/1/2 | AD 最强遗传风险因子 |
| hypnotic_use | 安眠药使用 | 0=否, 1=是 | 药物本身有认知副作用(STORM 陷阱) |

（STORM 五视角强调抑郁与安眠药为关键混杂，必须纳入。）

---

## 6. 工具变量与质量控制（锁定）

- **clump**：r² = 0.001、kb = 10,000、MAF ≥ 0.01。
- **instrument 强度**：F > 10（敏感性升到 20）。
- **harmonization**：链向自动判定；allele 翻转统一；回文 SNP 剔除（默认 MAF > 0.45 保留）。
- **样本重叠处理（锁定）**：
  - 失眠主暴露 BenElsworth 2018（ukb-b-3957, UKB）与复制结局 Bellenguez 2022（含 UKB 子集）存在样本重叠；主对结局 Kunkle/IGAP（ieu-b-2, 非 UKB）与 ukb-b-3957 无 UKB 重叠。
  - **主分析**：使用无重叠组合（失眠 ukb-b-3957 × AD Kunkle/IGAP ieu-b-2）作为主因果对，Bellenguez 2022 作大样本复制并量化重叠程度。
  - **敏感性 1（重叠校正，仅作用于复制对）**：主对（ukb-b-3957 × Kunkle/IGAP ieu-b-2）无 UKB 重叠，无需校正；`MRlap` 仅在 Bellenguez 2022 复制对（含 UKB 重叠）上运行，报告重叠比例并校正样本重叠偏倚。
  - **敏感性 2（因果 vs 多效性区分，仅作用于复制对）**：`CAUSE` 仅在 Bellenguez 2022 复制对上运行，区分因果与共享遗传架构/水平多效性混杂（CAUSE 对样本重叠和水平多效性更鲁棒）。
  - 若 `MRlap`/`CAUSE` 运行条件不满足（如 instrument 数不足），必须在 Limitations 中披露。

---

## 7. 敏感性分析清单（锁定，方法学审稿生死线）

### G1 双向 MR
- MR-Egger 截距（水平多效性检验）
- MR-PRESSO 离群检测
- 留一法（leave-one-out）
- Steiger 方向性过滤
- 异质性 Q 检验
- 加权中位数 / 加权众数
- 共定位 PP.H4（每个显著位点）

### G2 蛋白中介
- 反向两步（AD→蛋白→失眠，证伪）
- 仅保留强 pQTL（F > 20）
- coloc 复核 top 蛋白（蛋白 pQTL ↔ AD GWAS 共享变异）
- 排除与失眠/AD 均多效的蛋白（PhenoScanner v2 检索）
- Steiger 方向过滤（step2 中蛋白→AD 方向验证）

### G4 多状态
1. 仅住院 ICD 失眠定义（替代自评，提高特异性）
2. 全因痴呆（F00–F03）替代 AD（F00/G30），扩大事件数
3. 逐一剔除 APOE ε4 / 抑郁 / 安眠药的似然比检验（LRT）
4. 竞争风险（死亡已作为吸收态内置；补充 Fine-Gray 模型对照）
5. 进入年龄分层（< 65 vs ≥ 65 岁）

### 全局（样本重叠）
- 以无 UKB 重叠的 AD 源（Kunkle/IGAP ieu-b-2）为主分析、含重叠的 Bellenguez 作复制
- `MRlap` / `CAUSE` 重叠校正与多效性区分**仅作用于 Bellenguez 复制对**（主对无 UKB 重叠，无需校正）——与 `01_bidirectional_mr_coloc.R` §4c 实现一致

---

## 8. 显著性阈值（锁定）

| 分析 | 阈值 | 检验类型 |
|------|------|----------|
| G1 MR（IVW / Egger / WM / Mode） | α = 0.05 | 双侧 |
| G2 蛋白中介（间接效应） | FDR < 0.05（BH 校正，~2,923 蛋白） | 双侧 |
| G4 双路径对比（转移概率） | α = 0.05 | 双侧 |
| G4 分层生存 HR | 95% CI 不跨 1 | 双侧 |
| 共定位 | PP.H4 > 0.80 | — |
| Instrument 强度 | F > 10 | — |

---

## 9. 预期结果与发表策略

- **主结果**：报告 G1 双向 MR + 共定位、G2 top 介导蛋白、G4 路径对比与分层生存。
- **三角一致**（§2 定义的三条标准全满足）→ 投稿遗传学/神经病学顶刊（如 *Acta Neuropathologica* / *Molecular Psychiatry* / *Biological Psychiatry*）。
- **三角不一致**（至少一条不满足）→ 纠偏型高分（失眠或为 AD 临床前标记），同样可投顶刊。**不一致结果将以与一致结果同等篇幅呈现，不做选择性报告。**
- **G3 跨祖先**作为并行增量，强化 generalizability，避免"全欧裔"短板被审稿人一票否决。
- **阴性结果处理**：若 G1 正向 MR 不显著（P ≥ 0.05），将如实报告为"未发现失眠→AD 的因果证据"，并在 Discussion 中讨论可能原因（功率不足、反向因果、多效性），**不进行事后亚组挖掘以寻找阳性子集**。

---

## 10. 局限（主动披露，写进 Discussion）

| 局限 | 缓解措施 | 残余风险 |
|------|----------|----------|
| 失眠 UKB 自评弱（vs ICSD-3 临床标准） | ICD 住院敏感性 + 遗传工具(独立于自评) | 自评可能低估真实效应 |
| 反向因果（AD 临床前→失眠） | G1 MR + Steiger + G4 时序三重缓解 | MR 假设若违反则仍残留 |
| 蛋白单时间点 | 遗传 MR 自带时间锚（配子→终生），不受横断限制 | 无法验证蛋白纵向变化 |
| 全欧裔（G1/G2） | G3 跨祖先复制作并行增量 | 若 G3 不可及则 generalizability 受限 |
| 样本重叠（ukb-b-3957 × Bellenguez 均含 UKB） | 主对用无重叠 Kunkle/IGAP + MRlap 校正 + 独立源(BBJ/G3)复制 | 校正后精度可能下降 |
| G4 事件数不足（AD 发病率低） | 全因痴呆扩样本敏感性 + 事件数预检查 | 若 < 50 例转移则 msm 不稳定 |
| "可改变靶点"叙事夸大风险 | 预注册锁定 + 诚实声明"需干预研究验证" | 读者/媒体仍可能过度解读 |
| Prevalent case 左截断(G4) | msm 自动条件于基线状态 | 基线前状态持续时间未知 |

---

## 11. 注册信息

- **平台**：OSF（https://osf.io）
- **项目类型**：Preregistration（冻结后不可修改分析设计）
- **注册时间**：分析前（跑数前），即 G1/G2/G4 任何一条 MR/模型结果产出之前
- **锁定内容**：本文件全部章节 §1–§11（暴露/结局/协变量/方法顺序/敏感性/阈值/发表策略）
- **关联材料**：
  - 代码：`code/00_config.R`、`code/00b_verify_gwas.R`、`code/01_bidirectional_mr_coloc.R`、`code/02_protein_mediation.R`、`code/03_multistate_onset.R`（冻结版本快照上传 OSF）
  - 设计文档：`失眠-AD_三法整合设计.md`、`G3跨祖先复制方案.md`
  - 图表骨架：`论文图表骨架_Fig1-5_Table1.md`
  - 数据：UKB 个体级（需申请号 `[UKB_APPLICATION_ID]`，占位）；GWAS 汇总统计来源见 §3
- **修订协议**：若跑数后发现需修改设计，必须在 OSF 发布 Revision Note，记录修改内容、原因及日期。未声明的变更视为 p-hacking。
- **审计追溯**：本预注册对应的 STORM 多视角批判性审计见 `STORM跑数前审计.md`。
