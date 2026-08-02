# LDSC 完整版: 主分析 + 去 chr19 敏感性 (修复 capture.output 问题)
suppressMessages({ library(GenomicSEM); library(data.table) })

LD_REF   <- "C:/Temp/iad_g1/ld_ref"
LDSCORE  <- file.path(LD_REF, "LDscore")
HM3      <- file.path(LD_REF, "hm3_with_alleles.txt")
OUT_DIR  <- "C:/Temp/iad_g1/results/LDSC"
WORK_DIR <- "C:/Temp/iad_g1/ldsc_work"
dir.create(OUT_DIR, showWarnings = FALSE, recursive = TRUE)
setwd(WORK_DIR)

logmsg <- function(...) message("[LDSC] ", ..., " (", format(Sys.time(), "%H:%M:%S"), ")")

## ---- Munged files already exist from previous run ----
ins_munged <- "insomnia.sumstats.gz"
ad_munged  <- "ad_kunkle.sumstats.gz"
if (!file.exists(ins_munged) || !file.exists(ad_munged)) stop("Munged files missing")

## ---- Main LDSC ----
logmsg("Running main LDSC (insomnia x AD)...")
ldsc_out <- ldsc(
  traits = c(ins_munged, ad_munged),
  sample.prev = c(NA, 0.344),
  population.prev = c(NA, NA),
  ld = LDSCORE, wld = LDSCORE,
  trait.names = c("insomnia", "ad"))

rg <- as.numeric(ldsc_out$S[1, 2] / sqrt(ldsc_out$S[1, 1] * ldsc_out$S[2, 2]))
## Delta method for rg SE (not sqrt(V[2,2]) which is gcov_se)
## Var(rg) ≈ (1/(S11*S22))*V[2,2] + (rg²/(4*S11²))*V[1,1] + (rg²/(4*S22²))*V[3,3]
S11 <- as.numeric(ldsc_out$S[1,1]); S22 <- as.numeric(ldsc_out$S[2,2])
V11 <- as.numeric(ldsc_out$V[1,1]); V22 <- as.numeric(ldsc_out$V[2,2]); V33 <- as.numeric(ldsc_out$V[3,3])
rg_var <- (1/(S11*S22))*V22 + (rg^2/(4*S11^2))*V11 + (rg^2/(4*S22^2))*V33
rg_se <- sqrt(rg_var)
rg_p <- 2 * pnorm(-abs(rg) / rg_se)

results <- data.frame(
  pair = "insomnia x AD (Kunkle)",
  rg = signif(rg, 4), rg_se = signif(rg_se, 4), rg_p = signif(rg_p, 4),
  rg_z = signif(rg / rg_se, 4),
  h2_insomnia = signif(as.numeric(ldsc_out$S[1,1]), 4),
  h2_insomnia_se = signif(sqrt(as.numeric(ldsc_out$V[1,1])), 4),
  h2_ad = signif(as.numeric(ldsc_out$S[2,2]), 4),
  h2_ad_se = signif(sqrt(as.numeric(ldsc_out$V[3,3])), 4),
  gcov = signif(as.numeric(ldsc_out$S[1,2]), 4),
  gcov_se = signif(sqrt(as.numeric(ldsc_out$V[2,2])), 4),
  gcov_p = signif(2*pnorm(-abs(ldsc_out$S[1,2]/sqrt(ldsc_out$V[2,2]))), 4),
  intercept = signif(as.numeric(ldsc_out$I[1,2]), 4),
  stringsAsFactors = FALSE)

logmsg("=== Main Results ===")
logmsg("rg = ", signif(rg, 4), " +/- ", signif(rg_se, 4), " (p = ", signif(rg_p, 4), ")")
write.csv(results, file.path(OUT_DIR, "LDSC_insomnia_AD.csv"), row.names = FALSE)

## ---- Sensitivity: remove chr19 (APOE) ----
logmsg("Sensitivity: removing chr19 (APOE region)...")
# Re-munge without chr19
prep_no_chr19 <- function(file, trait_name) {
  dt <- fread(file, select = c("SNP","CHR","BP","A1","A2","beta","se","p","n","ncase","ncontrol"))
  dt <- dt[dt$CHR != 19, ]
  n_total <- dt$n[1]
  n_case  <- suppressWarnings(as.numeric(dt$ncase[1]))
  n_ctrl  <- suppressWarnings(as.numeric(dt$ncontrol[1]))
  prev <- if (!is.na(n_case) && !is.na(n_ctrl) && n_case > 0) n_case / (n_case + n_ctrl) else NA
  d <- data.frame(
    SNP = as.character(dt$SNP), chr = as.integer(dt$CHR), pos = as.integer(dt$BP),
    A1 = toupper(as.character(dt$A1)), A2 = toupper(as.character(dt$A2)),
    beta = as.numeric(dt$beta), se = as.numeric(dt$se), p = as.numeric(dt$p),
    N = as.integer(dt$n), stringsAsFactors = FALSE)
  d <- d[complete.cases(d[, c("SNP","A1","A2","beta","se","p","N")]), ]
  d <- d[!duplicated(d$SNP), ]
  out_path <- file.path(WORK_DIR, paste0(trait_name, "_nochr19.tsv"))
  write.table(d, out_path, sep = "\t", quote = FALSE, row.names = FALSE)
  list(path = out_path, n = n_total, prev = prev, name = paste0(trait_name, "_n19"))
}

INS_FILE <- "C:/Temp/iad_g1/data/raw/ukb-b-3957/ukb-b-3957.clean.tsv.gz"
AD_FILE  <- "C:/Temp/iad_g1/data/raw/ieu-b-2/ieu-b-2.clean.tsv.gz"

ins_n19 <- prep_no_chr19(INS_FILE, "insomnia")
ad_n19  <- prep_no_chr19(AD_FILE,  "ad_kunkle")

logmsg("Munging no-chr19 files...")
munge(ins_n19$path, HM3, ins_n19$name)
munge(ad_n19$path,  HM3, ad_n19$name)

ins_n19_munged <- paste0(ins_n19$name, ".sumstats.gz")
ad_n19_munged  <- paste0(ad_n19$name,  ".sumstats.gz")

logmsg("Running no-chr19 LDSC...")
ldsc_n19 <- ldsc(
  traits = c(ins_n19_munged, ad_n19_munged),
  sample.prev = c(ins_n19$prev, ad_n19$prev),
  population.prev = c(NA, NA),
  ld = LDSCORE, wld = LDSCORE,
  trait.names = c(ins_n19$name, ad_n19$name))

rg_n19 <- as.numeric(ldsc_n19$S[1, 2] / sqrt(ldsc_n19$S[1, 1] * ldsc_n19$S[2, 2]))
## Delta method for rg SE
S11n <- as.numeric(ldsc_n19$S[1,1]); S22n <- as.numeric(ldsc_n19$S[2,2])
V11n <- as.numeric(ldsc_n19$V[1,1]); V22n <- as.numeric(ldsc_n19$V[2,2]); V33n <- as.numeric(ldsc_n19$V[3,3])
rg_n19_var <- (1/(S11n*S22n))*V22n + (rg_n19^2/(4*S11n^2))*V11n + (rg_n19^2/(4*S22n^2))*V33n
rg_n19_se <- sqrt(rg_n19_var)
rg_n19_p <- 2 * pnorm(-abs(rg_n19) / rg_n19_se)

results_n19 <- data.frame(
  pair = "insomnia x AD (Kunkle, no chr19/APOE)",
  rg = signif(rg_n19, 4), rg_se = signif(rg_n19_se, 4), rg_p = signif(rg_n19_p, 4),
  rg_z = signif(rg_n19 / rg_n19_se, 4),
  h2_insomnia = signif(as.numeric(ldsc_n19$S[1,1]), 4),
  h2_ad = signif(as.numeric(ldsc_n19$S[2,2]), 4),
  stringsAsFactors = FALSE)

logmsg("=== No-chr19 Results ===")
logmsg("rg_no_chr19 = ", signif(rg_n19, 4), " (p = ", signif(rg_n19_p, 4), ")")
logmsg("rg change: ", signif(rg, 4), " -> ", signif(rg_n19, 4))

write.csv(results_n19, file.path(OUT_DIR, "LDSC_insomnia_AD_no_chr19.csv"), row.names = FALSE)

## ---- Summary ----
all_results <- rbind(results, results_n19)
write.csv(all_results, file.path(OUT_DIR, "LDSC_summary.csv"), row.names = FALSE)

logmsg("=== Summary ===")
logmsg("Full:     rg = ", signif(rg, 4), " (p = ", signif(rg_p, 4), ")")
logmsg("No chr19: rg = ", signif(rg_n19, 4), " (p = ", signif(rg_n19_p, 4), ")")
logmsg("Results saved to: ", OUT_DIR, "/LDSC_summary.csv")
logmsg("Done.")
