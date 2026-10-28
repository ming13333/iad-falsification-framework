"""Reproduce the marginal / cell-level operating characteristics of the six-gate
framework from the frozen replicate table, with explicit FDR definitions.

Why this script exists
----------------------
`sim_framework_operating_chars.py` writes `sim_marginal.csv` containing only
sens_AB / spec_D / p_gradeA-D. It does NOT write any FDR column, yet Table 2,
the Results section and the Abstract of the manuscript all quote a "marginal
empirical FDR" (0.08 balanced, 0.13 directional) plus a scenario range.
This script closes that reproducibility gap by computing FDR under three
explicit definitions and comparing them against the published values.

Definitions (all computed on positives = Grade A or B)
  cell   : within one (n_iv, ld, pleio, overlap) cell, pooling the three
           effect strata (1/3 null, 2/3 causal) -- this is the definition used
           inside sim_framework_operating_chars.py::main().
  pooled : within one pleiotropy regime, all 12 cells pooled (marginal over
           LD concentration, sample overlap, instrument count).
  mean   : unweighted mean of the 12 cell-level FDRs (equal weight per cell).
  range  : min/max of the 12 cell-level FDRs.

Usage:  python code/sim_marginal_fdr.py
"""
import os
import sys

import numpy as np
import pandas as pd

REP_FILE = os.path.join("output", "results", "Simulation", "sim_replicates.csv")
OUT_CELL = os.path.join("output", "results", "Simulation", "sim_cell_fdr.csv")
OUT_SUM = os.path.join("output", "results", "Simulation", "sim_marginal_fdr.csv")

CELL_KEYS = ["n_iv", "ld", "pleio", "overlap"]
POS = ("A", "B")


def fdr_of(sub: pd.DataFrame) -> float:
    """Empirical FDR among positive calls (Grade A/B) within `sub`."""
    calls = sub[sub["grade"].isin(POS)]
    if len(calls) == 0:
        return np.nan
    return float(np.mean(calls["effect"] == 0))


def main() -> int:
    if not os.path.exists(REP_FILE):
        print("missing replicate table: %s" % REP_FILE)
        return 1

    df = pd.read_csv(REP_FILE)
    print("replicates: %d  (expected 43200)" % len(df))
    print("grade counts:", df["grade"].value_counts().to_dict())

    # ---------------- cell level ----------------
    rows = []
    for key, g in df.groupby(CELL_KEYS):
        n_iv, ld, pleio, overlap = key
        null = g[g["effect"] == 0]
        rows.append({
            "n_iv": n_iv, "ld": ld, "pleio": pleio, "overlap": overlap,
            "n_reps": len(g),
            "fdr_cell": fdr_of(g),
            "spec_D": float(np.mean(null["grade"] == "D")) if len(null) else np.nan,
            "p_A_null": float(np.mean(null["grade"] == "A")) if len(null) else np.nan,
            "p_AB_null": float(null["grade"].isin(POS).mean()) if len(null) else np.nan,
            "sens_008": float(g[g["effect"] == 0.08]["grade"].isin(POS).mean()),
            "sens_015": float(g[g["effect"] == 0.15]["grade"].isin(POS).mean()),
            "p_A_015": float(np.mean(g[g["effect"] == 0.15]["grade"] == "A")),
        })
    cell = pd.DataFrame(rows).sort_values(CELL_KEYS).reset_index(drop=True)
    cell.to_csv(OUT_CELL, index=False)

    # ---------------- regime level ----------------
    pub = {
        "none":        {"fdr_marginal": 0.000, "fdr_lo": 0.000, "fdr_hi": 0.000,
                        "spec": 1.000, "sens_015": 0.878, "sens_008": 0.216,
                        "pA_null": 0.000, "pA_015": 0.875},
        "balanced":    {"fdr_marginal": 0.100, "fdr_lo": 0.060, "fdr_hi": 0.145,
                        "spec": 0.796, "sens_015": 0.724, "sens_008": 0.376,
                        "pA_null": 0.061, "pA_015": 0.717},
        "directional": {"fdr_marginal": 0.151, "fdr_lo": 0.102, "fdr_hi": 0.200,
                        "spec": 0.679, "sens_015": 0.692, "sens_008": 0.408,
                        "pA_null": 0.046, "pA_015": 0.667},
    }
    # Values as revised (Table 2 of the revision, scored with the decisive-failure
    # cap). The pre-cap figures submitted with the original manuscript
    # (0.973 / 0.847 / 0.804 for sensitivity, 0.08 / 0.13 for FDR) are retained in
    # output/results/Simulation/_archive/ and compared in Supplementary Table S12.5.

    summ = []
    for pleio, g in df.groupby("pleio"):
        null = g[g["effect"] == 0]
        cells = cell[cell["pleio"] == pleio]
        rec = {
            "pleio": pleio,
            "fdr_pooled": fdr_of(g),
            "fdr_cellmean": float(cells["fdr_cell"].mean()),
            "fdr_cell_lo": float(cells["fdr_cell"].min()),
            "fdr_cell_hi": float(cells["fdr_cell"].max()),
            "spec_pooled": float(np.mean(null["grade"] == "D")),
            "spec_cellmean": float(cells["spec_D"].mean()),
            "spec_lo": float(cells["spec_D"].min()),
            "spec_hi": float(cells["spec_D"].max()),
            "sens008_pooled": float(g[g["effect"] == 0.08]["grade"].isin(POS).mean()),
            "sens008_cellmean": float(cells["sens_008"].mean()),
            "sens015_pooled": float(g[g["effect"] == 0.15]["grade"].isin(POS).mean()),
            "sens015_cellmean": float(cells["sens_015"].mean()),
            "sens015_lo": float(cells["sens_015"].min()),
            "sens015_hi": float(cells["sens_015"].max()),
            "pA_null_pooled": float(np.mean(null["grade"] == "A")),
            "pA015_pooled": float(np.mean(g[g["effect"] == 0.15]["grade"] == "A")),
            "pA015_cellmean": float(cells["p_A_015"].mean()),
            "pA015_lo": float(cells["p_A_015"].min()),
            "pA015_hi": float(cells["p_A_015"].max()),
        }
        rec.update({"pub_" + k: v for k, v in pub[pleio].items()})
        summ.append(rec)
    s = pd.DataFrame(summ)
    s.to_csv(OUT_SUM, index=False)

    # ---------------- comparison table ----------------
    pd.set_option("display.width", 200)
    print("\n=== FDR by definition vs published ===")
    show = s[["pleio", "fdr_pooled", "fdr_cellmean", "fdr_cell_lo", "fdr_cell_hi",
              "pub_fdr_marginal", "pub_fdr_lo", "pub_fdr_hi"]]
    print(show.to_string(index=False, float_format=lambda x: "%.3f" % x))

    print("\n=== other published quantities ===")
    for pleio in ["none", "balanced", "directional"]:
        r = s[s["pleio"] == pleio].iloc[0]
        print("\n-- %s --" % pleio)
        for label, got, exp in [
            ("spec (marginal)", r["spec_pooled"], r["pub_spec"]),
            ("sens @0.08", r["sens008_pooled"], r["pub_sens_008"]),
            ("sens @0.15", r["sens015_pooled"], r["pub_sens_015"]),
            ("P(A) at null", r["pA_null_pooled"], r["pub_pA_null"]),
            ("P(A) @0.15", r["pA015_pooled"], r["pub_pA_015"]),
        ]:
            flag = "OK " if abs(got - exp) <= 0.0055 else "DIFF"
            print("  %-16s computed=%.4f  published=%.3f  %s" % (label, got, exp, flag))
        print("  sens@0.15 range computed=[%.3f, %.3f] published=[0.61,1.00] (none only)"
              % (r["sens015_lo"], r["sens015_hi"]))
        print("  P(A)@0.15 range computed=[%.3f, %.3f] published text=[0.61,1.00] (none only)"
              % (r["pA015_lo"], r["pA015_hi"]))

    print("\nwrote: %s\nwrote: %s" % (OUT_CELL, OUT_SUM))
    return 0


if __name__ == "__main__":
    sys.exit(main())
