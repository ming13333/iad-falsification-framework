# !/usr/bin/env Rscript
# ============================================================
# 01e_cause_fwd_ns1000.R - G1
# CAUSE->AD, IEU , p=0.004, nsamps=1000 500
# 01c patch listmods=mods, loos=loos .
# G1_cause_fwd_ns1000.rds patch live RDS.
# : 01e patched res , loos
# CAUSE withelpd, loos -> object 'loos' not found .
# ============================================================
set.seed(20240721)
options(width = 200, scipen = 3)
suppressMessages({ library(data.table); library(cause); library(loo) })

cat("loo version:", as.character(packageVersion("loo")), "\n")
cat("cause version:", as.character(packageVersion("cause")), "\n\n")

# ---- ----
DIR_RAW  <- "./output/data/raw"
DIR_RES  <- "./output/results"
DIR_LD   <- "./output/ld_ref/LDscore"
DIR_EXTR <- "./output/data/extracted"
NSAMPS   <- 1000   # * ( 500)

# ---- CHR+POS -> rsID
cat(" CHR+POS -> rsID ...\n")
rsid_map <- rbindlist(lapply(1:22, function(chr) {
  f <- file.path(DIR_LD, paste0(chr, ".l2.ldscore.gz"))
  if (!file.exists(f)) return(NULL)
  fread(f, select = c("CHR", "SNP", "BP"))
}))
setnames(rsid_map, c("SNP", "BP"), c("rsid", "POS"))
cat(":", nrow(rsid_map), "SNPs\n")

# ---- load_gwas_for_overlap 01c, M3/M5
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
    dt <- merge(dt, rsid_map[, .(CHR, POS, rsid)], by = c("CHR", "POS"), all.x = TRUE)
    n_mapped <- sum(!is.na(dt$rsid))
    cat("  :", n_mapped, "/", nrow(dt), "SNPs\n")
    dt <- dt[!is.na(rsid)]
    dt[, SNP := rsid]; dt[, rsid := NULL]
    if (anyDuplicated(dt$SNP)) { setorder(dt, SNP, p); dt <- dt[!duplicated(SNP)] }
  }
  dt <- dt[grepl("^rs", SNP)]
  if (anyDuplicated(dt$SNP)) { setorder(dt, SNP, p); dt <- dt[!duplicated(SNP)] }
  keep <- intersect(names(dt), c("SNP", "CHR", "POS", "A1", "A2", "beta", "se", "p", "n"))
  dt <- dt[, ..keep]
  return(dt)
}

GWAS_FILES <- list(
  "ukb-b-3957"         = file.path(DIR_RAW, "ukb-b-3957/ukb-b-3957.clean.tsv.gz"),
  "ieu-b-2"            = file.path(DIR_RAW, "ieu-b-2/ieu-b-2.clean.tsv.gz"),
  "ebi-a-GCST90027158" = file.path(DIR_RAW, "ebi-a-GCST90027158/GCST90027158_buildGRCh37.dedup.tsv.gz")
)

# ---- patched_in_sample_elpd_loo 01c , nsamps=1000
# : ret <- listmods=mods, loos=loos , CAUSE
# withelpd, loos object 'loos' not found.
patched_in_sample_elpd_loo <- function(X, fits, variants, nsamps = NSAMPS) {
    stopifnot(inherits(X, "cause_data"))
    if (!missing(variants)) {
        if (!all(variants %in% X$snp)) stop("Not all `variants` are in data.", call. = FALSE)
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

    cat("  [patched] Computing LOO (nsamps=", nsamps, ")...\n")
    loos <- lapply(lls, function(llmat) {
        if (is.null(dim(llmat))) {
            llmat <- matrix(llmat, ncol = 1)
        }
        if (ncol(llmat) == 1) return(NULL)
        loo(llmat, r_eff = rep(1, ncol(llmat)))
    })
    cat("  [patched] LOO computation done.\n")

    for (j in seq(nrow(mods))) {
        i1 <- mods$m1[j]
        i2 <- mods$m2[j]
        if (is.null(loos[[i1]])) {
            diff <- lls[[i1]] - loos[[i2]]$pointwise[, 1]
            est <- sum(diff)
            se <- sd(diff) * sqrt(nrow(X))
        } else if (is.null(loos[[i2]])) {
            diff <- loos[[i1]]$pointwise[, 1] - lls[[i2]]
            est <- sum(diff)
            se <- sd(diff) * sqrt(nrow(X))
        } else {
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

cat("Patching cause:::in_sample_elpd_loo for loo >= 2.6.0 compatibility (01c verified, nsamps=", NSAMPS, ")...\n")
assignInNamespace("in_sample_elpd_loo", patched_in_sample_elpd_loo, ns = "cause")
cat("Patch applied.\n\n")

# ---- : ukb-b-3957 -> ADieu-b-2
exp_id <- "ukb-b-3957"; out_id <- "ieu-b-2"; label <- "cause_fwd_ns1000"
cat("\n[", label, "] CAUSE  (exp=", exp_id, ", out=", out_id, ", nsamps=", NSAMPS, ")...\n")

e <- load_gwas_for_overlap(exp_id, GWAS_FILES)
o <- load_gwas_for_overlap(out_id, GWAS_FILES)
cat("[", label, "]  SNPs:", nrow(e), ";  SNPs:", nrow(o), "\n")
e <- data.frame(snp = e$SNP, beta_hat = e$beta, se = e$se, A1 = e$A1, A2 = e$A2, stringsAsFactors = FALSE)
o <- data.frame(snp = o$SNP, beta_hat = o$beta, se = o$se, A1 = o$A1, A2 = o$A2, stringsAsFactors = FALSE)

X <- cause::gwas_merge(e, o, snp_name_cols = c("snp", "snp"), beta_hat_cols = c("beta_hat", "beta_hat"),
                       se_cols = c("se", "se"), A1_cols = c("A1", "A1"), A2_cols = c("A2", "A2"),
                       compute_pvals = TRUE)
cat("[", label, "] gwas_merge :", nrow(X), "SNPs\n")

varlist <- { s <- X$snp; ns <- if (length(s) > 500000) 500000 else length(s); if (length(s) > ns) sample(s, ns) else s }
params <- cause::est_cause_params(X, variants = varlist)
cat("[", label, "] est_cause_params ; nsamps  =", NSAMPS, "\n")

variants <- X$snp[which(X$p1 < 1e-3)]
cat("[", label, "] p<1e-3 :", length(variants), "\n")
if (length(variants) > 50000) { variants <- sample(variants, 50000); cat("   50k\n") }

fit <- cause::cause(X = X, variants = variants, param_ests = params, force = TRUE)
cat("[", label, "] cause() \n")

summ <- summary(fit)
elpd <- fit$elpd
causal_p <- NA_real_
if (!is.null(summ) && !is.null(summ$p.value)) causal_p <- as.numeric(summ$p.value)
if (is.na(causal_p) && !is.null(elpd) && "z" %in% names(elpd) && is.finite(elpd$z[1]))
  causal_p <- 2 * pnorm(-abs(elpd$z[1]))
decision <- if (is.na(causal_p)) {
  "UNKNOWN"
} else if (causal_p < 0.05) {
  "CAUSAL"
} else {
  "PLEIOTROPY_OR_SHARING"
}
cat("\n========== RESULT (nsamps=", NSAMPS, ") ==========\n")
cat("causal_p =", if (is.na(causal_p)) "<NA>" else signif(causal_p, 4), "\n")
cat("decision =", decision, "\n")
cat("n_snp_used =", length(variants), "\n")

# ---- + patch live RDS
out_obj <- list(label = label, exp_id = exp_id, out_id = out_id, nsamps = NSAMPS,
                causal_p = causal_p, decision = decision, n_snp_used = length(variants),
                fit = fit, params = params)
saveRDS(out_obj, file.path(DIR_RES, "G1_cause_fwd_ns1000.rds"))
cat(":", file.path(DIR_RES, "G1_cause_fwd_ns1000.rds"), "\n")

RDS <- file.path(DIR_RES, "G1_bidirectional.rds")
dat <- readRDS(RDS)
dat$cause_fwd_ns1000 <- out_obj
saveRDS(dat, RDS)
cat(" patch live RDS: cause_fwd_ns1000  (causal_p=", signif(causal_p, 4), ")\n")
cat("[01e] . \n")