# 参考文献审计报告 — Genome Medicine 投稿稿（manuscript_GenomeMedicine_submission.docx）

**审计日期**：2026-08-09　|　**对象**：79 条参考文献 + 全文 58 处文内引用标记
**方法**：① 程序化解析 docx/md 提取引用与文献表；② 79 条 DOI 逐一查询 Crossref API 比对元数据；③ 按 BMC/Vancouver 规则检查格式与排序。
**审计脚本**：`code/ref_audit_parse.py`、`code/ref_audit_crossref.py`、`code/ref_audit_compare2.py`、`code/ref_audit_bmc_list.py`

---

## 一、结论摘要

| 检查项 | 结果 | 严重度 |
|--------|------|--------|
| 引用覆盖度（悬空/未引） | ✅ 79/79 全被引用，无悬空引用，无未引用条目 | — |
| DOI 有效性（Crossref） | ✅ 79/79 全部解析成功，无失效/缺失 DOI | — |
| 核心字段（年份/卷/页码/首作者） | ✅ 基本一致（仅 2 处年份口径 + 若干无害页码缩写） | — |
| **标题准确性** | ⚠️ **约 40+ 条标题被截断/改写**，与官方标题不符 | **中-高** |
| **排序（按首引顺序编号）** | ❌ **参考文献 51–79 违反首引顺序**（29 条需重编号） | **高** |
| **引用内容对应** | ❌ **ref35/37 所引论文实际主题与稿件声称不符**；ref43 引错位置 | **高** |
| 格式（BMC/Vancouver） | ❌ 现行为 Nature 风格（斜体期刊、加粗卷号、"页码 (年份)"、"doi:"前缀），非 BMC 要求 | **中** |

---

## 二、覆盖度检查 ✅

- 文内引用标记共 **58 处**（含区间与并列，如 `[2-5]`、`[13-17,32,39,43,60-63]`），展开后覆盖 **79/79** 个编号。
- 悬空引用（文中引用但文献表缺失）：**0**
- 未引用条目（文献表有但正文从未引用）：**0**

---

## 三、Crossref 元数据校验 ✅（重点：发现标题与个别条目不符）

### 3.1 全部 DOI 有效
79 条均含 DOI 且经 `api.crossref.org` 解析成功（79/79 OK）。无失效、无重复 DOI。

### 3.2 核心字段比对（稿件 vs Crossref）
- **年份**：77/79 完全一致。两处例外均为口径问题：
  - ref10 Lawlor 2016：Crossref 该记录仅存在线日期（2017-01-20），印刷卷期正确引文为 **2016;45(6):1866–1886**——稿件年份**正确**（且稿件缺期号，见格式节）。
  - ref40 Popper 书：Crossref 注册 2005（Routledge 电子书）；稿件 2002（Routledge Classics 版）可接受，建议按书格式书写。
- **卷号**：76 条可比，全部一致。
- **页码**：75 条可比；差异均为 Vancouver 允许的区间缩写（如 658-65 vs 658-665）或单页 e-locator（如 JAMA 1614-1621 与 Crossref 1614），无实质性错误。
- **第一作者**：人名型条目全部一致；13 处标记均为机构联盟（Crossref 将 consortium 列于首位）或重音（Munafò/Cavaillès）或复姓拆分（ref59 "Soler Artigas"），见 3.4。

### 3.3 ⚠️ 标题问题（本审计最大发现之一）
稿件中 **37 条标题被截断**、12 条措辞与官方不一致（合计约 49 条与 Crossref 官方标题不同）。典型：
- **ref1**：稿件 "…contribute to **understanding causation**?"；官方（Smith & Ebrahim 2003）为 "…**environmental determinants of disease**?"——实质内容不同。
- **ref4/5/7/8/14/17/19/20/21/24/27/28/39/44/45/46/48/55/58/59/60/61/62/64/66/69/71/73/74/75/76** 等：官方标题含副标题/被省略部分（如 ref44 官方为 "…corpus callosum **microstructure as potential mechanisms underlying ADHD–RLS comorbidity**"）。
- **ref35**：稿件 "…drug target genes **with Alzheimer's disease**"；Crossref 实际论文为 "…with **non-alcoholic fatty liver disease**"（EBioMedicine 2023;90:104543）——**主题不符**。
- **ref37**：稿件 "…and obesity indicators **with Alzheimer's disease**"；实际为 "…with **adverse cardiovascular events in patients with hypertension**"（Cardiovasc Diabetol 2025;24:11）——**主题不符**。
- **ref52**：稿件 "…identifies **putative causal pathways**"；实际 "…**putatively causal genes for multiple cancer types**"。
- **ref31**：Crossref 显示单作者 "Li W."，标题 "UK Biobank pharma proteomics resource"，页码 1781–1781——**该 DOI 记录存疑，建议人工核对论文全文**（稿件写作 "Li X, et al."，均可能与真实论文不符）。

### 3.4 ⚠️ 需人工核实的条目清单
| 新编号(旧编号) | 问题 | 建议 |
|---|---|---|
| 35(35) | 实际为 NAFLD 论文，非 AD | 若确为引用错误：替换为真正的 AD-脂质 MR 文献，或删除；若本意引用该文则改正文表述 |
| 37(37) | 实际为高血压心血管事件，非 AD | 同上 |
| 31(31) | 单作者记录存疑（Li W vs 稿件 Li X） | 到期刊页/PubMed 核对真实作者与标题 |
| 36(36) | 首作者 Zhang X vs 稿件 Zhang Y；标题 "protection" vs 稿件 "mediation" | 核对论文原文 |
| 38(38) | 首作者 Sun Y vs 稿件 Sun L；标题缺副标题 | 已按 Crossref 修正标题；作者以原文为准 |
| 47(47) | 首作者 Li T vs 稿件 Li X | 以原文为准 |
| 52(52) | 首作者 Li Y vs 稿件 Li X；标题不符 | 以原文为准 |
| 2(2) | Crossref 仅 2 位作者（Grover S, Sharma M），稿件原写 "et al." | 建议与 PubMed 核对完整作者 |
| 59(61) | 复姓 "Soler Artigas M" 被 Crossref 拆为 "Artigas MS" | 已人工改回 "Soler Artigas M" |
| 1(1) | 作者 "Smith GD" → 官方 "Davey Smith GD"；标题错误 | 已按 Crossref 修正 |

> 注：稿件中多处 "Li X, et al."（ref31/35/44/47/52）实际首作者各不相同（Li W/Z/F-J/T/Y），疑似早期草稿占位。**强烈建议以本轮 Crossref 生成的修正表为准并人工抽查全部 79 条作者名单。**

---

## 四、排序检查 ❌（需重编号 29 条）

BMC/Vancouver 要求**参考文献按正文首次引用顺序编号**。审计计算每号首引位置后发现：

- refs 1–50 首引顺序正确 ✅
- **refs 78–79（Voight 2012、Barter 2007）在 Discussion「Translational implications」节首次被引（offset 38973），早于 refs 51–77 的首次出现（offset 41139 起，Discussion「Beyond MR」及 Methods）** ❌
- 结果：**refs 51–79 共 29 条违反首引顺序**。

### 4.1 重编号映射（旧 → 新）
| 旧号 | 新号 | 旧号 | 新号 |
|---|---|---|---|
| 51–77 | 53–79（各 +2） | 78 | 51 |
| — | — | 79 | 52 |

### 4.2 文内引用改写映射（58 处标记中受影响 10 处）
| 原标记 | 新标记 | 原标记 | 新标记 |
|---|---|---|---|
| [51-59] | [53-61] | [67] | [69] |
| [60-63] | [62-65] | [68] | [70] |
| [64-66] | [66-68] | [69-70] | [71-72] |
| [30-31,33,64-66] | [30-31,33,66-68] | [71-76] | [73-78] |
| [30-32,71-76] | [30-32,73-78] | [77] | [79] |
| [13-17,32,39,43,60-63] | [13-17,32,39,43,62-65] | [78-79] | [51-52] |
| — | — | [78] | [51] |

其余标记（[1]-[50] 及各组合）不变。

---

## 五、格式合规 ❌（当前为 Nature 风格，需转 BMC/Vancouver）

对照官方 GM 范文（Leyden 2025, Genome Med 17:54）与 BMC 编辑政策，BMC 格式要点：

| 项目 | BMC 要求（范文实证） | 当前稿件 | 需改 |
|---|---|---|---|
| 文内引用 | 方括号编号 `[1]`，按首引顺序 | ✅ 已符合 | — |
| 期刊名 | **无斜体**，NLM 缩写，末尾句点（"Int J Epidemiol."） | ❌ 斜体 `*Int J Epidemiol*` | 改 |
| 卷号 | **无加粗**，紧跟分号（"2003;32(1):1–22."） | ❌ 加粗 `**32**` | 改 |
| 期号 | **必须带期号**（"32(1)"） | ❌ 全部缺期号 | 补 |
| 年份位置 | 期刊缩写之后（"2003;32…"） | ❌ 置于文末括号 "(2003)" | 移动 |
| 页码区间 | 连字符/半字线（"1–22"） | ⚠️ 短横为主 | 统一 |
| DOI | 条目末尾（可省略 "doi:" 前缀） | ❌ "doi: 10.xxx" 前缀 | 改 |
| 作者 | 姓+名缩写无句点；≤6 全列，7+ 加 "et al." | ⚠️ 部分 "et al." 过早在第 1 位作者后 | 改 |

**修正版已生成**：`GM_reference/references_BMC_formatted_renumbered_2026-08-09.md`（79 条，新编号，BMC 格式，标题/期号/DOI 已按 Crossref 修正）。

---

## 六、其他发现

1. **ref43 引用位置错误**：正文 "BMI–AD is a genuinely *contested* relationship **[43]**" 中，ref43 实为 Lee 2018 教育 GWAS，与 BMI-AD 争议无关。该句宜删除引用或改引合适的 BMI–AD MR 文献。
2. **docx 曾存在格式缺陷**：初版转换器误将参考文献转成 Word 自动编号列表（编号不在文本中）。已修复并重新导出 docx（编号显式写入文本，悬挂缩进）——**当前交付的 docx 已是修复版**。
3. ref40（Popper 书）与 ref42（Allara 2019）等书籍/特殊条目已单独处理。

---

## 七、建议的下一步（按优先级）

1. **人工核对 3.4 表中 9 条**（尤其 ref35/37/31），确认替换/删除后锁定最终文献集；
2. 将修正版 BMC 参考文献表 + 重编号映射应用回 `manuscript_draft_with_23refs.md` 与 docx（含 10 处文内标记改写）；
3. 删除/修正 ref43 处的 BMI-AD 引用；
4. 重新生成 docx 并复跑本审计脚本，确认 0 违规。

> 工具链说明：所有比对数据存于 `C:/Temp/iad_g1/`（crossref_results.json / refs_dump.json / renumber_map.json / bmc_references_clean.txt），可复现。

---

## 八、修复执行记录（2026-08-09 同日，用户确认后已应用）

**执行内容**（脚本 `code/ref_audit_apply_fixes.py`，原稿已备份为 `manuscript_draft_with_23refs_BEFORE_refaudit.md`）：

1. **舍弃存疑条目 3 条**：refs 31（UKB-PPP 记录存疑）、35（NAFLD 非 AD）、37（高血压心血管事件非 AD）——从文献表与全部文内引用标记中一并移除。
2. **修正 ref43 误引**：删除 "BMI–AD is a genuinely *contested* relationship [43]" 中的 `[43]`（ref43 Lee 2018 因 Methods 数据源另有引用而保留）。
3. **重算首引顺序并整体重编号**：删除与位移导致编号空间变化，已按新首引顺序重新编号 1–76（例如原 78/79 → 47/48；原 51–59 → 49–57；原 43 → 58；原 60–63 → 59–62；原 64–66 → 63–65；原 67→66、68→67、69–70→68–69、71–76→70–75、77→76）。全部文内标记已按新映射改写（含 [34-38]→[33-35]、[30-31,33,64-66]→[30,32,63-65]、[30-32,71-76]→[30-31,70-75] 等）。
4. **应用修正版 BMC 文献表**：76 条全部采用 Crossref 官方标题/作者/期号/DOI、NLM 期刊缩写、无斜体加粗、页码区间连字符、6 作者后 et al.、Soler Artigas 复姓人工修正。
5. **重新生成 docx**：`manuscript_GenomeMedicine_submission.docx`（76 条参考文献，显式编号，其余格式不变）。

**复跑审计结果（0 违规）**：
- 文献表 76 条 = 文内引用 76 个编号：**0 悬空、0 未引** ✓
- 首引顺序严格为 1→2→…→76：**通过** ✓
- 剩余 76 条 DOI 均为此前已通过 Crossref 解析（79/79 中剔除 3 条）✓

**最终交付物**：
- `manuscript_draft_with_23refs.md`（已应用全部修复）
- `manuscript_GenomeMedicine_submission.docx`（重新导出）
- `GM_reference/references_BMC_formatted_renumbered_2026-08-09.md`（最终 76 条版）
- 备份：`manuscript_draft_with_23refs_BEFORE_refaudit.md`
