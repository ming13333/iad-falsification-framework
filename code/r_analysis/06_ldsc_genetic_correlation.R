# =====================================================================
# 06_ldsc_genetic_correlation.R - C: LDSC cross-trait genetic correlation
# ---------------------------------------------------------------------
# Quantify genome-wide genetic correlation rg between insomnia and AD.
# Uses local clean GWAS + GenomicSEM::munge/ldsc + 1000G EUR LD scores.
# Expected: rg significant positive APOE-driven, drops after removing chr19.
# =====================================================================
suppressMessages({ library(GenomicSEM); library(data.table) })

LD_REF   <- "./output/ld_ref"
LDSCORE  <- file.path(LD_REF, "LDscore")       # per-chr l2.ldscore.gz
HM3      <- file.path(LD_REF, "hm3_with_alleles.txt")
INS_FILE <- "./output/data/raw/ukb-b-3957/ukb-b-3957.clean.tsv.gz"
AD_FILE  <- "./output/data/raw/ieu-b-2/ieu-b-2.clean.tsv.gz"
OUT_DIR  <- "./output/results/LDSC"
dir.create(OUT_DIR, showWarnings = FALSE, recursive = TRUE)
WORK_DIR <- "./output/ldsc_work"
dir.create(WORK_DIR, showWarnings = FALSE, recursive = TRUE)
setwd(WORK_DIR)

logmsg <- function(...) message("[LDSC] ", ..., " (", format(Sys.time(), "%H:%M:%S"), ")")

# ---- Prepare GWAS for munge
prep_gwas <- function(file, trait_name) {
  logmsg("Reading: ", file)
  dt <- fread(file, select = c("SNP","CHR","BP","A1","A2","beta","se","p","n","ncase","ncontrol"))
  n_total <- dt$n[1]
  n_case  <- suppressWarnings(as.numeric(dt$ncase[1]))
  n_ctrl  <- suppressWarnings(as.numeric(dt$ncontrol[1]))
  prev <- if (!is.na(n_case) && !is.na(n_ctrl) && n_case > 0) n_case / (n_case + n_ctrl) else NA
  logmsg(trait_name, ": N=", n_total, " prev=", round(prev, 4))

  # Format for GenomicSEM::munge
  d <- data.frame(
    SNP = as.character(dt$SNP),
    chr = as.integer(dt$CHR),
    pos = as.integer(dt$BP),
    A1 = toupper(as.character(dt$A1)),
    A2 = toupper(as.character(dt$A2)),
    beta = as.numeric(dt$beta),
    se = as.numeric(dt$se),
    p = as.numeric(dt$p),
    N = as.integer(dt$n),
    stringsAsFactors = FALSE
  )
  # Remove rows with missing values
  d <- d[complete.cases(d[, c("SNP","A1","A2","beta","se","p","N")]), ]
  # Remove duplicated SNPs
  d <- d[!duplicated(d$SNP), ]
  out_path <- file.path(WORK_DIR, paste0(trait_name, ".tsv"))
  write.table(d, out_path, sep = "\t", quote = FALSE, row.names = FALSE)
  logmsg(trait_name, ": written ", nrow(d), " SNPs to ", out_path)
  list(path = out_path, n = n_total, prev = prev, name = trait_name)
}

ins <- prep_gwas(INS_FILE, "insomnia")
ad  <- prep_gwas(AD_FILE,  "ad_kunkle")

# ---- Munge summary stats filter to HM3, format for LDSC
munge_trait <- function(info, hm3_file) {
  logmsg("Munging: ", info$name)
  invisible(capture.output(
    munge(info$path, hm3_file, info$name)
  ))
  munged_path <- paste0(info$name, ".sumstats.gz")
  if (!file.exists(munged_path)) stop("[LDSC] munge failed for ", info$name)
  logmsg(info$name, ": munged -> ", munged_path)
  munged_path
}

ins_munged <- munge_trait(ins, HM3)
ad_munged  <- munge_trait(ad,  HM3)

# ---- Run cross-trait LDSC
logmsg("Running cross-trait LDSC (insomnia x AD)...")

traits <- c(ins_munged, ad_munged)
sample.prev <- c(ins$prev, ad$prev)
population.prev <- c(NA, NA)
trait.names <- c(ins$name, ad$name)

invisible(capture.output(
  ldsc_out <- ldsc(
    traits = traits,
    sample.prev = sample.prev,
    population.prev = population.prev,
    ld = LDSCORE,
    wld = LDSCORE,
    trait.names = trait.names
  )
))

rg <- as.numeric(ldsc_out$S[1, 2] / sqrt(ldsc_out$S[1, 1] * ldsc_out$S[2, 2]))
rg_se <- sqrt(as.numeric(ldsc_out$V[2, 2]))
rg_p <- 2 * pnorm(-abs(rg) / rg_se)

h2_ins <- as.numeric(ldsc_out$S[1, 1])
h2_ins_se <- sqrt(as.numeric(ldsc_out$V[1, 1]))
h2_ad <- as.numeric(ldsc_out$S[2, 2])
h2_ad_se <- sqrt(as.numeric(ldsc_out$V[3, 3]))

gcov <- as.numeric(ldsc_out$S[1, 2])
gcov_se <- sqrt(as.numeric(ldsc_out$V[2, 2]))
intercept <- as.numeric(ldsc_out$I[1, 2])

results <- data.frame(
  pair = "insomnia x AD (Kunkle)",
  rg = signif(rg, 4),
  rg_se = signif(rg_se, 4),
  rg_p = signif(rg_p, 4),
  rg_z = signif(rg / rg_se, 4),
  h2_insomnia = signif(h2_ins, 4),
  h2_insomnia_se = signif(h2_ins_se, 4),
  h2_ad = signif(h2_ad, 4),
  h2_ad_se = signif(h2_ad_se, 4),
  gcov = signif(gcov, 4),
  gcov_se = signif(gcov_se, 4),
  intercept = signif(intercept, 4),
  n_insomnia = ins$n,
  n_ad = ad$n,
  ins_prev = ins$prev,
  ad_prev = ad$prev,
  stringsAsFactors = FALSE
)

logmsg("=== LDSC Results ===")
logmsg("rg = ", signif(rg, 4), " +/- ", signif(rg_se, 4), " (p = ", signif(rg_p, 4), ")")
logmsg("h2_insomnia = ", signif(h2_ins, 4), " +/- ", signif(h2_ins_se, 4))
logmsg("h2_ad = ", signif(h2_ad, 4), " +/- ", signif(h2_ad_se, 4))
logmsg("intercept = ", signif(intercept, 4))

write.csv(results, file.path(OUT_DIR, "LDSC_insomnia_AD.csv"), row.names = FALSE)

# ---- Sensitivity: remove chr19 APOE region
logmsg("Sensitivity: removing chr19 (APOE region)...")
prep_gwas_no_chr19 <- function(file, trait_name) {
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
    N = as.integer(dt$n), stringsAsFactors = FALSE
  )
  d <- d[complete.cases(d[, c("SNP","A1","A2","beta","se","p","N")]), ]
  d <- d[!duplicated(d$SNP), ]
  out_path <- file.path(WORK_DIR, paste0(trait_name, "_nochr19.tsv"))
  write.table(d, out_path, sep = "\t", quote = FALSE, row.names = FALSE)
  list(path = out_path, n = n_total, prev = prev, name = paste0(trait_name, "_nochr19"))
}

ins_n19 <- prep_gwas_no_chr19(INS_FILE, "insomnia_n19")
ad_n19  <- prep_gwas_no_chr19(AD_FILE,  "ad_kunkle_n19")

ins_n19_munged <- munge_trait(ins_n19, HM3)
ad_n19_munged  <- munge_trait(ad_n19,  HM3)

logmsg("Running cross-trait LDSC (no chr19)...")
traits_n19 <- c(ins_n19_munged, ad_n19_munged)
sample.prev_n19 <- c(ins_n19$prev, ad_n19$prev)

invisible(capture.output(
  ldsc_n19 <- ldsc(traits = traits_n19, sample.prev = sample.prev_n19,
                   population.prev = c(NA, NA), ld = LDSCORE, wld = LDSCORE,
                   trait.names = c(ins_n19$name, ad_n19$name))
))

rg_n19 <- as.numeric(ldsc_n19$S[1, 2] / sqrt(ldsc_n19$S[1, 1] * ldsc_n19$S[2, 2]))
rg_n19_se <- sqrt(as.numeric(ldsc_n19$V[2, 2]))
rg_n19_p <- 2 * pnorm(-abs(rg_n19) / rg_n19_se)

results_n19 <- data.frame(
  pair = "insomnia x AD (Kunkle, no chr19/APOE)",
  rg = signif(rg_n19, 4), rg_se = signif(rg_n19_se, 4), rg_p = signif(rg_n19_p, 4),
  rg_z = signif(rg_n19 / rg_n19_se, 4),
  h2_insomnia = signif(as.numeric(ldsc_n19$S[1,1]), 4),
  h2_ad = signif(as.numeric(ldsc_n19$S[2,2]), 4),
  stringsAsFactors = FALSE
)

logmsg("=== LDSC Results (no chr19) ===")
logmsg("rg_no_chr19 = ", signif(rg_n19, 4), " +/- ", signif(rg_n19_se, 4), " (p = ", signif(rg_n19_p, 4), ")")
logmsg("rg change: ", signif(rg, 4), " -> ", signif(rg_n19, 4), " (delta = ", signif(rg - rg_n19, 4), ")")

write.csv(results_n19, file.path(OUT_DIR, "LDSC_insomnia_AD_no_chr19.csv"), row.names = FALSE)

all_results <- rbind(results, results_n19)
write.csv(all_results, file.path(OUT_DIR, "LDSC_summary.csv"), row.names = FALSE)

logmsg("=== Summary ===")
logmsg("Full:       rg = ", signif(rg, 4), " (p = ", signif(rg_p, 4), ")")
logmsg("No chr19:   rg = ", signif(rg_n19, 4), " (p = ", signif(rg_n19_p, 4), ")")
if (!is.na(rg) && !is.na(rg_n19) && rg > rg_n19) {
  logmsg(">>> rg drops after removing chr19 -> APOE contributes to shared liability <<<")
} else if (!is.na(rg) && !is.na(rg_n19) && rg_n19 >= rg) {
  logmsg(">>> rg does NOT drop after removing chr19 -> shared liability is genome-wide, not APOE-specific <<<")
}
logmsg("Results saved to: ", OUT_DIR, "/LDSC_summary.csv")

# ---- Cleanup temp files
logmsg("Cleaning temporary munge files...")
temp_files <- list.files(WORK_DIR, pattern = "\\.(tsv|sumstats\\.gz|munge\\.log|log)$", full.names = TRUE)
file.remove(temp_files[file.exists(temp_files)])
logmsg("Done.")