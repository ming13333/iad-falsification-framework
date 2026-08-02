## 安装 MRlap / CAUSE 重叠校正依赖
## 用法: Rscript install_overlap_pkgs.R
options(repos = c(CRAN = "https://cloud.r-project.org"), timeout = 600)
options(warn = 1)

cat(Sys.time(), "=== ensure remotes ===\n")
if (!requireNamespace("remotes", quietly = TRUE)) {
  install.packages("remotes")
}

cat(Sys.time(), "=== installing MRlap (n-mounier/MRlap) ===\n")
remotes::install_github("n-mounier/MRlap", dependencies = TRUE, upgrade = "never")
cat(Sys.time(), "MRlap install attempt done.\n")

cat(Sys.time(), "=== installing cause (mrcieu r-universe) ===\n")
install.packages("cause", repos = "https://mrcieu.r-universe.dev", dependencies = TRUE)
cat(Sys.time(), "cause install attempt done.\n")

cat(Sys.time(), "=== verify ===\n")
cat("MRlap :", requireNamespace("MRlap", quietly = TRUE), "\n")
cat("cause :", requireNamespace("cause", quietly = TRUE), "\n")
if (requireNamespace("MRlap", quietly = TRUE)) cat("MRlap version :", as.character(packageVersion("MRlap")), "\n")
if (requireNamespace("cause", quietly = TRUE)) cat("cause version :", as.character(packageVersion("cause")), "\n")
cat(Sys.time(), "=== ALL DONE ===\n")
