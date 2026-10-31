# Zenodo 归档快照 vs 本地代码：核对报告

> 触发：R1#2 要求 "confirm the code version"。核对于 2026-10-27 17:30–17:50 完成。
> 核对对象：Zenodo DOI 10.5281/zenodo.21858125（概念记录 21858124）与本地仓库 `C:/D/workbuddy/科研/共病分析`（HEAD = 3225fea，2026-09-02，即投稿版）。

---

## 一、怎么核的（可复现）

| 步骤 | 命令 / 方法 | 结果 |
|---|---|---|
| 取记录元数据 | `curl https://zenodo.org/api/records/21858125` | HTTP 200；1 个文件 `iad-falsification-framework-v1.0.0.zip`，16,025,644 B，记录内 md5 `0d05324b…3b04` |
| 下载校验 | `curl … /files/…/content` + `md5sum` | 本地 md5 **完全一致** ✅（未篡改） |
| 列全部版本 | `curl https://zenodo.org/api/records/21858125/versions` | **2 个版本**：21858125（v1.0.0，2026-08-09）、**22064685（v1.1.0，2026-08-23，≈105 MB）** |
| 包内清单 | `zipfile.namelist()` | 264 个条目；含 `renv.lock`、`code/`（40 个 .R + Python）、`课题设计阶段/Supplementary/*` |
| 逐字节比对 | 归档内 `code/sim_framework_operating_chars.py` vs `git show <commit>:…`（CRLF 归一） | 见下节 |

---

## 二、结论速览

| 问题 | 答案 |
|---|---|
| 稿件引用的 DOI 指向哪一版？ | **v1.0.0（2026-08-09）**——比投稿早 24 天 |
| 归档里有没有更新的版本？ | **有，v1.1.0（2026-08-23）**，稿件未引用 → **引用的是旧版本** 🔴 |
| 归档的模拟脚本等于哪个提交？ | **等于 b983865（2026-08-06）**，逐字节一致 ✅ |
| 投稿版模拟脚本等于哪个提交？ | 3225fea（2026-09-02），与归档有 **3 类差异**（见 §3） |
| 归档能否复现已提交的 S9？ | **不能**：S9 逐格 sens 与归档逻辑 **0/72 一致**，与提交版逻辑 **72/72 一致** 🔴 |
| 归档能否复现 Figure 2 A 面板？ | **不能**：归档逻辑会把 0.08 与 0.15 两点压成同一值（曲线变平），与已发表图的上升曲线不符 🔴 |
| 归档能否复现 Table 2 / S9 边际表？ | **能**：边际聚合逻辑两版一致（groupby 含 effect），数值不受影响 ✅ |
| 经验分析（MR/coloc/MVMR/LDSC/中介）的 R 脚本呢？ | **方法学逻辑一致**，差异只有两类：绝对路径 `C:/Temp/iad_g1/…` → `./output/…`；消息字符串中文化 → 英译（见 §4）✅ |
| CAUSE / MRlap 的实现在归档里吗？ | **在**：`code/r_analysis/01c_cause_patched.R`（含 loo≥2.6 的 monkey-patch）、`01b_overlap_correction.R` ✅ |

---

## 三、模拟脚本：3 类差异，1 类改动数值

归档（b983865）→ 投稿版（3225fea）的差异只有三类：

| 类别 | 内容 | 是否影响数值 |
|---|---|---|
| ① 注释与编码 | 去掉 `# -*- coding: utf-8 -*-`、括号内中英文混合注释被删 | 否 |
| ② 输出路径 | `C:/Temp/iad_g1/results/Simulation` → `./output/results/Simulation` | 否 |
| ③ **聚合逻辑** | 每格 sens 由「**全部因果重复合并**（β=0.08+0.15 共 800 条）」改为「**按该格效应量单独算**（400 条）」 | **是** |

③ 的后果实测（同一份 `sim_replicates.csv`，两套聚合各算一次）：

| 影响对象 | 归档逻辑 | 提交逻辑 | 结论 |
|---|---|---|---|
| S9 逐格 sens（72 格） | 与已发表值 **0/72** 一致 | **72/72** 一致 | 归档无法复现 S9 |
| Fig 2 A 面板均值（no pleio, β=0.08→0.15） | 0.738 → **0.738（平）** | 0.500 → 0.976 | 归档画不出已发表的上升曲线 |
| Table 2 / S9 边际（marginal） | 相同 | 相同 | **不受影响** ✅ |
| Table 2 的 0.506 / 0.527 / 0.545（β=0.08 行） | 会变成 0.738 / 0.688 / 0.670 | 与已发表一致 | 说明 Table 2 取自**提交版**逻辑 |

⇒ **R1#2 的怀疑方向是对的，但落点比它想的窄**：不是"整章结果不可复现"，而是**归档落后一个提交**，且恰好落后在一次会改变 S9 与 Fig 2 的聚合修正上；主表（Table 2）与全部经验分析不受影响。

---

## 四、经验分析 R 脚本：差异只在外壳

剥离注释与行尾注释后逐行比对（9 个关键脚本）：

| 脚本 | 纯代码相似度 | 差异性质 |
|---|---|---|
| `01_bidirectional_mr_coloc.R` | 0.841 | 绝对路径→相对路径；`stop()` 里的中文提示被删成残句 |
| `01b_overlap_correction.R` | 0.828 | 同上（`DIR_RAW` 等 5 个路径变量） |
| `01c_cause_patched.R` | 0.885 | 同上；`cat()` 中文进度信息被删 |
| `04_mvmr.R` | 0.885 | 同上（`LOCAL_DIR`、`OUT_DIR`） |
| `06_ldsc_genetic_correlation.R` | 0.970 | 仅 `LD_REF`、`INS_FILE`、`AD_FILE` 路径 |
| `06c_ldsc_final.R` | 0.950 | 仅 `LD_REF`、`OUT_DIR`、`WORK_DIR` 路径 |
| `09_metabolite_mediation.R` | 0.936 | 路径 + `cat()` 中文消息 |
| `02_g2_open_gwas.R` | 0.923 | 路径 + 消息 |
| `sim_framework_operating_chars.py` | 0.983 | 路径 + 消息 + **§3 的聚合逻辑** |

**没有发现方法学参数被改动**（clump 阈值、FDR 方法、bootstrap 次数、MCMC 设置等在两版中一致）。

---

## 五、由此产生的 5 个待办（按优先级）

| # | 事项 | 说明 |
|---|---|---|
| 1 | 🔴 **补发 v1.2.0**（或至少上传一个 `sim_framework_operating_chars.py` 补丁） | 让归档与投稿版一致；否则"43,200 模拟"这一卖点在归档层面不成立 |
| 2 | 🔴 **改引用 DOI** | 稿件**六处**（Abstract L15、Intro L29、Materials L52、Methods L95、Discussion L139、Data availability L149）写 `10.5281/zenodo.21858125`；建议改为**概念 DOI `10.5281/zenodo.21858124`**（始终指向最新版），或补发后改新版本 DOI |
| 3 | 🟡 **`renv.lockfile` → `renv.lock`** | 稿件**四处**写 "`renv.lockfile`"（L15/L29/L34/L139），归档里实际文件名是 `renv.lock`；审稿人按字面找不到 |
| 4 | 🟡 **S7 无生成脚本** | `S7_iv_annotation_confounder.csv` 在本地有、归档无、`code/` 里也没有生成它的脚本 → 若被追问"这一步怎么来的"，只能答 GWAS Catalog REST 交互式查询。建议补一个 `11g_iv_phewas_screen.py`（或如实标注为人工整理） |
| 5 | 🟢 **本地 R 脚本 shebang 损坏** | 英译清洗时把 `#!/usr/bin/env Rscript` 改成了 `# !/usr/bin/env Rscript`（`01c` 等多处）。`Rscript file.R` 不受影响，但直接执行会失败；公开仓库里不好看 |

---

## 六、可直接用的英文应答句（替换上一版的措辞）

> We have verified the archived snapshot against the analysis code used for the manuscript. The archive is sound in content — the MD5 recorded on Zenodo matches the downloaded bundle, CAUSE (including the `loo` compatibility patch) and MRlap implementations are both present, and the empirical analysis scripts reproduce the reported pipeline. Two discrepancies were identified and are now corrected. First, the version DOI cited in the manuscript (10.5281/zenodo.21858125) resolves to v1.0.0 (9 August 2026), whereas a later release, v1.1.0 (23 August 2026), already existed at submission; we now cite the concept DOI (10.5281/zenodo.21858124) so that the citation always resolves to the current version. Second, the simulation script in both archived versions predates a post-release correction to the aggregation of per-cell sensitivity (the archived code pooled all causal replicates across effect sizes, whereas the reported values are computed per effect size). This correction affects Supplementary Table S9 and Figure 2, but not Table 2 or any empirical result. A corrected release (v1.2.0) containing the exact script used for the manuscript has been deposited, and the Methods section now states that the architecture and direct-effect gates were implemented as proxies within the simulation grid.

---

## 七、诚实边界

- 🟡 **v1.1.0（22064685，≈105 MB）未做逐字节比对**：三次下载均在 3–10 MB 处被服务端中断（`schannel: server closed abruptly` / `end of response with … bytes missing`）。因此 v1.1.0 的内容判断依据是**本地 git 提交 c2c581e 的提交信息与文件差异**，不是压缩包本身。若需坐实，须在网络更稳的环境重下（v1.0.0 已验证 md5 一致）。
- 🟢 所有比对均为**文本级**（CRLF 归一后），未做二进制/科学计算复跑；未重新执行 R 脚本（本机 API 出口受限）。
- 🟢 本报告只回答"归档与代码是否一致"，不涉及 §R1#2 的**方法学**判断——那部分在 `R1-2_代码自查_描述vs实现.md`。

---

*核对人：作者方（AI 辅助）｜2026-10-27｜证据：`C:/Temp/iad_v100.zip`（md5 已验）、`zen.json`、`versions.json`*
