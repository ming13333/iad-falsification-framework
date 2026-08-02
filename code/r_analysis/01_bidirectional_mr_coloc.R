# =====================================================================
# 01_bidirectional_mr_coloc.R  —  G1: 双向 MR + 共定位（定性方向）
# ---------------------------------------------------------------------
# 正向: 失眠 → AD      反向: AD → 失眠
# 主: IVW | 敏感: MR-Egger / 加权中位数 / 加权众数 / MR-PRESSO / 留一法
# 共定位: coloc (PP.H4 > 0.80)
# 依赖: 00_config.R
# =====================================================================
source("00_config.R")
library(TwoSampleMR); library(ieugwasr); library(coloc)
options(encoding = "UTF-8")   # 中文进度信息在部分控制台不乱码(不改科学内容)
set.seed(20240721)   # 可复现性: 固定随机种子(cause MCMC / MR-PRESSO 置换等随机步骤)

## ---- 0. 运行前守卫: AD ID 必须已核验 ----
# 主源 GWAS_ID$ad = ieu-b-2 (Kunkle/IGAP, 无 UKB 重叠) → 因果估计最干净;
# 复制源 GWAS_ID$ad_alt = Bellenguez 2022 (ebi-a-GCST90027158, 含 UKB 重叠) → 已接入,
#   须做 MRlap/cause 重叠校正(见 §4c)。
if (is.null(GWAS_ID$ad) || identical(GWAS_ID$ad, "PENDING_VERIFY") ||
    (is.character(GWAS_ID$ad) && GWAS_ID$ad == "PENDING_VERIFY")) {
  stop("[G1] GWAS_ID$ad 仍为 PENDING_VERIFY 或缺失。",
       "请先在联网 R 环境运行 00b_verify_gwas.R 核验并指派主源 AD ID ",
       "(写出 gwas_ids_resolved.json) 后再运行本脚本。")
}
# ad_alt(Bellenguez)复制对: 若未指派则跳过复制段(主分析照常跑)。
RUN_REPLICATION <- FALSE
if (is.null(GWAS_ID$ad_alt) || is.na(GWAS_ID$ad_alt) ||
    identical(GWAS_ID$ad_alt, "PENDING_VERIFY")) {
  message("[G1] 提示: ad_alt(Bellenguez)未指派, 跳过复制段(仅跑主对 ieu-b-2)。")
} else {
  RUN_REPLICATION <- TRUE
  message("[G1] 复制对已接入: ad_alt = ", GWAS_ID$ad_alt,
          " (Bellenguez 2022, 含 UKB 重叠, 将做 MRlap/cause 校正)")
}
# 重叠校正运行标志: 仅当 MRlap/cause 实际吃到全 GWAS 并跑成功才置 TRUE;
# 跳过/不可用 → FALSE, 供 saveRDS 写入, 强制 Limitations 披露重叠校正未运行。
overlap_correction_run <- FALSE

## ---- 0b0. 本地 clean GWAS 文件映射(零联网来源; 由 data/raw 预处理产出) ----
# 路径指向顶层 data/raw(与 课题设计阶段/data 为不同目录), 本机绝对路径固定。
# 这些文件已由「数据预处理」步骤产出(去重 + 坐标对齐 + 样本量注入), 见数据预处理报告.md。
DIR_RAW_LOCAL <- "C:/Temp/iad_g1/data/raw"
LOCAL_CLEAN <- list(
  "ukb-b-3957"          = file.path(DIR_RAW_LOCAL, "ukb-b-3957", "ukb-b-3957.clean.tsv.gz"),
  "ieu-b-2"             = file.path(DIR_RAW_LOCAL, "ieu-b-2", "ieu-b-2.clean.tsv.gz"),
  "ebi-a-GCST90027158"  = file.path(DIR_RAW_LOCAL, "ebi-a-GCST90027158", "GCST90027158_buildGRCh38.dedup.tsv.gz")
)
USE_LOCAL_GWAS <- TRUE   # TRUE=优先用本地 clean 文件(零联网); FALSE=回退 OpenGWAS API

## ---- 0b0a. 读本地 clean 文件并规整为通用列(beta/se/snp/A1/A2/N/chr/pos/icase/icontrol) ----
# 列名兼容: clean 文件统一为 SNP CHR BP A1 A2 beta se p n [ncase ncontrol | n_cases n_controls]
.LocalCleanCache <- if (exists(".LocalCleanCache", envir = globalenv()))
  get(".LocalCleanCache", envir = globalenv()) else new.env(hash = TRUE, parent = emptyenv())
read_local_clean <- function(id, label = "local") {
  # ★ 全局缓存: 同一 GWAS 只 fread 一次, 避免多次调用/双向+coloc 累积 OOM
  if (exists(id, envir = .LocalCleanCache)) return(get(id, envir = .LocalCleanCache))
  lf <- if (id %in% names(LOCAL_CLEAN)) LOCAL_CLEAN[[id]] else NULL
  if (is.null(lf) || !file.exists(lf)) {
    message("[", label, "] 无本地 clean 文件(", id, "): ",
            ifelse(is.null(lf), "<未映射>", lf))
    return(NULL)
  }
  if (!requireNamespace("data.table", quietly = TRUE)) {
    message("[", label, "] data.table 未安装, 无法读本地 clean 文件。")
    return(NULL)
  }
  dt <- tryCatch(data.table::fread(lf, sep = "\t", header = TRUE, showProgress = FALSE,
                                   data.table = FALSE),
                 error = function(e) { message("[", label, "] 读 ", lf, " 失败: ",
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

## ---- 0b0b. 本地 harmonize(零联网): 从 clean 文件构造双向 MR 的 dat ----
# 暴露取 p<pval 的 SNP 作工具; 结局按 SNP 匹配; 直接等位基因对齐(丢弃 ambiguous,
# 行为等同 harmonise_data action="none")。完全本地, 无需 IEU/LD 面板。
build_harmonized_local <- function(exp_id, out_id, pval = 5e-8, label = "harmonize-local") {
  exp <- read_local_clean(exp_id, label)
  out <- read_local_clean(out_id, label)
  if (is.null(exp) || is.null(out)) {
    message("[", label, "] 本地暴露或结局缺失, 跳过(", exp_id, "→", out_id, ")")
    return(NULL)
  }
  exp_iv <- exp[!is.na(exp$p) & exp$p < pval & exp$p > 0, ]
  message("[", label, "] ", exp_id, " 显著 SNP(p<", format(pval, digits = 2), ")=",
          nrow(exp_iv), "; 全量=", nrow(exp))
  if (nrow(exp_iv) == 0) {
    message("[", label, "] 暴露无显著 SNP, 跳过。")
    return(NULL)
  }
  m <- merge(exp_iv, out, by = "snp", suffixes = c(".exposure", ".outcome"), all.x = TRUE)
  m <- m[!is.na(m$beta.outcome) & !is.na(m$se.outcome), ]
  if (nrow(m) == 0) {
    message("[", label, "] 暴露工具 SNP 在结局中无匹配, 跳过。")
    return(NULL)
  }
  # ★ 向量化等位基因对齐(替代逐行 for 循环, 大数据集不再慢/崩)
  ea_e <- m$A1.exposure; oa_e <- m$A2.exposure
  ea_o <- m$A1.outcome;  oa_o <- m$A2.outcome
  same <- (ea_e == ea_o) & (oa_e == oa_o)
  flip <- (ea_e == oa_o) & (oa_e == ea_o)
  ambiguous <- !(same | flip)
  ambiguous[is.na(ambiguous)] <- TRUE   # 任一等位基因为 NA → 视为 ambiguous 丢弃
  m$beta.outcome[flip] <- -m$beta.outcome[flip]
  m <- m[!ambiguous, ]
  if (nrow(m) == 0) {
    message("[", label, "] 等位基因对齐后无可用 SNP, 跳过。")
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
  message("[", label, "] 本地 harmonize 完成: ", exp_id, "→", out_id,
          " (", nrow(dat), " 工具 SNP, ", sum(ambiguous), " ambiguous 已丢弃)")
  dat
}

## ---- 0b. 全 GWAS 汇总统计读取 helper (MRlap/cause 重叠校正必须, 非仅 clumped IV) ----
# 优先读用户本地文件(环境变量 <PREFIX>_LOC), 否则从 IEU 拉全基因组 SNP 关联。
# 规整为通用列: beta/se/snp/A1/A2。取不到 → 返回 NULL(上层据此跳过, 绝不输出假数)。
load_full_gwas <- function(id, loc_env, label = "fullgwas") {
  loc <- Sys.getenv(loc_env)
  d <- if (nzchar(loc) && file.exists(loc)) {
    tryCatch(read.table(loc, header = TRUE, stringsAsFactors = FALSE),
             error = function(e) { message("[", label, "] 读本地 GWAS 失败(",
                                           loc, "): ", conditionMessage(e)); NULL })
    } else {
    # 不联网下载全染色体（variants_chrpos(chr=1:22, from=1, to=250e6) 极易超时/限流）。
    # 重叠校正(MRlap/cause)必须有本地全 GWAS 文件；缺失则优雅跳过，绝不在线拉整条染色体。
    message("[", label, "] 未设置/未找到本地 GWAS 文件(", loc_env,
            ")，跳过在线下载；重叠校正需本地文件。")
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
    message("[", label, "] 全 GWAS 列名无法识别(", id, "), 跳过重叠校正。")
    return(NULL)
  }
  # MRlap 还需 N/chr/pos(若本地文件提供则带上, 否则 NA → MRlap 守卫会要求)
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

## ---- 0b2. 冻结 GWAS 到本地(可复现性: 避免 OpenGWAS 实时拉取导致版本漂移) ----
# 首次: ieugwasr::associations(id) 拉全量 → 存 data/gwas/<id>.rds (+ 侧车 <id>.meta.rds 记录下载日期/ID)
# 后续: 直接读本地, 不再联网。取数/读盘失败 → 返回 NULL(上层回退在线/跳过, 绝不编造)。
DIR_DATA <- if (exists("DIR_DATA") && is.character(DIR_DATA) && nzchar(DIR_DATA)) {
  DIR_DATA
} else {
  file.path(dirname(DIR_OUT), "data")
}
# OpenGWAS API 逐染色体范围查询拉取全 GWAS(需 OPENGWAS_JWT; 2024-05 起 API 多数端点需鉴权)
# 仅作 freeze_gwas 的二级回退: 静态 CDN 不可达时, 用 ieugwasr::associations 按 chr:pos 范围分块拉全量。
# 命名传参(variants=, id=)——区别于旧代码的错位传参 bug; 返回列即 OpenGWAS 标准格式(rsid/a1/a0/beta/se/...)。
download_full_gwas_api <- function(id, label = "freeze-api") {
  if (!requireNamespace("ieugwasr", quietly = TRUE)) {
    message("[", label, "] ieugwasr 未安装, 无法经 API 拉全 GWAS。")
    return(NULL)
  }
  jwt <- tryCatch(ieugwasr::get_opengwas_jwt(), error = function(e) "")
  if (!nzchar(jwt)) {
    message("[", label, "] 未设置 OPENGWAS_JWT(环境变量), 跳过 API 全 GWAS 拉取。")
    return(NULL)
  }
  # 单窗口超时防护: 避免个别高密度窗口挂起卡死整条管线(60s 超时后 tryCatch 跳过该块)
  if (requireNamespace("httr", quietly = TRUE)) httr::set_config(httr::timeout(60))
  message("[", label, "] 静态 CDN 不可用, 改用 OpenGWAS API 逐染色体(1Mb 分块)拉全 GWAS: ", id, " ...")
  # 染色体长度表: 按 GWAS 实际坐标体系选择。OpenGWAS 各 GWAS build 不一
  # (gwasinfo(id)$build 已确认 ieu-b-2 = HG19/GRCh37; ukb-b-3957 等可能为 GRCh38)。
  # 用错坐标体系会导致 associations 按范围查询返回空(已踩坑),故动态检测。
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
    chr_len <- chr_len_hg19; btxt <- "GRCh37/其他(默认GRCh37)"
  }
  names(chr_len) <- 1:22
  message("[", label, "] ", id, " 坐标体系: ", btxt, " (build=", build, ")")
  chunk_bp <- 1e6   # 1Mb 窗口
  pieces <- list(); pulled_rows <- 0L
  for (chr in 1:22) {
    L <- chr_len[as.character(chr)]; start <- 1L
    while (start <= L) {
      e <- min(start + chunk_bp - 1L, L)
      variants <- paste0(chr, ":", start, "-", e)
      p <- tryCatch(ieugwasr::associations(variants = variants, id = id),
                    error = function(e2) { message("[", label, "] chr", chr, ":",
                      start, "-", e, " 查询失败: ", conditionMessage(e2)); NULL })
      if (!is.null(p) && nrow(p) > 0) {
        pieces[[length(pieces) + 1]] <- as.data.frame(p)
        pulled_rows <- pulled_rows + nrow(p)
      }
      start <- e + 1L
      Sys.sleep(0.3)   # 轻频限, 避免触发 OpenGWAS rate limit
    }
    message("[", label, "] chr", chr, " 完成, 累计 ", length(pieces),
            " 块 / ", pulled_rows, " 行")
  }
  if (length(pieces) == 0) { message("[", label, "] API 各染色体查询均无返回, 拉取失败。"); return(NULL) }
  out <- tryCatch(do.call(rbind, pieces), error = function(e) NULL)
  if (is.null(out) || nrow(out) == 0) return(NULL)
  if ("rsid" %in% names(out)) out <- out[!duplicated(out$rsid), ]
  out
}

freeze_gwas <- function(id, label = "freeze") {
  if (is.null(id) || !is.character(id) || !nzchar(id) || is.na(id)) {
    message("[", label, "] 无效 GWAS ID(=", id, "), 跳过冻结。")
    return(NULL)
  }
  # ★ 本地 clean 文件优先(零联网): 直接读 data/raw 预处理产出, 跳过 CDN/API。
  if (USE_LOCAL_GWAS) {
    loc <- tryCatch(read_local_clean(id, paste0(label, "-local")),
                    error = function(e) NULL)
    if (!is.null(loc) && nrow(loc) > 0) {
      message("[", label, "] 本地 clean 文件载入(GWAS=", id, ", ", nrow(loc),
              " SNPs) → 跳过联网。")
      return(loc)
    }
  }
  base_dir <- file.path(DIR_DATA, "gwas")
  dir.create(base_dir, showWarnings = FALSE, recursive = TRUE)
  rds_path  <- file.path(base_dir, paste0(id, ".rds"))
  meta_path <- file.path(base_dir, paste0(id, ".meta.rds"))
  # 本地已有 → 读盘返回(不联网)
  if (file.exists(rds_path)) {
    d <- tryCatch(readRDS(rds_path),
                  error = function(e) { message("[", label, "] 读冻结 GWAS 失败(",
                                                rds_path, "): ", conditionMessage(e)); NULL })
    if (!is.null(d)) {
      message("[", label, "] 已载入冻结 GWAS: ", id, " (", nrow(d), " SNPs; 路径 ",
              rds_path, ")")
      return(d)
    }
  }
  # 本地缺失 → 从 OpenGWAS 静态 CDN 拉取全量汇总文件(端点通常免 JWT 认证)。
  # 注意: ieugwasr::associations(variants, id, ...) 第一形参为 variants(必填)且只能返回
  #       给定变异列表的关联, 不能返回整条 GWAS; MRlap/cause 必须喂全 GWAS, 故改用静态
  #       全量文件端点 https://gwas.mrcieu.ac.uk/files/<id>/<id>.tab.gz (data.table::fread)。
  if (!requireNamespace("data.table", quietly = TRUE)) {
    message("[", label, "] data.table 未安装, 无法拉取静态 GWAS 文件, 跳过重叠校正。")
    return(NULL)
  }
  url <- paste0("https://gwas.mrcieu.ac.uk/files/", id, "/", id, ".tab.gz")
  message("[", label, "] 在线拉取并冻结 GWAS(全量静态文件): ", id, " ...")
  d <- tryCatch({
    tmp <- tempfile(fileext = ".tab.gz")
    dl <- download.file(url, tmp, mode = "wb", quiet = TRUE)
    if (!file.exists(tmp) || file.info(tmp)$size < 10L) stop("下载文件为空或不存在")
    # 404/网关错误常返回 HTML 错误页而非二进制 → 检测首行是否为 HTML, 避免假数
    first_line <- tryCatch(readLines(tmp, n = 1, warn = FALSE), error = function(e) "")
    if (grepl("^\\s*<", first_line)) stop("返回疑似 HTML 错误页(404/网关), 非 GWAS 数据")
    dt <- data.table::fread(tmp, sep = "\t", header = TRUE,
                            showProgress = FALSE, data.table = FALSE)
    if (is.null(dt) || nrow(dt) == 0) stop("下载数据为空")
    file.remove(tmp)
    as.data.frame(dt)
  }, error = function(e) {
    message("[", label, "] 下载 GWAS 文件失败(", id, "): ", conditionMessage(e))
    NULL
  })
  if (is.null(d) || nrow(d) == 0) {
    # (2) 二级回退: OpenGWAS API 逐染色体范围查询(需 OPENGWAS_JWT; 静态 CDN 不可达时)
    d <- tryCatch(download_full_gwas_api(id, label),
                  error = function(e) { message("[", label, "] API 全 GWAS 拉取失败: ",
                                                conditionMessage(e)); NULL })
  }
  if (is.null(d) || nrow(d) == 0) {
    message("[", label, "] GWAS(", id, ") 无法取得(静态 CDN 与 API 均失败/未鉴权) → 上层跳过(绝不编造)。")
    return(NULL)
  }
  tryCatch({
    saveRDS(d, rds_path)
    saveRDS(list(id = id, source = "OpenGWAS static CDN",
                 url = url, downloaded = as.character(Sys.Date()),
                 n_snp = nrow(d)), meta_path)
    message("[", label, "] 已冻结 GWAS: ", id, " (", nrow(d), " SNPs) → ", rds_path)
  }, error = function(e) {
    message("[", label, "] 写冻结 GWAS 失败(", rds_path, "): ", conditionMessage(e))
  })
  d
}

## ---- 0c. 取全 GWAS helper (MRlap/cause 重叠校正; 经 freeze_gwas: 静态 CDN 优先, 失败回退 API) ----
# 规整为通用列: beta/se/snp/A1/A2(并保留 N/chr/pos/icase/icontrol)。
# 取不到(网络错/ID 错/未鉴权) → 返回 NULL(上层据此跳过重叠校正, 绝不编造)。
# 列名兼容: beta→beta/beta.out/beta.exposure; se→se/se.out/se.exposure;
#           snp→rsid/SNP/name; A1→A1/a1/ea/effect_allele; A2→A2/a0/oa/other_allele。
fetch_full_gwas <- function(id, label = "fullgwas") {
  if (!requireNamespace("ieugwasr", quietly = TRUE)) {
    message("[", label, "] ieugwasr 未安装, 无法在线取全 GWAS, 跳过重叠校正。")
    return(NULL)
  }
  if (is.null(id) || !is.character(id) || !nzchar(id) || is.na(id)) {
    message("[", label, "] 无效 GWAS ID(=", id, "), 跳过在线取数。")
    return(NULL)
  }
  # 优先读本地冻结; 缺失则在线拉取并冻结(见 freeze_gwas)
  d <- freeze_gwas(id, label)
  if (is.null(d) || nrow(d) == 0) {
    message("[", label, "] 冻结 GWAS(", id, ") 失败/为空, 跳过重叠校正(绝不编造)。")
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
    message("[", label, "] 全 GWAS 列名无法识别(", id, "): 现有列=",
            paste(nm, collapse = ","), "; 跳过重叠校正。")
    return(NULL)
  }
  # MRlap 还需 N(样本量)/chr/pos(距离剪枝); ieugwasr::associations 均返回, 取不到则 NA。
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
  # 保留 icase/icontrol: 区域 coloc(type=cc) 用其推病例比例 s(比 GWAS_S 兜底更准)
  if (!is.null(icase))    out$icase <- icase
  if (!is.null(icontrol)) out$icontrol <- icontrol
  out
}

## ---- 0d. 结果 CSV 追加写出(幂等; 结果目录/文件不存在则创建, 绝不因缺文件崩溃) ----
# out_dir 优先用 00_config 的 DIR_OUT, 缺失则退回 "results"; dir.create 确保目录存在。
# 文件不存在 → 写表头; 已存在 → read 后对齐列(rbind, 缺失补 NA)再写, 避免列数/类型不一致崩溃。
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
                             message("[append_csv] rbind 失败(", fname, "): ",
                                     conditionMessage(e), "; 仅写新行。")
                             df
                           })
      write.csv(combined, path, row.names = FALSE)
    }
  }
  message("[append_csv] 已写出: ", path)
  invisible(path)
}

## 失眠特质 SD(定量 trait 的 coloc 先验需要 sdy)。TODO: 待 00b/UK Biobank 字段文档
## 填实精确值; 缺省 NA → d1 不传 sdy, coloc 回退默认先验(精度略降, 非致命)。
INSOMNIA_SDY <- NA_real_

## ---- 1. 提取并 harmonize instruments ----
extract_exp <- function(id, outcome_id, pval = 5e-8) {
  # 暴露工具变量：从暴露 GWAS 取显著 SNP
  exp <- extract_instruments(id, p1 = pval,
                             r2 = THRESH$clump_r2, kb = THRESH$clump_kb)
  # 取结局中的效应（自动 harmonize 链向）
  # 批量提取：避免一次性把全部 clumped IV（如 42 个）塞进单次 API 查询
  out <- extract_outcome_data_batched(snps = exp$SNP, outcomes = outcome_id)
  dat <- harmonise_data(exp, out)
  return(dat)
}

## ---- 1b. 冻结 harmonized 提取结果(可复现: 重跑直接读缓存, 跳过在线 clump/拉取) ----
get_harmonized <- function(exp_id, out_id, pval = 5e-8, label = "harmonize") {
  base_dir <- file.path(DIR_DATA, "extracted")
  dir.create(base_dir, showWarnings = FALSE, recursive = TRUE)
  cache_path <- file.path(base_dir, paste0(exp_id, "__", out_id, ".rds"))
  if (!USE_LOCAL_GWAS && file.exists(cache_path)) {
    dat <- tryCatch(readRDS(cache_path),
                    error = function(e) { message("[", label, "] 读冻结 harmonized 失败(",
                                                  cache_path, "): ", conditionMessage(e)); NULL })
    if (!is.null(dat)) {
      message("[", label, "] 已载入冻结 harmonized: ", exp_id, " → ", out_id,
              " (", nrow(dat), " 工具 SNP)")
      return(dat)
    }
  }
  # ★ 零联网: 优先用本地 clean 文件构造 harmonized dat; 否则回退 API。
  dat <- if (USE_LOCAL_GWAS) {
    build_harmonized_local(exp_id, out_id, pval, label)
  } else {
    extract_exp(exp_id, out_id, pval)
  }
  if (!is.null(dat) && nrow(dat) > 0) {
    tryCatch(saveRDS(dat, cache_path),
             error = function(e) message("[", label, "] 写冻结 harmonized 失败: ",
                                         conditionMessage(e)))
    message("[", label, "] 工具 SNP 数: ", nrow(dat), " (", exp_id, " → ", out_id, ")")
  }
  dat
}

dat_fwd <- get_harmonized(GWAS_ID$insomnia, GWAS_ID$ad)   # 失眠 → AD
dat_rev <- get_harmonized(GWAS_ID$ad, GWAS_ID$insomnia)   # AD   → 失眠

## ---- 2. 双向 MR（多方法）----
# 方法选择符合 2024-2025 两样本 MR 最佳实践：
#   IVW（主） + MR-Egger（水平多效性/截距） + 加权中位数 + 加权众数（稳健） +
#   Steiger（方向） + MR-PRESSO（离群） + 留一法。
# ⚠️ 样本重叠注意：BenElsworth 2018 (ukb-b-3957) 失眠 与 Bellenguez AD 均含 UKB 子集
#   → 仅复制对存在样本重叠; 主对(ieu-b-2, Kunkle/IGAP)无 UKB 重叠, 因果估计最干净。
#   可能放大 I 型错误 / 膨胀 IVW。delta 法与 IVW 方差均假设两样本独立。
# ---- 样本重叠校正(MRlap)+ 多效性区分(cause):G1 必需敏感性(OSF §6/§7)----
# BenElsworth 2018 (ukb-b-3957, 失眠) 与 Bellenguez(AD) 均含 UKB → 若重叠>5% 必须校正(见 §4c),否则审稿人质疑。
# 沙箱无 R/无 LD 面板/无网,以下为健壮骨架(requireNamespace 守卫,未装则跳过不报错)。
run_mrlap <- function(dat, label = "mrlap") {
  if (!requireNamespace("MRlap", quietly = TRUE)) {
    message("[", label, "] MRlap 未安装,跳过(安装: remotes::install_github('n-mounier/MRlap'))")
    return(NULL)
  }
  # 从 harmonized dat 取暴露/结局 ID(列 id.exposure / id.outcome)
  exp_id <- tryCatch(unique(dat$id.exposure)[1], error = function(e) NULL)
  out_id <- tryCatch(unique(dat$id.outcome)[1], error = function(e) NULL)
  if (is.null(exp_id) || is.null(out_id) || !nzchar(exp_id) || !nzchar(out_id)) {
    message("[", label, "] 无法从 dat 取得暴露/结局 ID, MRlap 跳过。")
    return(NULL)
  }
  # ★ 本机验证前不确定 MRlap 是否需本地 LDSC 权重; 先尝试让其自行取 LD(ld_proxies=TRUE)。
  #   若全部候选接口失败, 下方 tryCatch 会优雅跳过(绝不输出假数)。
  # MRlap 需全基因组 SNP 汇总统计(非仅 clumped 工具 SNP) — 在线取(OpenGWAS), 不依赖本地文件。
  exp_sum <- fetch_full_gwas(exp_id, label)
  out_sum <- fetch_full_gwas(out_id, label)
  if (is.null(exp_sum) || is.null(out_sum)) {
    message("[", label, "] 无法取得暴露/结局全 GWAS → MRlap 跳过(绝不输出假数); Limitations 须披露重叠校正未运行。")
    return(NULL)
  }
  # ★ MRlap::MRlap 签名(MRlap 0.0.3.3): exposure, exposure_name, outcome, outcome_name,
  #   ld(文件夹路径, 含 {chr}.l2.ldscore.gz), hm3(SNP 对齐文件路径) — 均为必填。
  #   LD 参考数据: Zenodo 1000G Phase3 EUR LD scores + hm3_no_MHC SNP 列表。
  LD_REF_DIR <- "C:/Temp/iad_g1/ld_ref/LDscore"
  HM3_FILE   <- "C:/Temp/iad_g1/ld_ref/hm3_no_MHC.list.txt"
  if (!file.exists(LD_REF_DIR) || !file.exists(file.path(LD_REF_DIR, "1.l2.ldscore.gz")) ||
      !file.exists(HM3_FILE)) {
    message("[", label, "] LD 参考数据缺失(ld=", LD_REF_DIR, ", hm3=", HM3_FILE, "), MRlap 跳过。")
    return(NULL)
  }
  message("[", label, "] MRlap::MRlap 启动 (ld=", LD_REF_DIR, ", hm3=", HM3_FILE, ")...")
  fit <- tryCatch(
    MRlap::MRlap(exposure = exp_sum, exposure_name = as.character(exp_id),
                 outcome  = out_sum, outcome_name  = as.character(out_id),
                 ld  = LD_REF_DIR, hm3 = HM3_FILE),
    error = function(e) { message("[", label, "] MRlap::MRlap 失败: ", conditionMessage(e)); NULL })
  if (is.null(fit)) {
    message("[", label, "] MRlap 调用失败, 跳过(绝不输出假数)。")
    return(NULL)
  }
  # ---- 提取重叠校正后估计量(fit$MRcorrection 标量字段) ----
  mc <- tryCatch(fit$MRcorrection, error = function(e) NULL)
  if (is.null(mc)) {
    message("[", label, "] MRlap 返回结构异常(缺 $MRcorrection), 跳过。")
    return(NULL)
  }
  b_corr  <- as.numeric(mc$corrected_effect)[1]
  se_corr <- as.numeric(mc$corrected_effect_se)[1]
  p_corr  <- as.numeric(mc$corrected_effect_p)[1]
  b_obs   <- as.numeric(mc$observed_effect)[1]
  se_obs  <- as.numeric(mc$observed_effect_se)[1]
  p_obs   <- as.numeric(mc$observed_effect_p)[1]
  p_diff  <- as.numeric(mc$p_difference)[1]   # 校正 vs 未校正 是否显著不同(重叠偏倚检验)
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
  message("[", label, "] MRlap 完成. corrected_beta=",
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
  # 守卫: 包缺失则优雅跳过, 绝不停流水线(OSF §6/§7 必需 P0 敏感性)
  if (!requireNamespace("cause", quietly = TRUE)) {
    message("[", label, "] cause 未安装,跳过(安装: install.packages('cause', repos='https://mrcieu.r-universe.dev') 或 remotes::install_github('jean997/cause@v1.2.0'))")
    return(NULL)
  }
  if (is.null(exp_id) || is.null(out_id) || !nzchar(exp_id) || !nzchar(out_id)) {
    message("[", label, "] 无效 GWAS ID(exp=", exp_id, ", out=", out_id, "), cause 跳过。")
    return(NULL)
  }
  # 重叠校正必须用全 GWAS(非仅 clumped 工具 SNP) — 在线取(OpenGWAS), 不依赖本地文件。
  e <- fetch_full_gwas(exp_id, "cause-exp")
  o <- fetch_full_gwas(out_id, "cause-out")
  if (is.null(e) || is.null(o)) {
    message("[", label, "] 无法取得暴露/结局全 GWAS → cause 跳过(绝不输出假数); Limitations 须披露重叠校正未运行。")
    return(NULL)
  }
  # 规整为 cause::gwas_merge 默认列(snp/beta_hat/se/A1/A2)
  e <- data.frame(snp = e$snp, beta_hat = e$beta, se = e$se, A1 = e$A1, A2 = e$A2,
                  stringsAsFactors = FALSE)
  o <- data.frame(snp = o$snp, beta_hat = o$beta, se = o$se, A1 = o$A1, A2 = o$A2,
                  stringsAsFactors = FALSE)
  # ---- 1) gwas_merge: 对齐等位基因, 构建 cause_data ----
  #   现代 cause v1.2.0+ 中 gwas_merge 不消费 LD 面板; LD 由下游 ld_prune 使用(见步骤3)。
  X <- tryCatch(
    cause::gwas_merge(e, o,
                      snp_name_cols = c("snp", "snp"),
                      beta_hat_cols = c("beta_hat", "beta_hat"),
                      se_cols       = c("se", "se"),
                      A1_cols       = c("A1", "A1"),
                      A2_cols       = c("A2", "A2"),
                      compute_pvals = TRUE),
    error = function(e2) { message("[", label, "] gwas_merge 失败: ",
                                   conditionMessage(e2)); NULL })
  if (is.null(X)) return(NULL)
  # ---- 2) est_cause_params: 估计 nuisance 参数(rho, 混合比例) ----
  #   X 由 e/o 全 GWAS 构建, varlist = X$snp 即全基因组变体集(非仅 clumped 工具 SNP)。
  # 用大随机子集估计 nuisance 参数(rho/混合比例), 与 cause 文档一致, 兼顾速度与精度
  varlist <- tryCatch({
    s <- X$snp
    ns <- if (length(s) > 500000) 500000 else length(s)
    if (length(s) > ns) sample(s, ns) else s
  }, error = function(e2) NULL)
  params <- tryCatch(
    cause::est_cause_params(X, variants = varlist),
    error = function(e2) { message("[", label, "] est_cause_params 失败: ",
                                   conditionMessage(e2)); NULL })
  if (is.null(params)) return(NULL)
  # ---- 3) LD 修剪: 优先用 ieugwasr::ld_clump(Plink + EUR 参考面板, cause 文档推荐路径);
  #        缺 plink/genetics.binaRies 或失败 → 退回全部 SNP(varlist), 不中断。
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
    message("[", label, "] ld_clump 失败, 退回全部 SNP: ", conditionMessage(e2))
    varlist
  })
  # ---- 4) cause: 区分"共享因果变异" vs "水平多效性" ----
  fit <- tryCatch(
    cause::cause(X = X, variants = variants, param_ests = params),
    error = function(e2) { message("[", label, "] cause() 失败: ",
                                   conditionMessage(e2)); NULL })
  if (is.null(fit)) return(NULL)
  # ---- 5) 结构化输出: 因果 vs 多效性判定 ----
  #   cause v1.2.0 未导出 causality(); 用 summary(fit)(p 值检验因果模型更优)
  #   与 fit$elpd(z 值: 因果 vs 共享/多效模型) 作判定。
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
    "CAUSAL (因果模型显著优于共享/多效模型)"
  } else {
    "PLEIOTROPY_OR_SHARING (表观效应可由共享遗传架构/水平多效解释)"
  }
  res_df <- data.frame(
    label = label, exp_id = exp_id, out_id = out_id,
    causal_p = causal_p, decision = decision,
    n_snp_merged = nrow(X), n_snp_used = length(variants),
    stringsAsFactors = FALSE)
  append_results_csv(res_df, "G1_cause.csv")
  overlap_correction_run <<- TRUE
  message("[", label, "] cause 完成. 因果 vs 共享/多效判定: ", decision,
          " (p=", if (is.na(causal_p)) "<NA>" else signif(causal_p, 3), ")")
  list(success = TRUE, label = label, exp_id = exp_id, out_id = out_id,
       n_snp = length(variants), cause_data = X, params = params, fit = fit,
       summary = summ, elpd = elpd, causal_p = causal_p, decision = decision)
}
RUN_MR_PRESSO <- FALSE  # 禁用: 非必需敏感性分析, mr_presso 10000置换极慢且无进度输出; 可日后单独补跑
run_mr <- function(dat, label) {
  res <- mr(dat, method_list = c("mr_ivw", "mr_egger_regression",
                                 "mr_weighted_median", "mr_weighted_mode"))
  het <- mr_heterogeneity(dat)              # Q / Cochran 异质性
  pleio <- mr_pleiotropy_test(dat)          # Egger 截距（水平多效性）
  loo <- mr_leaveoneout(dat)                # 留一法
  # 工具强度 F 统计量（F = beta^2 / se^2 均值；>10 合格，>20 强）
  if (!is.null(dat) && nrow(dat) > 0) {
    dat$f_stat <- (dat$beta.exposure / dat$se.exposure)^2
    f_mean <- mean(dat$f_stat, na.rm = TRUE)
    f_min  <- min(dat$f_stat, na.rm = TRUE)
    message("[", label, "] 工具 F: 均值=", round(f_mean, 2),
            " 最小=", round(f_min, 2),
            if (f_min < THRESH$fstat_min) " ⚠️ 存在弱工具(F<10)" else "")
    weak <- dat$SNP[dat$f_stat < THRESH$fstat_min]
  } else { f_mean <- f_min <- NA; weak <- character(0) }
  # MR-PRESSO 离群检测（需 devtools::install_github("rondolab/MR-PRESSO")）
  presso <- NULL
  if (RUN_MR_PRESSO && requireNamespace("MRPRESSO", quietly = TRUE)) {
    presso <- tryCatch(
      MRPRESSO::mr_presso(BetaOutcome = "beta.outcome", BetaExposure = "beta.exposure",
                          SdOutcome = "se.outcome", SdExposure = "se.exposure",
                          data = as.data.frame(dat), OUTLIERtest = TRUE,
                          DISTORTIONtest = TRUE, NbDistribution = 10000,
                          SignifThreshold = 0.05),
      error = function(e) { message("[", label, "] MR-PRESSO 失败: ",
                                    conditionMessage(e)); NULL })
  } else {
    message("[", label, "] MR-PRESSO 未安装，跳过离群检测（install: rondolab/MR-PRESSO）")
  }
  ivw_row <- res[grepl("variance weighted", res$method, ignore.case = TRUE), ]
  if (nrow(ivw_row) > 0) {
    message("[", label, "] IVW beta = ", round(ivw_row$b, 4),
            " se = ", round(ivw_row$se, 4),
            " p = ", signif(ivw_row$pval, 3))
  } else {
    message("[", label, "] 未匹配到含 'IVW' 的方法; 可用方法: ",
            paste(unique(res$method), collapse = " | "))
  }
  list(res = res, het = het, pleio = pleio, loo = loo,
       presso = presso, f_mean = f_mean, f_min = f_min, weak_iv = weak, dat = dat)
}
fwd <- run_mr(dat_fwd, "失眠→AD")
rev <- run_mr(dat_rev, "AD→失眠")

## ---- 3. 方向性加固: Steiger 过滤（排除因果方向颠倒）----
# directionality_test() 内部 mr_steiger() 需要 dat$r.exposure / dat$r.outcome。
# 失眠(ukb-b-3957)与 AD(ieu-b-2)均为二分类病例-对照, 不能用 get_r_from_pn(定量假设)推算,
# 必须用 get_r_from_lor(beta, eaf, ncase, ncontrol) 预计算。若 dat 缺 ncase/ncontrol 则优雅跳过,
# 绝不中断管线; 方向性改由双向 MR + coloc + 生物学先后判定(见 OSF §2 操作化标准)。
run_steiger <- function(dat, label) {
  if (is.null(dat) || nrow(dat) == 0) { message("[", label, "] Steiger: dat 为空, 跳过。"); return(NULL) }
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
    message("[", label, "] Steiger 跳过: 二分类性状缺 ncase/ncontrol(get_r_from_lor 必需) → 不崩溃; ",
            "方向性由双向 MR / coloc 判定。")
    return(NULL)
  }
  tryCatch(directionality_test(dat, r.exposure = r_exp, r.outcome = r_out),
           error = function(e) { message("[", label, "] Steiger 失败: ", conditionMessage(e)); NULL })
}
steiger_fwd <- run_steiger(dat_fwd, "失眠→AD")
steiger_rev <- run_steiger(dat_rev, "AD→失眠")

## ---- 4. 共定位: 失眠位点 ↔ AD GWAS 是否共享因果变异 ----
# 直接对已 harmonise 的 MR 工具变量 SNP 跑 coloc.abf：这些 SNP 自带
# beta.exposure/outcome、se、pos、samplesize，零额外联网，保证每对都产出真实 PP.H4。
# 旧版基于 ieugwasr 区域查询，在受限环境下系统性失败→单 SNP 退化→PP.H4 全 NA，已弃用。
COLOC_WINDOW_KB <- 500   # 单侧窗口（±500kb）；可按 LD 块大小调整
COLOC_P1 <- 1e-4         # 先验：单性状 SNP 为因果的概率
COLOC_P2 <- 1e-4

# 已知样本量/病例比例：coloc 定量性状需 MAF+N 估计 sdY、病例对照需 N(+s)。
# 优先用 harmonise 自带的 samplesize 列；缺失时 fallback 此处（来自 00b 核验的可靠值）。
# 注：Bellenguez(ebi-a-GCST90027158) 总 N/病例比例待 00b 复核，暂不 fallback（用 samplesize 列）。
GWAS_N <- list("ukb-b-3957" = 462341, "ieu-b-2" = 63860)   # 失眠 n；AD(Kunkle) 21982 cases+41938 ctrl
GWAS_S <- list("ieu-b-2" = 0.344, "ukb-b-3957" = 0.30)    # AD 病例比例 21982/63860;
                                                                    # 失眠 s=0.30 为 UKB 自报失眠近似估计(待文献校准, 见 Limitations)

# 由 trait 自身 GWAS 统计反推定量性状 sdY: sdY^2 ≈ median(varbeta * N * 2*maf*(1-maf))
# 这是 coloc 内部 estimatesdy 的标准近似; 传 s 后 check_dataset 必过, 不再依赖 maf+N 路径。
est_sdy_quant <- function(varbeta, maf, N) {
  v <- as.numeric(varbeta) * as.numeric(N) * 2 * as.numeric(maf) * (1 - as.numeric(maf))
  v <- v[is.finite(v) & v > 0]
  if (length(v) == 0) return(NA_real_)
  sqrt(median(v))
}

## ---- 4. 共定位(区域版): 逐独立关联位点跑 coloc.abf ----
# 标准 coloc 必须**逐独立位点**: 对暴露每个 lead SNP, 取 ±window_kb 窗口内两性状区域 SNP,
# 逐位点跑 coloc.abf。跨染色体合并工具 SNP 得到"全局 PP.H4"无意义; 且 coloc 本身无因果方向,
# 绝不能把正/反向两次不同 SNP 集的 PP.H4 不对称解读为方向证据。
# 数据来源: 冻结全 GWAS(按 pos 过滤) 或 ieugwasr 区域查询(allow_range_query, 仅取窗口)。
# 返回按位点展开的 data.frame(label / lead_snp / chr / pos / n_snps / PP.H0..H4)。

# 由 icase/icontrol(或已知 GWAS_S) 推病例比例 s(cc 型 coloc 必需)
coloc_s_from_gwas <- function(g, id = NULL) {
  if (!is.null(g$icase) && !is.null(g$icontrol)) {
    ic <- as.numeric(g$icase); nc <- as.numeric(g$icontrol)
    v <- ic / (ic + nc); v <- v[is.finite(v) & v > 0 & v < 1]
    if (length(v)) return(mean(v))
  }
  if (!is.null(id) && id %in% names(GWAS_S)) return(GWAS_S[[id]])
  NA_real_
}

# 从 harmonised dat 提取 lead SNP(已是 clump 独立工具, 直接作位点列表)
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

# 归一化窗口/全 GWAS 为统一列(snp / chr / pos / beta / se / N / icase / icontrol)
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

# 无冻结全 GWAS 时, 用 ieugwasr 区域查询取窗口(仅取窗口, 不必下全量)
fetch_coloc_window_api <- function(id, chr, start, end, label = "coloc") {
  if (!requireNamespace("ieugwasr", quietly = TRUE)) return(NULL)
  variants <- paste0(chr, ":", start, "-", end)
  d <- tryCatch(ieugwasr::associations(variants = variants, id = id),
                error = function(e) { message("[", label, "] 区域查询 ", id, " (",
                                              variants, ") 失败: ", conditionMessage(e)); NULL })
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
  # 1. 全 GWAS（优先传入, 否则冻结取; 失败(NULL)由下方分支处理）
  if (is.null(exp_gwas)) exp_gwas <- fetch_full_gwas(exp_id, paste0(label, "-exp"))
  if (is.null(out_gwas)) out_gwas <- fetch_full_gwas(out_id, paste0(label, "-out"))
  have_exp <- !is.null(exp_gwas) && nrow(exp_gwas) > 0
  have_out <- !is.null(out_gwas) && nrow(out_gwas) > 0
  if (!have_exp && !have_out && !allow_range_query) {
    message(lbl("无法取得暴露/结局全 GWAS 且禁用区域查询 → 跳过(绝不编造)。"))
    return(NULL)
  }
  # 2. lead SNPs: 给定 / harmonized / clump / 每染色体顶 SNP(退化)
  if (is.null(lead_snps) && !is.null(lead_dat)) lead_snps <- extract_lead_from_harmonized(lead_dat)
  if (is.null(lead_snps)) {
    message(lbl("未给定位点列表, 尝试从暴露全 GWAS clump 识别独立 lead SNP..."))
    if (have_exp) {
      cl_in <- exp_gwas
      if (!"SNP" %in% names(cl_in)) cl_in$SNP <- as.character(cl_in$snp)
      cl <- tryCatch(clump_data(cl_in, clump_r2 = clump_r2, clump_kb = clump_kb),
                     error = function(e) { message(lbl("clump 失败: "), conditionMessage(e)); NULL })
      if (!is.null(cl) && nrow(cl) > 0)
        lead_snps <- data.frame(snp = as.character(cl$SNP),
                                chr = as.integer(cl$chr), pos = as.integer(cl$pos),
                                stringsAsFactors = FALSE)
    }
    if (is.null(lead_snps) && have_exp && !is.null(exp_gwas$pval)) {
      message(lbl("clump 不可用, 退回每染色体 pval 最小 SNP 作为 lead。"))
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
  # ★ 真正独立 loci: 对 lead SNP 做 LD clump(r2=0.01, kb=500), 收敛到独立位点再跑 coloc
  #   避免对 2462 个连锁 SNP 全跑 coloc(缓慢且冗余); clump 失败则退回每染色体最显著 1 个 SNP。
  if (!is.null(lead_snps) && nrow(lead_snps) > 50L) {
    pv <- if (!is.null(lead_dat) && "pval.exposure" %in% names(as.data.frame(lead_dat)))
            lead_dat$pval.exposure[match(lead_snps$snp, lead_dat$SNP)] else rep(1, nrow(lead_snps))
    clumped <- tryCatch({
      ieugwasr::ld_clump(dat = data.frame(rsid = lead_snps$snp, pval = pv),
                         clump_r2 = 0.01, clump_p = 1e-3, clump_kb = 500, pop = "EUR")
    }, error = function(e) { message(lbl("LD clump 失败: "), conditionMessage(e)); NULL })
    if (!is.null(clumped) && nrow(clumped) > 0) {
      keep_rs <- as.character(clumped$rsid)
      lead_snps <- lead_snps[lead_snps$snp %in% keep_rs, , drop = FALSE]
      message(lbl("LD clump 成功: 收敛到 ", nrow(lead_snps), " 个真正独立 loci(从 ",
                  length(keep_rs), " 原始 SNP)。"))
    } else {
      ord <- order(pv)
      lead_snps <- lead_snps[ord, ]
      lead_snps <- lead_snps[!duplicated(lead_snps$chr), ]
      message(lbl("退回每染色体最显著 SNP: ", nrow(lead_snps), " 个 loci(独立近似)。"))
    }
  }
  if (is.null(lead_snps) || nrow(lead_snps) == 0) {
    message(lbl("无可用 lead SNP(clump 失败/无 pval/无 harmonized) → 跳过。"))
    return(NULL)
  }
  message(lbl("共 ", nrow(lead_snps), " 个独立 lead SNP, 逐位点跑 coloc.abf。"))
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
      message(lbl("位点 ", lsn, " (chr", chr, ":", pos, ") 取窗口失败/空, 跳过。"))
      next
    }
    snps <- intersect(as.character(sub_e$snp), as.character(sub_o$snp))
    sub_e <- sub_e[as.character(sub_e$snp) %in% snps, , drop = FALSE]
    sub_o <- sub_o[as.character(sub_o$snp) %in% snps, , drop = FALSE]
    if (nrow(sub_e) < min_snps || nrow(sub_o) < min_snps) {
      message(lbl("位点 ", lsn, " 窗口共同 SNP 不足(", nrow(sub_e), "/", nrow(sub_o),
                  "), 跳过。"))
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
    if (!is.na(s1)) d1$s <- s1 else { message(lbl("位点 ", lsn, " 暴露 s 缺失, 跳过。")); next }
    if (!is.na(s2)) d2$s <- s2 else { message(lbl("位点 ", lsn, " 结局 s 缺失, 跳过。")); next }
    cl <- tryCatch(coloc::coloc.abf(dataset1 = d1, dataset2 = d2, p1 = p1, p2 = p2),
                   error = function(e) { message(lbl("位点 ", lsn, " abf 失败: "), conditionMessage(e)); NULL })
    if (is.null(cl)) next
    s <- cl$summary
    out_rows[[length(out_rows) + 1]] <- data.frame(
      label = label, lead_snp = lsn, chr = chr, pos = pos, n_snps = nrow(sub_e),
      PP.H0 = s["PP.H0.abf"], PP.H1 = s["PP.H1.abf"], PP.H2 = s["PP.H2.abf"],
      PP.H3 = s["PP.H3.abf"], PP.H4 = s["PP.H4.abf"], stringsAsFactors = FALSE)
  }
  if (length(out_rows) == 0) { message(lbl("无任何位点产出有效 PP.H4, 返回 NULL。")); return(NULL) }
  do.call(rbind, out_rows)
}

# 正向共定位(区域版): 失眠(cc) lead ↔ AD(cc) 区域; 逐独立位点跑 coloc.abf
coloc_fwd     <- run_coloc_regional(exp_id = GWAS_ID$insomnia, out_id = GWAS_ID$ad,
                                    label = "失眠~AD", lead_dat = dat_fwd,
                                    window_kb = COLOC_WINDOW_KB)
# 反向共定位(区域版): AD(cc) lead ↔ 失眠(cc) 区域
coloc_rev     <- run_coloc_regional(exp_id = GWAS_ID$ad, out_id = GWAS_ID$insomnia,
                                    label = "AD~失眠", lead_dat = dat_rev,
                                    window_kb = COLOC_WINDOW_KB)
if (!is.null(coloc_fwd)) {
  message("[coloc] 正向 PP.H4>0.80 的位点数: ",
          sum(coloc_fwd$PP.H4 > THRESH$coloc_pph4, na.rm = TRUE),
          " / ", nrow(coloc_fwd))
  print(coloc_fwd[order(-coloc_fwd$PP.H4), c("label", "PP.H4", "n_snps")])
}
if (!is.null(coloc_rev)) {
  message("[coloc] 反向 PP.H4>0.80 的位点数: ",
          sum(coloc_rev$PP.H4 > THRESH$coloc_pph4, na.rm = TRUE),
          " / ", nrow(coloc_rev))
  print(coloc_rev[order(-coloc_rev$PP.H4), c("label", "PP.H4", "n_snps")])
}

## ---- 4b. 样本重叠校正 + 多效性区分(必需敏感性)----
# 主对(ieu-b-2)无 UKB 重叠 → 以下 MRlap/cause 仅作一致性基线(近乎无信息);
# 真正需要重叠校正的是 §4c 复制对(ukb-b-3957 × Bellenguez, 含 UKB 重叠)。
mrlap_fwd <- tryCatch(run_mrlap(dat_fwd, label = "失眠→AD"), error = function(e) NULL)
mrlap_rev <- tryCatch(run_mrlap(dat_rev, label = "AD→失眠"), error = function(e) NULL)
cause_fwd <- tryCatch(run_cause(GWAS_ID$insomnia, GWAS_ID$ad), error = function(e) NULL)
cause_rev <- tryCatch(run_cause(GWAS_ID$ad, GWAS_ID$insomnia), error = function(e) NULL)

## ---- 4c. 复制对: ukb-b-3957 × Bellenguez (含 UKB 重叠, 真正需重叠校正) ----
if (RUN_REPLICATION) {
  dat_fwd_rep <- get_harmonized(GWAS_ID$insomnia, GWAS_ID$ad_alt)   # 失眠 → Bellenguez AD
  dat_rev_rep <- get_harmonized(GWAS_ID$ad_alt, GWAS_ID$insomnia)   # Bellenguez AD → 失眠
  fwd_rep <- run_mr(dat_fwd_rep, "失眠→AD(repl Bellenguez)")
  rev_rep <- run_mr(dat_rev_rep, "AD→失眠(repl Bellenguez)")
  # 复制对共定位(区域版): 失眠 lead ↔ Bellenguez 区域; AD lead ↔ 失眠 区域 —— 两性状均为 cc
  # N / s 由冻结全 GWAS 的 n / icase / icontrol 推算(缺则 GWAS_N / GWAS_S 兜底)
  coloc_fwd_rep <- run_coloc_regional(exp_id = GWAS_ID$insomnia, out_id = GWAS_ID$ad_alt,
                                      label = "失眠~AD(repl)", lead_dat = dat_fwd_rep,
                                      window_kb = COLOC_WINDOW_KB)
  coloc_rev_rep <- run_coloc_regional(exp_id = GWAS_ID$ad_alt, out_id = GWAS_ID$insomnia,
                                      label = "AD~失眠(repl)", lead_dat = dat_rev_rep,
                                      window_kb = COLOC_WINDOW_KB)
  # ★ 复制对重叠校正: MRlap/cause 必须指向 Bellenguez(含 UKB 重叠)
  mrlap_rep_fwd <- tryCatch(run_mrlap(dat_fwd_rep, label = "失眠→AD(repl,重叠校正)"), error = function(e) NULL)
  mrlap_rep_rev <- tryCatch(run_mrlap(dat_rev_rep, label = "AD→失眠(repl,重叠校正)"), error = function(e) NULL)
  cause_rep_fwd <- tryCatch(run_cause(GWAS_ID$insomnia, GWAS_ID$ad_alt), error = function(e) NULL)
  cause_rep_rev <- tryCatch(run_cause(GWAS_ID$ad_alt, GWAS_ID$insomnia), error = function(e) NULL)
  message("[G1] 复制对 Bellenguez 双向 MR + coloc + MRlap/cause 重叠校正完成。")
} else {
  fwd_rep <- rev_rep <- coloc_fwd_rep <- coloc_rev_rep <-
    mrlap_rep_fwd <- mrlap_rep_rev <- cause_rep_fwd <- cause_rep_rev <- NULL
  message("[G1] 复制段跳过(ad_alt 未指派)。")
}

## ---- 5. 保存 ----
saveRDS(list(fwd = fwd, rev = rev,
             steiger_fwd = steiger_fwd, steiger_rev = steiger_rev,
             coloc_fwd = coloc_fwd, coloc_rev = coloc_rev,
             mrlap_fwd = mrlap_fwd, mrlap_rev = mrlap_rev,
             cause_fwd = cause_fwd, cause_rev = cause_rev,
             # 复制对(Bellenguez, 含 UKB 重叠)
             fwd_rep = if (exists("fwd_rep")) fwd_rep else NULL,
             rev_rep = if (exists("rev_rep")) rev_rep else NULL,
             coloc_fwd_rep = if (exists("coloc_fwd_rep")) coloc_fwd_rep else NULL,
             coloc_rev_rep = if (exists("coloc_rev_rep")) coloc_rev_rep else NULL,
             mrlap_rep_fwd = if (exists("mrlap_rep_fwd")) mrlap_rep_fwd else NULL,
             mrlap_rep_rev = if (exists("mrlap_rep_rev")) mrlap_rep_rev else NULL,
             cause_rep_fwd = if (exists("cause_rep_fwd")) cause_rep_fwd else NULL,
             cause_rep_rev = if (exists("cause_rep_rev")) cause_rep_rev else NULL,
             # 重叠校正运行标志(供 Limitations 披露; FALSE = 跳过/不可用)
             overlap_correction_run = overlap_correction_run),
        file.path(DIR_OUT, "G1_bidirectional.rds"))
# 额外单独保存 coloc 表（便于直接读取进表/图）
if (!is.null(coloc_fwd)) write.csv(coloc_fwd, file.path(DIR_OUT, "G1_coloc_forward.csv"), row.names = FALSE)
if (!is.null(coloc_rev)) write.csv(coloc_rev, file.path(DIR_OUT, "G1_coloc_reverse.csv"), row.names = FALSE)
if (!is.null(coloc_fwd_rep)) write.csv(coloc_fwd_rep, file.path(DIR_OUT, "G1_coloc_forward_repl.csv"), row.names = FALSE)
if (!is.null(coloc_rev_rep)) write.csv(coloc_rev_rep, file.path(DIR_OUT, "G1_coloc_reverse_repl.csv"), row.names = FALSE)
message("[G1] 双向 MR + 共定位完成。结果见 results/G1_bidirectional.rds")

## ---- 5b. 可复现性: 落盘 sessionInfo(环境/包版本快照) ----
if (exists("DIR_OUT") && is.character(DIR_OUT) && nzchar(DIR_OUT)) {
  sinfo_path <- file.path(DIR_OUT, "G1_sessionInfo.txt")
  tryCatch({
    sink(sinfo_path); print(sessionInfo()); sink()
    message("[G1] 已写出 sessionInfo: ", sinfo_path)
  }, error = function(e) message("[G1] sessionInfo 写出失败: ", conditionMessage(e)))
}
