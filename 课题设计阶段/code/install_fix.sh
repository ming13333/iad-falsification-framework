cd "C:/D/workbuddy/科研/共病分析/课题设计阶段/code"
echo "$(date) === start fix: CAUSE reinstall + MRlap from ASCII path ===" >> install_log_fix.txt
# 1) copy MRlap_src (chinese parent path) -> pure ASCII path
rm -rf /c/MRlap_pkg
cp -r MRlap_src /c/MRlap_pkg
echo "MRlap_pkg copied: $(ls /c/MRlap_pkg/DESCRIPTION 2>&1)" >> install_log_fix.txt
# 2) reinstall both via R
Rscript -e "
options(timeout=600)
if(!requireNamespace('remotes', quietly=TRUE)) install.packages('remotes', repos='https://cloud.r-project.org')
# --- CAUSE: remove broken residual then reinstall from r-universe binary ---
p <- 'C:/Users/lm962/AppData/Local/R/win-library/4.5/CAUSE'
if(dir.exists(p)) { unlink(p, recursive=TRUE); cat('removed broken CAUSE dir\n') }
install.packages('CAUSE', repos=c('https://jean997.r-universe.dev','https://cloud.r-project.org'), dependencies=TRUE)
cat('CAUSE loaded:', requireNamespace('CAUSE', quietly=TRUE), '\n')
# --- MRlap: install from ASCII path ---
remotes::install_local('C:/MRlap_pkg', dependencies=TRUE)
cat('MRlap loaded:', requireNamespace('MRlap', quietly=TRUE), '\n')
" >> install_log_fix.txt 2>&1
echo "$(date) === done ===" >> install_log_fix.txt
