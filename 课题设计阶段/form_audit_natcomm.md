# Nature Communications 投稿形式审查报告
**文件**：`manuscript_draft_natcomm.md`（Nat Commun 压缩版，含 5 主图 + 5 补充图 + 8 补充表）
**审查依据**：Nature Portfolio 官方政策（nature.com/ncomms/submit/how-to-submit、nature.com/documents/aj-artworkguidelines.pdf、research-figure-guide.nature.com）、用户指定 reporting-standards 页（STROBE-MR / Nature Reporting Summary 要求）。Nature 官网对本机 IP 返回 406 拦截，以下政策条款来自其官方页面被第三方镜像与搜索引擎完整转引的内容。
**审查日期**：2026-08-05

---

## 一、结论速览

| 等级 | 数量 | 说明 |
|------|------|------|
| 🔴 **必须修改（投稿/送审阻塞项）** | 6 | 缺强制结构段、内部草稿残留、计数矛盾、主图格式违规 |
| 🟠 **强烈建议（避免退修/延迟）** | 5 | 报告摘要模板、STROBE-MR 独立文件、配色/字体核验、关键词、SI 整合 |
| 🟡 **次要（house style 微调）** | 4 | 面板标签大小写、参考文献 & 符号、摘要词数余量、图例表述 |

---

## 二、🔴 必须修改项（阻塞项）

### B1. 缺失 Nature 强制结构段
Nature Communications **强制要求**以下独立段落，当前稿件**完全没有**：
- **Author contributions**（作者贡献，CRediT 分类）
- **Competing interests**（利益冲突声明，无冲突亦须明示 "The authors declare no competing interests."）
- **Funding**（基金资助，含基金号）
- **Acknowledgements**（致谢，可选但建议；ORCID 关联在系统层完成）
- **Keywords**（3–5 个关键词，Nature 投稿系统必填字段）

> 缺任意一项，投稿系统（MTS）会在 technical check 阶段退回或编辑直接 desk return。**最高优先级。**

### B2. 内部草稿残留（必须删除后再投稿）
以下两段是写作/审计过程的脚手架，不属于文章本体，投稿前**必须移除**：
- 顶部引用块（第 3–5 行）："**版本说明：Nature Communications 投稿格式压缩版…**"
- 文末（第 253–255 行）："## Notes on citation style and crossref validation" 整段

### B3. 计数矛盾：摘要 "eleven additional" vs 正文 "twelve"
- 摘要（第 9 行）："Across **eleven additional** trait pairs…" 但随后枚举了 **12 对**（含 insomnia→AD）。
- 正文（L6、Discussion、S8）**一致使用 "twelve trait pairs"**，且 S8 列举 12 例（含 insomnia→AD）。
- 摘要枚举的 12 对 = 4(Grade A) + 1(Grade B) + 4(Grade C) + 3(Grade D) = 12，**已包含 insomnia→AD**。
- **修复**：将摘要 "eleven additional trait pairs" 改为 **"twelve trait pairs"**（或 "twelve trait pairs, including the insomnia–AD test case"）。这是编辑/审稿人必查的数字一致性硬伤。

### B4. 主图文件格式违规（PNG 不被接受）
Nature 对**主图**明确规定：
> "We do not accept the following formats: .jpeg, .tiff, **.png**, Canvas, DeltaGraph, Tex, ChemDraw, SigmaPlot."
> 主图要求矢量文件：**.ai / .eps / .pdf**（首选，保留可编辑层）；.svg 仅接受 *plain svg*（非 Inkscape svg）。

当前图表文件状况：
| 文件 | 格式 | 风险 |
|------|------|------|
| Fig1_framework_hierarchy.**png** | 位图 | 🔴 不被接受 |
| Fig2_MR_forest_coloc.**png** | 位图 | 🔴 不被接受 |
| Fig3_education_phewas.**png** | 位图 | 🔴 不被接受 |
| Fig4_education_phewas.**png** | 位图 | 🔴 不被接受（注：正文 Fig4 引用的是 Fig4_mediation_gate.svg，需确认实际提交图） |
| SuppFig3C_volcano.**png** | 位图 | 🟠 补充图，建议转 PDF/EPS |
| SuppFig5_simulation_operating.**png** | 位图 | 🟠 补充图，建议转 PDF/EPS |
| Fig1/2/3/4/5、SuppFig3A/B/C/4/5 **.svg** | 矢量 | ✅ 可用（matplotlib 导出的 plain svg；转 PDF 更稳妥） |

> **修复**：所有主图导出为 **PDF 或 EPS**（矢量）；PNG 一律替换。SVG 可保留但建议一并转 PDF（Nature 生产环节对 PDF 兼容性最佳）。补充图按 Extended Data 规则导出 JPEG(preferred)/TIFF/EPS。

### B5. 多面板图物理标签无法核验（Fig2 / Fig4 / SuppFig5）
- 图例明确引用面板：Fig2 **(A)(B)**、Fig4 **(A)(B)(C)**、SuppFig5 **Panel A/B/C**。
- SVG 解构显示：Fig2 / Fig4 / SuppFig5 / Fig3 / SuppFig3C **不含 `<text>` 节点**（文本被 matplotlib 转为 path，fonttype=path）——这本身对生产是**好事**（无字体依赖、可缩放），但也意味着**程序无法确认面板标签 a/b/c 是否真的画在图上**。
- Fig1 ✅ 含面板标签 a/b/c（与图例 Panel a/b/c 对应）；Fig5 的 A/B/C/D/F 是等级/列名而非面板标签（Fig5 为单面板，无需面板标签）。
- **修复**：目视确认 Fig2、Fig4、SuppFig5 三张多面板图**确实带有小写加粗 a / b / c 物理标签**，位置与图例一致。缺失则须在导出前补上。

### B6. Nature Reporting Summary 未准备
用户指定的 reporting-standards 页即对应 Nature 投稿系统的**标准化 Reporting Summary 模板**（生命科学用 Life Sciences Reporting Summary）。这是 Nature Communications **投稿时必交的独立文件**（与手稿、图表分开上传）。当前稿件未包含。
> 同时，本研究的 EQUATOR 报告规范是 **STROBE-MR**（稿件 S5 已列为 STROBE-MR checklist）——须确保该清单**已逐项填写并作为独立文件上传**，而非仅藏在 SI 文字里。

---

## 三、🟠 强烈建议项

### S1. 配色色盲安全（已初步核验，建议最终目检）
- SVG 解构结果：**未发现红–绿配对**（仅 SuppFig4 决策树用了红色 `#e65100/#c62828` 作为单色高亮，非红绿对比），整体**大概率色盲安全** ✅。
- 仍建议：用色盲模拟器（如 Coblis）对 Fig2 森林图、Fig5 分级表（四色）、SuppFig5 三面板做一次目检，确保不依赖红绿区分。

### S2. 字体与字号（部分图需显式声明）
- Fig1 / Fig5 / SuppFig4 显式使用 **Arial**（符合 Nature 要求 Helvetica/Arial）✅。
- Fig2 / Fig3 / Fig4 / SuppFig5 / SuppFig3C 因文本转 path **无 font-family 声明**——渲染后字体为 matplotlib 默认 DejaVu Sans（无衬线，可接受），但建议在生产导出时**显式设 `font.family='Arial'` / `Helvetica`** 以完全贴合 Nature 偏好。
- 字号须落在 **5–7 pt**（最终出版缩放后可读）；线条最细 ≥ 1 pt。

### S3. 面板标签大小写（house style）
Nature 要求多面板标签用**小写加粗 a, b, c**（与图中其他文字同字号）。稿件正文/图例使用大写 "Fig. 2A"、"Fig. 2B"、"(A)""(B)"——图例与正文引用建议统一为小写 **a/b/c**（图内标签亦须小写加粗）。属排版微调，编辑排版阶段也会处理，但提前统一可减少返工。

### S4. 摘要词数余量
- 实测摘要 **199 词**（Nature 上限通常 200 词）。处于临界，**建议删减 5–10 词**留余量（如 "the insomnia–Alzheimer's disease (AD) association as a challenging test case" 可精简），避免不同计数口径下超限。

### S5. 补充材料（SI）整合为单 PDF
Nature 要求 SI 作为**单一 PDF** 提交（含 Supp Fig 3A/B/C、4、5 与 Supp Table S1–S5、S7–S9、Note 1–3）。当前 SI 为分散的 markdown/CSV。投稿前须合并导出为一份 PDF，并确认 Supp Table 编号连续（当前跳过了 S6——属有意为之，正文无 S6 引用，✅ 无悬空引用）。

---

## 四、🟡 次要（house style 微调）

### M1. 参考文献格式
当前格式基本合规（编号、作者、期刊斜体、卷加粗、年、doi），两处偏离 Nature 习惯：
- 末位作者前用逗号，Nature 偏好 **`&`**（如 "Burgess S, Butterworth A & Thompson SG"）。
- "doi:" 前缀可改为完整 `https://doi.org/...`（Nature 线上版格式）。
- "et al." 用法可接受（≤5 作者列全，否则 et al.）。
> 属生产阶段排版范畴，可暂不改，但建议投稿前统一。

### M2. 图例表述
- 图例整体自包含、定义了符号，✅ 符合要求。
- 个别处 "Fig. 2A" 等在正文引用，建议与面板标签小写统一（见 S3）。

### M3. 图表数量在限额内
- Nat Commun：主图+表 ≤ 10，补充图 ≤ 8（如有充分理由）。当前 5 主图 + 5 补充图 ✅ 合规。

### M4. 初始投稿 vs 最终投稿
- **初始投稿**：图可内嵌正文（当前 markdown 即此形态），系统接受。
- **修回/接受后**：须上传**独立矢量文件**（PDF/EPS），见 B4。

---

## 五、逐项修复行动清单（建议执行顺序）

1. 删除 B2 两处草稿残留（版本说明块、crossref 注释段）。
2. 补全 B1 五大结构段（Author contributions / Competing interests / Funding / Acknowledgements / Keywords）。
3. 修正 B3 摘要 "eleven additional" → "twelve trait pairs"。
4. 导出 B4 主图为 PDF/EPS，替换所有 PNG。
5. 目视核验 B5（Fig2/Fig4/SuppFig5 面板 a/b/c 标签）。
6. 准备 B6 Nature Reporting Summary + 独立 STROBE-MR 清单文件。
7. 完成 S1–S5 核验与整合。
8. 统一 M1–M3 排版细节。

---

## 六、图表合规速查表

| 图 | 引用面板 | 文件格式 | 字体 | 面板标签 | 状态 |
|----|---------|---------|------|---------|------|
| Fig1 | a/b/c | svg(png 备份) | Arial ✅ | a/b/c ✅ | 需转 PDF |
| Fig2 | A/B | png 🔴 | path | 需目检 | 转 PDF + 补标签 |
| Fig3 | 单面板 | png 🔴 | path | — | 转 PDF |
| Fig4 | A/B/C | svg(+png) | path | 需目检 | 转 PDF + 补标签 |
| Fig5 | 单面板 | svg | Arial ✅ | — | 转 PDF |
| SuppFig3A/B/C | 单/多 | svg | path | 需目检 | 转 PDF/EPS |
| SuppFig4 | 单面板 | svg | Arial ✅ | — | 转 PDF |
| SuppFig5 | A/B/C | png/svg | path | 需目检 | 转 PDF + 补标签 |

**总评**：内容层面的数字一致性（B3）与强制结构段（B1）是最大阻塞；图表技术格式（B4 PNG 违规）是 Nature 明确拒收项，须在最终投稿前全部转矢量。配色与字体已初步符合，仅需目检确认。
