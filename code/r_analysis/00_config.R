# =====================================================================
# ---------------------------------------------------------------------
# GWAS ID / AD ID / Sakaue↔Bellenguez UKB /
# UKB-PPP panelGFAP / NfL / , ID
# gwas_ids_resolved.json. ; ID .
# = BenElsworth 2018 ukb-b-3957, n=462,341, European, 42 clumped IVs
# -- Sakaue 2021 ebi-a-GCST90018869 0 IV , ieu-a-1096=, Jansen 2019 1.33M
# AD = Kunkle BW 2019 / IGAP ieu-b-2, ncase=21,982 ukb-b-3957 UKB ->
# AD = Bellenguez C 2022 ebi-a-GCST90027158, ncase=39,106 PMID 35379992
# : = ukb-b-3957 × ADKunkle ieu-b-2; Bellenguez +
# IEU REST API , gwasinfo
# =====================================================================

pkgs <- c("TwoSampleMR", "ieugwasr", "coloc", "msm", "mstate",
          "survival", "dplyr", "readr", "data.table", "ggplot2")
for (p in pkgs) {
  if (!requireNamespace(p, quietly = TRUE)) {
    message(": ", p)
    # Bioconductor: BiocManager::install"coloc"
    # CRAN: install.packagesc"TwoSampleMR","msm","mstate","survival"
  }
}

DIR_ROOT   <- "./output"   # ( docs/historical/; )
DIR_DATA   <- file.path(DIR_ROOT, "data")            #  GWAS / UKB 
DIR_OUT    <- file.path(DIR_ROOT, "results")         # 
DIR_FIG    <- file.path(DIR_ROOT, "figures")
for (d in c(DIR_DATA, DIR_OUT, DIR_FIG)) dir.create(d, showWarnings = FALSE, recursive = TRUE)

# 00b_verify_gwas.R ID; .
RESOLVED <- file.path(DIR_ROOT, "code", "gwas_ids_resolved.json")
# : R locale C/ASCII , file.exists UTF-8 FALSE
# PENDING_VERIFY halt; , , .
GWAS_ID_LOCKED <- list(
  insomnia = "ukb-b-3957",          # BenElsworth 2018  (EUR, n=462,341)
  ad       = "ieu-b-2",             # Kunkle/IGAP 2019 AD( UKB , )
  ad_alt   = "ebi-a-GCST90027158"   # Bellenguez 2022 AD( UKB , +)
)
if (file.exists(RESOLVED)) {
  resolved <- tryCatch(jsonlite::fromJSON(RESOLVED), error = function(e) NULL)
  if (!is.null(resolved) && !is.null(resolved$ad) && resolved$ad != "PENDING_VERIFY") {
    GWAS_ID <- list(
      insomnia = if (is.null(resolved$insomnia)) GWAS_ID_LOCKED$insomnia else resolved$insomnia,
      ad       = resolved$ad,
      ad_alt   = if (is.null(resolved$ad_alt))   GWAS_ID_LOCKED$ad_alt   else resolved$ad_alt
    )
    message("[config]  GWAS ID: insomnia=", GWAS_ID$insomnia, " ad=", GWAS_ID$ad)
  } else {
    GWAS_ID <- GWAS_ID_LOCKED
    message("[config] resolved json .,  ID: ad=", GWAS_ID$ad)
  }
} else {
  GWAS_ID <- GWAS_ID_LOCKED
  message("[config]  gwas_ids_resolved.json,  ID(): ad=", GWAS_ID$ad)
}

THRESH <- list(
  clump_r2       = 0.001,
  clump_kb       = 10000,
  maf_min        = 0.01,
  fstat_min      = 10,       # instrument ( 20)
  coloc_pph4     = 0.80,     # 
  mr_alpha       = 0.05,
  protein_fdr    = 0.05,     # G2 (~2923 )
  msm_alpha      = 0.05
)

COVARS <- c("age", "sex", "education", "depression", "apoe_e4", "hypnotic_use")

set.seed(20260718)

# OpenGWAS SNP , SNP URL .
# BATCH_SIZE SNP, sleep_sec
# , rbind harmonise_data SNP.
BATCH_SIZE <- 20

extract_outcome_data_batched <- function(snps, outcomes,
                                         batch_size = BATCH_SIZE,
                                         sleep_sec = 1, ...) {
  snps <- unique(as.character(snps))
  n <- length(snps)
  if (n == 0) {
    message("[batch]  SNP ,  NULL")
    return(NULL)
  }
  n_batch <- ceiling(n / batch_size)
  message("[batch]  ", n, "  SNP  ", n_batch,
          " ( <=", batch_size, ")")
  pieces <- list()
  for (i in seq_len(n_batch)) {
    lo <- (i - 1) * batch_size + 1
    hi <- min(i * batch_size, n)
    chunk <- snps[lo:hi]
    message("  [batch]  ", i, "/", n_batch, " : ", length(chunk), " SNPs")
    res <- tryCatch(
      extract_outcome_data(snps = chunk, outcomes = outcomes, ...),
      error = function(e) {
        message("  [batch][warn]  ", i, " : ", conditionMessage(e))
        NULL
      })
    if (!is.null(res) && nrow(res) > 0) pieces[[length(pieces) + 1]] <- res
    if (i < n_batch && sleep_sec > 0) Sys.sleep(sleep_sec)
  }
  pieces <- Filter(function(x) !is.null(x) && nrow(x) > 0, pieces)
  if (length(pieces) == 0) {
    message("[batch] .,  NULL")
    return(NULL)
  }
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
      message("[batch][warn] bind_rows ,  base rbind: ", conditionMessage(e))
      do.call(rbind, pieces)
    })
  as.data.frame(out)
}

message("[config] . ",
        if (!file.exists(RESOLVED)) "(GWAS ID  00b )" else "(GWAS ID )")