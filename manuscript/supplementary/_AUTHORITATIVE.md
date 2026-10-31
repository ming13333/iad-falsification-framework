# 唯一有效版本声明（补充表）

**本目录 `manuscript/supplementary/` 是投稿用补充材料的唯一来源。任何其他路径下的同名文件均不得上传。**

- 工作簿：`Supplementary_Tables.xlsx` — **12 个 sheet**，S8 为 24 列
- MD5：`cc3a8f3f31cee6d5de34e7922b6b066f`（58,305 B，2026-10-31 重建，S8 修正后）
- 生成脚本：`code/build_supplementary_workbook.py`（默认输出到本目录；`--rules` 开关控制三线边框，默认关以保持与归档逐字节一致）

> **2026-10-31 重建说明**：S8 的 `n_IV`（Education→AD 40→312，原值误填为 EAS 复制工具数）与 `IVW_beta`（Insomnia→AD −0.128→−0.130）修正后重建；旧 MD5 为 `2436d374408eb668572e8354985b2b20`（58,306 B，2026-10-28），对应 **Zenodo v1.2.1 归档版本**。投稿件一律以本目录工作簿为准；归档与投稿件的这一处差异属版本演进，不属冲突。
>
> S12 不在工作簿内是**设计如此**（S12 为含 5 个面板的散文式表，见 `build_supplementary_workbook.py` 文档串），但正文旧声明写"S1–S11"与正文 3 处引 S12 矛盾，已改为 **S1–S12**。

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
