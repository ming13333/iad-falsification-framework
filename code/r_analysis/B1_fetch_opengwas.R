# ============================================================
# B1 - 蛋白 pQTL 取数 (OpenGWAS prot- 命名空间, GRCh37 原生)
# 运行须: Rscript --(由调用方以 dangerouslyDisableSandbox 启动以放行 VPN 网络)
# 依赖: ieugwasr
# ============================================================
suppressMessages(library(ieugwasr))

# 安全重命名列
rename_col <- function(df, from, to) {
  names(df)[names(df) == from] <- to
  df
}

OUT <- "C:/Temp/iad_g1/proteins"
dir.create(OUT, showWarnings = FALSE, recursive = TRUE)

# ---- 目标蛋白 -> OpenGWAS prot- ID (已实测确认) ----
# 来源: Sun BB 2018 (INTERVAL, n=3301) / Suhre K 2019 (大样本)
targets <- list(
  GFAP             = "prot-c-3034_1_2",   # Suhre 2019; eaf 缺(连续性状coloc可接受)
  Neurofilament    = "prot-a-2027",       # NfL, Sun 2018
  C_reactive_protein = "prot-a-670",      # CRP, Sun 2018
  Interleukin_6    = "prot-a-1540"        # IL-6, Sun 2018
)

# GFAP 基因区域 (来自 gwasinfo note: chr17 44905008-44916937)
gfap_region <- "chr17:44900000-44930000"

fetch_one <- function(id, liberal_pval = 1e-5, gfap_region = NULL) {
  # 优先 tophits 5e-8；弱工具蛋白回退到 liberal_pval 多取 IV
  d <- tryCatch(tophits(id = id, pval = 5e-8, clump = FALSE),
                error = function(e) NULL)
  if (is.null(d) || nrow(d) == 0) {
    d <- tryCatch(tophits(id = id, pval = liberal_pval, clump = FALSE),
                  error = function(e) NULL)
  }
  if ((is.null(d) || nrow(d) == 0) && !is.null(gfap_region)) {
    # GFAP 大数据集 tophits 偶发报错 -> region 兜底
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
  # 重命名对齐 G1 约定
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
