# -*- coding: utf-8 -*-
"""
Figure 5. Validation cohort - quantitative evidence grading (rubric v3).

Rendered directly from output/results/Validation/S8_v3_full.csv so that the
figure and Supplementary Table S8 cannot drift apart.

Columns: case, domain, grade, score, per-gate profile, IVW P, G6 evidence.
Rows are grouped by grade (A/B/C/D) with the same colour code as Table S8.

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
OUTDIRS = [os.path.join(HERE, "manuscript", "figures")]

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
    fig_h = 0.42 * n + 1.9
    fig, ax = plt.subplots(figsize=(13.2, fig_h))
    ax.set_xlim(0, 1)
    ax.set_ylim(0, n + 2.65)
    ax.axis("off")

    ax.text(0.5, n + 2.44, "Validation cohort - quantitative evidence grading (rubric v3)",
            ha="center", va="center", fontsize=15, fontweight="bold", color="#222222")
    ax.text(0.5, n + 2.10,
            "Twelve trait pairs scored 0-2 per gate (total 0-12); rows grouped by grade",
            ha="center", va="center", fontsize=9.5, color="#555555")

    cols = [("N", 0.030), ("Case", 0.175), ("Domain", 0.295), ("Grade", 0.375),
            ("Score", 0.425), ("Gate profile (G1-G6)", 0.560), ("IVW P", 0.665),
            ("G6 evidence", 0.760)]
    xw = [("N", 0.030, 0.035), ("Case", 0.085, 0.130), ("Domain", 0.225, 0.085),
          ("Grade", 0.325, 0.055), ("Score", 0.390, 0.060),
          ("Gate profile (G1-G6)", 0.460, 0.170), ("IVW P", 0.650, 0.075),
          ("G6 evidence", 0.735, 0.245)]

    hdr_y = n + 1.15
    ax.add_patch(Rectangle((0.015, hdr_y - 0.02), 0.97, 0.42,
                           facecolor="#3f3f5c", edgecolor="none"))
    for name, x0, _ in xw:
        ax.text(x0, hdr_y + 0.19, name, ha="left", va="center",
                fontsize=9.5, color="white", fontweight="bold")

    for i, r in d.iterrows():
        y = n - i + 0.35
        ax.add_patch(Rectangle((0.015, y - 0.30), 0.97, 0.60,
                               facecolor=FILL[r["grade"]], edgecolor=EDGE[r["grade"]],
                               linewidth=0.7))
        prof = "\u00b7".join(str(r[g]) for g in ["L1", "L2", "L3", "L4", "L5", "L6"])
        vals = [str(i + 1), r["case"], r["domain"], r["grade"], str(r["score"]), prof,
                fmt_p(r["IVW_P"]), short_g6(r["G6_evidence"])]
        for (name, x0, _), v in zip(xw, vals):
            wt = "bold" if name in ("Grade", "Score") else "normal"
            fs = 10 if name == "Case" else 9
            ax.text(x0, y, v, ha="left", va="center", fontsize=fs, fontweight=wt,
                    color="#1c1c1c", family="DejaVu Sans")

    ax.text(0.015, 0.22,
            "Grade A: 10-12 | B: 7-9 | C: 4-6 | D: 0-3.   "
            "G1 and G6 are binary; G1 = 0 sets the total to 0 (Grade D).\n"
            "Gate profile lists points awarded at G1-G6. Two blinded scoring passes "
            "agreed on 11/12 grades (kappa = 0.89).",
            ha="left", va="center", fontsize=8.2, color="#555555")

    fig.subplots_adjust(left=0.01, right=0.99, top=0.99, bottom=0.01)
    for dd in OUTDIRS:
        os.makedirs(dd, exist_ok=True)
        base = os.path.join(dd, "Fig5_validation_grading")
        fig.savefig(base + ".png", dpi=400, facecolor="white")
        fig.savefig(base + ".pdf", facecolor="white")
        fig.savefig(base + ".svg", facecolor="white")
        print("wrote", base + ".{png,pdf,svg}")


if __name__ == "__main__":
    main()
