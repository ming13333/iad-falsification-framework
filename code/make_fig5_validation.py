# -*- coding: utf-8 -*-
"""
Figure 5. Validation cohort - quantitative evidence grading (rubric v3).

Rendered directly from output/results/Validation/S8_v3_full.csv so that the
figure and Supplementary Table S8 cannot drift apart.

Columns: case, domain, grade, score, per-gate profile, IVW P, G6 evidence.
Rows are grouped by grade (A/B/C/D) with the same colour code as Table S8.

The canvas is 180 mm wide, the two-column width Frontiers specifies, so a font
size set here is the font size on the page. Minimum visible text is 8 pt and
rules are 2 pt, both taken from the Frontiers figure guidelines.

Run: python code/make_fig5_validation.py
"""

import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
import pandas as pd

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(HERE, "output", "results", "Validation", "S8_v3_full.csv")
OUTDIRS = [os.path.join(HERE, "manuscript", "figures"),
           os.path.join(HERE, "课题设计阶段", "figures")]

PRINT_WIDTH_IN = 180 / 25.4      # 7.0866 in
PRINT_DPI = 400                  # -> 400 dpi at 180 mm
MIN_FONT = 8                     # Frontiers: nothing below 8 pt
RULE_W = 2.0                     # Frontiers: no line below 2 pt

FILL = {"A": "#d9f0d9", "B": "#e6dff5", "C": "#fdf3d3", "D": "#fadcdc"}
EDGE = {"A": "#8fbf8f", "B": "#a58fd0", "C": "#d9b84a", "D": "#d98a8a"}


def fmt_p(p):
    if isinstance(p, str):
        return p
    if p == 0:
        return "0"
    if p < 0.01:
        m, e = f"{p:.1e}".split("e")
        return f"{m}x10$^{{{int(e)}}}$"
    return f"{p:.3f}".rstrip("0").rstrip(".")


def short_g6(s):
    s = str(s)
    if s.startswith("EAS GARD: beta=-0.029"):
        return "EAS GARD, power >= 84%"
    if s.startswith("EAS BioBank"):
        return "EAS BBJ, P = 0.012"
    if s.startswith("EAS GARD: beta=+0.006"):
        return "EAS GARD null (no points)"
    if s.startswith("trans-ethnic"):
        return "trans-ethnic, power < 6%"
    if s.startswith("EAS 26 IV"):
        return "EAS 26 IV, underpowered"
    if s.startswith("none"):
        return "no ancestry replication"
    return "not assessed"


def main():
    d = pd.read_csv(SRC)
    order = {"A": 0, "B": 1, "C": 2, "D": 3}
    d["_o"] = d["grade"].map(order)
    d = d.sort_values(["_o", "score"], ascending=[True, False]).reset_index(drop=True)

    n = len(d)
    fig_h = 0.30 * n + 2.25
    fig, ax = plt.subplots(figsize=(PRINT_WIDTH_IN, fig_h))
    ax.set_xlim(0, 1)
    ax.set_ylim(0, n + 3.00)
    ax.axis("off")

    ax.text(0.5, n + 2.72, "Validation cohort - quantitative evidence grading (rubric v3)",
            ha="center", va="center", fontsize=10, fontweight="bold", color="#222222")
    ax.text(0.5, n + 2.38,
            "Twelve trait pairs scored 0-2 per gate (total 0-12); rows grouped by grade",
            ha="center", va="center", fontsize=MIN_FONT, color="#555555")

    # Column x positions are inches divided by the 7.0866 in canvas, so the
    # 8 pt text of each column cannot run into its neighbour. Widths measured
    # with matplotlib.textpath (sum of content = 4.95 in, 6.99 in available).
    xw = [("N", 0.0085, 0.130), ("Case", 0.0339, 0.900), ("Domain", 0.1679, 0.760),
          ("Grade", 0.2907, 0.360), ("Score", 0.3500, 0.310),
          ("Gates G1-G6", 0.4092, 0.700), ("IVW P", 0.5306, 0.580),
          ("G6 evidence", 0.6322, 2.550)]

    hdr_y = n + 1.55
    ax.add_patch(Rectangle((0.008, hdr_y - 0.02), 0.984, 0.40,
                           facecolor="#3f3f5c", edgecolor="none"))
    for name, x0, _ in xw:
        ax.text(x0, hdr_y + 0.18, name, ha="left", va="center",
                fontsize=MIN_FONT, color="white", fontweight="bold")

    for i, r in d.iterrows():
        y = n - i + 0.35
        ax.add_patch(Rectangle((0.008, y - 0.27), 0.984, 0.54,
                               facecolor=FILL[r["grade"]], edgecolor=EDGE[r["grade"]],
                               linewidth=2.0))
        prof = "\u00b7".join(str(r[g]) for g in ["L1", "L2", "L3", "L4", "L5", "L6"])
        vals = [str(i + 1), r["case"], r["domain"], r["grade"], str(r["score"]), prof,
                fmt_p(r["IVW_P"]), short_g6(r["G6_evidence"])]
        for (name, x0, _), v in zip(xw, vals):
            wt = "bold" if name in ("Grade", "Score") else "normal"
            ax.text(x0, y, v, ha="left", va="center", fontsize=MIN_FONT,
                    fontweight=wt, color="#1c1c1c", family="DejaVu Sans")

    ax.text(0.008, 0.20,
            "Grade A: 10-12 | B: 7-9 | C: 4-6 | D: 0-3.   "
            "G1 and G6 are binary; G1 = 0 sets the total to 0 (Grade D).\n"
            "Gate profile lists points awarded at G1-G6. Two blinded scoring passes "
            "agreed on 11/12 grades (kappa = 0.89).",
            ha="left", va="center", fontsize=MIN_FONT, color="#555555")

    fig.subplots_adjust(left=0.005, right=0.995, top=0.995, bottom=0.005)
    for dd in OUTDIRS:
        os.makedirs(dd, exist_ok=True)
        base = os.path.join(dd, "Fig5_validation_grading")
        fig.savefig(base + ".png", dpi=PRINT_DPI, facecolor="white")
        fig.savefig(base + ".pdf", facecolor="white")
        fig.savefig(base + ".svg", facecolor="white")
        print("wrote", base + ".{png,pdf,svg}")


if __name__ == "__main__":
    main()
