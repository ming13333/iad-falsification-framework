cd "C:/D/workbuddy/科研/共病分析/课题设计阶段/code"
Rscript -e "
options(repos='https://mirrors.tuna.tsinghua.edu.cn/CRAN/', timeout=600)
if(!requireNamespace('remotes', quietly=TRUE)) install.packages('remotes')
cran <- c('e1071','gdata','lavaan','R.utils','simsalapar','R.methodsS3','colorspace','sfsmisc','R.oo','gtools','Rcpp')
install.packages(cran)
remotes::install_github('GenomicSEM/GenomicSEM', dependencies=TRUE, repos='https://mirrors.tuna.tsinghua.edu.cn/CRAN/')
cat('GenomicSEM:', requireNamespace('GenomicSEM', quietly=TRUE), '\n')
remotes::install_local('C:/MRlap_pkg', dependencies=TRUE, repos='https://mirrors.tuna.tsinghua.edu.cn/CRAN/')
cat('MRlap:', requireNamespace('MRlap', quietly=TRUE), '\n')
" >> install_log_mrlap2.txt 2>&1
echo "DONE $(date)" >> install_log_mrlap2.txt
