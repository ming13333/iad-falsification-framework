# -*- coding: utf-8 -*-
"""Generate core figures for the framework-elevated manuscript.
Figures: Fig1 (5-layer framework + quadrant), Fig2 (MR forest + coloc), Fig5 (triangulation).
Reproducible: managed python venv (matplotlib/numpy). Headless Agg backend.
All numbers sourced from Phase1_comprehensive_results.md / Phase2A §3.x / ea_mr_report.txt.
"""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
import numpy as np
import os

OUT = os.path.join(os.path.dirname(__file__), "..", "课题设计阶段", "figures")
os.makedirs(OUT, exist_ok=True)
plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 10,
                     "axes.spines.top": False, "axes.spines.right": False})

# ---------------------------------------------------------------------------
# FIG 1: Triangulation framework pipeline + comorbidity quadrant
# ---------------------------------------------------------------------------
def fig1():
    fig = plt.figure(figsize=(11, 5.2))
    # left: pipeline
    axL = fig.add_axes([0.03, 0.08, 0.56, 0.84])
    axL.axis("off")
    layers = [
        ("Layer 1  Phenomenological", "Bidirectional MR + LD-clump sensitivity",
         "Does the raw MR signal survive\ninstrument-independence?", "#cfe8ff"),
        ("Layer 2  Genome-wide", "LDSC genetic correlation +/- chr19/APOE",
         "Genome-wide shared architecture\nor locus-specific signal?", "#d6f0d6"),
        ("Layer 3  Locus-level", "Colocalization (coloc.abf)",
         "Same causal variant or\nlinkage disequilibrium?", "#fff2cc"),
        ("Layer 4  Mechanistic", "Two-step protein / metabolite mediation MR",
         "Do known mediators\ntransmit comorbidity?", "#ffe0cc"),
        ("Layer 5  Protective factor", "MVMR + educational PheWAS",
         "What protective factor\nremains after upstream?", "#f0d6f0"),
    ]
    y = 0.92
    for i, (t, m, q, c) in enumerate(layers):
        box = FancyBboxPatch((0.02, y-0.148), 0.52, 0.138,
                             boxstyle="round,pad=0.008,rounding_size=0.02",
                             facecolor=c, edgecolor="#555", lw=1.1)
        axL.add_patch(box)
        # title, method, question stacked vertically
        axL.text(0.05, y-0.04, t, fontsize=10.0, fontweight="bold", va="center")
        axL.text(0.05, y-0.09, "Analysis: " + m, fontsize=7.8, va="center", color="#333")
        qtext = "Q: " + q.replace("\n", " ")
        axL.text(0.05, y-0.125, qtext, fontsize=7.2, va="center",
                 color="#a33", style="italic", wrap=True)
        if i < 4:
            arr = FancyArrowPatch((0.28, y-0.148), (0.28, y-0.148-0.04),
                                  arrowstyle="-|>", mutation_scale=11, color="#777", lw=1.3)
            axL.add_patch(arr)
        y -= 0.190
    axL.text(0.28, 0.975, "Triangulation framework for causal verification", ha="center",
             fontsize=11.5, fontweight="bold")
    axL.text(0.28, 0.935, "Each layer narrows the space of plausible causal interpretations",
             ha="center", fontsize=8, style="italic", color="#666")

    # right: quadrant
    axR = fig.add_axes([0.64, 0.10, 0.34, 0.80])
    axR.set_xlim(0, 2); axR.set_ylim(0, 2)
    axR.set_xticks([0.5, 1.5]); axR.set_yticks([0.5, 1.5])
    axR.set_xticklabels(["rg ~ 0", "|rg| > 0"], fontsize=9)
    axR.set_yticklabels(["MR null", "MR causal"], fontsize=9)
    axR.set_xlabel("Genome-wide genetic correlation (LDSC)", fontsize=9)
    axR.set_ylabel("Causal evidence (MR/MVMR)", fontsize=9)
    cells = {(0.5,1.5):"I\nTrue causal\ncomorbidity",
             (1.5,1.5):"II\nIndependent\ncausal chain",
             (0.5,0.5):"III\nShared liability\n(no upstream)",
             (1.5,0.5):"IV\nApparent\ncomorbidity"}
    col = {(0.5,1.5):"#ffe6cc",(1.5,1.5):"#d9f2d9",(0.5,0.5):"#ffd6d6",(1.5,0.5):"#e8e8e8"}
    for (cx,cy),lab in cells.items():
        axR.add_patch(plt.Rectangle((cx-0.5,cy-0.5),1,1,facecolor=col[(cx,cy)],
                                    edgecolor="#888", lw=1.2))
        axR.text(cx, cy, lab, ha="center", va="center", fontsize=8.3)
    # highlight quadrant III for insomnia-AD
    axR.add_patch(plt.Rectangle((0,0),1,1, fill=False, edgecolor="#c00", lw=2.6))
    axR.text(0.5, 1.86, "insomnia - AD  ->  Quadrant III", ha="center",
             fontsize=9.2, fontweight="bold", color="#c00")
    axR.set_title("Comorbidity classification", fontsize=10.5, fontweight="bold", pad=10)
    fig.savefig(os.path.join(OUT, "Fig1_framework_quadrant.png"), dpi=300, bbox_inches="tight")
    fig.savefig(os.path.join(OUT, "Fig1_framework_quadrant.svg"), bbox_inches="tight")
    plt.close(fig)

# ---------------------------------------------------------------------------
# FIG 2A: MR forest (clump reversal + education protection)  2B: coloc loci
# ---------------------------------------------------------------------------
def fig2():
    # 2A forest
    est = [
        ("Unclumped UVMR\ninsomnia->AD", 0.1035, 0.041, 0.166, "#c00000"),
        ("Clumped UVMR (r2=0.1)\ninsomnia->AD", -0.130, -0.528, 0.268, "#555"),
        ("Clumped UVMR (r2=0.001)\ninsomnia->AD", -0.111, -0.567, 0.345, "#555"),
        ("MVMR insomnia\n(full model)", -0.567, -1.122, -0.012, "#555"),
        ("Education->AD\n(PheWAS)", -0.328, -0.480, -0.176, "#1f77b4"),
        ("Education->PD\n(PheWAS)", -0.387, -0.549, -0.225, "#1f77b4"),
        ("Education->AD\nEast Asian rep.", -0.0285, -0.327, 0.270, "#7fb3d5"),
    ]
    fig, (axA, axB) = plt.subplots(1, 2, figsize=(11, 4.6),
                                   gridspec_kw={"width_ratios":[2.4, 1]})
    ys = np.arange(len(est))[::-1]
    for (lab,b,lo,hi,c),y in zip(est, ys):
        axA.plot([b], [y], "o", color=c, ms=7, zorder=3)
        axA.plot([lo,hi], [y,y], "-", color=c, lw=2, zorder=2)
        axA.text(0.30 if b<0.30 else b+0.02, y, lab, va="center", fontsize=8.4,
                 ha="left" if b>=0.30 else "right", color="#222")
    axA.axvline(0, color="#999", lw=1, ls="--")
    axA.set_yticks([]); axA.set_ylim(-0.7, len(est)-0.3)
    axA.set_xlim(-1.25, 0.45)
    axA.set_xlabel("MR effect (log OR per SD)   [>0 insomnia promotes AD | <0 protective]", fontsize=8.8)
    axA.set_title("A. Key MR estimates: clump reversal & education protection", fontsize=10, fontweight="bold")
    axA.text(-1.2, len(est)-0.05, "Unclumped +0.10 flips to null after LD-clump; education protects AD/PD;",
             fontsize=7.6, style="italic", color="#666")

    # 2B coloc
    dirs = ["Fwd main", "Fwd repl", "Rev main", "Rev repl"]
    strong = [1, 0, 18, 0]
    total = [47, 49, 32, 1]
    x = np.arange(len(dirs))
    axB.bar(x, total, color="#e8e8e8", edgecolor="#999", label="tested loci")
    axB.bar(x, strong, color="#c00000", label="PP.H4>0.8 (shared)")
    for xi,s,t in zip(x, strong, total):
        axB.text(xi, t+0.6, f"{s}/{t}", ha="center", fontsize=8.2, fontweight="bold")
    axB.set_xticks(x); axB.set_xticklabels(dirs, fontsize=8.2, rotation=15)
    axB.set_ylabel("# loci", fontsize=9)
    axB.set_title("B. Colocalization (PP.H4>0.8)", fontsize=10, fontweight="bold")
    axB.legend(fontsize=7.5, loc="upper right")
    fig.tight_layout()
    fig.savefig(os.path.join(OUT, "Fig2_MR_forest_coloc.png"), dpi=300, bbox_inches="tight")
    fig.savefig(os.path.join(OUT, "Fig2_MR_forest_coloc.svg"), bbox_inches="tight")
    plt.close(fig)

# ---------------------------------------------------------------------------
# FIG 5: Triangulation synthesis -> quadrant III
# ---------------------------------------------------------------------------
def fig5():
    fig, ax = plt.subplots(figsize=(11, 3.4))
    ax.axis("off")
    rows = [
        ("Layer 1", "Phenomenological", "Unclumped +0.10 -> null after clump", "Gatekeeper TRIGGERED", "#ffd6d6"),
        ("Layer 2", "Genome-wide", "rg=-0.03 (p=0.57); no change after chr19/APOE", "No genome-wide shared arch", "#ffd6d6"),
        ("Layer 3", "Locus-level", "Reverse coloc strong (18/32); forward weak", "Shared liability, not directed", "#ffd6d6"),
        ("Layer 4", "Mechanistic", "Protein null (FDR=0.91); TG mediates education", "Lipid, not inflammation", "#ffd6d6"),
        ("Layer 5", "Protective factor", "Education protects AD/PD (p<1e-5); EA repl consistent", "Independent protective factor", "#d9f2d9"),
    ]
    y = 0.92
    for l, m, f, v, c in rows:
        ax.add_patch(FancyBboxPatch((0.02,y-0.13),0.10,0.12,boxstyle="round,pad=0.005",
                                    facecolor="#eee", edgecolor="#888", lw=1))
        ax.text(0.07, y-0.07, l, ha="center", va="center", fontsize=8.6, fontweight="bold")
        ax.text(0.14, y-0.035, m, fontsize=8.8, fontweight="bold", va="center")
        ax.text(0.14, y-0.095, f, fontsize=8.0, va="center", color="#333")
        ax.add_patch(FancyBboxPatch((0.62,y-0.13),0.36,0.12,boxstyle="round,pad=0.005",
                                    facecolor=c, edgecolor="#a00", lw=1.2))
        ax.text(0.80, y-0.07, v, ha="center", va="center", fontsize=8.4, fontweight="bold")
        if y > 0.30:
            ax.add_patch(FancyArrowPatch((0.52,y-0.07),(0.62,y-0.07),
                          arrowstyle="-|>", mutation_scale=9, color="#777", lw=1.2))
        y -= 0.165
    ax.add_patch(FancyBboxPatch((0.02,0.02),0.96,0.14,boxstyle="round,pad=0.008",
                                facecolor="#ffe0e0", edgecolor="#c00", lw=2))
    ax.text(0.50, 0.09, "SYNTHESIS:  insomnia-AD = Quadrant III  (shared APOE-locus liability, no independent causal upstream)",
            ha="center", va="center", fontsize=10, fontweight="bold", color="#900")
    ax.set_title("Triangulation synthesis across the five analytical dimensions", fontsize=11, fontweight="bold", loc="left")
    fig.savefig(os.path.join(OUT, "Fig5_triangulation.png"), dpi=300, bbox_inches="tight")
    fig.savefig(os.path.join(OUT, "Fig5_triangulation.svg"), bbox_inches="tight")
    plt.close(fig)

if __name__ == "__main__":
    fig1(); fig2(); fig5()
    print("Figures written to", os.path.abspath(OUT))
