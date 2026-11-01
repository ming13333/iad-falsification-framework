# -*- coding: utf-8 -*-
"""Figure 3. Case-study MR estimates and colocalization asymmetry (insomnia-AD).

Panel (A)  seven MR estimates: unclumped UVMR, the two clumped tiers, the MVMR
           direct effect, and the education PheWAS estimates (AD, PD, East Asian
           replication). Values are the archived estimates used throughout the
           manuscript and Supplementary Tables S2/S11.
Panel (B)  colocalization counts: loci tested and loci with PP.H4 > 0.8, forward
           (insomnia leads against AD windows) and reverse (AD leads against
           insomnia windows), main and replication scans.

Canvas is 180 mm wide, minimum text 8 pt, minimum rule 2 pt (Frontiers figure
guidelines). Replaces the Inkscape-merged Fig2_MR_forest_coloc.svg so the figure
can be regenerated from code.

Run: python code/make_fig3_case_study.py
"""

import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUTDIRS = [os.path.join(HERE, "manuscript", "figures"),
           os.path.join(HERE, "课题设计阶段", "figures")]

PRINT_WIDTH_IN = 180 / 25.4
PRINT_DPI = 400
MIN_FONT = 8
RULE_W = 2.0

# label, beta, CI low, CI high, colour
EST = [
    ("Unclumped UVMR\ninsomnia to AD", 0.1035, 0.041, 0.166, "#c00000"),
    ("Clumped UVMR (r2 = 0.1)\ninsomnia to AD", -0.130, -0.528, 0.268, "#555555"),
    ("Clumped UVMR (r2 = 0.001)\ninsomnia to AD", -0.111, -0.567, 0.345, "#555555"),
    ("MVMR insomnia\n(full model)", -0.567, -1.122, -0.012, "#555555"),
    ("Education to AD\n(PheWAS)", -0.328, -0.480, -0.176, "#1f77b4"),
    ("Education to PD\n(PheWAS)", -0.387, -0.549, -0.225, "#1f77b4"),
    ("Education to AD\nEast Asian rep.", -0.0285, -0.327, 0.270, "#7fb3d5"),
]

BAR_LABEL = ["Fwd\nmain", "Fwd\nrepl", "Rev\nmain", "Rev\nrepl"]
BAR_STRONG = [1, 0, 18, 0]
BAR_TOTAL = [47, 49, 32, 1]


def main():
    plt.rcParams.update({
        "font.family": "DejaVu Sans",
        "font.size": MIN_FONT,
        "axes.titlesize": 9,
        "axes.labelsize": MIN_FONT,
        "xtick.labelsize": MIN_FONT,
        "ytick.labelsize": MIN_FONT,
        "legend.fontsize": MIN_FONT,
        "axes.linewidth": RULE_W,
        "xtick.major.width": RULE_W,
        "ytick.major.width": RULE_W,
        "xtick.major.size": 3.5,
        "ytick.major.size": 3.5,
        "axes.spines.top": False,
        "axes.spines.right": False,
    })

    fig, (axA, axB) = plt.subplots(
        1, 2, figsize=(PRINT_WIDTH_IN, 3.45),
        gridspec_kw={"width_ratios": [2.65, 1.0]})
    fig.subplots_adjust(left=0.085, right=0.988, top=0.795, bottom=0.205, wspace=0.10)

    # ---------------- panel (A) forest -------------------------------------
    ys = np.arange(len(EST))[::-1]
    for (lab, b, lo, hi, c), y in zip(EST, ys):
        axA.plot([lo, hi], [y, y], "-", color=c, lw=RULE_W,
                 solid_capstyle="butt", zorder=2)
        axA.plot([b], [y], "o", color=c, ms=6, zorder=3,
                 markeredgecolor="white", markeredgewidth=1.0)
        axA.text(0.36, y, lab, va="center", ha="left", fontsize=MIN_FONT, color="#222222")
    axA.axvline(0, color="#888888", lw=RULE_W, ls=(0, (4, 3)), zorder=1)
    axA.set_yticks([])
    axA.set_ylim(-0.75, len(EST) - 0.25)
    axA.set_xlim(-1.25, 1.55)
    axA.set_xticks([-1.2, -1.0, -0.8, -0.6, -0.4, -0.2, 0.0, 0.2, 0.4])
    axA.set_xlabel("MR effect (log OR per SD)   [>0 insomnia promotes AD | <0 protective]",
                   fontsize=MIN_FONT)
    axA.set_title("Key MR estimates: clump reversal", loc="left",
                  fontweight="bold", fontsize=9)

    # ---------------- panel (B) colocalization -----------------------------
    x = np.arange(len(BAR_LABEL))
    axB.bar(x, BAR_TOTAL, width=0.62, color="#e8e8e8", edgecolor="#8a8a8a",
            linewidth=RULE_W, label="tested loci", zorder=2)
    axB.bar(x, BAR_STRONG, width=0.62, color="#c00000", edgecolor="#8a8a8a",
            linewidth=RULE_W, label="PP.H4 > 0.8", zorder=3)
    for xi, s, t in zip(x, BAR_STRONG, BAR_TOTAL):
        axB.text(xi, t + 1.2, f"{s}/{t}", ha="center", va="bottom",
                 fontsize=MIN_FONT, fontweight="bold")
    axB.set_xticks(x)
    axB.set_xticklabels(BAR_LABEL, fontsize=MIN_FONT,
                        rotation=22, ha="right", rotation_mode="anchor")
    axB.set_ylim(0, 74)
    axB.set_ylabel("Number of loci", fontsize=MIN_FONT)
    axB.set_title("Colocalization\n(PP.H4 > 0.8)", loc="left",
                  fontweight="bold", fontsize=9)
    axB.legend(frameon=False, loc="upper left", handlelength=1.2,
               borderaxespad=0.15, labelspacing=0.15, fontsize=MIN_FONT)

    for ax, letter in zip((axA, axB), "AB"):
        ax.text(-0.02, 1.175, f"({letter})", transform=ax.transAxes,
                fontsize=10, fontweight="bold", va="bottom", ha="left")

    for d in OUTDIRS:
        os.makedirs(d, exist_ok=True)
        base = os.path.join(d, "Fig3_case_study_MR")
        fig.savefig(base + ".png", dpi=PRINT_DPI, facecolor="white")
        fig.savefig(base + ".svg", facecolor="white")
        print("wrote", base + ".{png,svg}")
    plt.close(fig)


if __name__ == "__main__":
    main()
