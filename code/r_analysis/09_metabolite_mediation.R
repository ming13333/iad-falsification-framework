# !/usr/bin/env Rscript
# ============================================================
# C1 pivot: -> -> AD MR
# ------------------------------------------------------------
# : UKB-PPP IEU , Synapse .
# IEU met-d- 2020, n=115078, IV
# : ieu-b-2 AD Kunkle
# : MR + delta SE + BH-FDR
# ============================================================

suppressMessages(library(TwoSampleMR))
suppressMessages(library(dplyr))

set.seed(20240801)
EDU_ID <- "ieu-a-1239"
AD_ID  <- "ieu-b-2"
OUT    <- "./output/results/MetMediation"
dir.create(OUT, showWarnings=FALSE, recursive=TRUE)

mediators <- c(
  "met-d-Total_C","met-d-LDL_C","met-d-HDL_C","met-d-Total_TG","met-d-non_HDL_C",
  "met-d-Total_PL","met-d-Remnant_C","met-d-Total_FC","met-d-Total_CE",
  "met-d-Ile","met-d-Leu","met-d-Val","met-d-Total_BCAA","met-d-Phe","met-d-Gly",
  "met-d-Tyr","met-d-His","met-d-Gln","met-d-Ala",
  "met-d-DHA","met-d-Omega_3","met-d-Omega_6","met-d-PUFA","met-d-SFA","met-d-MUFA",
  "met-d-Phosphatidylc","met-d-Sphingomyelins","met-d-Cholines","met-d-Total_FA",
  "met-d-GlycA","met-d-Albumin","met-d-Creatinine","met-d-Acetate","met-d-Acetoacetate",
  "met-d-Lactate","met-d-Pyruvate","met-d-Citrate","met-d-Glucose"
)

safe_ivw <- function(harm) {
  tryCatch({
    if (!is.data.frame(harm) || nrow(harm) < 3) return(NULL)
    need <- c("beta.exposure","se.outcome","beta.outcome")
    if (!all(need %in% names(harm))) return(NULL)
    bx <- as.numeric(harm$beta.exposure)
    by <- as.numeric(harm$beta.outcome)
    se_out <- as.numeric(harm$se.outcome)
    valid <- is.finite(bx) & is.finite(by) & is.finite(se_out) & se_out > 0
    if (sum(valid) < 3) return(NULL)
    w <- 1 / (se_out[valid]^2)
    bx <- bx[valid]; by <- by[valid]
    denom <- sum(w * bx^2)
    if (!is.finite(denom) || denom <= 0) return(NULL)
    b <- sum(w * bx * by) / denom
    se <- sqrt(1 / denom)
    if (!is.finite(b) || !is.finite(se) || se <= 0) return(NULL)
    p <- 2 * pnorm(-abs(b / se))
    list(b=signif(b,4), se=signif(se,4), p=signif(p,4), n_snps=length(bx))
  }, error=function(e) NULL)
}

method_map <- c("Inverse variance weighted"="ivw","MR Egger"="egger",
                "Weighted median"="wmed","Weighted mode"="wmode")

cat("=== Step 1: education -> metabolite ===\n")
edu_exp <- tryCatch(extract_instruments(EDU_ID, p1=5e-8, r2=0.001, kb=10000),
                    error=function(e){cat(":",conditionMessage(e),"\n");NULL})
if (is.null(edu_exp)) { cat("ABORT: \n"); quit(status=1) }
cat("  IVs:", nrow(edu_exp), "\n")
step1_rows <- list()
for (m in mediators) {
  cat(sprintf("  [%s] Step1...\n", m))
  res <- tryCatch({
    od <- extract_outcome_data(snps=edu_exp$SNP, outcomes=m)
    if (is.null(od) || nrow(od)==0) { cat("    no outcome data\n"); return(NULL) }
    harm <- harmonise_data(edu_exp, od)
    nr <- nrow(harm)
    if (is.null(harm) || nr < 10) { cat(sprintf("    harm<10 (n=%d)\n", if(is.null(harm)) 0 else nr)); return(NULL) }
    # inline safe IVW
    bx <- as.numeric(harm$beta.exposure)
    by <- as.numeric(harm$beta.outcome)
    se_out <- as.numeric(harm$se.outcome)
    ok <- is.finite(bx) & is.finite(by) & is.finite(se_out) & se_out > 0
    if (sum(ok) < 3) { cat("    <3 valid SNPs\n"); return(NULL) }
    bx <- bx[ok]; by <- by[ok]; se_out <- se_out[ok]
    w <- 1 / se_out^2
    denom <- sum(w * bx^2)
    if (!is.finite(denom) || denom <= 0) { cat("    denom invalid\n"); return(NULL) }
    b <- sum(w * bx * by) / denom
    se_val <- sqrt(1 / denom)
    if (!is.finite(b) || !is.finite(se_val) || se_val <= 0) { cat("    b/se invalid\n"); return(NULL) }
    p <- 2 * pnorm(-abs(b / se_val))
    q_p <- NA_real_
    het <- tryCatch(mr_heterogeneity(harm, method_list="mr_ivw"),
                    error=function(e) NULL)
    if (!is.null(het) && nrow(het) > 0 && "pval" %in% names(het))
      q_p <- suppressWarnings(as.numeric(het$pval[1]))
    data.frame(metab=m, metab_id=m, n_snps=length(bx),
      b1=signif(b,4), se1=signif(se_val,4), p1=signif(p,4), q_p=signif(q_p,3),
      stringsAsFactors=FALSE)
  }, error=function(e){ cat("    ERROR:", conditionMessage(e), "\n"); NULL })
  if (is.null(res)) next
  step1_rows[[m]] <- res
  cat(sprintf("    b1=%.4f p1=%.2g n=%d\n", res$b1, res$p1, res$n_snps))
}
step1_df <- do.call(rbind, step1_rows)
write.csv(step1_df, file.path(OUT,"step1_education_metab.csv"), row.names=FALSE)
cat("Step1 :", nrow(step1_df), "\n")

cat("\n=== Step 2: metabolite -> AD ===\n")
step2_rows <- list()
for (m in step1_df$metab_id) {
  cat(sprintf("  [%s] Step2...", m))
  met_exp <- tryCatch(extract_instruments(m, p1=5e-8, r2=0.001, kb=10000),
                      error=function(e){cat(" inst_err",conditionMessage(e),"\n");NULL})
  if (is.null(met_exp) || nrow(met_exp) < 3) { cat(" <3 IVs\n"); next }
  ad_od <- tryCatch(extract_outcome_data(snps=met_exp$SNP, outcomes=AD_ID),
                    error=function(e){cat(" out_err",conditionMessage(e),"\n");NULL})
  if (is.null(ad_od) || nrow(ad_od)==0) { cat(" no AD overlap\n"); next }
  harm2 <- tryCatch(harmonise_data(met_exp, ad_od), error=function(e) NULL)
  if (is.null(harm2) || nrow(harm2) < 3) { cat(" harm<3\n"); next }
  ivw2 <- safe_ivw(harm2)
  if (is.null(ivw2)) {
    mr_res <- tryCatch(mr(harm2), error=function(e) NULL)
    if (!is.null(mr_res)) {
      r <- mr_res[grepl("Inverse variance", mr_res$method), ]
      if (nrow(r)>0) ivw2 <- data.frame(b=signif(r$b,4),se=signif(r$se,4),
            p=signif(r$pval,4), n_snps=nrow(harm2), stringsAsFactors=FALSE)
    }
  }
  if (is.null(ivw2)) { cat(" ivw NA\n"); next }
  step2_rows[[m]] <- data.frame(metab=m, metab_id=m, n_snps=ivw2$n_snps,
    b2=ivw2$b, se2=ivw2$se, p2=ivw2$p, stringsAsFactors=FALSE)
  cat(sprintf(" b2=%.4f p2=%.2g n=%d\n", ivw2$b, ivw2$p, ivw2$n_snps))
}
step2_df <- do.call(rbind, step2_rows)
write.csv(step2_df, file.path(OUT,"step2_metab_AD.csv"), row.names=FALSE)
cat("Step2 :", nrow(step2_df), "\n")

# ---- delta + BH-FDR
cat("\n=== Mediation (indirect = b1*b2) ===\n")
mg <- merge(step1_df, step2_df, by="metab_id")
mg$indirect <- mg$b1 * mg$b2
mg$se_indirect <- sqrt(mg$b2^2 * mg$se1^2 + mg$b1^2 * mg$se2^2)
mg$z_indirect <- mg$indirect / mg$se_indirect
mg$p_indirect <- 2 * pnorm(-abs(mg$z_indirect))
mg$q_indirect <- p.adjust(mg$p_indirect, method="BH")
mg <- mg[order(mg$p_indirect), ]
write.csv(mg, file.path(OUT,"mediation_education_metab_AD.csv"), row.names=FALSE)
cat("Mediation :", nrow(mg), "\n")
cat("====  (q<0.05) ====\n")
print(mg[mg$q_indirect < 0.05, c("metab","b1","p1","b2","p2","indirect","p_indirect","q_indirect")])
cat("\n[C1 metabolite mediation] DONE\n")