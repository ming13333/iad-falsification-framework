# -*- coding: utf-8 -*-
"""Figure 1. The six-gate falsification framework.

Panel (A)  the six gates as a descending hierarchy, each gate naming the analysis
           that implements it and the question it answers, ending in the 0-12
           grade.
Panel (B)  the same six gates as a pipeline, contrasted with the traditional
           one-shot MR pipeline.

The file that previously shipped under this name was an Inkscape composite
(Fig1_framework_hierarchy.svg) with no generating script. This version redraws
the same content at 180 mm, the two-column width Frontiers specifies, with a
minimum of 8 pt text and 2 pt rules, so the figure can be regenerated from code.

Run: python code/make_fig1_six_gate.py
"""

import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUTDIRS = [os.path.join(HERE, "manuscript", "figures"),
           os.path.join(HERE, "课题设计阶段", "figures")]

PRINT_WIDTH_IN = 180 / 25.4
PRINT_DPI = 400
MIN_FONT = 8
RULE_W = 2.0

NAME = ["Association", "Robustness", "Genetic architecture", "Direct effect",
        "Biological mediation", "External validation"]
ANALYSIS = [
    "UVMR (unclumped IVW): does a raw genetic signal exist? Screening only.",
    "Clumped UVMR + MRlap + CAUSE: does it survive instrument independence\nand sample overlap?",
    "LDSC rg + colocalization: genome-wide shared polygenic signal,\nor locus-specific sharing?",
    "MVMR: does the effect persist after multivariable adjustment\nfor correlated exposures?",
    "Two-step MR: is there a genetically proxied protein or metabolite\npathway?",
    "Cross-ancestry replication plus positive and negative control\ndiscrimination.",
]
FILL = ["#e8f4ea", "#fdf3d3", "#e3eef8", "#f0e8f8", "#fdf7d2", "#fbe6e6"]

SHORT = [
    ("L1: Association", "UVMR: signal exists?"),
    ("L2: Robustness", "Clump + MRlap + CAUSE"),
    ("L3: Architecture", "LDSC + coloc"),
    ("L4: Direct effect", "MVMR: confounders?"),
    ("L5: Mediation", "Two-step MR"),
    ("L6: Validation", "Cross-ancestry + controls"),
]


def box(ax, x, y, w, h, fill, edge="#333333", lw=RULE_W):
    ax.add_patch(FancyBboxPatch((x, y), w, h,
                                boxstyle="round,pad=0.004,rounding_size=0.010",
                                facecolor=fill, edgecolor=edge, linewidth=lw, zorder=2))


def big_card(ax, x, y, w, h, fill, title, body):
    """Two-block card: bold title above, body text below, both inside the box."""
    box(ax, x, y, w, h, fill)
    ax.text(x + 0.018, y + h - 0.026, title, ha="left", va="top",
            fontsize=8.5, fontweight="bold", color="#1a1a1a", zorder=3)
    ax.text(x + 0.018, y + h - 0.066, body, ha="left", va="top",
            fontsize=MIN_FONT, color="#333333", linespacing=1.35, zorder=3)


def small_card(ax, x, y, w, h, fill, title, body):
    """Compact card: bold title in the upper band, one line of body below."""
    box(ax, x, y, w, h, fill)
    ax.text(x + 0.022, y + h * 0.68, title, ha="left", va="center",
            fontsize=MIN_FONT, fontweight="bold", color="#1a1a1a", zorder=3)
    ax.text(x + 0.022, y + h * 0.26, body, ha="left", va="center",
            fontsize=MIN_FONT, color="#333333", zorder=3)


def arrow(ax, x, y0, y1):
    ax.add_patch(FancyArrowPatch((x, y0), (x, y1), arrowstyle="-|>",
                                 mutation_scale=9, color="#555555",
                                 linewidth=RULE_W, zorder=4))


def main():
    plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": MIN_FONT})
    fig = plt.figure(figsize=(PRINT_WIDTH_IN, 7.15))

    # ================= panel (A): six-gate hierarchy ======================
    axA = fig.add_axes([0.012, 0.020, 0.665, 0.955])
    axA.set_xlim(0, 1)
    axA.set_ylim(0, 1)
    axA.axis("off")

    axA.text(-0.015, 0.997, "(A)", fontsize=10, fontweight="bold", va="top", ha="left")
    axA.text(0.5, 0.972, "Six-level evidence hierarchy for causal claim validation",
             ha="center", va="top", fontsize=10, fontweight="bold", color="#111111")
    axA.text(0.5, 0.936,
             "Each level is a falsification gate; failure at any level downgrades the grade",
             ha="center", va="top", fontsize=MIN_FONT, style="italic", color="#555555")

    top, h, gap = 0.890, 0.106, 0.020
    for i in range(6):
        y = top - h - i * (h + gap)
        big_card(axA, 0.02, y, 0.96, h, FILL[i],
                 f"Level {i + 1} - {NAME[i]}", ANALYSIS[i])
        if i < 5:
            arrow(axA, 0.5, y - 0.001, y - gap + 0.001)

    gy = top - 6 * h - 5 * gap - 0.048
    box(axA, 0.02, gy, 0.96, 0.038, "#2e7d32", edge="#2e7d32")
    axA.text(0.50, gy + 0.019, "Grade A: high-confidence causal claim (score 10-12)",
             ha="center", va="center", fontsize=MIN_FONT, fontweight="bold",
             color="white", zorder=3)
    axA.text(0.50, gy - 0.022,
             "Scoring: 0/1/2 per level, 0-12 total  ->  D (0-3), C (4-6), B (7-9), A (10-12)",
             ha="center", va="top", fontsize=MIN_FONT, color="#444444")

    # ================= panel (B): pipeline comparison =====================
    axB = fig.add_axes([0.705, 0.020, 0.285, 0.955])
    axB.set_xlim(0, 1)
    axB.set_ylim(0, 1)
    axB.axis("off")

    axB.text(-0.10, 0.997, "(B)", fontsize=10, fontweight="bold", va="top", ha="left")
    axB.text(0.5, 0.974, "Traditional MR pipeline", ha="center", va="top",
             fontsize=9, fontweight="bold")
    axB.text(0.5, 0.946, "Discovery-oriented:", ha="center", va="top",
             fontsize=MIN_FONT, style="italic", color="#555555")
    axB.text(0.5, 0.927, "accumulates supporting evidence", ha="center", va="top",
             fontsize=MIN_FONT, style="italic", color="#555555")

    trad = [("GWAS -> IVW (unclumped)", "P < 0.05 -> claim supported"),
            ("Sensitivity analysis", "MR-Egger, PRESSO, WM"),
            ("Publish causal claim", '"X causally increases Y"')]
    y = 0.838
    for i, (t, s) in enumerate(trad):
        small_card(axB, 0.02, y, 0.96, 0.062, "#e3eef8", t, s)
        if i < 2:
            arrow(axB, 0.5, y - 0.001, y - 0.022)
        y -= 0.084

    axB.text(0.5, 0.602, "This framework", ha="center", va="top",
             fontsize=9, fontweight="bold")
    axB.text(0.5, 0.576, "Falsification-oriented:", ha="center", va="top",
             fontsize=MIN_FONT, style="italic", color="#555555")
    axB.text(0.5, 0.559, "accumulates falsifying evidence", ha="center", va="top",
             fontsize=MIN_FONT, style="italic", color="#555555")

    y = 0.470
    for i, (t, s) in enumerate(SHORT):
        small_card(axB, 0.02, y, 0.96, 0.050, FILL[i], t, s)
        if i < 5:
            arrow(axB, 0.5, y - 0.001, y - 0.020)
        y -= 0.0665

    gy = 0.056
    box(axB, 0.02, gy, 0.96, 0.032, "#2e7d32", edge="#2e7d32")
    axB.text(0.50, gy + 0.016, "Evidence grade A/B/C/D", ha="center", va="center",
             fontsize=MIN_FONT, fontweight="bold", color="white", zorder=3)
    axB.text(0.5, gy - 0.010,
             "Shift from accumulating supporting\nevidence to accumulating\nfalsifying evidence",
             ha="center", va="top", fontsize=MIN_FONT, color="#555555",
             linespacing=1.35)

    for d in OUTDIRS:
        os.makedirs(d, exist_ok=True)
        base = os.path.join(d, "Fig1_six_gate_framework")
        fig.savefig(base + ".png", dpi=PRINT_DPI, facecolor="white")
        fig.savefig(base + ".svg", facecolor="white")
        print("wrote", base + ".{png,svg}")
    plt.close(fig)


if __name__ == "__main__":
    main()
