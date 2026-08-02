## 安装 MRlap / CAUSE 重叠校正依赖 (v2: libcurl + 窄依赖 + tryCatch + 磁盘日志)
## 用法: Rscript install_overlap_pkgs_v2.R
options(repos = c(CRAN = "https://cloud.r-project.org"), timeout = 600)
options(download.file.method = "libcurl")
flush.console()

cat(Sys.time(), "=== start ===\n"); flush.console()

cat(Sys.time(), "=== MRlap (n-mounier/MRlap) ===\n"); flush.console()
tryCatch({
  if (!requireNamespace("remotes", quietly = TRUE)) install.packages("remotes")
  remotes::install_github("n-mounier/MRlap",
                          dependencies = c("Depends", "Imports"),
                          upgrade = "never")
  cat(Sys.time(), "MRlap OK\n")
}, error = function(e) cat(Sys.time(), "MRlap ERR: ", conditionMessage(e), "\n"))
flush.console()

cat(Sys.time(), "=== cause (mrcieu r-universe binary) ===\n"); flush.console()
tryCatch({
  install.packages("cause", repos = "https://mrcieu.r-universe.dev", dependencies = TRUE)
  cat(Sys.time(), "cause OK\n")
}, error = function(e) cat(Sys.time(), "cause ERR: ", conditionMessage(e), "\n"))
flush.console()

cat(Sys.time(), "=== verify ===\n")
cat("MRlap:", requireNamespace("MRlap", quietly = TRUE),
    " cause:", requireNamespace("cause", quietly = TRUE), "\n")
if (requireNamespace("MRlap", quietly = TRUE)) cat("MRlap version:", as.character(packageVersion("MRlap")), "\n")
if (requireNamespace("cause", quietly = TRUE)) cat("cause version:", as.character(packageVersion("cause")), "\n")
cat(Sys.time(), "=== ALL DONE ===\n"); flush.console()
