#!/usr/bin/env Rscript
# ============================================================
# 01d_g1_wrapup.R — G1 收尾补算
#   Task B: coloc_fwd_rep 真实重算并落盘(原 RDS 为 NULL 的真缺口)
#   Task C: Steiger — 本地 clean 缺 eaf, get_r_from_lor 不可算;
#            RDS 中显式存 computed=FALSE + 原因(诚实标注, 不编造)
#   最后 patch live RDS (C:/Temp/iad_g1/results/G1_bidirectional.rds)
# 注: 仅调用函数, 不重跑整管线(MR/coloc_fwd/coloc_rev/mrlap/cause 均已存)。
# ============================================================
suppressMessages({
  library(data.table)
  library(TwoSampleMR)
  library(coloc)
  library(ieugwasr)
})
options(width = 200, scipen = 3)
set.seed(20240721)   # 与原主稿/01c 一致, 保证可比性

## ---- 1. 配置(避免中文路径 source 失败, 直接定义所需量) ----
GWAS_ID <- list(insomnia = "ukb-b-3957", ad = "ieu-b-2", ad_alt = "ebi-a-GCST90027158")
THRESH  <- list(clump_r2 = 0.001, clump_kb = 10000, maf_min = 0.01, fstat_min = 10,
                coloc_pph4 = 0.80, mr_alpha = 0.05, protein_fdr = 0.05, msm_alpha = 0.05)
DIR_DATA       <- "C:/Temp/iad_g1/data"        # 对准已有 harmonized 缓存
DIR_OUT        <- "C:/Temp/iad_g1/results"     # live 输出(01b/01c 写入处)
DIR_RAW_LOCAL  <- "C:/Temp/iad_g1/data/raw"
LOCAL_CLEAN <- list(
  "ukb-b-3957"          = file.path(DIR_RAW_LOCAL, "ukb-b-3957", "ukb-b-3957.clean.tsv.gz"),
  "ieu-b-2"             = file.path(DIR_RAW_LOCAL, "ieu-b-2", "ieu-b-2.clean.tsv.gz"),
  "ebi-a-GCST90027158"  = file.path(DIR_RAW_LOCAL, "ebi-a-GCST90027158", "GCST90027158_buildGRCh37.dedup.tsv.gz")
)
USE_LOCAL_GWAS <- TRUE
LD_REF_DIR <- "C:/Temp/iad_g1/ld_ref/LDscore"
HM3_FILE   <- file.path(LD_REF_DIR, "hm3_with_alleles.txt")
.LocalCleanCache <- new.env(hash = TRUE, parent = emptyenv())
.rsid_map_cache <- new.env(hash = TRUE, parent = emptyenv())   # get_rsid_map 缓存(原稿 460-461)
COLOC_WINDOW_KB <- 500
COLOC_P1 <- 1e-4
COLOC_P2 <- 1e-4
GWAS_N <- list("ukb-b-3957" = 462341, "ieu-b-2" = 63860)
GWAS_S <- list("ieu-b-2" = 0.344, "ukb-b-3957" = 0.30)
RUN_REPLICATION <- TRUE
overlap_correction_run <- FALSE

## ---- 2. 加载函数(仅定义, 不执行管线) ----
source("C:/Temp/iad_g1/defs_only.R")

## ---- 3. 读取 live RDS ----
RDS <- file.path(DIR_OUT, "G1_bidirectional.rds")
dat <- readRDS(RDS)
cat("[01d] 载入 RDS:", RDS, "\n")
cat("[01d] coloc_fwd_rep 现状:", if (is.null(dat$coloc_fwd_rep)) "NULL(需补)" else nrow(dat$coloc_fwd_rep), "\n")

## ---- 4. Task B: coloc_fwd_rep (失眠 → Bellenguez AD) ----
cat("\n=== Task B: coloc_fwd_rep ===\n")
dat_fwd_rep <- get_harmonized(GWAS_ID$insomnia, GWAS_ID$ad_alt, label = "失眠→AD(repl)")
coloc_fwd_rep <- tryCatch(
  run_coloc_regional(exp_id = GWAS_ID$insomnia, out_id = GWAS_ID$ad_alt,
                     label = "失眠~AD(repl)", lead_dat = dat_fwd_rep,
                     window_kb = COLOC_WINDOW_KB),
  error = function(e) { message("  coloc_fwd_rep 失败: ", conditionMessage(e)); NULL })
if (!is.null(coloc_fwd_rep) && nrow(coloc_fwd_rep) > 0) {
  dat$coloc_fwd_rep <- coloc_fwd_rep
  write.csv(coloc_fwd_rep, file.path(DIR_OUT, "G1_coloc_forward_repl.csv"), row.names = FALSE)
  cat("  coloc_fwd_rep 完成:", nrow(coloc_fwd_rep), "loci\n")
  print(coloc_fwd_rep[order(-coloc_fwd_rep$PP.H4), c("lead_snp", "PP.H4", "n_snps")])
} else {
  cat("  coloc_fwd_rep 仍为 NULL(所有窗口不足/失败) — 如实保留 NULL\n")
}

## ---- 5. Task C: Steiger 方向性 ----
# 诚实结论: 本地 clean GWAS 缺 eaf 列, get_r_from_lor(beta,eaf,ncase,ncontrol) 必需 eaf,
# 无法从现有数据计算 r.exposure / r.outcome → directionality_test 不可行。
# 原稿 build_harmonized_local 亦将 eaf.exposure/outcome 置 NA(第161行), 作者已预判此限制。
# 方向性改由: 双向MR(反向β极小+Egger截距显著) + coloc(反向共享信号强) + 生物学先后 判定。
cat("\n=== Task C: Steiger (数据缺口文档化) ===\n")
g_ins <- read_local_clean(GWAS_ID$insomnia, label = "steiger-ins")
g_ad  <- read_local_clean(GWAS_ID$ad,       label = "steiger-ad")
has_eaf <- function(g) !is.null(g) && !is.null(g$eaf) && !all(is.na(g$eaf))
cat("  ukb-b-3957 含 eaf 列:", has_eaf(g_ins), "\n")
cat("  ieu-b-2    含 eaf 列:", has_eaf(g_ad),  "\n")
steiger_note <- list(
  computed = FALSE,
  reason = "本地 clean GWAS 摘要缺 eaf 列; get_r_from_lor(beta,eaf,ncase,ncontrol) 必需 eaf, 方向性 Steiger 检验不可计算。方向性由双向MR(反向β极小+Egger截距显著)+coloc(反向共享信号强)+生物学先后共同判定。",
  eaf_available_exposure = has_eaf(g_ins),
  eaf_available_outcome  = has_eaf(g_ad)
)
dat$steiger_fwd <- steiger_note
dat$steiger_rev <- steiger_note
cat("  Steiger 已以 computed=FALSE + 原因 显式存入 RDS(非静默 NULL)\n")

## ---- 6. 写回 RDS ----
saveRDS(dat, RDS)
cat("\n=== RDS 已更新:", RDS, "===\n")
cat("coloc_fwd_rep :", if (is.null(dat$coloc_fwd_rep)) "NULL" else nrow(dat$coloc_fwd_rep), "\n")
cat("steiger_fwd   :", if (is.null(dat$steiger_fwd)) "NULL" else paste0("documented(", dat$steiger_fwd$computed, ")"), "\n")
cat("steiger_rev   :", if (is.null(dat$steiger_rev)) "NULL" else paste0("documented(", dat$steiger_rev$computed, ")"), "\n")
cat("[01d] 完成。\n")
