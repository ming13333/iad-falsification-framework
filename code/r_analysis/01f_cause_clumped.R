#!/usr/bin/env Rscript
# ============================================================
# 01f_cause_clumped.R
# C3: 用 LD-clumped 变异集重跑 CAUSE，验证"未 clump 伪迹"
# ------------------------------------------------------------
# 背景:
#   原 01c (CAUSE) 对 p<1e-3 的 15564 个原始变异直接跑 cause(),
#   前向(失眠→AD) 给出 causal_p=0.004 ("CAUSAL") —— 这是未 LD-clump
#   导致的 LD 结构伪迹 (与 UVMR unclump +0.10 同理)。
# 修复:
#   先对 p<1e-3 变异做 LD-clump (r2=0.01, EUR 面板) 收敛到独立位点,
#   再喂给 cause()。预期: clumped CAUSE 前向不再显著 → 伪迹确认。
# 依赖: cause, loo, data.table, ieugwasr(仅 ld_clump 需联网)
# ============================================================

set.seed(20240721)
options(width=200, scipen=3)

suppressMessages({
  library(data.table)
  library(cause)
  library(loo)
  library(ieugwasr)
})

# ---- monkey-patch cause:::in_sample_elpd_loo (loo >= 2.6.0 兼容, 同 01c) ----
patched_in_sample_elpd_loo <- function(X, fits, variants, nsamps = 500) {
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
    mods$delta_elpd <- NA; mods$se_delta_elpd <- NA
    if (!is.null(names(fits))) {
        mods$model1 <- names(fits)[mods$m1]; mods$model2 <- names(fits)[mods$m2]
    } else { mods$model1 <- mods$m1; mods$model2 <- mods$m2 }
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
    loos <- lapply(lls, function(llmat) {
        if (is.null(dim(llmat))) llmat <- matrix(llmat, ncol = 1)
        if (ncol(llmat) == 1) return(NULL)
        loo(llmat, r_eff = rep(1, ncol(llmat)))
    })
    for (j in seq(nrow(mods))) {
        i1 <- mods$m1[j]; i2 <- mods$m2[j]
        if (is.null(loos[[i1]])) {
            diff <- lls[[i1]] - loos[[i2]]$pointwise[, 1]
            est <- sum(diff); se <- sd(diff) * sqrt(nrow(X))
        } else if (is.null(loos[[i2]])) {
            diff <- loos[[i1]]$pointwise[, 1] - lls[[i2]]
            est <- sum(diff); se <- sd(diff) * sqrt(nrow(X))
        } else {
            comp <- loo_compare(loos[[i1]], loos[[i2]])
            if ("model" %in% colnames(comp)) {
                best_is_model2 <- comp$model[1] == "model2"
                est_raw <- comp[2, "elpd_diff"]; se_val <- comp[2, "se_diff"]
            } else {
                best_is_model2 <- rownames(comp)[1] == "model2"
                est_raw <- comp[2, 1]; se_val <- comp[2, 2]
            }
            if (best_is_model2) { est <- est_raw; se <- se_val } else { est <- -1*est_raw; se <- se_val }
        }
        mods$delta_elpd[j] <- est; mods$se_delta_elpd[j] <- se
    }
    mods$z <- mods$delta_elpd / mods$se_delta_elpd
    mods <- mods[, c("model1", "model2", "delta_elpd", "se_delta_elpd", "z")]
    class(mods) <- c("cause_elpd", "data.frame")
    ret <- list(mods = mods, loos = loos)
    return(ret)
}
assignInNamespace("in_sample_elpd_loo", patched_in_sample_elpd_loo, ns = "cause")
cat("cause:::in_sample_elpd_loo patched.\n\n")

# ---- 路径 ----
DIR_RAW  <- "C:/Temp/iad_g1/data/raw"
DIR_RES  <- "C:/Temp/iad_g1/results"
DIR_LD   <- "C:/Temp/iad_g1/ld_ref/LDscore"

GWAS_FILES <- list(
  "ukb-b-3957"         = file.path(DIR_RAW, "ukb-b-3957/ukb-b-3957.clean.tsv.gz"),
  "ieu-b-2"            = file.path(DIR_RAW, "ieu-b-2/ieu-b-2.clean.tsv.gz"),
  "ebi-a-GCST90027158" = file.path(DIR_RAW, "ebi-a-GCST90027158/GCST90027158_buildGRCh37.dedup.tsv.gz")
)
COMBOS <- list(
  list(exp="ukb-b-3957",         out="ieu-b-2",            label="cause_fwd_clumped"),
  list(exp="ieu-b-2",            out="ukb-b-3957",          label="cause_rev_clumped"),
  list(exp="ukb-b-3957",         out="ebi-a-GCST90027158",  label="cause_rep_fwd_clumped"),
  list(exp="ebi-a-GCST90027158", out="ukb-b-3957",          label="cause_rep_rev_clumped")
)

# ---- CHR+POS -> rsID 映射 (同 01b/01c) ----
rsid_map <- rbindlist(lapply(1:22, function(chr) {
  f <- file.path(DIR_LD, paste0(chr, ".l2.ldscore.gz"))
  if (!file.exists(f)) return(NULL)
  fread(f, select=c("CHR","SNP","BP"))
}))
setnames(rsid_map, c("SNP","BP"), c("rsid","POS"))

load_gwas_for_overlap <- function(gwas_id) {
  f <- GWAS_FILES[[gwas_id]]
  dt <- fread(f)
  if ("BP" %in% names(dt)) setnames(dt, "BP", "POS")
  if (!"n" %in% names(dt) && "n_cases" %in% names(dt) && "n_controls" %in% names(dt)) {
    dt[, n := n_cases + n_controls]
  }
  if (!grepl("^rs", dt$SNP[1])) {
    dt <- merge(dt, rsid_map[, .(CHR, POS, rsid)], by=c("CHR","POS"), all.x=TRUE)
    dt <- dt[!is.na(rsid)]
    dt[, SNP := rsid]; dt[, rsid := NULL]
    if (anyDuplicated(dt$SNP)) { setorder(dt, SNP, p); dt <- dt[!duplicated(SNP)] }
  }
  dt <- dt[grepl("^rs", SNP)]
  if (anyDuplicated(dt$SNP)) { setorder(dt, SNP, p); dt <- dt[!duplicated(SNP)] }
  keep <- intersect(names(dt), c("SNP","CHR","POS","A1","A2","beta","se","p","n"))
  dt[, ..keep]
}

run_cause_clumped <- function(exp_id, out_id, label) {
  cat("\n[", label, "] CAUSE (LD-clumped variants) exp=", exp_id, " out=", out_id, "\n")
  e <- tryCatch(load_gwas_for_overlap(exp_id), error=function(err){cat("读暴露失败:",conditionMessage(err),"\n");NULL})
  o <- tryCatch(load_gwas_for_overlap(out_id), error=function(err){cat("读结局失败:",conditionMessage(err),"\n");NULL})
  if (is.null(e) || is.null(o)) return(NULL)

  e <- data.frame(snp=e$SNP, beta_hat=e$beta, se=e$se, A1=e$A1, A2=e$A2, stringsAsFactors=FALSE)
  o <- data.frame(snp=o$SNP, beta_hat=o$beta, se=o$se, A1=o$A1, A2=o$A2, stringsAsFactors=FALSE)

  X <- tryCatch(cause::gwas_merge(e, o, snp_name_cols=c("snp","snp"),
            beta_hat_cols=c("beta_hat","beta_hat"), se_cols=c("se","se"),
            A1_cols=c("A1","A1"), A2_cols=c("A2","A2"), compute_pvals=TRUE),
        error=function(err){cat("gwas_merge 失败:",conditionMessage(err),"\n");NULL})
  if (is.null(X)) return(NULL)
  cat("  gwas_merge:", nrow(X), "SNPs\n")

  # est_cause_params 用全部/大样本变异估计共享-特异方差混合 (同原 01c, 不 clump)
  varlist <- X$snp
  if (length(varlist) > 500000) varlist <- sample(varlist, 500000)
  params <- tryCatch(cause::est_cause_params(X, variants=varlist),
        error=function(err){cat("est_cause_params 失败:",conditionMessage(err),"\n");NULL})
  if (is.null(params)) return(NULL)

  # ---- 关键修复: p<1e-3 候选变异 -> LD-clump 到独立位点 ----
  raw_vars <- X$snp[which(X$p1 < 1e-3)]
  cat("  p<1e-3 候选变异 (暴露侧):", length(raw_vars), "\n")
  clumped <- tryCatch(
    ieugwasr::ld_clump(dat = data.frame(rsid = raw_vars,
                        pval = X$p1[which(X$p1 < 1e-3)]),
                        clump_r2 = 0.01, clump_p = 1e-3, clump_kb = 500, pop = "EUR"),
    error=function(err){cat("  ld_clump 失败 (退回原始候选):",conditionMessage(err),"\n");NULL})
  if (!is.null(clumped) && nrow(clumped) > 0) {
    variants <- as.character(clumped$rsid)
    cat("  LD-clump 后独立变异:", length(variants), " (压缩比 ",
        round(length(variants)/length(raw_vars),3), ")\n")
  } else {
    variants <- raw_vars
    cat("  ld_clump 不可用, 退回原始候选 (", length(variants), ")\n")
  }

  fit <- tryCatch(cause::cause(X=X, variants=variants, param_ests=params, force=TRUE),
        error=function(err){cat("  cause() 失败:",conditionMessage(err),"\n");NULL})
  if (is.null(fit)) return(NULL)

  summ <- tryCatch(summary(fit), error=function(err) NULL)
  elpd <- tryCatch(fit$elpd, error=function(err) NULL)
  causal_p <- NA_real_
  if (!is.null(summ) && !is.null(summ$p.value)) causal_p <- as.numeric(summ$p.value)
  if (is.na(causal_p) && !is.null(elpd) && "z" %in% names(elpd) && is.finite(elpd$z[1])) {
    causal_p <- 2 * pnorm(-abs(elpd$z[1]))
  }
  decision <- if (is.na(causal_p)) "UNKNOWN"
    else if (causal_p < 0.05) "CAUSAL"
    else "PLEIOTROPY_OR_SHARING"

  res <- data.frame(label=label, exp_id=exp_id, out_id=out_id,
    cause_causal_p=signif(causal_p,4), cause_decision=decision,
    cause_elpd_z=if(!is.null(elpd)&&"z"%in%names(elpd)) signif(as.numeric(elpd$z[1]),3) else NA,
    cause_n_variants_raw=length(raw_vars),
    cause_n_variants_clumped=length(variants),
    stringsAsFactors=FALSE)
  cat("  => causal_p=", signif(causal_p,4), " decision=", decision, "\n")
  res
}

cat("========================================\n")
cat("  C3: CAUSE with LD-clumped variants\n")
cat("========================================\n\n")

results <- list()
for (cmb in COMBOS) {
  r <- run_cause_clumped(cmb$exp, cmb$out, cmb$label)
  if (!is.null(r)) results[[cmb$label]] <- r
}

if (length(results) > 0) {
  df <- do.call(rbind, results)
  out_csv <- file.path(DIR_RES, "G1_cause_clumped.csv")
  write.csv(df, out_csv, row.names=FALSE)
  cat("\n=== C3 CAUSE (clumped) 结果 ===\n")
  print(df)
  cat("\n保存:", out_csv, "\n")

  # 对比旧版 (未 clump)
  old_csv <- file.path(DIR_RES, "G1_cause.csv")
  if (file.exists(old_csv)) {
    old <- fread(old_csv)
    cat("\n=== 对比: 旧版(未clump) vs 新版(clumped) ===\n")
    cmp <- merge(
      old[, .(label, cause_causal_p, cause_decision, cause_n_variants)],
      df[, .(label=gsub("_clumped$","",label), cause_causal_p_clumped=cause_causal_p,
             cause_decision_clumped=cause_decision, n_raw=cause_n_variants_raw,
             n_clumped=cause_n_variants_clumped)],
      by="label", all=TRUE)
    print(cmp)
  }
}
cat("\n[C3] DONE\n")
