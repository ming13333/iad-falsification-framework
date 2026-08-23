# =====================================================================
# 05_g1_verify.R -- G1 ->AD vs IEU
# =====================================================================
suppressMessages({ library(data.table); library(ieugwasr); library(TwoSampleMR); library(dplyr) })

LOCAL_DIR <- "./output/data/raw"
read_clean <- function(f) {
  dt <- fread(f, sep = "\t", header = TRUE)
  dt
}
ins_l <- read_clean(file.path(LOCAL_DIR, "ukb-b-3957", "ukb-b-3957.clean.tsv.gz"))
ad_l  <- read_clean(file.path(LOCAL_DIR, "ieu-b-2", "ieu-b-2.clean.tsv.gz"))
cat(" nrow:", nrow(ins_l), " | AD nrow:", nrow(ad_l), "\n")

# ---- A. G1 harmonize action=none: =, AD=
ins_iv <- ins_l[p < 5e-8]   #  instrument ()
cat(" instrument (p<5e-8):", nrow(ins_iv), "\n")
m <- merge(ins_iv[, .(SNP, A1, A2, beta, se)],
           ad_l[, .(SNP, A1, A2, beta, se)], by = "SNP", suffixes = c(".e", ".o"))
cat(" SNP:", nrow(m), "\n")
flip <- (m$A1.e == m$A2.o & m$A2.e == m$A1.o)   # 
keep <- (m$A1.e == m$A1.o & m$A2.e == m$A2.o) | flip
m <- m[keep]
m$beta.o2 <- m$beta.o; m$beta.o2[flip] <- -m$beta.o[flip]
cat(" SNP:", nrow(m), " (:", sum(flip), ")\n")
ivw <- sum(m$beta.e * m$beta.o2 / m$se.o^2) / sum(m$beta.e^2 / m$se.o^2)
se  <- sqrt(1 / sum(m$beta.e^2 / m$se.o^2))
z <- ivw/se; p <- 2*pnorm(-abs(z))
cat(sprintf(">>>  UVMR ->AD: b=%.4f se=%.4f z=%.3f p=%.4g (nSNP=%d)\n", ivw, se, z, p, nrow(m)))

# ---- B. : vs IEU 42 SNP
ins_on <- extract_instruments("ukb-b-3957", p1 = 5e-8, r2 = 0.001, kb = 10000)
cat("\nIEU  instrument:", nrow(ins_on), "\n")
ins_on2 <- ins_on[, c("SNP","effect_allele.exposure","other_allele.exposure","beta.exposure")]
ins_l2  <- ins_l[, c("SNP","A1","A2","beta")]
cmp <- merge(ins_on2, ins_l2, by = "SNP")
cmp$orient <- ifelse(cmp$effect_allele.exposure == cmp$A1, "same",
              ifelse(cmp$effect_allele.exposure == cmp$A2, "flip", "noold"))
cat("=== :  vs IEU  ===\n")
cat("same:", sum(cmp$orient=="same"), " flip:", sum(cmp$orient=="flip"), " noold:", sum(cmp$orient=="noold"), "\n")
cmp_h <- cmp[cmp$orient %in% c("same","flip"),]
cmp_h$sign_agree <- ifelse(cmp_h$orient=="same",
                     sign(cmp_h$beta.exposure)==sign(cmp_h$beta),
                     sign(cmp_h$beta.exposure)!=sign(cmp_h$beta))
cat(" beta  SNP:", sum(cmp_h$sign_agree), "/", nrow(cmp_h), "\n")

ad_on <- extract_outcome_data(snps = ins_on$SNP, outcomes = "ieu-b-2")
ad_on2 <- ad_on[, c("SNP","effect_allele.outcome","other_allele.outcome","beta.outcome")]
ad_l2  <- ad_l[, c("SNP","A1","A2","beta")]
cmp2 <- merge(ad_on2, ad_l2, by = "SNP")
cmp2$orient <- ifelse(cmp2$effect_allele.outcome == cmp2$A1, "same",
               ifelse(cmp2$effect_allele.outcome == cmp2$A2, "flip", "noold"))
cmp2_h <- cmp2[cmp2$orient %in% c("same","flip"),]
cmp2_h$sign_agree <- ifelse(cmp2_h$orient=="same",
                      sign(cmp2_h$beta.outcome)==sign(cmp2_h$beta),
                      sign(cmp2_h$beta.outcome)!=sign(cmp2_h$beta))
cat("\n=== AD:  vs IEU  ===\n")
cat("same:", sum(cmp2$orient=="same"), " flip:", sum(cmp2$orient=="flip"), " noold:", sum(cmp2$orient=="noold"), "\n")
cat("AD beta  SNP:", sum(cmp2_h$sign_agree), "/", nrow(cmp2_h), "\n")

cat("\n:\n")
cat("-  + AD  ->  harmonize ()\n")
cat("-  ->  munge \n")