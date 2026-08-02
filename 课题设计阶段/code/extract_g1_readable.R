# =====================================================================
# extract_g1_readable.R  —  从 results/G1_bidirectional.rds 提取 G1 核心数字
# ---------------------------------------------------------------------
# 用法 (PowerShell, 必须在 code/ 目录下):
#   cd C:\D\workbuddy\科研\共病分析\课题设计阶段\code
#   Rscript extract_g1_readable.R
# 输出:
#   results/G1_summary.txt   (人类可读, 直接回传主理人)
#   (G1_mr_table.csv 可选, 结构同 summary)
# 说明: 本脚本只读 RDS, 不联网、不改任何东西。
# =====================================================================
suppressMessages(source("00_config.R"))

rds <- file.path(DIR_OUT, "G1_bidirectional.rds")
if (!file.exists(rds)) {
  stop("未找到 ", rds, "。请先跑 Rscript 01_bidirectional_mr_coloc.R 生成该文件。")
}
G <- readRDS(rds)

out <- c()
cat_line <- function(...) out <<- c(out, paste0(...))

cat_line("============ G1 数字提取 ============")
cat_line("生成时间(本地): ", as.character(Sys.time()))
cat_line("重叠校正(MRlap/CAUSE)是否运行: ", G$overlap_correction_run)
cat_line("======================================")

# ---- 从 run_mr() 返回的 list 提取 IVW / Egger / 中位数 / 众数 + 敏感性 ----
extract_mr <- function(obj, lab) {
  if (is.null(obj) || is.null(obj$res)) {
    cat_line("\n--- ", lab, " ---\n  无结果(提取失败或该段被跳过)")
    return()
  }
  res <- obj$res
  cat_line("\n--- ", lab, " ---")
  cat_line("方法 | beta | se | pval")
  mm <- c("Inverse variance weighted" = "MR IVW",
          "MR Egger"                   = "MR Egger",
          "Weighted median"            = "Weighted median",
          "Weighted mode"              = "Weighted mode")
  for (m in names(mm)) {
    r <- res[res$method == m, ]
    if (nrow(r) == 1) cat_line(sprintf("  %s | %.4f | %.4f | %.3e",
                                        mm[m], r$b, r$se, r$pval))
  }
  if (!is.null(obj$het) && is.data.frame(obj$het)) {
    h <- obj$het
    w <- h[h$method == "Inverse variance weighted", ]
    if (nrow(w) == 1)
      cat_line(sprintf("  Cochran Q(IVW): Q=%.2f, df=%d, p=%.3e", w$Q, w$Q_df, w$Q_pval))
  }
  if (!is.null(obj$pleio) && is.data.frame(obj$pleio)) {
    p <- obj$pleio
    cat_line(sprintf("  Egger 截距: %.4f (se %.4f) p=%.3e", p$egger_intercept, p$se, p$pval))
  }
  cat_line(sprintf("  工具强度 F: 均值=%.1f, 最小=%.1f (合格阈值>10)",
                   obj$f_mean, obj$f_min))
  cat_line("  MR-PRESSO: ", if (is.null(obj$presso)) "未运行(包未装)" else "已运行")
}

extract_mr(G$fwd,     "失眠→AD (主对 ieu-b-2)")
extract_mr(G$rev,     "AD→失眠 (主对 ieu-b-2)")
extract_mr(G$fwd_rep, "失眠→AD (复制 Bellenguez)")
extract_mr(G$rev_rep, "AD→失眠 (复制 Bellenguez)")

# ---- Steiger 方向性 ----
cat_line("\n--- Steiger 方向性检验 ---")
steiger_pp <- function(s, lab) {
  if (is.null(s)) { cat_line("  ", lab, ": 无"); return() }
  if (!is.null(s$cor.exposure) && !is.null(s$cor.outcome)) {
    cat_line(sprintf("  %s: V(exp)=%.3f, V(out)=%.3f, 方向正确(暴露方差>结局)? %s",
                     lab, s$cor.exposure, s$cor.outcome,
                     ifelse(s$cor.exposure > s$cor.outcome, "是", "否")))
  } else cat_line("  ", lab, ": 结构未知, 请检查")
}
steiger_pp(G$steiger_fwd, "失眠→AD")
steiger_pp(G$steiger_rev, "AD→失眠")

# ---- coloc PP.H4 (run_coloc 返回 rbind 后的 data.frame, 含 PP.H4 列) ----
cat_line("\n--- coloc PP.H4 (共享因果变异, >0.80 显著) ---")
coloc_report <- function(cl, lab) {
  if (is.null(cl) || !is.data.frame(cl)) {
    cat_line("  ", lab, ": 无 coloc 结果(可跳过)"); return()
  }
  cat_line(sprintf("  %s: 位点=%d, PP.H4 均值=%.3f, 最大=%.3f, >0.80 位点数=%d",
                   lab, nrow(cl), mean(cl$PP.H4, na.rm = TRUE),
                   max(cl$PP.H4, na.rm = TRUE),
                   sum(cl$PP.H4 > 0.80, na.rm = TRUE)))
}
coloc_report(G$coloc_fwd,     "失眠~AD (主对 正向)")
coloc_report(G$coloc_rev,     "AD~失眠 (主对 反向)")
coloc_report(G$coloc_fwd_rep, "失眠~AD (复制 Bellenguez 正向)")
coloc_report(G$coloc_rev_rep, "AD~失眠 (复制 Bellenguez 反向)")

# ---- 重叠校正标志 ----
cat_line("\n--- 重叠校正 (MRlap / CAUSE) ---")
cat_line("  overlap_correction_run = ", G$overlap_correction_run)
if (isTRUE(G$overlap_correction_run)) {
  cat_line("  MRlap 主fwd: ", ifelse(is.null(G$mrlap_fwd), "NULL", "有"),
           " | CAUSE 主fwd: ", ifelse(is.null(G$cause_fwd), "NULL", "有"),
           " | MRlap 复制fwd: ", ifelse(is.null(G$mrlap_rep_fwd), "NULL", "有"),
           " | CAUSE 复制fwd: ", ifelse(is.null(G$cause_rep_fwd), "NULL", "有"))
} else {
  cat_line("  ⚠️ 重叠校正未运行(未设 LD 面板/全 GWAS 或包未装) — 稿件 Limitations 须披露")
}

writeLines(out, file.path(DIR_OUT, "G1_summary.txt"))
cat("\n[G1] 已写出 results/G1_summary.txt —— 请连同 G1_bidirectional.rds 与 4 个 coloc CSV 一起回传。\n")
