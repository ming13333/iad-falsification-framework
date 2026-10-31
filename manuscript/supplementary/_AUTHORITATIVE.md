# 唯一有效版本声明（补充表）

**本目录 `manuscript/supplementary/` 是投稿用补充材料的唯一来源。任何其他路径下的同名文件均不得上传。**

- 工作簿：`Supplementary_Tables.xlsx` — **12 个 sheet**，S8 为 24 列
- MD5：`2436d374408eb668572e8354985b2b20`（58,306 B，2026-10-28 重建）
- 生成脚本：`code/build_supplementary_workbook.py`（默认输出到本目录；`--rules` 开关控制三线边框，默认关以保持与归档逐字节一致）

## 为什么只有这一版能用

| 判据 | 本版 | 旧版 |
|---|---|---|
| sheet 数 | **12**（含 S10_gate_ablation、S11_instrument_tiers、S12_threshold_robustness） | 9（无 S10–S12） |
| S8 列数 | **24**（含 `decisive_failure`、`score_v1`、`delta`、`grade_changed`、`G6_evidence`、`Egger_P_semantics`、`n_IV`） | 17（无这些列） |
| S8 四例分数 | **10 / 10 / 10 / 8 / 4**（G2 封顶后） | 12 / 12 / 12 / 10 / 4（封顶前） |
| 与正文/回信对齐 | Table 2 敏感度 0.878/0.724/0.691、S10/S11 均能对上 | 与 Table 2、回信 L192/L316 全部冲突 |

## 已隔离的旧制文件（2026-10-30）

| 原路径 | 现名 |
|---|---|
| `课题设计阶段/Supplementary/Supplementary_Tables.xlsx` | `Supplementary_Tables_SUPERSEDED_20260902.xlsx` |
| `课题设计阶段/Supplementary_final/Supplementary_Tables.xlsx` | `Supplementary_Tables_SUPERSEDED_20260902.xlsx` |
| `课题设计阶段/Supplementary/S8_twelve_case_validation.csv` | `..._SUPERSEDED_20260804.csv` |
| `课题设计阶段/Supplementary/S8_twelve_case_validation.md` | `..._SUPERSEDED_20260810.md` |
| `课题设计阶段/Supplementary/S9_simulation_operating.csv` / `.md` / `_marginal.csv` | `..._SUPERSEDED_20260902.*` |

`课题设计阶段/Supplementary_final/` 已用本目录的工作簿覆盖（MD5 同上，逐字节一致）。该目录缺 `S12_threshold_robustness.md`，**不要以该目录的 CSV 重建工作簿**——会缺 S12 sheet。

## S8 的三种载体分工（勿混）

| 载体 | 作用 | 是否带脚注 |
|---|---|---|
| `S8_twelve_case_validation.md` | 正文式补充表，**7 条脚注 + Scoring reproducibility 段落在此** | 是 |
| `S8_twelve_case_validation.csv` | 纯数据源，供程序读 | 否（CSV 不承载脚注） |
| `Supplementary_Tables.xlsx` 的 `S8_twelve_case_validation` sheet | 渲染版 | 否 |

回信 L192「footnotes 5–7, revised reproducibility paragraph」与 L316「footnotes 1–7」指的就是上表第一行——已兑现，核查时不要只看 CSV。
