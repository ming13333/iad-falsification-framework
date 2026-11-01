# 封顶归档：Fig2 / Fig5 旧版（生成日 2026-09-02）

**一句话结论**：本目录里的 10 个文件是 2026-09-02 生成的 **Fig2、Fig5 旧版**，已封顶（文件名带 `__SUPERSEDED_20260902`）。**任何投稿、外审投喂、返修补充材料、后续作图都不要用它们**；现版见下表。

封顶日期：2026-11-01　|　操作人：罗明 / AI 协作　|　可逆：是（见 §4）

---

## 1. 现版权威文件（唯一可用）

| 图 | 权威路径 | 字节 | sha256[:16] | 生成方式 |
|---|---|---|---|---|
| Fig2 | `manuscript/figures/Fig2_simulation_operating.{png,svg}` | 289,607 / 123,741 | `6b4dff57582a7fe2` / `0d554127788432b8` | `code/make_fig2_simulation.py`（**2026-11-01 12:36 按印制尺寸 7.5 in 重排**；10:22 宽幅版已留档 `备份figure/Fig2_wide_canvas_20261101/`） |
| Fig5 | `manuscript/figures/Fig5_validation_grading.{png,svg,pdf}` | 577,386 / 126,774 / 38,493 | `32dafee60a6aa90a` / `e72130425176b37d` / `5ba45e88183eb268` | 2026-10-27/28 重制版 |

`课题设计阶段/figures/` 下的同名 Fig2(png/svg)、Fig5(png/svg/pdf) 与上述**逐字节一致**（Fig5 的 svg 例外，见 §5 脚注 1），可视为同一份。

## 2. 为什么封顶

| 图 | 旧版问题 | 处置依据 |
|---|---|---|
| **Fig2** | panel (b) 为**单口径**柱（旧 P(Grade A)≈0.90 一条柱）。现版改为**三柱双口径**：D-only 0.80、C/D 0.88、FDR 另列，与正文 Results、Figure 2 图注 (b)、Table 2 脚注的双口径表述对齐。旧图会与正文文字直接冲突。 | 2026-11-01 按"候选版重画"指令重跑 `code/make_fig2_simulation.py` |
| **Fig5** | 09-02 生成，早于 10-27/10-28 对图 5 的重制；像素与矢量均与现版不一致，内含早期分级口径（教育→AD 仪器的 `n_IV`、12 例评分表述等后续已修订）。 | 同属"未封顶旧图"，与 Fig2 一并处理 |
| **`Frontiers_Figures_upload.zip`** | 内含 **5 张 09-02 的 TIFF**，其中 Fig2、Fig5 两张即上述旧版。留着会被当作投稿上传包直接上传。 | 整包含旧图，故整包封顶 |

> 只做了"改名 + 迁入本目录"，**没有删除任何像素或矢量内容**，也没有改动 Fig1/Fig3/Fig4（`figures_final/` 现仅剩这三张，均已核验与 `manuscript/figures/` 逐字节一致）。

## 3. 文件清单

`from_figures/`（原在 `课题设计阶段/figures/`）：

| 归档文件名 | 字节 | 原文件名 |
|---|---|---|
| `Fig2_simulation_operating__SUPERSEDED_20260902.jpg` | 975,094 | `Fig2_simulation_operating.jpg` |
| `Fig2_simulation_operating__SUPERSEDED_20260902.pdf` | 70,811 | `Fig2_simulation_operating.pdf` |
| `Fig5_validation_grading__SUPERSEDED_20260902.jpg` | 1,082,284 | `Fig5_validation_grading.jpg` |

`from_figures_final/`（原在 `课题设计阶段/figures_final/`）：

| 归档文件名 | 字节 | 原文件名 |
|---|---|---|
| `Fig2_simulation_operating__SUPERSEDED_20260902.png` | 363,542 | `Fig2_simulation_operating.png`（600 dpi, 4034×1558） |
| `Fig2_simulation_operating__SUPERSEDED_20260902.svg` | 34,839 | `Fig2_simulation_operating.svg` |
| `Fig2_simulation_operating__SUPERSEDED_20260902.tiff` | 572,408 | `Fig2_simulation_operating.tiff`（LZW/RGB） |
| `Fig5_validation_grading__SUPERSEDED_20260902.png` | 696,536 | `Fig5_validation_grading.png`（800 dpi, 6000×3313） |
| `Fig5_validation_grading__SUPERSEDED_20260902.svg` | 24,622 | `Fig5_validation_grading.svg` |
| `Fig5_validation_grading__SUPERSEDED_20260902.tiff` | 1,340,218 | `Fig5_validation_grading.tiff` |
| `Frontiers_Figures_upload__SUPERSEDED_20260902.zip` | 3,149,214 | `Frontiers_Figures_upload.zip`（5 TIFF 上传包） |

合计 10 个文件、8,309,568 字节。逐文件哈希见 `SHA256SUMS.txt`，原路径/理由见 `PROVENANCE.csv`。

校验：在项目根执行 `sha256sum -c "课题设计阶段/_SUPERSEDED_figures_20260902/SHA256SUMS.txt"`（GNU 格式 `sha256<两空格>路径`，路径相对项目根；2026-11-01 实测 10/10 OK）。

## 4. 备份与恢复

- **独立备份**（封顶前先做，哈希逐个校验通过）：
  `备份figure/_SUPERSEDED_backup_20261101/{from_figures,from_figures_final}/`（10 个文件 + `_PLAN.json`，原名保留，未加后缀）
- **恢复单个文件**：
  ```bash
  cp "备份figure/_SUPERSEDED_backup_20261101/from_figures_final/Fig2_simulation_operating.tiff" \
     "课题设计阶段/figures_final/Fig2_simulation_operating.tiff"
  ```
- **恢复后请同步**：`课题设计阶段/figures_final/README_CURRENT.md` 与 `progress.md` 的图件清单，否则记录会与实际不符。

## 5. 遗留待办

1. ~~**`figures_final/` 现缺 Fig2、Fig5 的 TIFF**~~ ✅ **2026-11-01 12:37 已完成**：脚本 `code/export_submission_tiff.py`。5 张 TIFF 版面统一到 19.03–19.06 cm（Fig1 800 / Fig2 400 / Fig3 871 / Fig4 618 / Fig5 704 dpi），LZW/RGB/8bit，像素与源 PNG 全等；`Frontiers_Figures_upload.zip` 重建为 2.92 MB / 5 TIFF。**旧 zip 已封顶，不可再用。** 另：Fig2 已于 12:36 按印制尺寸重排，印出最小字号 6.5 pt（原宽幅版压缩后仅 ≈5.6 pt）。
2. `figures_final/` 这个目录名本身有误导性（历史命名，不等于最新）。是否改名为 `figures_submission_20260902/` 或直接退役，待定。
3. 脚注 1：`课题设计阶段/figures/Fig5_validation_grading.svg` 与 `manuscript/figures/Fig5_validation_grading.svg` 字节数同为 126,774 但 sha256 不同（`f74b33f8…` vs `e7213042…`），推测为重新导出时的元数据/时间戳差异；**投稿一律以 `manuscript/figures/` 为准**，此项未深究。
