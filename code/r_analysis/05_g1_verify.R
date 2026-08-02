# =====================================================================
# 05_g1_verify.R -- 核查 G1 失眠->AD 本地 vs IEU 在线 符号翻转来源
# =====================================================================
suppressMessages({ library(data.table); library(ieugwasr); library(TwoSampleMR); library(dplyr) })

LOCAL_DIR <- "C:/Temp/iad_g1/data/raw"
read_clean <- function(f) {
  dt <- fread(f, sep = "\t", header = TRUE)
  dt
}
ins_l <- read_clean(file.path(LOCAL_DIR, "ukb-b-3957", "ukb-b-3957.clean.tsv.gz"))
ad_l  <- read_clean(file.path(LOCAL_DIR, "ieu-b-2", "ieu-b-2.clean.tsv.gz"))
cat("本地失眠 nrow:", nrow(ins_l), " | 本地AD nrow:", nrow(ad_l), "\n")

## ---- A. G1 式手工 harmonize (action=none): 失眠=暴露, AD=结局 ----
ins_iv <- ins_l[p < 5e-8]   # 失眠 instrument (本地)
cat("本地失眠 instrument (p<5e-8):", nrow(ins_iv), "\n")
m <- merge(ins_iv[, .(SNP, A1, A2, beta, se)],
           ad_l[, .(SNP, A1, A2, beta, se)], by = "SNP", suffixes = c(".e", ".o"))
cat("合并 SNP:", nrow(m), "\n")
# 对齐: 暴露 A1/A2 为基准
flip <- (m$A1.e == m$A2.o & m$A2.e == m$A1.o)   # 结局等位翻转
keep <- (m$A1.e == m$A1.o & m$A2.e == m$A2.o) | flip
m <- m[keep]
m$beta.o2 <- m$beta.o; m$beta.o2[flip] <- -m$beta.o[flip]
cat("对齐后 SNP:", nrow(m), " (翻转:", sum(flip), ")\n")
ivw <- sum(m$beta.e * m$beta.o2 / m$se.o^2) / sum(m$beta.e^2 / m$se.o^2)
se  <- sqrt(1 / sum(m$beta.e^2 / m$se.o^2))
z <- ivw/se; p <- 2*pnorm(-abs(z))
cat(sprintf(">>> 本地文件 UVMR 失眠->AD: b=%.4f se=%.4f z=%.3f p=%.4g (nSNP=%d)\n", ivw, se, z, p, nrow(m)))

## ---- B. 定位符号翻转: 本地 vs IEU 在线 在 42 失眠 SNP 上的方向 ----
ins_on <- extract_instruments("ukb-b-3957", p1 = 5e-8, r2 = 0.001, kb = 10000)
cat("\nIEU 在线失眠 instrument:", nrow(ins_on), "\n")
ins_on2 <- ins_on[, c("SNP","effect_allele.exposure","other_allele.exposure","beta.exposure")]
ins_l2  <- ins_l[, c("SNP","A1","A2","beta")]
cmp <- merge(ins_on2, ins_l2, by = "SNP")
cmp$orient <- ifelse(cmp$effect_allele.exposure == cmp$A1, "same",
              ifelse(cmp$effect_allele.exposure == cmp$A2, "flip", "noold"))
cat("=== 失眠: 本地 vs IEU 等位方向 ===\n")
cat("same:", sum(cmp$orient=="same"), " flip:", sum(cmp$orient=="flip"), " noold:", sum(cmp$orient=="noold"), "\n")
cmp_h <- cmp[cmp$orient %in% c("same","flip"),]
cmp_h$sign_agree <- ifelse(cmp_h$orient=="same",
                     sign(cmp_h$beta.exposure)==sign(cmp_h$beta),
                     sign(cmp_h$beta.exposure)!=sign(cmp_h$beta))
cat("失眠 beta 方向一致 SNP:", sum(cmp_h$sign_agree), "/", nrow(cmp_h), "\n")

# AD 比较
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
cat("\n=== AD: 本地 vs IEU 等位方向 ===\n")
cat("same:", sum(cmp2$orient=="same"), " flip:", sum(cmp2$orient=="flip"), " noold:", sum(cmp2$orient=="noold"), "\n")
cat("AD beta 方向一致 SNP:", sum(cmp2_h$sign_agree), "/", nrow(cmp2_h), "\n")

cat("\n结论提示:\n")
cat("- 若失眠两源方向高度一致 + AD 两源方向高度一致 -> 符号翻转来自 harmonize 逻辑差异(非文件本身)\n")
cat("- 若某性状两源方向系统性相反 -> 该本地文件 munge 等位方向有误\n")
