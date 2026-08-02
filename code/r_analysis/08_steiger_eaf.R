# B2 v2: 补 eaf + Steiger（高效版）
# 策略：用 TwoSampleMR 原生 extract_instruments/outcome 获取 eaf
# 仅处理 clumped 主集（54 SNP, r2=0.1），避免 2462 SNP 批量查询超时
# 运行须 --dangerouslyDisableSandbox（联网）

suppressWarnings({
  library(TwoSampleMR)
  library(ieugwasr)
})

setwd("C:/Temp/iad_g1")
dir.create("results/steiger", showWarnings = FALSE, recursive = TRUE)

# ============================================================
# 1. 获取 clumped insomnia instruments（含 eaf）
# ============================================================
cat("[1] Extracting clumped insomnia instruments with eaf...\n")
ins_exp <- tryCatch({
  extract_instruments(
    outcomes = "ukb-b-3957",
    clump = TRUE,
    p1 = 5e-8,
    r2 = 0.1,
    kb = 10000
  )
}, error = function(e) {
  cat("  extract_instruments failed:", conditionMessage(e), "\n")
  NULL
})

if (!is.null(ins_exp)) {
  cat("  Got", nrow(ins_exp), "clumped instruments\n")
  cat("  Has eaf:", "eaf" %in% names(ins_exp), "\n")
  if ("eaf.exposure" %in% names(ins_exp)) cat("  eaf NA:", sum(is.na(ins_exp$eaf.exposure)), "\n")
  cat("  First 3 SNPs:", paste(head(ins_exp$SNP, 3), collapse=", "), "\n")
} else {
  cat("  FAILED. Trying alt approach...\n")
}

# ============================================================
# 2. 获取 AD outcome（含 eaf）
# ============================================================
if (!is.null(ins_exp) && nrow(ins_exp) > 0) {
  cat("\n[2] Extracting AD outcome data with eaf...\n")
  ad_out <- tryCatch({
    extract_outcome_data(
      snps = ins_exp$SNP,
      outcomes = "ieu-b-2"
    )
  }, error = function(e) {
    cat("  extract_outcome_data failed:", conditionMessage(e), "\n")
    NULL
  })
  
  if (!is.null(ad_out)) {
    cat("  Got", nrow(ad_out), "outcome SNPs\n")
    cat("  Has eaf:", "eaf.outcome" %in% names(ad_out), "\n")
    if ("eaf.outcome" %in% names(ad_out)) cat("  eaf NA:", sum(is.na(ad_out$eaf.outcome)), "/", nrow(ad_out),"\n")
  }
}

# ============================================================
# 3. Harmonise
# ============================================================
if (!is.null(ins_exp) && nrow(ins_exp) > 0 && !is.null(ad_out) && nrow(ad_out) > 0) {
  cat("\n[3] Harmonising...\n")
  harm <- tryCatch({
    harmonise_data(ins_exp, ad_out)
  }, error = function(e) {
    cat("  harmonise_data failed:", conditionMessage(e), "\n")
    NULL
  })
  
  if (!is.null(harm)) {
    cat("  Harmonised:", nrow(harm), "SNPs\n")
    cat("  Has eaf.exposure:", "eaf.exposure" %in% names(harm), "\n")
    cat("  Has eaf.outcome:", "eaf.outcome" %in% names(harm), "\n")
    if ("eaf.exposure" %in% names(harm)) cat("  eaf.exposure NA:", sum(is.na(harm$eaf.exposure)), "/", nrow(harm), "\n")
    if ("eaf.outcome" %in% names(harm))  cat("  eaf.outcome NA:",  sum(is.na(harm$eaf.outcome)), "/", nrow(harm), "\n")
  }
} else {
  cat("\n[3] SKIP harmonise - missing data\n")
  harm <- NULL
}

# ============================================================
# 4. Run Steiger
# ============================================================
if (!is.null(harm) && nrow(harm) > 0) {
  eaf_ok <- sum(!is.na(harm$eaf.exposure) & !is.na(harm$eaf.outcome))
  cat("\n[4] Running Steiger (", eaf_ok, "/", nrow(harm), " SNPs with non-NA eaf)...\n", sep="")
  
  if (eaf_ok > 0) {
    harm_clean <- harm[!is.na(harm$eaf.exposure) & !is.na(harm$eaf.outcome), ]
    
    st <- tryCatch({
      steiger(harm_clean)
    }, error = function(e) {
      cat("  steiger() failed:", conditionMessage(e), "\n")
      NULL
    })
    
    if (!is.null(st)) {
      cat("=== STEIGER RESULTS ===\n")
      print(st)
      
      # 保存
      st$exposure_id <- "ukb-b-3957"
      st$outcome_id <- "ieu-b-2"
      st$n_snps <- nrow(harm_clean)
      st$clump_r2 <- 0.1
      saveRDS(st, "results/steiger/G1_steiger_fwd_clumped.rds")
      
      # 文本摘要
      sink("results/steiger/G1_steiger_summary.txt")
      cat("Steiger directionality test\n")
      cat("Date:", as.character(Sys.Date()), "\n")
      cat("Exposure: insomnia (ukb-b-3957)\n")
      cat("Outcome: AD (ieu-b-2, Kunkle 2019)\n")
      cat("Clump: r2=0.1, kb=10000\n")
      cat("N SNPs:", nrow(harm_clean), "\n\n")
      print(st)
      sink()
      
      cat("Steiger results saved to results/steiger/\n")
    }
  } else {
    cat("  No SNPs with non-NA eaf - cannot run Steiger\n")
  }
} else {
  cat("[4] SKIP Steiger - no harmonised data\n")
}

cat("\n[B2] Done.\n")
