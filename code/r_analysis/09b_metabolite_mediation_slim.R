# !/usr/bin/env Rscript
# ============================================================
# 09b_metabolite_mediation_slim.R
# #2/#5: set.seed + Step1/Step2 F
# ============================================================
suppressMessages(library(TwoSampleMR))
set.seed(20260801)   # #5: (, )
BOOT_N <- 5000

# bootstrap ref: 02b_g2_enhanced.R bootstrap_mediation
# Step1edu->metab Step2metab->AD , => b1,b2
bootstrap_mediation <- function(b1, se1, b2, se2, n_boot=BOOT_N, seed=42) {
  set.seed(seed)
  boots <- numeric(n_boot)
  for (i in seq_len(n_boot)) {
    b1_b <- rnorm(1, mean=b1, sd=se1)
    b2_b <- rnorm(1, mean=b2, sd=se2)
    boots[i] <- b1_b * b2_b
  }
  list(
    boot_ci_lower = quantile(boots, 0.025),
    boot_ci_upper = quantile(boots, 0.975),
    boot_p = 2 * min(mean(boots > 0), mean(boots < 0))
  )
}
EDU_ID <- "ieu-a-1239"
AD_ID  <- "ieu-b-2"
OUT    <- "./output/results/MetMediation"
dir.create(OUT, showWarnings=FALSE, recursive=TRUE)

cat("\n===== C1 SLIM: 10 key metabolites (with instrument F-stat) =====\n\n")

mets <- c(
  "met-d-Total_C", "met-d-LDL_C", "met-d-HDL_C", "met-d-Total_TG",
  "met-d-DHA", "met-d-Omega_3",
  "met-d-Ile", "met-d-Leu", "met-d-Val",
  "met-d-GlycA"
)

cat("=== Extract education instruments ===\n")
edu <- extract_instruments(EDU_ID, p1=5e-8, r2=0.001, kb=10000)
cat("edu SNPs:", nrow(edu), "\n\n")

mk_df <- function(met_id, b1, se1, p1, n1, b2, se2, p2, n2,
                  indirect, se_ind, p_ind, f1_med, f2_med,
                  boot_ci_lower, boot_ci_upper, boot_p) {
  sig <- function(x) if (is.na(x)) NA else signif(x, 4)
  data.frame(met=met_id,
             b1=sig(b1), se1=sig(se1), p1=sig(p1), n1=n1,
             b2=sig(b2), se2=sig(se2), p2=sig(p2), n2=n2,
             indirect=sig(indirect), se_ind=sig(se_ind), p_ind=sig(p_ind),
             boot_ci_lower=sig(boot_ci_lower),
             boot_ci_upper=sig(boot_ci_upper),
             boot_p=sig(boot_p),
             f1_med=if(is.na(f1_med)) NA else signif(f1_med,3),
             f2_med=if(is.na(f2_med)) NA else signif(f2_med,3),
             stringsAsFactors=FALSE)
}

run_one <- function(met_id) {
  tryCatch({
    # Step 1: edu -> metab
    od <- extract_outcome_data(snps=edu$SNP, outcomes=met_id)
    if(nrow(od)==0) return(NULL)
    harm <- harmonise_data(edu, od)
    if(nrow(harm) < 10) return(NULL)
    bx <- as.numeric(harm$beta.exposure)
    by <- as.numeric(harm$beta.outcome)
    so <- as.numeric(harm$se.outcome)
    ok <- is.finite(bx)&is.finite(by)&is.finite(so)&so>0
    if(sum(ok)<3) return(NULL)
    bx<-bx[ok];by<-by[ok];so<-so[ok]
    # F Step1 =: F=beta/se^2
    f1 <- (harm$beta.exposure[ok]/harm$se.exposure[ok])^2
    f1_med <- median(f1, na.rm=TRUE)
    w<-1/so^2;denom<-sum(w*bx^2)
    if(!is.finite(denom)||denom<=0) return(NULL)
    b1<-sum(w*bx*by)/denom; se1<-sqrt(1/denom)
    if(!is.finite(b1)||!is.finite(se1)) return(NULL)
    p1<-2*pnorm(-abs(b1/se1))
    n1<-length(bx)
    cat(sprintf("  [%s] edu->metab: b=%.4f p=%.2g n=%d Fmed=%.1f\n", met_id, b1, p1, n1, f1_med))

    f2_med <- NA_real_
    # Step 2: metab -> AD
    met_instr <- tryCatch(extract_instruments(met_id, p1=5e-8, r2=0.001, kb=10000),
                          error=function(e)NULL)
    if(is.null(met_instr)||nrow(met_instr)<3) {
      cat(sprintf("    metab->AD: <3 IVs (n=%d) -> weak instrument\n",
                  if(is.null(met_instr)) 0 else nrow(met_instr)))
      return(mk_df(met_id,b1,se1,p1,n1,NA,NA,NA,NA,NA,NA,NA,f1_med,f2_med,NA,NA,NA))
    }
    ad_od <- extract_outcome_data(snps=met_instr$SNP, outcomes=AD_ID)
    if(is.null(ad_od)||nrow(ad_od)==0) {
      cat("    metab->AD: no AD overlap\n")
      return(mk_df(met_id,b1,se1,p1,n1,NA,NA,NA,NA,NA,NA,NA,f1_med,f2_med,NA,NA,NA))
    }
    harm2 <- harmonise_data(met_instr, ad_od)
    if(nrow(harm2)<3) {
      cat("    metab->AD: harm<3\n")
      return(mk_df(met_id,b1,se1,p1,n1,NA,NA,NA,nrow(harm2),NA,NA,NA,f1_med,f2_med,NA,NA,NA))
    }
    bx2<-as.numeric(harm2$beta.exposure)
    by2<-as.numeric(harm2$beta.outcome)
    so2<-as.numeric(harm2$se.outcome)
    ok2<-is.finite(bx2)&is.finite(by2)&is.finite(so2)&so2>0
    if(sum(ok2)<2) {
      cat("    metab->AD: <2 valid\n")
      return(mk_df(met_id,b1,se1,p1,n1,NA,NA,NA,sum(ok2),NA,NA,NA,f1_med,f2_med,NA,NA,NA))
    }
    bx2<-bx2[ok2];by2<-by2[ok2];so2<-so2[ok2]
    # F Step2 =: F=beta/se^2
    f2 <- (harm2$beta.exposure[ok2]/harm2$se.exposure[ok2])^2
    f2_med <- median(f2, na.rm=TRUE)
    w2<-1/so2^2;denom2<-sum(w2*bx2^2)
    if(!is.finite(denom2)||denom2<=0)
      return(mk_df(met_id,b1,se1,p1,n1,NA,NA,NA,length(bx2),NA,NA,NA,f1_med,f2_med,NA,NA,NA))
    b2<-sum(w2*bx2*by2)/denom2;se2<-sqrt(1/denom2)
    if(!is.finite(b2)||!is.finite(se2))
      return(mk_df(met_id,b1,se1,p1,n1,NA,NA,NA,length(bx2),NA,NA,NA,f1_med,f2_med,NA,NA,NA))
    p2<-2*pnorm(-abs(b2/se2)); n2<-length(bx2)
    cat(sprintf("    metab->AD: b=%.4f p=%.2g n=%d Fmed=%.1f\n", b2, p2, n2, f2_med))

    ind <- b1*b2
    se_ind <- sqrt(b2^2*se1^2 + b1^2*se2^2)
    p_ind <- 2*pnorm(-abs(ind/se_ind))
    cat(sprintf("    indirect=%.4f p=%.2g\n", ind, p_ind))

    # Bootstrap CI ref: 02b_g2_enhanced.R bootstrap_mediation
    if (!is.na(b1) && !is.na(se1) && !is.na(b2) && !is.na(se2) &&
        is.finite(se1) && se1 > 0 && is.finite(se2) && se2 > 0) {
      bt <- tryCatch(
        bootstrap_mediation(b1, se1, b2, se2, n_boot=BOOT_N, seed=42),
        error = function(e) list(boot_ci_lower=NA, boot_ci_upper=NA, boot_p=NA)
      )
      boot_ci_lower <- bt$boot_ci_lower
      boot_ci_upper <- bt$boot_ci_upper
      boot_p <- bt$boot_p
      cat(sprintf("    boot CI=[%.4f, %.4f] boot_p=%.2g\n",
                  boot_ci_lower, boot_ci_upper, boot_p))
    } else {
      boot_ci_lower <- boot_ci_upper <- boot_p <- NA
    }
    mk_df(met_id,b1,se1,p1,n1,b2,se2,p2,n2,ind,se_ind,p_ind,f1_med,f2_med,
          boot_ci_lower, boot_ci_upper, boot_p)
  }, error=function(e){
    cat(sprintf("  [%s] ERROR: %s\n", met_id, conditionMessage(e)))
    NULL
  })
}

results <- list()
for(m in mets) {
  cat(sprintf("\n--- %s ---\n", m))
  r <- run_one(m)
  if(!is.null(r)) results[[length(results)+1]] <- r
}

if(length(results)>0) {
  df <- do.call(rbind, results)
  df$q_ind <- p.adjust(df$p_ind, method="BH")
  df$weak_inst <- (df$n2 < 10 | (df$f2_med < 10 & !is.na(df$f2_med)))
  write.csv(df, file.path(OUT,"mediation_slim_10.csv"), row.names=FALSE)
  cat("\n===== RESULTS =====\n")
  print(df[,c("met","b1","p1","n1","f1_med","b2","p2","n2","f2_med","indirect","p_ind","q_ind","boot_ci_lower","boot_ci_upper","boot_p","weak_inst")])
  sig <- df[!is.na(df$q_ind) & df$q_ind<0.05, ]
  if(nrow(sig)>0) { cat("\n** SIGNIFICANT mediators (q<0.05): **\n"); print(sig$met) }
  else cat("\nNo significant mediator at FDR<0.05\n")
} else {
  cat("\nNo results produced\n")
}
cat("\n[DONE]\n")