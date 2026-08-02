## 备选安装脚本: GitHub zip 下载 + 本地安装 (仅在 v2/GitHub clone 失败时启用)
## 用法: Rscript install_overlap_pkgs_v3.R
## 日志: install_log_v3.txt
options(repos = c(CRAN = "https://cloud.r-project.org"),
        timeout = 600,
        download.file.method = "libcurl")

logf <- "install_log_v3.txt"
log <- function(...) {
  line <- paste(..., sep = " ")
  cat(line, "\n")
  cat(format(Sys.time(), "%Y-%m-%d %H:%M:%S"), line, "\n", file = logf, append = TRUE)
}

## ---- MRlap: 从 GitHub 下载 zip 再本地安装 (避开 git2r 整仓克隆) ----
log("=== MRlap (github zip -> install_local) ===")
mr_ok <- FALSE
tryCatch({
  tmp <- tempfile(fileext = ".zip")
  download.file("https://github.com/n-mounier/MRlap/archive/refs/heads/master.zip",
                destfile = tmp, mode = "wb", quiet = FALSE)
  if (file.exists(tmp) && file.info(tmp)$size > 1000) {
    log("MRlap zip downloaded: ", file.info(tmp)$size, " bytes")
    remotes::install_local(tmp, upgrade = "never", dependencies = TRUE, force = TRUE)
    mr_ok <- requireNamespace("MRlap", quietly = TRUE)
    log(if (mr_ok) "MRlap OK" else "MRlap ERR: installed but requireNamespace FALSE")
  } else {
    log("MRlap ERR: zip download too small / failed")
  }
}, error = function(e) log("MRlap ERR: ", conditionMessage(e)))
if (file.exists(tmp)) try(file.remove(tmp), silent = TRUE)

## ---- cause: r-universe Windows 二进制 (无需 Rtools) ----
log("=== cause (r-universe binary) ===")
cause_ok <- FALSE
tryCatch({
  install.packages("cause", repos = "https://mrcieu.r-universe.dev", dependencies = TRUE)
  cause_ok <- requireNamespace("cause", quietly = TRUE)
  log(if (cause_ok) "cause OK" else "cause ERR: installed but requireNamespace FALSE")
}, error = function(e) log("cause ERR: ", conditionMessage(e)))

## ---- 汇总 ----
log("=== SUMMARY ===")
log("MRlap :", mr_ok, " | cause :", cause_ok)
