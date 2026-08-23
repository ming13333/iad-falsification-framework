# =====================================================================
# make_g2b_screen_fig.py -- G2b post-02d
# ---------------------------------------------------------------------
# C:/Temp/iad_g1/results/G2b_screen/G2_screen_mediation.csv
# 02d_g2b_screen.R : protein, target, b1,b2, indirect, se_ind
# p_ind, fdr, boot_ci_lower, boot_ci_upper, n1, n2, ...
# G2b_screen_volcano.png -- indirect effect vs -log10p, FDR<0.05
# G2b_screen_forest_top15.png -- |indirect| 15
# G2b_screen_summary.txt -- §3.4.2 / Fig3C
# : python make_g2b_screen_fig.py
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

IN  = "./output/results/G2b_screen/G2_screen_mediation.csv"
OUT = "./output/results/G2b_screen"
os.makedirs(OUT, exist_ok=True)

df = pd.read_csv(IN)
numcols = ["indirect","se_ind","p_ind","fdr","boot_ci_lower","boot_ci_upper","b1","b2","n1","n2"]
for c in numcols:
    if c in df: df[c] = pd.to_numeric(df[c], errors="coervert") if False else pd.to_numeric(df[c], errors="coerce")

df = df.dropna(subset=["indirect","p_ind"]).copy()
df["logp"] = -np.log10(df["p_ind"].clip(lower=1e-300))
df["sig"]  = df["fdr"] < 0.05
df["target"] = df["target"].astype(str).str.replace(",", " ").str.slice(0, 30)

lines = []
lines.append(f"G2b proteome-wide screen summary (n_proteins_screened={len(df)})")
lines.append(f"FDR<0.05 hits: {int(df['sig'].sum())}")
if df["sig"].sum() > 0:
    hits = df[df["sig"]].sort_values("p_ind")
    for _, r in hits.iterrows():
        lines.append(f"  HIT {r['protein']} {r['target']}: indirect={r['indirect']:.4g} "
                     f"p={r['p_ind']:.2g} fdr={r['fdr']:.3g} "
                     f"bootCI=[{r['boot_ci_lower']:.3g},{r['boot_ci_upper']:.3g}] n1={int(r['n1'])} n2={int(r['n2'])}")
# top 5 by |indirect|
top = df.reindex(df["indirect"].abs().sort_values(ascending=False).index).head(5)
lines.append("Top 5 by |indirect|:")
for _, r in top.iterrows():
    lines.append(f"  {r['protein']} {r['target']}: indirect={r['indirect']:.4g} p={r['p_ind']:.2g} fdr={r['fdr']:.3g}")
# strongest by FDR smallest fdr even if >0.05
lines.append("Most significant (smallest FDR):")
for _, r in df.sort_values("fdr").head(5).iterrows():
    lines.append(f"  {r['protein']} {r['target']}: fdr={r['fdr']:.3g} indirect={r['indirect']:.4g} p={r['p_ind']:.2g}")
txt = "\n".join(lines)
with open(os.path.join(OUT, "G2b_screen_summary.txt"), "w", encoding="utf-8") as f:
    f.write(txt + "\n")
print(txt)

if not HAVE_MPL:
    print("[skip] figures not rendered (matplotlib missing)")
    sys.exit(0)

fig, ax = plt.subplots(figsize=(8, 6))
colors = np.where(df["sig"], "#c0392b", "#3498db")
ax.scatter(df["indirect"], df["logp"], c=colors, s=18, alpha=0.7, edgecolors="none")
ax.axhline(-np.log10(0.05), ls="--", c="gray", lw=1)
ax.axvline(0, ls=":", c="gray", lw=1)
ax.set_xlabel("Indirect effect (education -> protein -> AD)")
ax.set_ylabel(r"$-\log_{10}(p)$")
ax.set_title("G2b proteome-wide screen: education -> plasma protein -> AD")
for _, r in df.sort_values("p_ind").head(8).iterrows():
    ax.annotate(r["target"], (r["indirect"], r["logp"]), fontsize=6,
                xytext=(3, 2), textcoords="offset points")
plt.tight_layout()
plt.savefig(os.path.join(OUT, "G2b_screen_volcano.png"), dpi=150)
plt.close()

# ---- Forest top 15 by |indirect|
top15 = df.reindex(df["indirect"].abs().sort_values(ascending=False).index).head(15).iloc[::-1]
y = np.arange(len(top15))
err = 1.96 * top15["se_ind"]
fig, ax = plt.subplots(figsize=(8, 6))
ax.errorbar(top15["indirect"], y, xerr=err.values, fmt="o", c="#2c3e50", ecolor="#7f8c8d", capsize=3)
ax.axvline(0, ls="--", c="#c0392b", lw=1)
ax.set_yticks(y)
ax.set_yticklabels([f"{t[:20]} (n1={int(n)})" for t, n in zip(top15["target"], top15["n1"])], fontsize=7)
ax.set_xlabel("Indirect effect (95% CI)")
ax.set_title("G2b: top 15 protein mediators (education -> protein -> AD)")
plt.tight_layout()
plt.savefig(os.path.join(OUT, "G2b_screen_forest_top15.png"), dpi=150)
plt.close()
print("[ok] figures written to", OUT)