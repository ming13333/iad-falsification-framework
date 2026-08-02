# run_g1_ascii_launcher.ps1
# ============================================================================
# 修复 R C-locale 对中文路径 file.exists()/fread() 误判 FALSE 的问题。
#
# 根因(已用 G1_run.log 验证):
#   本机 R locale = C/ASCII 时, 含中文的 UTF-8 路径(如 ".../科研/共病分析/...")
#   在 file.exists()/fread() 中被误判为不存在 -> 两份 clean GWAS "未找到" ->
#   harmonize 跳过 -> 对空对象跑 MR -> "object 'id.exposure' not found" 退出。
#
# 做法(非侵入, 不修改原件):
#   1) 将 4 个 clean GWAS 复制到 ASCII 临时目录 C:\Temp\insomnia_ad_gwas\data\raw\<id>\
#   2) 将 00_config.R / 01_bidirectional_mr_coloc.R 复制到 ...\code\ (运行副本)
#   3) 在运行副本中, 把两处中文基路径替换为 ASCII 临时路径:
#        - 01 脚本 DIR_RAW_LOCAL  <- ".../科研/共病分析/data/raw"
#        - 00_config.R DIR_ROOT   <- ".../科研/共病分析/课题设计阶段"
#      (DIR_ROOT 派生 DIR_DATA/DIR_OUT/DIR_FIG/RESOLVED, 一并转为 ASCII, 输出不再写中文路径)
#   4) 后台启动 Rscript 跑 G1, 日志写入 C:\Temp\insomnia_ad_gwas\G1_run.log
#
# 用法:  powershell -ExecutionPolicy Bypass -File run_g1_ascii_launcher.ps1
# ============================================================================

$ErrorActionPreference = "Stop"

# ---- ASCII 临时根(无任何中文) ----
$TMP = "C:\Temp\insomnia_ad_gwas"

# ---- 原始中文项目根 ----
$srcRoot = "C:\D\workbuddy\科研\共病分析"
$srcCode = Join-Path $srcRoot "课题设计阶段\code"
$srcRaw  = Join-Path $srcRoot "data\raw"

# ---- 清理并重建临时结构 ----
if (Test-Path $TMP) { Remove-Item $TMP -Recurse -Force }
$tmpCode = Join-Path $TMP "code"
$tmpRaw  = Join-Path $TMP "data\raw"
$tmpOut  = Join-Path $TMP "results"
$tmpFig  = Join-Path $TMP "figures"
foreach ($d in @($tmpCode, $tmpRaw, $tmpOut, $tmpFig)) {
    New-Item -ItemType Directory -Force -Path $d | Out-Null
}

# ---- 1) 复制 clean GWAS(保持子目录, 仅取 4 个清洗交付件) ----
$ids = @("ukb-b-3957", "ieu-b-2", "ebi-a-GCST90027158")
foreach ($id in $ids) {
    $sd = Join-Path $srcRaw $id
    $dd = Join-Path $tmpRaw $id
    New-Item -ItemType Directory -Force -Path $dd | Out-Null
    Copy-Item (Join-Path $sd "*.clean.tsv.gz") $dd -Force
    Copy-Item (Join-Path $sd "*.dedup.tsv.gz") $dd -Force
}
Write-Host ("[launcher] clean GWAS 已复制到 " + $tmpRaw)

# ---- 2) 复制原始脚本到临时 code(运行副本, 不碰原件) ----
Copy-Item (Join-Path $srcCode "00_config.R")               $tmpCode -Force
Copy-Item (Join-Path $srcCode "01_bidirectional_mr_coloc.R") $tmpCode -Force

# ---- 3) 重定向中文基路径为 ASCII 临时路径(字面替换, 非正则) ----
$cfgPath  = Join-Path $tmpCode "00_config.R"
$cfg      = Get-Content $cfgPath -Raw -Encoding UTF8
$cfg      = $cfg.Replace("C:/D/workbuddy/科研/共病分析/课题设计阶段", "C:/Temp/insomnia_ad_gwas")
Set-Content $cfgPath $cfg -Encoding UTF8

$mainPath = Join-Path $tmpCode "01_bidirectional_mr_coloc.R"
$main     = Get-Content $mainPath -Raw -Encoding UTF8
$main     = $main.Replace("C:/D/workbuddy/科研/共病分析/data/raw", "C:/Temp/insomnia_ad_gwas/data/raw")
Set-Content $mainPath $main -Encoding UTF8
Write-Host "[launcher] 运行副本已生成并重定向路径到 ASCII 临时目录"

# ---- 4) 定位 Rscript 并后台启动 G1 ----
$rs = Get-Command Rscript -ErrorAction SilentlyContinue
if (-not $rs) {
    # 兜底: 常见安装位置
    $cands = @(
        "C:\Program Files\R\R-4.5.2\bin\Rscript.exe",
        "C:\Program Files\R\R-4.5.3\bin\Rscript.exe",
        "C:\Program Files\R\R-4.5.2\bin\x64\Rscript.exe"
    )
    foreach ($c in $cands) { if (Test-Path $c) { $rs = @{ Source = $c }; break } }
}
if (-not $rs) { throw "找不到 Rscript.exe, 请将其加入 PATH 或在此脚本中硬编码路径" }

$log = Join-Path $TMP "G1_run.log"
$err = Join-Path $TMP "G1_run.err"

$p = Start-Process -FilePath $rs.Source `
        -ArgumentList "01_bidirectional_mr_coloc.R" `
        -WorkingDirectory $tmpCode `
        -RedirectStandardOutput $log `
        -RedirectStandardError  $err `
        -NoNewWindow -PassThru

Write-Host ("[launcher] G1 已在后台启动 PID=" + $p.Id)
Write-Host ("[launcher] 标准输出: " + $log)
Write-Host ("[launcher] 标准错误: " + $err)
Write-Host "[launcher] 轮询: 用 Read 工具查看上述日志; 或 PowerShell: Get-Content <log> -Tail 40 -Wait"
