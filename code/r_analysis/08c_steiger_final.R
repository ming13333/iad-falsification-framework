#!/usr/bin/env Rscript
# ============================================================
# 08c_steiger_final.R  (cached extraction + validated pure-R r)
# Steiger directionality test (insomnia <-> AD)
#   - exposure eaf: from extract_instruments() API (ukb-b-3957 carries eaf.exposure)
#   - outcome eaf (Kunkle & Bellenguez): ieugwasr::associations() chunked API
#   - binary-trait r via VALIDATED pure-R r_from_lor() (get_r_from_lor segfaults in
#     this R4.5.2 / pkg-built-4.5.3 ABI-mismatched env; replaced by exact
#     population-genetics derivation.)
#   - directionality_test() reads r.exposure/r.outcome (does NOT call get_r_from_lor)
#   - CACHES extraction+eaf to RDS so retries skip the API (random load segfaults
#     are the only gate; once past load, Steiger runs fast).
# ============================================================
suppressMessages({
  library(TwoSampleMR)
  library(ieugwasr)
  library(data.table)
})
data.table::setDTthreads(1)
set.seed(20260802)

api_retry <- function(f, max_try=6, sleep_base=20) {
  for (i in seq_len(max_try)) {
    r <- tryCatch(f(), error=function(e) {
      msg <- conditionMessage(e)
      if (grepl("401", msg)) { cat(sprintf("  [401 transient] retry %d/%d after %ds\n", i, max_try, sleep_base*i)); Sys.sleep(sleep_base*i); NULL }
      else stop(e)
    })
    if (!is.null(r)) return(r)
  }
  stop("api_retry: exhausted attempts (persistent 401)")
}

INS_ID   <- "ukb-b-3957"
KUNKLE   <- "ieu-b-2"
BELL     <- "ebi-a-GCST90027158"
OUT      <- "C:/Temp/iad_g1/results/steiger"
dir.create(OUT, showWarnings=FALSE, recursive=TRUE)
CACHE    <- file.path(OUT, "steiger_cache.rds")

INS_N      <- 462341; INS_PREV <- 0.10
KUNKLE_NC  <- 21982;  KUNKLE_NN <- 41944
BELL_NC    <- 39762;  BELL_NN  <- 41302

cat("\n===== Steiger directionality test (insomnia <-> AD) =====\n\n"); flush.console()

# ---------- validated pure-R genotype-phenotype r for binary traits ----------
r_from_lor <- function(lor, af, ncase, ncontrol, prevalence) {
  q   <- exp(lor)
  afv <- af
  flip <- q < 1
  if (any(flip)) { q[flip] <- 1/q[flip]; afv[flip] <- 1 - afv[flip] }
  p_s <- ncase / (ncase + ncontrol)
  A <- (1 - p_s) * (q - 1)
  B <- 1 + (q - 1) * (p_s - afv)
  C <- -afv
  disc <- B*B - 4*A*C
  disc[disc < 0] <- 0
  b <- (-B + sqrt(disc)) / (2*A)
  a <- q * b / (1 + b * (q - 1))
  f_pop <- prevalence * a + (1 - prevalence) * b
  f_pop <- pmin(pmax(f_pop, 1e-4), 1 - 1e-4)
  r <- 2 * sqrt(prevalence * (1 - prevalence)) * (a - b) / sqrt(2 * f_pop * (1 - f_pop))
  r[is.na(r) | !is.finite(r)] <- 0
  r
}

get_eaf_chunked <- function(snp_list, id, chunk_size=100) {
  n <- length(snp_list); n_chunks <- ceiling(n/chunk_size); res <- list()
  for (i in seq_len(n_chunks)) {
    lo <- (i-1)*chunk_size + 1; hi <- min(i*chunk_size, n); chunk <- snp_list[lo:hi]
    r <- NULL; attempt <- 0
    while (is.null(r) && attempt < 3) {
      attempt <- attempt + 1
      r <- tryCatch(associations(variants=chunk, id=id),
                    error=function(e){ cat("  chunk", i, "err:", conditionMessage(e), "\n"); Sys.sleep(2); NULL })
    }
    if (!is.null(r) && nrow(r) > 0) res[[i]] <- r
    if (i < n_chunks) Sys.sleep(1)
  }
  if (length(res) == 0) return(NULL)
  do.call(rbind, res)
}

inject_eaf_outcome <- function(harm, eaf_df) {
  harm$eaf.outcome <- NA_real_
  if (!is.null(eaf_df)) {
    idx <- match(harm$SNP, eaf_df$SNP); mm <- !is.na(idx)
    harm$eaf.outcome[mm] <- eaf_df$eaf_outcome[idx[mm]]
    cat(sprintf("  injected outcome eaf: %d/%d matched\n", sum(mm), nrow(harm)))
  }
  harm
}

# ---------- extraction (cached) ----------
SKIP <- FALSE
if (file.exists(CACHE)) {
  cat("loading cached extraction+eaf...\n")
  L <- readRDS(CACHE)
  exp_eaf <- L$exp_eaf; harm_k <- L$harm_k; harm_b <- L$harm_b
  SKIP <- TRUE
}
if (!SKIP) {
  exp <- api_retry(function() extract_instruments(INS_ID, p1=5e-8, r2=0.001, kb=10000, clump=TRUE))
  cat("insomnia instruments:", nrow(exp), "\n")
  exp_eaf <- data.frame(SNP=exp$SNP, eaf_exposure=exp$eaf.exposure, stringsAsFactors=FALSE)
  cat("  insomnia eaf.exposure available from API:", sum(!is.na(exp_eaf$eaf_exposure)), "/", nrow(exp_eaf), "\n")

  out_k <- api_retry(function() extract_outcome_data(snps=exp$SNP, outcomes=KUNKLE))
  out_b <- api_retry(function() extract_outcome_data(snps=exp$SNP, outcomes=BELL))
  harm_k <- harmonise_data(exp, out_k)
  harm_b <- harmonise_data(exp, out_b)
  cat("harm_k:", nrow(harm_k), " harm_b:", nrow(harm_b), "\n")

  kunkle_ids <- unique(harm_k$SNP)
  cat("fetching Kunkle eaf via API (", length(kunkle_ids), "SNPs)...\n")
  kunkle_eaf_raw <- tryCatch(get_eaf_chunked(kunkle_ids, KUNKLE), error=function(e) NULL)
  kunkle_eaf <- NULL
  if (!is.null(kunkle_eaf_raw)) {
    eafcol <- grep("^eaf$|effect_allele_frequency", names(kunkle_eaf_raw), value=TRUE)[1]
    if (!is.na(eafcol)) {
      kunkle_eaf <- data.frame(SNP=kunkle_eaf_raw$rsid, eaf_outcome=as.numeric(kunkle_eaf_raw[[eafcol]]), stringsAsFactors=FALSE)
      cat("  Kunkle API returned", nrow(kunkle_eaf), "eaf rows\n")
    }
  }
  bell_ids <- unique(harm_b$SNP)
  cat("fetching Bellenguez eaf via API (", length(bell_ids), "SNPs)...\n")
  bell_eaf_raw <- tryCatch(get_eaf_chunked(bell_ids, BELL), error=function(e) NULL)
  bell_eaf <- NULL
  if (!is.null(bell_eaf_raw)) {
    eafcol <- grep("^eaf$|effect_allele_frequency", names(bell_eaf_raw), value=TRUE)[1]
    if (!is.na(eafcol)) {
      bell_eaf <- data.frame(SNP=bell_eaf_raw$rsid, eaf_outcome=as.numeric(bell_eaf_raw[[eafcol]]), stringsAsFactors=FALSE)
      cat("  Bellenguez API returned", nrow(bell_eaf), "eaf rows\n")
    }
  }
  harm_k <- inject_eaf_outcome(harm_k, kunkle_eaf)
  harm_b <- inject_eaf_outcome(harm_b, bell_eaf)
  saveRDS(list(exp_eaf=exp_eaf, harm_k=harm_k, harm_b=harm_b), CACHE)
  cat("cached extraction+eaf ->", CACHE, "\n")
}

# ---------- compute r via validated pure-R function ----------
harm_k$r.exposure <- r_from_lor(harm_k$beta.exposure, harm_k$eaf.exposure,
                                INS_N*INS_PREV, INS_N*(1-INS_PREV), INS_PREV)
harm_k$r.outcome  <- r_from_lor(harm_k$beta.outcome,  harm_k$eaf.outcome,
                                KUNKLE_NC, KUNKLE_NN, KUNKLE_NC/(KUNKLE_NC+KUNKLE_NN))
harm_b$r.exposure <- r_from_lor(harm_b$beta.exposure, harm_b$eaf.exposure,
                                INS_N*INS_PREV, INS_N*(1-INS_PREV), INS_PREV)
harm_b$r.outcome  <- r_from_lor(harm_b$beta.outcome,  harm_b$eaf.outcome,
                                BELL_NC, BELL_NN, BELL_NC/(BELL_NN+BELL_NC))
cat(sprintf("  Kunkle: median |r.exp|=%.4f, |r.out|=%.4f\n",
            median(abs(harm_k$r.exposure), na.rm=TRUE), median(abs(harm_k$r.outcome), na.rm=TRUE))); flush.console()
cat(sprintf("  Bellenguez: median |r.exp|=%.4f, |r.out|=%.4f\n",
            median(abs(harm_b$r.exposure), na.rm=TRUE), median(abs(harm_b$r.outcome), na.rm=TRUE))); flush.console()

# ---------- directionality_test (crash-safe list-collect) ----------
run_steiger <- function(harm, label, path) {
  n_r <- sum(!is.na(harm$r.exposure) & !is.na(harm$r.outcome))
  cat(sprintf("  [%s] SNPs with both r.exposure & r.outcome = %d\n", label, n_r)); flush.console()
  if (n_r < 2) { cat(sprintf("[%s] SKIPPED: <2 SNPs with both r\n", label)); return(NULL) }
  cat(sprintf("  [%s] calling directionality_test...\n", label)); flush.console()
  res <- tryCatch(directionality_test(harm),
                  error=function(e){ cat(sprintf("[%s] ERROR: %s\n", label, conditionMessage(e))); NULL })
  if (is.null(res)) return(NULL)
  cat(sprintf("=== Steiger: %s ===\n", label)); print(res)
  saveRDS(res, path)
  res
}
st_k <- run_steiger(harm_k, "insomnia<->Kunkle",    file.path(OUT, "steiger_ins_kunkle.rds"))
st_b <- run_steiger(harm_b, "insomnia<->Bellenguez", file.path(OUT, "steiger_ins_bell.rds"))

# ---------- summary ----------
summ <- function(res, label) {
  if (is.null(res)) return(data.frame(label=label, status="SKIPPED/ERROR",
                                       steiger_p=NA_real_, correct_causal=NA_character_,
                                       stringsAsFactors=FALSE))
  data.frame(label=label, status="OK",
             steiger_p=if("p" %in% names(res)) signif(res$p,3) else NA_real_,
             correct_causal=if("steiger" %in% names(res)) as.character(res$steiger) else NA_character_,
             stringsAsFactors=FALSE)
}
df_sum <- rbindlist(list(summ(st_k, "insomnia<->Kunkle"), summ(st_b, "insomnia<->Bellenguez")))
write.csv(df_sum, file.path(OUT, "steiger_summary.txt"), row.names=FALSE)
cat("\n===== STEIGER SUMMARY =====\n"); print(df_sum)
cat("\n[DONE]\n")
