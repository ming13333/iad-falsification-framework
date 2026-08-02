#!/usr/bin/env Rscript
# ============================================================
# 01b_overlap_correction.R
# 独立补跑 MRlap + CAUSE 重叠校正 (不重跑已完成的 MR/coloc)
# 依赖: MRlap, cause, data.table 已安装
# 输入: 本地 clean GWAS 文件 + LD 参考数据
# 输出: results/G1_mrlap.csv, results/G1_cause.csv, 更新 G1_bidirectional.rds
# ============================================================

set.seed(20240721)
options(width=200, scipen=3)

suppressMessages({
  library(data.table)
  library(MRlap)
  library(cause)
})

DIR_RAW  <- "C:/Temp/iad_g1/data/raw"
DIR_RES  <- "C:/Temp/iad_g1/results"
DIR_LD   <- "C:/Temp/iad_g1/ld_ref/LDscore"
FILE_HM3 <- "C:/Temp/iad_g1/ld_ref/hm3_with_alleles.txt"
DIR_EXTR <- "C:/Temp/iad_g1/data/extracted"

dir.create(DIR_RES, showWarnings=FALSE, recursive=TRUE)

# ---- 构建 CHR+POS → rsID 映射 (从 LD 参考面板) ----
# ukb-b-3957 用 UKB 风格 ID (CHR_POS_A1_A2), MRlap/CAUSE 需 rsID 与 LD 参考对齐
message("构建 CHR+POS → rsID 映射 (LD 参考面板)...")
rsid_map <- rbindlist(lapply(1:22, function(chr) {
  f <- file.path(DIR_LD, paste0(chr, ".l2.ldscore.gz"))
  if (!file.exists(f)) return(NULL)
  fread(f, select=c("CHR","SNP","BP"))
}))
setnames(rsid_map, c("SNP","BP"), c("rsid","POS"))
setkey(rsid_map, CHR, POS)
message("映射表: ", nrow(rsid_map), " SNPs (HapMap3)")

# ---- 辅助: 读 GWAS 并确保 SNP 列为 rsID + 有 n 列 ----
load_gwas_for_overlap <- function(gwas_id) {
  f <- GWAS_FILES[[gwas_id]]
  dt <- fread(f)
  if ("BP" %in% names(dt)) setnames(dt, "BP", "POS")
  # 补 n 列 (Bellenguez 只有 n_cases/n_controls, 无 n)
  if (!"n" %in% names(dt) && "n_cases" %in% names(dt) && "n_controls" %in% names(dt)) {
    dt[, n := n_cases + n_controls]
    message("  补 n 列: n = n_cases + n_controls")
  }
  # 检查是否需要 rsID 映射
  # 用 merge 代替 setkey+update join, 避免 key 残留干扰 MRlap 内部 data.table 操作
  if (!grepl("^rs", dt$SNP[1])) {
    message("  SNP 列非 rsID 格式 (", dt$SNP[1], "), 用 CHR+POS → rsID 映射...")
    dt <- merge(dt, rsid_map[, .(CHR, POS, rsid)], by=c("CHR","POS"), all.x=TRUE)
    n_mapped <- sum(!is.na(dt$rsid))
    message("  映射成功: ", n_mapped, " / ", nrow(dt), " SNPs 获得 rsID")
    # 用 rsID 替换 SNP; 无映射的行丢弃
    dt <- dt[!is.na(rsid)]
    dt[, SNP := rsid]
    dt[, rsid := NULL]
    # 去重: 多等位基因位点可能映射到同一 rsID, 保留 p 值最小的
    if (anyDuplicated(dt$SNP)) {
      n_before <- nrow(dt)
      setorder(dt, SNP, p)
      dt <- dt[!duplicated(SNP)]
      message("  去重: ", n_before, " → ", nrow(dt), " (移除 ", n_before - nrow(dt), " 重复 rsID)")
    }
  }
  # 过滤掉非 rsID 的行 (如 ieu-b-2 有 "." 值)
  dt <- dt[grepl("^rs", SNP)]
  # 再次去重 (ieu-b-2 可能有重复 rsID)
  if (anyDuplicated(dt$SNP)) {
    setorder(dt, SNP, p)
    dt <- dt[!duplicated(SNP)]
  }
  # 只保留 MRlap/CAUSE 需要的列, 避免与 LD 参考列名冲突
  keep <- intersect(names(dt), c("SNP","CHR","POS","A1","A2","beta","se","p","n"))
  dt <- dt[, ..keep]
  return(dt)
}

# ---- GWAS 文件路径 ----
GWAS_FILES <- list(
  "ukb-b-3957"           = file.path(DIR_RAW, "ukb-b-3957/ukb-b-3957.clean.tsv.gz"),
  "ieu-b-2"              = file.path(DIR_RAW, "ieu-b-2/ieu-b-2.clean.tsv.gz"),
  "ebi-a-GCST90027158"   = file.path(DIR_RAW, "ebi-a-GCST90027158/GCST90027158_buildGRCh37.dedup.tsv.gz")
)

# ---- 4 个方向: (exposure_id, outcome_id, label, need_overlap_corr) ----
COMBOS <- list(
  list(exp="ukb-b-3957", out="ieu-b-2",            label="mrlap_fwd",      cause_label="cause_fwd"),
  list(exp="ieu-b-2",    out="ukb-b-3957",          label="mrlap_rev",      cause_label="cause_rev"),
  list(exp="ukb-b-3957", out="ebi-a-GCST90027158",  label="mrlap_rep_fwd",  cause_label="cause_rep_fwd"),
  list(exp="ebi-a-GCST90027158", out="ukb-b-3957",  label="mrlap_rep_rev",  cause_label="cause_rep_rev")
)

# ============================================================
# MRlap
# ============================================================
run_mrlap_one <- function(exp_id, out_id, label) {
  exp_file <- GWAS_FILES[[exp_id]]
  out_file <- GWAS_FILES[[out_id]]
  if (!file.exists(exp_file) || !file.exists(out_file)) {
    message("[", label, "] GWAS 文件缺失, 跳过。")
    return(NULL)
  }
  message("\n[", label, "] MRlap::MRlap 启动 (exp=", exp_id, ", out=", out_id, ")...")
  message("[", label, "] ld=", DIR_LD, " hm3=", FILE_HM3)

  # MRlap 0.0.3.3 要求列名 POS(不接受 BP); 读为 data.frame 并确保 rsID
  exp_df <- tryCatch(load_gwas_for_overlap(exp_id), error=function(e) { message("[",label,"] 读暴露失败: ",conditionMessage(e)); NULL })
  out_df <- tryCatch(load_gwas_for_overlap(out_id), error=function(e) { message("[",label,"] 读结局失败: ",conditionMessage(e)); NULL })
  if (is.null(exp_df) || is.null(out_df)) return(NULL)
  message("[", label, "] 暴露 SNPs(rsID): ", nrow(exp_df), ", 结局 SNPs(rsID): ", nrow(out_df))

  fit <- tryCatch(
    MRlap::MRlap(
      exposure      = exp_df,
      exposure_name = exp_id,
      outcome       = out_df,
      outcome_name  = out_id,
      ld  = DIR_LD,
      hm3 = FILE_HM3
    ),
    error = function(e) {
      message("[", label, "] MRlap 失败: ", conditionMessage(e))
      NULL
    }
  )
  if (is.null(fit)) return(NULL)

  mc <- fit$MRcorrection
  if (is.null(mc)) {
    message("[", label, "] MRlap 返回结构异常(缺 $MRcorrection), 跳过。")
    return(NULL)
  }

  b_corr  <- as.numeric(mc$corrected_effect)[1]
  se_corr <- as.numeric(mc$corrected_effect_se)[1]
  p_corr  <- as.numeric(mc$corrected_effect_p)[1]
  b_obs   <- as.numeric(mc$observed_effect)[1]
  se_obs  <- as.numeric(mc$observed_effect_se)[1]
  p_obs   <- as.numeric(mc$observed_effect_p)[1]
  p_diff  <- as.numeric(mc$p_difference)[1]
  n_ivs   <- as.integer(mc$m_IVs)[1]
  ci_l <- if (is.finite(b_corr) && is.finite(se_corr)) b_corr - 1.96 * se_corr else NA
  ci_u <- if (is.finite(b_corr) && is.finite(se_corr)) b_corr + 1.96 * se_corr else NA

  res <- data.frame(
    label=label, exp_id=exp_id, out_id=out_id,
    mrlap_corrected_beta=b_corr, mrlap_corrected_se=se_corr,
    mrlap_corrected_p=p_corr,
    mrlap_corrected_ci_lower=ci_l, mrlap_corrected_ci_upper=ci_u,
    mrlap_observed_beta=b_obs, mrlap_observed_se=se_obs, mrlap_observed_p=p_obs,
    mrlap_p_difference=p_diff, n_ivs=n_ivs,
    stringsAsFactors=FALSE
  )
  message("[", label, "] MRlap 完成: corrected_beta=", round(b_corr,5),
          " (p=", signif(p_corr,3), "), observed_beta=", round(b_obs,5),
          " (p=", signif(p_obs,3), "), p_diff=", signif(p_diff,3))
  return(res)
}

# ============================================================
# CAUSE
# ============================================================
run_cause_one <- function(exp_id, out_id, label) {
  exp_file <- GWAS_FILES[[exp_id]]
  out_file <- GWAS_FILES[[out_id]]
  if (!file.exists(exp_file) || !file.exists(out_file)) {
    message("[", label, "] GWAS 文件缺失, 跳过。")
    return(NULL)
  }

  message("\n[", label, "] CAUSE 启动 (exp=", exp_id, ", out=", out_id, ")...")

  # 读取 GWAS (确保 rsID 格式, 用 load_gwas_for_overlap)
  e <- tryCatch(load_gwas_for_overlap(exp_id), error=function(e) { message("[",label,"] 读暴露失败: ",conditionMessage(e)); NULL })
  o <- tryCatch(load_gwas_for_overlap(out_id), error=function(e) { message("[",label,"] 读结局失败: ",conditionMessage(e)); NULL })
  if (is.null(e) || is.null(o)) return(NULL)

  # 规整为 cause::gwas_merge 默认列
  e <- data.frame(snp=e$SNP, beta_hat=e$beta, se=e$se, A1=e$A1, A2=e$A2, stringsAsFactors=FALSE)
  o <- data.frame(snp=o$SNP, beta_hat=o$beta, se=o$se, A1=o$A1, A2=o$A2, stringsAsFactors=FALSE)

  # 1) gwas_merge
  X <- tryCatch(
    cause::gwas_merge(e, o,
                      snp_name_cols=c("snp","snp"),
                      beta_hat_cols=c("beta_hat","beta_hat"),
                      se_cols=c("se","se"),
                      A1_cols=c("A1","A1"),
                      A2_cols=c("A2","A2"),
                      compute_pvals=TRUE),
    error=function(e2) { message("[",label,"] gwas_merge 失败: ",conditionMessage(e2)); NULL }
  )
  if (is.null(X)) return(NULL)
  message("[", label, "] gwas_merge 完成: ", nrow(X), " SNPs")

  # 2) est_cause_params (参数名: variants, 非 varlist)
  varlist <- tryCatch({
    s <- X$snp
    ns <- if (length(s) > 500000) 500000 else length(s)
    if (length(s) > ns) sample(s, ns) else s
  }, error=function(e2) NULL)
  params <- tryCatch(
    cause::est_cause_params(X, variants=varlist),
    error=function(e2) { message("[",label,"] est_cause_params 失败: ",conditionMessage(e2)); NULL }
  )
  if (is.null(params)) return(NULL)
  message("[", label, "] est_cause_params 完成")

  # 3) 变体选择: p<1e-3 阈值过滤 (CAUSE 推荐) + LD 修剪 (若可用)
  variants <- tryCatch({
    if (!is.null(X$p1)) {
      v <- X$snp[which(X$p1 < 1e-3)]
      message("[", label, "] p<1e-3 过滤后变体数: ", length(v))
      if (length(v) > 50000) {
        v <- sample(v, 50000)
        message("[", label, "] 随机降采样至 50k")
      }
      v
    } else {
      message("[", label, "] 无 p1 列, 退回 500k 子集")
      varlist
    }
  }, error=function(e2) {
    message("[", label, "] 变体选择失败, 退回 500k 子集: ", conditionMessage(e2))
    varlist
  })
  message("[", label, "] 最终变体数: ", length(variants))

  # 4) cause: 区分"共享因果变异" vs "水平多效性"
  # force=TRUE: 跳过 p>0.01 安全检查 (已用 p<1e-3 阈值过滤变体)
  fit <- tryCatch(
    cause::cause(X=X, variants=variants, param_ests=params, force=TRUE),
    error=function(e2) { message("[",label,"] cause() 失败: ",conditionMessage(e2)); NULL }
  )
  if (is.null(fit)) return(NULL)

  # 5) 结构化输出
  summ <- tryCatch(summary(fit), error=function(e2) NULL)
  elpd <- tryCatch(fit$elpd, error=function(e2) NULL)
  causal_p <- NA_real_
  if (!is.null(summ) && !is.null(summ$p.value)) causal_p <- as.numeric(summ$p.value)
  if (is.na(causal_p) && !is.null(elpd) && "z" %in% names(elpd) && is.finite(elpd$z[1])) {
    causal_p <- 2 * pnorm(-abs(elpd$z[1]))
  }
  decision <- if (is.na(causal_p)) {
    "UNKNOWN"
  } else if (causal_p < 0.05) {
    "CAUSAL (因果模型显著优于共享/多效模型)"
  } else {
    "PLEIOTROPY_OR_SHARING (表观效应可由共享遗传架构/水平多效解释)"
  }

  res <- data.frame(
    label=label, exp_id=exp_id, out_id=out_id,
    cause_causal_p=causal_p,
    cause_decision=decision,
    cause_elpd_z=if(!is.null(elpd)&&"z"%in%names(elpd)) as.numeric(elpd$z[1]) else NA,
    cause_n_variants=length(variants),
    stringsAsFactors=FALSE
  )
  message("[", label, "] CAUSE 完成: causal_p=", signif(causal_p,3),
          " decision=", decision)
  return(res)
}

# ============================================================
# 主执行
# ============================================================
message("\n========================================")
message("  MRlap + CAUSE 重叠校正补跑")
message("========================================\n")

# ---- MRlap ----
mrlap_results <- list()
for (cmb in COMBOS) {
  r <- run_mrlap_one(cmb$exp, cmb$out, cmb$label)
  if (!is.null(r)) mrlap_results[[cmb$label]] <- r
}
if (length(mrlap_results) > 0) {
  mrlap_df <- do.call(rbind, mrlap_results)
  write.csv(mrlap_df, file.path(DIR_RES, "G1_mrlap.csv"), row.names=FALSE)
  message("\n=== MRlap 结果已保存: ", file.path(DIR_RES, "G1_mrlap.csv"), " ===")
  print(mrlap_df)
} else {
  message("\n=== MRlap: 无成功结果 ===")
  mrlap_df <- NULL
}

# ---- CAUSE ----
cause_results <- list()
for (cmb in COMBOS) {
  r <- run_cause_one(cmb$exp, cmb$out, cmb$cause_label)
  if (!is.null(r)) cause_results[[cmb$cause_label]] <- r
}
if (length(cause_results) > 0) {
  cause_df <- do.call(rbind, cause_results)
  write.csv(cause_df, file.path(DIR_RES, "G1_cause.csv"), row.names=FALSE)
  message("\n=== CAUSE 结果已保存: ", file.path(DIR_RES, "G1_cause.csv"), " ===")
  print(cause_df)
} else {
  message("\n=== CAUSE: 无成功结果 ===")
  cause_df <- NULL
}

# ---- 更新 G1_bidirectional.rds ----
rds_path <- file.path(DIR_RES, "G1_bidirectional.rds")
if (file.exists(rds_path)) {
  dat <- readRDS(rds_path)
  dat$mrlap_fwd      <- if(!is.null(mrlap_results[["mrlap_fwd"]]))      mrlap_results[["mrlap_fwd"]]      else dat$mrlap_fwd
  dat$mrlap_rev      <- if(!is.null(mrlap_results[["mrlap_rev"]]))      mrlap_results[["mrlap_rev"]]      else dat$mrlap_rev
  dat$mrlap_rep_fwd  <- if(!is.null(mrlap_results[["mrlap_rep_fwd"]]))  mrlap_results[["mrlap_rep_fwd"]]  else dat$mrlap_rep_fwd
  dat$mrlap_rep_rev  <- if(!is.null(mrlap_results[["mrlap_rep_rev"]]))  mrlap_results[["mrlap_rep_rev"]]  else dat$mrlap_rep_rev
  dat$cause_fwd      <- if(!is.null(cause_results[["cause_fwd"]]))      cause_results[["cause_fwd"]]      else dat$cause_fwd
  dat$cause_rev      <- if(!is.null(cause_results[["cause_rev"]]))      cause_results[["cause_rev"]]      else dat$cause_rev
  dat$cause_rep_fwd  <- if(!is.null(cause_results[["cause_rep_fwd"]]))  cause_results[["cause_rep_fwd"]]  else dat$cause_rep_fwd
  dat$cause_rep_rev  <- if(!is.null(cause_results[["cause_rep_rev"]]))  cause_results[["cause_rep_rev"]]  else dat$cause_rep_rev
  dat$overlap_correction_run <- !is.null(mrlap_df) || !is.null(cause_df)
  saveRDS(dat, rds_path)
  message("\n=== G1_bidirectional.rds 已更新 (overlap_correction_run=", dat$overlap_correction_run, ") ===")
}

message("\n========================================")
message("  重叠校正补跑完成")
message("========================================\n")
