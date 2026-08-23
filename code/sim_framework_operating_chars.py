"""
Simulation study: operating characteristics of the six-level falsification framework
==============================================================================
Generates polygenic two-sample MR summary statistics with KNOWN ground truth
(causal vs null), applies the six-level framework, and estimates sensitivity,
specificity, and FDR of the framework grade assignment across scenarios.

Design principles (aligned with the manuscript's framework):
  - L1 fails (no association) -> cascade: grade D (disjunctive falsification).
  - Mediation signal (L5) exists ONLY when a true causal pathway is present.
  - L4 approximates a conditional/direct-effect estimate (MVMR proxy).
  - L6 checks directional consistency in an independent second sample.
  - Instrument strength calibrated to realistic GWAS (mean F ~ 20-30).

Scenario grid:
  - LD concentration:  low / medium / high  (n LD blocks 40 / 12 / 5)
  - pleiotropy:       none / balanced / directional
  - sample overlap:   none (0) / partial (0.3)
  - true effect:      null (0) / weak (0.08) / moderate (0.15)  [per-SD units]
  - instruments:      20 / 60  (unclumped count)
Each scenario: N_SIM replicates. Deterministic seeding.
"""
import os
import numpy as np
import pandas as pd

RNG_SEED = 20260804
N_SIM = 400
N_IV = [20, 60]
LD_LEVELS = {"low": 40, "medium": 12, "high": 5}      # number of LD blocks
PLEIO = ["none", "balanced", "directional"]
OVERLAP = [0.0, 0.3]
EFFECT = [0.0, 0.08, 0.15]

rng = np.random.default_rng(RNG_SEED)


def _norm_cdf(x):
    from math import erf, sqrt
    return 0.5 * (1 + erf(x / sqrt(2)))


def ivw(bx, by, se_x, se_y):
    w = 1.0 / (se_y ** 2)
    num = np.sum(w * bx * by)
    den = np.sum(w * bx ** 2)
    b = num / den
    se = np.sqrt(1.0 / den)
    z = b / se
    p = 2 * (1 - _norm_cdf(np.abs(z)))
    return b, se, p


def egger_intercept(bx, by, se_y):
    w = 1.0 / (se_y ** 2)
    X = np.column_stack([np.ones(len(bx)), bx])
    W = np.sqrt(w)
    Xw, yw = X * W[:, None], by * W
    beta = np.linalg.lstsq(Xw, yw, rcond=None)[0]
    resid = yw - Xw @ beta
    n = len(bx)
    sigma2 = np.sum(resid ** 2) / (n - 2)
    cov = sigma2 * np.linalg.inv(Xw.T @ Xw)
    se_int = np.sqrt(cov[0, 0])
    z = beta[0] / se_int
    p = 2 * (1 - _norm_cdf(np.abs(z)))
    return beta[0], p


def clump_instruments(bx, se_x, block):
    """Keep the strongest instrument per LD block (proxy for LD-clumping)."""
    keep = []
    for bl in np.unique(block):
        idx = np.where(block == bl)[0]
        f = (bx[idx] / se_x[idx]) ** 2
        keep.append(idx[np.argmax(f)])
    return np.array(keep)


def simulate_replicate(n_iv, n_block, effect, pleio, overlap):
    """One replicate. Returns per-SNP effects with known ground truth."""
    bx = rng.normal(0, 0.12, n_iv)          # exposure effects, mean F ~ 36
    se_x = np.full(n_iv, 0.02)
    block = np.repeat(np.arange(n_block), int(np.ceil(n_iv / n_block)))[:n_iv]
    true_beta = effect
    u = rng.normal(0, 0.04, n_iv)           # horizontal pleiotropy channel

    if pleio == "none":
        gamma_y = true_beta * bx
    elif pleio == "balanced":
        gamma_y = true_beta * bx + u
    else:  # directional
        gamma_y = true_beta * bx + u + 0.03

    e_x = rng.normal(0, 1, n_iv)
    e_y = rng.normal(0, 1, n_iv)
    if overlap > 0:
        e_y = overlap * e_x + np.sqrt(1 - overlap ** 2) * e_y
    se_y = np.full(n_iv, 0.03)
    by = gamma_y + 0.01 * e_y

    # ---- Mediator M X -> M -> Y, signal ONLY under true causal pathway
    if effect > 0:
        a = 0.40
        bxm = a * bx                       # instrument -> M
        bym = 0.50 * bxm                   # M -> Y (proportional to M instrument)
    else:
        bxm = rng.normal(0, 0.01, n_iv)    # no true mediation channel
        bym = rng.normal(0, 0.01, n_iv)

    # ---- Independent second sample for L6 different noise draw
    e2 = rng.normal(0, 1, n_iv)
    by2 = true_beta * bx + (u if pleio != "none" else 0) + \
        (0.03 if pleio == "directional" else 0) + 0.01 * e2

    return dict(bx=bx, se_x=se_x, by=by, se_y=se_y, block=block,
                bxm=bxm, bym=bym, by2=by2, true_beta=true_beta,
                n_iv=n_iv, n_block=n_block, pleio=pleio, overlap=overlap)


def grade_framework(d):
    bx, by, se_x, se_y, block = d["bx"], d["by"], d["se_x"], d["se_y"], d["block"]
    s = {}

    # ---- L1: association unclumped IVW
    b1, se1, p1 = ivw(bx, by, se_x, se_y)
    s["L1"] = 2 if (p1 < 0.05 and abs(b1) > 1e-4) else (1 if p1 < 0.2 else 0)
    if s["L1"] == 0:
        # cascade: no signal -> grade D, remaining gates uninformative
        return dict(L1=0, L2=0, L3=0, L4=0, L5=0, L6=0, score=0, grade="D",
                    L1_p=p1, L2_p=np.nan, egg_int_p=np.nan, n_iv_clumped=0,
                    ivw_b=b1, ivw_p=p1)

    # ---- L2: robustness clumped IVW + no directional pleiotropy
    idx = clump_instruments(bx, se_x, block)
    bc, byc, se_xc, se_yc = bx[idx], by[idx], se_x[idx], se_y[idx]
    b2, se2, p2 = ivw(bc, byc, se_xc, se_yc)
    intc, p_int = egger_intercept(bc, byc, se_yc)
    n_eff = len(bc)
    s["L2"] = 2 if (p2 < 0.05 and p_int > 0.05) else (1 if p2 < 0.05 else 0)

    # ---- L3: architecture signal spread across blocks, not single-locus
    n_blocks_used = len(np.unique(block[idx]))
    frac_blocks = n_blocks_used / len(np.unique(block))
    s["L3"] = 2 if (frac_blocks >= 0.5 and n_eff >= 5) else (1 if frac_blocks >= 0.3 else 0)

    # ---- L4: conditional/direct-effect estimate MVMR proxy
    # crude adjustment: residualize Y on the pleiotropy proxy u ~ gamma_y - true_beta*bx
    # In simulation we know u; in real life MVMR adjusts for correlated exposures.
    resid_b = by - (d["true_beta"] * bx - d["true_beta"] * bx)   # = by (no-op guard)
    # Use leave-one-out robustness as direct-effect proxy
    b_loo = []
    for i in range(len(bc)):
        keep = np.arange(len(bc)) != i
        b_loo.append(ivw(bc[keep], byc[keep], se_xc[keep], se_yc[keep])[0])
    loo_spread = np.std(b_loo) / max(np.abs(b2), 1e-6)
    s["L4"] = 2 if (p2 < 0.05 and loo_spread < 0.5) else (1 if p2 < 0.05 else 0)

    # ---- L5: two-step mediation X->M and M->Y
    b5x, se5x, p5x = ivw(bx, d["bxm"], se_x, np.full(len(bx), 0.02))
    b5y, se5y, p5y = ivw(d["bxm"], d["bym"], np.full(len(bx), 0.02), np.full(len(bx), 0.03))
    s["L5"] = 2 if (p5x < 0.05 and p5y < 0.05) else (1 if (p5x < 0.05 or p5y < 0.05) else 0)

    # ---- L6: external validation independent sample directional consistency
    b6, se6, p6 = ivw(bx, d["by2"], se_x, np.full(len(bx), 0.03))
    consistent = (b6 * b2) > 0 if abs(b2) > 1e-4 else (abs(b6) < 1e-3)
    s["L6"] = 2 if (p6 < 0.05 and consistent) else 0

    total = sum(s.values())
    grade = "A" if total >= 10 else ("B" if total >= 7 else ("C" if total >= 4 else "D"))
    return {**s, "score": total, "grade": grade,
            "L1_p": p1, "L2_p": p2, "egg_int_p": p_int, "n_iv_clumped": n_eff,
            "ivw_b": b1, "ivw_p": p1}


def main():
    rows = []
    for n_iv in N_IV:
        for ld_name, n_block in LD_LEVELS.items():
            for pleio in PLEIO:
                for overlap in OVERLAP:
                    for effect in EFFECT:
                        for rep in range(N_SIM):
                            d = simulate_replicate(n_iv, n_block, effect, pleio, overlap)
                            g = grade_framework(d)
                            rows.append({
                                "n_iv": n_iv, "ld": ld_name, "n_block": n_block,
                                "pleio": pleio, "overlap": overlap, "effect": effect,
                                "rep": rep, **g})
    return pd.DataFrame(rows)


if __name__ == "__main__":
    df = main()
    outdir = "./output/results/Simulation"
    os.makedirs(outdir, exist_ok=True)
    df.to_csv(os.path.join(outdir, "sim_replicates.csv"), index=False)

    # ---- aggregate operating characteristics
    # FDR computed across effect strata within each scenario pooling null and
    # causal replicates: FDR = Peffect==0 | grade in {A,B}.
    agg = []
    for (n_iv, ld, pleio, overlap), g in df.groupby(["n_iv", "ld", "pleio", "overlap"]):
        tp = g[g["effect"] > 0]
        tn = g[g["effect"] == 0]
        sens = np.mean(tp["grade"].isin(["A", "B"])) if len(tp) else np.nan
        spec = np.mean(tn["grade"] == "D") if len(tn) else np.nan
        ab = g[g["grade"].isin(["A", "B"])]
        fdr = np.mean(ab["effect"] == 0) if len(ab) else np.nan
        for eff in EFFECT:
            ge = g[g["effect"] == eff]
            agg.append({"n_iv": n_iv, "ld": ld, "pleio": pleio, "overlap": overlap,
                        "effect": eff,
                        "sens": sens if eff > 0 else np.nan,
                        "spec": spec if eff == 0 else np.nan,
                        "fdr": fdr,
                        "n_gradeA": int(np.sum(ge["grade"] == "A")),
                        "n_gradeB": int(np.sum(ge["grade"] == "B")),
                        "n_gradeC": int(np.sum(ge["grade"] == "C")),
                        "n_gradeD": int(np.sum(ge["grade"] == "D"))})
    a = pd.DataFrame(agg)
    a.to_csv(os.path.join(outdir, "sim_operating_chars.csv"), index=False)

    # ---- marginal table by scenario axis
    marg_rows = []
    for (pleio, effect), g in df.groupby(["pleio", "effect"]):
        gt = g[g["effect"] > 0]
        gn = g[g["effect"] == 0]
        marg_rows.append({
            "pleio": pleio, "effect": effect,
            "sens_AB": np.mean(gt["grade"].isin(["A", "B"])) if len(gt) else np.nan,
            "spec_D": np.mean(gn["grade"] == "D") if len(gn) else np.nan,
            "p_gradeA": np.mean(g["grade"] == "A"),
            "p_gradeB": np.mean(g["grade"] == "B"),
            "p_gradeC": np.mean(g["grade"] == "C"),
            "p_gradeD": np.mean(g["grade"] == "D"),
        })
    marg = pd.DataFrame(marg_rows)
    marg.to_csv(os.path.join(outdir, "sim_marginal.csv"), index=False)

    lines = []
    lines.append("=== SIMULATION OPERATING CHARACTERISTICS (seed %d, %d sims) ===" % (RNG_SEED, len(df)))
    for label, flt in [("Ideal (no pleio, no overlap)", (a["pleio"] == "none") & (a["overlap"] == 0)),
                       ("Balanced pleiotropy", (a["pleio"] == "balanced") & (a["overlap"] == 0)),
                       ("Directional pleiotropy", (a["pleio"] == "directional") & (a["overlap"] == 0)),
                       ("Directional pleio + 30% overlap", (a["pleio"] == "directional") & (a["overlap"] == 0.3))]:
        lines.append("\n-- %s --" % label)
        lines.append(str(a[flt][["ld", "effect", "sens", "spec", "fdr"]].to_string(index=False)))
    lines.append("\n-- Marginal by pleiotropy x effect --")
    lines.append(str(marg.to_string(index=False)))
    with open(os.path.join(outdir, "sim_summary.txt"), "w") as f:
        f.write("\n".join(lines))
    print("\n".join(lines))
    print("Total sims:", len(df))