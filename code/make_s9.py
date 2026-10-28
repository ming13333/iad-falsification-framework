# -*- coding: utf-8 -*-
"""Supplementary Table S9. Cell-level and marginal operating characteristics.

Rebuilds the three S9 artefacts from the frozen replicate table so that the
supplement, Table 2 and Figure 2 are generated from one file:

  manuscript/supplementary/S9_simulation_operating.csv          (cell level)
  manuscript/supplementary/S9_simulation_operating.md           (cell level, formatted)
  manuscript/supplementary/S9_simulation_operating_marginal.csv (marginal)

Cell = (n_iv, LD blocks, pleiotropy, overlap) with 400 replicates per effect
stratum. FDR is pooled within the cell across the one-third-null mixture.

Run: python code/make_s9.py
"""

import os

import numpy as np
import pandas as pd

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SIM = os.path.join(HERE, "output", "results", "Simulation")
SUPP = os.path.join(HERE, "manuscript", "supplementary")

KEYS = ["n_iv", "ld", "pleio", "overlap"]
POS = ("A", "B")


def main():
    d = pd.read_csv(os.path.join(SIM, "sim_replicates.csv"))
    d = d[d["grade"].notna()]

    rows = []
    for key, g in d.groupby(KEYS, sort=True):
        ab = g[g["grade"].isin(POS)]
        fdr = float(np.mean(ab["effect"] == 0)) if len(ab) else np.nan
        neg = g[g["effect"] == 0]
        spec = float(np.mean(neg["grade"] == "D")) if len(neg) else np.nan
        for eff, ge in g.groupby("effect"):
            rows.append(
                {
                    "n_iv": key[0],
                    "ld": key[1],
                    "pleio": key[2],
                    "overlap": key[3],
                    "effect": eff,
                    "sens": (
                        round(float(np.mean(ge["grade"].isin(POS))), 4) if eff > 0 else np.nan
                    ),
                    "spec": round(spec, 4) if eff == 0 else np.nan,
                    "fdr": round(fdr, 6),
                    "n_gradeA": int(np.sum(ge["grade"] == "A")),
                    "n_gradeB": int(np.sum(ge["grade"] == "B")),
                    "n_gradeC": int(np.sum(ge["grade"] == "C")),
                    "n_gradeD": int(np.sum(ge["grade"] == "D")),
                }
            )
    cell = pd.DataFrame(rows).sort_values(KEYS + ["effect"]).reset_index(drop=True)
    cell.to_csv(os.path.join(SUPP, "S9_simulation_operating.csv"), index=False)

    # marginal table by pleiotropy x effect
    marg_rows = []
    for (pleio, eff), g in d.groupby(["pleio", "effect"]):
        gt = g[g["effect"] > 0]
        gn = g[g["effect"] == 0]
        marg_rows.append(
            {
                "pleio": pleio,
                "effect": eff,
                "sens_AB": round(float(np.mean(gt["grade"].isin(POS))), 4) if len(gt) else np.nan,
                "spec_D": round(float(np.mean(gn["grade"] == "D")), 4) if len(gn) else np.nan,
                "p_gradeA": round(float(np.mean(g["grade"] == "A")), 4),
                "p_gradeB": round(float(np.mean(g["grade"] == "B")), 4),
                "p_gradeC": round(float(np.mean(g["grade"] == "C")), 4),
                "p_gradeD": round(float(np.mean(g["grade"] == "D")), 4),
            }
        )
    marg = pd.DataFrame(marg_rows).sort_values(["pleio", "effect"])
    marg.to_csv(os.path.join(SUPP, "S9_simulation_operating_marginal.csv"), index=False)

    lines = [
        "# Supplementary Table 9. Simulation operating characteristics "
        "(43,200 replicates; seed 20260804)\n",
        "The scoring rule is applied as published, including the decisive-failure "
        "cap: a replicate in which the robustness gate (G2) scores 0 has its total "
        "capped at 6, the upper bound of Grade C. Sensitivity (`sens`) and "
        "specificity (`spec`) are proportions of replicates (400 per cell) graded "
        "A/B or D respectively. FDR is the empirical false-discovery proportion "
        "among positive calls (grades A/B) that are null, pooled within scenario.\n",
        "Marginal summaries across LD, overlap and instrument count are in "
        "`S9_simulation_operating_marginal.csv`.\n",
        "| n_iv | ld | pleio | overlap | effect | sens | spec | fdr | n_gradeA | n_gradeB | n_gradeC | n_gradeD |",
        "|---|---|---|---|---|---|---|---|---|---|---|---|",
    ]
    for _, r in cell.iterrows():
        lines.append(
            "| {n_iv} | {ld} | {pleio} | {overlap} | {effect} | {sens} | {spec} | "
            "{fdr} | {n_gradeA} | {n_gradeB} | {n_gradeC} | {n_gradeD} |".format(
                **{k: ("" if (isinstance(v, float) and np.isnan(v)) else v)
                   for k, v in r.items()}
            )
        )
    with open(os.path.join(SUPP, "S9_simulation_operating.md"), "w", encoding="utf-8") as fh:
        fh.write("\n".join(lines) + "\n")
    print("wrote S9: cells=%d, marginal rows=%d" % (len(cell), len(marg)))


if __name__ == "__main__":
    main()
