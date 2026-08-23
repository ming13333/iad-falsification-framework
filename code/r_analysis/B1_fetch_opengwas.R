# ============================================================
# B1 - pQTL OpenGWAS prot- , GRCh37
# : Rscript -- dangerouslyDisableSandbox VPN
# ============================================================
suppressMessages(library(ieugwasr))

rename_col <- function(df, from, to) {
  names(df)[names(df) == from] <- to
  df
}

OUT <- "./output/proteins"
dir.create(OUT, showWarnings = FALSE, recursive = TRUE)

# ---- -> OpenGWAS prot- ID
# : Sun BB 2018 INTERVAL, n=3301 / Suhre K 2019
targets <- list(
  GFAP             = "prot-c-3034_1_2",   # Suhre 2019; eaf (coloc)
  Neurofilament    = "prot-a-2027",       # NfL, Sun 2018
  C_reactive_protein = "prot-a-670",      # CRP, Sun 2018
  Interleukin_6    = "prot-a-1540"        # IL-6, Sun 2018
)

# GFAP gwasinfo note: chr17 44905008-44916937
gfap_region <- "chr17:44900000-44930000"

fetch_one <- function(id, liberal_pval = 1e-5, gfap_region = NULL) {
  # tophits 5e-8; liberal_pval IV
  d <- tryCatch(tophits(id = id, pval = 5e-8, clump = FALSE),
                error = function(e) NULL)
  if (is.null(d) || nrow(d) == 0) {
    d <- tryCatch(tophits(id = id, pval = liberal_pval, clump = FALSE),
                  error = function(e) NULL)
  }
  if ((is.null(d) || nrow(d) == 0) && !is.null(gfap_region)) {
    # GFAP tophits -> region
    d <- tryCatch(tophits(id = id, pval = 1e-3, clump = TRUE),
                  error = function(e) NULL)
  }
  d
}

cat("=== fetch + normalize + save ===\n")
manifest <- data.frame()
for (nm in names(targets)) {
  id <- targets[[nm]]
  cat(sprintf("\n--- %s (%s) ---\n", nm, id))
  d <- fetch_one(id, gfap_region = if (nm == "GFAP") gfap_region else NULL)
  if (is.null(d) || nrow(d) == 0) { cat("  NO DATA, skip\n"); next }
  cat("  raw rows:", nrow(d), " cols:", paste(names(d), collapse = ","), "\n")
  colnames(d) <- tolower(colnames(d))
  if ("position" %in% names(d)) d <- rename_col(d, "position", "pos")
  f <- file.path(OUT, paste0(nm, ".pqtl.tsv"))
  write.table(d, f, sep = "\t", quote = FALSE, row.names = FALSE)
  n_eaf <- if ("eaf" %in% names(d)) sum(!is.na(d$eaf)) else 0
  cat(sprintf("  saved %s : %d rows, eaf_nonNA=%d, rsid_nonNA=%d\n",
              basename(f), nrow(d), n_eaf,
              if ("rsid" %in% names(d)) sum(!is.na(d$rsid)) else 0))
  manifest <- rbind(manifest, data.frame(
    target = nm, prot_id = id, n_rows = nrow(d),
    has_eaf = (n_eaf > 0), build = "GRCh37/HG19",
    note = if (nm == "GFAP") "Suhre2019 eaf NA" else "Sun2018 INTERVAL",
    file = f, stringsAsFactors = FALSE))
}
write.table(manifest, file.path(OUT, "manifest.csv"), sep = ",",
            quote = FALSE, row.names = FALSE)
cat("\n=== manifest ===\n"); print(manifest)
cat("\n[B1] DONE\n")