# 环境依赖与软件版本清单（可复现性基础设施）

> 生成日期：2026-08-01 | 审计项 #4（renv.lock 缺失的替代方案）
> 采集方式：`packageVersion()` 于运行环境 R 4.5.2

## R 版本
- R 4.5.2 (2025-10-31 ucrt)

## 关键包版本
| 包 | 版本 | 用途 |
|----|------|------|
| TwoSampleMR | 0.7.9 | 双向 MR、LD-clump、harmonise、mr() |
| ieugwasr | 1.1.0 | IEU OpenGWAS API 提取、ld_clump |
| MendelianRandomization | 0.10.0 | MVMR (mr_mvinput / mr_mvivw / mr_mvegger) |
| GenomicSEM | 0.0.5 | LDSC rg（ldsc() 包装） |
| cause | 1.2.0.335 | CAUSE 方差混合模型（含 monkey-patch 兼容 loo 2.6+） |
| loo | 2.10.0 | CAUSE 的 LOO 交叉验证 |
| dplyr | 1.2.1 | 数据框操作 |
| data.table | 1.18.4 | 本地 clean 文件高速读取 |

## 未单独安装（已确认）
- MRInstruments：未单独安装（LD 面板与仪器经 IEU API 在线获取，非本地包）
- pander：未安装（仅用于报告渲染，不影响分析）

## 复现建议
1. 投稿前运行 `renv::init()` + `renv::snapshot()` 生成完整 `renv.lock`，锁定全部传递依赖。
2. 原始 GWAS 本地落盘：
   - `ukb-b-3957.clean.tsv.gz`（196 MB，失眠，UKB n=462,341）
   - `ieu-b-2.clean.tsv.gz`（185 MB，AD Kunkle，IGAP n=63,926）
   - 代谢物 `met-d-*` full summary statistics 建议下载存档以消除 IEU API 依赖（见 Phase2A §三.3 / L10）。
3. 所有脚本已统一 `set.seed(20260801)`（CAUSE 脚本沿用 `set.seed(20240721)`）。

## 运行环境
- Rscript：`C:/Program Files/R/R-4.5.2/bin/x64/Rscript.exe`
- LD scores：`C:/Temp/iad_g1/ld_ref/LDscore/`
- hm3：`C:/Temp/iad_g1/ld_ref/hm3_with_alleles.txt`
- ieugwasr 联网须禁用沙箱（否则 libcurl 段错误 139）。
