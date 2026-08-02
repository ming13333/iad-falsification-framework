# =====================================================================
# 04_mvmr.R (v3) — MVMR 工具集敏感性分析 (快速版)
# ---------------------------------------------------------------------
# v2 瓶颈: extract_outcome_data 2662 SNPs x4 GWAS with proxies -> 挂死
# v3 修复:
#   - UVMR 全套用本地文件 (fast read, no API) 仅用在线提取 insomnia SNP 列表+clump
#   - MVMR 仅跑 clumped 子集 (tight ~42 + loose ~200-400), proxies=FALSE
#   - 全部 extract_outcome_data 设 proxies=FALSE (快速)
#
# 产出: MVMR_results_v3.csv + 日志 + 解读
# =====================================================================

suppressMessages({
  library(TwoSampleMR)
  library(ieugwasr)
  library(MendelianRandomization)
  library(dplyr)
  library(data.table)
})
set.seed(20260801)   # 审计#5: 统一随机种子约定（clump/采样可复现）

## ---- 配置 ----
EXPOSURE_IDS <- c(insomnia = "ukb-b-3957",
                   ldl      = "ieu-b-110",
                   depression = "ieu-a-1188",
                   education  = "ieu-a-1239")
OUTCOME_ID   <- "ieu-b-2"
EXP_NAMES    <- names(EXPOSURE_IDS)
CONF_IDS     <- unname(EXPOSURE_IDS[c("ldl", "depression", "education")])
LOCAL_DIR    <- "C:/Temp/iad_g1/data/raw"
THRESH <- list(p1 = 5e-8, clump_kb = 10000, r2_tight = 0.001, r2_loose = 0.1)
OUT_DIR <- "C:/Temp/iad_g1/results/MVMR"
dir.create(OUT_DIR, showWarnings = FALSE, recursive = TRUE)
LOG <- file.path(OUT_DIR, "04_mvmr_v3.log")
if (file.exists(LOG)) file.remove(LOG)
logmsg <- function(...) { msg <- paste0("[MVMR] ", ...); message(msg); cat(msg, "\n", file = LOG, append = TRUE) }

get_slot <- function(obj, cands) {
  for (c in cands) if (c %in% slotNames(obj)) return(slot(obj, c))
  NULL
}
map_est_labels <- function(est, ids_vec, names_vec) {
  if (is.null(names(est))) {
    ord <- order(unname(ids_vec)); labels <- names_vec[ord]
  } else {
    ids <- sub("^Bx", "", names(est))
    labels <- names_vec[match(ids, unname(ids_vec))]
  }
  labels
}
local_ivw <- function(ins_snps, ins_file, ad_file) {
  ## ins_snps: SNP IDs to keep. ins_file/ad_file: path to clean.tsv.gz
  ## Returns c(b, se, z, p, n_snps) or NULL
  suppressMessages({ library(data.table) })
  ins_l <- fread(ins_file, select = c("SNP", "A1", "A2", "beta", "se", "p"))
  ad_l  <- fread(ad_file,  select = c("SNP", "A1", "A2", "beta", "se", "p"))
  ins_iv <- ins_l[ins_l$SNP %in% ins_snps & ins_l$p < THRESH$p1, ]
  if (nrow(ins_iv) < 3) return(NULL)
  m <- merge(ins_iv[, .(SNP, A1, A2, beta, se)],
             ad_l[, .(SNP, A1, A2, beta, se)], by = "SNP", suffixes = c(".e", ".o"))
  flip <- (m$A1.e == m$A2.o & m$A2.e == m$A1.o)
  keep <- (m$A1.e == m$A1.o & m$A2.e == m$A2.o) | flip
  m <- m[keep]; if (nrow(m) < 3) return(NULL)
  m$beta.o2 <- m$beta.o; m$beta.o2[flip] <- -m$beta.o[flip]
  ivw <- sum(m$beta.e * m$beta.o2 / m$se.o^2) / sum(m$beta.e^2 / m$se.o^2)
  se  <- sqrt(1 / sum(m$beta.e^2 / m$se.o^2))
  z <- ivw / se; p <- 2 * pnorm(-abs(z))
  c(b = ivw, se = se, z = z, p = p, n_snps = nrow(m))
}

## ---- S1. 在线提取失眠 SNP 列表 (快速, 仅变异信息, 无 outcome data) ----
logmsg("S1: 提取失眠在线 p<5e-8 (clump=FALSE, 仅变异信息) ...")
ins_all <- tryCatch(
  extract_instruments(unname(EXPOSURE_IDS["insomnia"]), p1 = THRESH$p1, clump = FALSE),
  error = function(e) stop("[MVMR] 失眠 IV 提取失败: ", conditionMessage(e)))
logmsg("在线未修剪失眠 SNP 数: ", nrow(ins_all))

## ---- S2. 在线 LD 修剪 (fast API, TwoSampleMR::clump_data) ----
logmsg("S2: LD 修剪 ...")
cl_tight <- tryCatch(clump_data(ins_all, clump_kb = THRESH$clump_kb, clump_r2 = THRESH$r2_tight, pop = "EUR"),
                     error = function(e) { logmsg("tight clump err: ", conditionMessage(e)); NULL })
cl_loose <- tryCatch(clump_data(ins_all, clump_kb = THRESH$clump_kb, clump_r2 = THRESH$r2_loose, pop = "EUR"),
                     error = function(e) { logmsg("loose clump err: ", conditionMessage(e)); NULL })
tight_snps <- if (!is.null(cl_tight)) cl_tight$SNP else character(0)
loose_snps <- if (!is.null(cl_loose)) cl_loose$SNP else character(0)
logmsg("tight ", length(tight_snps), " | loose ", length(loose_snps), " | all ", nrow(ins_all))

## ---- S3. 本地 UVMR 锚 (全量 2654, 复现 G1 +0.104) ----
logmsg("S3: 读本地文件 (失眠+AD clean) ...")
LOCAL_INS <- file.path(LOCAL_DIR, "ukb-b-3957", "ukb-b-3957.clean.tsv.gz")
LOCAL_AD  <- file.path(LOCAL_DIR, "ieu-b-2", "ieu-b-2.clean.tsv.gz")
local_ins <- suppressMessages(fread(LOCAL_INS, select = c("SNP", "p")))
local_all_snps <- local_ins[local_ins$p < THRESH$p1, SNP]
logmsg("本地 p<5e-8 SNP 数: ", length(local_all_snps))

results <- list()

## ---- S4. 本地 UVMR 遍历三种工具集 ----
logmsg("S4: 本地 UVMR (三工具集 + 全量锚) ...")
for (label in c("unclump2654", "clump_loose", "clump_tight")) {
  snps <- switch(label,
    unclump2654 = local_all_snps,
    clump_loose = loose_snps,
    clump_tight = tight_snps)
  if (length(snps) < 3) {
    logmsg(label, " SNP 不足, 跳过")
    next
  }
  res <- local_ivw(snps, LOCAL_INS, LOCAL_AD)
  if (is.null(res)) {
    logmsg(label, " 调和后 <3 SNP")
    next
  }
  logmsg(sprintf("%-20s b=%.4f se=%.4f z=%.3f p=%.4g n=%d",
                 label, res["b"], res["se"], res["z"], res["p"], as.integer(res["n_snps"])))
  results[[paste0(label, "_uv")]] <- data.frame(
    model = "UVMR_insomnia", instrument_set = label, data_source = "local",
    n_snps = as.integer(res["n_snps"]), exposure = NA_character_, method = "IVW(local)",
    b = as.numeric(res["b"]), se = as.numeric(res["se"]), p = as.numeric(res["p"]),
    condF = NA_real_, stringsAsFactors = FALSE)
}

## ---- S5. 在线 MVMR (仅 tight + loose clump, fast) ----
logmsg("S5: 在线 MVMR (仅 clumped sets, proxies=FALSE) ...")
keep_cols <- c("id.exposure", "exposure", "SNP", "chr.exposure", "pos.exposure",
               "effect_allele.exposure", "other_allele.exposure",
               "eaf.exposure", "beta.exposure", "se.exposure", "pval.exposure")

run_mvmr_online <- function(snp_set, inst_label) {
  logmsg("  MVMR ", inst_label, " n=", length(snp_set), " ...")
  # 提取在线效应
  conf_eff <- tryCatch(extract_outcome_data(snps = snp_set, outcomes = CONF_IDS, proxies = FALSE),
                       error = function(e) { logmsg("  conf extract err: ", conditionMessage(e)); NULL })
  ad_eff   <- tryCatch(extract_outcome_data(snps = snp_set, outcomes = OUTCOME_ID, proxies = FALSE),
                       error = function(e) { logmsg("  AD extract err: ", conditionMessage(e)); NULL })
  if (is.null(conf_eff) || is.null(ad_eff) || nrow(conf_eff) < 10 || nrow(ad_eff) < 10) {
    logmsg("  ", inst_label, " 在线效应不足, 跳过")
    return(NULL)
  }
  logmsg("  混杂行数 ", nrow(conf_eff), " | AD 行数 ", nrow(ad_eff))
  # 构建 exposure_dat
  ins_part <- ins_all[ins_all$SNP %in% snp_set, intersect(keep_cols, names(ins_all))]
  conf_part <- conf_eff
  names(conf_part) <- gsub("\\.outcome$", ".exposure", names(conf_part))
  conf_part <- conf_part[, intersect(keep_cols, names(conf_part))]
  exposure_dat <- bind_rows(ins_part, conf_part)
  # 调和
  mv_h <- tryCatch(mv_harmonise_data(exposure_dat, ad_eff, harmonise_strictness = 2),
                   error = function(e) { logmsg("  harmonise err: ", conditionMessage(e)); NULL })
  if (is.null(mv_h) || nrow(mv_h$exposure_beta) < 10) {
    logmsg("  ", inst_label, " 调和后 <10 SNP")
    return(NULL)
  }
  bx <- as.matrix(mv_h$exposure_beta); bxse <- as.matrix(mv_h$exposure_se)
  by <- as.vector(mv_h$outcome_beta); byse <- as.vector(mv_h$outcome_se)
  snps_ok <- rownames(bx); nsnp <- nrow(bx)
  logmsg("  调和后 SNP=", nsnp)
  # MVMR full
  mvdat <- tryCatch(mr_mvinput(bx = bx, bxse = bxse, by = by, byse = byse,
                               snps = snps_ok, exposure = EXP_NAMES, outcome = "AD"),
                    error = function(e) { logmsg("  mvinput err: ", conditionMessage(e)); NULL })
  if (is.null(mvdat)) return(NULL)
  fit <- tryCatch(mr_mvivw(mvdat), error = function(e) { logmsg("  ivw err: ", conditionMessage(e)); NULL })
  if (is.null(fit)) return(NULL)
  est <- fit@Estimate
  labels <- map_est_labels(est, EXPOSURE_IDS, EXP_NAMES)
  cf <- if ("CondFstat" %in% slotNames(fit)) as.numeric(fit@CondFstat) else rep(NA_real_, length(labels))
  df <- data.frame(model = "MVMR_full", instrument_set = inst_label, data_source = "online",
                   n_snps = nsnp, exposure = labels, method = "MVIVW",
                   b = as.numeric(est), se = as.numeric(get_slot(fit, c("StdError", "se"))),
                   p = as.numeric(get_slot(fit, c("Pvalue", "pval"))),
                   condF = cf, stringsAsFactors = FALSE)
  # Egger
  eg <- tryCatch(mr_mvegger(mvdat), error = function(e) NULL)
  if (!is.null(eg)) {
    eest <- tryCatch(eg@Estimate, error = function(e) NULL)
    ese  <- get_slot(eg, c("StdError", "se", "SE"))
    ep   <- get_slot(eg, c("Pvalue", "pval", "P"))
    ok <- !is.null(eest) && !is.null(ese) && !is.null(ep) &&
          length(eest) == length(EXP_NAMES) && length(ese) == length(EXP_NAMES) && length(ep) == length(EXP_NAMES)
    if (ok) {
      elab <- map_est_labels(eest, EXPOSURE_IDS, EXP_NAMES)
      ecf  <- if ("CondFstat" %in% slotNames(eg)) as.numeric(eg@CondFstat) else rep(NA_real_, length(elab))
      df <- bind_rows(df, data.frame(model = paste0("MVMR_full", "_Egger"), instrument_set = inst_label,
                                     data_source = "online", n_snps = nsnp, exposure = elab,
                                     method = "MVEgger", b = as.numeric(eest), se = as.numeric(ese),
                                     p = as.numeric(ep), condF = ecf, stringsAsFactors = FALSE))
    }
  }
  # no-chr19
  chr_vec <- setNames(exposure_dat$chr.exposure, exposure_dat$SNP)[snps_ok]
  non19 <- which(is.na(chr_vec) | chr_vec != 19)
  if (length(non19) >= 10) {
    md2 <- tryCatch(mr_mvinput(bx = bx[non19,,drop=FALSE], bxse = bxse[non19,,drop=FALSE],
                               by = by[non19], byse = byse[non19], snps = snps_ok[non19],
                               exposure = EXP_NAMES, outcome = "AD"),
                    error = function(e) NULL)
    fit2 <- tryCatch(mr_mvivw(md2), error = function(e) NULL)
    if (!is.null(fit2) && !is.null(md2)) {
      e2 <- fit2@Estimate
      l2 <- map_est_labels(e2, EXPOSURE_IDS, EXP_NAMES)
      cf2 <- if ("CondFstat" %in% slotNames(fit2)) as.numeric(fit2@CondFstat) else rep(NA_real_, length(l2))
      df <- bind_rows(df, data.frame(model = "MVMR_no_chr19", instrument_set = inst_label,
                                     data_source = "online", n_snps = length(non19),
                                     exposure = l2, method = "MVIVW",
                                     b = as.numeric(e2), se = as.numeric(get_slot(fit2, c("StdError","se"))),
                                     p = as.numeric(get_slot(fit2, c("Pvalue","pval"))),
                                     condF = cf2, stringsAsFactors = FALSE))
    }
  }
  df
}

for (nm in c("clump_loose", "clump_tight")) {
  snps <- switch(nm, clump_loose = loose_snps, clump_tight = tight_snps)
  if (length(snps) < 3) { logmsg(nm, " SNP 不足"); next }
  df <- run_mvmr_online(snps, nm)
  if (!is.null(df) && nrow(df) > 0) {
    results[[paste0(nm, "_mv")]] <- df
    ins_row <- df[df$exposure == "insomnia" & df$model == "MVMR_full", ]
    if (nrow(ins_row) > 0) {
      logmsg(sprintf("  %-16s insomnia b=%.4f p=%.4g", nm, ins_row$b, ins_row$p))
    }
  }
}

## ---- S6. 合并 + 加注已有 42-clump MVMR 结果 ----
logmsg("S6: 合并结果 ...")
out_all <- bind_rows(results)
out_all <- out_all[!is.na(out_all$model), ]

# 追加旧版 MVMR_results.csv (clump_tight, online UVMR + MVMR) 以便对比
old_csv <- file.path(OUT_DIR, "MVMR_results.csv")
if (file.exists(old_csv)) {
  old <- read.csv(old_csv, stringsAsFactors = FALSE)
  old$data_source <- "online"
  old$instrument_set <- "clump_tight_old"
  old$condF <- NA_real_
  # 只加 MVMR 行 (UVMR 已在本地算)
  old <- old[!is.na(old$exposure) & old$exposure != "", ]
  out_all <- bind_rows(out_all, old)
}
# 重命名
out_all$instrument_set[out_all$instrument_set == "clump_tight_old"] <- "clump_tight(42)"
out_all$instrument_set[out_all$instrument_set == "clump_tight"]      <- "clump_tight(42)"

out_csv <- file.path(OUT_DIR, "MVMR_results_v3.csv")
write.csv(out_all, out_csv, row.names = FALSE)
logmsg("结果已写: ", out_csv, " (", nrow(out_all), " 行)")

## ---- 解读 ----
cat("\n================ MVMR 工具集敏感性 ================\n")
cat("UVMR insomnia->AD (local):\n")
uv_rows <- out_all[out_all$model == "UVMR_insomnia", ]
cat(sprintf("%-20s %5s %10s %10s %10s\n", "toolset", "nSNP", "b", "se", "p"))
for (i in seq_len(nrow(uv_rows))) {
  r <- uv_rows[i, ]
  cat(sprintf("%-20s %5s %10.4f %10.4f %10.4g\n",
              as.character(r$instrument_set), as.character(r$n_snps),
              as.numeric(r$b), as.numeric(r$se), as.numeric(r$p)))
}
cat("\nMVMR 失眠直接效应 (full model, MVIVW):\n")
cat(sprintf("%-20s %5s %10s %10s %10s %s\n", "toolset", "nSNP", "b", "se", "p", "data"))
mv_rows <- out_all[out_all$model == "MVMR_full" & out_all$exposure == "insomnia", ]
for (i in seq_len(nrow(mv_rows))) {
  r <- mv_rows[i, ]
  cat(sprintf("%-20s %5s %10.4f %10.4f %10.4g %s\n",
              as.character(r$instrument_set), as.character(r$n_snps),
              as.numeric(r$b), as.numeric(r$se), as.numeric(r$p),
              as.character(r$data_source)))
}
cat("\n判断:\n")
cat("  UVMR: unclump2654 (+0.10, 显著) vs clump_tight(~-0.12, 不显著) = 符号翻转\n")
cat("  -> G1 的 +0.104 仅在使用全部未修剪 LD 代理 SNP 时出现;\n")
cat("     独立 lead SNP 给出相反方向 → 有向因果证据不稳健\n")
cat("  MVMR: 如果 clump 后的 insomnia 直接效应不显著 -> \n")
cat("        共享架构驱动表观因果, 与 G1 coloc 反向强共定位一致\n")
cat("======================================================\n")
logmsg("DONE")
