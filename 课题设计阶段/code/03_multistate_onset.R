# =====================================================================
# 03_multistate_onset.R  —  G4: 多状态发病顺序模型（时序与预后）
# ---------------------------------------------------------------------
# 状态: S0 健康 | S1 仅失眠 | S2 仅 AD | S3 共病 | + 死亡(吸收)
# 目标转移: 0->1, 0->2, 1->3(失眠先), 2->3(AD先), 0->3, ->死亡
# 模型: 连续时间多状态 Markov (msm); 年龄作时间尺度(左截断)
# 数据: UKB 个体级（需权限提取字段见设计文档第五节）
# 依赖: 00_config.R
#
# 注意: 本脚本为"填入数据即可跑"的可执行骨架, 不含任何假数据。
#       需在具备 UKB 个体级权限 + R 环境中运行。
# =====================================================================
source("00_config.R")
suppressPackageStartupMessages({
  library(msm)
  library(survival)
  library(dplyr)
  library(ggplot2)
})

## ====================================================================
## ---- 1. 读取 UKB 个体级提取 ----
## ====================================================================
# 期望列(必需):
REQUIRED_COLS <- c(
  "eid",           # 个体 ID
  "t_insomnia",    # 失眠发病年龄(或 NA)
  "t_ad",          # AD 发病年龄(或 NA)
  "t_death",       # 死亡年龄或删失年龄
  "event_death",   # 1=死亡, 0=删失
  "age0",          # 基线年龄
  "sex",           # 性别
  "education",     # 教育年限/等级
  "depression",    # 抑郁(0/1 或量表分)
  "apoe_e4",       # APOE ε4 携带数(0/1/2)
  "hypnotic_use"   # 安眠药使用(0/1)
)

# 可选列(敏感性分析用):
OPTIONAL_COLS <- c(
  "t_insomnia_icd",   # 住院 ICD-10 G47.0 诊断年龄(敏感性 a)
  "t_dementia"        # 全因痴呆发病年龄(敏感性 b)
)

# 数据文件候选路径(优先 RDS, 其次 CSV)
DATA_FILE_RDS <- file.path(DIR_DATA, "ukb_longwide.rds")
DATA_FILE_CSV <- file.path(DIR_DATA, "ukb_longwide.csv")

load_ukb_data <- function() {
  if (file.exists(DATA_FILE_RDS)) {
    message("[G4] 读取 RDS: ", DATA_FILE_RDS)
    df <- readRDS(DATA_FILE_RDS)
  } else if (file.exists(DATA_FILE_CSV)) {
    message("[G4] 读取 CSV: ", DATA_FILE_CSV)
    df <- read.csv(DATA_FILE_CSV, stringsAsFactors = FALSE)
  } else {
    stop(
      "[G4] ⛔ UKB 个体级数据文件未找到。\n",
      "  期望路径(任一):\n",
      "    ", DATA_FILE_RDS, "\n",
      "    ", DATA_FILE_CSV, "\n",
      "  必需列: ", paste(REQUIRED_COLS, collapse = ", "), "\n",
      "  可选列: ", paste(OPTIONAL_COLS, collapse = ", "), "\n",
      "  数据需从 UKB 申请权限后提取(字段 2245/2255/G47.0/F00/G30/死亡登记/APOE ε4)。"
    )
  }

  # 校验必需列
  missing <- setdiff(REQUIRED_COLS, names(df))
  if (length(missing) > 0) {
    stop("[G4] ⛔ 数据缺少必需列: ", paste(missing, collapse = ", "),
         "\n  期望列: ", paste(REQUIRED_COLS, collapse = ", "))
  }

  # 报告可选列状态
  opt_present <- intersect(OPTIONAL_COLS, names(df))
  opt_absent  <- setdiff(OPTIONAL_COLS, names(df))
  if (length(opt_present) > 0)
    message("[G4] 可选列已就绪(敏感性可用): ", paste(opt_present, collapse = ", "))
  if (length(opt_absent) > 0)
    message("[G4] 可选列缺失(对应敏感性将跳过): ", paste(opt_absent, collapse = ", "))

  message("[G4] 数据载入成功: ", nrow(df), " 行, ", ncol(df), " 列")
  return(df)
}

df <- load_ukb_data()

## ====================================================================
## ---- 1b. 数据清洗 ----
## ====================================================================
clean_ukb_data <- function(d) {
  n0 <- nrow(d)

  # 排除基线年龄或死亡年龄缺失
  d <- d %>% filter(!is.na(age0) & !is.na(t_death))

  # 排除死亡早于基线的记录
  d <- d %>% filter(t_death >= age0)

  # 若条件发病年龄晚于死亡, 则置 NA(未真正发病)
  d <- d %>% mutate(
    t_insomnia = ifelse(!is.na(t_insomnia) & t_insomnia > t_death,
                        NA_real_, t_insomnia),
    t_ad       = ifelse(!is.na(t_ad) & t_ad > t_death,
                        NA_real_, t_ad)
  )

  # 数值型保证
  d <- d %>% mutate(
    age0         = as.numeric(age0),
    t_insomnia   = as.numeric(t_insomnia),
    t_ad         = as.numeric(t_ad),
    t_death      = as.numeric(t_death),
    event_death  = as.integer(event_death),
    apoe_e4      = as.integer(apoe_e4)
  )

  n1 <- nrow(d)
  if (n0 - n1 > 0)
    message("[G4] 数据清洗: 排除 ", n0 - n1, " 行(缺失/异常), 剩余 ", n1, " 行")
  return(d)
}

df <- clean_ukb_data(df)

## ====================================================================
## ---- 2. 构造多状态长表 ----
## ====================================================================
# 状态编码: 1=S0(健康), 2=S1(仅失眠), 3=S2(仅AD), 4=S3(共病), 5=死亡
#
# msm 需要面板数据: 每行 = (eid, age, state)
# 每个个体的事件时间线被拆成多行观测点。
#
# 左截断(left truncation)处理方式:
#   msm 以 age 为时间变量时, 不同 subject 首次观测年龄(age0)不同。
#   模型自动条件于"存活至 age0 时处于观测状态"——即标准左截断。
#   对于基线时已有失眠/AD 的 prevalent case, 同样条件于基线状态,
#   但基线前的状态持续时间未知(已知局限, 在 Limitations 披露)。

# 2a. 宽表层面标注路径(用于后续生存分析)
build_paths <- function(d) {
  d <- d %>% mutate(
    path = case_when(
      is.na(t_insomnia) & is.na(t_ad) ~ "S0",
      !is.na(t_insomnia) & is.na(t_ad) ~ "S1",
      is.na(t_insomnia) & !is.na(t_ad) ~ "S2",
      !is.na(t_insomnia) & !is.na(t_ad) &
        t_insomnia < t_ad ~ "S1thenS3",
      !is.na(t_insomnia) & !is.na(t_ad) &
        t_ad < t_insomnia ~ "S2thenS3",
      !is.na(t_insomnia) & !is.na(t_ad) &
        t_insomnia == t_ad ~ "S3_simul",
      TRUE ~ "unknown"
    )
  )
  return(d)
}

df <- build_paths(df)
message("[G4] 路径分布:\n",
        paste(capture.output(table(df$path, useNA = "ifany")), collapse = "\n"))

# 2b. 宽表 → msm 长表(每个 eid 多行, 每行一个 age-state 观测点)
wide_to_msm_long <- function(d) {
  rows <- vector("list", nrow(d))

  for (i in seq_len(nrow(d))) {
    eid_i   <- d$eid[i]
    age0_i  <- d$age0[i]
    t_ins   <- d$t_insomnia[i]
    t_ad_i  <- d$t_ad[i]
    t_dth   <- d$t_death[i]
    evt     <- d$event_death[i]
    cov_i   <- d[i, c("age0", "sex", "education", "depression",
                       "apoe_e4", "hypnotic_use"), drop = FALSE]

    # -- 确定基线状态 --
    ins_at_bl <- !is.na(t_ins) && t_ins <= age0_i
    ad_at_bl  <- !is.na(t_ad_i) && t_ad_i <= age0_i

    if (ins_at_bl && ad_at_bl)       init_state <- 4L  # S3
    else if (ins_at_bl)              init_state <- 2L  # S1
    else if (ad_at_bl)               init_state <- 3L  # S2
    else                             init_state <- 1L  # S0

    # -- 构建观测时间线 (age, state) --
    obs <- list()
    obs[[1]] <- data.frame(eid = eid_i, age = age0_i, state = init_state,
                           stringsAsFactors = FALSE)

    curr_ins <- ins_at_bl
    curr_ad  <- ad_at_bl
    curr_st  <- init_state

    # 失眠发病(基线后)
    if (!is.na(t_ins) && t_ins > age0_i) {
      curr_ins <- TRUE
      new_st <- ifelse(curr_ad, 4L, 2L)  # 若已有 AD → S3, 否则 → S1
      obs[[length(obs) + 1]] <-
        data.frame(eid = eid_i, age = t_ins, state = new_st,
                   stringsAsFactors = FALSE)
      curr_st <- new_st
    }

    # AD 发病(基线后)
    if (!is.na(t_ad_i) && t_ad_i > age0_i) {
      curr_ad <- TRUE
      new_st <- ifelse(curr_ins, 4L, 3L)  # 若已有失眠 → S3, 否则 → S2
      obs[[length(obs) + 1]] <-
        data.frame(eid = eid_i, age = t_ad_i, state = new_st,
                   stringsAsFactors = FALSE)
      curr_st <- new_st
    }

    # 死亡或删失(末次观测)
    if (!is.na(evt) && evt == 1) {
      obs[[length(obs) + 1]] <-
        data.frame(eid = eid_i, age = t_dth, state = 5L,
                   stringsAsFactors = FALSE)
    } else {
      # 删失: 保持在当前状态
      obs[[length(obs) + 1]] <-
        data.frame(eid = eid_i, age = t_dth, state = curr_st,
                   stringsAsFactors = FALSE)
    }

    obs_df <- do.call(rbind, obs)
    # 附带协变量(时间常数, 复制到每行)
    obs_df <- cbind(obs_df,
                    cov_i[rep(1, nrow(obs_df)), , drop = FALSE])
    rownames(obs_df) <- NULL
    rows[[i]] <- obs_df
  }

  df_long <- do.call(rbind, rows)
  rownames(df_long) <- NULL

  # 去重: 同一 eid 同一 age 的重复行保留首次
  df_long <- df_long %>%
    distinct(eid, age, .keep_all = TRUE) %>%
    arrange(eid, age)

  return(df_long)
}

df_long <- wide_to_msm_long(df)
message("[G4] 长表构造完成: ", nrow(df_long), " 行, ",
        n_distinct(df_long$eid), " 人")

# 2c. 状态转移频数表(msm 内置)
state_table <- statetable.msm(state, subject = eid, data = df_long)
message("[G4] 观测到的状态转移频数:\n",
        paste(capture.output(print(state_table)), collapse = "\n"))

## ====================================================================
## ---- 3. 连续时间多状态 Markov 模型 (msm) ----
## ====================================================================
# 状态编码: 1=S0, 2=S1, 3=S2, 4=S3, 5=死亡
# Q 矩阵: 非零 = 允许转移; 值 = 初始强度估计(对角线由 msm 自动填充)
#
# 允许的转移:
#   S0→S1, S0→S2, S0→S3, S0→Death
#   S1→S3, S1→Death
#   S2→S3, S2→Death
#   S3→Death
#   Death = 吸收态
#
# 初始值选取: 小正数(年强度), 失眠比 AD 常见故 q01 > q02
Q <- rbind(c(0,    0.01, 0.005, 0.001, 0.01),
           c(0,    0,    0,     0.01,  0.01),
           c(0,    0,    0,     0.01,  0.01),
           c(0,    0,    0,     0,     0.02),
           c(0,    0,    0,     0,     0))

# 事件数检查(与 OSF §10 锁定一致: 每个允许转移 ≥ 50 例观测, msm 方能稳定估计)
min_transitions <- 50
message("[G4] 事件数检查(阈值 ≥ ", min_transitions, "):")
for (i in 1:nrow(Q)) {
  for (j in 1:ncol(Q)) {
    if (Q[i, j] != 0 && i != j) {
      n_trans <- if (j <= ncol(state_table) && i <= nrow(state_table))
        state_table[i, j] else 0
      flag <- if (!is.na(n_trans) && n_trans >= min_transitions) "✓"
              else "⚠ 可能不足"
      message("  转移 ", i, "→", j, ": ", n_trans, " 例  ", flag)
    }
  }
}

# ---- msm 拟合 ----
# 左截断说明:
#   state ~ age 以年龄为时间尺度。每个 subject 首次观测在 age0(基线年龄)。
#   msm 自动处理左截断: 模型条件于"在 age0 时处于观测状态"。
#   不同 subject 的 age0 不同 → 自然实现左截断, 无需额外参数。
#
# covariates 中 age0 = 基线年龄(时间常数协变量), 区别于 age(时间变量)。
# death = 5 指定死亡为吸收态, msm 在估计竞争风险时正确处理。

message("[G4] 拟合 msm 模型(可能耗时数分钟至数十分钟)...")
msmfit <- msm(
  state     ~ age,
  subject   = eid,
  data      = df_long,
  qmatrix   = Q,
  covariates = ~ age0 + sex + depression + apoe_e4 +
                education + hypnotic_use,
  death     = 5,
  control   = list(maxit = 1e4),
  exacttimes = TRUE   # 我们从确切诊断/死亡时间构造, 用 exacttimes=TRUE 提高效率
)

message("[G4] msm 拟合完成。")
print(msmfit)

# 转移强度估计
qmatrix_est <- qmatrix.msm(msmfit)
message("[G4] 转移强度 Q:\n",
        paste(capture.output(print(qmatrix_est)), collapse = "\n"))

# 1 年转移概率矩阵(基准)
pmatrix_1yr <- pmatrix.msm(msmfit, t = 1)

## ====================================================================
## ---- 4. 核心对比: 1→3(失眠先发) vs 2→3(AD先发) 到达 S3 的累积概率
## ====================================================================
# 从 pmatrix 提取不同时间窗口下的转移概率:
#   P(S0→S3 at time t) = pm[1, 4]  (到达共病的总概率, 含两条路径)
#   P(S0→S1 at time t) = pm[1, 2]  (先发失眠的概率)
#   P(S0→S2 at time t) = pm[1, 3]  (先发 AD 的概率)
#   P(S1→S3 at time t) = pm[2, 4] (从失眠进展到共病的概率)
#   P(S2→S3 at time t) = pm[3, 4] (从 AD 进展到共病的概率)
#
# 路径累积概率近似:
#   经失眠先到达 S3 ≈ P(S0→S1) × P(S1→S3)
#   经 AD 先到达 S3  ≈ P(S0→S2) × P(S2→S3)
#   注意: 此乘积近似高估(因未扣 S0→S3 直达), 适合做相对比较而非绝对值引用。

compute_path_comparison <- function(fit, ref_age = 60,
                                    target_ages = seq(65, 90, 5)) {
  t_grid <- target_ages - ref_age  # 时间间隔
  t_grid <- t_grid[t_grid > 0]     # 排除 0

  results <- data.frame(
    target_age           = target_ages[target_ages > ref_age],
    t_years              = t_grid,
    p_S0_to_S1           = NA_real_,
    p_S0_to_S2           = NA_real_,
    p_S0_to_S3_total     = NA_real_,
    p_S0_to_death        = NA_real_,
    p_S1_to_S3           = NA_real_,
    p_S2_to_S3           = NA_real_,
    path_insomnia_first  = NA_real_,
    path_ad_first        = NA_real_,
    path_ratio_ins_over_ad = NA_real_
  )

  for (k in seq_along(t_grid)) {
    t <- t_grid[k]
    pm <- tryCatch(pmatrix.msm(fit, t = t),
                   error = function(e) {
                     message("[G4] pmatrix t=", t, " 失败: ", e$message)
                     return(NULL)
                   })
    if (is.null(pm)) next

    results$p_S0_to_S1[k]            <- pm[1, 2]
    results$p_S0_to_S2[k]            <- pm[1, 3]
    results$p_S0_to_S3_total[k]      <- pm[1, 4]
    results$p_S0_to_death[k]         <- pm[1, 5]
    results$p_S1_to_S3[k]            <- pm[2, 4]
    results$p_S2_to_S3[k]            <- pm[3, 4]

    # 路径近似(相对比较用)
    results$path_insomnia_first[k]   <- pm[1, 2] * pm[2, 4]
    results$path_ad_first[k]         <- pm[1, 3] * pm[3, 4]

    if (results$path_ad_first[k] > 0) {
      results$path_ratio_ins_over_ad[k] <-
        results$path_insomnia_first[k] / results$path_ad_first[k]
    }
  }

  return(results)
}

path_compare <- compute_path_comparison(msmfit, ref_age = 60,
                                        target_ages = seq(65, 90, 5))
message("[G4] 路径对比(累积概率, 参考年龄 60):\n",
        paste(capture.output(print(path_compare, digits = 4)), collapse = "\n"))

# 可选: ggplot 绘制路径对比图
plot_path_comparison <- function(pc) {
  pc_long <- data.frame(
    age = rep(pc$target_age, 2),
    prob = c(pc$path_insomnia_first, pc$path_ad_first),
    path = rep(c("Insomnia first (S0→S1→S3)",
                 "AD first (S0→S2→S3)"),
               each = nrow(pc))
  )

  p <- ggplot(pc_long, aes(x = age, y = prob, color = path, group = path)) +
    geom_line(linewidth = 1) +
    geom_point(size = 2.5) +
    scale_color_manual(
      values = c("Insomnia first (S0→S1→S3)" = "#E64B35",
                 "AD first (S0→S2→S3)" = "#4DBBD5")) +
    labs(
      title    = "Cumulative probability of reaching comorbid state (S3)",
      subtitle = "Approximate path probability: P(S0→Si) × P(Si→S3)",
      x = "Age (years)", y = "Cumulative probability",
      color = "Path"
    ) +
    theme_bw(base_size = 12) +
    theme(legend.position = "bottom")

  return(p)
}

p_path <- plot_path_comparison(path_compare)

## ====================================================================
## ---- 5. 预后: 到达 S3 后按进入路径分层的全因死亡生存 ----
## ====================================================================
# 从宽表提取到达 S3(共病)的子集, 按进入路径分层:
#   Insomnia_first = 失眠先发(path = S1thenS3)
#   AD_first       = AD 先发(path = S2thenS3)
# 排除同时发病者(S3_simul, 无明确路径)

df_s3 <- df %>%
  filter(path %in% c("S1thenS3", "S2thenS3")) %>%
  mutate(
    # 进入 S3 的年龄 = 后发疾病的年龄
    t_entry_s3 = pmax(t_insomnia, t_ad, na.rm = TRUE),
    # 从 S3 到死亡/删失的观测时间
    t_survival = t_death - t_entry_s3,
    # 进入路径
    entry_path = factor(case_when(
      path == "S1thenS3" ~ "Insomnia_first",
      path == "S2thenS3" ~ "AD_first",
      TRUE ~ NA_character_
    ))
  ) %>%
  filter(!is.na(t_entry_s3) & t_survival > 0)

message("[G4] S3 共病子集: ", nrow(df_s3), " 人",
        " (失眠先发 ", sum(df_s3$entry_path == "Insomnia_first", na.rm = TRUE),
        " / AD 先发 ", sum(df_s3$entry_path == "AD_first", na.rm = TRUE), ")")

if (nrow(df_s3) > 0 &&
    nrow(df_s3[df_s3$entry_path == "Insomnia_first", ]) > 0 &&
    nrow(df_s3[df_s3$entry_path == "AD_first", ]) > 0) {

  # Kaplan-Meier 分层生存曲线(左截断: 从 t_entry_s3 进入风险集)
  surv_fit <- survfit(Surv(t_entry_s3, t_death, event_death) ~ entry_path,
                      data = df_s3)
  message("[G4] 分层生存 KM:\n",
          paste(capture.output(print(surv_fit)), collapse = "\n"))

  # Cox 比例风险: 失眠先发 vs AD 先发 的全因死亡 HR
  # 调整协变量: age0, sex, depression, apoe_e4, education, hypnotic_use
  cox_fit <- coxph(
    Surv(t_entry_s3, t_death, event_death) ~ entry_path +
      age0 + sex + depression + apoe_e4 + education + hypnotic_use,
    data = df_s3
  )
  message("[G4] Cox HR(全因死亡, 失眠先发 vs AD 先发):\n",
          paste(capture.output(summary(cox_fit)), collapse = "\n"))

  # log-rank 检验
  logrank <- survdiff(Surv(t_entry_s3, t_death, event_death) ~ entry_path,
                      data = df_s3)
  message("[G4] Log-rank p = ", format.pval(1 - pchisq(logrank$chisq,
                                                       df = length(logrank$n) - 1),
                                             digits = 3))
} else {
  surv_fit <- NULL
  cox_fit  <- NULL
  warning("[G4] ⚠ S3 子集事件数不足, 生存分析跳过。",
          " 建议: (1) 使用全因痴呆扩样本; (2) 放宽 AD 定义; (3) 延长随访。")
}

## ====================================================================
## ---- 6. 保存 ----
## ====================================================================
saveRDS(
  list(
    msmfit       = msmfit,
    qmatrix      = qmatrix_est,
    pmatrix_1yr  = pmatrix_1yr,
    state_table  = state_table,
    path_compare = path_compare,
    survfit      = surv_fit,
    coxph        = cox_fit,
    df_long      = df_long,
    df_s3        = df_s3,
    plot_path    = p_path
  ),
  file.path(DIR_OUT, "G4_multistate.rds")
)
message("[G4] 结果已保存: ", file.path(DIR_OUT, "G4_multistate.rds"))

## ====================================================================
## ---- 7. 敏感性分析 ----
## ====================================================================
# 以下函数均为可调用代码块, 取消注释即可运行(需真实数据)。
# 每个函数自包含, 不依赖主模型结果。

# --- (a) 仅住院 ICD 失眠定义 (需 t_insomnia_icd 列) ---
# 用 ICD-10 G47.0 入院日期替代自评失眠, 重跑完整 msm 管线
sensitivity_icd_insomnia <- function(d) {
  if (!"t_insomnia_icd" %in% names(d)) {
    message("[G4][sens-a] 跳过: 缺少 t_insomnia_icd 列")
    return(NULL)
  }
  message("[G4][sens-a] 仅住院 ICD 失眠定义敏感性分析...")
  d_icd <- d %>% mutate(t_insomnia = t_insomnia_icd)
  d_icd <- clean_ukb_data(d_icd)
  d_icd <- build_paths(d_icd)
  d_long_icd <- wide_to_msm_long(d_icd)

  st_icd <- statetable.msm(state, subject = eid, data = d_long_icd)
  message("[G4][sens-a] ICD 失眠转移频数:\n",
          paste(capture.output(print(st_icd)), collapse = "\n"))

  fit_icd <- msm(state ~ age, subject = eid, data = d_long_icd,
                 qmatrix = Q,
                 covariates = ~ age0 + sex + depression + apoe_e4 +
                              education + hypnotic_use,
                 death = 5, control = list(maxit = 1e4),
                 exacttimes = TRUE)
  pc_icd <- compute_path_comparison(fit_icd)

  message("[G4][sens-a] ICD 失眠路径对比:\n",
          paste(capture.output(print(pc_icd, digits = 4)), collapse = "\n"))
  return(list(msmfit = fit_icd, path_compare = pc_icd, state_table = st_icd))
}

# --- (b) 全因痴呆 vs AD (需 t_dementia 列) ---
# 用全因痴呆(F00-F03)替代 AD(F00/G30), 扩大事件数
sensitivity_allcause_dementia <- function(d) {
  if (!"t_dementia" %in% names(d)) {
    message("[G4][sens-b] 跳过: 缺少 t_dementia 列")
    return(NULL)
  }
  message("[G4][sens-b] 全因痴呆(替代 AD) 敏感性分析...")
  d_dem <- d %>% mutate(t_ad = t_dementia)
  d_dem <- clean_ukb_data(d_dem)
  d_dem <- build_paths(d_dem)
  d_long_dem <- wide_to_msm_long(d_dem)

  st_dem <- statetable.msm(state, subject = eid, data = d_long_dem)
  message("[G4][sens-b] 全因痴呆转移频数:\n",
          paste(capture.output(print(st_dem)), collapse = "\n"))

  fit_dem <- msm(state ~ age, subject = eid, data = d_long_dem,
                 qmatrix = Q,
                 covariates = ~ age0 + sex + depression + apoe_e4 +
                              education + hypnotic_use,
                 death = 5, control = list(maxit = 1e4),
                 exacttimes = TRUE)
  pc_dem <- compute_path_comparison(fit_dem)

  message("[G4][sens-b] 全因痴呆路径对比:\n",
          paste(capture.output(print(pc_dem, digits = 4)), collapse = "\n"))
  return(list(msmfit = fit_dem, path_compare = pc_dem, state_table = st_dem))
}

# --- (c) 协变量剔除的似然比检验 (LRT) ---
# 逐一剔除 APOE ε4 / 抑郁 / 安眠药, 比较模型拟合
# 检验每个协变量对转移强度的贡献是否显著
sensitivity_lrt_covariates <- function(fit_full, d_long,
                                       covars_to_drop = c("apoe_e4",
                                                          "depression",
                                                          "hypnotic_use")) {
  # 提取 log-likelihood 的辅助函数
  get_loglik <- function(fit) {
    ll <- tryCatch(as.numeric(logLik(fit)), error = function(e) NULL)
    if (is.null(ll) && !is.null(fit$minus2loglik)) {
      ll <- -fit$minus2loglik / 2
    }
    return(ll)
  }

  full_covars <- c("age0", "sex", "depression", "apoe_e4",
                   "education", "hypnotic_use")
  ll_full <- get_loglik(fit_full)
  n_coef_full <- length(coef(fit_full))

  results <- list()
  for (cv in covars_to_drop) {
    message("[G4][sens-c] LRT: 剔除 ", cv)
    reduced_covars <- setdiff(full_covars, cv)
    reduced_formula <- as.formula(paste("~", paste(reduced_covars,
                                                    collapse = " + ")))
    fit_reduced <- tryCatch(
      msm(state ~ age, subject = eid, data = d_long,
          qmatrix = Q, covariates = reduced_formula,
          death = 5, control = list(maxit = 1e4),
          exacttimes = TRUE),
      error = function(e) {
        message("  拟合失败: ", e$message)
        return(NULL)
      }
    )
    if (is.null(fit_reduced)) next

    ll_reduced <- get_loglik(fit_reduced)
    n_coef_reduced <- length(coef(fit_reduced))

    lrt_stat <- 2 * (ll_full - ll_reduced)
    df_lrt   <- n_coef_full - n_coef_reduced
    p_lrt    <- pchisq(lrt_stat, df = df_lrt, lower.tail = FALSE)

    results[[cv]] <- data.frame(
      dropped_covariate = cv,
      lrt_statistic     = round(lrt_stat, 3),
      df                = df_lrt,
      p_value           = signif(p_lrt, 3)
    )
    message("  LRT χ² = ", round(lrt_stat, 3),
            ", df = ", df_lrt,
            ", P = ", format.pval(p_lrt, digits = 3))
  }

  return(do.call(rbind, results))
}

# --- (d) 竞争风险敏感性(死亡作为竞争事件, 非仅吸收态) ---
# 注: msm 中 death=5 已将死亡作为吸收态处理, 竞争风险在内。
#     此处给出 Fine-Gray 模型作为补充对照(需 cmprsk 包)。
# sensitivity_finegray <- function(d_s3) {
#   library(cmprsk)
#   d_fg <- d_s3 %>% mutate(
#     status = case_when(event_death == 1 ~ 1,    # 死亡
#                        TRUE ~ 0)                # 删失
#   )
#   fg_fit <- cuminc(ftime = t_survival, fstatus = status,
#                    group = entry_path, cencode = 0)
#   print(fg_fit)
#   return(fg_fit)
# }

# --- 运行敏感性分析(按需取消注释) ---
# sens_a <- sensitivity_icd_insomnia(df)
# sens_b <- sensitivity_allcause_dementia(df)
# sens_c <- sensitivity_lrt_covariates(msmfit, df_long)
#
# saveRDS(list(sens_a = sens_a, sens_b = sens_b, sens_c = sens_c),
#        file.path(DIR_OUT, "G4_sensitivity.rds"))

message("[G4] =====================================")
message("[G4] 多状态发病顺序模型完成。")
message("[G4] 主结果: results/G4_multistate.rds")
message("[G4] 敏感性: 取消注释第 7 节末尾代码块后运行(sens_a/b/c)。")
message("[G4] =====================================")
