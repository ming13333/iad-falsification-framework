# 本地运行指南:失眠 ↔ AD 三法整合因果分析

> 本指南对应专家团 **失眠-AD 共病因果研究专家团** 的 SOP(Phase 1→5)。
> 沙箱(WorkBuddy)**不能跑实际 MR / 多状态分析**(GWAS API 白名单 + 无 UKB 权限 + 无 R 运行时),以下全部步骤需在你**本地可联网 R 环境**执行。
> 代码骨架位于 `课题设计阶段/code/`(`00_config.R` / `00b_verify_gwas.R` / `01_*` / `02_*` / `03_*` / `README.md`)。

---

## 0. 环境准备(一次性)

**R ≥ 4.3**,在 R 控制台执行:

```r
install.packages(c("dplyr","data.table","survival"))
# 从 CRAN 安装 MR 生态
install.packages(c("TwoSampleMR","ieugwasr"))
# coloc 在 CRAN
install.packages("coloc")
# 多状态模型
install.packages(c("msm","mstate"))
# ---- P0 必需(GitHub 包):样本重叠校正(MRlap)+ 多效性区分(CAUSE) ----
# ⚠️ 这三个包不是"可选":run_local_pipeline.sh 第55行依赖检查强制要求 MRPRESSO/MRlap/CAUSE 三包齐全,
#    否则流水线直接 halt;且 OSF 预注册 §6/§7 将 MRlap/CAUSE 列为 P0 必需敏感性。
install.packages("remotes")                        # install_github 前置依赖
remotes::install_github("rondolab/MR-PRESSO")
remotes::install_github("explodecomputer/MRlap")
remotes::install_github("jean997/cause")

# P0 前置(跑流水线前必设):上述三包 + 两个 1000G EUR LD 面板环境变量
#   export MRlap_LDREF=/path/to/MRlap/LD_reference
#   export CAUSE_LDREF=/path/to/CAUSE/ld_ref
# 二者指向本地 1000G EUR LD 面板;脚本(run_local_pipeline.sh)已有对应检查与 SKIP_OVERLAP=1 跳过开关,此处不展开。
```

**联网校验**(必须能访问 IEU/OpenGWAS):
```r
library(ieugwasr)
# 应返回数据框而非报错;若超时说明网络被墙,需代理/学术网络
available_outcomes()
```

**数据权限清单**:
| 数据 | 用途 | 获取 |
|------|------|------|
| 失眠 GWAS(BenElsworth 2018) | G1 暴露 / G2 step1 | `ukb-b-3957`(已锁定, n=462,341)或本地 |
| AD GWAS(Bellenguez 2022) | G1 结局 / G2 step2 | 00b 搜索解析(IEU ID) |
| UKB-PPP 血浆蛋白 pQTL | G2 中介 | UKB-PPP 申请/Pharmaco Proteomics Project |
| UKB 个体级 | G4 多状态 | UKB 申请(字段 2245/2255/G47.0/F00/G30/死亡) |

---

## 1. 目录与配置

把 `课题设计阶段/code/` 拷到本地工作目录,编辑 `00_config.R`:
- `DIR_DATA`、`DIR_OUT`、`DIR_LOG` 设为本地绝对路径。
- `GWAS_ID$insomnia` 已锁定 `ukb-b-3957`(BenElsworth 2018);`GWAS_ID$ad` 锁定 `ieu-b-2`(Kunkle/IGAP);00b 已解析写入 `gwas_ids_resolved.json`。
- 蛋白 GWAS 列表 `PROTEIN_GWAS` 指向本地 UKB-PPP 汇总统计索引 csv。

---

## 2. Step 00b — 运行前强制核验(必须先做!)

**对应 SOP Phase 1(数据核验清单)**

```bash
Rscript code/00b_verify_gwas.R
```

**产出**:`data/gwas_ids_resolved.json`(确认的 ID + 样本量)。

**Go/No-go 检查项**(任一不过则先解决再往下):
- [ ] 失眠 ID 可 `gwasinfo` 取到样本量(ukb-b-3957, 约 462K)
- [ ] AD ID 经 `search` 解析到正确 IEU ID,Bellenguez 2022 111k cases
- [ ] BenElsworth↔Bellenguez 的 UKB 样本重叠:报告重叠比例,决定是否需要 LD 纠错/独立源
- [ ] UKB-PPP panel 覆盖 GFAP / NfL(NEFL)/ 炎症因子(IL-6/CRP 通路)——此条是 STORM 升 A 工程假设 #1,**必须实测确认**
- [ ] 工具变量数:暴露 SNP 经 clump 后 ≥ 合理性阈值(F>10)

> 若 00b 因 API 变动报错,手动在 R 里 `gwasinfo("ukb-b-3957")` 替代,把结果填回 `00_config.R` 与 json。

---

## 3. Step 01 — G1 双向 MR + 共定位

**对应 SOP Phase 2**(`mr-genetics-expert` 主导)

```bash
Rscript code/01_bidirectional_mr_coloc.R
```

**依赖**:`00b` 产出的 `gwas_ids_resolved.json`(脚本自动读取)。

**产出**:
- 正向(失眠→AD)、反向(AD→失眠)MR 效应表(β/SE/OR/p)
- 敏感性:MR-Egger 截距、MR-PRESSO 离群、留一法、异质性 Q
- Steiger 方向过滤结果
- 共定位 `coloc` PP.H4 表

**判定(写入下一步)**:
- 若正向显著、反向不显著 + Steiger 通过 ⇒ 方向=失眠→AD(进入 G2 正向中介)
- 若反向也显著 ⇒ 需 G4 时序 + CAUSE/MRlap 进一步区分

---

## 4. Step 02 — G2 血浆蛋白两步中介

**对应 SOP Phase 3**(`mr-genetics-expert`,依赖 G1 方向)

**准备**:放置 UKB-PPP 蛋白 pQTL 汇总统计,更新 `00_config.R` 的 `PROTEIN_GWAS`。

```bash
Rscript code/02_protein_mediation.R
```

**产出**:
- 蛋白级中介表:蛋白名、b1(失眠→蛋白)、b2(蛋白→AD)、中介效应=b1×b2、SE(delta 法)、P、FDR
- top 候选蛋白 coloc 复核(PP.H4)
- 反向两步(AD→蛋白→失眠)证伪结果

**注意**:脚本已修正原骨架的 FDR bug——从 `mr()` 捕获 b/se/p 后做乘性中介 + delta 法 SE + 正态近似 P + 真实 FDR,**不再是占位 P=1**。

**Go/No-go**:
- [ ] 至少 1 个蛋白经 FDR<0.05 且 coloc 复核
- [ ] 反向证伪排除"蛋白是 AD 上游"替代解释

---

## 5. Step 03 — G4 多状态发病顺序(需 UKB 个体级权限)

**对应 SOP Phase 4**(`writing-audit-expert`,可与 P2/P3 并行)

**准备**:UKB 个体级长表,字段见 `失眠-AD_三法整合设计.md` §三 G4。

```bash
Rscript code/03_multistate_onset.R
```

**产出**:
- 状态转移强度 q 表(S0→S1、S0→S2、S1→S3、S2→S3、各→死亡)
- 累积发病曲线:1→3(失眠先发)vs 2→3(AD 先发)
- 分层生存 HR(按进入路径)

**敏感性**(脚本内或手动):
- 仅住院 ICD 失眠定义 / 全因痴呆 vs AD / 调整 APOE ε4·抑郁·安眠药 / 竞争风险

---

## 6. OSF 预注册(跑数前锁定)

**对应 SOP Phase 1** 的预注册子任务。用 `OSF预注册计划.md` 直接复制到 OSF 项目锁定:
- 暴露=失眠、结局=AD、协变量固定清单
- 方法顺序 G1→G2→G4、敏感性清单、阈值(MR α=0.05 / G2 FDR<0.05 / G4 双路径 α=0.05)

> 建议:在跑 01/02/03 **之前**完成预注册,防 p-hacking 质疑。

---

## 7. G3 跨祖先复制(并行 / 后续增量)

**对应 SOP 最终报告的"下一步"**。按 `G3跨祖先复制方案.md`:
- BBJ(东亚)、UKB 东亚子集、CHARLS 复制 G1/G2
- 与欧裔主分析对比方向/介导蛋白一致性

---

## 8. 三角验证 + 写作 + 审计

**对应 SOP Phase 5**(`writing-audit-expert`)。把 01/02/03 的真实产出汇总:
- 三角验证:遗传(G1方向)+ 分子(G2机制)+ 临床时序(G4)是否收敛
- 按 `论文图表骨架_Fig1-5_Table1.md` 写 Fig1–5 + Table1
- STORM 五视角审计:找升 A 阻塞点(三处工程假设是否全坐实、不一致结果是否诚实呈现)

---

## 9. 总体顺序与依赖图

```
00b 核验 ──► 01 G1 方向 ──► 02 G2 机制(依赖G1方向)
                         └──► 03 G4 时序(可并行,需UKB权限)
                                    │
                    OSF 预注册(应在 01 前锁定)
                                    │
                    全部产出 ──► 三角验证 + 写作 + 审计(Phase 5)
                                    │
                               G3 跨祖先复制(增量)
```

## 10. 常见问题

- **`available_outcomes()` 超时**:网络受限,换学术网络/代理;或手动 `gwasinfo("ukb-b-3957")`。
- **样本重叠警告**:BenElsworth 2018 (ukb-b-3957) 与 Bellenguez 共享 UKB 个体,用 `ldlcr`/独立源或报告重叠比例。
- **蛋白 panel 未覆盖 GFAP/NfL**:先验假设落空,改用 UKB-PPP 实际包含的神经/炎症蛋白,更新 `PROTEIN_GWAS`。
- **G4 事件数少**:主分析用"全因痴呆"扩样本,AD 作敏感性(设计文档已规划)。

---

## 11. 与专家团的衔接

本地跑出真实数字后,可在 WorkBuddy 调用 **失眠-AD 共病因果研究专家团**:
- 调 `mr-genetics-expert` 复核 G1/G2 方法学或解释结果
- 调 `writing-audit-expert` 做 G4、OSF 预注册、手稿与 STORM 审计
- 调主理人(罗经纬)走完整 SOP 编排与三角验证汇总
