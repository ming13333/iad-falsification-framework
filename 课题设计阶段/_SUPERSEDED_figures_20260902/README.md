# 封顶归档：Fig1–Fig5 旧版（生成日 2026-08-04 / 2026-09-02）

**一句话结论**：本目录里的 **17 个文件**是 2026-09-02（Fig3 的 SVG 为 08-04）生成的**五张旧版图件**，已封顶（文件名带 `__SUPERSEDED_20260902`）。**任何投稿、外审投喂、返修补充材料、后续作图都不要用它们**；现版见 §1。

封顶日期：2026-11-01（两批：10:30 封 Fig2/Fig5 及其上传包；15:22 封 Fig1/Fig3/Fig4 位图与矢量）｜操作人：罗明 / AI 协作｜可逆：是（见 §4）

---

## 1. 现版权威文件（唯一可用）

**所有图件现按 Frontiers 规定的 180 mm 双栏宽度重画**（旧版是 19.05 cm = 7.5 in，超版心 10.6 mm，属不合规）；最小字号 8 pt、最细线 2 pt、分面 `(A)(B)(C)` 置于绘图区外。

| 图 | 位图 / 矢量（`manuscript/figures/`） | 投稿 TIFF（`figures_final/`） | 生成脚本 |
|---|---|---|---|
| Fig1 | `Fig1_six_gate_framework.{png,svg}` | 952,102 B · 18.00×18.16 cm | `code/make_fig1_six_gate.py`（**新增**，替换 Inkscape 手工合并） |
| Fig2 | `Fig2_simulation_operating.{png,svg}` | 362,802 B · 18.00×9.27 cm | `code/make_fig2_simulation.py` |
| Fig3 | `Fig3_case_study_MR.{png,svg}` | 313,744 B · 18.00×8.76 cm | `code/make_fig3_case_study.py`（**新增**，替换 Inkscape 森林图） |
| Fig4 | `Fig4_apoe_shared_liability.{png,svg}` | 240,414 B · 18.00×8.26 cm | `code/make_fig4_apoe_liability.py`（**新增**，替换错图） |
| Fig5 | `Fig5_validation_grading.{png,svg,pdf}` | 597,634 B · 18.00×14.86 cm | `code/make_fig5_validation.py` |

全部 400 dpi / RGB / LZW / ResolutionUnit=2；像素与源 PNG 逐点全等。逐文件哈希见 `figures_final/TIFF_manifest.csv`；上传包 `figures_final/Frontiers_Figures_upload.zip`（2.03 MB / 5 TIFF）。门禁 `python code/check_submission_figures.py` 全绿。

## 2. 为什么封顶

### 2.1 第一批（10:30，Fig2 / Fig5）

| 图 | 旧版问题 |
|---|---|
| **Fig2** | panel (b) 为**单口径**柱（旧 P(Grade A)≈0.90 一条柱）。现版改为**三柱双口径**：D-only 0.80、C/D 0.88、FDR 另列，与正文 Results、Figure 2 图注、Table 2 脚注的双口径表述对齐。旧图会与正文文字直接冲突。 |
| **Fig5** | 09-02 生成，早于 10-27/10-28 对图 5 的重制；内含早期分级口径（教育→AD 仪器的 `n_IV`、12 例评分表述等后续已修订）。 |
| **`Frontiers_Figures_upload.zip`** | 内含 5 张 09-02 的 TIFF，其中 Fig2、Fig5 两张即上述旧版。留着会被当作投稿上传包直接上传。 |

### 2.2 第二批（15:22，Fig1 / Fig3 / Fig4）

| 图 | 旧版问题 |
|---|---|
| **Fig1** | 19.05 cm 版面；由 6000×6317 组合图 clipPath 裁切，**不可复现**（无生成脚本）。现版 18.00×18.16 cm、8 pt 起。 |
| **Fig3** | 19.05 cm 版面；Inkscape 手工合并的森林图，**不可复现**（SVG 生成于 08-04）。现版 18.00×8.76 cm，并附 `make_fig3_case_study.py`（七个存档 MR 估计值硬编码于 `EST` 列表）。 |
| **Fig4** | **内容本身是错图**：磁盘上那张实际是「五维三角验证汇总」，与 Figure 4 图注、正文 Results 的 *APOE* 位点共享负债表述**完全不符**。新图从 `manuscript/supplementary/S1_coloc_loci.csv` 重画，并对 47/32 检测、1/18 强共享、16 在 APOE、2 在 chr11p11.2、0 其他做 `assert` 防漂移。 |

> 两批都只做"改名 + 迁入本目录"，**没有删除任何像素或矢量内容**。`figures_final/` 现仅剩 5 张 TIFF + 上传包 + `TIFF_manifest.csv` + `README_CURRENT.md`，可直接整包投出。

## 3. 文件清单（17 个文件，11,633,980 字节）

`from_figures/`（原在 `课题设计阶段/figures/`）：

| 归档文件名 | 字节 | sha256[:16] | 原文件名 |
|---|---|---|---|
| `Fig2_simulation_operating__SUPERSEDED_20260902.jpg` | 975,094 | `c0655865fe27d4a5` | `Fig2_simulation_operating.jpg` |
| `Fig2_simulation_operating__SUPERSEDED_20260902.pdf` | 70,811 | `6565db578f69da63` | `Fig2_simulation_operating.pdf` |
| `Fig5_validation_grading__SUPERSEDED_20260902.jpg` | 1,082,284 | `fa2e6dcf2acf4081` | `Fig5_validation_grading.jpg` |

`from_figures_final/`（原在 `课题设计阶段/figures_final/`）：

| 归档文件名 | 字节 | sha256[:16] | 原文件名 | 批次 |
|---|---|---|---|---|
| `Fig1_six_gate_framework__SUPERSEDED_20260902.jpg` | 1,295,309 | `e5576341a45d09f0` | `Fig1_six_gate_framework.jpg` | 2 |
| `Fig1_six_gate_framework__SUPERSEDED_20260902.png` | 818,575 | `709f288be96b304b` | `Fig1_six_gate_framework.png`（19.05 cm） | 2 |
| `Fig1_six_gate_framework__SUPERSEDED_20260902.svg` | 109,498 | `110a1ebbe21fb9d3` | `Fig1_six_gate_framework.svg`（Inkscape 裁切版） | 2 |
| `Fig2_simulation_operating__SUPERSEDED_20260902.png` | 363,542 | `9aad8397088b9cbb` | `Fig2_simulation_operating.png`（600 dpi, 4034×1558） | 1 |
| `Fig2_simulation_operating__SUPERSEDED_20260902.svg` | 34,839 | `3ee85249815e3724` | `Fig2_simulation_operating.svg` | 1 |
| `Fig2_simulation_operating__SUPERSEDED_20260902.tiff` | 572,408 | `83ed9c0eb0e8aaf0` | `Fig2_simulation_operating.tiff`（LZW/RGB） | 1 |
| `Fig3_case_study_MR__SUPERSEDED_20260902.png` | 520,007 | `0e682b4fa85058e9` | `Fig3_case_study_MR.png`（19.05 cm） | 2 |
| `Fig3_case_study_MR__SUPERSEDED_20260902.svg` | 158,624 | `e136319d76cfafe8` | `Fig3_case_study_MR.svg`（Inkscape 合并版） | 2 |
| `Fig4_apoe_shared_liability__SUPERSEDED_20260902.png` | 411,542 | `bec73b505a81f8de` | `Fig4_apoe_shared_liability.png`（**错图**：五维三角验证汇总） | 2 |
| `Fig4_apoe_shared_liability__SUPERSEDED_20260902.svg` | 10,857 | `59dc194876f186d0` | `Fig4_apoe_shared_liability.svg`（**错图**） | 2 |
| `Fig5_validation_grading__SUPERSEDED_20260902.png` | 696,536 | `8ad43a3ed25838ac` | `Fig5_validation_grading.png`（800 dpi, 6000×3313） | 1 |
| `Fig5_validation_grading__SUPERSEDED_20260902.svg` | 24,622 | `4f78daf5dc2cd3aa` | `Fig5_validation_grading.svg` | 1 |
| `Fig5_validation_grading__SUPERSEDED_20260902.tiff` | 1,340,218 | `8ad81a576b06bcd1` | `Fig5_validation_grading.tiff` | 1 |
| `Frontiers_Figures_upload__SUPERSEDED_20260902.zip` | 3,149,214 | `0720f82ab61e2e8f` | `Frontiers_Figures_upload.zip`（5 TIFF 上传包） | 1 |

逐文件完整哈希见 `SHA256SUMS.txt`，原路径 / 理由见 `PROVENANCE.csv`（17 行）。

校验：在项目根执行 `sha256sum -c "课题设计阶段/_SUPERSEDED_figures_20260902/SHA256SUMS.txt"`（GNU 格式 `sha256<两空格>路径`，路径相对项目根）。

> ⚠️ **本目录的二进制文件只在本地**：`.gitignore` 第 35 行排除了 `from_figures_final/`（第 32 行排除了 `figures_final/`），仓库里只有 `README.md` / `PROVENANCE.csv` / `SHA256SUMS.txt` 三份台账。克隆仓库后跑上面的校验会 17 行全部 `No such file`，属预期；台账的作用是记录"哪些文件被封顶过、原来是什么哈希"，不是可复现的存档源。

## 4. 备份与恢复

- **独立备份**：`备份figure/_SUPERSEDED_backup_20261101/{from_figures,from_figures_final}/`。**注意**：该备份只含第一批 10 个文件；第二批 7 个文件的原件只在一次 `shutil.move` 前后各做了一次哈希比对（移动前后 sha256 相同），未另建独立副本。
- **恢复单个文件**：
  ```bash
  cp "课题设计阶段/_SUPERSEDED_figures_20260902/from_figures_final/Fig2_simulation_operating__SUPERSEDED_20260902.tiff" \
     "课题设计阶段/figures_final/Fig2_simulation_operating.tiff"
  ```
- **恢复后请同步**：`figures_final/README_CURRENT.md` 与 `progress.md` 的图件清单，否则记录会与实际不符。
- **但一般不该恢复**：五个图现在都能由 `code/make_fig*.py` 一条命令重画，恢复旧件等于回退到不合规版面。

## 5. 遗留待办

1. `figures_final/` 这个目录名本身有误导性（历史命名，不等于"最终"）。现内容已是当版权威，但名字仍可能误导；是否改名待定。
2. `课题设计阶段/figures/` 目录内仍有 Fig1–Fig5 的 png/svg/pdf 副本（与 `manuscript/figures/` 同版或近似同版）。历史出现过"两处同名文件 sha256 不同"的情况，**投稿一律以 `manuscript/figures/` 为准**。
3. `备份figure/_SUPERSEDED_backup_20261101/_PLAN.json` 只登记了第一批，若日后要做完整可逆性审计，需补第二批。
