# !/usr/bin/env Rscript
# ============================================================
# download_metabolites_fullss.R
# - IEU full-SS : gwas.mrcieu.ac.uk/downloads/{id}/
# /downloads/{id}.tsv.gz 301->opengwas.io->404.
# - extract_instrumentsid, p1= 0<pval<=0.01, GWAS.
# - associationsid, variants= SS, ~64
# MODE="top1pct" : extract_instrumentsp1=0.01, clump=FALSE
# -> top~1% GWAS p<0.01, MR .
# MODE="fullframe" : associationsid, variants=<AD rsID >
# -> AD SNP SS GWAS, C1 lookup.
# : Rscript code/download_metabolites_fullss.R [top1pct|fullframe]
# ============================================================
suppressMessages(library(TwoSampleMR)); suppressMessages(library(data.table))
mode <- if (length(commandArgs(trailingOnly = TRUE)) > 0) commandArgs(trailingOnly = TRUE)[1] else "top1pct"
OUT  <- "./data/raw/metabolites"
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
  ad <- fread("./output/code/ieu-b-2.tsv", select = c("rsid"))
  for (m in mets) {
    a <- tryCatch(associations(id = m, variants = ad$rsid), error = function(e) NULL)
    if (!is.null(a) && nrow(a) > 0) {
      fwrite(a, file.path(OUT, sprintf("%s.fullframe.tsv.gz", m)), sep = "\t")
      cat(sprintf("  %s: %d SNPs (full SS in AD frame)\n", m, nrow(a)))
    } else cat(sprintf("  %s: FAILED\n", m))
  }
  cat("DONE (full SS in AD frame). Heavy: ~1.86e4 API calls per trait.\n")
} else stop("MODE must be 'top1pct' or 'fullframe'")