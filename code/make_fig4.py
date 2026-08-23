"""Figure 4: Education PheWAS - AD, PD, MS protection + East Asian replication.
Generates pure vector SVG + PNG."""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np, os

OUT = os.path.join(os.path.dirname(__file__), "..", "docs/historical", "figures")
os.makedirs(OUT, exist_ok=True)

# Data from manuscript §3.5 / §3.5.2
# Format: label, beta, se, p, color
data = [
    ("AD (Kunkle)\nEUR", -0.328, 0.0776, 1.1e-5, "#1f77b4"),
    ("PD (Nalls)\nEUR", -0.387, 0.0826, 7.2e-6, "#1f77b4"),
    ("MS (IMSGC)\nEUR", 0.015, 0.120, 0.90, "#8c8c8c"),
    ("AD (EAS rep.)\nEA", -0.0285, 0.1523, 0.85, "#7fb3d5"),
]

fig, ax = plt.subplots(figsize=(6.5, 3.0))
ys = np.arange(len(data))[::-1]

for (lab, b, se, p, c), y in zip(data, ys):
    lo = b - 1.96*se
    hi = b + 1.96*se
    ax.plot([b], [y], "o", color=c, ms=9, zorder=3)
    ax.plot([lo, hi], [y, y], "-", color=c, lw=2.5, zorder=2)
    p_str = f"p={p:.2g}" if p >= 0.001 else f"p={p:.1g}"
    label_text = f"{lab}\n{b:+.3f} [{lo:.3f}, {hi:.3f}]  {p_str}"
    ax.text(0.42 if b < 0.30 else b+0.02, y, label_text, va="center",
            fontsize=8.5, ha="left" if b >= 0.30 else "right",
            color="#222", linespacing=1.2)

ax.axvline(0, color="#999", lw=1.2, ls="--")
ax.set_yticks([])
ax.set_ylim(-0.7, len(data)-0.3)
ax.set_xlim(-0.55, 0.55)
ax.set_xlabel("MR effect (log OR / SD)  [<0 protective | >0 risk]", fontsize=9)
ax.set_title("Education PheWAS: protection across AD/PD with East Asian replication",
             fontsize=10, fontweight="bold")

ax.annotate("Strong protection\nin EUR", xy=(-0.33, 2.8), fontsize=7.8, color="#1f77b4",
            ha="center", style="italic")
ax.annotate("No effect", xy=(0.12, 1.0), fontsize=7.8, color="#8c8c8c",
            ha="center", style="italic")
ax.annotate("EA direction\nconsistent (wide CI)", xy=(0.05, 0.2), fontsize=7.8, color="#7fb3d5",
            ha="center", style="italic")

fig.tight_layout()
fig.savefig(os.path.join(OUT, "Fig4_education_phewas.png"), dpi=300, bbox_inches="tight")
fig.savefig(os.path.join(OUT, "Fig4_education_phewas.svg"), bbox_inches="tight")
plt.close(fig)
print(f"Figure 4 written to {OUT}")