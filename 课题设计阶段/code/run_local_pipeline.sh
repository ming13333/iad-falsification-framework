#!/usr/bin/env bash
# =====================================================================
# 失眠 → AD 共病 MR 研究 · 本地跑数流水线（run_local_pipeline.sh）
# ---------------------------------------------------------------------
# 沙箱（WorkBuddy）无法运行真实 MR：无 R 运行时 / 无 OpenGWAS 网络 / 无 UKB
# 个体级权限。本脚本专供【你本地联网 R 环境】按顺序执行，把
#   00b → 01 → 02 → 03
# 串起来，并在任何一步失败时停下来，避免"半成品"污染结果。
#
# 运行方式（需在 Git Bash / WSL / macOS 终端，Windows 用 Git Bash）：
#   cd "C:/D/workbuddy/科研/共病分析/课题设计阶段"
#   bash code/run_local_pipeline.sh
#
# 前置（P0 必需）：设置样本重叠校正所需的本地 LDSC 权重（MRlap 必需；CAUSE 走 IEU EUR LD 无需本地面板）
#   export MRlap_LDREF=/绝对路径/eur_w_ld_chr        # LDSC LD 分数目录（从 utexas.box.com 下载）
#   export MRlap_HM3=/绝对路径/w_hm3.noMHC.snplist  # hm3 snplist 文件（同上来源）
#   （MRlap 严格需要这两个权重；若未设置，脚本会停下并明确提示）
#   若你确认本环境不存在 BenElsworth(ukb-b-3957)↔Bellenguez 的 UKB 重叠、坚持跳过，
#   可设 SKIP_OVERLAP=1 后重跑（不推荐，违背 P0）。
# =====================================================================

set -euo pipefail

# ---- 自动定位项目根（脚本置于 code/ 下）----
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
cd "$PROJECT_DIR"

# ---- Rscript 路径（默认取 PATH 中的 Rscript；非标准安装请改下面）----
RSCRIPT="${RSCRIPT:-Rscript}"

echo "项目根目录: $PROJECT_DIR"
echo "Rscript    : $(command -v "$RSCRIPT" || echo '[未找到——请安装 R 或将 RSCRIPT 指向 Rscript.exe]')"

# ---- 产物目录 ----
mkdir -p results data

# ---- P0 样本重叠校正 LD 面板检查（MRlap 必需；CAUSE 用 IEU EUR LD，无需本地面板）----
if [[ -z "${MRlap_LDREF:-}" || -z "${MRlap_HM3:-}" ]]; then
  echo ""
  echo "[WARN] MRlap_LDREF / MRlap_HM3 未设置 → 01 的 MRlap 样本重叠校正将被跳过。" >&2
  echo "[WARN] P0 要求：BenElsworth(ukb-b-3957)↔Bellenguez 均含 UKB，重叠须校正。" >&2
  echo "[WARN] 请先下载 LDSC 权重（eur_w_ld_chr 目录 + w_hm3.noMHC.snplist，来源 utexas.box.com）并 export：" >&2
  if [[ "${SKIP_OVERLAP:-}" != "1" ]]; then
    echo "[HALT] 缺 LDSC 权重且未显式 SKIP_OVERLAP=1，停止。设置环境变量后重试：" >&2
    echo "        export MRlap_LDREF=/path/to/eur_w_ld_chr" >&2
    echo "        export MRlap_HM3=/path/to/w_hm3.noMHC.snplist" >&2
    exit 2
  fi
  echo "[WARN] SKIP_OVERLAP=1 已设，强制跳过 MRlap 重叠校正（违背 P0，结果谨慎解读）。" >&2
fi

# ---- R 依赖检查 ----
echo ""
echo "==> 检查 R 依赖 ..."
"$RSCRIPT" -e 'pkgs <- c("TwoSampleMR","ieugwasr","coloc","msm","mstate","MRPRESSO","MRlap","CAUSE"); ins <- rownames(installed.packages()); miss <- setdiff(pkgs, ins); if(length(miss)){ cat("缺失包：", paste(miss, collapse=", "), "\n请在 R 中执行 install.packages() 或 BiocManager::install() 补齐后重试。\n", sep=""); quit(status=1) } else { cat("依赖齐全：", paste(pkgs, collapse=", "), "\n") }'

# ---- 逐步执行（失败即停）----
run_step () {
  local name="$1"; local script="$2"
  echo ""
  echo "=================================================="
  echo "==> [$name] $script"
  echo "=================================================="
  "$RSCRIPT" "$script"
}

# 说明：02 需要 data/ukbppp_protein_gwas_index.csv + UKB-PPP 蛋白 GWAS；
#       03 需要 UKB 个体级长表（字段 2245/2255/G47.0/F00/G30/死亡/APOE）。
#       缺失时对应步骤会失败退出，属预期——补齐数据后从失败步重跑即可。
run_step "00b 核验 GWAS ID / 样本重叠 / panel 覆盖" "code/00b_verify_gwas.R"
run_step "01 G1 双向 MR + 共定位 + MRlap/CAUSE"      "code/01_bidirectional_mr_coloc.R"
run_step "02 G2 血浆蛋白两步中介 + coloc 复核"        "code/02_protein_mediation.R"
run_step "03 G4 多状态时序（需 UKB 个体级权限）"     "code/03_multistate_onset.R"

echo ""
echo "==> 流水线完成。预期产物："
echo "   code/gwas_ids_resolved.json            (00b 写出，供 01 读取)"
echo "   results/G1_bidirectional.rds          (01, 含 fwd/rev/coloc/MRlap/CAUSE)"
echo "   results/G1_coloc_forward.csv          (01)"
echo "   results/G1_coloc_reverse.csv          (01)"
echo "   results/G2_protein_mediation.rds      (02)"
echo "   results/G2_mediation_table.csv        (02)"
echo "   results/G2_mediation_reverse.csv      (02, 反向证伪)"
echo "   results/G2_protein_coloc.csv          (02)"
echo "   results/G2_direction_comparison.csv   (02)"
echo "   results/G4_multistate.rds             (03)"
echo ""
echo "下一步：复制 OSF预注册计划.md 到 OSF 锁定 → 启动 G3 跨祖先复制"
echo "        （BBJ / 东亚 UKB / CHARLS）→ 真数字产出后回专家团做 STORM 审计升 A。"
