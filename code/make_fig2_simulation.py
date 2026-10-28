# -*- coding: utf-8 -*-
"""Figure 2. Operating characteristics of the six-gate scoring rule
(43,200 simulated replicates, scoring rule v3 with the decisive-failure cap).

Rendered from output/results/Simulation/{sim_marginal.csv, sim_operating_chars.csv}
so that the figure, Table 2 and Supplementary Table S9 cannot drift apart.

Panel a  sensitivity (P grade A/B | true effect) against true effect size,
         by pleiotropy regime, with the 0.80 power line.
Panel b  specificity (P grade D | null) and empirical FDR (P null | grade A/B).
Panel c  grade distribution at the largest effect size (beta = 0.15).

Run: python code/make_fig2_simulation.py
"""

import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SIM = os.path.join(HERE, "output", "results", "Simulation")
OUTDIRS = [os.path.join(HERE, "manuscript", "figures")]

NAVY = "#1f3b73"
MID = "#4a6fa5"
LIGHT = "#9db4d4"
SALMON = "#e8a09a"
GREY = "#8a8a8a"
GRADE_FILL = {"A": NAVY, "B": LIGHT, "C": "#e2c05a", "D": "#cfcfcf"}

REGIME_LABEL = {"none": "No pleiotropy", "balanced": "Balanced", "directional": "Directional"}
REGIME_COLOR = {"none": NAVY, "balanced": MID, "directional": LIGHT}


def main():
    marg = pd.read_csv(os.path.join(SIM, "sim_marginal.csv"))
    cell = pd.read_csv(os.path.join(SIM, "sim_operating_chars.csv"))

    plt.rcParams.update({
        "font.family": "DejaVu Sans",
        "font.size": 10,
        "axes.titlesize": 11,
        "axes.labelsize": 10,
        "xtick.labelsize": 9.5,
        "ytick.labelsize": 9.5,
        "legend.fontsize": 9,
        "axes.spines.top": False,
        "axes.spines.right": False,
        "axes.linewidth": 0.9,
    })

    fig, axes = plt.subplots(1, 3, figsize=(11.4, 4.1))
    fig.subplots_adjust(left=0.065, right=0.985, top=0.80, bottom=0.17, wspace=0.32)

    # ---------------- panel a: sensitivity vs effect size -------------------
    ax = axes[0]
    effects = [0.08, 0.15]
    paths = {}
    for reg in ["none", "balanced", "directional"]:
        sub = marg[(marg["pleio"] == reg) & (marg["effect"].isin(effects))].sort_values("effect")
        y = sub["sens_AB"].values
        paths[reg] = y
        ax.plot(effects, y, "-o", color=REGIME_COLOR[reg], lw=1.8, ms=6, zorder=3,
                markeredgecolor="white", markeredgewidth=1.1,
                label=REGIME_LABEL[reg])
    # staggered end labels so the two close values (0.72 / 0.69) stay legible
    ends = sorted(((paths[r][-1], r) for r in paths), reverse=True)
    offsets = [8, 0, -12]
    for (val, reg), dy in zip(ends, offsets):
        ax.annotate(f"{val:.2f}", (effects[-1], val), xytext=(9, dy),
                    textcoords="offset points", va="center", fontsize=9,
                    color=REGIME_COLOR[reg])
    ax.axhline(0.80, color=GREY, lw=1.0, ls=(0, (4, 3)), zorder=2)
    ax.text(0.083, 0.815, "0.80 power", color=GREY, fontsize=9, va="bottom")
    ax.legend(frameon=False, loc="lower right", handlelength=1.8, borderaxespad=0.4)
    ax.set_xlim(0.045, 0.17)
    ax.set_ylim(0, 1.05)
    ax.set_xticks([0.08, 0.15])
    ax.set_xticklabels(["0.08", "0.15"])
    ax.set_xlabel("True effect size (beta, per SD)")
    ax.set_ylabel("Sensitivity  P(grade A/B | effect > 0)")
    ax.set_title("Sensitivity rises with effect;\nweak effects are capped at Grade C",
                 loc="left", fontweight="bold")

    # ---------------- panel b: specificity and FDR --------------------------
    ax = axes[1]
    regs = ["none", "balanced", "directional"]
    spec = []
    fdr = []
    for r in regs:
        sub = cell[(cell["pleio"] == r) & (cell["effect"] == 0)]
        spec.append(float(np.nanmean(sub["spec"])))
        fdr.append(float(np.nanmean(cell[cell["pleio"] == r]["fdr"])))
    x = np.arange(len(regs))
    w = 0.34
    b1 = ax.bar(x - w / 2, spec, w, color=NAVY, label="Specificity  P(D | null)")
    b2 = ax.bar(x + w / 2, fdr, w, color=SALMON, label="FDR  P(null | grade A/B)")
    for bars in (b1, b2):
        for rect in bars:
            h = rect.get_height()
            ax.annotate(f"{h:.2f}", (rect.get_x() + rect.get_width() / 2, h),
                        xytext=(0, 2), textcoords="offset points",
                        ha="center", va="bottom", fontsize=9)
    ax.set_xticks(x)
    ax.set_xticklabels([REGIME_LABEL[r].replace(" ", "\n") for r in regs], fontsize=9.5)
    ax.set_ylim(0, 1.12)
    ax.set_ylabel("Rate")
    ax.legend(frameon=False, loc="upper right", handlelength=1.2)
    ax.set_title("At the null, specificity holds;\nFDR stays inside tolerance",
                 loc="left", fontweight="bold")

    # ---------------- panel c: grade distribution at beta = 0.15 -----------
    ax = axes[2]
    sub = marg[np.isclose(marg["effect"], 0.15)]
    sub = sub.set_index("pleio").loc[regs]
    bottom = np.zeros(len(regs))
    for g in ["A", "B", "C", "D"]:
        vals = sub[f"p_grade{g}"].values
        ax.bar(np.arange(len(regs)), vals, bottom=bottom, width=0.55,
               color=GRADE_FILL[g], label=f"Grade {g}",
               edgecolor="white", linewidth=0.8)
        bottom += vals
    for i, r in enumerate(regs):
        ax.annotate(f"{sub.loc[r, 'p_gradeA']:.2f}", (i, sub.loc[r, "p_gradeA"] / 2),
                    ha="center", va="center", fontsize=9.5, color="white",
                    fontweight="bold")
    ax.set_xticks(np.arange(len(regs)))
    ax.set_xticklabels([REGIME_LABEL[r].replace(" ", "\n") for r in regs], fontsize=9.5)
    ax.set_ylim(0, 1.05)
    ax.set_ylabel("Proportion of replicates")
    ax.legend(frameon=False, ncol=4, loc="lower center",
              bbox_to_anchor=(0.5, -0.30), handlelength=1.0, columnspacing=1.2)
    ax.set_title("Grade A survives pleiotropy\nat beta = 0.15", loc="left",
                 fontweight="bold")

    for ax, letter in zip(axes, "abc"):
        ax.text(-0.16, 1.16, letter, transform=ax.transAxes, fontsize=13,
                fontweight="bold", va="top", ha="left")

    fig.suptitle(
        "Operating characteristics of the six-gate scoring rule across 43,200 simulated "
        "replicates (n_IV x LD blocks x pleiotropy x overlap x effect x 400); "
        "decisive-failure cap applied",
        x=0.065, y=0.965, ha="left", fontsize=9.5, style="italic", color="#555555")

    for d in OUTDIRS:
        os.makedirs(d, exist_ok=True)
        fig.savefig(os.path.join(d, "Fig2_simulation_operating.png"), dpi=300,
                    bbox_inches="tight", facecolor="white")
        fig.savefig(os.path.join(d, "Fig2_simulation_operating.svg"),
                    bbox_inches="tight", facecolor="white")
    plt.close(fig)
    print("spec:", [round(s, 4) for s in spec], "fdr:", [round(f, 4) for f in fdr])
    print("saved Fig2 to:", *OUTDIRS, sep="\n  ")


if __name__ == "__main__":
    main()
