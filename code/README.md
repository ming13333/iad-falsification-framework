# 代码树说明（双轨合并）

本项目曾分两条代码轨道：
- **R 轨道**（原始分析）：`C:/Temp/iad_g1/code/`
- **Python 轨道**（R 崩溃后的重实现）：项目 `code/`

自 2026-08-02 起 R 环境恢复可用（见 MEMORY / skill `r-segfault-pyreadr-workaround`），现将 R 规范脚本并入仓库，消除双轨。

## 目录结构

### `code/` — 主代码目录（Python + 主动 R 脚本）
- `08h_steiger_py.py` — Steiger 方向性检验纯 Python 实现（MR 分歧核心证据）
- `ea01_liftover_gard.py` / `ea02_instruments.py` / `ea03_harmonize.py` / `ea04_mr.py` — 东亚（EA）教育→AD 复制 MR
- `make_figures.py` — Fig1/2/5 核心图生成
- `cache_c1_inputs.R` — 在线抓取 C1 代谢物中介的 harmonised 输入并本地落盘（→ `data/raw/c1_cache/`）
- `local_run_C1.R` — **零 API** 复现 C1 中介结果（读 `c1_cache/`）

### `code/r_analysis/` — 规范 R 分析脚本（从 `C:/Temp/iad_g1/code/` 合并）
| 脚本 | 对应模块 |
|------|---------|
| `00_config.R` | 全局配置 |
| `01_bidirectional_mr_coloc.R`, `01b_overlap_correction.R`, `01c_cause_patched.R`, `01d_g1_wrapup.R`, `01e_cause_fwd_ns1000.R`, `01f_cause_clumped.R` | G1 双向 MR + CAUSE + clump 敏感性 |
| `02_g2_open_gwas.R`, `02b_g2_enhanced.R` | G2 蛋白中介（CRP/IL-6→AD） |
| `04_mvmr.R` | MVMR（教育直接效应） |
| `05_g1_verify.R` | G1 结果核验 |
| `06_ldsc_genetic_correlation.R`, `06b_ldsc_diag.R`, `06c_ldsc_final.R` | LDSC 遗传相关（全基因组 + 去 APOE） |
| `07_education_phewas_mr.R` | 教育 PheWAS（AD/PD/MS） |
| `08_steiger_eaf.R`, `08c_steiger_final.R` | Steiger 方向性（R 版，后被 Python 替代） |
| `09_metabolite_mediation.R`, `09b_metabolite_mediation_slim.R` | C1 代谢物中介（原在线版 / slim 版） |
| `10b_power_calc_eas.R` | EA 复制 power calc |
| `B1_fetch_opengwas.R`, `B1_fetch_ukbppp.py`, `B1_verify.py` | 蛋白 pQTL 取数 / 验证 |
| `package_versions.md` | 环境依赖版本清单 |

## 复现要点
- **R 版本**：`C:/Program Files/R/R-4.5.2`（包编译于 4.5.3，仅 warning，可正常运行）。
- **路径**：规范 R 脚本内路径仍指向 `C:/Temp/iad_g1/...`（历史存档）；主动脚本（`cache_c1_inputs.R`/`local_run_C1.R`）使用项目相对路径。
- **IEU 下载**：静态 full-SS 端点已失效（301→404）；`extract_instruments` 限 `pval≤0.01`；`associations(id, variants=)` 可批量取特定变体。C1 复现改用本地缓存（`data/raw/c1_cache/`）。
