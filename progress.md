# progress.md · 失眠↔AD 六门证伪框架

> 覆盖式更新 · **2026-10-30 21:20**（应答稿 22 条 + Table 2 重算 + 投稿 docx + 高亮版 + D3 标题 + Zenodo v1.2.1 + **第三方复核投喂包**；两处数值不一致已自查修掉）
> 续接口令：读 `RULES.md` + 本文件，接着干。详细历史见 `.workbuddy/memory/YYYY-MM-DD.md`。

---

## 当前项目

把"失眠 → 阿尔茨海默病（AD）有向因果"这一被反复报道的 MR 结论**证伪**，并把它升级为一套可复用的
**六门证伪框架**（association → robustness → genetic architecture → direct effect → biological mediation → external validation，0–12 分 → Grade A/B/C/D）。
失眠-AD 只作 proof-of-concept benchmark，**方法学框架才是主身份**。

- 标题（**D3 定稿 2026-10-28**）：*A six-gate falsification framework for diagnosing locus-driven confounding in Mendelian randomization: architecture, a 43,200-replicate benchmark of its scoring rule, and application to complex traits*
- 作者：Qin Liu^1,† · Wangyang Ye^1,† · Ming Luo^1,\*（温州医科大学附属第五医院/丽水市中心医院 神经外科）
- 核心结论：**失眠-AD = Grade C**（APOE 位点驱动的共享遗传负债，非独立上游因果）

### 一句话现状

**稿件 2026-09-02 投出，2026-10-22/23 两位审稿人意见已返回（共 22 条）。**
Manuscript ID **1986036**，Front. Genet. — Computational Genomics / Methods，编辑 Erika Salvi，Research Topic 73003。
**当前状态 = 应答期**：R1 十条（方法学审计型，末句 "I recommend major revision"）+ R3 十二条（澄清/技术准确性型）。
docx 内**无 Reviewer 2、无 Editor 决定信**。第一步产物已就绪 → `reviews/`（投喂包 + 提示词 + 生成脚本）。

---

## 投稿链（5 连 desk reject → 第 6 次投出，现审稿中）

| 日期 | 期刊 / 编号 | 结果 | 理由（编辑原话要点） |
|------|------------|------|--------------------|
| 2026-08-06 | Nature Communications `NCOMMS-26-064753` | desk reject（Leia Judge） | advancement / breadth / timeliness 不足；**明写"不质疑科学性"** |
| 2026-08-12 | Genome Medicine | desk reject（Gabriele Alfarano） | "findings fall short of broad-interest new insights"；主动推荐 transfer 至 BMC Medical Genomics |
| 2026-08-15 | Human Genomics | desk reject（Rituparna Bose） | "does not meet the standards or rigor required for MR studies" |
| 2026-08-26 | Scientific Reports | desk reject | 模板句"not sufficiently valid or original"，但关键词误配为 *extreme polygenicity*（疑似 AI 初审关键词错判） |
| 2026-09-01 | PLOS ONE `PONE-D-26-42927` | 第 5 次拒稿（Nikita Gupta） | **首次技术理由**：缺 power calc / PheWAS / STROBE-MR（PLOS 对 MR 稿的半自动硬筛查） |
| **2026-09-02** | **Frontiers in Genetics `1986036`** | ✅ **投出成功，Review ongoing** | Methods / Computational Genomics / RT 73003；编辑 Erika Salvi；截至 10-19 在审 **47 天**，无报告返回 |

**模式识别（重要）**：前 4 次 = 新颖性/广度不匹配（综合刊定位问题）；第 5 次 = 技术清单缺项。
两条应对都已落地：① 叙事升维为"方法论框架 + 43,200 模拟基准"；② P0/P1/P2 技术缺口全部补齐。
**第 6 次（Frontiers Methods）成功穿过编辑初筛**——说明"方法学体裁 + 专刊 scope 对口"这条路走对了。

---

## ✅ 已完成

### A. 科学结论（已固化，勿再改口径）

- **UVMR 工具敏感性**：未 clump 时 β=+0.104（P=9.3×10⁻⁴，伪精确）→ LD clump 后 **β=−0.130（P=0.52）翻转为 null**。正向信号是 clumping artifact。
- **遗传架构**：全基因组 r_g=−0.028（P=0.57）；去 APOE 区 −0.031（P=0.53）→ **rg≈0 但位点特异性共享强**。
- **共定位不对称**：正向弱（1/47 主），**反向强（18/32 主）** → 共享变异更像"AD 侧驱动"。
- **直接效应（MVMR）**：失眠直接效应为负、不显著；教育→AD **β≈−1.29（P=0.008）** 保护。
- **中介**：36 靶向蛋白 + CRP/IL-6 两步 MR **全 null**（indirect FDR=0.91）；教育保护部分由 **TG 中介**（indirect β=−0.031，q=5.7×10⁻⁴）。
- **跨祖先**：EAS 失眠→AD β=−0.84（P=0.28，方向一致，power<6%）；教育→AD EA 复制 β=−0.029（P=0.85），CI 含 EUR。
- **12 病例验证**：框架在 12 个 trait pair 上分级合理（S8）。

### B. 模拟基准（43,200 replicates，seed 20260804）

- 设计：3 pleiotropy 模式（none / balanced / directional）× LD 浓度 × 效应量（β=0/0.08/0.15）× 仪器数（20/60）× overlap（0 / 0.30）。
- **null 无多效**：specificity **1.00**，FDR **0**。
- **balanced**：marginal specificity ≈0.80，marginal FDR ≈0.08（场景 0.04–0.13）。
- **directional**：FDR ≈0.13（0.08–0.18）。
- **敏感度**：β=0.15 无多效时 **marginal 0.97（场景 0.95–1.00）**；Grade A 占比 0.88（0.62–1.00）/ balanced 0.72（0.51–0.95）。
- **2026-09-02 修掉的口径 bug**：`sim_operating_chars.py` 原按场景池算 sens 再写入每个 effect 行（β=0.08 与 0.15 同值）→ 已改 effect 级 `(A+B)/400` 重算，S9 全表覆盖。
- 复现性：43,200 重跑 27s，三输出文件**逐位 IDENTICAL**（numpy 2.1.3 / pandas 2.2.3 / Python 3.13.14）。

### C. 稿件（Frontiers Methods 路线，终态）

- **主稿**：`课题设计阶段/manuscript_Frontiers_Methods_v2_humanized.md`（55,953 字符，≈5,900 词含参考文献）
- **投稿 docx**：`课题设计阶段/manuscript Frontiers 0902.docx`（md5 `97378c3b…`，Table 1 已压成 7×4 紧凑版）
- **PDF 预览**：`课题设计阶段/manuscript Frontiers 0902.pdf`
- 规格合规：Abstract **305 词** ≤350；5 图 + 5 表 = 10 ≤15；A-type Methods ≤12,000 词；章节序 Declarations → References → Figure legends → Tables（Frontiers 规范）；参考文献 **42 条，全含 DOI**（孤儿引用问题已通过"裁到正文实际引用"解决）。
- 已做：去 AI 痕迹（em-dash 清零、句长收敛、AI 高频词清零）、数值 multiset 跨文件零差异、`$` 残留 0、作者上标保留。
- **AI 声明**：已按用户指定填 "GLM and DeepSeek, accessed through the WorkBuddy agent environment"（不写版本号，避免编造）。

### D. 图表（投稿就绪）

- `课题设计阶段/figures_final/`：5 主图 × **PNG + SVG + JPG + TIFF(LZW/RGB)** + `Frontiers_Figures_upload.zip`（3.1MB，5 TIFF）。
- 物理宽度全部合规（19.0–19.6 cm；dpi 元数据已修：Fig1 800 / Fig2 600 / Fig3 875 / Fig4 600 / Fig5 800）。
- Fig2（模拟操作特征）与 Fig4（APOE 共享负债）于 09-02 按 nature-figure 契约**重画**（NMI pastel 冷色系、hero callout、状态圆点替代大色块）。
- Fig1 为 a/b 双面板（六门框架 + 传统管线对比），SVG 由 6000×6317 组合图 clipPath 裁切上半得到。

### E. 补充材料

- `课题设计阶段/Supplementary_final/`（21 文件，209 KB）：`Supplementary_Tables.xlsx`（S1–S9 九 sheet，编号已对齐）+ Note 1 / Note 2 + `S5_Checklist_STROBE-MR.docx` + S1–S9 单表 csv/md 源。
- **S1–S9 编号错位已修**（原磁盘 S1–S8 与稿件 S1–S9 在 S7 分叉）；错误编号残留文件已删（有备份）。

### F. 仓库与归档

- GitHub `ming13333/iad-falsification-framework` main = **`3225fea`**（2026-09-02 10:39，36 文件 / 8289 行），内含 `manuscript/`（docx+md+figures+supplementary）、`code/`、`docs/`、`results/`。
- Zenodo **10.5281/zenodo.21858125 = v1.0.0（2026-08-09）**，即稿件六处引用的版本 DOI；v1.1.0 = 未引用的 22064685（08-23）；概念 DOI = 21858124。**v1.2.0 待补发**。
- `git push` 静默挂死已**根治**（移除 system 级 `credential.helper=helper-selector`，只留 GCM 主程序）。

### G. 基础设施（长期可用）

- gemini-web2api-bridge（gemini-3.1-pro @ 127.0.0.1:8081）、chatgpt-bridge（@ 10531）均已跑通。
- 已知教训：**别让 LLM 二次"压缩/改写"自己的输出** —— 09-02 压缩 Contribution 时模型编造了不存在的 R 包 "LocusFilter"、AUC=0.97、43,200 trait pairs 并翻转 β 符号，整段弃用。

### H. 投稿（已投出，在审）

- **Manuscript ID `1986036`**，2026-09-02 收稿，Front. Genet. — Computational Genomics，Methods 体裁。
- Research Topic **73003**（"Bioinformatics and Statistical Genetics Analyses for Omics-Based Dissection of Complex Traits"），编辑 **Erika Salvi**。
- 系统状态：**"Review is ongoing"**，明确 "NO ACTION IS REQUIRED FROM YOU"。
- 关键词已按投稿系统口径录入（Alzheimer's disease / APOE / Benchmarking / causal inference / Falsification framework / locus-driven confounding / Mendelian randomization / Operating characteristics）。

---

## 🚧 待解决 / 关键未知

### 1. 审稿应答（**当前最高优先级**）
22 条意见已拆解：**P0 4 条**（R1#1 评分表统一 / R1#2 代码↔Methods / R1#3 增量价值 / R1#4 sens·spec 定义）、
**P1 10 条**（需补数字或方法学论证）、**P2 8 条**（澄清与格式，可批量）。
- **未决前置**：R1#2 须核对 Zenodo 归档代码与 Methods 描述的实际差异 → 不自查则整条无法回应。
- **未决前置**：R1#1 根源已定位 = `S8` 用 1 分制而 Table 1 脚注写"仅 0/2 分"（K1）；列头 `L1–L6` vs 正文 `G1–G6`（K2）。
- 应答包与提示词见 `reviews/`；**改稿后必须重跑** `python reviews/make_review_packet.py` 刷新行号。

### 2. 旧预案命中率复盘（2026-09 预设的 6 类问题 vs 真实意见）

| 预设问题 | 是否命中 | 真实落点 |
|---|---|---|
| ① 新颖性 / 与 CAUSE·MRlap·coloc 的区别 | ✅ 命中 | **R1#3**（要求三路对照 + 序贯加门/逐一去门） |
| ② 模拟 DGP 真实性 | ✅ 命中且**严重升级** | **R1#2**（不是"真实性不足"，而是"代码与描述不符"）+ R3#9（参数依据） |
| ③ Grade 阈值合理性 | 🟡 部分 | 阈值本身**未被质疑**，被质疑的是**评分制式**（R1#1、R1#4）——与预设方向不同 |
| ④ 是否过度否定既有文献 | ❌ 未出现 | 无人质疑；R1#7 反而指出"三个 null"用词不准确 |
| ⑤ 单 benchmark 普适性 | 🟡 部分 | **R1#9** 要求 12 例逐例给出参考标签与支持门证据 |
| ⑥ κ=0.76 评分流程 | 🟡 部分 | **R1#9** 指出 **κ 是评分者一致性、不是因果准确性** |

- **未预测到的新增打击面**：评分体系内部矛盾（R1#1/#4）、sens/spec 统计定义（R1#4）、EAS 用 EUR LD 面板（R3#3）、跨祖先功效与偏倚（R3#7）、方法定位混乱（R3#8）、表格格式（R3#12）。
- **弹药仍在**：`课题设计阶段/Supplementary/Sensitivity_Note_Thresholds.md` 现直接对应 **R3#4**（r²<0.001 + 10 Mb 的依据）。
- ⚠️ G4 多状态时序、EAS 失眠→AD 两大软肋**未被本轮审稿人点名**，不要主动引入。

### 3. Frontiers 交互式审稿机制（需提前对齐）
- 审稿人**姓名对作者公开**，作者可在系统内实时回复，不是传统 blind review。
- 需确认三位作者（Qin Liu / Wangyang Ye / Ming Luo）是否接受署名互动；通讯作者承担主回复。
- 允许在 review 阶段上传修改稿，不必等最终决定——所以预案要能**快速出稿**。

### 4. OpenGWAS token 已过期（2026-09-15）
任何 LIVE 拉取（`extract_instruments` / 在线 clump）前必须重生成：api.opengwas.io/profile/ → 写 `~/.Renviron`。
本机出口仍封锁 `gwasapi.mrcieu.ac.uk`，LIVE 步骤须换网络或走 `data/raw/c1_cache/` 离线复现。

### 5. 永久性科学缺口（已披露，不阻塞）
- **G4 多状态时序**缺 UKB 个体级长表 → 未执行，已在 Limitations 披露。
- **失眠→AD 东亚复制**缺大样本 EAS 失眠 GWAS（GCST90018649 仅 389 例）→ 降级为探索性，Note 1 已写明不可行。

### 6. 文档卫生（低优先）
- `对话交接单_SESSION-HANDOFF.md` 停留在 **2026-07-18**，内容已严重过期（"沙箱不能跑 MR、待本地跑数"），**已被本文件取代**，建议归档到 `.workbuddy/memory/` 或加过期声明。
- 辅助图（`Fig3_Supp_protein_mediation` / `Fig3_education_phewas` / `Fig4_*` / `SuppFig*` 等）未在投稿稿引用，可留作他刊版本资产或归档。
- `S7_dual_track_concordance.md` / `S7b_gwascatalog_offline.csv` 是中文工作文档，文件名撞 S7 编号但未被引用。

---

## ✅ Step 0 数字溯源（2026-10-27 20:35 完成）

> 全文见 `reviews/Step0_数字溯源报告.md`。D1 已裁定「模拟=代理实现、结论收窄」；D2「许可范围内充分披露 AI」。

- **marginal FDR 可复现**：口径 = 12 格 cell-level FDR 的**等权均值**（balanced 0.0828→0.08；directional 0.1275→0.13）；两组 range 0.042–0.125 / 0.081–0.183 与稿件逐位一致。**数字不改**。
- **缺口补齐**：主脚本不输出 FDR 列 → 新增 `code/sim_marginal_fdr.py` + `sim_marginal_fdr.csv` / `sim_cell_fdr.csv`；归档 v1.2.0 需一并收录，Methods 写死该定义。
- **两处转录错误（已改）**：L100 sens@0.15 range `0.95–1.00`→`0.93–1.00`；P(A)@0.15 range `0.62`→`0.61`。
- **G6 只有 2/12 有据**：仅 Education→T2D（EAS BBJ，β=−0.145 P=0.012）与 Education→AD（EAS，power≥84% @R²≥0.05）有记录；LDL→CAD / BMI→T2D / Height→CAD / HDL→CAD 四格库内**零证据**。严格归零 → LDL 12→10 A、BMI→T2D 12→10 A、**Height 10→8 A→B（唯一改级）**、HDL 6→5 C。
- **L118 文本/表不一致**：正文只列 2 例 A（LDL、Education→AD），S8 实为 4 例 A。
- **数据盘点**：`data/` 仅含失眠、ieu-b-2、Bellenguez、GARD EAS、代谢物缓存；12 例中 10 例 GWAS 从未落地 ⇒ "not reported in source" 成立，且应表述为**对已发表汇总统计的再评分**，非本项目再分析。
- 🔴 **κ 来源存疑**：`code/interrater_reliability.py` 的 Rater 2 是硬编码数组（注释 "Deliberately stricter"），无第二评分者身份/日期/独立评分表。正文 "two independent raters" 需改写为 scoring reproducibility（K-a）。**已解决**：作者确认无第二评分者，正文已改为两次盲法评分、κ=0.89，旧脚本已 DEPRECATED。
- **A/B/C 已裁定并执行**：A＝G6 四格归零；B＝K-a（改写为 scoring reproducibility）；C＝两处 range 照改。

---

## ✅ Step 1–3 判据定稿 + 稿件同步（2026-10-27 20:55 完成）

> 全文见 `reviews/Step1-3_改动台账_2026-10-27.md`。

- **唯一判据件**：`output/results/Validation/rubric_spec_v3.csv`（两层：实证 2/1/0 + 模拟代理实现 + 差距说明 + 代码行号）；废止 v2 与旧 Table 1 草案。
- **S8 v3**：A3/B2/C4/D3；**唯一改级 Height→CAD A(10)→B(8)**；7 格改分（4×G6→0、3×G1→0 + 级联）。`S8_v3.csv` / `S8_v3_full.csv` / `S8_v3_ablation.csv`。
- **κ 改口径**：scoring reproducibility **0.89**（quad 0.97；per-gate 0.91；11/12 一致；boot CI 0.64–1.00）。升高的机制＝Height 两次评分都因 G6 归零而落到 B，**属证据修正连带，非判据放宽**（S8 表注第 6 条已写）。
- **消融（新 S10）**：逐门移除改级数 L1 6 / L2 2 / L3 3 / L4 3 / L5 2 / **L6 0**；无单门决定判决。
- 🔴 **新查实的两条不利事实（已写进正文）**：①模拟 `bx` 独立抽样 → **无工具间 LD**，原 L95 "block-diagonal correlation matrices" 表述不实，已改；②**G3 在基准中恒等于 G1>0（100%）、G4 与 G2 吻合 99.1%** → 43,200 次模拟实际只评估 G1/G2/G5/G6 四信号。
- **稿件已改 14 处**（摘要收窄、六门分数补齐 1 分档、G1/G6 二元化、κ 改写、DGP 纠错、Table 1 改两层、Table 2 脚注、Limitations 重写、AI 声明改如实披露、S1–S10）；摘要 347 词。（21:30 后再改：新增 S11，摘要 349 词，G6 判据收紧）
- **图表**：`Fig5_validation_grading` 由 `code/make_fig5_validation.py` 从 CSV 重绘（原图无生成脚本，缺口已补）。
- **环境锁**：新增 `requirements.txt`。

---

## ▶️ 下一步（按优先级；2026-10-27 21:30 刷新）

1. ~~**D3 标题**~~ → ✅ **已定稿（2026-10-28 20:15，用户选 A 双修）**：`correcting`→`diagnosing`（框架不校正混杂，只识别+改判），`43,200-simulation validation`→`a 43,200-replicate benchmark of its scoring rule`（基准只用 proxy 覆盖四信号，未验证任何基因组估计量）。已同步改：正文 md（humanized + v2）、回信 R1-2（改为"本次修订已改"并写明新旧标题与两条理由，Changes 行补 Title）、clean docx、高亮稿、`reviews/Marked_up_copy_legend.md`（新增 §6 记录两处改动理由）。**正文 body 10,982→10,987 词；表格 55 格未动；绿 32.9% 不变，黄 18.1%→18.4%。**
   - ✅ 文件锁已解（20:20）：旧件移入 `_archive/` 作对照，`_marked_v2.docx` 已改回原名 `manuscript_Frontiers_Methods_v2_marked.docx`（79,409 B，黄 13,915 / 绿 24,918 字符，标题已含 "diagnosing"），盘上不再有两份只差后缀的高亮稿。
2. ~~**Zenodo 补发**~~ → ✅ **已发布 v1.2.1，DOI `10.5281/zenodo.23733172`（record 23733172；concept 23732880）**，2026-10-28。走 GitHub Release → Zenodo 集成（用户裁决），未用手工 API。**新 concept 的事实须记住**：旧 DOI 21858125（v1.0.0）/22064685（v1.1.0）属 concept 21858124，因早期仓库链接变更已detach，本次发布自动落成新 concept，README/.zenodo.json 已如实写明"旧记录被取代、非本记录版本"。**归档已验证**：下载平台 zip（160 文件）→ 159 条清单逐条 sha256+字节数 **0 不符**；`doi.org` 200；DataCite 标题/版本 1.2.1/作者/MIT 全部对。
   - 🔴 **v1.2.0 曾带着坏清单发出**（已由 v1.2.1 修掉）：`build_manifest.py` 哈希的是 CRLF 工作树而非 git blob，159 条里 **125 条在任何其他机器上都校验失败**；字节数同病。修法=改读 `git cat-file blob`（docstring 已写明事故）。**教训：清单要哈希"归档里真实存在的字节"，不是本机检出。**
   - ⚠️ 归档快照内 README 仍是 `<DOI-TODO>`（DOI 在发布后才存在，回填于 main 提交 2869a03），属 mintage 顺序的固有代价，不要再为补 DOI 另发版本。
3. **v1.1.0 逐字节核验**（三次下载中断）——"both archived versions" 一句在核实前不得写出（letter 现写法只讲版本 DOI 与 git commit，未作逐字节断言）。
4. ~~**docx 同步 + 三线表**~~ → ✅ **已完成（2026-10-28 10:2x）**：`code/md_to_docx_frontiers.py` 从定稿 md 一键生成 `课题设计阶段/manuscript_Frontiers_Methods_v2.docx`（75.7 KB，162 段 / 5 表 / 10,982 词）。三线表已落实（R3#12 的承诺兑现）。
5. 未动遗留（保留）：`L1–L6`→`G1–G6` 纯格式统一；归档过期文档；BIB 备选路线待命。

### 2026-10-28 10:50 新增闭环（勿重做）

- **修订高亮版（marked-up copy）已生成**：`课题设计阶段/manuscript_Frontiers_Methods_v2_marked.docx`（77.5 KB），基线 = 投稿版 `manuscript Frontiers 0902.docx`（2026-09-02 Received）。
- 新脚本 `code/mark_changes.py`：两阶段设计 —— clean docx 由 `md_to_docx_frontiers.py` 正常产出，再与基线 diff 后在 **OOXML run 层**涂色，渲染路径零改动。
  - **黄** = 与投稿版不同的文字（词级 / 句级）；**亮绿** = 整段新增或重写；表格单元格一律黄。
  - **三层粒度**：sim≥0.85 词级 → 0.55–0.85 句子级（句序重排时词级会碎成涂鸦）→ <0.55 整段。碎片化保护：区间>5 且覆盖>40% 判重排。
  - **三处对齐难题已解**：①列名漂移（`Grade D`→`Grade D only` 是改名，`Grade C/D` 才是新列）→ 表头 ratio + 列内数字 Jaccard 各 0.5；②段落被拆分（基线 6 个 Methods 步骤挤在 1 段 1,245 字符）→ containment 必须排在 1:1 配对之前；③LaTeX 残留（`r_g`/`rg`、`r²`/`r2`、`--`/`–`）→ norm 去下划线 + 上标映射 + 连字符归并。
  - **图表题注**按 `^(Figure|Table)\s*\d+` 编号配对，避免"删一段+加一段"。
- **数字**：正文 68/157 段标记（词级 23、句级 15、重写 12、拆分段 12、新增 6）；表格 55 格（T1 29 / T2 26；**T3–T5 未动**）；删除段 **0**；黄 18.1% / 绿 32.9%；投稿 6,845 词 → 修订 10,982 词。
- **校验**：文本逐字一致（81,249 chars）；表格行列/列宽/边框、A4/行号/页码、上标数(35) 与 clean 版完全相同；斜体 β/P 与 10⁻⁴ 上标保留。
- 配套：`..._marked_changes.csv`（逐条台账）、`..._marked_deletions.md`、`reviews/Marked_up_copy_legend.md`（图例 + 改动分布）。
- ⚠️ **能力边界**：本机无 Word 且 WPS COM 被沙箱拦截 → **做不出真 tracked changes**（可 accept/reject 的修订记录），高亮版是位置标注，不是 Word 修订。

### 2026-10-28 10:20 新增闭环（勿重做）

- **投稿 docx 已生成**：新建 `code/md_to_docx_frontiers.py`（纯 python-docx，无 pandoc/无 editor_sdk 依赖），输入定稿 md → 输出 `课题设计阶段/manuscript_Frontiers_Methods_v2.docx`。
  - **三线表**：`tblBorders` 全 none + 首行 top(12/8 eighths) / 末行 bottom(12)；表头重复行 `tblHeader`；`tblW`/`tblLayout` 按 OOXML 顺序插入（tblW→jc→tblBorders→tblLayout→tblLook）。
  - **数学公式原生渲染**：自写 LaTeX→run 解析器，单字母斜体（变量）、`\text{}` 正体（SE/PP.H4/OR）、上下标用真 Word 格式；全文 `$`=0、反斜杠=0、`**`=0、反引号=0。
  - **版面**：A4 / 2.54cm 边距 / 双倍行距（正文）/ 连续行号 `lnNumType` / 页脚 PAGE 域。
  - **两个 bug 已修**：①`\text{--}` 的连接号因"先替换后合并"顺序错误留下 `1--2`（改为先合并再替换）；②`\text{SE}` 被误设斜体（字母分支硬编码 `"it"`，改为跟随 base）。
  - **列宽**：Table 1 与 Table 4 手工指定（否则短标签列被压到 1.4cm），其余按内容长度加权；五表宽度均 15.9cm = 版心宽。
- 校验：pandoc 3.12 第三方解析通过（11,823 词读出）；表格 5 张逐格与 md 比对仅 `\ge`→`≥` 类正常差异；参考文献 42 条齐全。
- ⚠️ 本机**无 Word、WPS 的 COM 被安全策略拦截**，无法转 PDF 做像素级预览；视觉确认需在装有 Word/WPS 的机器上打开一次。

### 2026-10-28 09:20 新增闭环（勿重做）

- **阈值追问预案（R1#1 延伸）**：新建 `code/threshold_robustness.py` → **S12**（S12.1 单点扰动 / S12.2 220 种单调四段全枚举 / S12.3 封顶能否绑定 / S12.4 基准 ROC 定位 / S12.5 封顶前后对照）。核心：±1 移动任一参数 → **极性翻转 0 例**；A 10→11 三例 A→B、10→9 一例 B→A；B 7→5 三例 5 分案 C→B；C 4→5 主案 C→D（仍负）；**封顶 4/6/8/取消在本队列全部 0 例**。基准 ROC：C=4→FPR .175、B=7→.103、A=10→.036（三条边界=三个嵌套假阳性水位，**事后核验**）。案卷：`reviews/R1-1_threshold_followup_playbook.md`。
- 🔴 **Table 2 重算（用户裁决 a）**：原 `sim_framework_operating_chars.py` **从未施加 G2 封顶**，与已发布规则不符。已把封顶写入 `grade_framework()`（含 `decisive_failure` 列），同种子重跑：**L1–L6 逐位一致**，4,363/43,200（10.1%）重复 **B→C**（全为真效应）。新 Table 2：sens(β=.15) .973/.847/.804 → **.878/.724/.691**；sens(β=.08) .506/.527/.545 → **.216/.376/.408**；FDR(1/3 null) .083/.128 → **.100/.151**；**特异度与 P(Grade A) 完全不变**。
- 连带更新：Results 段（含 β=.08 反序的结构解释：无多效性下 78% 复制在 G2 失败 vs 62%/59%）、Abstract（.08→.10、0.97→0.88）、Discussion（同）、Limitations 第二/第四点、Table 2 脚注、`manuscript/supplementary/S9_*`（新建 `code/make_s9.py`）、**Fig 2 重绘**（新建 `code/make_fig2_simulation.py`，原图无生成脚本）、`code/sim_marginal_fdr.py` 自查基准值、response letter 的 R1-1/R1-2/R1-4 与文件表。
- 审计产物：`output/results/Simulation/_archive/sim_replicates_pre_cap_20261028.csv`（封顶前副本，S12.5 的对照臂）。
- 校验：Table 2 九行逐格与 `table2_uncertainty.csv` / `sim_marginal_fdr.csv` 比对 **0 不符**；`sim_marginal_fdr.py` 自查全 OK。

### 2026-10-27 21:30 本轮新增闭环（勿重做）
- **R1#1 决定性失败规则**：G2=0 → 总分封顶 6（C 上界），写入 `build_s8_v3.py`、Table 1 脚注、Methods、S8 脚注 6。**零改级**（仅 Insomnia 触发且原本已 C）。
- **R1#4 特异度双口径**：spec(C+D)=1.000/0.882/0.809；全表加 Wilson 95% CI；0.20 阈值给出理由；FDR 随零比例 0.08→0.15 / 0.13→0.22（π=1/3→1/2）。脚本 `make_table2_uncertainty.py`。
- **R1#3 实证三路**：新增 **S11**（2462 → 54 → 37；SE 膨胀 **6.50× / 7.54×**；β 由 +0.104 翻转为 −0.130/−0.111）。正文新增小节 "What LD correction changes: precision, not only direction"。
- **R1#9 G6 降级**：Education→AD 的 EAS 复制 β=−0.029、**P=0.85（power ≥84%）** ⇒ 判为"未复制"，G6 由 2→0，**12→10 分，仍 A**。G6 判据改为"方向一致 **且** 名义显著（P<0.05）"。S8/S10/Fig5/κ/正文/Limitations 全部联动。
- **R1#6 coloc 区域**：47 forward 与 32 reverse **lead SNP 零重叠**；18 个 reverse strong 中 **16 个在 APOE（chr19:45.06–45.82 Mb, PP.H4>0.98）**，另 2 个在 **chr11p11.2**。明示 APOE 在 19q13.32、chr19 排除非 APOE 特异。
- **R1#7/Q2 修正正文错误**：CAUSE 实为 **15,564 个 P<1e-3 变异 + 1,000 MCMC**，**不是** clumped 集；MRlap 用全共有变异集自有剪枝。"three null results" 已改为"三分析均不支持原正向假设"（其中 MVMR 为名义负向）。
- **R1#8 披露缺口**：条件 F **从未提取**（MVIVW 对象无该槽，S3 全 NA），已在正文与 Limitations 明写为 reporting gap；TG 两路径 β1=−0.183/β2=+0.169，中介占比 **9.5%**（分母 = 总效应 −0.328）。
- **R3#11**：r_g "remained unchanged" → "not significantly different from zero" / "comparably null"。
- **R3#1/#2**：Methods 新增 Terminology 段；摘要 "precise" 改为"apparent precision reflects correlated instruments rather than information"；摘要 349 词。
- **R3#3/#7/#10**：新增 Methods "Trans-ethnic re-clumping" 算法段 + 无面板时的处理与两项偏倚。
- **R3#5/#6/#8/#9**：新增 "What each correction operates on"（只有 clumping 改 IV 集）；G4 confounder 选择依据 + 为何条件 F 只能在 G4；模拟参数依据。
- **R1#10**：drug-target 段扩写（cis-pQTL 锚定、组织、抑制/激活方向、安全性、成药性、prospective validation）。
- **消融数更新**（因 S8 变动重算）：G1 **7/12**、G2 3、G3 4、G4 4、G5 3、G6 0；正文与 letter 已同步。
- **交付物**：`reviews/Response_to_Reviewers_Frontiers.md`（22 条逐条应答，约 6.9k 词，含 concede/partial 标注与改动位置）+ `reviews/reviewer_comments_raw.md`（22 条原文逐字提取，供核对）。

### 已闭环的证据（备查指针，勿重算）

- **Egger_P 是混合列**：判为 MR-Egger **斜率** 为主（L2 拟合 8/11 vs 截距 6/11；HDL 备注 "Egger null"），但 CRP→CAD 只能是截距、Education→T2D 备注明写 "Egger int" → v3 已加 `Egger_P_semantics` 列逐格标注，未把未核实值搬进斜率列。见 `reviews/R1-1_Egger语义与CochranQ回溯.md`。
- **Cochran Q 从未计算**：仅 2/12 可回收（Education→AD Q=268.60/df=311/p=0.427；Insomnia Q=37.62/df=30/p=0.160，属 31-IV 版，与 54-IV 行不同口径**不可混填**）；10/12 离线不可回收。
- **无单一规则复现 12 个 L2**（最佳 IVW∧WM 失配 2/12：HDL→CAD、Education→T2D）⇒ L2 = 报告诊断 + 人工判断，这正是需要 κ 的原因。
- **R1#2 归档核对**：引用 DOI 21858125=v1.0.0(08-09)，另有未引用 v1.1.0(08-23)；归档脚本 git `b983865`，投稿版 `3225fea`，差一次聚合修正 → 归档复现不了 S9(0/72) 与 Fig2-A，Table 2 与实证结果不受影响。

---

## 📌 关键事实速查（避免重新检索）

| 项 | 值 |
|---|---|
| **投稿** | **Front. Genet. `1986036`，2026-09-02 收稿，Review ongoing，编辑 Erika Salvi，RT 73003** |
| 分级规则 | 六门 A–D：0–12 分；A 10–12 / B 7–9 / C 4–6 / D 0–3 |
| 失眠-AD | **Grade C**（shared APOE-locus liability） |
| G1 未 clump | β=+0.104，P=9.3×10⁻⁴（伪信号） |
| G1 clump 后 | β=−0.130，P=0.52（null） |
| G3 r_g | −0.028（P=0.57）；去 APOE −0.031（P=0.53） |
| G4 教育→AD | UVMR β=−0.33（P=1.1×10⁻⁵）；MVMR β≈−1.29（P=0.008） |
| G5 蛋白中介 | 全 null（indirect FDR=0.91）；TG 中介教育保护 β=−0.031，q=5.7×10⁻⁴ |
| G6 EAS 失眠→AD | β=−0.84，P=0.28（方向一致，power<6%） |
| 模拟 | 43,200 reps；null spec 1.00 / FDR 0；balanced spec≈0.80、FDR≈0.08；sens 0.97（0.95–1.00） |
| 评分可复现性 | **scoring reproducibility κ=0.89（quad 0.97，2 次盲法评分 / 72 items）**；v1 旧值 0.76–0.94 已弃（改称 inter-rater 不成立） |
| 审稿意见 | **22 条**：R1 十条（22 Oct 2026）/ R3 十二条（23 Oct 2026）；无 R2、无编辑决定信 |
| 应答包 | `reviews/审稿应答_review_packet.md`（≈8.3k tok，含 22 条逐字）+ 两轮提示词 + `make_review_packet.py` |
| 第 2 轮包 | `审稿应答_prompt_round2.md`（6.7KB）+ `审稿应答_精读摘录_round2.md`（45.6KB / 12 段 / ≈12.7k tok）+ `make_round2_excerpt.py`；含 F1–F7 已核实事实块 |
| S8 诊断回收 | `output/results/Simulation/S8_diagnostics_recovery.csv`（12×11）+ `reviews/S8_v2_proposed.csv`（拆列草案）|
| R1#2 自查 | `reviews/R1-2_代码自查_描述vs实现.md`：8 条指控核对 + 3 处审稿人未发现的缺陷 |
| Zenodo 归档 | DOI 21858125=v1.0.0（08-09，md5 已验）；v1.1.0=22064685（08-23，≈105MB）；**稿件六处引用均指旧版**；概念 DOI=21858124 |
| 可复现缺口 | 归档模拟脚本＝b983865，S9 逐格 sens 0/72 可复现；Fig2-A 会变平；S7 无生成脚本；`renv.lockfile` 实为 `renv.lock` |
| 稿件体量 | 正文 4,520 words（Abstract→References 前）/ 全文 6,628 words；上限 12,000 → 余量充裕 |
| 数据 ID | 失眠 `ukb-b-3957`（n=462,341）；AD 主 `ieu-b-2`（Kunkle 21,982/41,944）、敏感 `ebi-a-GCST90027158`（Bellenguez 85,934/401,577）；教育 `ieu-a-1239`（n=766,345）；EAS AD `NG00182` |
| 环境 | R 4.5.2；TwoSampleMR 0.7.9 / MendelianRandomization 0.10.0 / ieugwasr 1.1.0；numpy 2.1.3 / pandas 2.2.3 |
| 坐标 | 全 GRCh37；EA 数据 GARD 已 liftover hg38→hg19 |

---

## 🔗 关键文件地图

**投稿记录**
- 稿件编号 **1986036** · 收稿 2026-09-02 · 状态 Review ongoing（凭系统确认，工作区无独立回执文件）
- 投稿正文：`课题设计阶段/manuscript Frontiers 0902.docx`

**投稿三件套（终态）**
- `课题设计阶段/manuscript Frontiers 0902.docx` ← 投稿正文（**唯一终稿**）
- `课题设计阶段/figures_final/Frontiers_Figures_upload.zip` ← 5 TIFF 批量上传包
- `课题设计阶段/Supplementary_final/` ← S1–S9 + Note 1/2 + STROBE-MR

**稿件源与历史**
- `课题设计阶段/manuscript_Frontiers_Methods_v2_humanized.md` ← canonical 源（改稿改这里）
- `课题设计阶段/manuscript_Frontiers_Methods_v2.md` / `_v1.md` ← 前序版本
- `课题设计阶段/manuscript_BIB_protocol_v2_humanized.docx` ← BIB 备选路线
- `manuscript/` ← GitHub 归档副本（英文目录，勿与 `课题设计阶段/` 混淆）

**审计与决策**
- `课题设计阶段/audit_reproducibility_2026-09-01.md` ← 复现性审计 + 7 处事实修复
- `课题设计阶段/P2_resubmit_strategy_BIB_2026-09-01.md`、`BIB_protocol_restructure_2026-09-01.md`
- `课题设计阶段/reframe_highIF_blueprint.md` ← 升维蓝图（历史决策依据）

**代码**
- `code/sim_framework_operating_chars.py` ← 43,200 模拟（sens 已修）
- `code/make_figures.py`、`code/r_analysis/`（25 个 R 模块，`00_config.R` 为入口）
- `C:/Temp/iad_g1/fig2_v2.py` / `fig4_v2.py` ← 重画脚本（可复用"高级感 baseline"）

**归档**
- `.workbuddy/memory/2026-09-02.md` ← 最后一次完整工作日日志（图表重画、编号修复、投稿包成型）
- `.workbuddy/memory/MEMORY.md` ← 跨日长期记忆（结论速查 + 工具链坑）

---

## 📦 修订投稿包 + Zenodo v1.2.1（2026-10-28 终态）

**上传用文件（勿拿 0902 投稿版）**
- `课题设计阶段/manuscript_Frontiers_Methods_v2.docx` ← 修订正文（162 段 / 5 表 / 10,987 词，DOI 已换 23733172）
- `课题设计阶段/manuscript_Frontiers_Methods_v2_marked.docx` ← 高亮修订稿（71 段标记 / 表格 55 格 / 黄 18.5% / 绿 32.9%）
- `reviews/Response_to_Reviewers_Frontiers.md` ← 应答稿（R1-2 已写明 v1.2.1 + DOI）
- `manuscript/supplementary/` ← S1–S12 + `Supplementary_Tables.xlsx`（12 表，由 CSV 重建）

**GitHub / Zenodo**
- 仓库 `ming13333/iad-falsification-framework`：main `2869a03`，tag `v1.2.0` / `v1.2.1`，Release v1.2.0 + v1.2.1
- 归档 DOI **10.5281/zenodo.23733172**（v1.2.1，record 23733172）；concept 10.5281/zenodo.23732880
- 旧 concept 10.5281/zenodo.21858124（v1.0.0 21858125 / v1.1.0 22064685）已被取代，非本记录版本
- 清单 `MANIFEST_sha256.csv`（159 条）与归档 **逐条 sha256+size 全对**

**本次顺带修掉的三个"会随归档一起发出去"的缺陷**
1. `manuscript/supplementary/S8` 还是 9-02 投稿版（Education→AD 12 分）→ 换修订版（10 分）
2. `课题设计阶段/Supplementary_final/S9*` 是封顶前（sens .847）→ 统一到封顶后（.724）
3. `Supplementary_Tables.xlsx` 9-02 手搓件含旧 S8/S9、缺 S10–S12 → 新建 `code/build_supplementary_workbook.py` 重建 12 表
4. 6 个脚本硬编码中文路径 → ASCII 默认 + `IAD_SUPP_DIR` 覆盖；重跑输出逐字节一致

---

## ✉️ 逐条回复信（2026-10-28 22:30 完成）

**交付物**
- `reviews/Response_to_Reviewers_Frontiers.md`（源）+ `reviews/Response_to_Reviewers_Frontiers.docx`（148 段 / 2 表 / 8,084 词 / 0 markdown 残留；2026-10-30 21:47 重导，含 R1-2 标题+v1.2.1、R1-9 12→10 分、Height/LDL/BMI 三例补全与 "eight" 计数句）
- 生成器 `code/md_to_docx_response.py`（引文斜体+左竖线、Response 段、Changes 灰体索引行、三线表、页码、无行号）
- 审计器 `code/audit_response_letter.py`（22 条覆盖 / 引文 / 表态 / Changes / 字数 / DOI 一致性）

**覆盖**：R1 10 条 + R3 12 条 = 22/22，逐条含「审稿原文引文 → Response → Changes」
- 表态：accepted in full **20**、in part **2**（R1-3 模拟无法做三臂对比、R3-4 阈值无法从原理推导）、declined **0**
- 正文论据 5,112 词；新增 **Table R1 处置总表**（22 行：Comment / Topic / Disposition / Where）
- 统一了 12 处含糊的 "accepted." → "accepted in full."，便于编辑扫读
- 7 条 <120 词的短答均为澄清/格式类（R3-1/2/5/8/10/11/12），非敷衍，审计中列为 brief 而非缺陷

**本轮自查抓到的两处回信缺陷（已修）**
1. 🔴 只披露了 Education→AD 12→10，**漏了 Height→CAD 10→8（A→B，全队列唯一跨级变化）**；另 HDL→CAD 6→5、CRP/BMI→AD/T2D→AD 1→0 未提。现 Summary 第 6 条逐项列全，并指向 S8 的 `score_v1`/`delta`/`grade_changed` 三列。
2. 🟡 原第 6 条标题 "One published grade withdrawn" 与事实不符（撤回的是分数/G6 点，真正的等级变化是 Height 的 A→B）→ 改为 "One published grade changed, and every score that moved is accounted for"。

**一致性核对（回信 vs 正文 vs 补充表，全部实查）**
- Table 2 特异度 D-only 1.000/0.796/0.679、C/D 1.000/0.882/0.809、C/D 平衡组 CI 0.873–0.891 → 回信数字逐位一致
- S11 三档：0.1035/0.0313/2462、−0.1298/0.2031/54、−0.1114/0.2356/37，SE 膨胀 6.5/7.54 → 回信写 0.104/0.031/2462、−0.130/0.203/54、−0.111/0.236/37、6.5–7.5 ✅
- Education→T2D 各门 2,1,2,1,1,2 = 9 → 与 R1-1 算例一致 ✅
- Limitations 用 First–Seventh 分条，回信引用的 Second/Third/Fourth/Fifth/Seventh 均存在 ✅
- S10 72 行（CSV 73 含表头）、S8 12 案 24 列（含 `G6_evidence`）✅
- 回信末表补注：CSV 里六门沿用内部名 `L1`–`L6`，即正文的 G1–G6（避免审稿人对照时困惑）

**⚠️ 未发新版本（有意）**
- 曾给 `Supplementary_Tables.xlsx` 加三线边框以贴合 R3-12，随后**回滚**：归档 v1.2.1 里的 xlsx 无边框，改了会让工作树与已发布物不符。改为 builder 加 `--rules` 开关（默认关，投稿版可按需生成），回信如实写"CSV/工作簿均无竖线，若期刊要求可一键生成三线表版"。
- 回滚后 `build_manifest.py --check` 仍 **159/159 全对**（它比对 git blob，工作树改动不掩盖归档一致性）。

**下一步**：Frontiers 交互评审系统逐条粘贴 / 上传 `Response_to_Reviewers_Frontiers.docx` + `manuscript_Frontiers_Methods_v2.docx` + 高亮稿 + S1–S12。

---

## 🔍 第三方复核投喂包（2026-10-30 21:20）

**目的**：把「答复审稿人」这一轮交外部独立核账 —— 核的不是文笔，是**回信的每个断言能否在正文/补充表里对上**。

**交付物**

| 文件 | 体量 | 作用 |
|---|---|---|
| `reviews/review_packet_audit.md` | 19.5 KB | 投喂包：用法 → 预算 → 提示词 → 硬约束 → 正文骨架 → 回信骨架 → 数字卡 → **已知未决项 11 条** → 深读索引 → 审计契约 |
| `reviews/handoff_prompt_round1.md` | 1.1 KB | 首轮：只读包、禁读正文、输出两清单、停 |
| `reviews/handoff_prompt_round2.md` | 1.7 KB | 次轮：整份读回信 + 定向读正文 + S8，输出三张表 |
| `code/make_review_packet.py` | 12 KB | 生成器，行区间/字数/体量全从磁盘实时算，`--check` 校验 |

**与常规投喂包的区别**：常规包为「提修改意见」而建，只要骨架 + 数字卡；本包为「核账」而建，必须带
*已知未决项*（防外审把已声明缺口当新发现）与*判定口径*（PASS / MISMATCH / NOT IN ARCHIVE / OVERCLAIM）。
首轮 ≈6k token，次轮 ≈25k；**唯一允许整份读的文档是回信**（它就是审计对象）。

**本轮自查抓到的两处数值不一致（已修）**

1. 🔴 **Summary 第 6 条漏两个 A 级案例**。标题写「every score that moved」并称列全，实际只写 6 例；
   S8 的 `delta` 非零有 **8 例** —— 漏了 `LDL→CAD` 与 `BMI→T2D`（均 12→10，同因 G6 无记录复制）。
   已补全并加计数句「eight of the twelve moved, and all eight are named here」。审稿人手里有 S8，一查即现。
2. 🔴 **R1-9 把 LDL→CAD 投稿版分数写成 `10/10`**，S8 的 `score_v1` 为 **12**（原 G6 给 2 分）。
   已改为「12 points in the submitted version … 10 now, still Grade A」。

**核实后判定为「定义差异、非错误」的一处**（已写入包内 §7 第 11 条，防外审误判）

- FDR 存在两种口径：Table 2 / S14 用**12 格等权平均**（balanced = 0.1001）；`fdr_null_fraction_sensitivity.csv`
  用 **4,800 次合并**（balanced = 0.0969）。差额 0.003 源于格间 null 判定率不同 → 平均≠合并。
  回信正文 0.100 用前者、重加权讨论 0.18/0.26 用后者，两者各自自洽，但**正文未声明口径**。
  已在包内显式标注；是否在正文补一句口径说明，待定。

**✅ 已解决（2026-10-30 21:47）**：预览面板关闭后重导成功，md 与 docx 现已同步。
`reviews/Response_to_Reviewers_Frontiers.docx` = 148 段 / 2 表 / 8,084 词，旧件备份于 `C:/Temp/Response_docx_backup_*.docx`。
校验：新标题句 "six-gate falsification framework for diagnosing" ✅、"Two words were changed" ✅、
"Release v1.2.1 has now been deposited" ✅、"Changes: Title (both clauses revised" ✅；
审计器 `audit_response_letter.py` 全绿（22/22 覆盖，20 full + 2 in part + 0 declined，正文 5,144 词，Table R1 22 行，DOI 一致）。

**下一步**：按 `reviews/ACTION_ITEMS_2026-10-30.md` 逐条改稿；改完跑附录 B 的七步校验；重导 docx 后交编辑。

---

## 🔧 三份外审报告裁决 + 待改清单（2026-10-30 22:20）

**输入**：A（13 PASS/3 MISMATCH/6 OVERCLAIM）、B（9/5/8）、C（17/4/1，自称补读截断后重判）。
**裁决**：C 判定质量最高（唯一抓到 L116/L120 的 APOE 硬矛盾、L116 修法最可用），但 `COVERAGE` 虚高——表 A 判 PASS 的 6 条（R1-1/R1-3/R1-5/R1-10/R3-3/R3-6）在表 B 另列问题，真实为 **11 全通 / 6 部分 / 4 MISMATCH / 1 OVERCLAIM**。B 的 `PASS 仅针对本行断言` 声明必须搬进 C。

**落盘**：`reviews/ACTION_ITEMS_2026-10-30.md`（16 条，P0×7 / P1×5 / P2×4），每条含文件:行、逐字原文、替换句、验证命令。26 组原文锚点脚本校验 **26/26 命中**。

**🔴 两处翻转（推翻此前口头结论）**：
1. **撤回"A 的 30 vs 40 IV = MISMATCH"**：`results/ea_mr/ea_transethnic_insomnia_ad_report.txt` 实锤 `40 LD-independent instruments` → `Harmonized: 30/40 ... 30 retained`。40 是提取数、30 是 harmonise 后，**两者都对**，仅缺一句损耗说明。A 建议"统一为 40 IV"若照改，S8 会与入模数 30 不符。
2. **回信 R1-2 (iv) 过度认错**：`code/sim_framework_operating_chars.py:L108-109` 的 `e_y = overlap*e_x + sqrt(1-overlap²)*e_y` 证明样本重叠正是靠相关残差实现 → 审稿人此项指控只对一半，**正文 L101 是对的，该改回信**。连带须把 "correct in every particular" 降级为"五项成立、一项更正"。

**🟠 补充表版本已隔离（22:36 执行完毕）**
实际是**三目录两状态**，不是"两套"：`manuscript/supplementary/`=12 sheet/S8 24 列/10-10-10-8-4（唯一权威，MD5 `2436d374`）；`Supplementary_final/`=**混合态**（CSV/MD 全是新版，唯 xlsx 停在 Sep 2 旧制）；`课题设计阶段/Supplementary/`=全面旧版。
处置：7 个旧制文件加 `_SUPERSEDED_<日期>` 后缀（保留原内容只改名，不动目录结构以免断 `reviews/` 下 20+ 处引用）；`Supplementary_final/Supplementary_Tables.xlsx` 用权威版覆盖（MD5 逐字节一致）；新增 `manuscript/supplementary/_AUTHORITATIVE.md` + `课题设计阶段/Supplementary/_SUPERSEDED_README.md`。9 个 ONLY-HERE 历史文件与 `Supplementary_Notes.docx` 有意保留。
校验：`build_supplementary_workbook.py --check` → `workbook OK`；`make_review_packet.py` 依赖的新版 CSV 未改名，引用完好。

**🔴 清单定稿 15 条（撤回 D1）**：S8 的脚注 1–7 与 reproducibility 段落**确实存在**，在 `S8_twelve_case_validation.md` 里（7,489 B，含 7 条脚注 + Scoring reproducibility 段）；CSV 不带脚注是设计而非缺陷。A 的 R1-9 MISMATCH 与我的 D1 均撤回。**教训：判"承诺是否兑现/两处数值是否冲突"须枚举全部载体（md/csv/xlsx/docx）与上游日志，不能只查一个文件。**

## 2026-10-31 · M0/M1/M2 已改（方案 A）

- **M1/M2（正文 L116）**：54 变异档阈值 `r²<0.001`→`r²<0.1`，首句与 instrument count chain 两处同改；补 tight 档 `37 harmonised variants / SE=0.236 / P=0.64`。
- **M0（比原 15 条更根本，新发现）**：Methods 声明的 clumping 阈值 ≠ 产生主结果的阈值。铁证 `code/r_analysis/04_mvmr.R:28`（`r2_loose=0.1` → 54 IV / β=−0.130；`r2_tight=0.001` → 37 IV / β=−0.111）。**用户选定方案 A**：Methods 向 0.1 对齐。
  - 正文 L67 主句改 `r²<0.1` + 括注严格档；L91 / L289 流程句同改（replace_all 一次改两处）。
  - 回信 R3-4 重写：先承认投稿版 Methods 误写主档，再论证"前提不再成立、结论在最宽松档已翻转"；标题加 `*(Methods corrected in revision)*`、Changes 明写 corrected、处置表 `Accepted in part; Methods corrected`、Summary 第 6 条补更正说明。
  - **未动**：摘要（不含阈值）、Table 2、Fig 2A（本就同画两档）。
- **连带修正**：正文原称 54 与跨族裔 40 差异"仅源于面板更新"，实测跨族裔 `r²<0.001`、主分析 `r²<0.1`，**阈值与面板同时变** → 改为 "two sources" + 不可 like-for-like + 仅作低效能方向筛查；`ea05_transethnic_insomnia_ad.py:155` 的 "under the same thresholds" 同步修正（已归档 `results/ea_mr/` 输出保持 v1.2.1 原样）。
- **校验**：`54→44→38→33` 与 `S7_iv_annotation_confounder.csv`（44 行/6 excluded/38 retained）吻合；正文 docx 162 段/5 表/段落 11,056 词；回信 docx 149 段/2 表/8,251 词；`audit_response_letter.py` 全绿（22/22；20 full + 2 in part；正文 5,218 词）。
- **🔴 待办风险**：`课题设计阶段/` 与 `reviews/` 整目录未纳入 git（非 ignore，是从未 add）→ 改错无法回滚。已临时备份 `C:/Temp/ms_humanized_20261031_111120.md`、`C:/Temp/resp_20261031_111120.md`。**建议先 `git add` 再继续改 M3–D4。**
- **剩余**：M3（APOE 硬矛盾）、M4（回信 above→below）、M5（方差/SE 串台）、M6（L153 六门）、M7（G3 规则）、W1–W5、D2/D3/D4。

## 2026-10-31 · 16 条全部改完（16:05）

- **P0 全清**：M0（阈值，方案 A）、M1/M2（L116 两处）、M3（APOE 硬矛盾→改为"不归因于 19 号染色体单独"并指向 G3）、M4（above→below）、M5（SE 倍率，另注方差差 42–56 倍）、M6（L153 六门→Grade A under the current rubric；warrant target investment→prioritize trait-level hypotheses）、M7（G3 规则 or→neither…nor，并注明仅缺 coloc 记 1 分）。
- **P1 全清**：W1（restores the sampling variance→clumping 同时改了工具集与 SE，比值不能识别抽样方差）、W2（低效能向零偏倚→降分辨率、单次符号反转证据弱）、W3（删"不影响 null 符号"保证，改为可影响符号故仅作方向筛查不计分，正文×2+回信）、W4（网格全在 0.226 之下→every grid point lies below that boundary，采样的是低效能区）、W5（R1-2 (iv) 拆两层：无 LD 协方差成立／相关残差确实生成并给出代码公式；"correct in every particular"收紧；正文 L101 补层间区分）。
- **P2 全清**：D2（Wilson 范围限定 sensitivity+两种 specificity，说明 P(A) 点值与 FDR 范围）、D3（补 40 提取→30 位置匹配入模）、D4（L106 的 0.80 标 D-only）。
- **校验（附录 B 全绿）**：6 组"期望无输出"全部无输出；`r²<0.1` 出现 2 次（同在 L116，`grep -c` 按行计数显示 1）；harm.tsv 31 行；审计器 22/22、20 full + 2 in part、5,379 词；正文 docx 162 段/5 表、15 处关键句全命中；回信 docx 149 段/2 表/8,422 词、7 处全命中。
- **下一步**：①~~`git add` 正文与回信 md~~ ✅ 已完成（见下）；②~~高亮标注稿重做~~ ✅ 已完成（见下）；③正文/回信定稿后重跑 `make_review_packet.py --check` 更新外审投喂包。

## 2026-10-31 · 版本控制 + 高亮稿重建（16:40）

### ① 纳入 git（commit `0cdb7c7`，46 文件 / 0.45 MB）

此前 `课题设计阶段/` 与 `reviews/` **整目录从未 git add**（非 ignore 所致），16 条修订零回滚能力。已补：

- **纳管**：正文源 `manuscript_Frontiers_Methods_v2_humanized.md`（12,258 词）+ 投稿 docx；`reviews/` 全量；4 个新脚本（audit_response_letter / md_to_docx_response / make_review_packet / extract_bib_docx）；`progress.md`、`RULES.md`、`requirements.txt`、manuscript 下 scope/贡献声明
- **`.gitignore` 新增排除段**（防一次 `git add .` 拖入 418 MB）：`课题设计阶段/code/`（MRlap 源码副本含 124 MB .git pack）、`figures/`、`figures_final/`、`备份figure/`、`_archive/`、`GM_reference/`、`Supplementary*/`、`*.pdf`、`*.json`、3 个期刊版大 docx（3.4–4.0 MB）、`.workbuddy/`
- 校验：5 个待纳管文件 `check-ignore` 全 NOT IGNORED；5 类大件全部 IGNORED

### ② 高亮稿重建（commit `a399002`）

旧 `_marked.docx` 停在 10-28 的 D3 批次，与 16 条修订后正文对不上。以同一 baseline（`manuscript Frontiers 0902.docx`，02 Sep 投稿版）重跑 `mark_changes.py`：

| 项 | 旧（10-28） | 新（10-31） |
|---|---|---|
| 正文标记段 | 68 / 157 | **71 / 162** |
| 明细 | 词级 23 / 句级 15 / 重写 12 / 拆分 12 / 新增 6 | 词级 23 / 句级 18 / 重写 12 / 拆分 11 / 新增 7 |
| 表格格 | 55（T1 29 / T2 26） | **56（T1 29 / T2 26 / T4 1）** |
| 高亮占比 | 黄 18.5% / 绿 32.9% | 黄 **20.7%** / 绿 **31.2%** |
| 删除段 | 0 | 0 |

- **T4 那 1 格 = M0 阈值更正**（`r2<0.1 … repeat at the stricter r2<0.001 tier`），旧版"T3–T5 未动"是当时实况，非回归
- **一致性校验全绿**：与 clean docx 文本逐字一致 **82,353 字符**；段 162 / 表 5 相同；A4、2.54cm 边距、`lnNumType×1`、页脚 PAGE 域、5 表三线边框全部相同；斜体 **2,312 字符**、上标 **71 字符**与 clean 版完全相同（run 数 +4 仅为涂色拆分，无视觉影响）
- **16 条改动覆盖抽查**：M0/M1/M3/M6/W1/W2/W3/W4/D3/D4 共 10 个锚点，全部落在高亮区内
- **同时清理**：`reviews/marked_changes.csv`（旧数据 127 行 vs 权威 128 行）与 `reviews/marked_deletions.md` 已移除，避免"两套同名文件数字不同"——上次补充表就栽在这上面。权威三件套统一在 `课题设计阶段/`
- `reviews/Marked_up_copy_legend.md` 已重写统计并新增 §2.1 逐条列出本轮 8 处正文 + 1 格表格改动

### ③ 推送

`d07214c..a399002 main -> main` 已同步；`size-pack 13.69 MiB`。

- ~~**剩余**：③重跑 `make_review_packet.py --check`~~ → **已于 16:45 完成**，见下节

### ④ 顺手修掉的引用错误（commit `568d3df`）

`code/audit_response_letter.py:26` 的 `MS` 指向 `manuscript_Frontiers_Methods_v2.md`，而那是**内部审阅草稿**（表头自述 `**Status:** v2 draft for internal review`，7,305 词，无作者块，未收到任何一轮修订），真正的投稿源是 `..._v2_humanized.md`（12,258 词）。

- **影响范围有限**：正文在该脚本里只被读一处——提取 Zenodo DOI 做比对（L158），不做引文核对；两文件 DOI 均为 `10.5281/zenodo.23733172`，**故今晨的审计结论不受影响**（重跑后 22/22、20 full + 2 in part、5,379 答复词均不变）
- 仍已改为指向 humanized 版，并加注释说明两者 307 行骨架相同但内容分叉，防止将来扩展校验时静默跑在草稿上
- 同时把 `manuscript_Frontiers_Methods_v2_humanized.docx`（Sep 2，6,794 词，旧标题 `correcting`）改名加 `_SUPERSEDED_20260902`——它与投稿文件只差一个词，误投风险最高
- `reviews/Marked_up_copy_legend.md` 新增「Which manuscript file is the manuscript」表，一次讲清四个近乎同名文件分别是**源文件 / 上传件 / 内部草稿 / 被取代导出件**
- `.gitignore` 增加 `*.bak_*`、`*.bak`（编辑前备份不入库，git 已有历史）

> 口径澄清：审计器输出的 `total response words 5,379` 是**答复正文**总词数，不是稿件正文词数（稿件正文段落 11,162 词 / 源 md 12,258 词）。此前口语里称"正文 5,379 词"易被误读，后续按此三分口径报数。

## 2026-10-31 16:45 · 第 17 条（条件 F 表述）+ 投喂包刷新（commit `7a3ea8c`）

### ① 第四份外审核账的净结论

外部又投喂一份核账（表 A 逐条 22 条 / 表 B 只说未改 6 条 / 表 C 修订新引入错误 8 条 = 36 条判定）。逐条实测后：
**35 条已落地或属误判，净新增真问题 1 条**。它核的是改稿前快照——表 A 的 4 个 MISMATCH（R1-4 Wilson / R1-6 APOE / R1-7 above / R3-2 sampling variance）正是上一轮 M0–M7 改掉的那几条。

- **它的价值**：表 C 单设「修订新引入的错误」维度，是前三份都没做的视角；且识别出 SE 倍率与方差倍率的概念混淆（6.5–7.5× vs 42–56×），是真功底
- **它判错 2 条**：①表 C 第 8 条「30 vs 40 IV」是误判——40 = 提取数、30 = 协调后进拟合数，正文 L116 已明写链条，S8 写 30 正确，**不应统一为单一数值**（统一反而丢信息）；②表 C 第 7 条方向猜反——它假设「代码可能未生成残差相关」，实际代码是 `e_y = overlap*e_x + sqrt(1-overlap²)*e_y`，残差相关确实生成，回信 L78 已正面驳回该半句
- **结构瑕疵**：表 A 判 R1-1 PASS 而表 B 同时列 R1-1「改动幅度小于承诺」，同一编号两个判定未交叉消解

### ② 唯一真问题（已改，两处载体）

`manuscript_..._humanized.md:L73` 与 `Response_to_Reviewers_Frontiers.md:L260` 原写
`its collapse indicates collinearity rather than weak instruments` —— 把共线性与弱工具对立，统计上不成立：**条件 F 低本身就是条件弱工具识别，共线性是其成因而非替代解释**。

已改为 `identifies conditional weak instruments whose origin is collinearity, not a failure of unconditional instrument relevance`。旧表述全稿残留 **0**。

### ③ 投喂包刷新（`code/make_review_packet.py`）

注意存在新旧两份脚本：`code/`（31 KB，2026-10-30，权威）vs `reviews/`（13 KB，10-27，旧）。**用 `code/` 的**。

| 产物 | 变化 |
|------|------|
| `review_packet_audit.md` | 回信 331→333 行 / 8,358→8,670 词；正文 10,993→11,172 词；§8 十个区间整体 +2 行 |
| `handoff_prompt_round2.md` | 行区间同步 |
| `handoff_prompt_round1.md` | 未变（内容未受影响） |

**校验**：`--check` 三件全 `ok`；抽样验证 `## R3-4`=L234、`## R3-6`=L254、`## R3-12`=L304、`## R3-10`=L288 与 packet 声明逐条精确吻合；正文 `## Results`=102 / `### Operating`=104 / `### Example`=110 / `### Precision`=130 / `## Discussion`=143 / `## Declarations`=159 / `## References`=177 全部命中；数据卡 54/−0.130/0.203/6.50 与 37/−0.111/0.236/7.54 与 S11 一致。

### ④ 推送

`git commit 7a3ea8c`（4 文件，+17/−17）+ `2fc9b95`（本文件）。首次 push 报 `Recv failure: Connection was aborted`（github:443 瞬时不可达），**重试即通**：`49ef7e2..2fc9b95 main -> main` 已同步。
（同批出现的 `git-credential-manager.exe: No such file or directory` 是无害警告，凭据已缓存，不影响推送结果。）

## 2026-10-31 19:50 · 三份 docx 重建（commit `d9ac84f` / `47a5bf2` / `bdb4e9e`）

### 发现的问题（严重，差一步就投出去）

`.md` 源在 **16:41** 改完，但三份 **docx 分别停在 16:01 / 16:33 / 16:01**，都还是 16 条修改之前的状态——**投稿件里仍带着 "collinearity rather than weak instruments" 这句旧话**，而这句正是本轮声称已修正的。若直接投出，等于把"说要改却没改"的证据亲手附上。

### 重建顺序（依赖链）

1. `code/md_to_docx_frontiers.py --in <humanized.md> --out manuscript_Frontiers_Methods_v2.docx`（162 段 / 5 表）
2. `code/mark_changes.py --baseline "manuscript Frontiers 0902.docx" --target <新docx> --out <_marked.docx> --csv ... --deletions ...`（71 段标记 / 56 表格单元 / 0 删除，与上一版数量一致）
3. `code/md_to_docx_response.py --in <回信.md> --out Response_to_Reviewers_Frontiers.docx`（149 段 / 2 表 / 8,432 词）

### 校验

| 项 | 结果 |
|---|---|
| 新句 `origin is collinearity` | 三份 docx **全在** |
| 旧句 `rather than weak instruments` | 三份 docx **全无** |
| 13 点关键句探测（含 12 条前轮修改） | **13/13 命中**，重建未丢前轮成果 |
| LaTeX 残留 | `$` 0 个、反斜杠命令 0 个 |
| 高亮清单变化 | 仅 G4 段（para 41）1 行，1,878→1,948 字符（+70），与单句替换吻合 |
| `audit_response_letter.py` | OK；22/22；5,389 答复词 |

### 同步更新

- `reviews/ACTION_ITEMS_2026-10-30.md`：汇总表加 **W6**，正文标注"总计 17 条全部 ✅"，收尾校验表补"三份 docx 与 md 同步"一行、回信 docx 词数 8,422→8,432
- `reviews/Marked_up_copy_legend.md`：时间 16:33→19:44，条数 16→17（71/56/127 数字经复核未变）

### 待办

**4 个本地 commit 未推送**（`8dddcf4` `d9ac84f` `47a5bf2` `bdb4e9e`）：代理连续 `CONNECT tunnel failed, response 502`，三次重试失败。本地库已完整，网络恢复后 `git push origin main` 一条即可。

## 2026-10-31 20:20 · 元审计：修掉一条统计理由错误 + 6 项文档卫生

用户要求"回顾整个返修过程，找出错误和不严谨处"。采用**元审计**（审过程而非审内容），发现 6 类问题，按批准顺序处置。

### #1 回信 L108 的统计理由是错的（本轮最重要）

原句 `P(Grade A) is reported as a point estimate and empirical FDR as the range ... because neither is a frequency over the pooled set`。

**P(Grade A) 恰恰就是 pooled 频率**——正文 Table 2 脚注自证：12 格 × 400 重复等权，未加权均值 = pooled 比例；它与 sensitivity 同批 4,800 次重复、同性质（A 占 0.667 / A∪B 占 0.691）。给 sensitivity 算 Wilson 却说 P(Grade A)"不是频率"，理由不成立。

**FDR 那半句是对的**：12 格"比值的均值"、各格阳性呼叫数不同，不可池化成单一二项比例——这才是给范围的正确理由。

成因：D2 修"every proportion has Wilson"的过度声称时，把 FDR 的理由错套到 P(Grade A) 上。

已改（两载体同步）：P(Grade A) 不给区间的理由是"它是描述性等级分布，不是本框架要控制的操作特性"；FDR 保留"分母不等不可池化"；并补一句 Wilson 是在 pooled 4,800 上算、把 12 格视为 exchangeable 的前提。正文脚注（L263）同步。

### #2 正文 L126 补 40→30

L126 原只说 `40 LD-independent European instruments`，S8 写 `trans-ethnic 30 IV`。解释只在 L116，审稿人读 G6 结果段不会回翻。已改为 `40 ... (30 retained after harmonisation)`。

上一轮我判第四份核账这条"纯属误判、不必改"——数字判断没错，但"不必改"下得太绝对。

### #3/#4 legend 自相矛盾（我上一轮造成的）

L3 已改 17 条，但 §2.1 仍写"16 audit items changed eight places"，且缺 W6 行。已补 W6 行、改"nine places"、trans-ethnic 行注明"两处都写了"。

同时发现两个**不可复现的旧数字**：
- 词数 11,162 → 实测 **11,235**（body paragraphs）
- 字符比例 yellow 20.7% / green 31.2% → 实测 **22.3% / 33.8%**（body only；含表格则 23.4% / 31.7%）。旧值任何一次构建都复现不出来，已替换并写明口径

另核实：§2 的五类细分（23/18/12/11/7 = 71）与脚本 stdout 的"52 word-level / 19 whole"**完全自洽**（52=23+18+11，19=12+7），只是粒度不同，无需修正。

### #5 ACTION_ITEMS 条数账目

"16 条全部改完"与"定稿 15（撤回 1 条）"并存且 D1 是撤回非改完。已加一张账目表：口述 13 → 落盘 16 → 撤回 1（D1）→ 有效 15 → 追加 W6 → **当前 17（16 改 + 1 撤）**；标题同步改为"口头 13 → 落盘 16 → 有效 15 → 追加后 17"。

### #6 脚本卫生

`reviews/make_review_packet.py`（13 KB / 10-27 旧版）与 `code/make_review_packet.py`（31 KB / 权威）并存，误跑旧版会静默产出过期包。已 `git mv` 为 `..._SUPERSEDED_20261027.py`（保留历史）并在文件头写明"do not run"。

### 重建与校验

正文 docx → 高亮稿 → 回信 docx → 投喂包，全链条重跑。

| 项 | 结果 |
|---|---|
| 新表述三处进 docx | L126 `30 retained`、脚注 `descriptive grade distribution`、`unequal denominators` 全部 OK |
| 回信 docx | `does not pool into a single binomial proportion` OK；旧理由 grep 计数 **0**（md 两文件均 0） |
| 高亮稿 | 71 段 / 56 格 / 0 删除（改的两段本就在标记集内，计数不变） |
| 投喂包 | 回信 8,722 词 / 正文 11,236 词；`--check` 三件全 ok |
| `audit_response_letter.py` | OK，22/22 |

### 仍待

推送（网络 502）。另：本次元审计是**定点+抽样**，未逐字通读 333 行回信与 307 行正文，References/S1–S12 交叉引用、R1-8/R1-9/R3-5/R3-8/R3-10/R3-11/R3-12 七条未逐句核——若要"确保零遗漏"需再补一轮全文通读。
