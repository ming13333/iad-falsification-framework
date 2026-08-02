cd "C:/D/workbuddy/科研/共病分析/课题设计阶段/code"
# primary: GitHub r-windows/rtools-installer releases (case-insensitive match)
URL=$(curl -sL https://api.github.com/repos/r-windows/rtools-installer/releases | grep -ioE 'https://github.com/r-windows/rtools-installer/releases/download/[^"]*rtools45[^"]*\.exe' | head -1)
echo "$(date) GitHub URL: $URL" > install_log_rtools.txt
# fallback: CRAN rtools45 page
if [ -z "$URL" ]; then
  FNAME=$(curl -sL https://cran.r-project.org/bin/windows/Rtools/rtools45.html | grep -ioE 'rtools45[^"]*\.exe' | head -1)
  URL="https://cran.r-project.org/bin/windows/Rtools/rtools45/$FNAME"
  echo "$(date) CRAN fallback URL: $URL" >> install_log_rtools.txt
fi
echo "$(date) FINAL URL: $URL" >> install_log_rtools.txt
curl -L --max-time 900 -o C:/rtools45_installer.exe "$URL"
echo "$(date) download exit=$? size:" >> install_log_rtools.txt
ls -la C:/rtools45_installer.exe >> install_log_rtools.txt 2>&1
echo "$(date) === done ===" >> install_log_rtools.txt
