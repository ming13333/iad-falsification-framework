# !/usr/bin/env Rscript
# ============================================================
# Task B: coloc_fwd_rep RDS NULL
# Task C: Steiger - clean eaf, get_r_from_lor
# RDS computed=FALSE +
# patch live RDS C:/Temp/iad_g1/results/G1_bidirectional.rds
# : , MR/coloc_fwd/coloc_rev/mrlap/cause .
# ============================================================
suppressMessages({
  library(data.table)
  library(TwoSampleMR)
  library(coloc)
  library(ieugwasr)
})
options(width = 200, scipen = 3)
set.seed(20240721)   # /01c , 

GWAS_ID <- list(insomnia = "ukb-b-3957", ad = "ieu-b-2", ad_alt = "ebi-a-GCST90027158")
THRESH  <- list(clump_r2 = 0.001, clump_kb = 10000, maf_min = 0.01, fstat_min = 10,
                coloc_pph4 = 0.80, mr_alpha = 0.05, protein_fdr = 0.05, msm_alpha = 0.05)
DIR_DATA       <- "./output/data"        #  harmonized 
DIR_OUT        <- "./output/results"     # live (01b/01c )
DIR_RAW_LOCAL  <- "./output/data/raw"
LOCAL_CLEAN <- list(
  "ukb-b-3957"          = file.path(DIR_RAW_LOCAL, "ukb-b-3957", "ukb-b-3957.clean.tsv.gz"),
  "ieu-b-2"             = file.path(DIR_RAW_LOCAL, "ieu-b-2", "ieu-b-2.clean.tsv.gz"),
  "ebi-a-GCST90027158"  = file.path(DIR_RAW_LOCAL, "ebi-a-GCST90027158", "GCST90027158_buildGRCh37.dedup.tsv.gz")
)
USE_LOCAL_GWAS <- TRUE
LD_REF_DIR <- "./output/ld_ref/LDscore"
HM3_FILE   <- file.path(LD_REF_DIR, "hm3_with_alleles.txt")
.LocalCleanCache <- new.env(hash = TRUE, parent = emptyenv())
.rsid_map_cache <- new.env(hash = TRUE, parent = emptyenv())   # get_rsid_map ( 460-461)
COLOC_WINDOW_KB <- 500
COLOC_P1 <- 1e-4
COLOC_P2 <- 1e-4
GWAS_N <- list("ukb-b-3957" = 462341, "ieu-b-2" = 63860)
GWAS_S <- list("ieu-b-2" = 0.344, "ukb-b-3957" = 0.30)
RUN_REPLICATION <- TRUE
overlap_correction_run <- FALSE

source("./output/defs_only.R")

RDS <- file.path(DIR_OUT, "G1_bidirectional.rds")
dat <- readRDS(RDS)
cat("[01d]  RDS:", RDS, "\n")
cat("[01d] coloc_fwd_rep :", if (is.null(dat$coloc_fwd_rep)) "NULL()" else nrow(dat$coloc_fwd_rep), "\n")

# ---- 4. Task B: coloc_fwd_rep -> Bellenguez AD
cat("\n=== Task B: coloc_fwd_rep ===\n")
dat_fwd_rep <- get_harmonized(GWAS_ID$insomnia, GWAS_ID$ad_alt, label = "->AD(repl)")
coloc_fwd_rep <- tryCatch(
  run_coloc_regional(exp_id = GWAS_ID$insomnia, out_id = GWAS_ID$ad_alt,
                     label = "~AD(repl)", lead_dat = dat_fwd_rep,
                     window_kb = COLOC_WINDOW_KB),
  error = function(e) { message("  coloc_fwd_rep : ", conditionMessage(e)); NULL })
if (!is.null(coloc_fwd_rep) && nrow(coloc_fwd_rep) > 0) {
  dat$coloc_fwd_rep <- coloc_fwd_rep
  write.csv(coloc_fwd_rep, file.path(DIR_OUT, "G1_coloc_forward_repl.csv"), row.names = FALSE)
  cat("  coloc_fwd_rep :", nrow(coloc_fwd_rep), "loci\n")
  print(coloc_fwd_rep[order(-coloc_fwd_rep$PP.H4), c("lead_snp", "PP.H4", "n_snps")])
} else {
  cat("  coloc_fwd_rep  NULL(.) -  NULL\n")
}

# : clean GWAS eaf , get_r_from_lorbeta,eaf,ncase,ncontrol eaf
# r.exposure / r.outcome -> directionality_test .
# build_harmonized_local eaf.exposure/outcome NA161, .
# : MRβ+Egger + coloc + .
cat("\n=== Task C: Steiger () ===\n")
g_ins <- read_local_clean(GWAS_ID$insomnia, label = "steiger-ins")
g_ad  <- read_local_clean(GWAS_ID$ad,       label = "steiger-ad")
has_eaf <- function(g) !is.null(g) && !is.null(g$eaf) && !all(is.na(g$eaf))
cat("  ukb-b-3957  eaf :", has_eaf(g_ins), "\n")
cat("  ieu-b-2     eaf :", has_eaf(g_ad),  "\n")
steiger_note <- list(
  computed = FALSE,
  reason = " clean GWAS  eaf ; get_r_from_lor(beta,eaf,ncase,ncontrol)  eaf,  Steiger . MR(β+Egger)+coloc()+. ",
  eaf_available_exposure = has_eaf(g_ins),
  eaf_available_outcome  = has_eaf(g_ad)
)
dat$steiger_fwd <- steiger_note
dat$steiger_rev <- steiger_note
cat("  Steiger  computed=FALSE +   RDS( NULL)\n")

saveRDS(dat, RDS)
cat("\n=== RDS :", RDS, "===\n")
cat("coloc_fwd_rep :", if (is.null(dat$coloc_fwd_rep)) "NULL" else nrow(dat$coloc_fwd_rep), "\n")
cat("steiger_fwd   :", if (is.null(dat$steiger_fwd)) "NULL" else paste0("documented(", dat$steiger_fwd$computed, ")"), "\n")
cat("steiger_rev   :", if (is.null(dat$steiger_rev)) "NULL" else paste0("documented(", dat$steiger_rev$computed, ")"), "\n")
cat("[01d] . \n")