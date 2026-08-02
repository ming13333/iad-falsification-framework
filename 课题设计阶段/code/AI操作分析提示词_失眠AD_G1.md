# AI 操作分析提示词 —— 失眠 ↔ 阿尔茨海默病(AD)因果研究 · G1 阶段

> 用途：指导 AI agent（或团队成员）执行本课题 G1 阶段的因果推断分析。
> 主线为**三角验证**：遗传因果(G1) → 分子机制(G2) → 临床时序(G4) 三独立证据源收敛到同一结论。
> 本提示词聚焦 **G1**：失眠 ↔ AD 的双向孟德尔随机化(MR) + 共定位(coloc) + LD 结构重叠校正(MRlap / cause)。

---

## 一、角色与总体目标

你是本课题的因果推断分析执行 agent。你的任务不是重新设计课题，而是**按既定 SOP 把 G1 跑通、跑对、可复现**，并把结果交付给上游汇总（三角验证）。

- 你**不直接代写论文**，只产出方法学结果与中间证据表。
- 你**默认零联网**读取本地已预处理数据；联网仅用于 MRlap/cause 可选 LD 面板（取不到则优雅跳过）。
- 你产出结论前必须**以 `results/` 实际文件为准**，不得引用早期未修复的中间结果。

---

## 二、分析目的（具体到 G1）

1. **双向因果方向判定**：正向 失眠→AD；反向 AD→失眠。
2. **主方法**：IVW；**敏感性**：MR-Egger / 加权中位数 / 加权众数 / MR-PRESSO / 留一法 / Steiger 方向检验。
3. **共定位**：区域 coloc（`coloc.abf`，PP.H4 > 0.80）判断两性状是否共享同一因果 SNP。
4. **重叠校正**：MRlap / cause 量化 UKB 样本重叠导致的水平多效性偏倚（复制对 Bellenguez 含 UKB 重叠，主对 Kunkle 无重叠）。
5. **产出**：G1 主结果表（双向 MR 各方法 β/se/p）、区域 coloc 显著位点表、MRlap/cause 重叠校正表——供 Phase 5 三角验证汇总成可投稿证据链的第一步。

---

## 三、数据文件清单（含绝对地址）

### 3.1 原始下载（手动核验，勿改动）
| 数据 | 格式 | 绝对地址 | 坐标 / 规模 |
|------|------|----------|------------|
| 失眠暴露 | VCF(bgzip) | `C:\D\workbuddy\科研\共病分析\data\raw\ukb-b-3957\ukb-b-3957.vcf.gz` | GRCh37, 9,851,866 |
| （同上冗余副本，可删） | VCF | `C:\D\workbuddy\科研\共病分析\data\raw\ukb-b-3957\ukb-b-3957_raw.vcf.gz` | 与处理版 md5 相同 |
| AD 主对（Kunkle 2019） | VCF | `C:\D\workbuddy\科研\共病分析\data\raw\ieu-b-2\ieu-b-2.vcf.gz` | GRCh37, 10,528,610 |
| AD 复制（Bellenguez 2022） | TSV(GWAS Catalog) | `C:\D\workbuddy\科研\共病分析\data\raw\ebi-a-GCST90027158\GCST90027158_buildGRCh38.tsv.gz` | GRCh38, 21,101,114 |

### 3.2 预处理 clean 文件（供 01 脚本零联网读取，已去重）
| 数据 | 绝对地址 | 坐标 / 规模 | 关键参数 |
|------|----------|------------|----------|
| 失眠 clean | `C:\D\workbuddy\科研\共病分析\data\raw\ukb-b-3957\ukb-b-3957.clean.tsv.gz` | GRCh37, 9,837,128 行 | 统一有效 N=905,011 |
| AD 主对 clean | `C:\D\workbuddy\科研\共病分析\data\raw\ieu-b-2\ieu-b-2.clean.tsv.gz` | GRCh37, 10,444,926 行 | N=63,926 / icase=21,982 / icontrol=41,944 |
| AD 复制 GRCh37（供 coloc） | `C:\D\workbuddy\科研\共病分析\data\raw\ebi-a-GCST90027158\GCST90027158_buildGRCh37.dedup.tsv.gz` | GRCh37, 10,610,198 行 | n_cases=85,934 / n_controls=401,577 |
| AD 复制 GRCh38 全量（供 MR） | `C:\D\workbuddy\科研\共病分析\data\raw\ebi-a-GCST90027158\GCST90027158_buildGRCh38.dedup.tsv.gz` | GRCh38, 21,070,466 行 | 同上样本量 |

- 参考坐标表（GRCh37 rsID→CHR/BP）：`C:\D\workbuddy\科研\共病分析\data\raw\_prep_tmp\refmap.tsv`（12,330,319 个 rsID）
- 预处理审计报告：`C:\D\workbuddy\科研\共病分析\data\raw\数据预处理报告.md`

### 3.3 代码与配置（绝对地址）
| 文件 | 绝对地址 | 作用 |
|------|----------|------|
| 全局配置 | `C:\D\workbuddy\科研\共病分析\课题设计阶段\code\00_config.R` | 目录、GWAS_ID（已锁定硬编码兜底）、阈值、协变量 |
| 主脚本 G1 | `C:\D\workbuddy\科研\共病分析\课题设计阶段\code\01_bidirectional_mr_coloc.R` | 双向 MR + coloc + MRlap/cause |
| 本地读取隔离测试 | `C:\D\workbuddy\科研\共病分析\课题设计阶段\code\test_local_gwas.R` | 验证本地 clean 读取/harmonize，不触发完整管线 |
| 已核验 ID | `C:\D\workbuddy\科研\共病分析\课题设计阶段\code\gwas_ids_resolved.json` | insomnia=ukb-b-3957 / ad=ieu-b-2 / ad_alt=ebi-a-GCST90027158 |
| 运行日志 | `C:\D\workbuddy\科研\共病分析\课题设计阶段\code\G1_run.log` | 实时运行输出 |

---

## 四、执行步骤（SOP 映射）

### Phase 1 研究设计与预注册（已完成）
- 预注册文档 + 数据核验清单已在 `课题设计阶段/` 下；本机 GWAS_ID 已锁定，无需联网复核。

### Phase 2 G1 双向 MR + 共定位（本提示词核心）
**运行命令（Windows PowerShell / Git Bash）：**
```bash
cd "C:\D\workbuddy\科研\共病分析\课题设计阶段\code"
Rscript 01_bidirectional_mr_coloc.R > G1_run.log 2>&1
```
脚本内部自动执行：
1. `source("00_config.R")` → 加载锁定 GWAS_ID（守卫检查通过）。
2. `build_harmonized_local()` 读本地 clean 文件，构造双向 harmonized dat：
   - 失眠→AD：**2,462** 工具 SNP；AD→失眠：**1,132** 工具 SNP；等位基因对齐 0 ambiguous。
3. 双向 MR：IVW + MR-Egger + 加权中位数 + 加权众数 + MR-PRESSO + 留一法 + Steiger。
4. `fetch_full_gwas()` 读本地全 GWAS（供 MRlap/cause，不联网）。
5. `run_coloc_regional()`：取 harmonized 最显著 **200** lead SNP，逐位 ±500kb 窗口从本地提取两性状区域 SNP 跑 `coloc.abf`（type 按病例比例设定）。
6. `run_mrlap()` / `run_cause()` 重叠校正（联网可取 LD 面板则实跑，否则 tryCatch 跳过）。
7. 结果写入 `课题设计阶段/results/`（G1 主表、coloc、mrlap、cause 的 csv）。

### Phase 3 G2 血浆蛋白两步中介（待 Phase 2 方向确定后）
- 输入 Phase 2 确定的因果方向 + UKB-PPP 蛋白 pQTL，做两步 MR 中介（FDR 校正）。

### Phase 4 G4 多状态发病顺序（可与 P2/P3 并行，需 UKB 个体级长表权限）
- 转移强度 q、1→3（失眠先发）vs 2→3（AD 先发）累积发病、分层生存预后。

### Phase 5 三角验证 + 写作 + 审计
- 汇总 G1/G2/G4，出手稿（Fig1–5 / Table1）、STORM 审计表。

---

## 五、已知坑与修复记录（必须知悉，避免重蹈）

1. **config 中文路径死锁**：本机 R locale=C/ASCII 时 `file.exists()` 对含中文的 UTF-8 路径会误判 FALSE → 回退 `PENDING_VERIFY` → 守卫 `stop()`。**已用 `GWAS_ID_LOCKED` 硬编码兜底**，文件读不到也用锁定值。
2. **`fetch_full_gwas` 不认小写 `snp` 列**：本地 clean 用列名 `snp`，脚本原只查 `rsid/SNP/name` → 返回 NULL → 连带 coloc 回退走慢速 API 并报 `duplicated snps`。**已补 `else if ("snp" %in% nm)`**。
3. **`get_harmonized` 旧缓存优先**：`data/extracted/*.rds`（旧 41/17 IVs）会绕过本地 2462/1132。**已改 `!USE_LOCAL_GWAS && file.exists(...)` 条件并物理删除旧缓存**。
4. **coloc 失眠 `s` 缺失**：失眠 clean 只注统一 N、无 icase/icontrol → coloc 每个位点被判 `s` 缺失而跳过。**已在 `GWAS_S` 补 `ukb-b-3957 = 0.30`**（UKB 自报失眠近似比例，待文献校准）。
5. **coloc lead 截断 200**：原设计 41 lead，本地化后 harmonized 2462 全当 lead 会极慢；截断最显著 200 作探索性近似（完整独立 LD-clump 待补）。
6. **jsonlite 间歇性被 WDAC 阻止**：首次 `library(TwoSampleMR)` 偶发 DLL 加载阻止，重试即恢复；启动慢时耐心等，勿误判为代码错。
7. **磁盘与内存**：clean 文件共约 1GB；`build_harmonized_local` 已加全局缓存（每文件只 fread 一次）+ 向量化等位基因对齐（去 for 循环，防 OOM/慢）。运行前确保磁盘余量 ≥15GB。
8. **`ukb-b-3957` 标识体系**：983 万行中 99.98% 为 rsID（仅 2298 个 UKB 风格 ID），与 ieu-b-2（100% rsID）直接 ID 匹配 795 万（79%）——**无需担心 ID 不匹配**，双向 harmonize 实测成功。

---

## 六、给 AI 的即拷即用执行指令模板

```
你负责执行失眠↔AD 因果研究 G1 阶段分析。
【目的】双向 MR（失眠↔AD）+ 区域 coloc + MRlap/cause 重叠校正，产出可投稿 G1 证据。
【数据】已预处理，直接读本地，勿联网取数：
  - 失眠 clean:   C:\D\workbuddy\科研\共病分析\data\raw\ukb-b-3957\ukb-b-3957.clean.tsv.gz
  - AD 主对 clean: C:\D\workbuddy\科研\共病分析\data\raw\ieu-b-2\ieu-b-2.clean.tsv.gz
  - AD 复制 GRCh37(供coloc): C:\D\workbuddy\科研\共病分析\data\raw\ebi-a-GCST90027158\GCST90027158_buildGRCh37.dedup.tsv.gz
  - AD 复制 GRCh38(供MR):   C:\D\workbuddy\科研\共病分析\data\raw\ebi-a-GCST90027158\GCST90027158_buildGRCh38.dedup.tsv.gz
【运行】cd 到 code 目录后执行：
  Rscript 01_bidirectional_mr_coloc.R > G1_run.log 2>&1
【配置】00_config.R 已锁定 GWAS_ID（insomnia=ukb-b-3957, ad=ieu-b-2, ad_alt=ebi-a-GCST90027158）。
【约束】不要修改 clean 文件；不要联网覆盖本地数据；跑完汇报：
  ① 双向 MR IVW 的方向/β/se/p；
  ② coloc PP.H4>0.80 的显著位点数；
  ③ MRlap/cause 是否实跑（LD 面板可取则跑，否则注明跳过）。
【排错】遇报错先对照同目录 AI操作分析提示词_失眠AD_G1.md 第五节“已知坑”。
```

---

## 七、质量与披露要求

- 三角验证需三源收敛；G1 单独不成稿。
- Limitations 必须披露：
  1. 失眠 `s=0.30` 为 UKB 自报失眠近似估计值（待文献校准）；
  2. coloc lead 截断 200 为探索性近似，完整独立 LD-clump 待补；
  3. rsID 转移式 liftover（非标准 chain）对 Bellenguez 约 50% 丢弃率对 coloc 的影响；
  4. MRlap/cause 若跳过须注明（零联网目标下的方法学局限）。
- 所有结论以重跑后 `results/` 实际输出为准，**不得引用早期 41/17 IVs 的中间结果**。
