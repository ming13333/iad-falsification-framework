# =====================================================================
# 02_protein_mediation.R  —  G2: 血浆蛋白两步中介 MR（落地机制）
# ---------------------------------------------------------------------
# Step1: 失眠 GWAS → 蛋白 pQTL (b1, se1, p1)
# Step2: 蛋白 pQTL → AD GWAS   (b2, se2, p2)
# 间接效应 ≈ b1 × b2 ; SE 用 delta 法; P 值正态近似; FDR 校正（~2923 蛋白）
# 数据: UKB Pharma Proteomics Project (UKB-PPP, Olink ~2923 蛋白)
# 依赖: 00_config.R
# =====================================================================
source("00_config.R")
library(TwoSampleMR); library(ieugwasr); library(coloc); library(dplyr)

# 默认样本量（coloc 方差估计用；若蛋白映射表提供 n_samples / n_samples_ad 则按蛋白覆盖）
# UKB-PPP Olink 面板样本量随蛋白而异，此处给保守下限，请在映射表提供真实值以提精度
UKB_PPP_N <- 50000
AD_N      <- 63860   # ieu-b-2 (Kunkle/IGAP 汇总) 总样本量

## ---- 0. 运行前守卫: AD ID 必须已核验 ----
if (is.character(GWAS_ID$ad) && GWAS_ID$ad == "PENDING_VERIFY") {
  stop("[G2] GWAS_ID$ad 仍为 PENDING_VERIFY。",
       "请先在联网 R 环境运行 00b_verify_gwas.R 核验并指派 AD ID 后再运行本脚本。")
}

## ---- 1. 加载蛋白 pQTL 汇总统计 ----
## UKB-PPP 的 ~2923 蛋白 pQTL 多数需从 UKB RAP / 发布源取得本地 GWAS，
## 再用 read_exposure_data() 读入；少数已在 IEU 托管（ieu-a-PROT...）。
## 下面给出「本地文件」与「IEU」两种加载模板，按你的数据来源二选一。
## 蛋白名 → 文件/ID 的映射表需事先准备好（含 Olink target 名，便于核对 GFAP/NfL）。
#
# 方式A（本地文件，推荐）: 每个蛋白一个 GWAS 文件
#   protein_map <- read.csv(file.path(DIR_DATA, "ukbppp_protein_gwas_index.csv"))
#   # 列: protein_id, olink_target, file
# 方式B（IEU）:
#   protein_ids <- c("ieu-a-PROT1", "ieu-a-PROT2", ...)   # 由 ieugwasr 筛选 UKB-PPP 来源

protein_csv <- file.path(DIR_DATA, "ukbppp_protein_gwas_index.csv")
if (!file.exists(protein_csv)) {
  stop("[G2] 缺少蛋白 pQTL 映射表: ", protein_csv,
       "\n请先准备该文件，期望列: protein_id, olink_target, file(本地GWAS路径) 或 ieu_id(IEU托管时)。",
       "\n来源: UKB-PPP Olink ~2923 蛋白；本地文件用 read_exposure_data 读入，IEU 托管用 extract_instruments。")
}
protein_map <- read.csv(protein_csv, stringsAsFactors = FALSE)
# 兼容 file/ieu_id 两种来源列：统一成 source 列 + id/path 列
if ("ieu_id" %in% names(protein_map) && !"file" %in% names(protein_map)) {
  protein_map$source <- "ieu"
  protein_map$path   <- protein_map$ieu_id
} else if ("file" %in% names(protein_map)) {
  protein_map$source <- "local"
  protein_map$path   <- protein_map$file
} else {
  stop("[G2] 映射表必须含 'file'(本地路径) 或 'ieu_id'(IEU ID) 列之一。")
}
# protein_id 列兜底
if (!"protein_id" %in% names(protein_map)) stop("[G2] 映射表缺 protein_id 列。")
if (!"olink_target" %in% names(protein_map)) {
  warning("[G2] 映射表缺 olink_target 列，将用 protein_id 作 target。")
  protein_map$olink_target <- protein_map$protein_id
}
if (!"n_samples" %in% names(protein_map))
  warning("[G2] 映射表缺 n_samples 列，coloc 蛋白侧 N 将用默认 UKB_PPP_N=",
          UKB_PPP_N, "（建议补充真实蛋白样本量以提精度）")
message("[G2] 加载蛋白映射表: ", nrow(protein_map), " 个蛋白 (",
        sum(protein_map$source == "local"), " 本地 / ",
        sum(protein_map$source == "ieu"), " IEU)")

## ---- 工具: 对单对(暴露GWAS id, 结局GWAS id)跑 IVW 并取 b/se/p ----
## 蛋白 pQTL 可能是本地文件(source="local")或 IEU 托管(source="ieu")。
## 下面两个 helper 把“取暴露工具”与“取结局关联”按来源分流。

get_protein_instruments <- function(protein_row, p1 = 5e-8) {
  # 返回 clumped 暴露工具 data.frame（TwoSampleMR 格式）
  if (protein_row$source == "ieu") {
    extract_instruments(protein_row$path, p1 = p1,
                        r2 = THRESH$clump_r2, kb = THRESH$clump_kb)
  } else {
    # 本地 GWAS 文件: 列需含 SNP, beta, se, pval, chr/pos, eaf 等
    read_exposure_data(
      filename = protein_row$path,
      clump = TRUE, clump_r2 = THRESH$clump_r2, clump_kb = THRESH$clump_kb,
      pval_threshold = p1,
      snp_col = "SNP", beta_col = "beta", se_col = "se",
      pval_col = "pval", chr_col = "chr", pos_col = "pos",
      eaf_col = "eaf", effect_allele_col = "effect_allele",
      other_allele_col = "other_allele")
  }
}

get_protein_outcome <- function(snps, protein_row) {
  if (protein_row$source == "ieu") {
    extract_outcome_data_batched(snps = snps, outcomes = protein_row$path)
  } else {
    # 本地文件: 读全文后按 SNP 子集（避免反复读盘，可在循环外缓存，此处从简）
    full <- read_exposure_data(
      filename = protein_row$path, clump = FALSE,
      snp_col = "SNP", beta_col = "beta", se_col = "se",
      pval_col = "pval", chr_col = "chr", pos_col = "pos",
      eaf_col = "eaf", effect_allele_col = "effect_allele",
      other_allele_col = "other_allele")
    full <- full[full$SNP %in% snps, ]
    # 转成 outcome 格式（read_exposure_data 输出 exposure.* 列，需 rename）
    names(full) <- gsub("\\.exposure$", ".outcome", names(full))
    full$outcome <- protein_row$olink_target
    full
  }
}

# 通用两样本 IVW（暴露/结局均为 IEU id 时用）
ivw_est <- function(exp_id, out_id, p1 = 5e-8) {
  exp <- extract_instruments(exp_id, p1 = p1,
                             r2 = THRESH$clump_r2, kb = THRESH$clump_kb)
  if (nrow(exp) == 0) return(NULL)
  out <- tryCatch(extract_outcome_data_batched(snps = exp$SNP, outcomes = out_id), error = function(e) NULL)
  if (is.null(out) || nrow(out) == 0) return(NULL)
  d <- harmonise_data(exp, out)
  if (nrow(d) < 3) return(NULL)
  res <- mr(d, method_list = "mr_ivw")
  row <- res[res$method == "MR IVW", ]
  if (nrow(row) == 0) return(NULL)
  data.frame(b = row$b, se = row$se, p = row$pval, n_snps = nrow(d),
             stringsAsFactors = FALSE)
}

# 蛋白作暴露或结局的 IVW（按 protein_row 来源分流）
ivw_est_protein <- function(exp_obj_or_row, out_obj_or_row, exp_is_protein, out_is_protein,
                            p1 = 5e-8) {
  # 取暴露工具
  if (exp_is_protein) {
    exp <- get_protein_instruments(exp_obj_or_row, p1 = p1)
  } else {
    exp <- extract_instruments(exp_obj_or_row, p1 = p1,
                               r2 = THRESH$clump_r2, kb = THRESH$clump_kb)
  }
  if (is.null(exp) || nrow(exp) == 0) return(NULL)
  # 取结局关联
  if (out_is_protein) {
    out <- tryCatch(get_protein_outcome(exp$SNP, out_obj_or_row), error = function(e) NULL)
  } else {
    out <- tryCatch(extract_outcome_data_batched(snps = exp$SNP, outcomes = out_obj_or_row), error = function(e) NULL)
  }
  if (is.null(out) || nrow(out) == 0) return(NULL)
  d <- harmonise_data(exp, out)
  if (nrow(d) < 3) return(NULL)
  res <- mr(d, method_list = "mr_ivw")
  row <- res[res$method == "MR IVW", ]
  if (nrow(row) == 0) return(NULL)
  data.frame(b = row$b, se = row$se, p = row$pval, n_snps = nrow(d),
             stringsAsFactors = FALSE)
}

## ---- 2a. Step1 重叠稳健敏感性（休眠钩子，默认关闭）----
## 背景: Step1(失眠 ukb-b-3957 ↔ 蛋白 UKB-PPP) 双侧均 UKB → 样本重叠,
##       delta 法 SE 会低估(见 §3 局限)。此钩子用 MRlap 对每蛋白 Step1 MR 做重叠稳健校正,
##       作为【敏感性】, 不覆盖主结果(delta 法 SE)。
## 默认 G2_STEP1_MRLAP = FALSE; 仅当 MRlap 已安装且显式置 TRUE 时,
##       在【真实 R 环境】逐蛋白跑 mr_lap, 写入 b1_mrlap/se1_mrlap/p1_mrlap。
## ⚠️ 沙箱无法验证此钩子( MRlap 未安装/无法跑 ); 上线前须在真实 R 环境跑一遍校准
##       mr_lap 签名与返回列名(不同 MRlap 版本可能不同)。Methods/Limitations 须显式
##       披露 Step1 残余 UKB 重叠(失眠×蛋白同 UKB)——诚实边界, 不可省。
G2_STEP1_MRLAP <- FALSE   # 显式开关。实_env 开启前须确认 MRlap 已安装。

step1_mrlap_est <- function(protein_row, exp_id, p1 = 5e-8) {
  # 取失眠工具(暴露) + 蛋白关联(结局), 跑 MRlap 校正 Step1
  exp <- extract_instruments(exp_id, p1 = p1,
                             r2 = THRESH$clump_r2, kb = THRESH$clump_kb)
  if (is.null(exp) || nrow(exp) == 0) return(NULL)
  out <- tryCatch(get_protein_outcome(exp$SNP, protein_row), error = function(e) NULL)
  if (is.null(out) || nrow(out) == 0) return(NULL)
  d <- tryCatch(harmonise_data(exp, out), error = function(e) NULL)
  if (is.null(d) || nrow(d) < 3) return(NULL)
  if (!requireNamespace("MRlap", quietly = TRUE)) {
    message("[G2-mrlap] MRlap 未安装, 跳过 ", protein_row$protein_id)
    return(NULL)
  }
  res <- tryCatch(MRlap::mr_lap(exposure = d, pval_threshold = p1),
                  error = function(e) {
                    message("[G2-mrlap] ", protein_row$protein_id,
                            " mr_lap 失败: ", conditionMessage(e)); NULL })
  if (is.null(res)) return(NULL)
  # 提取 MRlap 主估计 —— 候选列名/访问方式, 实_env 须按已装 MRlap 版本校准
  beta <- se <- pval <- NULL
  if (!is.null(res$beta)) beta <- res$beta
  if (!is.null(res$se))   se   <- res$se
  if (!is.null(res$pval)) pval <- res$pval
  if (is.null(beta) && is.data.frame(res)) {
    cn <- tolower(names(res))
    if ("beta" %in% cn) beta <- res[[which(cn == "beta")[1]]]
    if ("se"   %in% cn) se   <- res[[which(cn == "se")[1]]]
    if ("pval" %in% cn) pval <- res[[which(cn == "pval")[1]]]
  }
  if (is.null(beta) || is.null(se)) {
    message("[G2-mrlap] ", protein_row$protein_id,
            " 无法从 mr_lap 结果提取 beta/se, 请按已装 MRlap 版本校准 step1_mrlap_est")
    return(NULL)
  }
  data.frame(b1_mrlap = beta, se1_mrlap = se,
             p1_mrlap = if (is.null(pval)) NA_real_ else pval,
             stringsAsFactors = FALSE)
}

## ---- 2. 两步中介 ----
insomnia_exp_id <- GWAS_ID$insomnia
ad_out_id       <- GWAS_ID$ad

rows <- list()
for (i in seq_len(nrow(protein_map))) {
  prow <- protein_map[i, ]
  pid  <- prow$protein_id
  name <- prow$olink_target
  # Step1: 失眠 → 蛋白（蛋白作结局）
  s1 <- tryCatch(ivw_est_protein(exp_obj_or_row = insomnia_exp_id,
                                 out_obj_or_row = prow,
                                 exp_is_protein = FALSE, out_is_protein = TRUE),
                 error = function(e) { message("[G2] step1 ", pid, " err: ",
                                               conditionMessage(e)); NULL })
  if (is.null(s1)) next
  # Step1 重叠稳健敏感性(MRlap 休眠钩子): 仅 G2_STEP1_MRLAP=TRUE 且 MRlap 已安装时跑,
  # 不覆盖主结果(delta 法); 见 step1_mrlap_est 定义与文件头 §2a 注释。
  s1m <- NULL
  if (G2_STEP1_MRLAP) {
    s1m <- tryCatch(step1_mrlap_est(prow, insomnia_exp_id),
                    error = function(e) { message("[G2-mrlap] ", pid, " err: ",
                                                  conditionMessage(e)); NULL })
  }
  # Step2: 蛋白 → AD（蛋白作暴露）
  s2 <- tryCatch(ivw_est_protein(exp_obj_or_row = prow,
                                 out_obj_or_row = ad_out_id,
                                 exp_is_protein = TRUE, out_is_protein = FALSE),
                 error = function(e) { message("[G2] step2 ", pid, " err: ",
                                               conditionMessage(e)); NULL })
  if (is.null(s2)) next
  rows[[pid]] <- data.frame(
    protein = pid, target = name, source = prow$source,
    b1 = s1$b, se1 = s1$se, p1 = s1$p, n1 = s1$n_snps,
    b2 = s2$b, se2 = s2$se, p2 = s2$p, n2 = s2$n_snps,
    b1_mrlap = if (is.null(s1m)) NA_real_ else s1m$b1_mrlap,
    se1_mrlap = if (is.null(s1m)) NA_real_ else s1m$se1_mrlap,
    p1_mrlap = if (is.null(s1m)) NA_real_ else s1m$p1_mrlap,
    stringsAsFactors = FALSE
  )
  if (i %% 200 == 0) message("[G2] 已处理 ", i, " / ", nrow(protein_map))
}
if (length(rows) == 0) stop("[G2] 未得到任何蛋白的两步估计，检查 GWAS ID / 数据可达性 / 映射表路径。")

mediation <- bind_rows(rows)

## ---- 3. 间接效应 + 乘积法 SE（delta 法）+ P 值 ----
# 公式复核（2024-2025 蛋白中介 MR 通用写法）：
#   indirect = b1 * b2                              （乘积法点估计）
#   se_ind   = sqrt(b2^2*se1^2 + b1^2*se2^2)        （delta 法，假设两步独立）
#   p_ind    = 2 * pnorm(-|indirect|/se_ind)        （正态近似）
#   fdr      = p.adjust(p_ind, "fdr")               （~2923 蛋白多重检验）
# ⚠️ 关键局限: 两步(失眠→蛋白 / 蛋白→AD)若共用 UKB-PPP 与含 UKB 的 BenElsworth(ukb-b-3957)/Bellenguez,
#   则两步样本不独立 → delta 法 SE 会【低估】, P 值偏小, FDR 膨胀假阳性。
#   缓解建议(敏感性):
#     (a) bootstrap 重抽样估计 SE: 对工具 SNP 非参数 bootstrap R=1000 次,
#         每次重算 b1*b2, 取经验分位数 (2.5%,97.5%) 作 95% CI;
#     (b) 用 MRlap 校正两步各自的样本重叠后再做乘积;
#     (c) 若有非重叠的蛋白 pQTL(如 SCALLOP/AGA) 或独立 AD 源(Kunkle/IGAP),
#         作敏感性复制。沙箱无法跑 bootstrap, 本脚本给 delta 法主结果 + 注释。
#     (d) Step1(失眠↔蛋白, 双侧均 UKB)重叠的 MRlap 校正已接线为【休眠敏感性钩子】
#         (step1_mrlap_est + 开关 G2_STEP1_MRLAP, 默认 FALSE): 仅实_env 且 MRlap
#         已安装且显式开 Flag 时, 逐蛋白跑 mr_lap 并写入 b1_mrlap/se1_mrlap/p1_mrlap;
#         主结果 SE 仍为 delta 法。Methods/Limitations 须显式披露此残余 UKB 重叠。
mediation <- mediation %>%
  mutate(
    indirect = b1 * b2,
    se_ind   = sqrt(b2^2 * se1^2 + b1^2 * se2^2),   # delta 法（假设两步独立；见上局限）
    p_ind    = 2 * pnorm(-abs(indirect) / se_ind),
    fdr      = p.adjust(p_ind, method = "fdr")
  ) %>%
  arrange(p_ind)

## ---- 4. 显著候选（FDR<0.05）----
sig <- mediation[mediation$fdr < THRESH$protein_fdr, ]
message("[G2] 总蛋白数=", nrow(mediation),
        " | FDR<", THRESH$protein_fdr, " 显著候选=", nrow(sig))
top <- mediation[order(-abs(mediation$indirect)), ][1:20, ]
message("[G2] 候选介导蛋白 top20 (按 |indirect|):")
print(top[, c("protein", "target", "b1", "b2", "indirect", "se_ind", "p_ind", "fdr")])

## ---- 5. coloc 复核 top 蛋白 (蛋白 pQTL ↔ AD 共享变异) ----
# 对显著(FDR<THRESH$protein_fdr)或 top20 蛋白, 逐一取蛋白 pQTL 的 lead SNP 附近
# 区域关联 + AD 的同区域关联, 跑 coloc.abf, 收集 PP.H4 (>0.80 为共定位支持)。
coloc_protein <- function(protein_row, out_id, window_kb = 500, label = "prot~AD") {
  # 取蛋白 pQTL 的 clumped lead SNP
  pexp <- tryCatch(get_protein_instruments(protein_row), error = function(e) NULL)
  if (is.null(pexp) || nrow(pexp) == 0) return(NULL)
  # 兼容 read_exposure_data 本地文件列名 chr.exposure/pos.exposure
  # （extract_instruments 的 IEU 蛋白返回 chr/pos；本地文件为 chr.exposure/pos.exposure）
  if (is.null(pexp$chr) && !is.null(pexp$chr.exposure)) pexp$chr <- pexp$chr.exposure
  if (is.null(pexp$pos) && !is.null(pexp$pos.exposure)) pexp$pos <- pexp$pos.exposure
  lead <- unique(pexp$SNP)
  out_list <- list()
  for (snp in lead) {
    # lead SNP 的 chr/pos
    chr <- pexp$chr[pexp$SNP == snp][1]
    pos <- pexp$pos[pexp$SNP == snp][1]
    if (is.na(chr) || is.na(pos)) {
      # 回退: 用 IEU variants_search(仅 IEU 蛋白可行)
      si <- tryCatch(ieugwasr::variants_search(snp), error = function(e) NULL)
      if (is.null(si) || nrow(si) == 0) next
      chr <- si$chr[1]; pos <- si$pos[1]
    }
    lo <- pos - window_kb * 1000L; hi <- pos + window_kb * 1000L
    win <- tryCatch(ieugwasr::variants_to_rsid(
              ieugwasr::variants_chrpos(chr = chr, from = lo, to = hi)),
            error = function(e) snp)
    # 区域查询失败(退化为单 lead SNP)→ 单 SNP coloc 价值极低, 安全跳过
    if (length(win) <= 1) {
      message("[G2-coloc] ", protein_row$protein_id, " ", snp,
              " 窗口区域查询失败(仅 lead SNP), 跳过 coloc")
      next
    }
    # 蛋白侧窗口关联（本地文件按 SNP 子集; IEU 用 associations）
    if (protein_row$source == "ieu") {
      ap <- tryCatch(ieugwasr::associations(variants = win, id = protein_row$path),
                     error = function(e) NULL)
      if (!is.null(ap)) {
        if (is.null(ap$rsid) && !is.null(ap$name)) ap$rsid <- as.character(ap$name)
        if (is.null(ap$position) && !is.null(ap$pos)) ap$position <- ap$pos
      }
    } else {
      full <- tryCatch(get_protein_outcome(win, protein_row), error = function(e) NULL)
      ap <- if (is.null(full)) NULL else
        data.frame(rsid = as.character(full$SNP),
                   beta = full$beta.outcome, se = full$se.outcome,
                   position = if (!is.null(full$pos.outcome)) full$pos.outcome else NA,
                   stringsAsFactors = FALSE)
    }
    aa <- tryCatch(ieugwasr::associations(variants = win, id = out_id),
                   error = function(e) NULL)
    if (!is.null(aa)) {
      if (is.null(aa$rsid) && !is.null(aa$name)) aa$rsid <- as.character(aa$name)
      if (is.null(aa$position) && !is.null(aa$pos)) aa$position <- aa$pos
    }
    if (is.null(ap) || is.null(aa)) next
    ap <- ap[!is.na(ap$beta) & !is.na(ap$se), ]
    aa <- aa[!is.na(aa$beta) & !is.na(aa$se), ]
    # coloc.abf 强制要求 position 非缺失（与 G1 一致）
    if (is.null(ap$position) || any(is.na(ap$position))) {
      message("[G2-coloc] ", protein_row$protein_id, " ", snp,
              " 蛋白侧 position 缺失，跳过该 locus"); next }
    if (is.null(aa$position) || any(is.na(aa$position))) {
      message("[G2-coloc] ", protein_row$protein_id, " ", snp,
              " AD 侧 position 缺失，跳过该 locus"); next }
    m <- merge(ap, aa, by = "rsid", suffixes = c(".p", ".a"))
    if (nrow(m) == 0) next
    # 蛋白(quant)侧需 sdY 或 (MAF + N) 估计方差; 缺则补 MAF(由 eaf)+ N(面板样本量)
    maf_p <- if (!is.null(m$eaf.p)) m$eaf.p else
             if (!is.null(m$maf.p)) m$maf.p else rep(0.5, nrow(m))
    n_p   <- if (!is.null(protein_row$n_samples)) protein_row$n_samples else UKB_PPP_N
    n_a   <- if (!is.null(protein_row$n_samples_ad)) protein_row$n_samples_ad else AD_N
    d1 <- list(beta = m$beta.p, varbeta = m$se.p^2, snp = m$rsid,
               position = as.integer(m$position.p), MAF = maf_p, N = n_p,
               type = "quant")
    d2 <- list(beta = m$beta.a, varbeta = m$se.a^2, snp = m$rsid,
               position = as.integer(m$position.a), N = n_a, type = "cc")
    cl <- tryCatch(coloc::coloc.abf(dataset1 = d1, dataset2 = d2, p1 = 1e-4, p2 = 1e-4),
                   error = function(e) { message("[G2-coloc] ", protein_row$protein_id,
                                                 " ", snp, " abf 失败: ", conditionMessage(e)); NULL })
    if (is.null(cl)) next
    s <- cl$summary
    out_list[[snp]] <- data.frame(
      protein = protein_row$protein_id, target = protein_row$olink_target,
      lead_snp = snp, chr = chr, pos = pos, n_snps = nrow(m),
      PP.H4 = unname(s["PP.H4.abf"]), coloc_pass = unname(s["PP.H4.abf"] > THRESH$coloc_pph4),
      stringsAsFactors = FALSE)
  }
  if (length(out_list) == 0) return(NULL)
  bind_rows(out_list)
}

# 选复核对象: 显著 ∪ top20
review_set <- unique(c(sig$protein, top$protein))
review_rows <- protein_map[protein_map$protein_id %in% review_set, ]
message("[G2] coloc 复核蛋白数: ", nrow(review_rows))
coloc_results <- list()
for (i in seq_len(nrow(review_rows))) {
  cr <- tryCatch(coloc_protein(review_rows[i, ], ad_out_id, label = "prot~AD"),
                 error = function(e) { message("[G2] coloc ", review_rows$protein_id[i],
                                               " err: ", conditionMessage(e)); NULL })
  if (!is.null(cr)) coloc_results[[review_rows$protein_id[i]]] <- cr
}
coloc_df <- if (length(coloc_results) > 0) bind_rows(coloc_results) else NULL
if (!is.null(coloc_df)) {
  # 每个蛋白取最大 PP.H4 作为该蛋白的 coloc 证据
  coloc_summary <- coloc_df %>%
    group_by(protein, target) %>%
    summarise(coloc_pph4 = max(PP.H4, na.rm = TRUE),
              coloc_pass = any(coloc_pass, na.rm = TRUE),
              n_loci = n(), .groups = "drop")
  mediation <- mediation %>%
    left_join(coloc_summary, by = c("protein", "target"))
  message("[G2] coloc PP.H4>0.80 的蛋白数: ",
          sum(coloc_summary$coloc_pass, na.rm = TRUE), " / ", nrow(coloc_summary))
} else {
  mediation$coloc_pph4 <- NA_real_
  mediation$coloc_pass <- NA
  message("[G2] 无蛋白完成 coloc 复核（可能本地文件缺 chr/pos 或 AD 关联拉取失败）。")
}

## ---- 6. 反向机制对照: AD → 蛋白 → 失眠 (证伪) ----
# 同结构反跑: step1=AD→蛋白(蛋白作结局), step2=蛋白→失眠(蛋白作暴露)
# 若正向(失眠→蛋白→AD)显著而反向不显著 → 支持失眠位于 AD 上游的方向。
rows_rev <- list()
for (i in seq_len(nrow(protein_map))) {
  prow <- protein_map[i, ]
  pid  <- prow$protein_id
  name <- prow$olink_target
  # 反向 step1: AD → 蛋白
  s1r <- tryCatch(ivw_est_protein(exp_obj_or_row = ad_out_id,
                                  out_obj_or_row = prow,
                                  exp_is_protein = FALSE, out_is_protein = TRUE),
                  error = function(e) NULL)
  if (is.null(s1r)) next
  # 反向 step2: 蛋白 → 失眠
  s2r <- tryCatch(ivw_est_protein(exp_obj_or_row = prow,
                                  out_obj_or_row = insomnia_exp_id,
                                  exp_is_protein = TRUE, out_is_protein = FALSE),
                  error = function(e) NULL)
  if (is.null(s2r)) next
  rows_rev[[pid]] <- data.frame(
    protein = pid, target = name,
    b1_rev = s1r$b, se1_rev = s1r$se, p1_rev = s1r$p, n1_rev = s1r$n_snps,
    b2_rev = s2r$b, se2_rev = s2r$se, p2_rev = s2r$p, n2_rev = s2r$n_snps,
    stringsAsFactors = FALSE)
  if (i %% 200 == 0) message("[G2-rev] 已处理 ", i, " / ", nrow(protein_map))
}
if (length(rows_rev) > 0) {
  mediation_rev <- bind_rows(rows_rev) %>%
    mutate(
      indirect_rev = b1_rev * b2_rev,
      se_ind_rev   = sqrt(b2_rev^2 * se1_rev^2 + b1_rev^2 * se2_rev^2),
      p_ind_rev    = 2 * pnorm(-abs(indirect_rev) / se_ind_rev),
      fdr_rev      = p.adjust(p_ind_rev, method = "fdr")
    ) %>%
    arrange(p_ind_rev)
  # 与正向对比: 正向显著(FDR<0.05) 且 反向不显著(FDR>=0.05) → 方向证据
  direction_cmp <- mediation %>%
    select(protein, target, p_ind, fdr, indirect) %>%
    left_join(mediation_rev %>% select(protein, p_ind_rev, fdr_rev, indirect_rev),
              by = "protein") %>%
    mutate(
      fwd_sig = fdr < THRESH$protein_fdr,
      rev_sig = (!is.na(fdr_rev)) & (fdr_rev < THRESH$protein_fdr),
      direction_support = fwd_sig & !rev_sig   # 正向显著 & 反向不显著
    )
  n_dir <- sum(direction_cmp$direction_support, na.rm = TRUE)
  message("[G2-rev] 反向两步完成。正向显著且反向不显著(支持方向)的蛋白数: ",
          n_dir, " / ", nrow(direction_cmp))
} else {
  mediation_rev <- NULL
  direction_cmp <- NULL
  message("[G2-rev] 反向两步未得到任何估计（可能数据受限）。反向证伪未完成。")
}

## ---- 7. 保存 ----
saveRDS(list(mediation = mediation, sig = sig, top = top,
             coloc_df = coloc_df, coloc_summary = if(exists("coloc_summary")) coloc_summary else NULL,
             mediation_rev = mediation_rev, direction_cmp = direction_cmp),
        file.path(DIR_OUT, "G2_protein_mediation.rds"))
saveRDS(sig, file.path(DIR_OUT, "G2_protein_mediation_significant.rds"))
write.csv(mediation, file.path(DIR_OUT, "G2_mediation_table.csv"), row.names = FALSE)
if (!is.null(mediation_rev)) write.csv(mediation_rev, file.path(DIR_OUT, "G2_mediation_reverse.csv"), row.names = FALSE)
if (!is.null(coloc_df)) write.csv(coloc_df, file.path(DIR_OUT, "G2_protein_coloc.csv"), row.names = FALSE)
if (!is.null(direction_cmp)) write.csv(direction_cmp, file.path(DIR_OUT, "G2_direction_comparison.csv"), row.names = FALSE)
message("[G2] 蛋白两步中介完成。结果见 results/G2_protein_mediation.rds (+ *_table.csv / *_reverse.csv / *_coloc.csv)")
