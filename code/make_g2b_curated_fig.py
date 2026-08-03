# =====================================================================
# make_g2b_curated_fig.py -- G2b 靶向蛋白教育->蛋白->AD 两步 MR 中介可视化
# ---------------------------------------------------------------------
# 读 C:/Temp/iad_g1/results/G2b_curated_fdr.csv
#   (02e_g2b_curated.R 产物 + g2b_fdr.py 加 q_ind)
#   protein, target, iv_count, b1,se1,p1, b2,se2,p2, indirect,se_ind,p_ind,
#   boot_mean, boot_ci_lower, boot_ci_upper, boot_p, q_ind
# 产出 (C:/Temp/iad_g1/results/):
#   G2b_curated_volcano.png  -- indirect effect vs -log10(q), q<0.05 标红
#   G2b_curated_forest_top15.png -- |indirect| 最大 15 个蛋白森林图
#   G2b_curated_summary.txt  -- 文本汇总 (供 §3.4.2 / Fig3C 使用)
# 运行: python make_g2b_curated_fig.py
# =====================================================================
import os, sys
import pandas as pd
import numpy as np

try:
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    HAVE_MPL = True
except Exception as e:
    HAVE_MPL = False
    sys.stderr.write(f"[warn] matplotlib unavailable: {e}\n")

IN  = "C:/Temp/iad_g1/results/G2b_curated_fdr.csv"
OUT = "C:/Temp/iad_g1/results"
os.makedirs(OUT, exist_ok=True)

df = pd.read_csv(IN)
numcols = ["indirect","se_ind","p_ind","q_ind","boot_ci_lower","boot_ci_upper",
           "b1","b2","n1","n2","iv_count"]
for c in numcols:
    if c in df: df[c] = pd.to_numeric(df[c], errors="coerce")

n_total    = len(df)
df_eval    = df.dropna(subset=["indirect","p_ind"]).copy()
n_excl     = n_total - len(df_eval)
n_eval     = len(df_eval)
df_eval["logq"] = -np.log10(df_eval["q_ind"].clip(lower=1e-300))
df_eval["sig"]  = df_eval["q_ind"] < 0.05
df_eval["target"] = df_eval["target"].astype(str).str.replace(",", " ").str.slice(0, 30)

excluded = df[df["p_ind"].isna()]["protein"].tolist()

lines = []
lines.append(f"G2b curated targeted mediation summary")
lines.append(f"  total targeted proteins = {n_total}")
lines.append(f"  evaluated (Step1+Step2 both >=2 IVs) = {n_eval}")
lines.append(f"  excluded (insufficient protein->AD instruments) = {n_excl}")
lines.append(f"    -> {', '.join(excluded)}")
lines.append(f"  FDR(q)<0.05 significant = {int(df_eval['sig'].sum())}")
if df_eval["sig"].sum() == 0:
    lines.append("  -> NO protein mediates education->AD at FDR<0.05 (null)")
lines.append(f"  most significant p_ind = {df_eval['p_ind'].min():.4g} "
             f"({df_eval.loc[df_eval['p_ind'].idxmin(),'protein']} "
             f"{df_eval.loc[df_eval['p_ind'].idxmin(),'target']})")
lines.append(f"  smallest boot_p = {df_eval['boot_p'].min():.4g}")
lines.append("Top 15 by |indirect|:")
top = df_eval.reindex(df_eval["indirect"].abs().sort_values(ascending=False).index).head(15)
for _, r in top.iterrows():
    lines.append(f"  {r['protein']} {r['target']}: indirect={r['indirect']:.4g} "
                 f"p={r['p_ind']:.3g} q={r['q_ind']:.3g} "
                 f"bootCI=[{r['boot_ci_lower']:.3g},{r['boot_ci_upper']:.3g}] "
                 f"n1={int(r['n1'])} n2={int(r['n2'])}")
txt = "\n".join(lines)
with open(os.path.join(OUT, "G2b_curated_summary.txt"), "w", encoding="utf-8") as f:
    f.write(txt + "\n")
print(txt)

if not HAVE_MPL:
    print("[skip] figures not rendered (matplotlib missing)")
    sys.exit(0)

# ---- Volcano: indirect vs -log10(q) ----
fig, ax = plt.subplots(figsize=(8, 6))
colors = np.where(df_eval["sig"], "#c0392b", "#3498db")
ax.scatter(df_eval["indirect"], df_eval["logq"], c=colors, s=22, alpha=0.75, edgecolors="none")
ax.axhline(-np.log10(0.05), ls="--", c="gray", lw=1)
ax.axvline(0, ls=":", c="gray", lw=1)
ax.set_xlabel("Indirect effect (education -> plasma protein -> AD)")
ax.set_ylabel(r"$-\log_{10}(q_{\mathrm{BH}})$")
ax.set_title("G2b (curated): education -> plasma protein -> AD mediation")
for _, r in df_eval.sort_values("p_ind").head(8).iterrows():
    ax.annotate(r["target"], (r["indirect"], r["logq"]), fontsize=6,
                xytext=(3, 2), textcoords="offset points")
plt.tight_layout()
plt.savefig(os.path.join(OUT, "G2b_curated_volcano.png"), dpi=150)
plt.close()

# ---- Forest top 15 by |indirect| ----
top15 = df_eval.reindex(df_eval["indirect"].abs().sort_values(ascending=False).index).head(15).iloc[::-1]
y = np.arange(len(top15))
err = 1.96 * top15["se_ind"]
fig, ax = plt.subplots(figsize=(8, 6))
ax.errorbar(top15["indirect"], y, xerr=err.values, fmt="o", c="#2c3e50", ecolor="#7f8c8d", capsize=3)
ax.axvline(0, ls="--", c="#c0392b", lw=1)
ax.set_yticks(y)
ax.set_yticklabels([f"{t[:20]} (n1={int(n1)},n2={int(n2)})"
                    for t, n1, n2 in zip(top15["target"], top15["n1"], top15["n2"])], fontsize=7)
ax.set_xlabel("Indirect effect (95% CI)")
ax.set_title("G2b (curated): top 15 candidate protein mediators")
plt.tight_layout()
plt.savefig(os.path.join(OUT, "G2b_curated_forest_top15.png"), dpi=150)
plt.close()
print("[ok] figures written to", OUT)
