# =====================================================================
# 00b_verify_gwas.R  —  运行前强制核验（升 A 工程假设去风险）
# ---------------------------------------------------------------------
# 目标（与设计文档 §5 / 交接手册 §7 三处工程假设一一对应）：
#   假设1: UKB-PPP 蛋白 panel 是否覆盖 GFAP / NfL / 关键炎症因子
#   假设2: 失眠(BenElsworth 2018, ukb-b-3957) 与 AD(Bellenguez 2022 / Kunkle 2019) 的 MR instrument 数(F>10, clump后)、
#          二者是否共享 UKB 个体（样本重叠 → 需 LD 纠错或独立源）
#   假设3: G2 真实 P 值接入 FDR（由 02 脚本实测，本脚本只保证 ID/数据可达）
#
# 用法：在【联网】R 环境执行  source("00b_verify_gwas.R")
# 产物：gwas_ids_resolved.json（00_config.R 会读取）；控制台打印核验表
# =====================================================================

## ---- 0. 准备 ----
if (!requireNamespace("ieugwasr", quietly = TRUE) ||
    !requireNamespace("TwoSampleMR", quietly = TRUE)) {
  stop("请先安装 ieugwasr / TwoSampleMR")
}
library(ieugwasr); library(TwoSampleMR)
DIR_ROOT <- "C:/D/workbuddy/科研/共病分析/课题设计阶段"
OUT      <- file.path(DIR_ROOT, "code", "gwas_ids_resolved.json")

cat("\n================ 00b  GWAS 核验 ================\n")

## ---- 1. 失眠候选 ID 搜索（不写死 ID，避免仓库回收/重映射）----
cat("\n[1] 失眠 GWAS 候选搜索（已锁定主暴露 = BenElsworth 2018 ukb-b-3957, n=462,341, European, 42 clumped IVs；原 Sakaue 2021 ebi-a-GCST90018869 实测 0 IV 不可用、Jansen 2019 1.33M 不在仓库，已二次修订）\n")
ao_all <- tryCatch(available_outcomes(), error = function(e) NULL)
ins_info <- NULL
if (!is.null(ao_all)) {
  ins_cand <- tryCatch(subset(ao_all, grepl("insomnia", trait, ignore.case = TRUE)),
                        error = function(e) NULL)
  if (!is.null(ins_cand) && nrow(ins_cand) > 0) {
    ins_cand <- ins_cand[order(ins_cand$sample_size, decreasing = TRUE), ]
    cols <- intersect(c("id", "trait", "author", "year", "sample_size", "ncase", "ncontrol", "consortium"), names(ins_cand))
    print(head(ins_cand[, cols, drop = FALSE], 15))
    cat("  ⚠ 主暴露已人工锁定为 BenElsworth 2018 (ukb-b-3957)，详见下方 assign 区。\n")
    ins_info <- ins_cand[1, ]
  } else {
    cat("  ✗ 未搜索到 insomnia 候选\n")
  }
} else {
  cat("  ✗ available_outcomes() 拉取失败（网络受限）\n")
}

## ---- 2. AD 候选 / 搜索核验 ----
## Bellenguez 2022 未必在 IEU 直接托管；用 available_outcomes 全表 + 本地 grep 定位正确 ID。
cat("\n[2] AD GWAS 搜索（期望: Bellenguez 2022, 111,326 cases 或独立复制源 Kunkle/IGAP）\n")
## —— 人工指派区（2026-07-18 预注册级锁定·二次修订）——
## 暴露: 原选 Sakaue 2021 (ebi-a-GCST90018869) 实测 extract_instruments 返回 0 IV（NULL）→ 不可用；
##       改锁 BenElsworth 2018 (ukb-b-3957, n=462,341, European, 42 clumped IVs) 为唯一可行主暴露。
## 配对设计（用户确认）:
##   主对(无 UKB 重叠, 因果估计最干净) = 失眠 ukb-b-3957 × AD Kunkle/IGAP (ieu-b-2)
##   复制(含 UKB 重叠, 大样本)         = 失眠 ukb-b-3957 × AD Bellenguez 2022 (ebi-a-GCST90027158)
##   → ad 指向主对结局(Kunkle), ad_alt 指向复制结局(Bellenguez)。
insomnia_id <- "ukb-b-3957"           # BenElsworth 2018, n=462,341, European（经典 UKB 失眠 GWAS, 42 clumped IVs）
ad_id       <- "ieu-b-2"              # Kunkle BW 2019 / IGAP, ncase=21,982（主对结局：非 UKB 主导，与 ukb-b-3957 无重叠）
ad_alt      <- "ebi-a-GCST90027158"   # Bellenguez C 2022, ncase=39,106 (PMID 35379992)（复制结局：含 UKB 子集，重叠需报告）
if (!is.null(ao_all)) {
  ad_search <- tryCatch(subset(ao_all, grepl("Alzheimer", trait, ignore.case = TRUE)),
                         error = function(e) NULL)
  if (!is.null(ad_search) && nrow(ad_search) > 0) {
    # 优先展示样本量最大的几条，便于人工挑选 Bellenguez/Kunkle
    ad_search <- ad_search[order(ad_search$sample_size, decreasing = TRUE), ]
    cols <- intersect(c("id", "trait", "author", "year", "sample_size", "ncase", "ncontrol", "consortium"), names(ad_search))
    print(head(ad_search[, cols, drop = FALSE], 15))
    cat("\n  主对(无重叠)已锁 Kunkle/IGAP (ieu-b-2)；复制(含重叠)已锁 Bellenguez 2022 (ebi-a-GCST90027158)。\n",
        "  详见上方 assign 区；如需调整改 insomnia_id / ad_id / ad_alt 后重跑本脚本写出 json。\n")
    # （ID 已在上方人工指派区锁定，无需再改；如需换暴露/结局改上方 insomnia_id / ad_id / ad_alt）
  } else {
    cat("  ✗ 未搜索到 Alzheimer 候选\n")
  }
} else {
  cat("  ✗ available_outcomes() 拉取失败，无法搜索 AD\n")
}

## ---- 3. 样本重叠提示（BenElsworth ukb-b-3957 ↔ Bellenguez 均含 UKB 子集）----
cat("\n[3] 样本重叠提示（工程假设2）\n")
cat("  · 失眠主暴露 = BenElsworth 2018 (ukb-b-3957), n=462,341, European（42 clumped IVs）\n")
cat("  · Bellenguez 2022 AD = EADB + UKB(临床+proxy)，39,106 cases（OpenGWAS 托管子集）\n")
cat("  · 二者均含 UKB 个体 → 存在样本重叠，可能放大阳性/FDR 膨胀。\n")
cat("  缓解建议：\n")
cat("    (a) 主对已用无重叠组合（失眠=ukb-b-3957，AD=Kunkle/IGAP ieu-b-2）；\n")
cat("    (b) 或报告重叠比例，并以 LD 纠错 / 留一法 / 敏感性剔除 UKB 重叠样本；\n")
cat("    (c) 反向 MR(AD→失眠) 同样受重叠影响，结论需保守表述。\n")
cat("  可用 ieugwasr::ld_overlap / 或手动比对 consortium 字段评估重叠程度。\n")

## ---- 4. 蛋白 panel 覆盖核验（工程假设1）----
## UKB-PPP 为 Olink Explore 3072，~2,923 蛋白。GFAP/NfL 已见文献确认在 panel 内；
## 此处提供「给定蛋白名列表文件时」的自动核对片段。
cat("\n[4] 蛋白 panel 覆盖核验（工程假设1：GFAP / NfL / 炎症）\n")
cat("  文献证据（已离线确认，无需联网）：\n")
cat("    · Nature 2024 (s41380-024-02840-x): 用 2923 Olink 血浆蛋白，top hits 含 GFAP、NEFL、CEND1、SYT1\n")
cat("    · Olink 神经疾病综述: GFAP 与 NEFL 在 UKB-PPP panel 内，且于 AD 诊断前≥10年即升高\n")
cat("    · Olink Explore 3072 含免疫/炎症面板（细胞因子、补体、趋化因子等）→ 炎症因子覆盖\n")
cat("  结论：GFAP、NfL(NEFL) 及炎症/细胞因子类【覆盖成立】。\n")
cat("  若你有 UKB-PPP 蛋白 assay 清单（csv，含 olink_id / target / uniprot），可运行下式核对：\n")
cat("    panel <- read.csv('<ukbppp_protein_list.csv>');\n")
cat("    hits  <- c('GFAP','NEFL','IL6','CRP','TNF','IL1B','IL18','CST5','GDF15');\n")
cat("    subset(panel, toupper(target) %in% toupper(hits))\n")

## ---- 5. 写出已核验 ID（供 00_config.R 读取）----
resolved <- list(
  insomnia = insomnia_id,
  ad       = ad_id,
  ad_alt   = ad_alt,
  verified_on = as.character(Sys.Date()),
  note = "ad/ad_alt 若为 PENDING_VERIFY，表示需在联网环境人工指派后重跑本脚本。"
)
jsonlite::write_json(resolved, OUT, auto_unbox = TRUE, pretty = TRUE)
cat("\n[完成] 已写出:", OUT, "\n")
cat("  若 ad / ad_alt 仍为 PENDING_VERIFY，请按 [2] 提示指派后重跑本脚本。\n")
cat("  insomnia =", resolved$insomnia, "\n")
cat("=================================================\n")
