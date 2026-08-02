# 对话交接单（SESSION HANDOFF）

> **用途**：更换对话/新开会话后，把这份贴给 AI，即可无缝续接。
> **最后更新**：2026-07-18 19:05 · **课题**：失眠 → 阿尔茨海默病（AD）共病因果机制
> **项目根目录**：`C:\D\workbuddy\科研\共病分析\课题设计阶段\`

---

## 0. 一句话现状
课题的**设计、代码框架、专家团、本地运行指南全部就绪**；**唯一未完成的是"本地联网跑真实 MR 数字"**——这一步沙箱做不了，必须在你本地 R 环境执行。

---

## 1. 课题方法学骨架（已固化，勿改）
**G1 双向 MR + 共定位（定方向）→ G2 血浆蛋白两步中介（落机制）→ G4 多状态时序（给时序）→ 三角验证收敛**
外加：**OSF 预注册** + **STORM 式批判性审计**。

- 暴露：失眠（BenElsworth 2018，IEU ID `ukb-b-3957`，n=462,341，EUR，42 clumped IVs；Jansen 2019 不在仓库、ieu-a-1096=儿童肥胖均已废弃）
- 结局（主对，无样本重叠）：AD（Kunkle/IGAP 2019，IEU ID `ieu-b-2`，ncase=21,982，与 ukb-b-3957 无 UKB 重叠 → 因果估计最干净）
- 结局（复制，含 UKB 重叠→须 MRlap/CAUSE 校正）：AD（Bellenguez 2022，IEU ID `ebi-a-GCST90027158`，ncase=39,106；ID 已由 `00b` 联网核验并写入 gwas_ids_resolved.json）
- 中介：UKB-PPP 血浆蛋白（GFAP / NfL(NEFL) / 炎症因子——**已离线证实在 Olink panel 内**）

---

## 2. 关键硬约束（每次续接必须记住）
1. **本 WorkBuddy 沙箱不能跑实际 MR**：OpenGWAS 的 `gwasinfo`/`search` 被网关白名单拦截（返回网关 404，非真不存在）；沙箱无 R、无 UKB 个体级权限。
2. 因此**任何"失眠→AD 因果显著"的数字都不能在沙箱产出**，只能你本地联网 R 环境跑。
3. 严禁用框架占位数字冒充真实结果——诚实边界优先。
4. 本会话原系统角色是"单细胞研究团（sc-repro-team）"，**与本 MR 课题不匹配，已解耦，勿硬套**。

---

## 3. 已完成的交付物（沙箱阶段）

### 代码（`code/`）
| 文件 | 状态 |
|------|------|
| `00_config.R` | ✅ 填实候选 GWAS ID + 读取 `00b` 写出的 `gwas_ids_resolved.json` 钩子 + 样本重叠提示 |
| `00b_verify_gwas.R` | ✅ 新增·运行前强制核验（ID 样本量/AD 正确 ID/样本重叠/蛋白 panel 覆盖，写出确认 ID） |
| `01_bidirectional_mr_coloc.R` | ⚠️ 框架完成，待本地跑数 |
| `02_protein_mediation.R` | ✅ 已修 FDR bug（原用占位 P=1；改为 mr() 捕获 b/se/p + 乘积法 + delta 法 SE + 真实 FDR），待本地跑数 |
| `03_multistate_onset.R` | ⚠️ 框架完成，需 UKB 个体级长表，待本地跑数 |

### 文档（`课题设计阶段/`）
- `本地运行指南_失眠-AD三法整合.md` ← **你下一步照这个跑**
- `OSF预注册计划.md`（暴露/结局/协变量/方法顺序/敏感性/阈值已锁）
- `G3跨祖先复制方案.md`（BBJ / 东亚 UKB / CHARLS）
- `论文图表骨架_Fig1-5_Table1.md`
- `执行边界与下一步_沙箱说明.md`
- `项目交接手册.md`（已更新里程碑 #8、进度快照、文件清单）

### 专家团（已注册 + 打包，专家中心可见）
- 位置：`C:\Users\lm962\.workbuddy\plugins\marketplaces\my-experts\plugins\insomnia-ad-causal-team\`
- 「失眠-AD 共病因果研究专家团」(team 型，类别 04-DataAI)，含 4 张 cyan-teal 头像，已打包 `insomnia-ad-causal-team.zip`
- 角色：**罗经纬**（主理人·统筹编排/三角验证裁决）·**孟因之**（MR 因果推断 G1/G2）·**范审明**（G4 时序+OSF+写作+STORM 审计）

---

## 4. 下一步执行顺序（本地，从这里接着做）
```
① 本地装依赖：TwoSampleMR / ieugwasr / coloc / msm / mstate
② Rscript code/00b_verify_gwas.R        → 核验 ID/样本重叠/panel 覆盖，生成 gwas_ids_resolved.json
③ 备 data/ukbppp_protein_gwas_index.csv （蛋白 GWAS 索引）
④ Rscript code/01_bidirectional_mr_coloc.R   → G1 方向 + 共定位
⑤ Rscript code/02_protein_mediation.R        → G2 蛋白两步中介
⑥ Rscript code/03_multistate_onset.R         → G4 多状态时序（需 UKB 个体级数据）
⑦ 复制 OSF预注册计划.md 到 OSF 锁定
⑧ 并行启动 G3 跨祖先复制
⑨ 真数字出来后 → 调专家团做复核/写作/STORM 审计
```

---

## 5. 待办中未做的三处"升 A 工程假设"核验
1. ✅ **蛋白 panel 覆盖**（GFAP/NfL/炎症）——已离线证实成立。
2. ⏳ **instrument 数 / 样本重叠**——必须 `00b` 联网实测。
3. ⏳ **真实 P 值 FDR**——必须本地跑 `02` 产出，不能占位。

---

## 6. 新对话续接提示词（复制这段给新 AI）
> 接手"失眠→AD 共病因果课题"。请先读
> `C:\D\workbuddy\科研\共病分析\课题设计阶段\对话交接单_SESSION-HANDOFF.md`
> 和 `本地运行指南_失眠-AD三法整合.md`。
> 已知硬约束：沙箱不能跑实际 MR（GWAS API 白名单+无 UKB 权限+无 R），真实数字须本地产出，勿用占位冒充。
> 已建「失眠-AD 共病因果研究专家团」。现在我想做：______（在此填你的目标）。

---

## 7. 沙箱跑数前终审成果（2026-07-18 晚 · 增量）

> 本节能见：专家团（team `insomnia-ad-preflight`）完成「跑数前终审与代码补全」。沙箱硬约束不变（无 R / 无 OpenGWAS 网络 / 无 UKB 权限），真实 MR 数字仍须你本地产出。

### 7.1 交付物（全部文件级 Read 验证通过）
- **01_bidirectional_mr_coloc.R**：run_coloc 实装（区域 SNP 对齐 + coloc.abf）+ PENDING_VERIFY 守卫 + saveRDS 含 coloc + MR-PRESSO / F 统计 / MRlap 注释 + **P0 收尾：run_mrlap / run_cause 实装（样本重叠校正 + 多效性区分，OSF §6/§7 已锁「必须」）**。
- **02_protein_mediation.R**：文件守卫 + 来源感知 helper（本地文件 / IEU）+ coloc 复核（PP.H4）+ 反向证伪（direction_cmp）+ delta 法局限注释。
- **03_multistate_onset.R**：657 行可执行（数据守卫 / 清洗 / 宽转长 / msm 拟合 / 路径对比 / 分层生存 / 3 敏感性）。
- **OSF预注册计划.md**：打磨至可粘贴（§0 元数据 / §2 操作化标准 / §3 回退策略 / §6 MRlap+CAUSE 必需 / §9 阴性处理 / §10 局限表格）。
- **STORM跑数前审计.md**：新建，五视角 + P0/P1 清单 + 信度自评。

### 7.2 接手必读
- **孟因之（mr-genetics-expert）两次「汇报完成但文件未改」**：#1 仅改守卫、#5 经两次文件级验证仍注释/缺失 → 已按声明换 mr_fix_p0 接管并真实落盘（P0）。**教训：任何团员「完成」声明必须以文件级 Read 验证为准，不可听汇报。**
- **P0 已收尾但待本地验证（2026-07-20 已按真实 API 修正）**：MRlap 仓库实为 `n-mounier/MRlap`（非 explodecomputer），主函数 `MRlap::MRlap(exposure, outcome, ld, hm3, ...)`，需 LDSC 权重 `eur_w_ld_chr` 目录 + `w_hm3.noMHC.snplist` 文件（来源 utexas.box.com）；返回 `fit$MRcorrection$corrected_effect/observed_effect/p_difference/m_IVs`。CAUSE 经 `install.packages('cause', repos='https://mrcieu.r-universe.dev')` 安装更稳，LD 修剪用 `ieugwasr::ld_clump(pop="EUR")`（无需本地面板）。跑数前必须跑 00b 确认重叠比例；若 >5% 必须启用 MRlap（设 `MRlap_LDREF` / `MRlap_HM3` 环境变量指向 LDSC 权重）。
- **真实数字仍须本地**：沙箱不能跑，见 §0/§2/§4。

### 7.3 下一步（本地，不变）
见 §4 ④~⑨。代码层阻塞已清零，进入「本地跑数」阶段。
- **新增 `code/run_local_pipeline.sh`**：本地一键串跑 `00b→01→02→03`，含 **P0 LDSC 权重强制检查（MRlap_LDREF / MRlap_HM3）** 与 R 依赖检查，任一步失败即停，避免半成品污染结果。运行：`cd 课题设计阶段 && bash code/run_local_pipeline.sh`（需 Git Bash / WSL）。
