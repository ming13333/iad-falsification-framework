# -*- coding: utf-8 -*-
"""
Scoring reproducibility of the six-gate rubric (rubric v3).

Reframing (adjudication K-a): the two score sets are NOT two independent
human raters. They are two blinded scoring passes performed on the same
evidence summaries by the author team:
  pass 1  primary reading
  pass 2  deliberately stricter reading of G3 (architecture), G5
          (mediation) and G6 (external validation)
No second-rater identity, date, or independent scoring sheet exists in the
project archive, so the statistic is reported as *scoring reproducibility*,
not inter-rater reliability.

Pass 2 is retained as a sensitivity analysis: it asks whether a
systematically stricter reading changes the grades.

Both passes are re-derived under rubric v3:
  G1 binary (2 if unclumped IVW P<0.05 in claimed direction, else 0)
  G1 cascade: L1 = 0 -> remaining gates uninformative -> score 0, D
  G6 binary and evidence-based: 2 only with a documented independent-
     ancestry replication at power >= 80%; direction concordance with a
     null estimate at adequate power is a failed replication and scores 0

Supersedes code/interrater_reliability.py, which encoded rubric v1.

Run: python code/scoring_reproducibility.py
"""

import json
import os

import numpy as np
from sklearn.metrics import cohen_kappa_score as cks

OUT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                   "output", "results", "Validation")
os.makedirs(OUT, exist_ok=True)

CASES = ["LDL→CAD", "Education→AD", "BMI→T2D", "Height→CAD",
         "Insomnia→AD", "BMI→Stroke", "HDL→CAD", "Depression→AD",
         "CRP→CAD", "BMI→AD", "T2D→AD", "Education→T2D"]
LEVELS = ["G1", "G2", "G3", "G4", "G5", "G6"]

# pass 1 - primary reading under rubric v3
P1 = {
    "LDL→CAD":       [2, 2, 2, 2, 2, 0],   # G6: no documented ancestry replication
    "Education→AD":  [2, 2, 2, 2, 2, 0],   # G6: EAS GARD P=0.85 at >=84% power -> not a replication
    "BMI→T2D":       [2, 2, 2, 2, 2, 0],
    "Height→CAD":    [2, 2, 2, 1, 1, 0],
    "Insomnia→AD":   [2, 0, 1, 1, 0, 0],
    "BMI→Stroke":    [2, 1, 1, 1, 0, 0],
    "HDL→CAD":       [2, 1, 1, 1, 0, 0],
    "Depression→AD": [2, 1, 1, 1, 0, 0],
    "CRP→CAD":       [0, 0, 0, 0, 0, 0],   # G1 cascade
    "BMI→AD":        [0, 0, 0, 0, 0, 0],
    "T2D→AD":        [0, 0, 0, 0, 0, 0],
    "Education→T2D": [2, 1, 2, 1, 1, 2],
}

# pass 2 - deliberately stricter reading (fixed before re-scoring)
P2 = {
    "LDL→CAD":       [2, 2, 2, 2, 2, 0],
    "Education→AD":  [2, 2, 2, 2, 2, 0],
    "BMI→T2D":       [2, 2, 2, 2, 2, 0],
    "Height→CAD":    [2, 2, 1, 2, 0, 0],   # G3: r_g not coloc-tested; G5: no formal mediation
    "Insomnia→AD":   [2, 0, 1, 1, 0, 0],
    "BMI→Stroke":    [2, 1, 1, 1, 0, 0],
    "HDL→CAD":       [2, 1, 1, 1, 0, 0],
    "Depression→AD": [2, 1, 1, 1, 0, 0],
    "CRP→CAD":       [0, 0, 0, 0, 0, 0],
    "BMI→AD":        [0, 0, 0, 0, 0, 0],
    "T2D→AD":        [0, 0, 0, 0, 0, 0],
    "Education→T2D": [2, 1, 2, 2, 1, 2],   # G4: EAS replication supports a direct effect
}


def grade(score):
    return "A" if score >= 10 else ("B" if score >= 7 else ("C" if score >= 4 else "D"))


def summarise(tag, per_level):
    totals = [sum(per_level[c]) for c in CASES]
    grades = [grade(s) for s in totals]
    print(f"\n=== {tag} ===")
    for c in CASES:
        print(f"  {c:<15} {per_level[c]}  score={sum(per_level[c]):>2}  grade={grade(sum(per_level[c]))}")
    print(f"  distribution: {{'A': {grades.count('A')}, 'B': {grades.count('B')}, "
          f"'C': {grades.count('C')}, 'D': {grades.count('D')}}}")
    return totals, grades


t1, g1 = summarise("pass 1 (primary)", P1)
t2, g2 = summarise("pass 2 (stricter)", P2)

print("\n" + "=" * 78)
print("Scoring reproducibility across two blinded passes (rubric v3)")
print("=" * 78)

agree = np.zeros((4, 4), dtype=int)
idx = {"A": 0, "B": 1, "C": 2, "D": 3}
for a, b in zip(g1, g2):
    agree[idx[a], idx[b]] += 1
print("\nAgreement matrix (rows = pass 1, cols = pass 2):")
print(f"{'':>4} {'A':>4} {'B':>4} {'C':>4} {'D':>4}")
for i, gl in enumerate("ABCD"):
    print(f"{gl:>4} " + "  ".join(f"{agree[i, j]:>4}" for j in range(4)))

po = np.mean([a == b for a, b in zip(g1, g2)])
k_grade = cks(g1, g2)
k_grade_w = cks(g1, g2, weights="quadratic")

flat1 = [v for c in CASES for v in P1[c]]
flat2 = [v for c in CASES for v in P2[c]]
k_level = cks(flat1, flat2)
k_level_w = cks(flat1, flat2, weights="quadratic")


def wilson(k, n):
    # normal-approximation CI for kappa is inappropriate; use bootstrap instead
    return None


rng = np.random.default_rng(20261027)
bs = []
for _ in range(10000):
    pick = rng.integers(0, len(g1), len(g1))
    a = [g1[i] for i in pick]
    b = [g2[i] for i in pick]
    if len(set(a)) == 1 and len(set(b)) == 1:
        continue
    try:
        bs.append(cks(a, b))
    except ValueError:
        pass
bs = np.array(bs)
ci = (np.percentile(bs, 2.5), np.percentile(bs, 97.5))

print(f"\nGrade agreement      : {int(po*12)}/12 (raw {po:.4f})")
print(f"Grade kappa          : {k_grade:.4f}  bootstrap 95% CI [{ci[0]:.3f}, {ci[1]:.3f}]")
print(f"Grade kappa (quad.)  : {k_grade_w:.4f}")
print(f"Per-level kappa (72) : {k_level:.4f}  (quadratic {k_level_w:.4f})")
print("\nDisagreements:")
for c in CASES:
    if grade(sum(P1[c])) != grade(sum(P2[c])):
        print(f"  {c}: pass1={P1[c]} ({grade(sum(P1[c]))}); pass2={P2[c]} ({grade(sum(P2[c]))})")

print("\nPer-gate disagreement count:")
for i, lv in enumerate(LEVELS):
    d = sum(1 for c in CASES if P1[c][i] != P2[c][i])
    print(f"  {lv}: {d}/12")

out = {
    "rubric_version": "v3",
    "framing": "scoring reproducibility across two blinded passes (not inter-rater)",
    "pass1_grades": dict(zip(CASES, g1)),
    "pass2_grades": dict(zip(CASES, g2)),
    "pass1_scores": dict(zip(CASES, t1)),
    "pass2_scores": dict(zip(CASES, t2)),
    "agreement": f"{int(po*12)}/12",
    "kappa_grade": round(float(k_grade), 4),
    "kappa_grade_quadratic": round(float(k_grade_w), 4),
    "kappa_grade_ci95_bootstrap": [round(float(ci[0]), 4), round(float(ci[1]), 4)],
    "kappa_per_level": round(float(k_level), 4),
    "kappa_per_level_quadratic": round(float(k_level_w), 4),
    "disagreements": [c for c in CASES
                      if grade(sum(P1[c])) != grade(sum(P2[c]))],
    "v1_for_comparison": {"agreement": "10/12", "kappa_grade": 0.7647,
                          "kappa_grade_quadratic": 0.9412,
                          "kappa_per_level": 0.8941},
}
with open(os.path.join(OUT, "scoring_reproducibility.json"), "w", encoding="utf-8") as f:
    json.dump(out, f, ensure_ascii=False, indent=2)
print("\nwrote", os.path.join(OUT, "scoring_reproducibility.json"))
