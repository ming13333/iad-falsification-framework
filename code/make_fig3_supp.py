# -*- coding: utf-8 -*-
"""Supplementary Figure 3: two-step MR mediation via plasma proteins (CRP, IL-6).
Left panel: insomnia -> protein -> AD (G2). Right panel: education -> protein -> AD (G2b).
Both show null indirect effects, demonstrating that the inflammatory-protein pathway
is not a mediator of either exposure.
"""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
import numpy as np

OUT = "C:/D/workbuddy/科研/共病分析/课题设计阶段/figures/Fig3_Supp_protein_mediation.png"

# Data: exposure, protein, step_label, b, se, n
data = {
    "Insomnia": [
        ("Interleukin-6", "Step1: insomnia -> IL-6", 0.3908, 0.3989, 42),
        ("Interleukin-6", "Step2: IL-6 -> AD", -0.004269, 0.01288, 2),
        ("Interleukin-6", "Indirect", -0.001668, 0.005314, None),
        ("C-reactive protein", "Step1: insomnia -> CRP", 0.05751, 0.4202, 42),
        ("C-reactive protein", "Step2: CRP -> AD", -0.008921, 0.04869, 3),
        ("C-reactive protein", "Indirect", -0.000513, 0.004679, None),
    ],
    "Education": [
        ("Interleukin-6", "Step1: education -> IL-6", -0.03576, 0.1232, 317),
        ("Interleukin-6", "Step2: IL-6 -> AD", -0.004269, 0.01288, 2),
        ("Interleukin-6", "Indirect", 0.0001527, 0.001075, None),
        ("C-reactive protein", "Step1: education -> CRP", -0.2371, 0.1246, 317),
        ("C-reactive protein", "Step2: CRP -> AD", -0.008921, 0.04869, 3),
        ("C-reactive protein", "Indirect", 0.002115, 0.01132, None),
    ]
}

colors = {"Step1": "#4c72b0", "Step2": "#55a868", "Indirect": "#c44e52"}

def draw_panel(ax, title, rows):
    y = np.arange(len(rows))[::-1]
    for i, (prot, lbl, b, se, n) in enumerate(rows):
        ci = 1.96 * se
        lo, hi = b - ci, b + ci
        key = lbl.split(":")[0]
        c = colors.get(key, "#333")
        ax.errorbar(b, y[i], xerr=[[b-lo], [hi-b]], fmt="o", color=c,
                    ecolor=c, elinewidth=1.6, capsize=3.5, markersize=6, zorder=3)
        ann = f"n={n}" if n is not None else "boot"
        ax.annotate(ann, (hi, y[i]), xytext=(5, 0), textcoords="offset points",
                    fontsize=7, color="#555", va="center")
    ax.axvline(0, color="#333", lw=1.2, ls="--", zorder=1)
    ax.set_yticks(y)
    ax.set_yticklabels([r[1] for r in rows], fontsize=8.5)
    ax.set_title(title, fontsize=10.5, fontweight="bold")
    ax.set_xlabel("MR beta (log-OR scale)", fontsize=9)
    ax.grid(axis="x", color="#e5e5e5", lw=0.6, zorder=0)
    ax.set_axisbelow(True)
    ax.axhspan(-0.5, 2.5, color="#f0f4fa", zorder=0, alpha=0.6)
    ax.axhspan(2.5, 5.5, color="#f3faf3", zorder=0, alpha=0.6)

fig, axes = plt.subplots(1, 2, figsize=(12.5, 5.0), sharex=True)
draw_panel(axes[0], "A. Insomnia -> protein -> AD", data["Insomnia"])
draw_panel(axes[1], "B. Education -> protein -> AD", data["Education"])

# shared x-limits
for ax in axes:
    ax.set_xlim(-0.7, 0.7)

# legend
leg = [Line2D([0], [0], marker="o", color=colors["Step1"], lw=0, markersize=6, label="Step1 (exposure -> protein)"),
       Line2D([0], [0], marker="o", color=colors["Step2"], lw=0, markersize=6, label="Step2 (protein -> AD)"),
       Line2D([0], [0], marker="o", color=colors["Indirect"], lw=0, markersize=6, label="Indirect (product)")]
fig.legend(handles=leg, loc="lower center", ncol=3, fontsize=9, framealpha=0.95,
           bbox_to_anchor=(0.5, -0.02))

fig.suptitle("Supplementary Fig 3. Two-step MR mediation via inflammatory proteins\n"
             "Null indirect effects for both insomnia (G2) and education (G2b) exposures",
             fontsize=12, fontweight="bold", y=1.02)
plt.tight_layout(rect=[0, 0.05, 1, 0.98])
plt.savefig(OUT, dpi=160, bbox_inches="tight")
print("WROTE", OUT)
