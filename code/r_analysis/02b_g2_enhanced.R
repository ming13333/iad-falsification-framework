# =====================================================================
# ---------------------------------------------------------------------
# 1. MR IVW, MR-Egger, weighted median, weighted mode
# 2. Cochran's Q via mr_heterogeneity
# 3. MR-Egger intercept via mr_pleiotropy_test
# 5. Steiger directionality_test, eaf
# 6. F + Bootstrap CI indirect effect
# - Step1 insomnia -> protein: 42 IV ->
# - Step2 protein -> AD: CRP=3 IV / IL-6=2 IV -> Egger/
# - NfL/GFAP IV , UKB-PPP
# VPN IEU REST
# =====================================================================
suppressMessages({
  library(TwoSampleMR); library(ieugwasr); library(coloc); library(dplyr)
})

GWAS_ID <- list(insomnia = "ukb-b-3957", ad = "ieu-b-2")
THRESH  <- list(clump_r2 = 0.001, clump_kb = 10000, protein_fdr = 0.05, n_boot = 5000)
AD_N    <- 63860
G2_OUT  <- "./output/results/G2_enhanced"
dir.create(G2_OUT, showWarnings = FALSE, recursive = TRUE)
PROT_INDEX <- "./output/proteins/g2_index.csv"

logmsg <- function(...) message("[G2+] ", ..., " (", format(Sys.time(), "%H:%M:%S"), ")")

## ---- ----
if (!file.exists(PROT_INDEX)) stop("[G2+] : ", PROT_INDEX)
protein_map <- read.csv(PROT_INDEX, stringsAsFactors = FALSE, fileEncoding = "UTF-8-BOM")
if (!"ieu_id" %in% names(protein_map)) stop("[G2+]  ieu_id ")
if (!"protein_id" %in% names(protein_map)) stop("[G2+]  protein_id")
if (!"olink_target" %in% names(protein_map)) protein_map$olink_target <- protein_map$protein_id
if (!"n_samples" %in% names(protein_map)) { protein_map$n_samples <- 3301; warning(" n_samples,  3301") }
protein_map$source <- "ieu"; protein_map$path <- protein_map$ieu_id
logmsg(": ", nrow(protein_map), "  (", paste(protein_map$olink_target, collapse=", "), ")")

BATCH_SIZE <- 20
extract_outcome_data_batched <- function(snps, outcomes, batch_size=BATCH_SIZE, sleep_sec=1, ...) {
  snps <- unique(as.character(snps)); n <- length(snps)
  if (n == 0) return(NULL)
  nb <- ceiling(n / batch_size); pieces <- list()
  for (i in seq_len(nb)) {
    lo <- (i-1)*batch_size + 1; hi <- min(i*batch_size, n); chunk <- snps[lo:hi]
    res <- tryCatch(extract_outcome_data(snps=chunk, outcomes=outcomes, ...),
                    error=function(e) { message("  [batch] err: ", conditionMessage(e)); NULL })
    if (!is.null(res) && nrow(res) > 0) pieces[[length(pieces)+1]] <- res
    if (i < nb && sleep_sec > 0) Sys.sleep(sleep_sec)
  }
  pieces <- Filter(function(x) !is.null(x) && nrow(x) > 0, pieces)
  if (length(pieces) == 0) return(NULL)
  dplyr::bind_rows(pieces)
}

get_protein_instruments <- function(prow, p1=5e-8) {
  d <- tryCatch(extract_instruments(prow$path, p1=p1, r2=THRESH$clump_r2, kb=THRESH$clump_kb),
                error=function(e) { message("[G2+] ieu_exp ", prow$protein_id, " err: ", conditionMessage(e)); NULL })
  if (is.null(d) || nrow(d) == 0) return(NULL)
  d$outcome <- prow$olink_target  # 
  d
}
get_protein_outcome <- function(snps, prow) {
  out <- tryCatch(extract_outcome_data_batched(snps=snps, outcomes=prow$path),
                  error=function(e) { message("[G2+] ieu_out ", prow$protein_id, " err: ", conditionMessage(e)); NULL })
  if (is.null(out) || nrow(out) == 0) return(NULL)
  out$outcome <- prow$olink_target
  out
}

compute_fstat <- function(d) {
  if (is.null(d) || nrow(d) == 0) return(NA_real_)
  # : F ≈ beta^2 / se^2 SNP
  if ("beta.exposure" %in% names(d) && "se.exposure" %in% names(d)) {
    f_per <- (d$beta.exposure / d$se.exposure)^2
  } else if ("beta" %in% names(d) && "se" %in% names(d)) {
    f_per <- (d$beta / d$se)^2
  } else return(NA_real_)
  round(median(f_per, na.rm=TRUE), 1)
}

run_mr_suite <- function(d, label) {
  if (is.null(d) || nrow(d) == 0) {
    logmsg(label, ":  harmonised , "); return(NULL)
  }
  n_iv <- nrow(d)
  logmsg(label, ": n_iv=", n_iv, " ->  MR ")

  result <- list(label=label, n_iv=n_iv)
  result$b_ivw <- NA; result$se_ivw <- NA; result$p_ivw <- NA
  result$b_egger <- NA; result$p_egger <- NA
  result$b_wmed <- NA; result$p_wmed <- NA
  result$b_wmode <- NA; result$p_wmode <- NA
  result$Q_ivw <- NA; result$Q_p_ivw <- NA
  result$egger_intercept <- NA; result$egger_intercept_p <- NA
  result$loo_min_p <- NA; result$loo_max_p <- NA; result$loo_driven <- NA
  result$steiger_snpc <- NA
  result$median_F <- NA

  methods <- c("mr_ivw", "mr_weighted_median", "mr_weighted_mode")
  if (n_iv >= 3) methods <- c("mr_egger_regression", methods)
  mr_res <- tryCatch(mr(d, method_list=methods), error=function(e) {
    logmsg(label, ": mr() multi err, trying IVW only: ", conditionMessage(e))
    tryCatch(mr(d, method_list="mr_ivw"), error=function(e2) {
      logmsg(label, ": mr() IVW-only also err: ", conditionMessage(e2)); NULL }) })

  method_map <- c(
    "Inverse variance weighted" = "ivw",
    "MR Egger"                  = "egger",
    "Weighted median"            = "wmed",
    "Weighted mode"              = "wmode"
  )
  if (!is.null(mr_res) && nrow(mr_res) > 0) {
    result$mr_all <- mr_res
    for (m in unique(mr_res$method)) {
      row <- mr_res[mr_res$method == m, ][1, ]
      key <- method_map[m]
      if (is.na(key)) key <- gsub(" ", "_", tolower(m))
      result[[paste0("b_",  key)]] <- suppressWarnings(signif(as.numeric(row$b), 4))
      result[[paste0("se_", key)]] <- suppressWarnings(signif(as.numeric(row$se), 4))
      result[[paste0("p_",  key)]] <- suppressWarnings(signif(as.numeric(row$pval), 4))
    }
  } else {
    # fallback: IVW mr proxy SNP
    logmsg(label, ":  IVW  (mr() )")
    w <- 1 / d$se.outcome^2
    bx <- d$beta.exposure
    by <- d$beta.outcome
    denom <- sum(w * bx^2)
    if (denom > 0) {
      b_ivw <- sum(w * bx * by) / denom
      se_ivw <- sqrt(1 / denom)
      p_ivw <- 2 * pnorm(-abs(b_ivw / se_ivw))
      result$b_ivw <- signif(b_ivw, 4)
      result$se_ivw <- signif(se_ivw, 4)
      result$p_ivw <- signif(p_ivw, 4)
      exp_name <- if(length(unique(d$exposure)) > 0) as.character(unique(d$exposure)[1]) else "unknown"
      out_name <- if(length(unique(d$outcome)) > 0 && !all(is.na(d$outcome))) as.character(unique(d$outcome)[1]) else "AD"
      result$mr_all <- data.frame(
        exposure=exp_name, outcome=out_name,
        method="Inverse variance weighted (manual)",
        b=b_ivw, se=se_ivw, pval=p_ivw, nsnp=n_iv,
        stringsAsFactors=FALSE)
    }
  }

  if (n_iv >= 2) {
    het <- tryCatch(mr_heterogeneity(d, method_list=c("mr_egger_regression", "mr_ivw")),
                    error=function(e) { logmsg(label, ": het err: ", conditionMessage(e)); NULL })
    if (!is.null(het) && nrow(het) > 0) {
      result$heterogeneity <- het
      ivw_het <- het[grepl("Inverse variance|IVW", het$method), ]
      if (nrow(ivw_het) > 0) {
        result$Q_ivw <- signif(ivw_het$Q, 4)
        result$Q_p_ivw <- signif(ivw_het$Q_pval, 4)
      }
    }
  }

  # 3. MR-Egger intercept - >=3 SNPs
  if (n_iv >= 3) {
    pleio <- tryCatch(mr_pleiotropy_test(d), error=function(e) {
      logmsg(label, ": pleio err: ", conditionMessage(e)); NULL })
    if (!is.null(pleio) && nrow(pleio) > 0) {
      result$pleiotropy <- pleio
      result$egger_intercept <- signif(pleio$egger_intercept[1], 4)
      result$egger_intercept_se <- signif(pleio$se[1], 4)
      result$egger_intercept_p <- signif(pleio$pval[1], 4)
    }
  } else {
    result$egger_intercept <- NA; result$egger_intercept_p <- NA
    logmsg(label, ": n_iv < 3, Egger ")
  }

  if (n_iv >= 2) {
    loo <- tryCatch(mr_leaveoneout(d), error=function(e) {
      logmsg(label, ": loo err: ", conditionMessage(e)); NULL })
    if (!is.null(loo) && nrow(loo) > 0) {
      result$loo <- loo
      loo_ivw <- if ("method" %in% names(loo)) loo[grepl("Inverse variance|IVW", loo$method), ] else loo
      if (nrow(loo_ivw) > 0) {
        result$loo_min_p <- signif(min(loo_ivw$p, na.rm=TRUE), 4)
        result$loo_max_p <- signif(max(loo_ivw$p, na.rm=TRUE), 4)
        # SNP p sig ns
        full_p <- result$p_ivw
        if (!is.na(full_p) && full_p < 0.05) {
          result$loo_driven <- any(loo_ivw$p > 0.05, na.rm=TRUE)
        } else {
          result$loo_driven <- FALSE
        }
      }
    }
  }

  # 5. Steiger - eaf.exposure + eaf.outcome
  has_eaf_exp <- !is.null(d$eaf.exposure) && any(!is.na(d$eaf.exposure))
  has_eaf_out <- !is.null(d$eaf.outcome) && any(!is.na(d$eaf.outcome))
  if (has_eaf_exp && has_eaf_out && n_iv >= 2) {
    steiger <- tryCatch(directionality_test(d), error=function(e) {
      logmsg(label, ": steiger err: ", conditionMessage(e)); NULL })
    if (!is.null(steiger) && nrow(steiger) > 0) {
      result$steiger <- steiger
      result$steiger_snpc <- steiger$steiger_dir[1]  # TRUE=exp->out 
    }
  } else {
    result$steiger_snpc <- NA
    logmsg(label, ": eaf , Steiger ")
  }

  result$median_F <- compute_fstat(d)
  logmsg(label, ": median F=", result$median_F,
         " | IVW p=", result$p_ivw,
         " | Egger int p=", result$egger_intercept_p,
         " | Q p=", result$Q_p_ivw)
  result
}

# ---- Bootstrap CI for indirect effect
bootstrap_mediation <- function(b1, se1, b2, se2, n_boot=THRESH$n_boot, seed=42) {
  set.seed(seed)
  boots <- numeric(n_boot)
  for (i in seq_len(n_boot)) {
    b1_b <- rnorm(1, mean=b1, sd=se1)
    b2_b <- rnorm(1, mean=b2, sd=se2)
    boots[i] <- b1_b * b2_b
  }
  list(
    boot_mean = mean(boots),
    boot_median = median(boots),
    boot_ci_lower = quantile(boots, 0.025),
    boot_ci_upper = quantile(boots, 0.975),
    boot_p = 2 * min(mean(boots > 0), mean(boots < 0))
  )
}

prepare_harmonised <- function(exp_id, out_id, exp_is_protein, out_is_protein, prow=NULL, p1=5e-8) {
  if (exp_is_protein) {
    exp <- get_protein_instruments(prow, p1=p1)
  } else {
    exp <- tryCatch(extract_instruments(exp_id, p1=p1, r2=THRESH$clump_r2, kb=THRESH$clump_kb),
                    error=function(e) { logmsg("exp err: ", conditionMessage(e)); NULL })
  }
  if (is.null(exp) || nrow(exp) == 0) { logmsg("exp NULL/empty"); return(NULL) }

  if (out_is_protein) {
    out <- get_protein_outcome(exp$SNP, prow)
  } else {
    out <- tryCatch(extract_outcome_data_batched(snps=exp$SNP, outcomes=out_id),
                    error=function(e) { logmsg("out err: ", conditionMessage(e)); NULL })
  }
  if (is.null(out) || nrow(out) == 0) { logmsg("out NULL/empty (exp n=", nrow(exp), ")"); return(NULL) }

  d <- tryCatch(harmonise_data(exp, out), error=function(e) {
    logmsg("harm err: ", conditionMessage(e)); NULL })
  if (is.null(d) || nrow(d) < 2) { logmsg("harm fail n=", if(is.data.frame(d)) nrow(d) else "NULL"); return(NULL) }
  d
}

## =====================================================================
## =====================================================================
insomnia_exp_id <- GWAS_ID$insomnia
ad_out_id       <- GWAS_ID$ad

all_step1 <- list()  # insomnia -> protein
all_step2 <- list()  # protein -> AD
all_mediation <- list()

for (i in seq_len(nrow(protein_map))) {
  prow <- protein_map[i, ]
  pid <- prow$protein_id
  name <- prow$olink_target
  logmsg("=====  ", i, "/", nrow(protein_map), ": ", pid, " (", name, ") =====")

  # ---- Step1: insomnia -> protein
  logmsg("Step1: insomnia -> ", name)
  d1 <- prepare_harmonised(exp_id=insomnia_exp_id, out_id=prow$path,
                           exp_is_protein=FALSE, out_is_protein=TRUE, prow=prow)
  if (is.null(d1)) {
    logmsg("Step1 ,  ", pid); next
  }
  s1_suite <- run_mr_suite(d1, paste0("Step1_ins_to_", name))
  all_step1[[pid]] <- s1_suite

  # IVW NA mr
  s1_b  <- as.numeric(s1_suite$b_ivw)
  s1_se <- as.numeric(s1_suite$se_ivw)
  s1_ivw <- as.numeric(s1_suite$p_ivw)
  s1_n  <- s1_suite$n_iv

  # ---- Step2: protein -> AD
  logmsg("Step2: ", name, " -> AD")
  d2 <- prepare_harmonised(exp_id=prow$path, out_id=ad_out_id,
                           exp_is_protein=TRUE, out_is_protein=FALSE, prow=prow)
  if (is.null(d2)) {
    logmsg("Step2 ,  ", pid); next
  }
  s2_suite <- run_mr_suite(d2, paste0("Step2_", name, "_to_AD"))
  all_step2[[pid]] <- s2_suite

  s2_b  <- as.numeric(s2_suite$b_ivw)
  s2_se <- as.numeric(s2_suite$se_ivw)
  s2_ivw <- as.numeric(s2_suite$p_ivw)
  s2_n  <- s2_suite$n_iv

  indirect <- if (any(is.na(c(s1_b, s2_b)))) NA_real_ else s1_b * s2_b
  se_ind <- if (any(is.na(c(s1_se, s2_se, s1_b, s2_b)))) NA_real_ else sqrt(s2_b^2 * s1_se^2 + s1_b^2 * s2_se^2)
  p_ind <- if (any(is.na(c(indirect, se_ind))) || se_ind == 0) NA_real_ else 2 * pnorm(-abs(indirect) / se_ind)

  boot <- if (any(is.na(c(s1_b, s1_se, s2_b, s2_se)))) {
    list(boot_mean=NA_real_, boot_ci_lower=NA_real_, boot_ci_upper=NA_real_, boot_p=NA_real_)
  } else {
    tryCatch(bootstrap_mediation(s1_b, s1_se, s2_b, s2_se, n_boot=THRESH$n_boot),
             error=function(e) {
               logmsg("bootstrap err: ", conditionMessage(e))
               list(boot_mean=NA_real_, boot_ci_lower=NA_real_, boot_ci_upper=NA_real_, boot_p=NA_real_) })
  }

  sg <- function(x) {
    v <- suppressWarnings(as.numeric(x))
    if (length(v) == 0) NA_real_ else suppressWarnings(signif(v[1], 4))
  }

  all_mediation[[pid]] <- data.frame(
    protein=pid, target=name,
    b1=sg(s1_b), se1=sg(s1_se), p1=sg(s1_ivw), n1=s1_n,
    b1_egger=sg(s1_suite$b_egger), p1_egger=sg(s1_suite$p_egger),
    egger_int1=sg(s1_suite$egger_intercept), egger_int_p1=sg(s1_suite$egger_intercept_p),
    Q_p1=sg(s1_suite$Q_p_ivw), loo_min_p1=sg(s1_suite$loo_min_p), loo_max_p1=sg(s1_suite$loo_max_p),
    loo_driven1=if(is.null(s1_suite$loo_driven)) NA else s1_suite$loo_driven,
    median_F1=sg(s1_suite$median_F), steiger1=sg(s1_suite$steiger_snpc),
    b2=sg(s2_b), se2=sg(s2_se), p2=sg(s2_ivw), n2=s2_n,
    b2_egger=sg(s2_suite$b_egger), p2_egger=sg(s2_suite$p_egger),
    egger_int2=sg(s2_suite$egger_intercept), egger_int_p2=sg(s2_suite$egger_intercept_p),
    Q_p2=sg(s2_suite$Q_p_ivw), loo_min_p2=sg(s2_suite$loo_min_p), loo_max_p2=sg(s2_suite$loo_max_p),
    loo_driven2=if(is.null(s2_suite$loo_driven)) NA else s2_suite$loo_driven,
    median_F2=sg(s2_suite$median_F), steiger2=sg(s2_suite$steiger_snpc),
    indirect=sg(indirect), se_ind=sg(se_ind), p_ind=sg(p_ind),
    boot_mean=sg(boot$boot_mean),
    boot_ci_lower=sg(boot$boot_ci_lower),
    boot_ci_upper=sg(boot$boot_ci_upper),
    boot_p=sg(boot$boot_p),
    stringsAsFactors=FALSE
  )
  logmsg(pid, " : indirect=", sg(indirect),
         " (delta p=", sg(p_ind), ", boot p=", sg(boot$boot_p), ")")
}

if (length(all_mediation) == 0) stop("[G2+] ")

mediation_df <- dplyr::bind_rows(all_mediation) %>%
  mutate(fdr = p.adjust(p_ind, method="fdr")) %>%
  arrange(p_ind)

## ---- ----
saveRDS(list(step1=all_step1, step2=all_step2, mediation=mediation_df),
        file.path(G2_OUT, "G2_enhanced_full.rds"))
write.csv(mediation_df, file.path(G2_OUT, "G2_enhanced_mediation.csv"), row.names=FALSE)

for (pid in names(all_step1)) {
  s1 <- all_step1[[pid]]
  if (!is.null(s1$mr_all)) {
    write.csv(s1$mr_all, file.path(G2_OUT, paste0("G2_step1_mr_", pid, ".csv")), row.names=FALSE)
  }
  if (!is.null(s1$heterogeneity)) {
    write.csv(s1$heterogeneity, file.path(G2_OUT, paste0("G2_step1_het_", pid, ".csv")), row.names=FALSE)
  }
  if (!is.null(s1$pleiotropy)) {
    write.csv(s1$pleiotropy, file.path(G2_OUT, paste0("G2_step1_pleio_", pid, ".csv")), row.names=FALSE)
  }
  if (!is.null(s1$loo)) {
    write.csv(s1$loo, file.path(G2_OUT, paste0("G2_step1_loo_", pid, ".csv")), row.names=FALSE)
  }
}
for (pid in names(all_step2)) {
  s2 <- all_step2[[pid]]
  if (!is.null(s2$mr_all)) {
    write.csv(s2$mr_all, file.path(G2_OUT, paste0("G2_step2_mr_", pid, ".csv")), row.names=FALSE)
  }
  if (!is.null(s2$heterogeneity)) {
    write.csv(s2$heterogeneity, file.path(G2_OUT, paste0("G2_step2_het_", pid, ".csv")), row.names=FALSE)
  }
  if (!is.null(s2$pleiotropy)) {
    write.csv(s2$pleiotropy, file.path(G2_OUT, paste0("G2_step2_pleio_", pid, ".csv")), row.names=FALSE)
  }
  if (!is.null(s2$loo)) {
    write.csv(s2$loo, file.path(G2_OUT, paste0("G2_step2_loo_", pid, ".csv")), row.names=FALSE)
  }
}

## ---- ----
logmsg("=== G2  ===")
logmsg(": ", nrow(mediation_df))
logmsg(" (FDR<0.05): ", sum(mediation_df$fdr < THRESH$protein_fdr))
for (i in seq_len(nrow(mediation_df))) {
  r <- mediation_df[i, ]
  logmsg(r$protein, " (", r$target, "):")
  logmsg("  Step1: b=", r$b1, " p=", r$p1, " n=", r$n1,
         " | Egger p=", r$p1_egger, " int p=", r$egger_int_p1,
         " | Q p=", r$Q_p1, " | F=", r$median_F1,
         " | Steiger=", r$steiger1)
  logmsg("  Step2: b=", r$b2, " p=", r$p2, " n=", r$n2,
         " | Egger p=", r$p2_egger, " int p=", r$egger_int_p2,
         " | Q p=", r$Q_p2, " | F=", r$median_F2,
         " | Steiger=", r$steiger2)
  logmsg("  Indirect: ", r$indirect, " (delta p=", r$p_ind,
         ", boot p=", r$boot_p, ", 95% CI=[", r$boot_ci_lower, ", ", r$boot_ci_upper, "])")
}
logmsg(": ", G2_OUT)
logmsg("Done.")