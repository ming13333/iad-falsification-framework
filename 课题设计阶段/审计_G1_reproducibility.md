# G1 阶段可复现性审计报告

- **审计日期**:2026-07-21
- **审计对象**:`code/01_bidirectional_mr_coloc.R` + `code/extract_g1_readable.R`,输出 `results/`
- **审计框架**:ai-research-repro-guard(DRIL + Reviewer Mode)
- **审计人**:罗经纬(主理人,独立复核,非脚本自审)

---

## 0. 总裁决

**核心 MR + coloc 结果:可复现(同环境 + 同 OpenGWAS 快照下,逐字节一致)。**
**形式上"完美复现":尚未达到。** 存在 4 个阻断性缺口(版本未锁定、无随机种子、数据未冻结、重叠校正未运行)与 2 个透明度/方法学待披露项。

> 即:在你这台机器、用当前 OpenGWAS 数据再跑一次,数字会和现在完全一样(已用 rds MD5 验证)。但若换环境、或 OpenGWAS 将来更新了这几个 GWAS,结果可能漂移——且重叠校正这步目前根本没跑。

---

## A. 已验证一致 / 无错的部分(PASS)

| 检查项 | 结果 |
|---|---|
| rds 跨两次运行一致性 | `G1_bidirectional.rds` MD5 完全相同(`34516ee2…761649b`),逐字节一致 |
| 4 个 coloc CSV 跨两次运行 | `diff` 全部一致 |
| summary 数字 vs 运行日志 | IVW β/se/p、Cochran Q、Egger 截距、F 值全部吻合,无造假 |
| coloc 模式 | 已用 `type="cc"` + 真实 `ncase/ncontrol` 推 `s`,**未再出现 "must give sdY for type quant"** |
| 回文 SNP 删除 | 已显式打印(如 forward 删 10 个),**非静默丢弃** |
| 重叠校正未运行 | `G1_summary.txt` 诚实标注 `overlap_correction_run = FALSE` 并要求 Limitations 披露,**非静默丢弃** |
| 方向一致性 | 正向(失眠→AD)四种 MR 方法均不显著;反向(AD→失眠)四种均显著且同向;Bellenguez 复制反向仍显著 → 反向因果信号稳健 |

---

## B. 阻断"完美复现"的硬缺口(须修复,GAP)

### B1. 无版本锁定(environment.yml / renv.lock 缺失) ⛔高
- 脚本未钉任何包版本。已知版本来自运行日志:R 4.5.3、TwoSampleMR 0.7.9、ieugwasr、coloc 5.2.3。
- 风险:TwoSampleMR/coloc 跨小版本行为可能变(如 `harmonise_data` 默认 action、coloc 默认值),重跑结果可能不可复现。
- **修复**:在 code 目录跑 `renv::init()` + `renv::snapshot()`,或在 00_config 头部写 `sessionInfo()` 落盘。`MRlap`/`CAUSE` 一旦安装也须纳入。

### B2. 无随机种子 set.seed ⛔高
- 全文 grep `set.seed` = 0 命中。
- MR/coloc 本身确定性(无随机),但 **MR-PRESSO** 与 **CAUSE 的 MCMC** 含随机性。当前 CAUSE 未跑;一旦跑,不设种子则每次 MCMC 结果微漂移,无法逐字节复现。
- **修复**:在 01 脚本开头 `set.seed(20260721)`(并记入方法)。

### B3. OpenGWAS 实时拉取,数据未冻结 ⛔高
- `ukb-b-3957` / `ieu-b-2` / `ebi-a-GCST90027158` 每次运行都从 OpenGWAS 在线取。
- 风险:OpenGWAS 后续更新注解/样本量,同 accession 重跑返回不同数据 → 版本漂移(技能明确警示项)。
- **修复**:首次成功运行后,把三个 GWAS 全量关联用 `ieugwasr::associations()` 存为本地 `.rds`,记录**下载日期 + accession 版本**;脚本增加"本地优先,缺失才在线"分支。这同时能加速 CAUSE(避免每次重拉百万级 SNP)。

### B4. 重叠校正(MRlap/CAUSE)未运行 → Phase 2 未收口 ⛔高
- `results/` 当前**无 `G1_mrlap.csv` / `G1_cause.csv`**。
- 意义:课题预设的"样本重叠校正 + 多效性区分"敏感性分析尚未执行,Phase 2 数学上未完成。
- **修复**:装对包(`n-mounier/MRlap` + r-universe `cause`)后重跑;见下方"修复清单"。

---

## C. 透明度 / 方法学待披露项(发表前须处理)

### C1. 各方向最终工具 SNP 数未显式打印 ⚠️中
- `n_snps` = `nrow(dat)`(harmonise 后传入 coloc 的行数):正向 41、反向 17。
- **数字不自洽点**:正向日志"提取 42 个 SNP、删 10 个回文"→ 算术应剩 32,但 coloc 收到 41。差值只能由 harmonise 阶段的 **proxy 插入**解释(42 − 10 删 + 9 个 proxy ≈ 41),而脚本未打印此过程,读者无法核对。
- 反向 18 − 1 = 17 对得上,说明 proxy 插入不是每方向都发生,更需显式记录。
- **修复**:在 `run_coloc` 调用前 `message("方向 X 最终工具 SNP 数: ", nrow(dat))`,并在 summary 增加一列。

### C2. coloc 为"全 IV 单数据集"而非逐 locus LD 区域 ⚠️中
- 当前每个方向只跑一次 coloc(把全部工具 SNP 当一个数据集),PP.H4 是"全基因组共享信号"概率,不是某个独立 LD 区域的共定位。
- 日志里"位点数 0/1、1/1"只是在数"这唯一一次跑有没有过 0.80 线",易误导成"扫了多个位点"。
- **修复(发表级)**:改为按独立 LD 区域(`ieugwasr::ld_clump` 或 1000G LD)分段跑 coloc,统计通过 0.80 的 locus 数。当前结果可作探索,正文须注明方法。

### C3. Steiger 方向性检验对二分类性状整体跳过 ⚠️低
- 因 `get_r_from_lor` 需 `ncase/ncontrol`,二分类性状未跑 Steiger,方向性完全依赖"双向 MR + coloc"一致性。
- 这是合理设计,但方法部分须写明,并说明为何反向因果判定不依赖 Steiger。

---

## D. 对"结果已经全部生成"的纠正

不准确。当前 `results/` 含:G1_bidirectional.rds、4 个 coloc CSV、G1_summary.txt(刚由 extract 生成)。
**缺**:`G1_mrlap.csv`、`G1_cause.csv`(重叠校正输出)。
好在 `G1_summary.txt` 已诚实标 `overlap_correction_run = FALSE`,所以这不是"静默丢弃",而是"这步还没做"。Phase 2 收口前必须补。

---

## E. 修复清单(主理人可执行 vs 需你拍板)

**我可直接改代码(低风险,你重跑验证即可):**
1. 01 脚本开头加 `set.seed(20260721)`。
2. `run_coloc` 调用前加 `message("... 最终工具 SNP 数: ", nrow(dat))`,summary 增列。
3. 加"本地 GWAS 优先"分支 + `sessionInfo()` 落盘到 `results/env_sessionInfo.txt`。
4. 生成 `renv.lock`(需在你机器跑 `renv::snapshot()`)。

**需你拍板的设计决策:**
5. 是否把 GWAS 冻结为本地 `.rds`(推荐是,但占空间、且需你本机先拉一次)。
6. coloc 是否升级为逐 locus LD 区域(工作量大,建议作为"发表级"单独排期,不阻塞当前 Phase 2 收口)。
7. 装包跑 MRlap/CAUSE 重叠校正(你之前已同意,尚未执行)。

---

## F. Reviewer Mode 一句话结论

> "MR 与 coloc 核心结果内部一致、可复现,且缺失/跳过项均已诚实披露,无 AI 静默错误。但本分析尚未达到可发表级复现标准:缺版本锁定、随机种子与数据冻结,且计划内的样本重叠校正(MRlap/CAUSE)尚未执行。三项加齐、并把工具 SNP 计数与 coloc 区域化方法写清后,方可声称'完美复现'。"

---

*审计原则遵循 ai-research-repro-guard:人类决定结论,agent 仅执行;本审计为独立复核,非脚本自审。*
