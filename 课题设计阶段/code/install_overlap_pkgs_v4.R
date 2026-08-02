## v4 综合安装: MRlap(github zip+install_local) + cause(CRAN 依赖 + r-universe 二进制)
## 日志: install_log_v4.txt
options(repos = c(CRAN = "https://cloud.r-project.org"),
        timeout = 600,
        download.file.method = "libcurl")

logf <- "install_log_v4.txt"
log <- function(...) {
  line <- paste(..., sep = " ")
  cat(line, "\n")
  cat(format(Sys.time(), "%Y-%m-%d %H:%M:%S"), line, "\n", file = logf, append = TRUE)
}
log("=== start v4 ===")

## ---- MRlap: github codeload zip + 本地安装 (绕开 api.github.com tarball 失败) ----
log("=== MRlap (github zip -> install_local) ===")
mr_ok <- FALSE
tryCatch({
  tmp <- tempfile(fileext = ".zip")
  download.file("https://github.com/n-mounier/MRlap/archive/refs/heads/master.zip",
                destfile = tmp, mode = "wb", quiet = FALSE)
  if (file.exists(tmp) && file.info(tmp)$size > 50000) {
    log("MRlap zip downloaded: ", round(file.info(tmp)$size / 1e6, 1), " MB")
    remotes::install_local(tmp, upgrade = "never", dependencies = TRUE, force = TRUE)
    mr_ok <- requireNamespace("MRlap", quietly = TRUE)
    log(if (mr_ok) "MRlap OK" else "MRlap ERR: installed but requireNamespace FALSE")
  } else {
    log("MRlap ERR: zip too small / not downloaded")
  }
  if (file.exists(tmp)) try(file.remove(tmp), silent = TRUE)
}, error = function(e) log("MRlap ERR: ", conditionMessage(e)))

## ---- cause: 先装 CRAN 依赖, 再装 r-universe 二进制 ----
log("=== cause deps (CRAN) ===")
tryCatch({
  install.packages(c("ashr", "RcppParallel", "numDeriv", "loo", "intervals", "testthat"),
                   dependencies = TRUE)
  log("cause deps installed")
}, error = function(e) log("cause deps ERR: ", conditionMessage(e)))

log("=== cause (r-universe binary) ===")
cause_ok <- FALSE
tryCatch({
  install.packages("cause", repos = "https://mrcieu.r-universe.dev", dependencies = TRUE)
  cause_ok <- requireNamespace("cause", quietly = TRUE)
  log(if (cause_ok) "cause OK" else "cause ERR: installed but requireNamespace FALSE")
}, error = function(e) log("cause ERR: ", conditionMessage(e)))

## ---- 最终核验 ----
log("=== SUMMARY ===")
log("MRlap:", mr_ok, "| cause:", cause_ok)
tryCatch({
  if (mr_ok) library(MRlap)
  if (cause_ok) library(cause)
  log("final load check: MRlap", requireNamespace("MRlap", quietly=TRUE),
      "cause", requireNamespace("cause", quietly=TRUE))
}, error = function(e) log("final load ERR:", conditionMessage(e)))
