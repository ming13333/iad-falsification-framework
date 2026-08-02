#!/bin/bash
set -u
LOG="install_log_mrlap.txt"
URL="https://github.com/n-mounier/MRlap/archive/refs/heads/master.zip"
ZIP="MRlap_master.zip"
cd "C:/D/workbuddy/科研/共病分析/课题设计阶段/code"
echo "$(date) === v5 start (full re-download + verify + install_local) ===" >> "$LOG"
for i in 1 2 3; do
  echo "$(date) attempt $i: full download (max 1800s)" >> "$LOG"
  curl -L --max-time 1800 -o "$ZIP" "$URL" -w "HTTP=%{http_code} size=%{size_download} time=%{time_total}s\n" >> "$LOG" 2>&1
  if unzip -t "$ZIP" >/dev/null 2>&1; then
    echo "$(date) ZIP OK" >> "$LOG"
    break
  else
    echo "$(date) ZIP CORRUPT, will retry" >> "$LOG"
  fi
done
if unzip -t "$ZIP" >/dev/null 2>&1; then
  echo "$(date) install_local MRlap (deps from CRAN)" >> "$LOG"
  Rscript -e "options(timeout=600); if(!requireNamespace('remotes',quietly=TRUE)) install.packages('remotes',repos='https://cloud.r-project.org'); remotes::install_local('MRlap_master.zip', dependencies=TRUE); cat('requireNamespace MRlap:', requireNamespace('MRlap', quietly=TRUE), '\n')" >> "$LOG" 2>&1
else
  echo "$(date) ZIP still corrupt after 3 retries, MRlap FAILED" >> "$LOG"
fi
echo "$(date) === v5 end ===" >> "$LOG"
