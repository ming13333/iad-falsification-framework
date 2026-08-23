# !/usr/bin/env Rscript
# ============================================================
# MRlap + CAUSE MR/coloc
# : MRlap, cause, data.table
# : clean GWAS + LD
# : results/G1_mrlap.csv, results/G1_cause.csv, G1_bidirectional.rds
# ============================================================

set.seed(20240721)
options(width=200, scipen=3)

suppressMessages({
  library(data.table)
  library(MRlap)
  library(cause)
})

DIR_RAW  <- "./output/data/raw"
DIR_RES  <- "./output/results"
DIR_LD   <- "./output/ld_ref/LDscore"
FILE_HM3 <- "./output/ld_ref/hm3_with_alleles.txt"
DIR_EXTR <- "./output/data/extracted"

dir.create(DIR_RES, showWarnings=FALSE, recursive=TRUE)

# ---- CHR+POS -> rsID LD
# ukb-b-3957 UKB ID CHR_POS_A1_A2, MRlap/CAUSE rsID LD
message(" CHR+POS -> rsID  (LD )...")
rsid_map <- rbindlist(lapply(1:22, function(chr) {
  f <- file.path(DIR_LD, paste0(chr, ".l2.ldscore.gz"))
  if (!file.exists(f)) return(NULL)
  fread(f, select=c("CHR","SNP","BP"))
}))
setnames(rsid_map, c("SNP","BP"), c("rsid","POS"))
setkey(rsid_map, CHR, POS)
message(": ", nrow(rsid_map), " SNPs (HapMap3)")

# ---- : GWAS SNP rsID + n
load_gwas_for_overlap <- function(gwas_id) {
  f <- GWAS_FILES[[gwas_id]]
  dt <- fread(f)
  if ("BP" %in% names(dt)) setnames(dt, "BP", "POS")
  # n Bellenguez n_cases/n_controls, n
  if (!"n" %in% names(dt) && "n_cases" %in% names(dt) && "n_controls" %in% names(dt)) {
    dt[, n := n_cases + n_controls]
    message("   n : n = n_cases + n_controls")
  }
  # merge setkey+update join, key MRlap data.table
  if (!grepl("^rs", dt$SNP[1])) {
    message("  SNP  rsID  (", dt$SNP[1], "),  CHR+POS -> rsID ...")
    dt <- merge(dt, rsid_map[, .(CHR, POS, rsid)], by=c("CHR","POS"), all.x=TRUE)
    n_mapped <- sum(!is.na(dt$rsid))
    message("  : ", n_mapped, " / ", nrow(dt), " SNPs  rsID")
    dt <- dt[!is.na(rsid)]
    dt[, SNP := rsid]
    dt[, rsid := NULL]
    if (anyDuplicated(dt$SNP)) {
      n_before <- nrow(dt)
      setorder(dt, SNP, p)
      dt <- dt[!duplicated(SNP)]
      message("  : ", n_before, " -> ", nrow(dt), " ( ", n_before - nrow(dt), "  rsID)")
    }
  }
  dt <- dt[grepl("^rs", SNP)]
  if (anyDuplicated(dt$SNP)) {
    setorder(dt, SNP, p)
    dt <- dt[!duplicated(SNP)]
  }
  # MRlap/CAUSE , LD
  keep <- intersect(names(dt), c("SNP","CHR","POS","A1","A2","beta","se","p","n"))
  dt <- dt[, ..keep]
  return(dt)
}

GWAS_FILES <- list(
  "ukb-b-3957"           = file.path(DIR_RAW, "ukb-b-3957/ukb-b-3957.clean.tsv.gz"),
  "ieu-b-2"              = file.path(DIR_RAW, "ieu-b-2/ieu-b-2.clean.tsv.gz"),
  "ebi-a-GCST90027158"   = file.path(DIR_RAW, "ebi-a-GCST90027158/GCST90027158_buildGRCh37.dedup.tsv.gz")
)

# ---- 4 : exposure_id, outcome_id, label, need_overlap_corr
COMBOS <- list(
  list(exp="ukb-b-3957", out="ieu-b-2",            label="mrlap_fwd",      cause_label="cause_fwd"),
  list(exp="ieu-b-2",    out="ukb-b-3957",          label="mrlap_rev",      cause_label="cause_rev"),
  list(exp="ukb-b-3957", out="ebi-a-GCST90027158",  label="mrlap_rep_fwd",  cause_label="cause_rep_fwd"),
  list(exp="ebi-a-GCST90027158", out="ukb-b-3957",  label="mrlap_rep_rev",  cause_label="cause_rep_rev")
)

# ============================================================
# ============================================================
run_mrlap_one <- function(exp_id, out_id, label) {
  exp_file <- GWAS_FILES[[exp_id]]
  out_file <- GWAS_FILES[[out_id]]
  if (!file.exists(exp_file) || !file.exists(out_file)) {
    message("[", label, "] GWAS , . ")
    return(NULL)
  }
  message("\n[", label, "] MRlap::MRlap  (exp=", exp_id, ", out=", out_id, ")...")
  message("[", label, "] ld=", DIR_LD, " hm3=", FILE_HM3)

  # MRlap 0.0.3.3 POS BP; data.frame rsID
  exp_df <- tryCatch(load_gwas_for_overlap(exp_id), error=function(e) { message("[",label,"] : ",conditionMessage(e)); NULL })
  out_df <- tryCatch(load_gwas_for_overlap(out_id), error=function(e) { message("[",label,"] : ",conditionMessage(e)); NULL })
  if (is.null(exp_df) || is.null(out_df)) return(NULL)
  message("[", label, "]  SNPs(rsID): ", nrow(exp_df), ",  SNPs(rsID): ", nrow(out_df))

  fit <- tryCatch(
    MRlap::MRlap(
      exposure      = exp_df,
      exposure_name = exp_id,
      outcome       = out_df,
      outcome_name  = out_id,
      ld  = DIR_LD,
      hm3 = FILE_HM3
    ),
    error = function(e) {
      message("[", label, "] MRlap : ", conditionMessage(e))
      NULL
    }
  )
  if (is.null(fit)) return(NULL)

  mc <- fit$MRcorrection
  if (is.null(mc)) {
    message("[", label, "] MRlap ( $MRcorrection), . ")
    return(NULL)
  }

  b_corr  <- as.numeric(mc$corrected_effect)[1]
  se_corr <- as.numeric(mc$corrected_effect_se)[1]
  p_corr  <- as.numeric(mc$corrected_effect_p)[1]
  b_obs   <- as.numeric(mc$observed_effect)[1]
  se_obs  <- as.numeric(mc$observed_effect_se)[1]
  p_obs   <- as.numeric(mc$observed_effect_p)[1]
  p_diff  <- as.numeric(mc$p_difference)[1]
  n_ivs   <- as.integer(mc$m_IVs)[1]
  ci_l <- if (is.finite(b_corr) && is.finite(se_corr)) b_corr - 1.96 * se_corr else NA
  ci_u <- if (is.finite(b_corr) && is.finite(se_corr)) b_corr + 1.96 * se_corr else NA

  res <- data.frame(
    label=label, exp_id=exp_id, out_id=out_id,
    mrlap_corrected_beta=b_corr, mrlap_corrected_se=se_corr,
    mrlap_corrected_p=p_corr,
    mrlap_corrected_ci_lower=ci_l, mrlap_corrected_ci_upper=ci_u,
    mrlap_observed_beta=b_obs, mrlap_observed_se=se_obs, mrlap_observed_p=p_obs,
    mrlap_p_difference=p_diff, n_ivs=n_ivs,
    stringsAsFactors=FALSE
  )
  message("[", label, "] MRlap : corrected_beta=", round(b_corr,5),
          " (p=", signif(p_corr,3), "), observed_beta=", round(b_obs,5),
          " (p=", signif(p_obs,3), "), p_diff=", signif(p_diff,3))
  return(res)
}

# ============================================================
# ============================================================
run_cause_one <- function(exp_id, out_id, label) {
  exp_file <- GWAS_FILES[[exp_id]]
  out_file <- GWAS_FILES[[out_id]]
  if (!file.exists(exp_file) || !file.exists(out_file)) {
    message("[", label, "] GWAS , . ")
    return(NULL)
  }

  message("\n[", label, "] CAUSE  (exp=", exp_id, ", out=", out_id, ")...")

  # GWAS rsID , load_gwas_for_overlap
  e <- tryCatch(load_gwas_for_overlap(exp_id), error=function(e) { message("[",label,"] : ",conditionMessage(e)); NULL })
  o <- tryCatch(load_gwas_for_overlap(out_id), error=function(e) { message("[",label,"] : ",conditionMessage(e)); NULL })
  if (is.null(e) || is.null(o)) return(NULL)

  # cause::gwas_merge
  e <- data.frame(snp=e$SNP, beta_hat=e$beta, se=e$se, A1=e$A1, A2=e$A2, stringsAsFactors=FALSE)
  o <- data.frame(snp=o$SNP, beta_hat=o$beta, se=o$se, A1=o$A1, A2=o$A2, stringsAsFactors=FALSE)

  X <- tryCatch(
    cause::gwas_merge(e, o,
                      snp_name_cols=c("snp","snp"),
                      beta_hat_cols=c("beta_hat","beta_hat"),
                      se_cols=c("se","se"),
                      A1_cols=c("A1","A1"),
                      A2_cols=c("A2","A2"),
                      compute_pvals=TRUE),
    error=function(e2) { message("[",label,"] gwas_merge : ",conditionMessage(e2)); NULL }
  )
  if (is.null(X)) return(NULL)
  message("[", label, "] gwas_merge : ", nrow(X), " SNPs")

  # 2 est_cause_params : variants, varlist
  varlist <- tryCatch({
    s <- X$snp
    ns <- if (length(s) > 500000) 500000 else length(s)
    if (length(s) > ns) sample(s, ns) else s
  }, error=function(e2) NULL)
  params <- tryCatch(
    cause::est_cause_params(X, variants=varlist),
    error=function(e2) { message("[",label,"] est_cause_params : ",conditionMessage(e2)); NULL }
  )
  if (is.null(params)) return(NULL)
  message("[", label, "] est_cause_params ")

  variants <- tryCatch({
    if (!is.null(X$p1)) {
      v <- X$snp[which(X$p1 < 1e-3)]
      message("[", label, "] p<1e-3 : ", length(v))
      if (length(v) > 50000) {
        v <- sample(v, 50000)
        message("[", label, "]  50k")
      }
      v
    } else {
      message("[", label, "]  p1 ,  500k ")
      varlist
    }
  }, error=function(e2) {
    message("[", label, "] ,  500k : ", conditionMessage(e2))
    varlist
  })
  message("[", label, "] : ", length(variants))

  fit <- tryCatch(
    cause::cause(X=X, variants=variants, param_ests=params, force=TRUE),
    error=function(e2) { message("[",label,"] cause() : ",conditionMessage(e2)); NULL }
  )
  if (is.null(fit)) return(NULL)

  summ <- tryCatch(summary(fit), error=function(e2) NULL)
  elpd <- tryCatch(fit$elpd, error=function(e2) NULL)
  causal_p <- NA_real_
  if (!is.null(summ) && !is.null(summ$p.value)) causal_p <- as.numeric(summ$p.value)
  if (is.na(causal_p) && !is.null(elpd) && "z" %in% names(elpd) && is.finite(elpd$z[1])) {
    causal_p <- 2 * pnorm(-abs(elpd$z[1]))
  }
  decision <- if (is.na(causal_p)) {
    "UNKNOWN"
  } else if (causal_p < 0.05) {
    "CAUSAL (.)"
  } else {
    "PLEIOTROPY_OR_SHARING (.)"
  }

  res <- data.frame(
    label=label, exp_id=exp_id, out_id=out_id,
    cause_causal_p=causal_p,
    cause_decision=decision,
    cause_elpd_z=if(!is.null(elpd)&&"z"%in%names(elpd)) as.numeric(elpd$z[1]) else NA,
    cause_n_variants=length(variants),
    stringsAsFactors=FALSE
  )
  message("[", label, "] CAUSE : causal_p=", signif(causal_p,3),
          " decision=", decision)
  return(res)
}

# ============================================================
# ============================================================
message("\n========================================")
message("  MRlap + CAUSE ")
message("========================================\n")

mrlap_results <- list()
for (cmb in COMBOS) {
  r <- run_mrlap_one(cmb$exp, cmb$out, cmb$label)
  if (!is.null(r)) mrlap_results[[cmb$label]] <- r
}
if (length(mrlap_results) > 0) {
  mrlap_df <- do.call(rbind, mrlap_results)
  write.csv(mrlap_df, file.path(DIR_RES, "G1_mrlap.csv"), row.names=FALSE)
  message("\n=== MRlap : ", file.path(DIR_RES, "G1_mrlap.csv"), " ===")
  print(mrlap_df)
} else {
  message("\n=== MRlap:  ===")
  mrlap_df <- NULL
}

cause_results <- list()
for (cmb in COMBOS) {
  r <- run_cause_one(cmb$exp, cmb$out, cmb$cause_label)
  if (!is.null(r)) cause_results[[cmb$cause_label]] <- r
}
if (length(cause_results) > 0) {
  cause_df <- do.call(rbind, cause_results)
  write.csv(cause_df, file.path(DIR_RES, "G1_cause.csv"), row.names=FALSE)
  message("\n=== CAUSE : ", file.path(DIR_RES, "G1_cause.csv"), " ===")
  print(cause_df)
} else {
  message("\n=== CAUSE:  ===")
  cause_df <- NULL
}

rds_path <- file.path(DIR_RES, "G1_bidirectional.rds")
if (file.exists(rds_path)) {
  dat <- readRDS(rds_path)
  dat$mrlap_fwd      <- if(!is.null(mrlap_results[["mrlap_fwd"]]))      mrlap_results[["mrlap_fwd"]]      else dat$mrlap_fwd
  dat$mrlap_rev      <- if(!is.null(mrlap_results[["mrlap_rev"]]))      mrlap_results[["mrlap_rev"]]      else dat$mrlap_rev
  dat$mrlap_rep_fwd  <- if(!is.null(mrlap_results[["mrlap_rep_fwd"]]))  mrlap_results[["mrlap_rep_fwd"]]  else dat$mrlap_rep_fwd
  dat$mrlap_rep_rev  <- if(!is.null(mrlap_results[["mrlap_rep_rev"]]))  mrlap_results[["mrlap_rep_rev"]]  else dat$mrlap_rep_rev
  dat$cause_fwd      <- if(!is.null(cause_results[["cause_fwd"]]))      cause_results[["cause_fwd"]]      else dat$cause_fwd
  dat$cause_rev      <- if(!is.null(cause_results[["cause_rev"]]))      cause_results[["cause_rev"]]      else dat$cause_rev
  dat$cause_rep_fwd  <- if(!is.null(cause_results[["cause_rep_fwd"]]))  cause_results[["cause_rep_fwd"]]  else dat$cause_rep_fwd
  dat$cause_rep_rev  <- if(!is.null(cause_results[["cause_rep_rev"]]))  cause_results[["cause_rep_rev"]]  else dat$cause_rep_rev
  dat$overlap_correction_run <- !is.null(mrlap_df) || !is.null(cause_df)
  saveRDS(dat, rds_path)
  message("\n=== G1_bidirectional.rds  (overlap_correction_run=", dat$overlap_correction_run, ") ===")
}

message("\n========================================")
message("  ")
message("========================================\n")