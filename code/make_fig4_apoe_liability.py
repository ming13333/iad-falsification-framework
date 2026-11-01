# -*- coding: utf-8 -*-
"""Figure 4. APOE-locus shared liability between insomnia and Alzheimer's disease.

Panel (A)  cross-trait LDSC genetic correlation, genome-wide and after removing
           chromosome 19. Estimates and standard errors are the archived values
           in Phase1_comprehensive_results.md (rg -0.0283, SE 0.0496, P 0.568;
           rg -0.0314, SE 0.0494, P 0.526).
Panel (B)  per-locus colocalization PP.H4 in the forward (47 insomnia leads
           against AD windows) and reverse (32 AD leads against insomnia windows)
           scans, with the 0.80 support threshold marked.
Panel (C)  where the 18 reverse-sharing loci sit: 16 in the APOE region
           (GRCh37 chr19:45.06-45.82 Mb), 2 at chr11p11.2, none elsewhere.

This figure replaces a mislabelled file: the PNG/SVG previously shipped as
"Fig4_apoe_shared_liability" was the five-dimension triangulation summary, which
is not what the Figure 4 legend or the Results text describes. Counts are
asserted below so the figure cannot silently drift from Supplementary Table S1.

Run: python code/make_fig4_apoe_liability.py
"""

import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(HERE, "manuscript", "supplementary", "S1_coloc_loci.csv")
OUTDIRS = [os.path.join(HERE, "manuscript", "figures"),
           os.path.join(HERE, "课题设计阶段", "figures")]

PRINT_WIDTH_IN = 180 / 25.4
PRINT_DPI = 400
MIN_FONT = 8
RULE_W = 2.0

APOE_LO, APOE_HI = 45_060_000, 45_820_000
RG = [("Genome-wide", -0.0283, 0.0496, "P = 0.57"),
      ("No chr19", -0.0314, 0.0494, "P = 0.53")]

C_APOE, C_CHR11, C_OTHER, C_FWD = "#c00000", "#e08a00", "#9a9a9a", "#2f5d8a"


def main():
    d = pd.read_csv(SRC)
    d = d[(d["dataset"] == "main") & (d["direction"].isin(["forward", "reverse"]))].copy()

    fwd = d[d["direction"] == "forward"]
    rev = d[d["direction"] == "reverse"]
    n_fwd, n_rev = len(fwd), len(rev)
    s_fwd = int((fwd["PP.H4"] >= 0.80).sum())
    s_rev = int((rev["PP.H4"] >= 0.80).sum())

    strong = rev[rev["PP.H4"] >= 0.80].copy()
    in_apoe = strong[(strong["chr"] == 19) &
                     (strong["pos"] >= APOE_LO) & (strong["pos"] <= APOE_HI)]
    in_chr11 = strong[strong["chr"] == 11]
    elsewhere = len(strong) - len(in_apoe) - len(in_chr11)

    # hard gate: the figure must agree with the Results text and Table S1
    assert (n_fwd, n_rev) == (47, 32), (n_fwd, n_rev)
    assert (s_fwd, s_rev) == (1, 18), (s_fwd, s_rev)
    assert (len(in_apoe), len(in_chr11), elsewhere) == (16, 2, 0), (
        len(in_apoe), len(in_chr11), elsewhere)

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

    fig, (axA, axB, axC) = plt.subplots(
        1, 3, figsize=(PRINT_WIDTH_IN, 3.25),
        gridspec_kw={"width_ratios": [1.05, 1.55, 0.85]})
    fig.subplots_adjust(left=0.145, right=0.982, top=0.795, bottom=0.245, wspace=0.46)

    # ---------------- panel (A): rg forest --------------------------------
    ys = np.arange(len(RG))[::-1]
    for (lab, b, se, ptxt), y in zip(RG, ys):
        axA.plot([b - 1.96 * se, b + 1.96 * se], [y, y], "-", color=C_FWD,
                 lw=RULE_W, solid_capstyle="butt", zorder=2)
        axA.plot([b], [y], "o", color=C_FWD, ms=6, zorder=3,
                 markeredgecolor="white", markeredgewidth=1.0)
        axA.text(b, y + 0.22, f"{b:.3f} ({ptxt})", ha="center", va="bottom",
                 fontsize=MIN_FONT, color="#222222")
    axA.axvline(0, color="#888888", lw=RULE_W, ls=(0, (4, 3)), zorder=1)
    axA.set_yticks(ys)
    axA.set_yticklabels([r[0] for r in RG], fontsize=MIN_FONT)
    axA.set_ylim(-0.7, len(RG) - 0.05)
    axA.set_xlim(-0.16, 0.12)
    axA.set_xlabel("Cross-trait $r_g$ (95% CI)", fontsize=MIN_FONT)
    axA.set_title("Genetic correlation", loc="left", fontweight="bold", fontsize=9)

    # ---------------- panel (B): PP.H4 per locus --------------------------
    rng = np.random.default_rng(20261101)
    for x0, sub, col_default in ((0, fwd, C_FWD), (1, rev, C_OTHER)):
        jit = rng.uniform(-0.16, 0.16, len(sub))
        axB.scatter(np.full(len(sub), x0) + jit, sub["PP.H4"], s=7,
                    color=col_default, alpha=0.55, linewidths=0, zorder=2)
    revj = rev[rev["PP.H4"] >= 0.80]
    apoe = revj[(revj["chr"] == 19) & (revj["pos"] >= APOE_LO) & (revj["pos"] <= APOE_HI)]
    c11 = revj[revj["chr"] == 11]
    axB.scatter(np.clip(rng.uniform(0.86, 1.14, len(apoe)), 0.84, 1.16),
                apoe["PP.H4"], s=16, color=C_APOE, linewidths=0, zorder=4)
    axB.scatter(np.clip(rng.uniform(0.86, 1.14, len(c11)), 0.84, 1.16),
                c11["PP.H4"], s=16, color=C_CHR11, linewidths=0, zorder=4)
    axB.axhline(0.80, color="#555555", lw=RULE_W, ls=(0, (4, 3)), zorder=1)
    axB.text(-0.42, 0.815, "PP.H4 = 0.80", fontsize=MIN_FONT, color="#555555",
             va="bottom", ha="left")
    axB.text(1.0, 1.045, "APOE region, 16", ha="center", va="bottom",
             fontsize=MIN_FONT, color=C_APOE, fontweight="bold")
    axB.text(1.0, 0.875, "chr11p11.2, 2", ha="center", va="bottom",
             fontsize=MIN_FONT, color=C_CHR11, fontweight="bold")
    axB.text(0, 0.55, f"{s_fwd}/{n_fwd}", ha="center", fontsize=MIN_FONT,
             fontweight="bold", color="#333333")
    axB.text(1, 0.55, f"{s_rev}/{n_rev}", ha="center", fontsize=MIN_FONT,
             fontweight="bold", color="#333333")
    axB.set_xticks([0, 1])
    axB.set_xticklabels(["Forward\n(insomnia to AD)", "Reverse\n(AD to insomnia)"],
                        fontsize=MIN_FONT)
    axB.set_xlim(-0.5, 1.5)
    axB.set_ylim(0, 1.12)
    axB.set_ylabel("PP.H4 per locus", fontsize=MIN_FONT)
    axB.set_title("Locus-level colocalization", loc="left", fontweight="bold", fontsize=9)

    # ---------------- panel (C): where the strong loci sit ----------------
    cats = ["APOE\nregion", "chr11\np11.2", "Other"]
    vals = [len(apoe), len(c11), elsewhere]
    cols = [C_APOE, C_CHR11, C_OTHER]
    bars = axC.bar(np.arange(3), vals, width=0.62, color=cols,
                   edgecolor="white", linewidth=RULE_W, zorder=2)
    for b, v in zip(bars, vals):
        axC.text(b.get_x() + b.get_width() / 2, v + 0.4, str(v), ha="center",
                 va="bottom", fontsize=MIN_FONT, fontweight="bold")
    axC.set_xticks(np.arange(3))
    axC.set_xticklabels(cats, fontsize=MIN_FONT)
    axC.set_ylim(0, max(vals) * 1.28)
    axC.set_ylabel("Loci with PP.H4 > 0.8", fontsize=MIN_FONT)
    axC.set_title("Where the 18 sit", loc="left", fontweight="bold", fontsize=9)

    for ax, letter in zip((axA, axB, axC), "ABC"):
        ax.text(-0.02, 1.155, f"({letter})", transform=ax.transAxes,
                fontsize=10, fontweight="bold", va="bottom", ha="left")

    for d_ in OUTDIRS:
        os.makedirs(d_, exist_ok=True)
        base = os.path.join(d_, "Fig4_apoe_shared_liability")
        fig.savefig(base + ".png", dpi=PRINT_DPI, facecolor="white")
        fig.savefig(base + ".svg", facecolor="white")
        print("wrote", base + ".{png,svg}")
    plt.close(fig)


if __name__ == "__main__":
    main()
