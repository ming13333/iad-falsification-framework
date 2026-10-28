#!/usr/bin/env python3
"""Build Supplementary Table S10: leave-one-gate-out ablation.

Reads the ablation table produced by code/build_s8_v3.py and writes the
published version. Kept as a separate step so the published table can be
regenerated whenever the scoring table changes (it did, when the G6 criterion
was tightened).

Outputs
  output/results/Validation/S10_gate_ablation.csv
  manuscript/supplementary/S10_gate_ablation.csv
"""
import os

import pandas as pd

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, "results", "validation", "S8_v3_ablation.csv")
# Supplement location. The deposited layout is manuscript/supplementary; set
# IAD_SUPP_DIR to write somewhere else without editing the script.
SUPP = os.path.join(ROOT, os.environ.get("IAD_SUPP_DIR", "manuscript/supplementary"))

RENAME = {
    "case": "Case",
    "gate_removed": "Gate removed",
    "gate_points": "Points of removed gate",
    "score_5gates_out_of_10": "Score of remaining five gates (max 10)",
    "score_rescaled_0_12": "Rescaled to 0-12",
    "grade": "Grade",
    "full_grade": "Full-rubric grade",
    "verdict_flips": "Grade changes",
}


def main():
    d = pd.read_csv(SRC)
    missing = set(RENAME) - set(d.columns)
    if missing:
        raise SystemExit(f"ablation file missing columns: {sorted(missing)}")
    out = d[list(RENAME)].rename(columns=RENAME)
    out = out.sort_values(["Case", "Gate removed"], kind="stable")

    out.to_csv(os.path.join(SUPP, "S10_gate_ablation.csv"),
               index=False, encoding="utf-8-sig")

    per_gate = out.groupby("Gate removed")["Grade changes"].sum()
    print("grade changes per removed gate:")
    print(per_gate.to_string())
    print(f"\nrows: {len(out)}  cases: {out['Case'].nunique()}")


if __name__ == "__main__":
    main()
