# 失眠 ↔ 阿尔茨海默病 · 三法整合分析代码框架

把 G1（双向 MR + 共定位）、G2（血浆蛋白两步中介 MR）、G4（多状态发病顺序模型）整合为一套因果三角验证分析。

## 运行环境要求

- **R ≥ 4.3**，需安装：
  - CRAN：`TwoSampleMR`、`ieugwasr`、`msm`、`mstate`、`survival`、`dplyr`、`data.table`、`ggplot2`
  - Bioconductor：`coloc`（`BiocManager::install("coloc")`）
  - 可选：`MR-PRESSO`（`devtools::install_github("rondolab/MR-PRESSO")`）
- **网络**：需能访问 IEU / OpenGWAS（`api.opengwas.io`）拉 GWAS 汇总统计；UKB-PPP 蛋白 pQTL 汇总统计。当前 WorkBuddy 沙箱对 GWAS REST API 有网关白名单限制，**请在本地可联网 R 环境执行**。
- **UKB 权限**：G4 需 UKB 个体级数据申请（字段 2245/2255、住院 ICD-10 G47.0/F00/G30、死亡登记、APOE 等）。

## 执行顺序

```r
source("00_config.R")              # 先改 TODO：路径 + GWAS ID + 蛋白 panel 覆盖核查
source("01_bidirectional_mr_coloc.R")  # G1：双向 MR + 共定位 → 结果/G1_bidirectional.rds
source("02_protein_mediation.R")       # G2：血浆蛋白两步中介 → 结果/G2_protein_mediation.rds
source("03_multistate_onset.R")        # G4：多状态顺序模型（需先填 UKB 长表）
```

## 各脚本要点

| 文件 | 组件 | 关键产出 | 主要 TODO |
|------|------|----------|-----------|
| `00_config.R` | 全局配置 | GWAS ID / 阈值 / 协变量 | 替换真实 ID 与路径 |
| `01_*.R` | G1 双向 MR+共定位 | 正/反向 MR、Steiger、coloc PP.H4 | 构建 coloc dataset |
| `02_*.R` | G2 蛋白两步中介 | b1×b2 中介、FDR、top 蛋白 | 加载 UKB-PPP 蛋白 ID；真实 P 值 |
| `03_*.R` | G4 多状态顺序 | 转移强度 q、路径对比、分层生存 | 载入 UKB 个体级长表 |

## 三角验证逻辑（见设计文档第四节）

G1 方向 + G2 机制 + G4 时序三者是否一致收敛：一致 ⇒ 失眠为 AD 上游可因果/可机制靶点；不一致 ⇒ 纠偏型结论（失眠或为 AD 临床前标记）。

## 预注册

分析前在 OSF 锁定：暴露=失眠、结局=AD、协变量=年龄/性别/教育/抑郁/APOE ε4/安眠药、敏感性清单（见设计文档第六节）、显著性阈值。
