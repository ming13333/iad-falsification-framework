#!/usr/bin/env python3
"""Build Supplementary Table S11: instrument-tier sensitivity for insomnia -> AD.

Reads the archived instrument-sensitivity table (S2) and summarises the three
instrument sets used to answer the reviewer question "what happens to the IVW
estimate after LD correction". All numbers are derived from S2; nothing is
recomputed or re-fitted here, so S11 cannot drift from S2.

Outputs
  output/results/Validation/S11_instrument_tiers.csv
  manuscript/supplementary/S11_instrument_tiers.csv
"""
import os
import pandas as pd

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# Supplement location. The deposited layout is manuscript/supplementary; set
# IAD_SUPP_DIR to read and write somewhere else without editing the script.
SUPP = os.path.join(ROOT, os.environ.get("IAD_SUPP_DIR", "manuscript/supplementary"))
S2 = os.path.join(SUPP, "S2_instrument_sensitivity.csv")
OUT = os.path.join(ROOT, "output", "results", "Validation")

TIERS = [
    # NB: S2 carries two unclumped rows. The "G1 ... (unclumped)" row is the
    # multi-method MR fit (SE = 0.038); the main text quotes the UVMR fit
    # (SE = 0.031, P = 9.3e-4), so that row is the reference tier here.
    ("Unclumped", "None (genome-wide significant only)", "UVMR Insomnia -> AD (unclump2654)"),
    ("Loose",     "r2 < 0.1, 10,000 kb",                  "UVMR Insomnia -> AD (clump_loose)"),
    ("Tight",     "r2 < 0.001, 10,000 kb",                "UVMR Insomnia -> AD (clump_tight(42))"),
]


def main():
    s2 = pd.read_csv(S2)
    s2["analysis"] = s2["analysis"].astype(str).str.strip()
    rows = []
    for tier, clumping, key in TIERS:
        hit = s2[s2["analysis"] == key]
        if hit.empty:
            raise SystemExit(f"row not found in S2: {key}")
        r = hit.iloc[0]
        rows.append({
            "tier": tier,
            "clumping": clumping,
            "n_iv": int(r["n_snps"]),
            "beta": float(r["b_ivw"]),
            "se": float(r["se_ivw"]),
            "p": float(r["p_ivw"]),
        })

    base = rows[0]["se"]
    for r in rows:
        r["se_inflation_vs_unclumped"] = round(r["se"] / base, 2)
        r["direction"] = "positive" if r["beta"] > 0 else "negative"
        r["gate_g2"] = "Pass" if (r["p"] < 0.05 and r["beta"] > 0) else "Fail"

    df = pd.DataFrame(rows)[
        ["tier", "clumping", "n_iv", "beta", "se", "p",
         "se_inflation_vs_unclumped", "direction", "gate_g2"]]
    df.columns = ["Instrument tier", "Clumping", "n IV", "beta", "SE", "P",
                  "SE inflation vs unclumped", "Direction", "Gate G2"]

    os.makedirs(OUT, exist_ok=True)
    for path in [os.path.join(OUT, "S11_instrument_tiers.csv"),
                 os.path.join(SUPP, "S11_instrument_tiers.csv")]:
        df.to_csv(path, index=False, encoding="utf-8-sig")

    md = [
        "# Supplementary Table S11",
        "",
        "**Instrument-tier sensitivity of the insomnia -> AD IVW estimate.** "
        "All values are taken from Supplementary Table S2 (local harmonised "
        "summary statistics; Kunkle et al., 2019 outcome). SE inflation is the "
        "ratio of the clumped standard error to the unclumped standard error. "
        "No estimate was re-fitted for this table.",
        "",
        "| " + " | ".join(df.columns) + " |",
        "|" + "|".join(["---"] * len(df.columns)) + "|",
    ]
    for _, r in df.iterrows():
        md.append("| " + " | ".join([
            str(r["Instrument tier"]), str(r["Clumping"]), str(r["n IV"]),
            f"{r['beta']:+.3f}", f"{r['SE']:.3f}", f"{r['P']:.3g}",
            f"{r['SE inflation vs unclumped']:.2f}x", str(r["Direction"]),
            str(r["Gate G2"]),
        ]) + " |")
    md += [
        "",
        "**Notes.** (1) The tight tier is defined by r2 < 0.001 clumping at a "
        "10,000-kb window, which leaves 42 loci; 37 variants remain after "
        "harmonisation and the 5,000-kb window reported in the main text. "
        "(2) Gate G2 requires a clumped IVW estimate that remains significant "
        "in the claimed direction, so no tier passes. (3) The unclumped "
        "estimate is shown for reference only; correlated instruments violate "
        "the independence assumption and its standard error is not "
        "interpretable as sampling precision.",
        "",
    ]
    with open(os.path.join(SUPP, "S11_instrument_tiers.md"), "w",
              encoding="utf-8") as fh:
        fh.write("\n".join(md))

    print(df.to_string(index=False))
    print("\nwritten:", os.path.join(SUPP, "S11_instrument_tiers.md"))


if __name__ == "__main__":
    main()
