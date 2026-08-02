# verify_iv_yield.R — Phase 1 闸门：实测各候选 GWAS 能否提出足量工具变量
# 目的：Sakaue 2021 (ebi-a-GCST90018869) 实测返回 0 IV（NULL 静默失败），
#       其 ncase=1402 异常证实该 GWAS Catalog 条目在 OpenGWAS 不可靠。
#       改测全部 4 个失眠候选 + AD 双源，输出决策用对比表。
# 用法：Rscript verify_iv_yield.R   （需联网）

library(TwoSampleMR)
library(ieugwasr)

cat("TwoSampleMR version:", as.character(packageVersion("TwoSampleMR")), "\n\n")

# ---- 失眠暴露候选（预注册级决策对象）----
ins_candidates <- list(
  "Sakaue 2021 (原选)"       = "ebi-a-GCST90018869",
  "BenElsworth 2018 (UKB)"   = "ukb-b-3957",
  "Mbatchou 2021 (SPA corr)" = "ebi-a-GCST90013934",
  "Hammerschlag 2017"        = "ebi-a-GCST004695"
)

cat("===== INSOMNIA 暴露 IV 产出 =====\n")
for (nm in names(ins_candidates)) {
  id <- ins_candidates[[nm]]
  cat(sprintf("\n--- %s [%s] ---\n", nm, id))
  exp <- tryCatch(
    extract_instruments(outcomes = id, p1 = 5e-8, clump = TRUE, r2 = 0.001, kb = 10000),
    error = function(e) { cat("  ERROR:", conditionMessage(e), "\n"); NULL }
  )
  if (is.null(exp) || nrow(exp) == 0) {
    cat("  RESULT: 0 / NULL（未托管提取 / 无全基因组显著位点）→ 不可用\n")
    next
  }
  cat("  n IVs (clumped):      ", nrow(exp), "\n")
  cat("  non-NA beta.exposure: ", sum(!is.na(exp$beta.exposure)), "\n")
  cat("  non-NA se.exposure:   ", sum(!is.na(exp$se.exposure)), "\n")
  cat("  min pval.exposure:    ", format(min(exp$pval.exposure, na.rm = TRUE), scientific = TRUE), "\n")
  cat("  id.exposure:          ", paste(unique(exp$id.exposure), collapse = " | "), "\n")
}

# ---- AD 结局候选（健全性核查）----
ad_candidates <- list(
  "Bellenguez 2022 (主源)" = "ebi-a-GCST90027158",
  "Kunkle 2019 / IGAP (复制)" = "ieu-b-2"
)

cat("\n\n===== ALZHEIMER 结局 IV 产出（健全性）=====\n")
for (nm in names(ad_candidates)) {
  id <- ad_candidates[[nm]]
  cat(sprintf("\n--- %s [%s] ---\n", nm, id))
  exp <- tryCatch(
    extract_instruments(outcomes = id, p1 = 5e-8, clump = TRUE, r2 = 0.001, kb = 10000),
    error = function(e) { cat("  ERROR:", conditionMessage(e), "\n"); NULL }
  )
  if (is.null(exp) || nrow(exp) == 0) {
    cat("  RESULT: 0 / NULL → 需复核\n")
    next
  }
  cat("  n IVs (clumped):   ", nrow(exp), "\n")
  cat("  min pval.exposure: ", format(min(exp$pval.exposure, na.rm = TRUE), scientific = TRUE), "\n")
}
