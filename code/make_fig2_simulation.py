# -*- coding: utf-8 -*-
"""Figure 2. Operating characteristics of the six-gate scoring rule
(43,200 simulated replicates, scoring rule v3 with the decisive-failure cap).

Rendered from output/results/Simulation/{sim_marginal.csv, sim_operating_chars.csv}
so that the figure, Table 2 and Supplementary Table S9 cannot drift apart.

Panel a  sensitivity (P grade A/B | true effect) against true effect size,
         by pleiotropy regime, with the 0.80 power line.
Panel b  specificity under both conventions the paper reports (Grade D only,
         and Grade C or D, which is the convention the operating claim refers
         to) alongside the empirical FDR (P null | grade A/B).
Panel c  grade distribution at the largest effect size (beta = 0.15).

Panel b reads the per-cell grade counts rather than the stored `spec` column,
because the C/D convention has to be formed from n_gradeC + n_gradeD. For the
D-only bars this reproduces the stored column exactly (1.000 / 0.796 / 0.679),
so the figure, Table 2 and Supplementary Table S9 remain one dataset.

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

# Final printed width in inches. 7.5 in = 19.05 cm, the width the figure set
# targets; drawing at this size keeps font sizes physically correct.
PRINT_WIDTH_IN = 7.5
PRINT_DPI = 400                      # -> 400 dpi at 19.05 cm, above the 300 minimum


def main():
    marg = pd.read_csv(os.path.join(SIM, "sim_marginal.csv"))
    cell = pd.read_csv(os.path.join(SIM, "sim_operating_chars.csv"))

    # ---- print-sized canvas -------------------------------------------------
    # The figure is drawn at its final printed width (7.5 in = 19.05 cm), so a
    # font size set here is the font size that reaches the page. Drawing wide
    # (11.4 in) and letting the journal shrink it to column width was the reason
    # the earlier version had an effective 5.6 pt smallest label.
    plt.rcParams.update({
        "font.family": "DejaVu Sans",
        "font.size": 8,
        "axes.titlesize": 8.5,
        "axes.labelsize": 8,
        "xtick.labelsize": 7.5,
        "ytick.labelsize": 7.5,
        "legend.fontsize": 7,
        "axes.spines.top": False,
        "axes.spines.right": False,
        "axes.linewidth": 0.8,
    })

    fig, axes = plt.subplots(1, 3, figsize=(PRINT_WIDTH_IN, 2.95))
    fig.subplots_adjust(left=0.085, right=0.988, top=0.745, bottom=0.205, wspace=0.42)

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
                    textcoords="offset points", va="center", fontsize=7,
                    color=REGIME_COLOR[reg])
    ax.axhline(0.80, color=GREY, lw=1.0, ls=(0, (4, 3)), zorder=2)
    ax.text(0.085, 0.825, "0.80 power", color=GREY, fontsize=6.8, va="bottom")
    ax.legend(frameon=False, loc="lower right", handlelength=1.8, borderaxespad=0.4)
    ax.set_xlim(0.045, 0.17)
    ax.set_ylim(0, 1.05)
    ax.set_xticks([0.08, 0.15])
    ax.set_xticklabels(["0.08", "0.15"])
    ax.set_xlabel("True effect size (beta, per SD)")
    ax.set_ylabel("P(grade A/B | effect > 0)", fontsize=7.5)
    ax.set_title("Sensitivity rises with effect;\nweak effects capped at Grade C",
                 loc="left", fontweight="bold")

    # ---------------- panel b: both specificity conventions + FDR -----------
    ax = axes[1]
    regs = ["none", "balanced", "directional"]
    spec_d, spec_cd, fdr = [], [], []
    for r in regs:
        null = cell[(cell["pleio"] == r) & (cell["effect"] == 0)]
        tot = null[["n_gradeA", "n_gradeB", "n_gradeC", "n_gradeD"]].sum(axis=1)
        spec_d.append(float(np.mean(null["n_gradeD"] / tot)))
        spec_cd.append(float(np.mean((null["n_gradeC"] + null["n_gradeD"]) / tot)))
        fdr.append(float(np.nanmean(cell[cell["pleio"] == r]["fdr"])))
    x = np.arange(len(regs))
    w = 0.26
    ax.bar(x - w, spec_d, w, color=NAVY, label="Specificity, D only")
    ax.bar(x, spec_cd, w, color=LIGHT, label="Specificity, C/D (claimed)")
    ax.bar(x + w, fdr, w, color=SALMON, label="FDR")
    for i in range(len(regs)):
        if abs(spec_d[i] - spec_cd[i]) < 5e-3:
            # the two conventions coincide at the ideal null, so one centred
            # label replaces two that would collide
            ax.annotate(f"{spec_d[i]:.2f}", (x[i] - w / 2, spec_d[i]), xytext=(0, 2),
                        textcoords="offset points", ha="center", va="bottom",
                        fontsize=6.8)
        else:
            ax.annotate(f"{spec_d[i]:.2f}", (x[i] - w, spec_d[i]), xytext=(0, 2),
                        textcoords="offset points", ha="center", va="bottom",
                        fontsize=6.8)
            ax.annotate(f"{spec_cd[i]:.2f}", (x[i], spec_cd[i]), xytext=(0, 2),
                        textcoords="offset points", ha="center", va="bottom",
                        fontsize=6.8)
        ax.annotate(f"{fdr[i]:.2f}", (x[i] + w, fdr[i]), xytext=(0, 2),
                    textcoords="offset points", ha="center", va="bottom",
                    fontsize=6.8)
    ax.set_xticks(x)
    ax.set_xticklabels([REGIME_LABEL[r].replace(" ", "\n") for r in regs], fontsize=7.2)
    # headroom for the legend, but no phantom ticks above 1.0
    ax.set_ylim(0, 1.46)
    ax.set_yticks([0, 0.25, 0.50, 0.75, 1.00])
    ax.set_ylabel("Rate")
    ax.legend(frameon=False, loc="upper right", handlelength=1.1, fontsize=6.6,
              borderaxespad=0.15, labelspacing=0.25)
    ax.set_title("Both specificity conventions\nhold at the null; FDR in tolerance",
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
                    ha="center", va="center", fontsize=7.5, color="white",
                    fontweight="bold")
    ax.set_xticks(np.arange(len(regs)))
    ax.set_xticklabels([REGIME_LABEL[r].replace(" ", "\n") for r in regs], fontsize=7.2)
    ax.set_ylim(0, 1.05)
    ax.set_ylabel("Proportion of replicates")
    ax.legend(frameon=False, ncol=2, loc="lower center",
              bbox_to_anchor=(0.5, -0.46), handlelength=1.0, columnspacing=1.0,
              fontsize=6.8, labelspacing=0.22)
    ax.set_title("Grade A survives pleiotropy\nat beta = 0.15", loc="left",
                 fontweight="bold")

    for ax, letter in zip(axes, "abc"):
        ax.text(-0.155, 1.20, letter, transform=ax.transAxes, fontsize=10,
                fontweight="bold", va="top", ha="left")

    fig.suptitle(
        "Operating characteristics of the six-gate scoring rule across 43,200 simulated replicates\n"
        "(n_IV x LD blocks x pleiotropy x overlap x effect x 400 per cell; decisive-failure cap applied)",
        x=0.085, y=0.985, va="top", ha="left", fontsize=6.5, style="italic", color="#555555",
        linespacing=1.35)

    for d in OUTDIRS:
        os.makedirs(d, exist_ok=True)
        fig.savefig(os.path.join(d, "Fig2_simulation_operating.png"), dpi=PRINT_DPI,
                    bbox_inches="tight", facecolor="white")
        fig.savefig(os.path.join(d, "Fig2_simulation_operating.svg"),
                    bbox_inches="tight", facecolor="white")
    plt.close(fig)
    print("spec D-only:", [round(s, 4) for s in spec_d])
    print("spec C/D   :", [round(s, 4) for s in spec_cd])
    print("fdr        :", [round(f, 4) for f in fdr])
    print("saved Fig2 to:", *OUTDIRS, sep="\n  ")


if __name__ == "__main__":
    main()
