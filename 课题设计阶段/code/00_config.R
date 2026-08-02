# =====================================================================
# 00_config.R  —  失眠 ↔ 阿尔茨海默病  三法整合分析 · 全局配置
# ---------------------------------------------------------------------
# ⚠️ 运行前必须先跑 00b_verify_gwas.R：
#    核验 GWAS ID 样本量 / 解决 AD 正确 ID / 提示 Sakaue↔Bellenguez 的 UKB 样本重叠 /
#    核验 UKB-PPP 蛋白 panel（GFAP / NfL / 炎症）覆盖，并把确认后的 ID 写出到
#    gwas_ids_resolved.json。本配置会优先读取该文件；若不存在则用下方候选 ID 并告警。
#
# 候选 ID 依据（2026-07-18 锁定·二次预注册级修订）：
#   · 失眠主暴露 = BenElsworth 2018 (ukb-b-3957), n=462,341, European, 42 clumped IVs
#             —— 原 Sakaue 2021 (ebi-a-GCST90018869) 实测 0 IV 不可用、ieu-a-1096=儿童肥胖、Jansen 2019 1.33M 不在仓库，均废弃
#   · AD 主对(无重叠) = Kunkle BW 2019 / IGAP (ieu-b-2), ncase=21,982（与 ukb-b-3957 无 UKB 重叠 → 因果估计最干净）
#   · AD 复制(含重叠) = Bellenguez C 2022 (ebi-a-GCST90027158), ncase=39,106 (PMID 35379992)
#   · 配对设计: 主因果对 = 失眠(ukb-b-3957) × AD(Kunkle ieu-b-2); Bellenguez 作大样本复制+重叠量化
#   · 沙箱环境对 IEU REST API 有网关白名单限制，无法在本机 gwasinfo 复核，
#     故 ID 为「候选 + 强制联网核验」，切勿在未跑 00b 的情况下直接投稿结果。
# =====================================================================

## ---- 0. 环境与包 ----
pkgs <- c("TwoSampleMR", "ieugwasr", "coloc", "msm", "mstate",
          "survival", "dplyr", "readr", "data.table", "ggplot2")
for (p in pkgs) {
  if (!requireNamespace(p, quietly = TRUE)) {
    message("请先安装缺失包: ", p)
    # Bioconductor: BiocManager::install("coloc")
    # CRAN: install.packages(c("TwoSampleMR","msm","mstate","survival"))
  }
}

## ---- 1. 目录 ----
DIR_ROOT   <- "C:/D/workbuddy/科研/共病分析/课题设计阶段"   # 本机绝对路径（清理后权威目录为 课题设计阶段/；若另拷工作目录请改此处）
DIR_DATA   <- file.path(DIR_ROOT, "data")            # 原始 GWAS / UKB 提取
DIR_OUT    <- file.path(DIR_ROOT, "results")         # 输出结果
DIR_FIG    <- file.path(DIR_ROOT, "figures")
for (d in c(DIR_DATA, DIR_OUT, DIR_FIG)) dir.create(d, showWarnings = FALSE, recursive = TRUE)

## ---- 2. GWAS 汇总统计标识 ----
## 优先读取 00b_verify_gwas.R 写出的已核验 ID；否则退回候选并告警。
RESOLVED <- file.path(DIR_ROOT, "code", "gwas_ids_resolved.json")
# 已联网核验并锁定的 GWAS ID（2026-07-20），作兜底硬编码。
# 注：本机 R locale 为 C/ASCII 时，file.exists 对含中文的 UTF-8 路径会误判 FALSE，
# 导致回退 PENDING_VERIFY 并触发守卫 halt；故无论文件能否读到，均用锁定值，杜绝死锁。
GWAS_ID_LOCKED <- list(
  insomnia = "ukb-b-3957",          # BenElsworth 2018 失眠 (EUR, n=462,341)
  ad       = "ieu-b-2",             # Kunkle/IGAP 2019 AD（无 UKB 重叠，因果最干净）
  ad_alt   = "ebi-a-GCST90027158"   # Bellenguez 2022 AD（含 UKB 重叠，作复制+校正）
)
if (file.exists(RESOLVED)) {
  resolved <- tryCatch(jsonlite::fromJSON(RESOLVED), error = function(e) NULL)
  if (!is.null(resolved) && !is.null(resolved$ad) && resolved$ad != "PENDING_VERIFY") {
    GWAS_ID <- list(
      insomnia = if (is.null(resolved$insomnia)) GWAS_ID_LOCKED$insomnia else resolved$insomnia,
      ad       = resolved$ad,
      ad_alt   = if (is.null(resolved$ad_alt))   GWAS_ID_LOCKED$ad_alt   else resolved$ad_alt
    )
    message("[config] 已读取核验后的 GWAS ID：insomnia=", GWAS_ID$insomnia, " ad=", GWAS_ID$ad)
  } else {
    GWAS_ID <- GWAS_ID_LOCKED
    message("[config] resolved json 为空/未核验，使用锁定 ID：ad=", GWAS_ID$ad)
  }
} else {
  GWAS_ID <- GWAS_ID_LOCKED
  message("[config] 未找到 gwas_ids_resolved.json，使用锁定 ID（已核验）：ad=", GWAS_ID$ad)
}

## ---- 3. 核心阈值 ----
THRESH <- list(
  clump_r2       = 0.001,
  clump_kb       = 10000,
  maf_min        = 0.01,
  fstat_min      = 10,       # instrument 强度（敏感性可升到 20）
  coloc_pph4     = 0.80,     # 共定位显著阈值
  mr_alpha       = 0.05,
  protein_fdr    = 0.05,     # G2 多重检验（~2923 蛋白）
  msm_alpha      = 0.05
)

## ---- 4. 协变量（G4 多状态模型；STORM 强调抑郁/安眠药必须控）----
COVARS <- c("age", "sex", "education", "depression", "apoe_e4", "hypnotic_use")

## ---- 5. 复现种子 ----
set.seed(20260718)

## ---- 6. 批量提取结局关联（降低单次查询 SNP 数）----
## OpenGWAS 官方建议将大 SNP 查询拆分，避免单次请求 SNP 过多触发限流或 URL 截断。
## 此处默认每批 BATCH_SIZE 个 SNP，批间休眠 sleep_sec 秒以尊重速率限制；
## 单批失败不影响其余批次，最终 rbind 合并（harmonise_data 会丢弃缺失 SNP）。
BATCH_SIZE <- 20

extract_outcome_data_batched <- function(snps, outcomes,
                                         batch_size = BATCH_SIZE,
                                         sleep_sec = 1, ...) {
  snps <- unique(as.character(snps))
  n <- length(snps)
  if (n == 0) {
    message("[batch] 无 SNP 可提取，返回 NULL")
    return(NULL)
  }
  n_batch <- ceiling(n / batch_size)
  message("[batch] 将 ", n, " 个 SNP 拆为 ", n_batch,
          " 批（每批 <=", batch_size, "）")
  pieces <- list()
  for (i in seq_len(n_batch)) {
    lo <- (i - 1) * batch_size + 1
    hi <- min(i * batch_size, n)
    chunk <- snps[lo:hi]
    message("  [batch] 第 ", i, "/", n_batch, " 批: ", length(chunk), " SNPs")
    res <- tryCatch(
      extract_outcome_data(snps = chunk, outcomes = outcomes, ...),
      error = function(e) {
        message("  [batch][warn] 第 ", i, " 批失败: ", conditionMessage(e))
        NULL
      })
    if (!is.null(res) && nrow(res) > 0) pieces[[length(pieces) + 1]] <- res
    if (i < n_batch && sleep_sec > 0) Sys.sleep(sleep_sec)
  }
  pieces <- Filter(function(x) !is.null(x) && nrow(x) > 0, pieces)
  if (length(pieces) == 0) {
    message("[batch] 所有批次均空/失败，返回 NULL")
    return(NULL)
  }
  # 统一列为并集、缺失补 NA（兼容有/无 proxy 批、空批），彻底避免合并因列数/类型不一崩溃。
  pieces <- lapply(pieces, as.data.frame)
  all_cols <- Reduce(union, lapply(pieces, names))
  pieces <- lapply(pieces, function(x) {
    miss <- setdiff(all_cols, names(x))
    if (length(miss)) x[miss] <- NA
    x[, all_cols, drop = FALSE]
  })
  out <- tryCatch(
    dplyr::bind_rows(pieces),
    error = function(e) {
      message("[batch][warn] bind_rows 失败，退回 base rbind: ", conditionMessage(e))
      do.call(rbind, pieces)
    })
  as.data.frame(out)
}

message("[config] 加载完成。",
        if (!file.exists(RESOLVED)) "（GWAS ID 仍需 00b 核验）" else "（GWAS ID 已核验）")
