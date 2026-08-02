cd "C:/D/workbuddy/科研/共病分析/课题设计阶段/code"
OUT="C:/Users/lm962/rtools45_installer.exe"
# GitHub releases page (case-insensitive)
URL=$(curl -sL https://github.com/r-windows/rtools-installer/releases | grep -ioE 'https://github.com/r-windows/rtools-installer/releases/download/[^"<> ]*rtools45[^"<> ]*\.exe' | head -1)
echo "$(date) GitHub URL: $URL" > install_log_rtools.txt
# CRAN fallback (case-insensitive)
if [ -z "$URL" ]; then
  FNAME=$(curl -sL https://cran.r-project.org/bin/windows/Rtools/rtools45.html | grep -ioE 'rtools45[^"<> ]*\.exe' | head -1)
  URL="https://cran.r-project.org/bin/windows/Rtools/rtools45/$FNAME"
  echo "$(date) CRAN URL: $URL" >> install_log_rtools.txt
fi
echo "$(date) FINAL: $URL" >> install_log_rtools.txt
curl -L --max-time 900 -o "$OUT" "$URL"
echo "$(date) exit=$? size:" >> install_log_rtools.txt
ls -la "$OUT" >> install_log_rtools.txt 2>&1
echo "$(date) === done ===" >> install_log_rtools.txt
