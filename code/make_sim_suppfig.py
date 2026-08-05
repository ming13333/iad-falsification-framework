# -*- coding: utf-8 -*-
"""SuppFig: Simulation operating characteristics of the six-level framework.
Panel A: sensitivity (P(grade A/B | true effect>0)) vs effect size, by pleiotropy.
Panel B: specificity (P(grade D | null)) and FDR (P(null | grade A/B)) by scenario.
Panel C: grade distribution (A/B/C/D) across pleiotropy x effect (marginal).
"""
import os
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

OUT = "C:/Temp/iad_g1/results/Simulation"
df = pd.read_csv(os.path.join(OUT, "sim_operating_chars.csv"))
marg = pd.read_csv(os.path.join(OUT, "sim_marginal.csv"))

plt.rcParams.update({"font.size": 9, "axes.titlesize": 10, "axes.labelsize": 9.5,
                     "xtick.labelsize": 8.5, "ytick.labelsize": 8.5,
                     "legend.fontsize": 8, "figure.dpi": 150})

fig, axes = plt.subplots(1, 3, figsize=(13.5, 4.2))

# ---- Panel A: sensitivity vs effect size by pleiotropy (avg over ld, n_iv, overlap=0) ----
ax = axes[0]
sub = df[df["overlap"] == 0].groupby(["pleio", "effect"])["sens"].mean().reset_index()
colors = {"none": "#1a7f37", "balanced": "#d29922", "directional": "#c0392b"}
for pleio, c in colors.items():
    g = sub[sub["pleio"] == pleio]
    ax.plot(g["effect"], g["sens"], "o-", c=c, label=pleio, lw=1.6, ms=4)
ax.set_xlabel("True effect size (per-SD)")
ax.set_ylabel("Sensitivity (P grade A/B | causal)")
ax.set_ylim(0, 1.05)
ax.set_title("A. Sensitivity")
ax.legend(title="Pleiotropy", frameon=False)

# ---- Panel B: specificity & FDR by scenario (marginal over ld/n_iv, null stratum) ----
ax = axes[1]
scen = df.groupby("pleio").agg(
    spec=("spec", lambda x: np.nanmean(x)),
    fdr=("fdr", lambda x: np.nanmean(x))).reset_index()
x = np.arange(len(scen))
w = 0.35
ax.bar(x - w / 2, scen["spec"], w, label="Specificity (P D | null)", color="#2c6fbb")
ax.bar(x + w / 2, scen["fdr"], w, label="FDR (P null | grade A/B)", color="#e67e22")
ax.set_xticks(x); ax.set_xticklabels(scen["pleio"])
ax.set_ylim(0, 1.05)
ax.set_title("B. Specificity and FDR")
ax.legend(frameon=False)

# ---- Panel C: grade distribution by pleiotropy x effect (marginal) ----
ax = axes[2]
labels = []
n_groups = len(marg)
for _, r in marg.iterrows():
    labels.append("%s\n%.2f" % (r["pleio"], r["effect"]))
bottom = np.zeros(n_groups)
for grade, color in [("A", "#1a7f37"), ("B", "#d29922"), ("C", "#c0392b"), ("D", "#7f8c8d")]:
    vals = marg["p_grade%s" % grade].values
    ax.bar(np.arange(n_groups), vals, bottom=bottom, color=color, label="Grade " + grade, width=0.7)
    bottom += vals
ax.set_xticks(np.arange(n_groups)); ax.set_xticklabels(labels, fontsize=7.5)
ax.set_ylabel("Proportion")
ax.set_ylim(0, 1.05)
ax.set_title("C. Grade assignment (null / weak / moderate)")
ax.legend(frameon=False, ncol=2)

plt.tight_layout()
fig_path = os.path.join(OUT, "SuppFig5_simulation_operating.png")
svg_path = os.path.join(OUT, "SuppFig5_simulation_operating.svg")
plt.savefig(fig_path, bbox_inches="tight")
plt.savefig(svg_path, bbox_inches="tight")
plt.close()
print("saved:", fig_path, svg_path)
