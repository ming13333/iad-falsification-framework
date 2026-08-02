# 可复现性基础设施审计与 3A 完成清单

> 2026-08-02 | 执行 3A 基础设施硬化 + 框架升维配套产出

---

## 3A 交付状态总览

| 任务 | 状态 | 产物/处置 |
|------|------|----------|
| 3A.1 renv.lock | ✅ 已生成 | `/renv.lock`（手工重建，因 R 无法运行 `renv::snapshot()`） |
| 3A.2 set.seed 审计 | ✅ 已审计 | 关键脚本均已含 `set.seed()`（见下 §2） |
| 3A.3 代谢物 full SS 本地落盘 | ⚠️ 未执行 | 依赖 IEU OpenGWAS 网络；沙箱网络受限，列为投稿前待办 |
| 3A.4 手动 IVW 交叉验证 | ✅ 已产出 | `课题设计阶段/SupplementaryTable_IVW_crossval.md` |
| 3A.5 Git init + .gitignore | ✅ 已提交 | `.gitignore` + git repo，102 个文件纳入版本控制 |
| 3A.6 OSF 预注册修订 | ✅ 已修订 | `课题设计阶段/OSF预注册_失眠AD.md` 新增 §0.5 Revision Note + H1 修订标注 |

---

## 1. 3A.1 `renv.lock`

**背景**：R 环境在本机完全不可用——`TwoSampleMR 0.7.9` / `ieugwasr 1.1.0` / `data.table 1.18.4` 编译于 R-4.5.3，运行于 R-4.5.2 时 `library()` 加载即触发 ABI 段错误（20/20 复现）。因此无法运行 `renv::snapshot()`。

**处置**：依据正文 §四.3 的 Session Info 手工重建 `renv.lock`，列出关键包版本（TwoSampleMR、ieugwasr、MendelianRandomization、GenomicSEM、cause、loo、dplyr、data.table）及 Python 复现依赖（pyreadr、matplotlib、numpy）。文件含明确 Notes：投稿前须在可用 R 环境中用 `renv::snapshot()` 重新生成权威 lockfile，并附容器化声明。

---

## 2. 3A.2 set.seed 审计

**发现**：项目本地 `课题设计阶段/code/` 仅有部分脚本，但**规范 R 分析脚本实际位于 `C:/Temp/iad_g1/code/`**。对该目录的 `set.seed()` 检查结果：

| 脚本 | set.seed |
|------|----------|
| `01_bidirectional_mr_coloc.R` | 1 |
| `02b_g2_enhanced.R` | 1 |
| `04_mvmr.R` | 1 |
| `07_education_phewas_mr.R` | 1 |
| `09b_metabolite_mediation_slim.R` | 3 |
| `00_config.R` | 1 |
| Python 复现脚本 (`08h_steiger_py.py`, `ea0*.py`) | 已用 `np.random.RandomState` / `random.seed` |

**结论**：所有涉及 MCMC、bootstrap、置换等随机步骤的关键脚本均已固定种子。repro-guard 审计中的 "MVMR 缺 set.seed" 问题**已被解决**（该脚本含 `set.seed`）。

**注意**：当前项目目录 `C:/D/workbuddy/科研/共病分析/课题设计阶段/code/` 仅存有部分代码（00、01、02、03 等）。建议在投稿前把 `C:/Temp/iad_g1/code/` 中的规范分析脚本复制/合并到同一 Git 仓库，避免双轨代码。

---

## 3. 3A.3 代谢物 full summary statistics 落盘

**状态**：⚠️ 未完成。

**原因**：C1 代谢物中介当前依赖 IEU OpenGWAS 实时 API 提取（`met-d-*` 系列）。在沙箱环境中，GWAS Catalog 文件 CDN 已确认 404，IEU API 下载未成功测试。由于该步骤属于网络依赖且无新数值产生，本次执行未重复尝试；已列为正文 §四.3 / 局限 L10 的投稿前必做项。

**下一步（用户 / 投稿前）**：在可用网络环境下，对每个 `met-d-*` 代谢物 GWAS 下载完整 .tsv.gz，存放到 `data/metabolomics/` 并替换 API 调用路径；更新 `renv.lock` 与 Data Availability 声明。

---

## 4. 3A.4 手动 IVW 交叉验证表

已完成：`课题设计阶段/SupplementaryTable_IVW_crossval.md`。

核心结论：手动固定效应 IVW 与 TwoSampleMR 标准 `mr_ivw` 在教育→AD 主估计上存在约 5% 偏差（−0.311 vs −0.328），但不改变方向/显著性/核心结论。该偏差已在正文 §四.2（L8）显式披露。

---

## 5. 3A.5 Git 版本控制

- **仓库位置**：`C:/D/workbuddy/科研/共病分析/`
- **初始提交**：`7c1b951` "Phase 2B: framework elevation + 3A reproducibility infra"（102 个文件）
- **`.gitignore` 策略**：排除 `data/`、所有 `.rds`、`.tsv.gz`、`.csv.gz`、`.vcf.gz` 等大型二进制；保留 `.md` 文档、`.R`/`.py` 脚本、小型 `.csv` 结果。
- **已知问题**：规范 R 分析脚本仍在 `C:/Temp/iad_g1/code/`，未完全纳入本仓库。建议投稿前合并。

---

## 6. 3A.6 OSF 预注册 Revision Note

已完成：在 `课题设计阶段/OSF预注册_失眠AD.md` 新增 §0.5 Revision Note（2026-08-02），并将 §2 主假设 H1 标注为"原预注册 · 已被数据推翻"，同时给出修订后主结论。 OSF 冻结后须将本 Note 作为 Revision Note 附件发布。

---

## 7. 剩余可复现性风险（投稿前）

| 风险 | 当前状态 | 处置 |
|------|----------|------|
| R 环境 ABI 段错误 | 未解决 | 投稿前须换用匹配 R 版本或容器化环境 |
| 代谢物 full SS 未落盘 | 未执行 | 投稿前下载本地存档 |
| 双轨代码位置 | 未合并 | 投稿前把 `C:/Temp/iad_g1/code/` 合并到本仓库 |
| renv.lock 手工重建 | 已做但非自动生成 | 投稿前用 `renv::snapshot()` 重新生成 |

---

*说明：本审计与 `AI-repro-guard-audit-2026-08-01.md` 一脉相承；3A 完成后 repro-guard 中的 P0 高风险项（renv、set.seed、API 依赖披露、手动 IVW 偏差披露）已悉数处理或明确路径。*
