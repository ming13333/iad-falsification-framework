# test_local_gwas.R — 隔离验证本地 clean 文件读取与 harmonize(不触发 01 完整管线)
# 不 source 00_config.R(其 library(TwoSampleMR) 会触发 jsonlite.dll 被 WDAC 阻止)。
# 本地读取/对齐函数仅依赖 data.table, 与 TwoSampleMR 生态无关。
library(data.table)

DIR_RAW_LOCAL <- "C:/D/workbuddy/科研/共病分析/data/raw"
LOCAL_CLEAN <- list(
  "ukb-b-3957"          = file.path(DIR_RAW_LOCAL, "ukb-b-3957", "ukb-b-3957.clean.tsv.gz"),
  "ieu-b-2"             = file.path(DIR_RAW_LOCAL, "ieu-b-2", "ieu-b-2.clean.tsv.gz"),
  "ebi-a-GCST90027158"  = file.path(DIR_RAW_LOCAL, "ebi-a-GCST90027158", "GCST90027158_buildGRCh38.dedup.tsv.gz")
)

.LocalCleanCache <- if (exists(".LocalCleanCache", envir = globalenv()))
  get(".LocalCleanCache", envir = globalenv()) else new.env(hash = TRUE, parent = emptyenv())
read_local_clean <- function(id, label = "local") {
  if (exists(id, envir = .LocalCleanCache)) return(get(id, envir = .LocalCleanCache))
  lf <- if (id %in% names(LOCAL_CLEAN)) LOCAL_CLEAN[[id]] else NULL
  if (is.null(lf) || !file.exists(lf)) {
    message("[", label, "] 无本地 clean 文件(", id, ")"); return(NULL)
  }
  dt <- tryCatch(data.table::fread(lf, sep = "\t", header = TRUE, showProgress = FALSE,
                                   data.table = FALSE),
                 error = function(e) { message("读失败:", conditionMessage(e)); NULL })
  if (is.null(dt) || nrow(dt) == 0) return(NULL)
  nm <- tolower(names(dt)); names(dt) <- nm
  out <- data.frame(
    snp = as.character(dt$snp),
    beta = as.numeric(dt$beta),
    se = as.numeric(dt$se),
    A1 = as.character(dt$a1),
    A2 = as.character(dt$a2),
    chr = suppressWarnings(as.integer(dt$chr)),
    pos = suppressWarnings(as.integer(dt$bp)),
    p = as.numeric(dt$p),
    stringsAsFactors = FALSE)
  if (!is.null(dt$n)) out$N <- as.numeric(dt$n)
  if (!is.null(dt$ncase))      out$icase <- as.numeric(dt$ncase)
  if (!is.null(dt$ncontrol))   out$icontrol <- as.numeric(dt$ncontrol)
  if (!is.null(dt$n_cases))    out$icase <- as.numeric(dt$n_cases)
  if (!is.null(dt$n_controls)) out$icontrol <- as.numeric(dt$n_controls)
  if (is.null(out$N) && !is.null(out$icase) && !is.null(out$icontrol))
    out$N <- out$icase + out$icontrol
  keep <- !is.na(out$beta) & !is.na(out$se) & nzchar(out$snp) & out$snp != "."
  res <- out[keep, ]
  assign(id, res, envir = .LocalCleanCache)
  res
}

build_harmonized_local <- function(exp_id, out_id, pval = 5e-8, label = "harmonize-local") {
  exp <- read_local_clean(exp_id, label); out <- read_local_clean(out_id, label)
  if (is.null(exp) || is.null(out)) return(NULL)
  exp_iv <- exp[!is.na(exp$p) & exp$p < pval & exp$p > 0, ]
  message("[", label, "] ", exp_id, " 显著 SNP(p<", format(pval, digits=2), ")=",
          nrow(exp_iv), " 全量=", nrow(exp))
  if (nrow(exp_iv) == 0) return(NULL)
  m <- merge(exp_iv, out, by = "snp", suffixes = c(".exposure", ".outcome"), all.x = TRUE)
  m <- m[!is.na(m$beta.outcome) & !is.na(m$se.outcome), ]
  if (nrow(m) == 0) return(NULL)
  ea_e <- m$A1.exposure; oa_e <- m$A2.exposure
  ea_o <- m$A1.outcome;  oa_o <- m$A2.outcome
  same <- (ea_e == ea_o) & (oa_e == oa_o)
  flip <- (ea_e == oa_o) & (oa_e == ea_o)
  ambiguous <- !(same | flip); ambiguous[is.na(ambiguous)] <- TRUE
  m$beta.outcome[flip] <- -m$beta.outcome[flip]
  m <- m[!ambiguous, ]
  if (nrow(m) == 0) return(NULL)
  n <- nrow(m)
  exp_N <- if (!is.null(exp$N)) exp$N[1] else NA_real_
  out_N <- if (!is.null(out$N)) out$N[1] else NA_real_
  dat <- data.frame(
    id.exposure = rep(exp_id, n), id.outcome = rep(out_id, n),
    SNP = m$snp,
    chr.exposure = m$chr.exposure, pos.exposure = m$pos.exposure,
    effect_allele.exposure = m$A1.exposure, other_allele.exposure = m$A2.exposure,
    effect_allele.outcome = m$A1.outcome, other_allele.outcome = m$A2.outcome,
    beta.exposure = m$beta.exposure, se.exposure = m$se.exposure,
    beta.outcome = m$beta.outcome, se.outcome = m$se.outcome,
    stringsAsFactors = FALSE)
  message("[", label, "] 完成: ", nrow(dat), " 工具 SNP, ", sum(ambiguous), " ambiguous")
  dat
}

cat("=== 1. read_local_clean ===\n")
for (id in c("ukb-b-3957","ieu-b-2","ebi-a-GCST90027158")) {
  d <- read_local_clean(id)
  if (!is.null(d)) cat(sprintf("%-22s rows=%-10d cols=%s\n", id, nrow(d),
                                paste(names(d), collapse=","))) else cat(id, "NULL\n")
}

cat("=== 2. harmonize 双向 ===\n")
d1 <- tryCatch(build_harmonized_local("ukb-b-3957","ieu-b-2"),
               error=function(e){cat("BUILD_ERR_FWD:", conditionMessage(e), "\n"); NULL})
if(!is.null(d1)) cat("fwd=",nrow(d1),"\n")
d2 <- tryCatch(build_harmonized_local("ieu-b-2","ukb-b-3957"),
               error=function(e){cat("BUILD_ERR_REV:", conditionMessage(e), "\n"); NULL})
if(!is.null(d2)) cat("rev=",nrow(d2),"\n")

cat("=== 3. N 字段 ===\n")
e <- read_local_clean("ieu-b-2"); cat("ieu N=", ifelse(is.null(e$N),NA,e$N[1]),
    " icase=", ifelse(is.null(e$icase),NA,e$icase[1]), "\n")
u <- read_local_clean("ukb-b-3957"); cat("ukb N=", ifelse(is.null(u$N),NA,u$N[1]), "\n")
b <- read_local_clean("ebi-a-GCST90027158"); cat("bell N=", ifelse(is.null(b$N),NA,b$N[1]),
    " icase=", ifelse(is.null(b$icase),NA,b$icase[1]), "\n")

cat("=== 4. SNP 标识体系诊断 ===\n")
u <- read_local_clean("ukb-b-3957"); a <- read_local_clean("ieu-b-2")
u_rs <- sum(grepl("^rs", u$snp)); a_rs <- sum(grepl("^rs", a$snp))
cat("ukb 总=", nrow(u), " rs开头=", u_rs, " 非rs=", nrow(u)-u_rs, "\n")
cat("ieu 总=", nrow(a), " rs开头=", a_rs, " 非rs=", nrow(a)-a_rs, "\n")
cat("ukb∩ieu 直接ID匹配=", length(intersect(u$snp, a$snp)), "\n")
uk <- paste(u$chr,u$pos,sep=":"); ak <- paste(a$chr,a$pos,sep=":")
cat("ukb∩ieu 按chr:pos匹配=", length(intersect(uk, ak)), "\n")
cat("TEST_DONE\n")
