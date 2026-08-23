# =====================================================================
# build_supplementary_tables.R
# CSV/RDS Supplementary Tables S1-S4
# : /Supplementary/ .md + .csv
# =====================================================================
suppressMessages({
  library(data.table); library(dplyr)
})
set.seed(20260802)

OUT_DIR <- "./output/results/Supplementary"
dir.create(OUT_DIR, showWarnings = FALSE, recursive = TRUE)

signif3 <- function(x) ifelse(is.na(x), "NA", formatC(as.numeric(x), digits = 3, format = "g"))
signif4 <- function(x) ifelse(is.na(x), "NA", formatC(as.numeric(x), digits = 4, format = "g"))

# =====================================================================
# =====================================================================
coloc_files <- list(
  c("forward", "main", "./output/results/G1_coloc_forward.csv"),
  c("forward", "replication", "./output/results/G1_coloc_forward_repl.csv"),
  c("reverse", "main", "./output/results/G1_coloc_reverse.csv"),
  c("reverse", "replication", "./output/results/G1_coloc_reverse_repl.csv")
)
s1 <- lapply(coloc_files, function(r) {
  df <- fread(r[3], data.table = FALSE)
  df$direction <- r[1]
  df$dataset <- r[2]
  df
}) %>% bind_rows()
s1$PP.H4_class <- cut(s1$PP.H4, breaks = c(-Inf, 0.5, 0.8, Inf),
                      labels = c("weak(<0.5)", "moderate(0.5-0.8)", "strong(>=0.8)"))
s1 <- s1 %>% select(direction, dataset, lead_snp, chr, pos, n_snps, PP.H0, PP.H1, PP.H2, PP.H3, PP.H4, PP.H4_class)
write.csv(s1, file.path(OUT_DIR, "S1_coloc_loci.csv"), row.names = FALSE)

cat("S1 rows:", nrow(s1), "\n")

# =====================================================================
# S2. G1 MR + UVMR clump
# =====================================================================
g1 <- readRDS("./output/results/G1_bidirectional.rds")

extract_mr_summary <- function(obj, label, n_iv_override = NA) {
  if (is.null(obj)) return(NULL)
  res <- obj$res
  het <- obj$het
  pleio <- obj$pleiotropy
  out <- data.frame(
    analysis = label,
    n_snps = ifelse(is.na(n_iv_override), nrow(obj$dat), n_iv_override),
    F_mean = obj$f_mean,
    F_min = obj$f_min,
    b_ivw = NA_real_, se_ivw = NA_real_, p_ivw = NA_real_,
    b_egger = NA_real_, p_egger = NA_real_,
    b_wmed = NA_real_, p_wmed = NA_real_,
    b_wmode = NA_real_, p_wmode = NA_real_,
    Q_ivw = NA_real_, Q_p_ivw = NA_real_,
    egger_intercept = NA_real_, egger_intercept_p = NA_real_,
    stringsAsFactors = FALSE
  )
  if (!is.null(res)) {
    for (m in c("Inverse variance weighted", "MR Egger", "Weighted median", "Weighted mode")) {
      row <- res[res$method == m, ]
      if (nrow(row) > 0) {
        key <- switch(m,
                      "Inverse variance weighted" = "ivw",
                      "MR Egger" = "egger",
                      "Weighted median" = "wmed",
                      "Weighted mode" = "wmode")
        out[[paste0("b_", key)]] <- row$b[1]
        out[[paste0("se_", key)]] <- row$se[1]
        out[[paste0("p_", key)]] <- row$pval[1]
      }
    }
  }
  if (!is.null(het)) {
    qrow <- het[grepl("Inverse variance|IVW", het$method, ignore.case = TRUE), ]
    if (nrow(qrow) > 0) { out$Q_ivw <- qrow$Q[1]; out$Q_p_ivw <- qrow$Q_pval[1] }
  }
  if (!is.null(pleio) && nrow(pleio) > 0) {
    out$egger_intercept <- pleio$egger_intercept[1]
    out$egger_intercept_p <- pleio$pval[1]
  }
  out
}

s2_list <- list(
  extract_mr_summary(g1$fwd, "G1  -> AD (unclumped)"),
  extract_mr_summary(g1$rev, "G1 AD ->  (unclumped)"),
  extract_mr_summary(g1$fwd_rep, "G1  -> AD (replication, unclumped)"),
  extract_mr_summary(g1$rev_rep, "G1 AD ->  (replication, unclumped)")
)

# UVMR instrument-set sensitivity from MVMR_results_v3 IVW only
mvmr <- fread("./output/results/MVMR/MVMR_results_v3.csv", data.table = FALSE)
uv <- mvmr[mvmr$model == "UVMR_insomnia", c("instrument_set", "n_snps", "b", "se", "p")]
uv$analysis <- paste0("UVMR  -> AD (", uv$instrument_set, ")")
uv$F_mean <- NA_real_; uv$F_min <- NA_real_
uv$b_ivw <- uv$b; uv$se_ivw <- uv$se; uv$p_ivw <- uv$p
for (c in c("b_egger", "p_egger", "b_wmed", "p_wmed", "b_wmode", "p_wmode", "Q_ivw", "Q_p_ivw", "egger_intercept", "egger_intercept_p")) {
  if (!c %in% names(uv)) uv[[c]] <- NA_real_
}
uv <- uv[, c("analysis", "n_snps", "F_mean", "F_min", "b_ivw", "se_ivw", "p_ivw",
             "b_egger", "p_egger", "b_wmed", "p_wmed", "b_wmode", "p_wmode",
             "Q_ivw", "Q_p_ivw", "egger_intercept", "egger_intercept_p")]
s2 <- bind_rows(lapply(s2_list, function(x) x), uv)
write.csv(s2, file.path(OUT_DIR, "S2_instrument_sensitivity.csv"), row.names = FALSE)
cat("S2 rows:", nrow(s2), "\n")

# =====================================================================
# =====================================================================
s3 <- mvmr %>% mutate(
  b_fmt = signif3(b),
  se_fmt = signif3(se),
  p_fmt = signif3(p),
  note = case_when(
    model == "UVMR_insomnia" ~ "Univariable MR of insomnia on AD across instrument sets",
    model == "MVMR_full" ~ "Multivariable MR with insomnia + LDL + depression + education",
    model == "MVMR_no_edu" ~ "Multivariable MR excluding education",
    TRUE ~ ""
  )
)
write.csv(s3, file.path(OUT_DIR, "S3_MVMR_complete.csv"), row.names = FALSE)
cat("S3 rows:", nrow(s3), "\n")

# =====================================================================
# =====================================================================
sum <- fread("./output/results/Education_PheWAS/phewas_summary.csv", data.table = FALSE)
s4 <- sum %>% select(-b_egger, -p_egger)

enrich <- function(prefix) {
  mr_f <- paste0("./output/results/Education_PheWAS/phewas_mr_", prefix, ".csv")
  het_f <- paste0("./output/results/Education_PheWAS/phewas_het_", prefix, ".csv")
  pleio_f <- paste0("./output/results/Education_PheWAS/phewas_pleio_", prefix, ".csv")
  if (!all(file.exists(c(mr_f, het_f, pleio_f)))) return(NULL)
  mr <- fread(mr_f, data.table = FALSE)
  het <- fread(het_f, data.table = FALSE)
  pleio <- fread(pleio_f, data.table = FALSE)
  out <- data.frame(outcome = prefix, stringsAsFactors = FALSE)
  key_map <- c("Weighted median" = "wmed", "Weighted mode" = "wmode")
  for (m in names(key_map)) {
    row <- mr[mr$method == m, ]
    key <- key_map[m]
    out[[paste0("b_", key)]] <- if (nrow(row) > 0) row$b[1] else NA_real_
    out[[paste0("p_", key)]] <- if (nrow(row) > 0) row$pval[1] else NA_real_
  }
  row <- mr[mr$method == "MR Egger", ]
  out$b_egger <- if (nrow(row) > 0) row$b[1] else NA_real_
  out$p_egger <- if (nrow(row) > 0) row$pval[1] else NA_real_
  qrow <- het[grepl("Inverse variance|IVW", het$method, ignore.case = TRUE), ]
  out$Q_ivw <- if (nrow(qrow) > 0) qrow$Q[1] else NA_real_
  out$Q_p_ivw <- if (nrow(qrow) > 0) qrow$Q_pval[1] else NA_real_
  out$egger_intercept_p <- if (nrow(pleio) > 0) pleio$pval[1] else NA_real_
  out
}

s4_enrich <- bind_rows(lapply(sum$outcome, enrich))
s4 <- left_join(s4, s4_enrich, by = "outcome")
s4 <- s4 %>% select(outcome, group, id, n_iv, b_ivw, se_ivw, p_ivw,
                    b_wmed, p_wmed, b_wmode, p_wmode, b_egger, p_egger,
                    Q_ivw, Q_p_ivw, egger_intercept_p, direction, note)
write.csv(s4, file.path(OUT_DIR, "S4_education_PheWAS.csv"), row.names = FALSE)
cat("S4 rows:", nrow(s4), "\n")

# =====================================================================
# Markdown wrappers compact tables with footnotes
# =====================================================================
md_header <- function(title, note) {
  paste0("# ", title, "\n\n", note, "\n\n")
}

df_to_md <- function(df) {
  cols <- names(df)
  header <- paste0("| ", paste(cols, collapse = " | "), " |")
  sep <- paste0("|", paste(rep("---|", length(cols)), collapse = ""))
  rows <- apply(df, 1, function(r) paste0("| ", paste(as.character(r), collapse = " | "), " |"))
  paste(c(header, sep, rows), collapse = "\n")
}

s1_md <- s1
s1_md[, 7:11] <- lapply(s1_md[, 7:11], signif3)
writeLines(paste0(
  md_header("Supplementary Table 1. Colocalisation loci (insomnia and AD)",
            "PP.H4 >= 0.8 considered strong evidence of shared causal variant. Forward = insomnia lead SNP vs AD window; Reverse = AD lead SNP vs insomnia window. Replication dataset = Bellenguez 2022 AD."),
  df_to_md(s1_md)
), file.path(OUT_DIR, "S1_coloc_loci.md"))

s2_md <- s2
for (c in c("F_mean", "F_min", "b_ivw", "se_ivw", "p_ivw", "b_egger", "p_egger", "b_wmed", "p_wmed", "b_wmode", "p_wmode", "Q_ivw", "Q_p_ivw", "egger_intercept", "egger_intercept_p")) {
  s2_md[[c]] <- signif3(s2_md[[c]])
}
writeLines(paste0(
  md_header("Supplementary Table 2. Instrument-set sensitivity for insomnia -> AD",
            "Unclumped G1 analysis reports full multi-method MR (IVW / MR-Egger / weighted median / weighted mode) plus Cochran's Q and MR-Egger intercept. UVMR rows from MVMR instrument-set sensitivity report IVW only for unclumped/clumped-loose/clumped-tight sets; Egger/WMed/WMode were not run for clumped subsets (NA)."),
  df_to_md(s2_md)
), file.path(OUT_DIR, "S2_instrument_sensitivity.md"))

s3_md <- s3 %>% select(model, instrument_set, data_source, n_snps, exposure, method, b_fmt, se_fmt, p_fmt, condF, note)
names(s3_md)[7:9] <- c("b", "se", "p")
writeLines(paste0(
  md_header("Supplementary Table 3. Multivariable MR (MVMR) and UVMR sensitivity results",
            "condF = conditional F-statistic for the exposure in the MVMR model (NA for UVMR rows and when not computable)."),
  df_to_md(s3_md)
), file.path(OUT_DIR, "S3_MVMR_complete.md"))

s4_md <- s4
for (c in c("n_iv", "b_ivw", "se_ivw", "p_ivw", "b_wmed", "p_wmed", "b_wmode", "p_wmode", "b_egger", "p_egger", "Q_ivw", "Q_p_ivw", "egger_intercept_p")) {
  s4_md[[c]] <- signif3(s4_md[[c]])
}
writeLines(paste0(
  md_header("Supplementary Table 4. Educational attainment PheWAS against neurodegenerative outcomes",
            "Education instruments = ieu-a-1239. Q_p_ivw = Cochran's Q p-value for IVW; egger_intercept_p = MR-Egger intercept p-value."),
  df_to_md(s4_md)
), file.path(OUT_DIR, "S4_education_PheWAS.md"))

cat("Supplementary tables written to", OUT_DIR, "\n")