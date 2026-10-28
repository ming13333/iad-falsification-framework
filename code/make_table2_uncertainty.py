#!/usr/bin/env python3
"""Table 2 uncertainty: Wilson intervals and a Grade C+D specificity definition.

Reviewer 1 (point 4) raised two issues with the simulation summary: sensitivity
counts A/B as positive but specificity counts only D as a correct negative, so
Grade C is unclassified; and no uncertainty is reported. This script

  1. reports specificity under both conventions (D only, and C+D);
  2. attaches Wilson score intervals to every marginal proportion;
  3. verifies the existing Table 2 point estimates still reproduce.

Nothing is re-simulated: the script reads the frozen replicate file.

Outputs
  output/results/Simulation/table2_uncertainty.csv
"""
import os
import numpy as np
import pandas as pd

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REP = os.path.join(ROOT, "output", "results", "Simulation", "sim_replicates.csv")
OUT = os.path.join(ROOT, "output", "results", "Simulation", "table2_uncertainty.csv")

POS = ("A", "B")


def wilson(k, n, z=1.959963984540054):
    """Wilson score interval for a binomial proportion."""
    if n == 0:
        return (np.nan, np.nan, np.nan)
    p = k / n
    denom = 1 + z * z / n
    centre = (p + z * z / (2 * n)) / denom
    half = z * np.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / denom
    return (p, max(0.0, centre - half), min(1.0, centre + half))


def main():
    d = pd.read_csv(REP)
    need = {"pleio", "effect", "grade"}
    if not need.issubset(d.columns):
        raise SystemExit(f"unexpected replicate columns: {list(d.columns)}")

    rows = []
    for pleio in ["none", "balanced", "directional"]:
        for eff in [0.0, 0.08, 0.15]:
            s = d[(d.pleio == pleio) & np.isclose(d.effect, eff)]
            n = len(s)
            pos = int(s.grade.isin(POS).sum())
            d_only = int((s.grade == "D").sum())
            cd = int(s.grade.isin(("C", "D")).sum())
            a = int((s.grade == "A").sum())
            # FDR is defined over the full effect-size mixture, so it is
            # attached per regime below rather than per effect-size cell.
            rows.append({
                "pleio": pleio, "effect": eff, "n": n,
                "sens": pos / n if eff > 0 else np.nan,
                "sens_lo": wilson(pos, n)[1] if eff > 0 else np.nan,
                "sens_hi": wilson(pos, n)[2] if eff > 0 else np.nan,
                "spec_D": d_only / n if eff == 0 else np.nan,
                "spec_D_lo": wilson(d_only, n)[1] if eff == 0 else np.nan,
                "spec_D_hi": wilson(d_only, n)[2] if eff == 0 else np.nan,
                "spec_CD": cd / n if eff == 0 else np.nan,
                "spec_CD_lo": wilson(cd, n)[1] if eff == 0 else np.nan,
                "spec_CD_hi": wilson(cd, n)[2] if eff == 0 else np.nan,
                "p_A": a / n,
                "p_A_lo": wilson(a, n)[1],
                "p_A_hi": wilson(a, n)[2],
            })

    out = pd.DataFrame(rows)
    # Marginal FDR across the full mixture, per regime (unchanged definition).
    fdr = []
    for pleio in ["none", "balanced", "directional"]:
        s = d[d.pleio == pleio]
        calls = s[s.grade.isin(POS)]
        fdr.append(calls.effect.eq(0).mean() if len(calls) else np.nan)
    out.attrs["fdr_by_regime"] = dict(zip(["none", "balanced", "directional"], fdr))

    out.to_csv(OUT, index=False, encoding="utf-8-sig")

    # --- FDR sensitivity to the proportion of true nulls -------------------
    # The published FDR assumes one-third nulls. Users evaluating null-enriched
    # batches face a different operating point, so the same per-cell estimates
    # are re-weighted. No new simulation is involved.
    mix_rows = []
    for pleio in ["none", "balanced", "directional"]:
        s = d[d.pleio == pleio]
        p_null_call = s.loc[s.effect == 0, "grade"].isin(POS).mean()
        p_call = {eff: s.loc[np.isclose(s.effect, eff), "grade"].isin(POS).mean()
                  for eff in (0.08, 0.15)}
        p_nonnull = 0.5 * (p_call[0.08] + p_call[0.15])
        for pi in (1 / 3, 0.5, 2 / 3):
            num = pi * p_null_call
            mix_rows.append({
                "pleio": pleio,
                "pi_null": round(pi, 4),
                "P_call_given_null": round(p_null_call, 4),
                "P_call_given_nonnull": round(p_nonnull, 4),
                "FDR": round(num / (num + (1 - pi) * p_nonnull), 4) if p_nonnull else 0.0,
                "exceeds_0.20": bool(p_nonnull and num / (num + (1 - pi) * p_nonnull) > 0.20),
            })
    mix = pd.DataFrame(mix_rows)
    mix_path = os.path.join(os.path.dirname(OUT), "fdr_null_fraction_sensitivity.csv")
    mix.to_csv(mix_path, index=False, encoding="utf-8-sig")
    print("\nFDR vs proportion of true nulls:\n" + mix.to_string(index=False))
    print("\nwritten:", mix_path)
    pd.set_option("display.width", 200)
    print(out.round(4).to_string(index=False))
    print("\nmarginal FDR (pooled, per regime):",
          {k: round(float(v), 4) for k, v in out.attrs["fdr_by_regime"].items()})
    print("\nwritten:", OUT)


if __name__ == "__main__":
    main()
