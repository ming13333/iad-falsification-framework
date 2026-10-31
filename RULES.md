# RULES.md · 失眠↔AD 六门证伪框架（只放长期规则）

> 新 session 先读本文件 + `progress.md`，再动手。本文件 ≤300 字，**不放进度**。

## 工作法
- 聊天 = 草稿纸；结论 / 数字 / 决策一律落本地文件。
- 每完成一个节点，**覆盖**更新 `progress.md`（快照，非流水账）。
- 已结束记录归档 `.workbuddy/memory/YYYY-MM-DD.md`（append-only，平时不读）。

## 证据红线
- 不编数值 / DOI / PMID / 样本量 / 版本号；无源不写，不确定就说不知道。
- 关键统计量必须能追到 `results/` 或 memory 日志里的实测记录。
- **禁引 PhenoScanner**（已死 + 本机出口封锁）；IV 多效性改用 GWAS Catalog 双轨或 MR 诊断（Egger / LOO / Steiger / Cochran Q）。
- 跑不出来的数（UKB 个体级、LIVE OpenGWAS）**不得用占位数字冒充**。

## 环境坑（勿回退）
- R 不写中文路径 → 输出到 `C:/Temp/iad_g1/` 再 cp 回。
- `gwasapi.mrcieu.ac.uk` 本机出口封锁；离线复现走 `data/raw/c1_cache/`。
- OpenGWAS token **2026-09-15 已过期**，LIVE 拉取前须重生成写 `~/.Renviron`。
- docx 用 python-docx，**勿用 editor_sdk**；`git push` 已修（GCM selector 已移除），直接推。

## 禁碰
- 不删 `课题设计阶段/`、`manuscript/`、`data/raw/c1_cache/`、`.workbuddy/memory/`。
- 已投稿版本的 md/docx **不改**，新版另存新名。

## 续接口令
读 `RULES.md` + `progress.md`，接着干。
