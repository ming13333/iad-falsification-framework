# =====================================================================
# 07_education_phewas_mr.R  --  F: 教育 PheWAS-MR (教育保护谱)
# ---------------------------------------------------------------------
# 用教育年限 (ieu-a-1239, Lee 2018) 做暴露, 扫描多种神经退行性疾病:
#   - AD (Kunkle/IGAP + Bellenguez)
#   - Parkinson's disease (Nalls 2019)
#   - ALS (van Rheenen 2016)
#   - Multiple sclerosis (IMSGC 2019)
#   - FTD / LBD (若有 IEU ID)
# 每个结局: IVW + Egger + weighted median/mode + 异质性 + 多效性 + 留一 + Steiger
# 输出: 教育 -> 每种疾病 的 MR 估计表 (education protection spectrum)
#
# 运行(需 VPN + 禁用沙箱):
#   Rscript 07_education_phewas_mr.R
# =====================================================================
suppressMessages({ library(TwoSampleMR); library(ieugwasr); library(dplyr) })
set.seed(20260801)   # 审计#5: 统一随机种子约定

## ---- 配置 ----
EDU_ID  <- "ieu-a-1239"   # Lee et al. 2018, college completion
G_F_OUT <- "C:/Temp/iad_g1/results/Education_PheWAS"
dir.create(G_F_OUT, showWarnings = FALSE, recursive = TRUE)
THRESH  <- list(clump_r2 = 0.001, clump_kb = 10000, p1 = 5e-8)
BATCH_SIZE <- 20

logmsg <- function(...) message("[EduPheWAS] ", ..., " (", format(Sys.time(), "%H:%M:%S"), ")")

## ---- 神经退行性疾病结局 ID 列表 ----
outcomes <- list(
  list(id = "ieu-b-2",             name = "AD_Kunkle",     group = "Dementia"),
  list(id = "ebi-a-GCST90027158",  name = "AD_Bellenguez", group = "Dementia"),
  list(id = "ieu-a-297",           name = "PD_Nalls2019",  group = "Parkinson"),
  list(id = "ebi-a-GCST90012806",  name = "ALS_vanRheenen",group = "ALS"),
  list(id = "ieu-b-18",            name = "MS_IMSGC",      group = "MS"),
  # 尝试更多 (若 ID 不存在会被跳过)
  list(id = "ebi-a-GCST90017035",  name = "PD_alt",        group = "Parkinson"),
  list(id = "ieu-a-72277457",      name = "ALS_alt",       group = "ALS")
)

## ---- 批量提取结局关联 ----
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

## ---- 完整 MR 套件 ----
run_mr_suite <- function(d, label) {
  if (is.null(d) || nrow(d) == 0) return(NULL)
  n_iv <- nrow(d)
  logmsg(label, ": n_iv=", n_iv)

  result <- list(label=label, n_iv=n_iv)
  # 默认值
  result$b_ivw <- NA; result$se_ivw <- NA; result$p_ivw <- NA
  result$b_egger <- NA; result$p_egger <- NA
  result$b_wmed <- NA; result$p_wmed <- NA
  result$b_wmode <- NA; result$p_wmode <- NA
  result$Q_ivw <- NA; result$Q_p_ivw <- NA
  result$egger_intercept <- NA; result$egger_intercept_p <- NA
  result$loo_min_p <- NA; result$loo_max_p <- NA
  result$steiger_dir <- NA
  result$median_F <- NA

  # 方法名映射
  method_map <- c(
    "Inverse variance weighted" = "ivw",
    "MR Egger" = "egger",
    "Weighted median" = "wmed",
    "Weighted mode" = "wmode"
  )

  # 多方法 MR
  methods <- c("mr_ivw", "mr_weighted_median", "mr_weighted_mode")
  if (n_iv >= 3) methods <- c("mr_egger_regression", methods)
  mr_res <- tryCatch(mr(d, method_list=methods), error=function(e) {
    logmsg("mr err, trying IVW only: ", conditionMessage(e))
    tryCatch(mr(d, method_list="mr_ivw"), error=function(e2) {
      logmsg("mr IVW-only also err: ", conditionMessage(e2)); NULL }) })
  if (!is.null(mr_res) && nrow(mr_res) > 0) {
    result$mr_all <- mr_res
    for (m in unique(mr_res$method)) {
      row <- mr_res[mr_res$method == m, ][1, ]
      key <- method_map[m]
      if (is.na(key)) key <- gsub(" ", "_", tolower(m))
      result[[paste0("b_", key)]] <- suppressWarnings(signif(as.numeric(row$b), 4))
      result[[paste0("se_", key)]] <- suppressWarnings(signif(as.numeric(row$se), 4))
      result[[paste0("p_", key)]] <- suppressWarnings(signif(as.numeric(row$pval), 4))
    }
  }

  # 异质性
  if (n_iv >= 2) {
    het <- tryCatch(mr_heterogeneity(d, method_list=c("mr_egger_regression", "mr_ivw")),
                    error=function(e) NULL)
    if (!is.null(het) && nrow(het) > 0) {
      result$heterogeneity <- het
      ivw_het <- het[grepl("Inverse variance|IVW", het$method), ]
      if (nrow(ivw_het) > 0) {
        result$Q_ivw <- signif(ivw_het$Q, 4)
        result$Q_p_ivw <- signif(ivw_het$Q_pval, 4)
      }
    }
  }

  # 多效性 (Egger intercept)
  if (n_iv >= 3) {
    pleio <- tryCatch(mr_pleiotropy_test(d), error=function(e) NULL)
    if (!is.null(pleio) && nrow(pleio) > 0) {
      result$pleiotropy <- pleio
      result$egger_intercept <- signif(pleio$egger_intercept[1], 4)
      result$egger_intercept_p <- signif(pleio$pval[1], 4)
    }
  } else {
    result$egger_intercept <- NA; result$egger_intercept_p <- NA
  }

  # 留一法
  if (n_iv >= 2) {
    loo <- tryCatch(mr_leaveoneout(d), error=function(e) NULL)
    if (!is.null(loo) && nrow(loo) > 0) {
      result$loo <- loo
      loo_ivw <- if ("method" %in% names(loo)) loo[grepl("Inverse variance|IVW", loo$method), ] else loo
      if (nrow(loo_ivw) > 0) {
        result$loo_min_p <- signif(min(loo_ivw$p, na.rm=TRUE), 4)
        result$loo_max_p <- signif(max(loo_ivw$p, na.rm=TRUE), 4)
      }
    }
  }

  # Steiger 方向性
  has_eaf_exp <- !is.null(d$eaf.exposure) && any(!is.na(d$eaf.exposure))
  has_eaf_out <- !is.null(d$eaf.outcome) && any(!is.na(d$eaf.outcome))
  if (has_eaf_exp && has_eaf_out && n_iv >= 2) {
    steiger <- tryCatch(directionality_test(d), error=function(e) NULL)
    if (!is.null(steiger) && nrow(steiger) > 0) {
      result$steiger <- steiger
      result$steiger_dir <- steiger$steiger_dir[1]
    }
  } else { result$steiger_dir <- NA }

  # F 统计量
  f_per <- (d$beta.exposure / d$se.exposure)^2
  result$median_F <- round(median(f_per, na.rm=TRUE), 1)

  result
}

## =====================================================================
## 主分析: 教育 -> 每种神经退行性疾病
## =====================================================================
logmsg("提取教育 IV (", EDU_ID, ")...")
edu_exp <- tryCatch(extract_instruments(EDU_ID, p1=THRESH$p1, r2=THRESH$clump_r2, kb=THRESH$clump_kb),
                    error=function(e) { logmsg("edu exp err: ", conditionMessage(e)); NULL })
if (is.null(edu_exp) || nrow(edu_exp) == 0) stop("[EduPheWAS] 教育 IV 提取失败")
logmsg("教育 IV: ", nrow(edu_exp), " SNPs, median F=", round(median((edu_exp$beta.exposure/edu_exp$se.exposure)^2), 1))

edu_snps <- edu_exp$SNP

all_results <- list()
for (o in outcomes) {
  logmsg("===== 结局: ", o$name, " (", o$id, ") =====")
  out_data <- tryCatch(extract_outcome_data_batched(snps=edu_snps, outcomes=o$id),
                       error=function(e) { logmsg("outcome err: ", conditionMessage(e)); NULL })
  if (is.null(out_data) || nrow(out_data) == 0) {
    logmsg(o$name, ": 无结局数据, 跳过")
    all_results[[o$name]] <- list(id=o$id, name=o$name, group=o$group, error="no outcome data")
    next
  }
  logmsg(o$name, ": 获得关联 ", nrow(out_data), "/", length(edu_snps), " SNPs")

  d <- tryCatch(harmonise_data(edu_exp, out_data), error=function(e) {
    logmsg("harm err: ", conditionMessage(e)); NULL })
  if (is.null(d) || nrow(d) < 2) {
    logmsg(o$name, ": harmonise 失败 (n=", if(is.data.frame(d)) nrow(d) else "NULL", ")")
    all_results[[o$name]] <- list(id=o$id, name=o$name, group=o$group, error="harmonise failed")
    next
  }

  suite <- run_mr_suite(d, o$name)
  if (is.null(suite)) {
    all_results[[o$name]] <- list(id=o$id, name=o$name, group=o$group, error="MR suite failed")
    next
  }

  all_results[[o$name]] <- c(list(id=o$id, name=o$name, group=o$group), suite)

  # 保存明细
  if (!is.null(suite$mr_all))
    write.csv(suite$mr_all, file.path(G_F_OUT, paste0("phewas_mr_", o$name, ".csv")), row.names=FALSE)
  if (!is.null(suite$heterogeneity))
    write.csv(suite$heterogeneity, file.path(G_F_OUT, paste0("phewas_het_", o$name, ".csv")), row.names=FALSE)
  if (!is.null(suite$pleiotropy))
    write.csv(suite$pleiotropy, file.path(G_F_OUT, paste0("phewas_pleio_", o$name, ".csv")), row.names=FALSE)
  if (!is.null(suite$loo))
    write.csv(suite$loo, file.path(G_F_OUT, paste0("phewas_loo_", o$name, ".csv")), row.names=FALSE)

  logmsg(o$name, ": IVW b=", suite$b_ivw, " p=", suite$p_ivw,
         " | Egger b=", suite$b_egger,
         " p=", suite$p_egger,
         " | int p=", suite$egger_intercept_p, " | Q p=", suite$Q_p_ivw,
         " | Steiger=", suite$steiger_dir)
}

## ---- 汇总表 ----
summary_rows <- list()
for (nm in names(all_results)) {
  r <- all_results[[nm]]
  if (!is.null(r$error)) {
    summary_rows[[nm]] <- data.frame(
      outcome=r$name, group=r$group, id=r$id, n_iv=NA,
      b_ivw=NA, se_ivw=NA, p_ivw=NA,
      b_egger=NA, p_egger=NA, egger_int=NA, egger_int_p=NA,
      b_wmed=NA, p_wmed=NA, b_wmode=NA, p_wmode=NA,
      Q_p=NA, loo_min_p=NA, loo_max_p=NA, median_F=NA, steiger=NA,
      error=r$error, stringsAsFactors=FALSE)
  } else {
    summary_rows[[nm]] <- data.frame(
      outcome=r$name, group=r$group, id=r$id, n_iv=r$n_iv,
      b_ivw=r$b_ivw, se_ivw=r$se_ivw, p_ivw=r$p_ivw,
      b_egger=r$b_egger,
      p_egger=r$p_egger,
      egger_int=r$egger_intercept, egger_int_p=r$egger_intercept_p,
      b_wmed=r$b_wmed,
      p_wmed=r$p_wmed,
      b_wmode=r$b_wmode,
      p_wmode=r$p_wmode,
      Q_p=r$Q_p_ivw, loo_min_p=r$loo_min_p, loo_max_p=r$loo_max_p,
      median_F=r$median_F, steiger=r$steiger_dir,
      error="", stringsAsFactors=FALSE)
  }
}
summary_df <- dplyr::bind_rows(summary_rows) %>%
  mutate(fdr = p.adjust(p_ivw, method="fdr"),
         sig_raw = !is.na(p_ivw) & p_ivw < 0.05,
         sig_fdr = !is.na(fdr) & fdr < 0.05,
         direction = ifelse(!is.na(b_ivw), ifelse(b_ivw < 0, "Protective", "Risk"), NA)) %>%
  arrange(p_ivw)

write.csv(summary_df, file.path(G_F_OUT, "Education_PheWAS_summary.csv"), row.names=FALSE)
saveRDS(all_results, file.path(G_F_OUT, "Education_PheWAS_full.rds"))

## ---- 打印汇总 ----
logmsg("=== 教育保护谱汇总 ===")
logmsg("结局数: ", nrow(summary_df), " | 显著(raw p<0.05): ", sum(summary_df$sig_raw, na.rm=TRUE),
       " | 显著(FDR<0.05): ", sum(summary_df$sig_fdr, na.rm=TRUE))
for (i in seq_len(nrow(summary_df))) {
  r <- summary_df[i, ]
  if (!is.na(r$error) && r$error != "") {
    logmsg(r$outcome, ": ERROR - ", r$error)
  } else {
    logmsg(r$outcome, " (", r$group, "): b=", r$b_ivw, " p=", r$p_ivw,
           " FDR=", r$fdr, " dir=", r$direction,
           " n=", r$n_iv, " F=", r$median_F,
           " | Egger int p=", r$egger_int_p, " | Q p=", r$Q_p,
           " | Steiger=", r$steiger, " | LOO [", r$loo_min_p, "-", r$loo_max_p, "]")
  }
}
logmsg("结果保存至: ", G_F_OUT)
logmsg("Done.")
