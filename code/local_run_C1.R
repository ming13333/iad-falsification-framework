# !/usr/bin/env Rscript
# ============================================================
# API C1 09b_metabolite_mediation_slim.R .
# : data/raw/c1_cache/ cache_c1_inputs.R harmonised .
# : results/MetMediation_local/mediation_slim_10.csv
# C:/Temp/iad_g1/results/MetMediation/mediation_slim_10.csv
# : Rscript code/local_run_C1.R
# ============================================================
suppressMessages(library(data.table))
set.seed(20260801)
BOOT_N <- 5000

CACHE <- "./data/raw/c1_cache"
OUT   <- "./results/MetMediation_local"
dir.create(OUT, showWarnings = FALSE, recursive = TRUE)

mets <- c("met-d-Total_C","met-d-LDL_C","met-d-HDL_C","met-d-Total_TG",
          "met-d-DHA","met-d-Omega_3","met-d-Ile","met-d-Leu","met-d-Val","met-d-GlycA")

bootstrap_mediation <- function(b1, se1, b2, se2, n_boot = BOOT_N, seed = 42) {
  set.seed(seed)
  boots <- numeric(n_boot)
  for (i in seq_len(n_boot)) {
    b1_b <- rnorm(1, mean = b1, sd = se1)
    b2_b <- rnorm(1, mean = b2, sd = se2)
    boots[i] <- b1_b * b2_b
  }
  list(boot_ci_lower = quantile(boots, 0.025),
       boot_ci_upper = quantile(boots, 0.975),
       boot_p = 2 * min(mean(boots > 0), mean(boots < 0)))
}
sig <- function(x) if (is.na(x)) NA else signif(x, 4)

rows <- list()
for (m in mets) {
  f1 <- file.path(CACHE, sprintf("%s_step1_harm.tsv.gz", m))
  f2 <- file.path(CACHE, sprintf("%s_step2_harm.tsv.gz", m))
  if (!file.exists(f1) || !file.exists(f2)) { cat(sprintf("SKIP %s (missing cache)\n", m)); next }
  h1 <- fread(f1); h2 <- fread(f2)

  # Step1 IVW edu -> met
  bx <- h1$beta.exposure; by <- h1$beta.outcome; so <- h1$se.outcome
  ok <- is.finite(bx) & is.finite(by) & is.finite(so) & so > 0
  bx <- bx[ok]; by <- by[ok]; so <- so[ok]
  f1v <- (h1$beta.exposure[ok] / h1$se.exposure[ok])^2; f1_med <- median(f1v, na.rm = TRUE)
  w <- 1 / so^2; den <- sum(w * bx^2)
  b1 <- sum(w * bx * by) / den; se1 <- sqrt(1 / den); p1 <- 2 * pnorm(-abs(b1 / se1)); n1 <- length(bx)

  # Step2 IVW met -> AD
  bx2 <- h2$beta.exposure; by2 <- h2$beta.outcome; so2 <- h2$se.outcome
  ok2 <- is.finite(bx2) & is.finite(by2) & is.finite(so2) & so2 > 0
  bx2 <- bx2[ok2]; by2 <- by2[ok2]; so2 <- so2[ok2]
  f2v <- (h2$beta.exposure[ok2] / h2$se.exposure[ok2])^2; f2_med <- median(f2v, na.rm = TRUE)
  w2 <- 1 / so2^2; den2 <- sum(w2 * bx2^2)
  b2 <- sum(w2 * bx2 * by2) / den2; se2 <- sqrt(1 / den2); p2 <- 2 * pnorm(-abs(b2 / se2)); n2 <- length(bx2)

  ind <- b1 * b2; se_ind <- sqrt(b2^2 * se1^2 + b1^2 * se2^2); p_ind <- 2 * pnorm(-abs(ind / se_ind))
  bt <- bootstrap_mediation(b1, se1, b2, se2, n_boot = BOOT_N, seed = 42)

  rows[[length(rows) + 1]] <- data.frame(
    met = m, b1 = sig(b1), se1 = sig(se1), p1 = sig(p1), n1 = n1, f1_med = signif(f1_med, 3),
    b2 = sig(b2), se2 = sig(se2), p2 = sig(p2), n2 = n2, f2_med = signif(f2_med, 3),
    indirect = sig(ind), se_ind = sig(se_ind), p_ind = sig(p_ind),
    boot_ci_lower = sig(bt$boot_ci_lower), boot_ci_upper = sig(bt$boot_ci_upper), boot_p = sig(bt$boot_p),
    weak_inst = (n2 < 10 | (f2_med < 10 & !is.na(f2_med))), stringsAsFactors = FALSE)
  cat(sprintf("  %s: b1=%.4f b2=%.4f indirect=%.4f p_ind=%.2g\n", m, b1, b2, ind, p_ind))
}
df <- do.call(rbind, rows)
df$q_ind <- p.adjust(df$p_ind, method = "BH")
write.csv(df, file.path(OUT, "mediation_slim_10.csv"), row.names = FALSE)
cat("\n=== LOCAL C1 DONE ===\n")
print(df[, c("met","b1","p1","b2","p2","indirect","p_ind","q_ind","boot_p","weak_inst")])
sig_m <- df[!is.na(df$q_ind) & df$q_ind < 0.05, ]
if (nrow(sig_m) > 0) {
  cat("\n** Significant mediators (q<0.05): **\n"); print(sig_m$met)
} else cat("\nNo significant mediator at FDR<0.05\n")