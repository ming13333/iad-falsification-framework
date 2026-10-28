# -*- coding: utf-8 -*-
"""
Build S8-v3 (twelve-case validation table) under the adjudicated rubric v3.

Corrections applied to S8-v1 (relative to the published supplementary table):
  C1. G1 is a binary gate (2 if the unclumped IVW estimate is nominally
      significant in the claimed direction, 0 otherwise). S8-v1 assigned
      1 point to three cases whose association P was > 0.05.
  C2. G6 is evidence-based: 2 points only where a documented independent-
      ancestry replication with power >= 80% exists. Four cells that
      carried 2 points had no such record in the project archive and are
      set to 0 (adjudication A).
  C3. The G1 cascade implemented in the scoring engine
      (code/sim_framework_operating_chars.py, grade_framework) is applied
      explicitly: L1 = 0 -> remaining gates uninformative -> score 0, D.

Outputs
  output/results/Validation/S8_v3.csv            corrected 12-case table
  output/results/Validation/S8_v3_ablation.csv   leave-one-gate-out ablation
  output/results/Validation/S8_v3_summary.json   grade distribution, boundary shifts

Run: python code/build_s8_v3.py
"""

import json
import os
import pandas as pd

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# Input must be the frozen submitted version, never the script's own output;
# otherwise a re-run silently reads back its previous corrections.
SRC = os.path.join(HERE, "results", "validation", "S8_v1_original_backup.csv")
if not os.path.exists(SRC):
    SRC = os.path.join(HERE, "manuscript", "supplementary",
                       "S8_twelve_case_validation.csv")
OUT = os.path.join(HERE, "output", "results", "Validation")
os.makedirs(OUT, exist_ok=True)

GATES = ["L1", "L2", "L3", "L4", "L5", "L6"]

# ---------------------------------------------------------------------------
# Evidence notes for the corrections (kept in the table for transparency)
# ---------------------------------------------------------------------------
G6_EVIDENCE = {
    "LDL→CAD":    "none: no cross-ancestry or independent-cohort record in archive",
    "Education→AD": "EAS GARD: beta=-0.029, P=0.85; direction concordant but null at >=84% power -> not a replication, scores 0",
    "BMI→T2D":    "none: no cross-ancestry or independent-cohort record in archive",
    "Height→CAD": "none: no cross-ancestry or independent-cohort record in archive",
    "Education→T2D": "EAS BioBank Japan: beta=-0.145, P=0.012, F=35.5, WM concordant",
}

# G1 basis: only the insomnia case has a separately documented unclumped run
L1_BASIS = {
    "Insomnia→AD": "unclumped IVW, 2,462 instruments (P=9.3e-4); clumped estimate reported in IVW columns",
}
L1_UNCLUMPED_P = {"Insomnia→AD": 9.3e-4}

# G6 veto: adequate power, direction concordant, but the estimate is null.
# Direction concordance alone is not external validation; if the replication
# had the power to detect the claimed effect and did not, the gate fails.
G6_NO_REPLICATION = {
    "Education→AD": "P=0.85 at >=84% power: null replication, not validation",
}

# ---------------------------------------------------------------------------
# Annotation of the published diagnostic columns (no value is invented; where
# provenance is not documented the cell is marked n.r.)
# ---------------------------------------------------------------------------
EGGER_SEMANTICS = {
    "LDL→CAD": "slope (assumed)",
    "Education→AD": "n.r.",
    "BMI→T2D": "slope (assumed)",
    "Height→CAD": "slope (assumed)",
    "Insomnia→AD": "n.r.",
    "BMI→Stroke": "slope (assumed)",
    "HDL→CAD": "MR-Egger causal estimate, not intercept",
    "CRP→CAD": "intercept",
    "BMI→AD": "slope (assumed)",
    "Education→T2D": "intercept",
    "Depression→AD": "slope (assumed)",
    "T2D→AD": "slope (assumed)",
}

N_IV = {
    "Insomnia→AD": "54 clumped (2,462 unclumped)",
    "Education→AD": "40",
}


def grade(score, cuts=(10, 7, 4)):
    a, b, c = cuts
    return "A" if score >= a else ("B" if score >= b else ("C" if score >= c else "D"))


def main():
    d = pd.read_csv(SRC, encoding="utf-8-sig")
    d = d.rename(columns={"Case": "case"})
    orig = d.copy()

    rows = []
    for _, r in d.iterrows():
        case = r["case"]
        s = {g: int(r[g]) for g in GATES}

        # C1: binary G1
        p1 = L1_UNCLUMPED_P.get(case, float(r["IVW_P"]))
        s["L1"] = 2 if p1 < 0.05 else 0

        # C3: cascade
        if s["L1"] == 0:
            for g in GATES[1:]:
                s[g] = 0
        else:
            # C2: evidence-based G6 (only downward corrections applied)
            if s["L6"] > 0 and G6_EVIDENCE.get(case, "none").startswith("none"):
                s["L6"] = 0
            # C4: direction concordance without replication is not validation.
            # Where the cross-ancestry step had adequate power and still
            # returned a null estimate, the step failed to replicate and
            # scores 0, consistent with the insufficient-versus-against
            # distinction applied to the primary case.
            if case in G6_NO_REPLICATION:
                s["L6"] = 0
            if s["L6"] == 1:          # binary gate, no partial tier
                s["L6"] = 0

        total = sum(s.values())

        # Decisive-failure rule (reviewer 1, point 1): failing G2 means the
        # claim did not survive LD/overlap/pleiotropy correction, i.e. it is
        # falsified on robustness grounds. The additive total must not then
        # reach Grade A. Cap the total at the upper bound of Grade C.
        decisive = []
        if s["L2"] == 0 and s["L1"] > 0:
            decisive.append("G2=0 (falsified on robustness)")
            total = min(total, 6)
        rows.append({
            "case": case,
            "domain": r["Domain"],
            **s,
            "score": total,
            "grade": grade(total),
            "decisive_failure": "; ".join(decisive) if decisive else "none",
            "score_v1": int(r["Score"]),
            "grade_v1": r["Grade"],
            "delta": total - int(r["Score"]),
            "grade_changed": grade(total) != r["Grade"],
        })

    v3 = pd.DataFrame(rows)

    # -------------------------------------------------------------------
    # Annotated version: keep the published diagnostics, label provenance
    # -------------------------------------------------------------------
    G6_LABEL = {
        "Insomnia→AD":   "trans-ethnic 30 IV; power <6% -> screening only, no points",
        "Depression→AD": "EAS 26 IV; underpowered -> no points",
        "T2D→AD":        "EAS GARD: beta=+0.006, P=0.93 (null concordant) -> no points",
        "BMI→Stroke":    "not assessed",
        "CRP→CAD":       "not assessed",
        "BMI→AD":        "not assessed",
    }
    full = v3.copy()
    full["IVW_beta"] = orig.set_index("case").loc[v3["case"], "IVW_beta"].values
    full["IVW_SE"] = orig.set_index("case").loc[v3["case"], "IVW_SE"].values
    full["IVW_P"] = orig.set_index("case").loc[v3["case"], "IVW_P"].values
    full["WM_P"] = orig.set_index("case").loc[v3["case"], "WM_P"].values
    full["Egger_P"] = orig.set_index("case").loc[v3["case"], "Egger_P"].values
    full["Egger_P_semantics"] = [EGGER_SEMANTICS.get(c, "n.r.") for c in v3["case"]]
    full["n_IV"] = [N_IV.get(c, "n.r.") for c in v3["case"]]
    full["G6_evidence"] = [G6_EVIDENCE.get(c) or G6_LABEL.get(c, "not assessed")
                           for c in v3["case"]]
    full["notes"] = orig.set_index("case").loc[v3["case"], "Notes"].values
    full.to_csv(os.path.join(OUT, "S8_v3_full.csv"), index=False, encoding="utf-8-sig")

    v3.to_csv(os.path.join(OUT, "S8_v3.csv"), index=False, encoding="utf-8-sig")

    # -------------------------------------------------------------------
    # Leave-one-gate-out ablation (pure arithmetic, no simulation involved)
    # -------------------------------------------------------------------
    abl = []
    for _, r in v3.iterrows():
        base_score, base_grade = r["score"], r["grade"]
        for g in GATES:
            kept = [r[x] for x in GATES if x != g]
            s10 = sum(kept)
            s12 = s10 * 12 / 10                     # rescale to the 0-12 axis
            gd = grade(s12)
            abl.append({
                "case": r["case"], "gate_removed": g,
                "gate_points": r[g],
                "score_5gates_out_of_10": s10,
                "score_rescaled_0_12": round(s12, 2),
                "grade": gd, "full_grade": base_grade,
                "delta_score_full": s10 - base_score,
                "verdict_flips": gd != base_grade,
            })
    abd = pd.DataFrame(abl)
    abd.to_csv(os.path.join(OUT, "S8_v3_ablation.csv"), index=False, encoding="utf-8-sig")

    # -------------------------------------------------------------------
    # Grade-boundary sensitivity
    # -------------------------------------------------------------------
    shifts = {}
    for name, cuts in {"base(10/7/4)": (10, 7, 4),
                       "strictA(11/7/4)": (11, 7, 4),
                       "looseA(9/7/4)": (9, 7, 4),
                       "strictB(10/8/4)": (10, 8, 4),
                       "looseB(10/6/4)": (10, 6, 4)}.items():
        gs = [grade(s, cuts) for s in v3["score"]]
        moved = [(c, gg) for c, gg, sg in zip(v3["case"], gs, v3["score"])
                 if gg != grade(sg)]
        shifts[name] = {"distribution": {k: gs.count(k) for k in "ABCD"},
                        "moved": moved}

    o = orig.set_index("case")
    cell_log = []
    for _, r in v3.iterrows():
        for g in GATES:
            before, after = int(o.loc[r["case"], g]), int(r[g])
            if before != after:
                cell_log.append({"case": r["case"], "gate": g,
                                 "v1": before, "v3": after})

    summary = {
        "n_cases": len(v3),
        "distribution_v3": {k: int((v3["grade"] == k).sum()) for k in "ABCD"},
        "distribution_v1": {k: int((v3["grade_v1"] == k).sum()) for k in "ABCD"},
        "grade_changes": v3.loc[v3["grade_changed"],
                                ["case", "score_v1", "grade_v1", "score", "grade"]]
                           .to_dict("records"),
        "cell_changes": cell_log,
        "boundary_shifts": shifts,
        "ablation_flips": int(abd["verdict_flips"].sum()),
        "ablation_critical_gates": sorted(abd.loc[abd["verdict_flips"],
                                                  "gate_removed"].unique().tolist()),
    }
    with open(os.path.join(OUT, "S8_v3_summary.json"), "w", encoding="utf-8") as f:
        json.dump(summary, f, ensure_ascii=False, indent=2)

    print(v3.to_string(index=False))
    print("\nDistribution v1:", summary["distribution_v1"])
    print("Distribution v3:", summary["distribution_v3"])
    print("\nGrade changes:")
    for c in summary["grade_changes"]:
        print("  ", c)
    print("\nAblation: %d flips; critical gates %s"
          % (summary["ablation_flips"], summary["ablation_critical_gates"]))
    for k, v in shifts.items():
        print(f"  {k}: {v['distribution']} moved={v['moved']}")


if __name__ == "__main__":
    main()
