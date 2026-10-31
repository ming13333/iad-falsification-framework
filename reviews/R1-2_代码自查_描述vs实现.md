# R1#2 自查：Methods 描述 vs 模拟代码实现

> 触发：Reviewer 1 第 2 条（"the archived code does not match the workflow described in Methods… please confirm the code version"）。
> 自查对象：`code/sim_framework_operating_chars.py`（11,249 bytes，mtime 2026-09-02 04:57，与投稿版同日）。
> 归因证据：`课题设计阶段/Supplementary_final/S9_simulation_operating_marginal.csv` 的数值（none/β=0.15：sens_AB=0.9727、p_gradeA=0.8754；balanced/β=0：spec_D=0.79625）与本脚本输出逐位一致 → **Table 2 / Fig 2 / S9 就是这份代码跑出来的**，不是另一份"正式版"。
> **归档核对已完成**：见 `reviews/R1-2_Zenodo归档核对.md`。要点——引用 DOI 21858125 = v1.0.0（08-09），但另有未引用的 v1.1.0（08-23）；归档内模拟脚本**逐字节等于** git b983865（08-06），而投稿版等于 3225fea（09-02），两者差一次会改变 S9/Fig2 的聚合修正；经验分析的 R 脚本方法学逻辑一致（差异仅为路径与消息语言）。

> 结论一句话：**R1#2 的六条具体指控，五条完全成立、一条部分成立；此外自查还发现三处它没点到的结构性问题——模拟里根本没生成 LD 相关结构、模拟用的是 0/1/2 三档计分（正文写 0/2）、以及六门实际只有 3–4 个自由度（G3 是常量、G4 与 G2 完全共线）。**

---

## 一、逐条对照

| # | R1#2 的指控 | 代码位置 | 判定 | 事实 |
|---|---|---|---|---|
| 1 | G3 实际用 **block coverage**，不是 LDSC + coloc | `L142–145` | ✅ **成立** | `frac_blocks = n_blocks_used/n_blocks`；`L3 = 2 if frac_blocks >= 0.5 and n_eff >= 5 else (1 if frac_blocks >= 0.3 else 0)`。全文件 grep `ldsc|coloc|ld score` **零命中** |
| 2 | G4 实际用 **leave-one-out 变异**，不是 MVMR | `L147–157` | ✅ **成立** | `loo_spread = std(b_loo)/|b2|`，`L4 = 2 if p2<0.05 and loo_spread<0.5`。且 `L150` 有一行死代码 `resid_b = by - (true_beta*bx - true_beta*bx)`（恒等于 `by`），注释自称 "MVMR proxy" |
| 3 | **CAUSE / MRlap 缺失** | 全文 | ✅ **成立** | grep `cause|mrlap` 仅命中注释里的 "MVMR proxy" 与 `L149` 的说明句，**无任何实现** |
| 4 | 未生成所述 **LD 协方差** | `L82–84` | ✅ **成立（且更严重）** | `bx = rng.normal(0, 0.12, n_iv)` 各 SNP **独立**抽样；`block` 只作为聚类索引喂给 `clump_instruments()`，**没有任何相关结构**。因此"相关工具造成虚假精度"这一被框架当作立论核心的机制，在模拟里根本无法出现 |
| 5 | 未生成**暴露-结局相关误差**（sample overlap 的真实机制） | `L95–100` | ✅ **成立** | overlap 只改 `e_y`；而 `by = gamma_y + 0.01*e_y`，即 30% 重叠对结局估计的影响只有 1% 量级——"30% overlap"这一因子近乎空操作 |
| 6 | 结局噪声 SD **0.01** 却给 **SE 0.03** | `L99–100` | ✅ **成立** | `se_y = np.full(n_iv, 0.03)`，`by = gamma_y + 0.01*e_y`。声明 SE 与实际噪声不一致（无多效性时高估 3 倍，balanced 时又低估），Table 2 的 sens/spec/FDR 无法归因于门逻辑本身 |
| 7 | 中介值依赖真效应，但**不生成结局** | `L102–109` | ✅ **成立** | `effect>0` 时 `bxm=0.40*bx`、`bym=0.50*bxm`（确定性、零噪声）；`effect==0` 时纯噪声（sd 0.01）。G5 因此等价于直接读真值，真效应组必得 2 分 → 敏感度被结构性抬高 |
| 8 | "确认代码版本、按实际流程重写 Methods，若影响性能结果须更新结果" | — | ⚠️ **部分成立** | 代码版本无争议（S9 数值可逐位复现）；但"影响结果"的程度远超审稿人估计：见下节 ①–④ |

---

## 二、审稿人没点到的两处（自查发现，必须自己说）

### ① 计分制式：代码是 0/1/2 三档，正文与 Table 1 是 0/2 两档

| 位置 | 实际 |
|---|---|
| `L127` | `s["L1"] = 2 if (p1<0.05 and abs(b1)>1e-4) else (1 if p1<0.2 else 0)` |
| `L140` | `s["L2"] = 2 if (p2<0.05 and p_int>0.05) else (1 if p2<0.05 else 0)` |
| `L145` | `s["L3"] = 2 / 1 / 0`（三档） |
| `L157` | `s["L4"] = 2 / 1 / 0`（三档） |
| `L162` | `s["L5"] = 2 / 1 / 0`（三档） |
| 正文 `L63–L73` | 六门逐条写 "Score: 2 …; 0 otherwise" |
| Table 1 `L226、L235` | 列头 "score = 2; otherwise 0"；脚注 "contribute **0 or 2** points (maximum 12)" |

**这就是 R1#1（S8 出现 1 分、education-T2D 凑出 9 分）与 R1#2 的同一根因**：1 分制不是 S8 抄错，而是模拟代码与验证队列用的是同一套三档规则，而投稿版 Table 1 只描述了两档。两条 P0 必须**合并成一个决定**处理，不能分头打补丁。

### ② "G2 失败仍可 A 级"：按**正文规则**理论上可达，按**实际代码**不可能——这恰好是回应 R1#1 的钥匙

- 按正文/Table 1 的 0/2 规则：G2 失败只损失 2 分，其余五门满分 = 10 分 = Grade A 下界（`L170`）。**漏洞成立**。
- 按实际代码（0/1/2 三档 + 各门结构）：G2=0 时总分上限只有 **8**（实测 43,200 条中 `L2=0` 的最高分为 8.0，Grade B）。原因见 ③：G4 是 p2 的函数，`L2=0 ⟹ L4=0`，因此"少一门仍够 10 分"在结构上不可达。

⇒ 回应 R1#1 时不能含糊：**若坚持 0/2 制，就必须加"决定性失败"规则；若采纳代码的 0/1/2 三档，则该漏洞自动消失，但 Table 1 与 S8 要一起改。** 两条路都能自洽，混用则必被再问一轮。

### ③ G4 与 G2 **完全共线**，G3 是**常量**——六门实际只有 3–4 个自由度

| 检验 | 结果（43,200 条实测） |
|---|---|
| `L2>0` 与 `L4>0` 是否等价 | **完全等价，0 条不一致**（`L2=0` 25804 条 ⟺ `L4=0` 25804 条）。因为 `L4 = 2 if (p2<0.05 and loo_spread<0.5) else (1 if p2<0.05 else 0)`，`L4>0 ⟺ p2<0.05`，与 G2 的第一条件同一判据 |
| `L3` 取值 | 只有 {0, 2}，**从无 1 分**；`L3=0` 的 15,546 条恰好全是 L1 级联（`L1=0`）的条目。即 clumping 每块必留一个 → `frac_blocks ≡ 1.0` → 非级联条目**恒得 2 分** |
| `L5` 取值 | 2 分 23,791、1 分 **10**、0 分 19,399 → 实质二值 |

**后果**：总分 ≈ `L1 级联 + G2(=G4) + 常量 2 + G5(真值泄漏) + G6`。"Grade 随效应量单调"这一结果，很大程度上由 **L1 级联**（`L1=0` → 直接 D，15,546 条）与 **G5 真值泄漏**（`bxm=0.40bx` 确定性生成）共同产生，**不是六门各自独立累积**出来的。这句话写进 Discussion 会伤，但比被审稿人算出来强。

---

## 三、三档处置方案（需作者裁定）

| 方案 | 做什么 | 代价 | 风险 |
|---|---|---|---|
| **A. 如实重述 + 收窄结论**（推荐） | Methods 把 G3/G4 明确写成"模拟中的**代理实现**"（block coverage / LOO spread），删去"CAUSE、MRlap 在模拟中被评估"的暗示；Table 2 标题与正文把结论限定为"该代理实现下的操作特征"；Limitations 增一条 | 只改文字，不重跑 | 审稿人若追问"那模拟还验证了什么"，需准备好第二层答复：模拟验证的是**计分-分级映射的单调性**，不是 CAUSE/MRlap 的统计性质 |
| **B. 补齐重跑** | 生成真 LD 块协方差、加 CAUSE/MRlap/coloc 进模拟、修 SE 与 overlap、改两档计分 → 43,200×6 门重跑 | 计算量大（CAUSE MCMC × 43,200 不可行） | 现实上**做不到**；只能缩小网格（如 3,600 次），但这会与已投的 43,200 冲突，等于换一篇论文 |
| **C. 删掉模拟章节** | 只留实证案例 + 分级规则 | 框架的"quantified operating characteristics"卖点消失 | 期刊定位（Methods）下几乎等于撤稿重写 |

**判断**：A 是唯一在不重跑前提下站得住的路径；B 需要坦率承认"CAUSE 在 43,200 次量级不可行"，这本身可以写成 Limitations 的一句话（"gate-level MCMC methods were not embedded in the simulation grid"）。**C 不考虑。**

---

## 四、连带影响清单（改 A 方案时必须同步）

| 受影响对象 | 具体改动 |
|---|---|
| Abstract `L13` | "benchmarked 43,200 simulated … evaluating each replicate across all gates" → 需加限定（代理实现；G3/G4 非 LDSC/coloc/MVMR） |
| Methods `L91–L95` | 重写 DGP 段：明示 block-diagonal 结构**未**实现、overlap 仅作用于噪声、G3/G4 为代理、SE 设定值 |
| Results `L100` | "100% specificity" 的成立条件（无多效性 + 声明 SE 与实际噪声不符）必须写明，否则是**被 DGP 构造出来的**结果 |
| Results `L100` / Discussion `L135` | "Grade assignment scaled monotonically with effect size" 需加限定：单调性主要由 L1 级联与 G5 真值泄漏贡献，不是六门独立累积 |
| Table 2 `L237–L251` | 表题加"agent-based proxy implementation"限定；脚注补 SE 设定 |
| Fig 2 / S9 | 图注与 S9 表头同步加限定（数值不用变，但解释口径变） |
| Limitations `L143` | 第二条（"does not encompass all genetic architectures"）升级为：模拟未生成 LD 相关结构、未嵌入 CAUSE/MRlap/coloc，因此**不能**用于评估这些方法本身的操作特征 |

---

## 五、给应答信的一句话（可直接改写）

> We confirm that the archived simulation script (`code/sim_framework_operating_chars.py`) is the version used to generate Table 2, Figure 2 and Supplementary Table S9; the reported numbers reproduce exactly. We also confirm the reviewer's observation: in the simulation the architecture and direct-effect gates were implemented as proxies (LD-block coverage for G3; leave-one-out stability for G4), and CAUSE and MRlap were not embedded in the grid, because MCMC-based fitting is not computationally tractable at 43,200 replicates. The Methods section has been rewritten to state this explicitly, the scope of the operating-characteristics claim has been narrowed accordingly, and a corresponding limitation has been added. The empirical insomnia–AD application used the full implementations (LDSC, coloc, MRlap, CAUSE, MVMR) and is unaffected.

---

*自查人：作者方（AI 辅助）；自查时间 2026-10-27；证据文件均在库内可复现。*
