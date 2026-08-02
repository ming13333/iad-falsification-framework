#!/usr/bin/env Rscript
# ============================================================
# download_metabolites_fullss.R
# 目的: 将 C1 代谢物中介所用 GWAS 本地落盘（可复现性）。
# 重要背景 (2026-08-02 实测):
#   - IEU 静态 full-SS 端点已失效: gwas.mrcieu.ac.uk/downloads/{id}/
#     与 /downloads/{id}.tsv.gz 均 301->opengwas.io->404。
#   - extract_instruments(id, p1=) 限 0<pval<=0.01, 不能拉全 GWAS。
#   - associations(id, variants=) 可重建全 SS, 但内部 ~64 变体分块,
#     1.19M SNP 性状需 ~1.86万次调用 (缓慢, 单性状 ~20min)。
# 故提供两种本地化方式:
#   MODE="top1pct"  (默认, 快速): extract_instruments(p1=0.01, clump=FALSE)
#                      -> 各代谢物 top~1% GWAS 提取 (p<0.01), MR 可用。
#   MODE="fullframe" (慢, 需网络): associations(id, variants=<AD rsID 帧>)
#                      -> 在 AD SNP 帧内重建全 SS (非字面全 GWAS, 但覆盖 C1 全部 lookup)。
# 运行: Rscript code/download_metabolites_fullss.R [top1pct|fullframe]
# ============================================================
suppressMessages(library(TwoSampleMR)); suppressMessages(library(data.table))
mode <- if (length(commandArgs(trailingOnly = TRUE)) > 0) commandArgs(trailingOnly = TRUE)[1] else "top1pct"
OUT  <- "c:/D/workbuddy/科研/共病分析/data/raw/metabolites"
dir.create(OUT, showWarnings = FALSE, recursive = TRUE)
mets <- c("met-d-Total_C","met-d-LDL_C","met-d-HDL_C","met-d-Total_TG",
          "met-d-DHA","met-d-Omega_3","met-d-Ile","met-d-Leu","met-d-Val","met-d-GlycA")
cat(sprintf("MODE=%s\n", mode))

if (mode == "top1pct") {
  for (m in mets) {
    d <- tryCatch(extract_instruments(m, p1 = 0.01, clump = FALSE, r2 = 0, kb = 0),
                  error = function(e) NULL)
    if (!is.null(d) && nrow(d) > 0) {
      fwrite(d, file.path(OUT, sprintf("%s.top1pct.tsv.gz", m)), sep = "\t")
      cat(sprintf("  %s: %d SNPs (top-1%% extract, p<0.01)\n", m, nrow(d)))
    } else cat(sprintf("  %s: FAILED\n", m))
  }
  cat("DONE (top-1% extracts). NOTE: not literal full SS; use cache_c1_inputs.R for exact C1 reproducibility.\n")
} else if (mode == "fullframe") {
  ad <- fread("c:/Temp/iad_g1/code/ieu-b-2.tsv", select = c("rsid"))
  for (m in mets) {
    a <- tryCatch(associations(id = m, variants = ad$rsid), error = function(e) NULL)
    if (!is.null(a) && nrow(a) > 0) {
      fwrite(a, file.path(OUT, sprintf("%s.fullframe.tsv.gz", m)), sep = "\t")
      cat(sprintf("  %s: %d SNPs (full SS in AD frame)\n", m, nrow(a)))
    } else cat(sprintf("  %s: FAILED\n", m))
  }
  cat("DONE (full SS in AD frame). Heavy: ~1.86e4 API calls per trait.\n")
} else stop("MODE must be 'top1pct' or 'fullframe'")
