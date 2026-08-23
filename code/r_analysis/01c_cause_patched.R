# !/usr/bin/env Rscript
# ============================================================
# : loo 2.10.0 S x N draws x obs, cause N x S obs x draws
# : monkey-patch cause:::in_sample_elpd_loo, loo
# : ncol NULL if
# ============================================================

set.seed(20240721)
options(width=200, scipen=3)

suppressMessages({
  library(data.table)
  library(cause)
  library(loo)
})

cat("loo version:", as.character(packageVersion("loo")), "\n")
cat("cause version:", as.character(packageVersion("cause")), "\n\n")

# ============================================================
# Monkey-patch cause:::in_sample_elpd_loo
# ============================================================
patched_in_sample_elpd_loo <- function(X, fits, variants, nsamps = 500) {
    stopifnot(inherits(X, "cause_data"))
    if (!missing(variants)) {
        if (!all(variants %in% X$snp)) {
            stop("Not all `variants` are in data.", call. = FALSE)
        }
        X <- cause:::filter(X, snp %in% variants)
        X <- cause:::new_cause_data(X)
    }
    stopifnot(length(fits) >= 2)
    k <- length(fits)
    for (x in fits) stopifnot(inherits(x, "cause_post"))

    mods <- expand.grid(m1 = 1:k, m2 = 1:k)
    mods <- mods[mods$m1 < mods$m2, ]
    mods$delta_elpd <- NA
    mods$se_delta_elpd <- NA
    if (!is.null(names(fits))) {
        mods$model1 <- names(fits)[mods$m1]
        mods$model2 <- names(fits)[mods$m2]
    } else {
        mods$model1 <- mods$m1
        mods$model2 <- mods$m2
    }

    lls <- lapply(fits, FUN = function(fit) {
        if (is.null(fit$joint_post)) {
            # null model: -> SNP loglik
            llmat <- cause:::loglik_loo(0, 0, 0, fit$rho, fit$mix_grid$S1,
                fit$mix_grid$S2, fit$mix_grid$pi, X$beta_hat_1,
                X$beta_hat_2, X$seb1, X$seb2)
            return(llmat)
        }
        samps <- cause:::samp_from_grid(fit$joint_post, c("q", "gamma", "eta"), nsamps)
        llmat <- t(cause:::loglik_loo(samps$gamma, samps$eta, samps$q,
            fit$rho, fit$mix_grid$S1, fit$mix_grid$S2, fit$mix_grid$pi,
            X$beta_hat_1, X$beta_hat_2, X$seb1, X$seb2))
        return(llmat)
    })

    # 1. -> 1 ncolvector=NULL
    # 2. llmat nsamps x n_obs draws x obs cause t
    # loo 2.10.0 S x N draws x obs
    # r_eff: = ncolllmat = n_obs
    cat("  [patched] Computing LOO (nsamps=", nsamps, ")...\n")
    loos <- lapply(lls, function(llmat) {
        if (is.null(dim(llmat))) {
            llmat <- matrix(llmat, ncol = 1)
        }
        if (ncol(llmat) == 1) return(NULL)
        # llmat: nsamps x n_obs draws x observations - loo 2.10.0
        loo(llmat, r_eff = rep(1, ncol(llmat)))
    })
    cat("  [patched] LOO computation done.\n")

    for (j in seq(nrow(mods))) {
        i1 <- mods$m1[j]
        i2 <- mods$m2[j]
        if (is.null(loos[[i1]])) {
            # null model vs sharing/causal: loglik
            diff <- lls[[i1]] - loos[[i2]]$pointwise[, 1]
            est <- sum(diff)
            se <- sd(diff) * sqrt(nrow(X))
        } else if (is.null(loos[[i2]])) {
            # bug: loos[i2] NULL, [[i2]]
            diff <- loos[[i1]]$pointwise[, 1] - lls[[i2]]
            est <- sum(diff)
            se <- sd(diff) * sqrt(nrow(X))
        } else {
            # ---- : loo >= 2.6.0 loo_compare
            # loo 2.10.0: "model" , elpd_diff/se_diff 2/3
            # loo: elpd_diff , model
            comp <- loo_compare(loos[[i1]], loos[[i2]])
            if ("model" %in% colnames(comp)) {
                best_is_model2 <- comp$model[1] == "model2"
                est_raw <- comp[2, "elpd_diff"]
                se_val <- comp[2, "se_diff"]
            } else {
                best_is_model2 <- rownames(comp)[1] == "model2"
                est_raw <- comp[2, 1]
                se_val <- comp[2, 2]
            }
            if (best_is_model2) {
                est <- est_raw
                se <- se_val
            } else {
                est <- -1 * est_raw
                se <- se_val
            }
        }
        mods$delta_elpd[j] <- est
        mods$se_delta_elpd[j] <- se
    }
    mods$z <- mods$delta_elpd / mods$se_delta_elpd
    mods <- mods[, c("model1", "model2", "delta_elpd", "se_delta_elpd", "z")]
    class(mods) <- c("cause_elpd", "data.frame")
    ret <- list(mods = mods, loos = loos)
    return(ret)
}

cat("Patching cause:::in_sample_elpd_loo for loo >= 2.6.0 compatibility...\n")
assignInNamespace("in_sample_elpd_loo", patched_in_sample_elpd_loo, ns = "cause")
cat("Patch applied successfully.\n\n")

# ============================================================
# ============================================================
DIR_RAW  <- "./output/data/raw"
DIR_RES  <- "./output/results"
DIR_LD   <- "./output/ld_ref/LDscore"
DIR_EXTR <- "./output/data/extracted"

# ---- CHR+POS -> rsID
cat(" CHR+POS -> rsID ...\n")
rsid_map <- rbindlist(lapply(1:22, function(chr) {
  f <- file.path(DIR_LD, paste0(chr, ".l2.ldscore.gz"))
  if (!file.exists(f)) return(NULL)
  fread(f, select=c("CHR","SNP","BP"))
}))
setnames(rsid_map, c("SNP","BP"), c("rsid","POS"))
cat(":", nrow(rsid_map), "SNPs\n")

load_gwas_for_overlap <- function(gwas_id, GWAS_FILES) {
  f <- GWAS_FILES[[gwas_id]]
  dt <- fread(f)
  if ("BP" %in% names(dt)) setnames(dt, "BP", "POS")
  if (!"n" %in% names(dt) && "n_cases" %in% names(dt) && "n_controls" %in% names(dt)) {
    dt[, n := n_cases + n_controls]
    cat("   n : n = n_cases + n_controls\n")
  }
  if (!grepl("^rs", dt$SNP[1])) {
    cat("  SNP  rsID  (", dt$SNP[1], "),  CHR+POS -> rsID ...\n")
    dt <- merge(dt, rsid_map[, .(CHR, POS, rsid)], by=c("CHR","POS"), all.x=TRUE)
    n_mapped <- sum(!is.na(dt$rsid))
    cat("  :", n_mapped, "/", nrow(dt), "SNPs\n")
    dt <- dt[!is.na(rsid)]
    dt[, SNP := rsid]
    dt[, rsid := NULL]
    if (anyDuplicated(dt$SNP)) {
      n_before <- nrow(dt)
      setorder(dt, SNP, p)
      dt <- dt[!duplicated(SNP)]
      cat("  :", n_before, "->", nrow(dt), "\n")
    }
  }
  dt <- dt[grepl("^rs", SNP)]
  if (anyDuplicated(dt$SNP)) { setorder(dt, SNP, p); dt <- dt[!duplicated(SNP)] }
  keep <- intersect(names(dt), c("SNP","CHR","POS","A1","A2","beta","se","p","n"))
  dt <- dt[, ..keep]
  return(dt)
}

GWAS_FILES <- list(
  "ukb-b-3957"         = file.path(DIR_RAW, "ukb-b-3957/ukb-b-3957.clean.tsv.gz"),
  "ieu-b-2"            = file.path(DIR_RAW, "ieu-b-2/ieu-b-2.clean.tsv.gz"),
  "ebi-a-GCST90027158" = file.path(DIR_RAW, "ebi-a-GCST90027158/GCST90027158_buildGRCh37.dedup.tsv.gz")
)

COMBOS <- list(
  list(exp="ukb-b-3957",         out="ieu-b-2",            label="cause_fwd"),
  list(exp="ieu-b-2",            out="ukb-b-3957",          label="cause_rev"),
  list(exp="ukb-b-3957",         out="ebi-a-GCST90027158",  label="cause_rep_fwd"),
  list(exp="ebi-a-GCST90027158", out="ukb-b-3957",          label="cause_rep_rev")
)

# ============================================================
# ============================================================
run_cause_one <- function(exp_id, out_id, label) {
  cat("\n[", label, "] CAUSE  (exp=", exp_id, ", out=", out_id, ")...\n")

  e <- tryCatch(load_gwas_for_overlap(exp_id, GWAS_FILES),
    error=function(err) { cat("[",label,"] :", conditionMessage(err), "\n"); NULL })
  o <- tryCatch(load_gwas_for_overlap(out_id, GWAS_FILES),
    error=function(err) { cat("[",label,"] :", conditionMessage(err), "\n"); NULL })
  if (is.null(e) || is.null(o)) return(NULL)

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
    error=function(err) { cat("[",label,"] gwas_merge :", conditionMessage(err), "\n"); NULL }
  )
  if (is.null(X)) return(NULL)
  cat("[", label, "] gwas_merge :", nrow(X), "SNPs\n")

  # 2 est_cause_params
  varlist <- tryCatch({
    s <- X$snp
    ns <- if (length(s) > 500000) 500000 else length(s)
    if (length(s) > ns) sample(s, ns) else s
  }, error=function(err) NULL)
  params <- tryCatch(
    cause::est_cause_params(X, variants=varlist),
    error=function(err) { cat("[",label,"] est_cause_params :", conditionMessage(err), "\n"); NULL }
  )
  if (is.null(params)) return(NULL)
  cat("[", label, "] est_cause_params \n")

  variants <- tryCatch({
    if (!is.null(X$p1)) {
      v <- X$snp[which(X$p1 < 1e-3)]
      cat("[", label, "] p<1e-3 :", length(v), "\n")
      if (length(v) > 50000) { v <- sample(v, 50000); cat("[", label, "]  50k\n") }
      v
    } else {
      cat("[", label, "]  p1 ,  500k \n")
      varlist
    }
  }, error=function(err) {
    cat("[", label, "] :", conditionMessage(err), "\n")
    varlist
  })
  cat("[", label, "] :", length(variants), "\n")

  fit <- tryCatch(
    cause::cause(X=X, variants=variants, param_ests=params, force=TRUE),
    error=function(err) { cat("[",label,"] cause() :", conditionMessage(err), "\n"); NULL }
  )
  if (is.null(fit)) return(NULL)

  summ <- tryCatch(summary(fit), error=function(err) NULL)
  elpd <- tryCatch(fit$elpd, error=function(err) NULL)
  causal_p <- NA_real_
  if (!is.null(summ) && !is.null(summ$p.value)) causal_p <- as.numeric(summ$p.value)
  if (is.na(causal_p) && !is.null(elpd) && "z" %in% names(elpd) && is.finite(elpd$z[1])) {
    causal_p <- 2 * pnorm(-abs(elpd$z[1]))
  }
  decision <- if (is.na(causal_p)) {
    "UNKNOWN"
  } else if (causal_p < 0.05) {
    "CAUSAL"
  } else {
    "PLEIOTROPY_OR_SHARING"
  }

  res <- data.frame(
    label=label, exp_id=exp_id, out_id=out_id,
    cause_causal_p=causal_p,
    cause_decision=decision,
    cause_elpd_z=if(!is.null(elpd)&&"z"%in%names(elpd)) as.numeric(elpd$z[1]) else NA,
    cause_n_variants=length(variants),
    stringsAsFactors=FALSE
  )
  cat("[", label, "] CAUSE : causal_p=", signif(causal_p,3),
      " decision=", decision, "\n")
  return(res)
}

# ============================================================
# ============================================================
cat("\n========================================\n")
cat("  CAUSE  (loo )\n")
cat("========================================\n\n")

cause_results <- list()
for (cmb in COMBOS) {
  r <- run_cause_one(cmb$exp, cmb$out, cmb$label)
  if (!is.null(r)) cause_results[[cmb$label]] <- r
}

if (length(cause_results) > 0) {
  cause_df <- do.call(rbind, cause_results)
  write.csv(cause_df, file.path(DIR_RES, "G1_cause.csv"), row.names=FALSE)
  cat("\n=== CAUSE :", file.path(DIR_RES, "G1_cause.csv"), "===\n")
  print(cause_df)
} else {
  cat("\n=== CAUSE:  ===\n")
  cause_df <- NULL
}

rds_path <- file.path(DIR_RES, "G1_bidirectional.rds")
if (file.exists(rds_path)) {
  dat <- readRDS(rds_path)

  mrlap_csv <- file.path(DIR_RES, "G1_mrlap.csv")
  if (file.exists(mrlap_csv)) {
    mrlap_df <- fread(mrlap_csv)
    for (lbl in c("mrlap_fwd","mrlap_rev","mrlap_rep_fwd","mrlap_rep_rev")) {
      row <- mrlap_df[label == lbl]
      if (nrow(row) > 0) {
        dat[[lbl]] <- as.data.frame(row)
        cat("MRlap", lbl, "-> RDS \n")
      }
    }
  }

  for (lbl in c("cause_fwd","cause_rev","cause_rep_fwd","cause_rep_rev")) {
    if (!is.null(cause_results[[lbl]])) {
      dat[[lbl]] <- cause_results[[lbl]]
      cat("CAUSE", lbl, "-> RDS \n")
    }
  }

  dat$overlap_correction_run <- TRUE
  saveRDS(dat, rds_path)
  cat("\n=== G1_bidirectional.rds  (overlap_correction_run=TRUE) ===\n")
}

cat("\n========================================\n")
cat("  CAUSE \n")
cat("========================================\n")