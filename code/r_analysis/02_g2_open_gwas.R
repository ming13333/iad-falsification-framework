# =====================================================================
# 02_g2_open_gwas.R  —  G2 落地: 血浆蛋白两步中介 MR (OpenGWAS prot- 本地文件)
# ---------------------------------------------------------------------
# 适配 B1 产物: C:/Temp/iad_g1/proteins/*.pqtl.tsv
#   列: id, trait, chr, pos, rsid, ea, nea, eaf, beta, se, p, n  (GRCh37)
# 先跑 CRP / IL-6 (OpenGWAS 强 IV, 212/748 hits); GFAP/NfL 待 UKB-PPP 补全。
# 重叠说明: 蛋白源 = INTERVAL (非 UKB), 故
#   Step1(ukb-b-3957 失眠 → 蛋白) 与 Step2(蛋白 → ieu-b-2 AD) 双侧均非 UKB×UKB,
#   无样本重叠 → delta 法 SE 独立性假设成立, MRlap 重叠校正钩子保持关闭。
# 运行(需 VPN 以访问 IEU REST): Rscript 02_g2_open_gwas.R
# =====================================================================
suppressMessages({ library(TwoSampleMR); library(ieugwasr); library(coloc); library(dplyr) })

## ---- 配置(自包含, 不依赖 00_config) ----
GWAS_ID <- list(insomnia = "ukb-b-3957", ad = "ieu-b-2", ad_alt = "ebi-a-GCST90027158")
THRESH  <- list(clump_r2 = 0.001, clump_kb = 10000, coloc_pph4 = 0.80, protein_fdr = 0.05)
AD_N    <- 63860      # ieu-b-2 (Kunkle/IGAP) 总样本量
G2_OUT  <- "C:/Temp/iad_g1/results"
PROT_INDEX <- "C:/Temp/iad_g1/proteins/g2_index.csv"
dir.create(G2_OUT, showWarnings = FALSE, recursive = TRUE)

## ---- 读蛋白索引 ----
if (!file.exists(PROT_INDEX)) stop("[G2] 缺索引: ", PROT_INDEX)
protein_map <- read.csv(PROT_INDEX, stringsAsFactors = FALSE, fileEncoding = "UTF-8-BOM")
if (!"ieu_id" %in% names(protein_map) && !"file" %in% names(protein_map))
  stop("[G2] 索引需含 ieu_id(在线) 或 file(本地) 列")
if (!"protein_id" %in% names(protein_map)) stop("[G2] 索引缺 protein_id")
if (!"olink_target" %in% names(protein_map)) protein_map$olink_target <- protein_map$protein_id
if (!"n_samples" %in% names(protein_map)) warning("[G2] 索引缺 n_samples, coloc 蛋白侧 N 用 3301")
if ("ieu_id" %in% names(protein_map)) { protein_map$source <- "ieu"; protein_map$path <- protein_map$ieu_id } else { protein_map$source <- "local"; protein_map$path <- protein_map$file }
message("[G2] 蛋白索引: ", nrow(protein_map), " 个 (", paste(protein_map$olink_target, collapse = ", "), ")")

## ---- 读取 B1 本地蛋白文件, 对齐 TwoSampleMR 列名 (供 coloc 窗口过滤) ----
load_b1_protein <- function(file) {
  if (!file.exists(file)) { warning("[G2] 文件缺失: ", file); return(NULL) }
  d <- utils::read.delim(file, stringsAsFactors = FALSE, fileEncoding = "UTF-8-BOM")
  rn <- c(rsid="SNP", ea="effect_allele", nea="other_allele", p="pval",
          beta="beta", se="se", chr="chr", pos="pos", eaf="eaf")
  nms <- names(d)
  for (o in names(rn)) if (o %in% nms) names(d)[which(nms == o)] <- rn[o]
  keep <- c("SNP","beta","se","pval","chr","pos","eaf","effect_allele","other_allele")
  for (k in keep) if (!k %in% names(d)) d[[k]] <- NA
  d[, keep, drop = FALSE]
}

## ---- 蛋白作暴露 / 结局 的分流 (read_exposure_data 保证 .exposure/.outcome 格式) ----
get_protein_instruments <- function(prow, p1 = 5e-8) {
  if (prow$source == "ieu") {
    d <- tryCatch(extract_instruments(prow$path, p1 = p1, r2 = THRESH$clump_r2, kb = THRESH$clump_kb),
                  error = function(e) { message("[G2] ieu_exp ", prow$protein_id, " err: ", conditionMessage(e)); NULL })
  } else {
    # 本地 B1 文件 (显著位点子集)
    d <- tryCatch(read_exposure_data(
        filename = prow$path, sep = "\t", clump = FALSE, pval_threshold = p1,
        snp_col = "rsid", beta_col = "beta", se_col = "se", pval_col = "p",
        chr_col = "chr", pos_col = "pos", eaf_col = "eaf",
        effect_allele_col = "ea", other_allele_col = "nea"),
      error = function(e) { message("[G2] read_exp ", prow$protein_id, " err: ", conditionMessage(e)); NULL })
  }
  if (is.null(d) || nrow(d) == 0) return(NULL)
  if (nrow(d) < 2) { message("[G2] ", prow$protein_id, " IV 不足(<2), 跳过"); return(NULL) }
  d
}
get_protein_outcome <- function(snps, prow) {
  if (prow$source == "ieu") {
    out <- tryCatch(extract_outcome_data_batched(snps = snps, outcomes = prow$path),
                    error = function(e) { message("[G2] ieu_out ", prow$protein_id, " err: ", conditionMessage(e)); NULL })
    if (is.null(out) || nrow(out) == 0) return(NULL)
    out$outcome <- prow$olink_target
    return(out)
  }
  # 本地 B1 文件 (仅显著位点, 步1 失眠 IV 不在其中 → 需 IEU; 保留作备用)
  full <- tryCatch(read_exposure_data(
      filename = prow$path, sep = "\t", clump = FALSE,
      snp_col = "rsid", beta_col = "beta", se_col = "se", pval_col = "p",
      chr_col = "chr", pos_col = "pos", eaf_col = "eaf",
      effect_allele_col = "ea", other_allele_col = "nea"),
    error = function(e) { message("[G2] read_out ", prow$protein_id, " err: ", conditionMessage(e)); NULL })
  if (is.null(full)) return(NULL)
  full <- full[full$SNP %in% as.character(snps), ]
  if (nrow(full) == 0) return(NULL)
  names(full) <- gsub("\\.exposure$", ".outcome", names(full))
  full$outcome <- prow$olink_target
  full
}

## ---- 批量拉结局关联 (IEU, 分批降速) ----
BATCH_SIZE <- 20
extract_outcome_data_batched <- function(snps, outcomes, batch_size = BATCH_SIZE, sleep_sec = 1, ...) {
  snps <- unique(as.character(snps)); n <- length(snps)
  if (n == 0) return(NULL)
  nb <- ceiling(n / batch_size); pieces <- list()
  for (i in seq_len(nb)) {
    lo <- (i-1)*batch_size + 1; hi <- min(i*batch_size, n); chunk <- snps[lo:hi]
    res <- tryCatch(extract_outcome_data(snps = chunk, outcomes = outcomes, ...),
                    error = function(e) { message("  [batch] 失败: ", conditionMessage(e)); NULL })
    if (!is.null(res) && nrow(res) > 0) pieces[[length(pieces)+1]] <- res
    if (i < nb && sleep_sec > 0) Sys.sleep(sleep_sec)
  }
  pieces <- Filter(function(x) !is.null(x) && nrow(x) > 0, pieces)
  if (length(pieces) == 0) return(NULL)
  dplyr::bind_rows(pieces)
}

## ---- 两样本 IVW ----
ivw_est_protein <- function(exp_id_or_row, out_id_or_row, exp_is_protein, out_is_protein, p1 = 5e-8) {
  if (exp_is_protein) exp <- get_protein_instruments(exp_id_or_row, p1 = p1)
  else exp <- tryCatch(extract_instruments(exp_id_or_row, p1 = p1, r2 = THRESH$clump_r2, kb = THRESH$clump_kb),
                        error = function(e) NULL)
  if (is.null(exp) || nrow(exp) == 0) { message("  [ivw] exp NULL/empty"); return(NULL) }
  if (out_is_protein) out <- tryCatch(get_protein_outcome(exp$SNP, out_id_or_row), error = function(e) NULL)
  else out <- tryCatch(extract_outcome_data_batched(snps = exp$SNP, outcomes = out_id_or_row), error = function(e) NULL)
  if (is.null(out) || nrow(out) == 0) { message("  [ivw] out NULL/empty (exp n=", nrow(exp), ")"); return(NULL) }
  d <- tryCatch(harmonise_data(exp, out), error = function(e) { message("  [harm] err: ", conditionMessage(e)); NULL })
  if (is.null(d) || nrow(d) < 2) { message("  [ivw] harm fail n=", if(is.data.frame(d)) nrow(d) else "NULL"); return(NULL) }
  res <- mr(d, method_list = "mr_ivw")
  row <- res[grepl("Inverse variance", res$method), ]
  if (nrow(row) == 0) { message("  [ivw] no IVW row (methods: ", paste(unique(res$method), collapse=","), ")"); return(NULL) }
  data.frame(b = row$b, se = row$se, p = row$pval, n_snps = nrow(d), stringsAsFactors = FALSE)
}

## ---- 2. 两步中介 ----
insomnia_exp_id <- GWAS_ID$insomnia
ad_out_id       <- GWAS_ID$ad
rows <- list()
for (i in seq_len(nrow(protein_map))) {
  prow <- protein_map[i, ]; pid <- prow$protein_id; name <- prow$olink_target
  s1 <- tryCatch(ivw_est_protein(exp_id_or_row = insomnia_exp_id, out_id_or_row = prow,
                                 exp_is_protein = FALSE, out_is_protein = TRUE),
                 error = function(e) { message("[G2] step1 ", pid, " err: ", conditionMessage(e)); NULL })
  if (is.null(s1)) next
  s2 <- tryCatch(ivw_est_protein(exp_id_or_row = prow, out_id_or_row = ad_out_id,
                                 exp_is_protein = TRUE, out_is_protein = FALSE),
                 error = function(e) { message("[G2] step2 ", pid, " err: ", conditionMessage(e)); NULL })
  if (is.null(s2)) next
  rows[[pid]] <- data.frame(protein = pid, target = name, source = "local",
                            b1 = s1$b, se1 = s1$se, p1 = s1$p, n1 = s1$n_snps,
                            b2 = s2$b, se2 = s2$se, p2 = s2$p, n2 = s2$n_snps,
                            stringsAsFactors = FALSE)
  message("[G2] ", pid, " done: n1=", s1$n_snps, " n2=", s2$n_snps,
          " b1=", signif(s1$b,3), " b2=", signif(s2$b,3))
}
if (length(rows) == 0) stop("[G2] 未得到任何两步估计，检查 GWAS ID / 网络 / 索引。")
mediation <- dplyr::bind_rows(rows)

## ---- 3. 间接效应 (delta 法) ----
mediation <- mediation %>%
  mutate(
    indirect = b1 * b2,
    se_ind   = sqrt(b2^2 * se1^2 + b1^2 * se2^2),
    p_ind    = 2 * pnorm(-abs(indirect) / se_ind),
    fdr      = p.adjust(p_ind, method = "fdr")
  ) %>% arrange(p_ind)
sig <- mediation[mediation$fdr < THRESH$protein_fdr, ]
message("[G2] 总蛋白=", nrow(mediation), " | FDR<", THRESH$protein_fdr, " 显著=", nrow(sig))
print(mediation[, c("protein","target","b1","b2","indirect","se_ind","p_ind","fdr","n1","n2")])

## ---- 4. coloc 复核 top 蛋白 (蛋白 pQTL ↔ AD) ----
# 注意: B1 仅提供 p<5e-8 显著位点(非全变异), 区域窗口内 SNP 可能稀少;
#       仅对窗口内 蛋白∩AD 交集 >=3 的 locus 做 coloc.abf, 否则记 NA (探索性).
coloc_protein <- function(prow, out_id, window_kb = 500) {
  pexp <- get_protein_instruments(prow)
  if (is.null(pexp) || nrow(pexp) == 0) return(NULL)
  if (is.null(pexp$chr)) pexp$chr <- pexp$chr.exposure
  if (is.null(pexp$pos)) pexp$pos <- pexp$pos.exposure
  out_list <- list()
  for (snp in unique(pexp$SNP)) {
    chr <- pexp$chr[pexp$SNP == snp][1]; pos <- pexp$pos[pexp$SNP == snp][1]
    if (is.na(chr) || is.na(pos)) next
    lo <- pos - window_kb*1000L; hi <- pos + window_kb*1000L
    # 蛋白侧: 用 IEU 蛋白 IV 窗口内子集 (pexp 已含 .exposure 列, 在线全变异)
    if (is.null(pexp$chr.exposure)) pexp$chr.exposure <- pexp$chr
    if (is.null(pexp$pos.exposure)) pexp$pos.exposure <- pexp$pos
    pf <- pexp[!is.na(pexp$pos.exposure) & pexp$chr.exposure == chr &
               pexp$pos.exposure >= lo & pexp$pos.exposure <= hi, ]
    if (nrow(pf) == 0) next
    ap <- data.frame(rsid = pf$SNP, beta = pf$beta.exposure, se = pf$se.exposure,
                     position = pf$pos.exposure, eaf = pf$eaf.exposure, stringsAsFactors = FALSE)
    win <- tryCatch(ieugwasr::variants_chrpos(chr = chr, from = lo, to = hi), error = function(e) NULL)
    aa <- if (is.null(win)) NULL else tryCatch(ieugwasr::associations(variants = win, id = out_id),
                                                error = function(e) NULL)
    if (!is.null(aa)) { if (is.null(aa$rsid) && !is.null(aa$name)) aa$rsid <- as.character(aa$name)
                        if (is.null(aa$position) && !is.null(aa$pos)) aa$position <- aa$pos }
    if (is.null(aa)) next
    aa <- aa[!is.na(aa$beta) & !is.na(aa$se), c("rsid","beta","se","position")]
    m <- merge(ap, aa, by = "rsid", suffixes = c(".p",".a"))
    if (nrow(m) < 3) { message("[G2-coloc] ", prow$protein_id, " ", snp, " 窗口交集=", nrow(m), " (<3, 跳过 abf)"); next }
    n_p <- if (!is.null(prow$n_samples)) prow$n_samples else 3301
    maf_p <- if (!is.null(m$eaf)) m$eaf else rep(0.5, nrow(m))
    d1 <- list(beta = m$beta.p, varbeta = m$se.p^2, snp = m$rsid, position = as.integer(m$position.p),
               MAF = maf_p, N = n_p, type = "quant")
    d2 <- list(beta = m$beta.a, varbeta = m$se.a^2, snp = m$rsid, position = as.integer(m$position.a),
               N = AD_N, type = "cc")
    cl <- tryCatch(coloc::coloc.abf(dataset1 = d1, dataset2 = d2, p1 = 1e-4, p2 = 1e-4),
                   error = function(e) { message("[G2-coloc] abf err: ", conditionMessage(e)); NULL })
    if (is.null(cl)) next
    s <- cl$summary
    out_list[[snp]] <- data.frame(protein = prow$protein_id, target = prow$olink_target,
      lead_snp = snp, chr = chr, pos = pos, n_snps = nrow(m),
      PP.H4 = unname(s["PP.H4.abf"]), coloc_pass = unname(s["PP.H4.abf"]) > THRESH$coloc_pph4,
      stringsAsFactors = FALSE)
  }
  if (length(out_list) == 0) NULL else dplyr::bind_rows(out_list)
}
coloc_results <- list()
for (i in seq_len(nrow(protein_map))) {
  cr <- tryCatch(coloc_protein(protein_map[i, ], ad_out_id),
                 error = function(e) { message("[G2] coloc ", protein_map$protein_id[i], " err: ", conditionMessage(e)); NULL })
  if (!is.null(cr)) coloc_results[[protein_map$protein_id[i]]] <- cr
}
coloc_df <- if (length(coloc_results) > 0) dplyr::bind_rows(coloc_results) else NULL
if (!is.null(coloc_df)) {
  coloc_summary <- coloc_df %>% group_by(protein, target) %>%
    summarise(coloc_pph4 = max(PP.H4, na.rm = TRUE), coloc_pass = any(coloc_pass, na.rm = TRUE),
              n_loci = n(), .groups = "drop")
  mediation <- mediation %>% left_join(coloc_summary, by = c("protein","target"))
  message("[G2] coloc PP.H4>0.80 蛋白数: ", sum(coloc_summary$coloc_pass, na.rm = TRUE), " / ", nrow(coloc_summary))
} else {
  mediation$coloc_pph4 <- NA_real_; mediation$coloc_pass <- NA
  message("[G2] 无蛋白完成 coloc 复核。")
}

## ---- 5. 反向证伪: AD → 蛋白 → 失眠 ----
rows_rev <- list()
for (i in seq_len(nrow(protein_map))) {
  prow <- protein_map[i, ]; pid <- prow$protein_id
  s1r <- tryCatch(ivw_est_protein(exp_id_or_row = ad_out_id, out_id_or_row = prow,
                                  exp_is_protein = FALSE, out_is_protein = TRUE), error = function(e) NULL)
  if (is.null(s1r)) next
  s2r <- tryCatch(ivw_est_protein(exp_id_or_row = prow, out_id_or_row = insomnia_exp_id,
                                  exp_is_protein = TRUE, out_is_protein = FALSE), error = function(e) NULL)
  if (is.null(s2r)) next
  rows_rev[[pid]] <- data.frame(protein = pid, target = prow$olink_target,
    b1_rev = s1r$b, se1_rev = s1r$se, p1_rev = s1r$p, n1_rev = s1r$n_snps,
    b2_rev = s2r$b, se2_rev = s2r$se, p2_rev = s2r$p, n2_rev = s2r$n_snps, stringsAsFactors = FALSE)
}
if (length(rows_rev) > 0) {
  mediation_rev <- dplyr::bind_rows(rows_rev) %>%
    mutate(indirect_rev = b1_rev*b2_rev,
           se_ind_rev = sqrt(b2_rev^2*se1_rev^2 + b1_rev^2*se2_rev^2),
           p_ind_rev = 2*pnorm(-abs(indirect_rev)/se_ind_rev),
           fdr_rev = p.adjust(p_ind_rev, method = "fdr")) %>% arrange(p_ind_rev)
  direction_cmp <- mediation %>% select(protein, target, p_ind, fdr, indirect) %>%
    left_join(mediation_rev %>% select(protein, p_ind_rev, fdr_rev, indirect_rev), by = "protein") %>%
    mutate(fwd_sig = fdr < THRESH$protein_fdr,
           rev_sig = (!is.na(fdr_rev)) & (fdr_rev < THRESH$protein_fdr),
           direction_support = fwd_sig & !rev_sig)
  message("[G2-rev] 正向显著且反向不显著(支持方向)蛋白数: ", sum(direction_cmp$direction_support, na.rm = TRUE))
} else { mediation_rev <- NULL; direction_cmp <- NULL }

## ---- 6. 保存 ----
saveRDS(list(mediation = mediation, sig = sig, coloc_df = coloc_df,
             mediation_rev = mediation_rev, direction_cmp = direction_cmp),
        file.path(G2_OUT, "G2_protein_mediation.rds"))
write.csv(mediation, file.path(G2_OUT, "G2_mediation_table.csv"), row.names = FALSE)
if (!is.null(mediation_rev)) write.csv(mediation_rev, file.path(G2_OUT, "G2_mediation_reverse.csv"), row.names = FALSE)
if (!is.null(coloc_df)) write.csv(coloc_df, file.path(G2_OUT, "G2_protein_coloc.csv"), row.names = FALSE)
if (!is.null(direction_cmp)) write.csv(direction_cmp, file.path(G2_OUT, "G2_direction_comparison.csv"), row.names = FALSE)
message("[G2] 完成。结果见 ", G2_OUT, "/G2_protein_mediation.rds 等")
