## CAUSE 重装:删除损坏残留,用 Rtools45 从 GitHub 源码编译安装
lib <- 'C:/Users/lm962/AppData/Local/R/win-library/4.5'

## 1) 把 Rtools45 工具链显式加入 PATH(确保 R CMD INSTALL 能编译 C++)
rtools_bins <- c('c:/rtools45/usr/bin', 'c:/rtools45/x86_64-w64-mingw32.static.posix/bin')
Sys.setenv(PATH = paste(c(rtools_bins, Sys.getenv('PATH')), collapse = ';'))

## 2) CRAN 走清华镜像(用户网络已验证稳)
options(repos = c(CRAN = 'https://mirrors.tuna.tsinghua.edu.cn/CRAN/'))

## 3) 确保 remotes 可用
if (!requireNamespace('remotes', quietly = TRUE)) {
  install.packages('remotes', lib = lib)
}

## 4) 删除损坏的 CAUSE 残留
cat('=== removing broken CAUSE ===\n')
try(remove.packages('CAUSE', lib = lib), silent = TRUE)

## 5) 从 GitHub 源码编译安装 CAUSE(含 CRAN 依赖)
cat('=== installing CAUSE from GitHub source (compile) ===\n')
remotes::install_github(
  'jean997/cause',
  lib   = lib,
  dependencies = TRUE,
  Ncpus = 4,
  force = TRUE,
  upgrade = 'never'
)

## 6) 权威验证
cat('=== CAUSE requireNamespace:', requireNamespace('CAUSE', quietly = TRUE), '===\n')
if (requireNamespace('CAUSE', quietly = TRUE)) {
  cat('CAUSE version:', as.character(packageVersion('CAUSE')), '\n')
}
