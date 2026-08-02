#!/usr/bin/env Rscript
# ============================================================
# cache_c1_inputs.R
# 目的: 在线抓取 C1 代谢物中介分析 (09b) 的全部 harmonised 输入，
#       本地落盘到 data/raw/c1_cache/，使 local_run_C1.R 可零 API 复现。
# 背景: IEU 静态 full-SS 下载端点已失效 (301->404)，associations() 需
#       变体列表且内部按 ~64 变体分块 (1.19M SNP 需 ~1.8万次调用，不可行)。
#       故改为缓存 09b 实际使用的 harmonised 表 —— 这是可复现性的最小完备集。
# 运行: Rscript code/cache_c1_inputs.R  (需联网 / 禁用沙箱)
# ============================================================
suppressMessages(library(TwoSampleMR))
suppressMessages(library(data.table))

EDU_ID <- "ieu-a-1239"
AD_ID  <- "ieu-b-2"
OUT    <- "c:/D/workbuddy/科研/共病分析/data/raw/c1_cache"
dir.create(OUT, showWarnings = FALSE, recursive = TRUE)

mets <- c("met-d-Total_C","met-d-LDL_C","met-d-HDL_C","met-d-Total_TG",
          "met-d-DHA","met-d-Omega_3","met-d-Ile","met-d-Leu","met-d-Val","met-d-GlycA")

cat("=== Step 0: education instruments (clumped, mirrors 09b) ===\n")
edu <- extract_instruments(EDU_ID, p1 = 5e-8, r2 = 0.001, kb = 10000)
cat("  edu IVs:", nrow(edu), "\n")
fwrite(edu, file.path(OUT, "edu_instruments.tsv.gz"), sep = "\t")

man <- data.frame(met = character(), step = character(),
                  n_snps = integer(), src = character(), stringsAsFactors = FALSE)

for (m in mets) {
  cat(sprintf("\n--- %s ---\n", m))
  # Step 1: edu -> metabolite (exposure = edu, outcome = metabolite)
  od1 <- tryCatch(extract_outcome_data(snps = edu$SNP, outcomes = m), error = function(e) NULL)
  if (!is.null(od1) && nrow(od1) > 0) {
    h1 <- tryCatch(harmonise_data(edu, od1), error = function(e) NULL)
    if (!is.null(h1) && nrow(h1) >= 3) {
      fwrite(h1, file.path(OUT, sprintf("%s_step1_harm.tsv.gz", m)), sep = "\t")
      cat(sprintf("  step1 harm: %d SNPs\n", nrow(h1)))
      man <- rbind(man, data.frame(met = m, step = "step1_edu_to_met",
                                   n_snps = nrow(h1), src = "extract_outcome_data+harmonise",
                                   stringsAsFactors = FALSE))
    } else cat("  step1 harmonise failed/small\n")
  } else cat("  step1 no outcome data\n")

  # Step 2: metabolite -> AD (exposure = metabolite, outcome = AD)
  minstr <- tryCatch(extract_instruments(m, p1 = 5e-8, r2 = 0.001, kb = 10000),
                     error = function(e) NULL)
  if (!is.null(minstr) && nrow(minstr) >= 3) {
    fwrite(minstr, file.path(OUT, sprintf("%s_instruments.tsv.gz", m)), sep = "\t")
    ad_od <- tryCatch(extract_outcome_data(snps = minstr$SNP, outcomes = AD_ID),
                      error = function(e) NULL)
    if (!is.null(ad_od) && nrow(ad_od) > 0) {
      h2 <- tryCatch(harmonise_data(minstr, ad_od), error = function(e) NULL)
      if (!is.null(h2) && nrow(h2) >= 3) {
        fwrite(h2, file.path(OUT, sprintf("%s_step2_harm.tsv.gz", m)), sep = "\t")
        cat(sprintf("  step2 harm: %d SNPs (met IVs=%d)\n", nrow(h2), nrow(minstr)))
        man <- rbind(man, data.frame(met = m, step = "step2_met_to_AD",
                                     n_snps = nrow(h2), src = "extract_outcome_data+harmonise",
                                     stringsAsFactors = FALSE))
      } else cat("  step2 harmonise failed/small\n")
    } else cat("  step2 no AD overlap\n")
  } else cat("  step2 <3 metabolite IVs\n")
}
fwrite(man, file.path(OUT, "MANIFEST.csv"), sep = ",")
cat("\n=== CACHE DONE ===\n"); print(man)
