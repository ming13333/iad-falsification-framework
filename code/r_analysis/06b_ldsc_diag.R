suppressMessages({ library(GenomicSEM); library(data.table) })
setwd("./output/ldsc_work")

LDSCORE <- "./output/ld_ref/LDscore"

cat("=== LDSC  ===\n")
cat("LDSCORE dir:", LDSCORE, "\n")
cat("Munged files:\n")
print(list.files(pattern="\\.sumstats\\.gz$"))

traits <- c("insomnia.sumstats.gz", "ad_kunkle.sumstats.gz")
cat("\nCalling ldsc()...\n")
flush.console()

result <- tryCatch({
  ldsc(traits = traits,
       sample.prev = c(NA, 0.344),
       population.prev = c(NA, NA),
       ld = LDSCORE,
       wld = LDSCORE,
       trait.names = c("insomnia", "ad"))
}, error = function(e) {
  cat("\n[ERROR] ldsc() failed:\n")
  cat("Message:", conditionMessage(e), "\n")
  cat("Class:", class(e), "\n")
  traceback()
  NULL
}, warning = function(w) {
  cat("[WARNING]", conditionMessage(w), "\n")
  suppressWarnings(ldsc(traits = traits,
       sample.prev = c(NA, 0.344),
       population.prev = c(NA, NA),
       ld = LDSCORE, wld = LDSCORE,
       trait.names = c("insomnia", "ad")))
})

if (!is.null(result)) {
  cat("\n=== LDSC ! ===\n")
  cat("S matrix:\n"); print(result$S)
  cat("V matrix:\n"); print(result$V)
  cat("I matrix:\n"); print(result$I)
  rg <- result$S[1,2] / sqrt(result$S[1,1] * result$S[2,2])
  cat("\nrg =", rg, "\n")
} else {
  cat("\n[FAILED] ldsc() returned NULL\n")
}