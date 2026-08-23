# =====================================================================
# 01_bidirectional_mr_coloc.R - G1: MR +
# ---------------------------------------------------------------------
# : IVW | : MR-Egger / / / MR-PRESSO /
# =====================================================================
source("00_config.R")
library(TwoSampleMR); library(ieugwasr); library(coloc)
options(encoding = "UTF-8")   # ()
set.seed(20240721)   # : (cause MCMC / MR-PRESSO )

# GWAS_ID$ad = ieu-b-2 Kunkle/IGAP, UKB ->
# GWAS_ID$ad_alt = Bellenguez 2022 ebi-a-GCST90027158, UKB ->
if (is.null(GWAS_ID$ad) || identical(GWAS_ID$ad, "PENDING_VERIFY") ||
    (is.character(GWAS_ID$ad) && GWAS_ID$ad == "PENDING_VERIFY")) {
  stop("[G1] GWAS_ID$ad  PENDING_VERIFY . ",
       " R  00b_verify_gwas.R  AD ID ",
       "( gwas_ids_resolved.json) . ")
}
# ad_altBellenguez: .
RUN_REPLICATION <- FALSE
if (is.null(GWAS_ID$ad_alt) || is.na(GWAS_ID$ad_alt) ||
    identical(GWAS_ID$ad_alt, "PENDING_VERIFY")) {
  message("[G1] : ad_alt(Bellenguez), ( ieu-b-2). ")
} else {
  RUN_REPLICATION <- TRUE
  message("[G1] : ad_alt = ", GWAS_ID$ad_alt,
          " (Bellenguez 2022,  UKB ,  MRlap/cause )")
}
# : MRlap/cause GWAS TRUE
# / -> FALSE, saveRDS , Limitations .
overlap_correction_run <- FALSE

# ---- 0b0. clean GWAS ; data/raw
# data/raw /data , .
DIR_RAW_LOCAL <- "./output/data/raw"
LOCAL_CLEAN <- list(
  "ukb-b-3957"          = file.path(DIR_RAW_LOCAL, "ukb-b-3957", "ukb-b-3957.clean.tsv.gz"),
  "ieu-b-2"             = file.path(DIR_RAW_LOCAL, "ieu-b-2", "ieu-b-2.clean.tsv.gz"),
  "ebi-a-GCST90027158"  = file.path(DIR_RAW_LOCAL, "ebi-a-GCST90027158", "GCST90027158_buildGRCh38.dedup.tsv.gz")
)
USE_LOCAL_GWAS <- TRUE   # TRUE= clean (); FALSE= OpenGWAS API

# ---- 0b0a. clean beta/se/snp/A1/A2/N/chr/pos/icase/icontrol
# : clean SNP CHR BP A1 A2 beta se p n [ncase ncontrol | n_cases n_controls]
.LocalCleanCache <- if (exists(".LocalCleanCache", envir = globalenv()))
  get(".LocalCleanCache", envir = globalenv()) else new.env(hash = TRUE, parent = emptyenv())
read_local_clean <- function(id, label = "local") {
  # * : GWAS fread , /+coloc OOM
  if (exists(id, envir = .LocalCleanCache)) return(get(id, envir = .LocalCleanCache))
  lf <- if (id %in% names(LOCAL_CLEAN)) LOCAL_CLEAN[[id]] else NULL
  if (is.null(lf) || !file.exists(lf)) {
    message("[", label, "]  clean (", id, "): ",
            ifelse(is.null(lf), "<>", lf))
    return(NULL)
  }
  if (!requireNamespace("data.table", quietly = TRUE)) {
    message("[", label, "] data.table ,  clean . ")
    return(NULL)
  }
  dt <- tryCatch(data.table::fread(lf, sep = "\t", header = TRUE, showProgress = FALSE,
                                   data.table = FALSE),
                 error = function(e) { message("[", label, "]  ", lf, " : ",
                                               conditionMessage(e)); NULL })
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

# ---- 0b0b. harmonize: clean MR dat
# p<pval SNP ; SNP ; ambiguous
# harmonise_data action="none". , IEU/LD .
build_harmonized_local <- function(exp_id, out_id, pval = 5e-8, label = "harmonize-local") {
  exp <- read_local_clean(exp_id, label)
  out <- read_local_clean(out_id, label)
  if (is.null(exp) || is.null(out)) {
    message("[", label, "] , (", exp_id, "->", out_id, ")")
    return(NULL)
  }
  exp_iv <- exp[!is.na(exp$p) & exp$p < pval & exp$p > 0, ]
  message("[", label, "] ", exp_id, "  SNP(p<", format(pval, digits = 2), ")=",
          nrow(exp_iv), "; =", nrow(exp))
  if (nrow(exp_iv) == 0) {
    message("[", label, "]  SNP, . ")
    return(NULL)
  }
  m <- merge(exp_iv, out, by = "snp", suffixes = c(".exposure", ".outcome"), all.x = TRUE)
  m <- m[!is.na(m$beta.outcome) & !is.na(m$se.outcome), ]
  if (nrow(m) == 0) {
    message("[", label, "]  SNP , . ")
    return(NULL)
  }
  ea_e <- m$A1.exposure; oa_e <- m$A2.exposure
  ea_o <- m$A1.outcome;  oa_o <- m$A2.outcome
  same <- (ea_e == ea_o) & (oa_e == oa_o)
  flip <- (ea_e == oa_o) & (oa_e == ea_o)
  ambiguous <- !(same | flip)
  ambiguous[is.na(ambiguous)] <- TRUE   #  NA ->  ambiguous 
  m$beta.outcome[flip] <- -m$beta.outcome[flip]
  m <- m[!ambiguous, ]
  if (nrow(m) == 0) {
    message("[", label, "]  SNP, . ")
    return(NULL)
  }
  exp_N <- if (!is.null(exp$N)) exp$N[1] else NA_real_
  out_N <- if (!is.null(out$N)) out$N[1] else NA_real_
  exp_ic <- if (!is.null(exp$icase)) exp$icase[1] else NA_real_
  exp_oc <- if (!is.null(exp$icontrol)) exp$icontrol[1] else NA_real_
  out_ic <- if (!is.null(out$icase)) out$icase[1] else NA_real_
  out_oc <- if (!is.null(out$icontrol)) out$icontrol[1] else NA_real_
  n <- nrow(m)
  dat <- data.frame(
    id.exposure = rep(exp_id, n), id.outcome = rep(out_id, n),
    exposure = rep(exp_id, n), outcome = rep(out_id, n),
    SNP = m$snp,
    chr.exposure = m$chr.exposure, pos.exposure = m$pos.exposure,
    chr.outcome = m$chr.outcome, pos.outcome = m$pos.outcome,
    effect_allele.exposure = m$A1.exposure, other_allele.exposure = m$A2.exposure,
    effect_allele.outcome = m$A1.outcome,   other_allele.outcome = m$A2.outcome,
    beta.exposure = m$beta.exposure, se.exposure = m$se.exposure,
    beta.outcome = m$beta.outcome,   se.outcome = m$se.outcome,
    eaf.exposure = NA_real_, eaf.outcome = NA_real_,
    pval.exposure = m$p.exposure, pval.outcome = m$p.outcome,
    ncase.exposure = rep(exp_ic, n), ncontrol.exposure = rep(exp_oc, n),
    ncase.outcome = rep(out_ic, n), ncontrol.outcome = rep(out_oc, n),
    samplesize.exposure = rep(exp_N, n), samplesize.outcome = rep(out_N, n),
    stringsAsFactors = FALSE,
    mr_keep = rep(TRUE, n))
  rownames(dat) <- NULL
  message("[", label, "]  harmonize : ", exp_id, "->", out_id,
          " (", nrow(dat), "  SNP, ", sum(ambiguous), " ambiguous )")
  dat
}

# ---- 0b. GWAS helper MRlap/cause , clumped IV
# <PREFIX>_LOC, IEU SNP .
# : beta/se/snp/A1/A2. -> NULL.
load_full_gwas <- function(id, loc_env, label = "fullgwas") {
  loc <- Sys.getenv(loc_env)
  d <- if (nzchar(loc) && file.exists(loc)) {
    tryCatch(read.table(loc, header = TRUE, stringsAsFactors = FALSE),
             error = function(e) { message("[", label, "]  GWAS (",
                                           loc, "): ", conditionMessage(e)); NULL })
    } else {
    # variants_chrposchr=1:22, from=1, to=250e6 /.
    # MRlap/cause GWAS ; , .
    message("[", label, "] . GWAS (", loc_env,
            "), ; . ")
    d <- NULL
  }
  if (is.null(d)) return(NULL)
  d <- as.data.frame(d); nm <- names(d)
  beta <- if ("beta" %in% nm) d$beta else if ("beta.out" %in% nm) d$beta.out else d$beta.exposure
  se   <- if ("se"   %in% nm) d$se   else if ("se.out"   %in% nm) d$se.out   else d$se.exposure
  snp  <- if ("rsid" %in% nm) d$rsid else if ("SNP" %in% nm) d$SNP else d$name
  a1   <- if ("A1" %in% nm) d$A1 else if ("effect_allele" %in% nm) d$effect_allele else d$effect_allele.exposure
  a2   <- if ("A2" %in% nm) d$A2 else if ("other_allele" %in% nm) d$other_allele else d$other_allele.exposure
  if (any(sapply(list(beta, se, snp, a1, a2), is.null))) {
    message("[", label, "]  GWAS (", id, "), . ")
    return(NULL)
  }
  # MRlap N/chr/pos, NA -> MRlap
  NN  <- if ("n" %in% nm) d$n else if ("N" %in% nm) d$N else NULL
  chr <- if ("chromosome" %in% nm) d$chromosome
         else if ("chr" %in% nm) d$chr else NULL
  pos <- if ("position" %in% nm) d$position
         else if ("pos" %in% nm) d$pos else NULL
  out <- data.frame(beta = beta, se = se, snp = as.character(snp),
             A1 = as.character(a1), A2 = as.character(a2), stringsAsFactors = FALSE)
  if (!is.null(NN))  out$N  <- NN
  if (!is.null(chr)) out$chr <- chr
  if (!is.null(pos)) out$pos <- pos
  out
}

# : ieugwasr::associationsid -> data/gwas/<id>.rds + <id>.meta.rds /ID
DIR_DATA <- if (exists("DIR_DATA") && is.character(DIR_DATA) && nzchar(DIR_DATA)) {
  DIR_DATA
} else {
  file.path(dirname(DIR_OUT), "data")
}
# OpenGWAS API GWAS OPENGWAS_JWT; 2024-05 API
# freeze_gwas : CDN , ieugwasr::associations chr:pos .
# variants=, id=-- bug; OpenGWAS rsid/a1/a0/beta/se/....
download_full_gwas_api <- function(id, label = "freeze-api") {
  if (!requireNamespace("ieugwasr", quietly = TRUE)) {
    message("[", label, "] ieugwasr ,  API  GWAS. ")
    return(NULL)
  }
  jwt <- tryCatch(ieugwasr::get_opengwas_jwt(), error = function(e) "")
  if (!nzchar(jwt)) {
    message("[", label, "]  OPENGWAS_JWT(),  API  GWAS . ")
    return(NULL)
  }
  if (requireNamespace("httr", quietly = TRUE)) httr::set_config(httr::timeout(60))
  message("[", label, "]  CDN ,  OpenGWAS API (1Mb ) GWAS: ", id, " ...")
  # : GWAS . OpenGWAS GWAS build
  # gwasinfoid$build ieu-b-2 = HG19/GRCh37; ukb-b-3957 GRCh38.
  chr_len_hg19 <- c(249250621, 243199373, 198022430, 191154276, 180915260, 171115067,
                    159138663, 146364022, 141213431, 135534747, 135006516, 133851895,
                    115169878, 107349540, 102531392, 90354753, 81195210, 78077248,
                    59128983, 63025520, 48129895, 51304466)
  chr_len_hg38 <- c(248956422, 242193529, 198295559, 190214555, 181538259, 170805979,
                    159345973, 145138636, 138394717, 133797422, 135086622, 133275309,
                    114364328, 107043718, 101991189, 90338345, 83257441, 80373285,
                    58617616, 64444167, 46709983, 50818468)
  build <- tryCatch(as.character(ieugwasr::gwasinfo(id)$build), error = function(e) "")
  if (grepl("GRCh38|HG38", build, ignore.case = TRUE)) {
    chr_len <- chr_len_hg38; btxt <- "GRCh38"
  } else {
    chr_len <- chr_len_hg19; btxt <- "GRCh37/(GRCh37)"
  }
  names(chr_len) <- 1:22
  message("[", label, "] ", id, " : ", btxt, " (build=", build, ")")
  chunk_bp <- 1e6   # 1Mb 
  pieces <- list(); pulled_rows <- 0L
  for (chr in 1:22) {
    L <- chr_len[as.character(chr)]; start <- 1L
    while (start <= L) {
      e <- min(start + chunk_bp - 1L, L)
      variants <- paste0(chr, ":", start, "-", e)
      p <- tryCatch(ieugwasr::associations(variants = variants, id = id),
                    error = function(e2) { message("[", label, "] chr", chr, ":",
                      start, "-", e, " : ", conditionMessage(e2)); NULL })
      if (!is.null(p) && nrow(p) > 0) {
        pieces[[length(pieces) + 1]] <- as.data.frame(p)
        pulled_rows <- pulled_rows + nrow(p)
      }
      start <- e + 1L
      Sys.sleep(0.3)   # ,  OpenGWAS rate limit
    }
    message("[", label, "] chr", chr, " ,  ", length(pieces),
            "  / ", pulled_rows, " ")
  }
  if (length(pieces) == 0) { message("[", label, "] API , . "); return(NULL) }
  out <- tryCatch(do.call(rbind, pieces), error = function(e) NULL)
  if (is.null(out) || nrow(out) == 0) return(NULL)
  if ("rsid" %in% names(out)) out <- out[!duplicated(out$rsid), ]
  out
}

freeze_gwas <- function(id, label = "freeze") {
  if (is.null(id) || !is.character(id) || !nzchar(id) || is.na(id)) {
    message("[", label, "]  GWAS ID(=", id, "), . ")
    return(NULL)
  }
  # * clean : data/raw , CDN/API.
  if (USE_LOCAL_GWAS) {
    loc <- tryCatch(read_local_clean(id, paste0(label, "-local")),
                    error = function(e) NULL)
    if (!is.null(loc) && nrow(loc) > 0) {
      message("[", label, "]  clean (GWAS=", id, ", ", nrow(loc),
              " SNPs) -> . ")
      return(loc)
    }
  }
  base_dir <- file.path(DIR_DATA, "gwas")
  dir.create(base_dir, showWarnings = FALSE, recursive = TRUE)
  rds_path  <- file.path(base_dir, paste0(id, ".rds"))
  meta_path <- file.path(base_dir, paste0(id, ".meta.rds"))
  if (file.exists(rds_path)) {
    d <- tryCatch(readRDS(rds_path),
                  error = function(e) { message("[", label, "]  GWAS (",
                                                rds_path, "): ", conditionMessage(e)); NULL })
    if (!is.null(d)) {
      message("[", label, "]  GWAS: ", id, " (", nrow(d), " SNPs;  ",
              rds_path, ")")
      return(d)
    }
  }
  # -> OpenGWAS CDN JWT .
  # : ieugwasr::associationsvariants, id, ... variants
  # , GWAS; MRlap/cause GWAS
  # https://gwas.mrcieu.ac.uk/files/<id>/<id>.tab.gz data.table::fread.
  if (!requireNamespace("data.table", quietly = TRUE)) {
    message("[", label, "] data.table ,  GWAS , . ")
    return(NULL)
  }
  url <- paste0("https://gwas.mrcieu.ac.uk/files/", id, "/", id, ".tab.gz")
  message("[", label, "]  GWAS(): ", id, " ...")
  d <- tryCatch({
    tmp <- tempfile(fileext = ".tab.gz")
    dl <- download.file(url, tmp, mode = "wb", quiet = TRUE)
    if (!file.exists(tmp) || file.info(tmp)$size < 10L) stop("")
    first_line <- tryCatch(readLines(tmp, n = 1, warn = FALSE), error = function(e) "")
    if (grepl("^\\s*<", first_line)) stop(" HTML (404/),  GWAS ")
    dt <- data.table::fread(tmp, sep = "\t", header = TRUE,
                            showProgress = FALSE, data.table = FALSE)
    if (is.null(dt) || nrow(dt) == 0) stop("")
    file.remove(tmp)
    as.data.frame(dt)
  }, error = function(e) {
    message("[", label, "]  GWAS (", id, "): ", conditionMessage(e))
    NULL
  })
  if (is.null(d) || nrow(d) == 0) {
    # 2 : OpenGWAS API OPENGWAS_JWT; CDN
    d <- tryCatch(download_full_gwas_api(id, label),
                  error = function(e) { message("[", label, "] API  GWAS : ",
                                                conditionMessage(e)); NULL })
  }
  if (is.null(d) || nrow(d) == 0) {
    message("[", label, "] GWAS(", id, ") ( CDN  API .) -> (). ")
    return(NULL)
  }
  tryCatch({
    saveRDS(d, rds_path)
    saveRDS(list(id = id, source = "OpenGWAS static CDN",
                 url = url, downloaded = as.character(Sys.Date()),
                 n_snp = nrow(d)), meta_path)
    message("[", label, "]  GWAS: ", id, " (", nrow(d), " SNPs) -> ", rds_path)
  }, error = function(e) {
    message("[", label, "]  GWAS (", rds_path, "): ", conditionMessage(e))
  })
  d
}

# ---- 0c. GWAS helper MRlap/cause ; freeze_gwas: CDN , API
# : beta/se/snp/A1/A2 N/chr/pos/icase/icontrol.
# : beta->beta/beta.out/beta.exposure; se->se/se.out/se.exposure
# snp->rsid/SNP/name; A1->A1/a1/ea/effect_allele; A2->A2/a0/oa/other_allele.
fetch_full_gwas <- function(id, label = "fullgwas") {
  if (!requireNamespace("ieugwasr", quietly = TRUE)) {
    message("[", label, "] ieugwasr ,  GWAS, . ")
    return(NULL)
  }
  if (is.null(id) || !is.character(id) || !nzchar(id) || is.na(id)) {
    message("[", label, "]  GWAS ID(=", id, "), . ")
    return(NULL)
  }
  d <- freeze_gwas(id, label)
  if (is.null(d) || nrow(d) == 0) {
    message("[", label, "]  GWAS(", id, ") ., (). ")
    return(NULL)
  }
  d <- as.data.frame(d); nm <- names(d)
  beta <- if ("beta" %in% nm) d$beta
          else if ("beta.out" %in% nm) d$beta.out
          else if ("beta.exposure" %in% nm) d$beta.exposure else NULL
  se   <- if ("se" %in% nm) d$se
          else if ("se.out" %in% nm) d$se.out
          else if ("se.exposure" %in% nm) d$se.exposure else NULL
  snp  <- if ("rsid" %in% nm) d$rsid
          else if ("SNP" %in% nm) d$SNP
          else if ("snp" %in% nm) d$snp
          else if ("name" %in% nm) d$name else NULL
  a1   <- if ("A1" %in% nm) d$A1
          else if ("a1" %in% nm) d$a1
          else if ("ea" %in% nm) d$ea
          else if ("effect_allele" %in% nm) d$effect_allele else NULL
  a2   <- if ("A2" %in% nm) d$A2
          else if ("a0" %in% nm) d$a0
          else if ("oa" %in% nm) d$oa
          else if ("nea" %in% nm) d$nea
          else if ("other_allele" %in% nm) d$other_allele else NULL
  if (any(sapply(list(beta, se, snp, a1, a2), is.null))) {
    message("[", label, "]  GWAS (", id, "): =",
            paste(nm, collapse = ","), "; . ")
    return(NULL)
  }
  # MRlap N/chr/pos; ieugwasr::associations , NA.
  NN  <- if ("n" %in% nm) as.numeric(d$n) else NULL
  chr <- if ("chromosome" %in% nm) as.integer(d$chromosome)
         else if ("chr" %in% nm) as.integer(d$chr) else NULL
  pos <- if ("position" %in% nm) as.integer(d$position)
         else if ("pos" %in% nm) as.integer(d$pos) else NULL
  icase    <- if ("icase"    %in% nm) as.numeric(d$icase) else NULL
  icontrol <- if ("icontrol" %in% nm) as.numeric(d$icontrol) else NULL
  out <- data.frame(beta = as.numeric(beta), se = as.numeric(se),
             snp = as.character(snp),
             A1 = as.character(a1), A2 = as.character(a2),
             stringsAsFactors = FALSE)
  if (!is.null(NN))  out$N  <- NN
  if (!is.null(chr)) out$chr <- chr
  if (!is.null(pos)) out$pos <- pos
  # icase/icontrol: coloctype=cc s GWAS_S
  if (!is.null(icase))    out$icase <- icase
  if (!is.null(icontrol)) out$icontrol <- icontrol
  out
}

# out_dir 00_config DIR_OUT, "results"; dir.create .
# -> ; -> read rbind, NA, /.
append_results_csv <- function(df, fname) {
  out_dir <- if (exists("DIR_OUT") && is.character(DIR_OUT) &&
                 length(DIR_OUT) == 1 && nzchar(DIR_OUT)) DIR_OUT else "results"
  dir.create(out_dir, showWarnings = FALSE, recursive = TRUE)
  path <- file.path(out_dir, fname)
  if (!file.exists(path)) {
    write.csv(df, path, row.names = FALSE)
  } else {
    existing <- tryCatch(read.csv(path, stringsAsFactors = FALSE),
                         error = function(e) NULL)
    if (is.null(existing) || nrow(existing) == 0) {
      write.csv(df, path, row.names = FALSE)
    } else {
      for (c in setdiff(names(existing), names(df))) df[[c]] <- NA
      for (c in setdiff(names(df), names(existing))) existing[[c]] <- NA
      combined <- tryCatch(rbind(existing, df[, names(existing), drop = FALSE]),
                           error = function(e) {
                             message("[append_csv] rbind (", fname, "): ",
                                     conditionMessage(e), "; . ")
                             df
                           })
      write.csv(combined, path, row.names = FALSE)
    }
  }
  message("[append_csv] : ", path)
  invisible(path)
}

# SD trait coloc sdy. TODO: 00b/UK Biobank
# ; NA -> d1 sdy, coloc .
INSOMNIA_SDY <- NA_real_

extract_exp <- function(id, outcome_id, pval = 5e-8) {
  exp <- extract_instruments(id, p1 = pval,
                             r2 = THRESH$clump_r2, kb = THRESH$clump_kb)
  # : clumped IV 42 API
  out <- extract_outcome_data_batched(snps = exp$SNP, outcomes = outcome_id)
  dat <- harmonise_data(exp, out)
  return(dat)
}

get_harmonized <- function(exp_id, out_id, pval = 5e-8, label = "harmonize") {
  base_dir <- file.path(DIR_DATA, "extracted")
  dir.create(base_dir, showWarnings = FALSE, recursive = TRUE)
  cache_path <- file.path(base_dir, paste0(exp_id, "__", out_id, ".rds"))
  if (!USE_LOCAL_GWAS && file.exists(cache_path)) {
    dat <- tryCatch(readRDS(cache_path),
                    error = function(e) { message("[", label, "]  harmonized (",
                                                  cache_path, "): ", conditionMessage(e)); NULL })
    if (!is.null(dat)) {
      message("[", label, "]  harmonized: ", exp_id, " -> ", out_id,
              " (", nrow(dat), "  SNP)")
      return(dat)
    }
  }
  # * : clean harmonized dat; API.
  dat <- if (USE_LOCAL_GWAS) {
    build_harmonized_local(exp_id, out_id, pval, label)
  } else {
    extract_exp(exp_id, out_id, pval)
  }
  if (!is.null(dat) && nrow(dat) > 0) {
    tryCatch(saveRDS(dat, cache_path),
             error = function(e) message("[", label, "]  harmonized : ",
                                         conditionMessage(e)))
    message("[", label, "]  SNP : ", nrow(dat), " (", exp_id, " -> ", out_id, ")")
  }
  dat
}

dat_fwd <- get_harmonized(GWAS_ID$insomnia, GWAS_ID$ad)   #  -> AD
dat_rev <- get_harmonized(GWAS_ID$ad, GWAS_ID$insomnia)   # AD   -> 

# IVW + MR-Egger + + +
# Steiger + MR-PRESSO + .
# ⚠️ : BenElsworth 2018 ukb-b-3957 Bellenguez AD UKB
# -> ; ieu-b-2, Kunkle/IGAP UKB , .
# I / IVW. delta IVW .
# ---- MRlap+ cause:G1 OSF §6/§7
# BenElsworth 2018 ukb-b-3957, BellenguezAD UKB -> >5% §4c,.
run_mrlap <- function(dat, label = "mrlap") {
  if (!requireNamespace("MRlap", quietly = TRUE)) {
    message("[", label, "] MRlap ,(: remotes::install_github('n-mounier/MRlap'))")
    return(NULL)
  }
  # harmonized dat / ID id.exposure / id.outcome
  exp_id <- tryCatch(unique(dat$id.exposure)[1], error = function(e) NULL)
  out_id <- tryCatch(unique(dat$id.outcome)[1], error = function(e) NULL)
  if (is.null(exp_id) || is.null(out_id) || !nzchar(exp_id) || !nzchar(out_id)) {
    message("[", label, "]  dat . ID, MRlap . ")
    return(NULL)
  }
  # * MRlap LDSC ; LDld_proxies=TRUE.
  # MRlap SNP clumped SNP - OpenGWAS, .
  exp_sum <- fetch_full_gwas(exp_id, label)
  out_sum <- fetch_full_gwas(out_id, label)
  if (is.null(exp_sum) || is.null(out_sum)) {
    message("[", label, "] . GWAS -> MRlap (); Limitations . ")
    return(NULL)
  }
  # * MRlap::MRlap MRlap 0.0.3.3: exposure, exposure_name, outcome, outcome_name
  # ld, {chr}.l2.ldscore.gz, hm3SNP - .
  # LD : Zenodo 1000G Phase3 EUR LD scores + hm3_no_MHC SNP .
  LD_REF_DIR <- "./output/ld_ref/LDscore"
  HM3_FILE   <- "./output/ld_ref/hm3_no_MHC.list.txt"
  if (!file.exists(LD_REF_DIR) || !file.exists(file.path(LD_REF_DIR, "1.l2.ldscore.gz")) ||
      !file.exists(HM3_FILE)) {
    message("[", label, "] LD (ld=", LD_REF_DIR, ", hm3=", HM3_FILE, "), MRlap . ")
    return(NULL)
  }
  message("[", label, "] MRlap::MRlap  (ld=", LD_REF_DIR, ", hm3=", HM3_FILE, ")...")
  fit <- tryCatch(
    MRlap::MRlap(exposure = exp_sum, exposure_name = as.character(exp_id),
                 outcome  = out_sum, outcome_name  = as.character(out_id),
                 ld  = LD_REF_DIR, hm3 = HM3_FILE),
    error = function(e) { message("[", label, "] MRlap::MRlap : ", conditionMessage(e)); NULL })
  if (is.null(fit)) {
    message("[", label, "] MRlap , (). ")
    return(NULL)
  }
  mc <- tryCatch(fit$MRcorrection, error = function(e) NULL)
  if (is.null(mc)) {
    message("[", label, "] MRlap ( $MRcorrection), . ")
    return(NULL)
  }
  b_corr  <- as.numeric(mc$corrected_effect)[1]
  se_corr <- as.numeric(mc$corrected_effect_se)[1]
  p_corr  <- as.numeric(mc$corrected_effect_p)[1]
  b_obs   <- as.numeric(mc$observed_effect)[1]
  se_obs  <- as.numeric(mc$observed_effect_se)[1]
  p_obs   <- as.numeric(mc$observed_effect_p)[1]
  p_diff  <- as.numeric(mc$p_difference)[1]   #  vs  ()
  n_ivs   <- as.integer(mc$m_IVs)[1]
  ci_l <- if (is.finite(b_corr) && is.finite(se_corr)) b_corr - 1.96 * se_corr else NA_real_
  ci_u <- if (is.finite(b_corr) && is.finite(se_corr)) b_corr + 1.96 * se_corr else NA_real_
  res_df <- data.frame(
    label = label, exp_id = exp_id, out_id = out_id,
    mrlap_corrected_beta = b_corr, mrlap_corrected_se = se_corr,
    mrlap_corrected_p = p_corr,
    mrlap_corrected_ci_lower = ci_l, mrlap_corrected_ci_upper = ci_u,
    mrlap_observed_beta = b_obs, mrlap_observed_se = se_obs, mrlap_observed_p = p_obs,
    mrlap_p_difference = p_diff, n_ivs = n_ivs,
    n_snp_exp = nrow(exp_sum), n_snp_out = nrow(out_sum),
    stringsAsFactors = FALSE)
  append_results_csv(res_df, "G1_mrlap.csv")
  overlap_correction_run <<- TRUE
  message("[", label, "] MRlap . corrected_beta=",
          if (is.finite(b_corr)) signif(b_corr, 4) else "<NA>",
          " se=", if (is.finite(se_corr)) signif(se_corr, 4) else "<NA>",
          " p_diff=", if (is.finite(p_diff)) signif(p_diff, 3) else "<NA>",
          " n_IVs=", if (is.finite(n_ivs)) n_ivs else "<NA>")
  list(success = TRUE, label = label, exp_id = exp_id, out_id = out_id,
       corrected_beta = b_corr, corrected_se = se_corr, corrected_p = p_corr,
       corrected_ci_lower = ci_l, corrected_ci_upper = ci_u,
       observed_beta = b_obs, observed_se = se_obs, observed_p = p_obs,
       p_difference = p_diff, n_ivs = n_ivs,
       n_snp_exp = nrow(exp_sum), n_snp_out = nrow(out_sum))
}

run_cause <- function(exp_id, out_id, label = "cause") {
  if (!requireNamespace("cause", quietly = TRUE)) {
    message("[", label, "] cause ,(: install.packages('cause', repos='https://mrcieu.r-universe.dev')  remotes::install_github('jean997/cause@v1.2.0'))")
    return(NULL)
  }
  if (is.null(exp_id) || is.null(out_id) || !nzchar(exp_id) || !nzchar(out_id)) {
    message("[", label, "]  GWAS ID(exp=", exp_id, ", out=", out_id, "), cause . ")
    return(NULL)
  }
  # GWAS clumped SNP - OpenGWAS, .
  e <- fetch_full_gwas(exp_id, "cause-exp")
  o <- fetch_full_gwas(out_id, "cause-out")
  if (is.null(e) || is.null(o)) {
    message("[", label, "] . GWAS -> cause (); Limitations . ")
    return(NULL)
  }
  # cause::gwas_merge snp/beta_hat/se/A1/A2
  e <- data.frame(snp = e$snp, beta_hat = e$beta, se = e$se, A1 = e$A1, A2 = e$A2,
                  stringsAsFactors = FALSE)
  o <- data.frame(snp = o$snp, beta_hat = o$beta, se = o$se, A1 = o$A1, A2 = o$A2,
                  stringsAsFactors = FALSE)
  # ---- 1 gwas_merge: , cause_data
  # cause v1.2.0+ gwas_merge LD ; LD ld_prune 3.
  X <- tryCatch(
    cause::gwas_merge(e, o,
                      snp_name_cols = c("snp", "snp"),
                      beta_hat_cols = c("beta_hat", "beta_hat"),
                      se_cols       = c("se", "se"),
                      A1_cols       = c("A1", "A1"),
                      A2_cols       = c("A2", "A2"),
                      compute_pvals = TRUE),
    error = function(e2) { message("[", label, "] gwas_merge : ",
                                   conditionMessage(e2)); NULL })
  if (is.null(X)) return(NULL)
  # ---- 2 est_cause_params: nuisance rho
  # X e/o GWAS , varlist = X$snp clumped SNP.
  # nuisance rho/, cause
  varlist <- tryCatch({
    s <- X$snp
    ns <- if (length(s) > 500000) 500000 else length(s)
    if (length(s) > ns) sample(s, ns) else s
  }, error = function(e2) NULL)
  params <- tryCatch(
    cause::est_cause_params(X, variants = varlist),
    error = function(e2) { message("[", label, "] est_cause_params : ",
                                   conditionMessage(e2)); NULL })
  if (is.null(params)) return(NULL)
  # ---- 3 LD : ieugwasr::ld_clumpPlink + EUR , cause
  # plink/genetics.binaRies -> SNPvarlist, .
  variants <- tryCatch({
    if (requireNamespace("ieugwasr", quietly = TRUE) &&
        requireNamespace("genetics.binaRies", quietly = TRUE) &&
        !is.null(X$p1)) {
      cl <- ieugwasr::ld_clump(dat = data.frame(rsid = X$snp, pval = X$p1),
                               clump_r2 = 0.01, clump_p = 1e-3,
                               plink_bin = genetics.binaRies::get_plink_binary(),
                               pop = "EUR")
      if (!is.null(cl) && nrow(cl) > 0) cl$rsid else varlist
    } else {
      varlist
    }
  }, error = function(e2) {
    message("[", label, "] ld_clump ,  SNP: ", conditionMessage(e2))
    varlist
  })
  fit <- tryCatch(
    cause::cause(X = X, variants = variants, param_ests = params),
    error = function(e2) { message("[", label, "] cause() : ",
                                   conditionMessage(e2)); NULL })
  if (is.null(fit)) return(NULL)
  # cause v1.2.0 causality; summaryfitp
  # fit$elpdz : vs / .
  summ <- tryCatch(summary(fit), error = function(e2) NULL)
  elpd <- tryCatch(fit$elpd, error = function(e2) NULL)
  causal_p <- NA_real_
  if (!is.null(summ) && !is.null(summ$p.value)) causal_p <- as.numeric(summ$p.value)
  if (is.na(causal_p) && !is.null(elpd) && "z" %in% names(elpd) && is.finite(elpd$z[1])) {
    causal_p <- 2 * pnorm(-abs(elpd$z[1]))
  }
  decision <- if (is.na(causal_p)) {
    "UNKNOWN"
  } else if (causal_p < 0.05) {
    "CAUSAL (.)"
  } else {
    "PLEIOTROPY_OR_SHARING (.)"
  }
  res_df <- data.frame(
    label = label, exp_id = exp_id, out_id = out_id,
    causal_p = causal_p, decision = decision,
    n_snp_merged = nrow(X), n_snp_used = length(variants),
    stringsAsFactors = FALSE)
  append_results_csv(res_df, "G1_cause.csv")
  overlap_correction_run <<- TRUE
  message("[", label, "] cause .  vs .: ", decision,
          " (p=", if (is.na(causal_p)) "<NA>" else signif(causal_p, 3), ")")
  list(success = TRUE, label = label, exp_id = exp_id, out_id = out_id,
       n_snp = length(variants), cause_data = X, params = params, fit = fit,
       summary = summ, elpd = elpd, causal_p = causal_p, decision = decision)
}
RUN_MR_PRESSO <- FALSE  # : , mr_presso 10000; 
run_mr <- function(dat, label) {
  res <- mr(dat, method_list = c("mr_ivw", "mr_egger_regression",
                                 "mr_weighted_median", "mr_weighted_mode"))
  het <- mr_heterogeneity(dat)              # Q / Cochran 
  pleio <- mr_pleiotropy_test(dat)          # Egger ()
  loo <- mr_leaveoneout(dat)                # 
  if (!is.null(dat) && nrow(dat) > 0) {
    dat$f_stat <- (dat$beta.exposure / dat$se.exposure)^2
    f_mean <- mean(dat$f_stat, na.rm = TRUE)
    f_min  <- min(dat$f_stat, na.rm = TRUE)
    message("[", label, "]  F: =", round(f_mean, 2),
            " =", round(f_min, 2),
            if (f_min < THRESH$fstat_min) " ⚠️ (F<10)" else "")
    weak <- dat$SNP[dat$f_stat < THRESH$fstat_min]
  } else { f_mean <- f_min <- NA; weak <- character(0) }
  # MR-PRESSO devtools::install_github"rondolab/MR-PRESSO"
  presso <- NULL
  if (RUN_MR_PRESSO && requireNamespace("MRPRESSO", quietly = TRUE)) {
    presso <- tryCatch(
      MRPRESSO::mr_presso(BetaOutcome = "beta.outcome", BetaExposure = "beta.exposure",
                          SdOutcome = "se.outcome", SdExposure = "se.exposure",
                          data = as.data.frame(dat), OUTLIERtest = TRUE,
                          DISTORTIONtest = TRUE, NbDistribution = 10000,
                          SignifThreshold = 0.05),
      error = function(e) { message("[", label, "] MR-PRESSO : ",
                                    conditionMessage(e)); NULL })
  } else {
    message("[", label, "] MR-PRESSO , (install: rondolab/MR-PRESSO)")
  }
  ivw_row <- res[grepl("variance weighted", res$method, ignore.case = TRUE), ]
  if (nrow(ivw_row) > 0) {
    message("[", label, "] IVW beta = ", round(ivw_row$b, 4),
            " se = ", round(ivw_row$se, 4),
            " p = ", signif(ivw_row$pval, 3))
  } else {
    message("[", label, "]  'IVW' ; : ",
            paste(unique(res$method), collapse = " | "))
  }
  list(res = res, het = het, pleio = pleio, loo = loo,
       presso = presso, f_mean = f_mean, f_min = f_min, weak_iv = weak, dat = dat)
}
fwd <- run_mr(dat_fwd, "->AD")
rev <- run_mr(dat_rev, "AD->")

# directionality_test mr_steiger dat$r.exposure / dat$r.outcome.
# ukb-b-3957 ADieu-b-2-, get_r_from_pn
# get_r_from_lorbeta, eaf, ncase, ncontrol . dat ncase/ncontrol
# ; MR + coloc + OSF §2 .
run_steiger <- function(dat, label) {
  if (is.null(dat) || nrow(dat) == 0) { message("[", label, "] Steiger: dat , . "); return(NULL) }
  comp_r <- function(role) {
    nc  <- dat[[paste0("ncase.", role)]]
    nt  <- dat[[paste0("ncontrol.", role)]]
    b   <- dat[[paste0("beta.", role)]]
    eaf <- dat[[paste0("eaf.", role)]]
    if (is.null(nc) || is.null(nt) || is.null(b) || is.null(eaf) ||
        any(is.na(nc)) || any(is.na(nt))) return(NULL)
    tryCatch(get_r_from_lor(beta = b, eaf = eaf, ncase = nc, ncontrol = nt),
             error = function(e) NULL)
  }
  r_exp <- comp_r("exposure")
  r_out <- comp_r("outcome")
  if (is.null(r_exp) || is.null(r_out)) {
    message("[", label, "] Steiger :  ncase/ncontrol(get_r_from_lor ) -> ; ",
            " MR / coloc . ")
    return(NULL)
  }
  tryCatch(directionality_test(dat, r.exposure = r_exp, r.outcome = r_out),
           error = function(e) { message("[", label, "] Steiger : ", conditionMessage(e)); NULL })
}
steiger_fwd <- run_steiger(dat_fwd, "->AD")
steiger_rev <- run_steiger(dat_rev, "AD->")

# harmonise MR SNP coloc.abf: SNP
# beta.exposure/outcome, se, pos, samplesize, , PP.H4.
# ieugwasr , -> SNP ->PP.H4 NA, .
COLOC_WINDOW_KB <- 500   # (±500kb);  LD 
COLOC_P1 <- 1e-4         # :  SNP 
COLOC_P2 <- 1e-4

# /: coloc MAF+N sdY, N+s.
# harmonise samplesize ; fallback 00b .
# : Bellenguezebi-a-GCST90027158 N/ 00b , fallback samplesize .
GWAS_N <- list("ukb-b-3957" = 462341, "ieu-b-2" = 63860)   #  n; AD(Kunkle) 21982 cases+41938 ctrl
GWAS_S <- list("ieu-b-2" = 0.344, "ukb-b-3957" = 0.30)    # AD  21982/63860;

# trait GWAS sdY: sdY^2 ≈ medianvarbeta * N * 2*maf*1-maf
# coloc estimatesdy ; s check_dataset , maf+N .
est_sdy_quant <- function(varbeta, maf, N) {
  v <- as.numeric(varbeta) * as.numeric(N) * 2 * as.numeric(maf) * (1 - as.numeric(maf))
  v <- v[is.finite(v) & v > 0]
  if (length(v) == 0) return(NA_real_)
  sqrt(median(v))
}

# coloc ****: lead SNP, ±window_kb SNP
# coloc.abf. SNP " PP.H4"; coloc
# : GWAS pos ieugwasr allow_range_query, .
# data.framelabel / lead_snp / chr / pos / n_snps / PP.H0..H4.

# icase/icontrol GWAS_S scc coloc
coloc_s_from_gwas <- function(g, id = NULL) {
  if (!is.null(g$icase) && !is.null(g$icontrol)) {
    ic <- as.numeric(g$icase); nc <- as.numeric(g$icontrol)
    v <- ic / (ic + nc); v <- v[is.finite(v) & v > 0 & v < 1]
    if (length(v)) return(mean(v))
  }
  if (!is.null(id) && id %in% names(GWAS_S)) return(GWAS_S[[id]])
  NA_real_
}

# harmonised dat lead SNP clump
extract_lead_from_harmonized <- function(dat) {
  dat <- as.data.frame(dat)
  snp <- as.character(dat$SNP)
  pos <- if (!is.null(dat$pos.exposure)) dat$pos.exposure
         else if (!is.null(dat$pos)) dat$pos else NA
  chr <- if (!is.null(dat$chr.exposure)) dat$chr.exposure
         else if (!is.null(dat$chr)) dat$chr else NA
  pos <- as.integer(pos); chr <- as.integer(chr)
  keep <- !is.na(snp) & !is.na(pos) & !is.na(chr)
  data.frame(snp = snp[keep], chr = chr[keep], pos = pos[keep],
             stringsAsFactors = FALSE)
}

# / GWAS snp / chr / pos / beta / se / N / icase / icontrol
norm_coloc_window <- function(df) {
  df <- as.data.frame(df); nm <- names(df)
  snp <- if ("rsid"%in%nm) df$rsid else if ("SNP"%in%nm) df$SNP else df$snp
  a1  <- if ("a1"%in%nm) df$a1 else if ("A1"%in%nm) df$A1 else if ("ea"%in%nm) df$ea
         else if ("effect_allele"%in%nm) df$effect_allele else NULL
  a2  <- if ("a0"%in%nm) df$a0 else if ("A2"%in%nm) df$A2 else if ("oa"%in%nm) df$oa
         else if ("other_allele"%in%nm) df$other_allele else NULL
  beta<- if ("beta"%in%nm) df$beta else df$beta.out
  se  <- if ("se"%in%nm) df$se else df$se.out
  NN  <- if ("n"%in%nm) df$n else if ("N"%in%nm) df$N else NA
  chr <- if ("chr"%in%nm) df$chr else if ("chromosome"%in%nm) df$chromosome else NA
  pos <- if ("pos"%in%nm) df$pos else if ("position"%in%nm) df$position else NA
  ic  <- if ("icase"%in%nm) df$icase else NA
  ict <- if ("icontrol"%in%nm) df$icontrol else NA
  data.frame(snp = as.character(snp), chr = as.integer(chr), pos = as.integer(pos),
             beta = as.numeric(beta), se = as.numeric(se), N = as.numeric(NN),
             icase = as.numeric(ic), icontrol = as.numeric(ict),
             stringsAsFactors = FALSE)
}

fetch_coloc_window_api <- function(id, chr, start, end, label = "coloc") {
  if (!requireNamespace("ieugwasr", quietly = TRUE)) return(NULL)
  variants <- paste0(chr, ":", start, "-", end)
  d <- tryCatch(ieugwasr::associations(variants = variants, id = id),
                error = function(e) { message("[", label, "]  ", id, " (",
                                              variants, ") : ", conditionMessage(e)); NULL })
  if (is.null(d) || nrow(d) == 0) return(NULL)
  norm_coloc_window(d)
}

run_coloc_regional <- function(exp_id, out_id, label,
                               exp_gwas = NULL, out_gwas = NULL,
                               lead_snps = NULL, lead_dat = NULL,
                               window_kb = COLOC_WINDOW_KB,
                               p1 = COLOC_P1, p2 = COLOC_P2,
                               min_snps = 3,
                               clump_r2 = THRESH$clump_r2,
                               clump_kb = THRESH$clump_kb,
                               allow_range_query = TRUE) {
  lbl <- function(...) paste0("[coloc-reg ", label, "] ", paste0(...))
  if (is.null(exp_gwas)) exp_gwas <- fetch_full_gwas(exp_id, paste0(label, "-exp"))
  if (is.null(out_gwas)) out_gwas <- fetch_full_gwas(out_id, paste0(label, "-out"))
  have_exp <- !is.null(exp_gwas) && nrow(exp_gwas) > 0
  have_out <- !is.null(out_gwas) && nrow(out_gwas) > 0
  if (!have_exp && !have_out && !allow_range_query) {
    message(lbl(". GWAS  -> (). "))
    return(NULL)
  }
  # 2. lead SNPs: / harmonized / clump / SNP
  if (is.null(lead_snps) && !is.null(lead_dat)) lead_snps <- extract_lead_from_harmonized(lead_dat)
  if (is.null(lead_snps)) {
    message(lbl(",  GWAS clump  lead SNP..."))
    if (have_exp) {
      cl_in <- exp_gwas
      if (!"SNP" %in% names(cl_in)) cl_in$SNP <- as.character(cl_in$snp)
      cl <- tryCatch(clump_data(cl_in, clump_r2 = clump_r2, clump_kb = clump_kb),
                     error = function(e) { message(lbl("clump : "), conditionMessage(e)); NULL })
      if (!is.null(cl) && nrow(cl) > 0)
        lead_snps <- data.frame(snp = as.character(cl$SNP),
                                chr = as.integer(cl$chr), pos = as.integer(cl$pos),
                                stringsAsFactors = FALSE)
    }
    if (is.null(lead_snps) && have_exp && !is.null(exp_gwas$pval)) {
      message(lbl("clump ,  pval  SNP  lead. "))
      g <- exp_gwas; g$pval <- as.numeric(g$pval)
      g <- g[!is.na(g$pval) & !is.na(g$chr) & !is.na(g$pos), ]
      if (nrow(g) > 0) {
        g <- g[order(g$pval), ]
        keep <- !duplicated(g$chr)
        lead_snps <- data.frame(snp = as.character(g$snp[keep]),
                                chr = as.integer(g$chr[keep]),
                                pos = as.integer(g$pos[keep]),
                                stringsAsFactors = FALSE)
      }
    }
  }
  # * loci: lead SNP LD clumpr2=0.01, kb=500, coloc
  # 2462 SNP coloc; clump 1 SNP.
  if (!is.null(lead_snps) && nrow(lead_snps) > 50L) {
    pv <- if (!is.null(lead_dat) && "pval.exposure" %in% names(as.data.frame(lead_dat)))
            lead_dat$pval.exposure[match(lead_snps$snp, lead_dat$SNP)] else rep(1, nrow(lead_snps))
    clumped <- tryCatch({
      ieugwasr::ld_clump(dat = data.frame(rsid = lead_snps$snp, pval = pv),
                         clump_r2 = 0.01, clump_p = 1e-3, clump_kb = 500, pop = "EUR")
    }, error = function(e) { message(lbl("LD clump : "), conditionMessage(e)); NULL })
    if (!is.null(clumped) && nrow(clumped) > 0) {
      keep_rs <- as.character(clumped$rsid)
      lead_snps <- lead_snps[lead_snps$snp %in% keep_rs, , drop = FALSE]
      message(lbl("LD clump :  ", nrow(lead_snps), "  loci( ",
                  length(keep_rs), "  SNP). "))
    } else {
      ord <- order(pv)
      lead_snps <- lead_snps[ord, ]
      lead_snps <- lead_snps[!duplicated(lead_snps$chr), ]
      message(lbl(" SNP: ", nrow(lead_snps), "  loci(). "))
    }
  }
  if (is.null(lead_snps) || nrow(lead_snps) == 0) {
    message(lbl(" lead SNP(clump . pval/ harmonized) -> . "))
    return(NULL)
  }
  message(lbl(" ", nrow(lead_snps), "  lead SNP,  coloc.abf. "))
  out_rows <- list()
  for (i in seq_len(nrow(lead_snps))) {
    ld <- lead_snps[i, ]; chr <- ld$chr; pos <- ld$pos; lsn <- as.character(ld$snp)
    lo <- pos - window_kb * 1000L; hi <- pos + window_kb * 1000L
    sub_e <- if (have_exp) norm_coloc_window(exp_gwas[exp_gwas$chr == chr &
                       exp_gwas$pos >= lo & exp_gwas$pos <= hi, , drop = FALSE])
             else if (allow_range_query) fetch_coloc_window_api(exp_id, chr, lo, hi, lbl)
             else NULL
    sub_o <- if (have_out) norm_coloc_window(out_gwas[out_gwas$chr == chr &
                       out_gwas$pos >= lo & out_gwas$pos <= hi, , drop = FALSE])
             else if (allow_range_query) fetch_coloc_window_api(out_id, chr, lo, hi, lbl)
             else NULL
    if (is.null(sub_e) || is.null(sub_o) || nrow(sub_e) == 0 || nrow(sub_o) == 0) {
      message(lbl(" ", lsn, " (chr", chr, ":", pos, ") ., . "))
      next
    }
    snps <- intersect(as.character(sub_e$snp), as.character(sub_o$snp))
    sub_e <- sub_e[as.character(sub_e$snp) %in% snps, , drop = FALSE]
    sub_o <- sub_o[as.character(sub_o$snp) %in% snps, , drop = FALSE]
    if (nrow(sub_e) < min_snps || nrow(sub_o) < min_snps) {
      message(lbl(" ", lsn, "  SNP (", nrow(sub_e), "/", nrow(sub_o),
                  "), . "))
      next
    }
    N1 <- if (!is.null(sub_e$N) && !all(is.na(sub_e$N))) sub_e$N[1] else NA
    N2 <- if (!is.null(sub_o$N) && !all(is.na(sub_o$N))) sub_o$N[1] else NA
    if (is.na(N1) && !is.null(exp_id) && exp_id %in% names(GWAS_N)) N1 <- GWAS_N[[exp_id]]
    if (is.na(N2) && !is.null(out_id) && out_id %in% names(GWAS_N)) N2 <- GWAS_N[[out_id]]
    s1 <- coloc_s_from_gwas(sub_e, exp_id); s2 <- coloc_s_from_gwas(sub_o, out_id)
    d1 <- list(beta = sub_e$beta, varbeta = sub_e$se^2, snp = as.character(sub_e$snp),
               position = as.integer(sub_e$pos), type = "cc")
    d2 <- list(beta = sub_o$beta, varbeta = sub_o$se^2, snp = as.character(sub_o$snp),
               position = as.integer(sub_o$pos), type = "cc")
    if (!is.na(N1)) d1$N <- N1
    if (!is.na(N2)) d2$N <- N2
    if (!is.na(s1)) d1$s <- s1 else { message(lbl(" ", lsn, "  s , . ")); next }
    if (!is.na(s2)) d2$s <- s2 else { message(lbl(" ", lsn, "  s , . ")); next }
    cl <- tryCatch(coloc::coloc.abf(dataset1 = d1, dataset2 = d2, p1 = p1, p2 = p2),
                   error = function(e) { message(lbl(" ", lsn, " abf : "), conditionMessage(e)); NULL })
    if (is.null(cl)) next
    s <- cl$summary
    out_rows[[length(out_rows) + 1]] <- data.frame(
      label = label, lead_snp = lsn, chr = chr, pos = pos, n_snps = nrow(sub_e),
      PP.H0 = s["PP.H0.abf"], PP.H1 = s["PP.H1.abf"], PP.H2 = s["PP.H2.abf"],
      PP.H3 = s["PP.H3.abf"], PP.H4 = s["PP.H4.abf"], stringsAsFactors = FALSE)
  }
  if (length(out_rows) == 0) { message(lbl(" PP.H4,  NULL. ")); return(NULL) }
  do.call(rbind, out_rows)
}

# : cc lead ↔ ADcc ; coloc.abf
coloc_fwd     <- run_coloc_regional(exp_id = GWAS_ID$insomnia, out_id = GWAS_ID$ad,
                                    label = "~AD", lead_dat = dat_fwd,
                                    window_kb = COLOC_WINDOW_KB)
# : ADcc lead ↔ cc
coloc_rev     <- run_coloc_regional(exp_id = GWAS_ID$ad, out_id = GWAS_ID$insomnia,
                                    label = "AD~", lead_dat = dat_rev,
                                    window_kb = COLOC_WINDOW_KB)
if (!is.null(coloc_fwd)) {
  message("[coloc]  PP.H4>0.80 : ",
          sum(coloc_fwd$PP.H4 > THRESH$coloc_pph4, na.rm = TRUE),
          " / ", nrow(coloc_fwd))
  print(coloc_fwd[order(-coloc_fwd$PP.H4), c("label", "PP.H4", "n_snps")])
}
if (!is.null(coloc_rev)) {
  message("[coloc]  PP.H4>0.80 : ",
          sum(coloc_rev$PP.H4 > THRESH$coloc_pph4, na.rm = TRUE),
          " / ", nrow(coloc_rev))
  print(coloc_rev[order(-coloc_rev$PP.H4), c("label", "PP.H4", "n_snps")])
}

# ieu-b-2 UKB -> MRlap/cause
# §4c ukb-b-3957 × Bellenguez, UKB .
mrlap_fwd <- tryCatch(run_mrlap(dat_fwd, label = "->AD"), error = function(e) NULL)
mrlap_rev <- tryCatch(run_mrlap(dat_rev, label = "AD->"), error = function(e) NULL)
cause_fwd <- tryCatch(run_cause(GWAS_ID$insomnia, GWAS_ID$ad), error = function(e) NULL)
cause_rev <- tryCatch(run_cause(GWAS_ID$ad, GWAS_ID$insomnia), error = function(e) NULL)

# ---- 4c. : ukb-b-3957 × Bellenguez UKB
if (RUN_REPLICATION) {
  dat_fwd_rep <- get_harmonized(GWAS_ID$insomnia, GWAS_ID$ad_alt)   #  -> Bellenguez AD
  dat_rev_rep <- get_harmonized(GWAS_ID$ad_alt, GWAS_ID$insomnia)   # Bellenguez AD -> 
  fwd_rep <- run_mr(dat_fwd_rep, "->AD(repl Bellenguez)")
  rev_rep <- run_mr(dat_rev_rep, "AD->(repl Bellenguez)")
  # : lead ↔ Bellenguez ; AD lead ↔ -- cc
  # N / s GWAS n / icase / icontrol GWAS_N / GWAS_S
  coloc_fwd_rep <- run_coloc_regional(exp_id = GWAS_ID$insomnia, out_id = GWAS_ID$ad_alt,
                                      label = "~AD(repl)", lead_dat = dat_fwd_rep,
                                      window_kb = COLOC_WINDOW_KB)
  coloc_rev_rep <- run_coloc_regional(exp_id = GWAS_ID$ad_alt, out_id = GWAS_ID$insomnia,
                                      label = "AD~(repl)", lead_dat = dat_rev_rep,
                                      window_kb = COLOC_WINDOW_KB)
  # * : MRlap/cause Bellenguez UKB
  mrlap_rep_fwd <- tryCatch(run_mrlap(dat_fwd_rep, label = "->AD(repl,)"), error = function(e) NULL)
  mrlap_rep_rev <- tryCatch(run_mrlap(dat_rev_rep, label = "AD->(repl,)"), error = function(e) NULL)
  cause_rep_fwd <- tryCatch(run_cause(GWAS_ID$insomnia, GWAS_ID$ad_alt), error = function(e) NULL)
  cause_rep_rev <- tryCatch(run_cause(GWAS_ID$ad_alt, GWAS_ID$insomnia), error = function(e) NULL)
  message("[G1]  Bellenguez  MR + coloc + MRlap/cause . ")
} else {
  fwd_rep <- rev_rep <- coloc_fwd_rep <- coloc_rev_rep <-
    mrlap_rep_fwd <- mrlap_rep_rev <- cause_rep_fwd <- cause_rep_rev <- NULL
  message("[G1] (ad_alt ). ")
}

saveRDS(list(fwd = fwd, rev = rev,
             steiger_fwd = steiger_fwd, steiger_rev = steiger_rev,
             coloc_fwd = coloc_fwd, coloc_rev = coloc_rev,
             mrlap_fwd = mrlap_fwd, mrlap_rev = mrlap_rev,
             cause_fwd = cause_fwd, cause_rev = cause_rev,
             fwd_rep = if (exists("fwd_rep")) fwd_rep else NULL,
             rev_rep = if (exists("rev_rep")) rev_rep else NULL,
             coloc_fwd_rep = if (exists("coloc_fwd_rep")) coloc_fwd_rep else NULL,
             coloc_rev_rep = if (exists("coloc_rev_rep")) coloc_rev_rep else NULL,
             mrlap_rep_fwd = if (exists("mrlap_rep_fwd")) mrlap_rep_fwd else NULL,
             mrlap_rep_rev = if (exists("mrlap_rep_rev")) mrlap_rep_rev else NULL,
             cause_rep_fwd = if (exists("cause_rep_fwd")) cause_rep_fwd else NULL,
             cause_rep_rev = if (exists("cause_rep_rev")) cause_rep_rev else NULL,
             overlap_correction_run = overlap_correction_run),
        file.path(DIR_OUT, "G1_bidirectional.rds"))
if (!is.null(coloc_fwd)) write.csv(coloc_fwd, file.path(DIR_OUT, "G1_coloc_forward.csv"), row.names = FALSE)
if (!is.null(coloc_rev)) write.csv(coloc_rev, file.path(DIR_OUT, "G1_coloc_reverse.csv"), row.names = FALSE)
if (!is.null(coloc_fwd_rep)) write.csv(coloc_fwd_rep, file.path(DIR_OUT, "G1_coloc_forward_repl.csv"), row.names = FALSE)
if (!is.null(coloc_rev_rep)) write.csv(coloc_rev_rep, file.path(DIR_OUT, "G1_coloc_reverse_repl.csv"), row.names = FALSE)
message("[G1]  MR + .  results/G1_bidirectional.rds")

if (exists("DIR_OUT") && is.character(DIR_OUT) && nzchar(DIR_OUT)) {
  sinfo_path <- file.path(DIR_OUT, "G1_sessionInfo.txt")
  tryCatch({
    sink(sinfo_path); print(sessionInfo()); sink()
    message("[G1]  sessionInfo: ", sinfo_path)
  }, error = function(e) message("[G1] sessionInfo : ", conditionMessage(e)))
}