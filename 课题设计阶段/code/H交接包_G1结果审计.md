# H 部分交接包：G1 结果解读 + 方法学审计

> **使用说明**：G1 运行完成后，将本文件内容 + 实际产出的结果文件内容，粘贴到高阶模型会话中。高阶模型无需回看前序对话即可独立完成。

---

## 【任务】

对失眠↔阿尔茨海默病(AD)双向孟德尔随机化(MR)+共定位(coloc)+重叠校正的 G1 阶段结果，产出一份**方法学审计表 + 因果方向判定 + 局限性披露 + 下一步决策建议**。

## 【背景】

### 研究主线
三角验证因果链：遗传因果(G1 双向 MR+coloc) → 分子机制(G2 血浆蛋白中介) → 临床时序(G4 多状态发病顺序)。G1 是第一根支柱，目标是判定"失眠→AD"还是"AD→失眠"的遗传因果方向。

### 暴露与结局（三 GWAS 数据集）
| 角色 | GWAS ID | 来源 | 样本量 | 坐标 | 工具 SNP 数 |
|------|---------|------|--------|------|-------------|
| 失眠(暴露) | ukb-b-3957 | UK Biobank Neale | N≈905,011(估计) | GRCh37 | 2462(本地 harmonize) |
| AD 主对(结局) | ieu-b-2 | Kunkle 2019 | N=63,926 (case=21,982 / ctrl=41,944) | GRCh37 | 1132(反向) |
| AD 复制(结局) | ebi-a-GCST90027158 | Bellenguez 2022 | N≈487,511 (case=85,934 / ctrl=401,577) | GRCh38→37转移 | 待G1输出 |

### 方法清单
| 方法 | 用途 | 关键参数 |
|------|------|----------|
| 双向 MR | 方向判定 | IVW + Egger + 加权中位数 + 加权众数 |
| 异质性检验 | Cochran's Q | 检测工具间一致性 |
| Egger 截距 | 水平多效性 | 检测系统性偏倚 |
| 留一法 | 稳健性 | 逐 SNP 排除后效应 |
| MR-PRESSO | 离群检测 | 10,000 次 bootstrap |
| Steiger filtering | 因果方向 | 比较 R²_exposure vs R²_outcome |
| 区域 coloc (coloc.abf) | 共享因果变异 | 逐 lead SNP ±500kb 窗口, type="cc", PP.H4>0.8 为强证据 |
| MRlap | 样本重叠校正 | 估计 Directional Pleiotropy + biases |
| CAUSE | 样本重叠+未测量混杂 | 因果 vs 背景相关模型选择 |

## 【我已完成的铺垫】

### 数据预处理（已完成并验证）
- 三 GWAS 原始文件已下载并验证完整性（gzip 完整、md5 一致、记录数与公布值吻合）
- 去重：逐 rsID 保留最显著记录（ieu-b-2 去重后 10,444,926；ukb-b-3957 去重后 9,837,128；Bellenguez 去重后 21,070,466）
- 坐标统一：Bellenguez GRCh38→GRCh37（rsID 转移法，映射率 50.36%，未覆盖者用 GRCh38 全量补充）
- 样本量注入：ieu-b-2 N=63,926 (case=21,982)；ukb-b-3957 统一有效 N=905,011；Bellenguez 自带逐位点 n_cases/n_controls

### 代码本地化（已完成并验证）
- `01_bidirectional_mr_coloc.R` 已改为零联网读取本地 clean 文件
- 隔离测试验证：harmonize 双向成功（fwd=2462 SNP / rev=1132 SNP / 0 ambiguous）
- SNP 标识体系验证：ukb 99.98% 为 rsID，ieu 100% rsID，直接 ID 匹配 79%

## 【输入材料 — G1 运行完成后读取】

### 结果文件路径（全部在 ASCII 临时目录 `C:/Temp/iad_g1/`）
| 文件 | 路径 | 内容 |
|------|------|------|
| 主结果 RDS | `C:/Temp/iad_g1/results/G1_bidirectional.rds` | 全部结果对象(fwd/rev/steiger/coloc/mrlap/cause + 复制) |
| coloc 正向 | `C:/Temp/iad_g1/results/G1_coloc_forward.csv` | 失眠→AD 共定位 PP.H0-H4 |
| coloc 反向 | `C:/Temp/iad_g1/results/G1_coloc_reverse.csv` | AD→失眠 共定位 |
| coloc 复制正 | `C:/Temp/iad_g1/results/G1_coloc_forward_repl.csv` | Bellenguez 复制 |
| coloc 复制反 | `C:/Temp/iad_g1/results/G1_coloc_reverse_repl.csv` | Bellenguez 复制 |
| MRlap | `C:/Temp/iad_g1/results/G1_mrlap.csv` | 重叠校正估计 |
| 运行日志 | `C:/Temp/iad_g1/G1_run.log` | 全程日志（含跳过/失败原因） |
| 环境 | `C:/Temp/iad_g1/results/G1_sessionInfo.txt` | R/包版本快照 |

### 读取 RDS 的 R 命令
```r
res <- readRDS("C:/Temp/iad_g1/results/G1_bidirectional.rds")
# res$fwd = 正向(失眠→AD) MR 结果对象
# res$rev = 反向(AD→失眠) MR 结果对象
# res$steiger_fwd / res$steiger_rev = Steiger 方向检验
# res$coloc_fwd / res$coloc_rev = coloc 表
# res$mrlap_fwd / res$mrlap_rev = MRlap 估计
# res$cause_fwd / res$cause_rev = CAUSE 估计
# res$fwd_rep / res$rev_rep = Bellenguez 复制
# res$overlap_correction_run = 重叠校正是否实际运行(FALSE=跳过)
```

## 【具体要求】

### 必须做到的：
1. **因果方向判定**：基于 IVW 主分析 + Egger 截距 + Steiger 方向检验，明确判定"失眠→AD"和"AD→失眠"各方向是否成立。报告 β/se/p 及方向。
2. **共定位解读**：报告各方向 coloc 的 PP.H4 中位数和最大值，判定是否 PP.H4>0.8（强共享因果变异证据）。注意：区域 coloc（逐 lead ±500kb），非全局。
3. **重叠校正解读**：若 MRlap/CAUSE 实际运行（`overlap_correction_run=TRUE`），报告其估计；若跳过（FALSE），在 Limitations 中明确披露。
4. **敏感性分析**：异质性(Q p值)、水平多效性(Egger 截距 p值)、留一法(是否有驱动性 SNP)、MR-PRESSO(是否有离群) 逐项报告。
5. **三角验证判定**：MR 方向 + coloc 证据 + 重叠校正 → 三源是否收敛到同一因果结论。

### 验收标准：
- 产出一张 **STORM 式方法学审计表**（行=方法，列=结果/判定/风险/置信度）
- 产出一段 **因果方向结论**（明确哪方向成立、证据强度）
- 产出一份 **Limitations 清单**（须覆盖下方"已知局限"全部 6 项）
- 产出 **下一步决策**：G2(血浆蛋白中介)和 G4(多状态时序)是否应启动、需补什么

### 输出格式：
- 审计表：Markdown 表格
- 结论：结构化段落（方向判定 → 证据强度 → 局限 → 下一步）
- 中文输出，术语括注英文

### 请勿：
- 不要重新运行 G1 脚本（已跑完）
- 不要修改原始数据或脚本
- 不要引入新的 MR 方法（只解读已跑的）

## 【已知局限 — 审计时必须覆盖】

1. **ukb 有效 N=905,011 为估计值**：由常见变异(MAF 0.4-0.6)的 se²×2×af×(1-af) 反推中位数，非研究级元数据。影响 MRlap/CAUSE 的样本量输入。
2. **rsID 转移式 liftover**：Bellenguez GRCh38→GRCh37 用 rsID join 参考（非标准 UCSC chain），映射率 50.36%。未映射的 50% 为 Bellenguez 特有罕见/深imputed SNP，对 coloc 有覆盖损失。
3. **coloc lead 截断 200**：原设计为独立 lead SNP（clump 后 41 个），但本地 harmonize 无 clump 步骤，工具 SNP 达 2462 个，截断为 top 200 最显著（探索性近似）。
4. **失眠 s=0.30 为近似值**：UKB 失眠为二分性状，s(病例比例)取 0.30 为 UKB 自报失眠患病率近似，未做精确文献校准。coloc(type="cc")依赖此值。
5. **MRlap/CAUSE 可能跳过**：零联网约束下若 LD 参考面板不可用，两者 tryCatch 优雅跳过（不产出假数），需在 Limitations 披露。
6. **工具 SNP 来源**：2462/1132 来自本地 harmonize（两 clean 文件直接按 SNP ID 交集对齐），非 API clump。可能含 LD 连锁的冗余 SNP（未做 r²<0.001 clump），影响 IVW 精度。

## 【返回时请包含】

1. STORM 审计表（Markdown）
2. 因果方向结论（结构化）
3. Limitations 清单（6 项全覆盖 + 补充发现）
4. 下一步决策（G2/G4 启动建议 + 需补的数据/方法）
5. 任何审计中发现的额外风险或异常
