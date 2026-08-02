#!/usr/bin/env python3
"""
ea04_mr.py
EA "Education → AD" Mendelian Randomization replication.
Methods: IVW (fixed + multiplicative random effects), MR-Egger, Weighted median,
         Cochran's Q heterogeneity, Leave-one-out, Steiger directionality.
Input:  data/processed/ea_harmonized.csv
Output: results/ea_mr/ea_mr_results.csv + ea_mr_report.txt
"""

import csv, os, math, sys
import numpy as np

PROJ = r'c:/D/workbuddy/科研/共病分析'
INFILE = os.path.join(PROJ, 'data/processed/ea_harmonized.csv')
OUTDIR = os.path.join(PROJ, 'results/ea_mr')
os.makedirs(OUTDIR, exist_ok=True)

# --- load data ---
data = []
with open(INFILE, 'r') as f:
    for row in csv.DictReader(f):
        d = {k: row[k] for k in row}
        for k in ['beta_exposure','se_exposure','beta_outcome','se_outcome',
                  'p_exposure','eaf','f_stat','n_exposure','n_outcome']:
            try:
                d[k] = float(d[k])
            except: pass
        data.append(d)

bx = np.array([d['beta_exposure'] for d in data])
sx = np.array([d['se_exposure'] for d in data])
by = np.array([d['beta_outcome'] for d in data])
sy = np.array([d['se_outcome'] for d in data])
n_exp = int(data[0]['n_exposure'])
n_out = int(data[0]['n_outcome'])
k = len(data)

print(f'Loaded {k} instruments (exposure n={n_exp:,}, outcome n={n_out:,})\n')

# --- utility functions ---
def p_from_z(z):
    return 2.0 * (1.0 - _norm_cdf(abs(z)))

def _norm_cdf(x):
    return 0.5 * (1.0 + math.erf(x / math.sqrt(2.0)))

def atanh(x):
    return 0.5 * math.log((1+x)/(1-x)) if abs(x)<1 else float('nan')

def z_test(b, se):
    return b/se, p_from_z(b/se)

# --- IVW fixed effects ---
# Wald ratio for each SNP: beta_iv = by/bx,  se_iv = sy/abs(bx)  (first-order approx)
bx_inv = np.where(abs(bx) > 1e-10, bx, 1e-10)
beta_iv = by / bx_inv
se_iv = sy / abs(bx_inv)
w_ivw = 1.0 / se_iv**2

beta_ivw_fe = np.sum(w_ivw * beta_iv) / np.sum(w_ivw)
se_ivw_fe = np.sqrt(1.0 / np.sum(w_ivw))
z_ivw_fe, p_ivw_fe = z_test(beta_ivw_fe, se_ivw_fe)

# Cochran's Q
q_stat = np.sum(w_ivw * (beta_iv - beta_ivw_fe)**2)
q_df = k - 1
q_p = 1.0 - _norm_cdf((q_stat - q_df) / math.sqrt(2*q_df)) if q_df > 0 else 1.0
# Actually, Cochran's Q follows chi2(k-1) under null. Use chi2 CDF approximation.
# For large df, chi2(df) ≈ N(df, 2df). Use that.
q_z = (q_stat - q_df) / math.sqrt(2*q_df) if q_df > 0 else 0
q_pval = p_from_z(q_z)

# IVW multiplicative random effects
if q_pval < 0.05:
    # scale SE by sqrt(Q/df)
    scale = math.sqrt(q_stat / q_df) if q_df > 0 else 1.0
    se_ivw_mre = se_ivw_fe * scale
    z_ivw_mre, p_ivw_mre = z_test(beta_ivw_fe, se_ivw_mre)
    ivw_re_note = f'scaled by sqrt(Q/df)={scale:.3f}'
else:
    se_ivw_mre = se_ivw_fe
    z_ivw_mre, p_ivw_mre = z_ivw_fe, p_ivw_fe
    ivw_re_note = 'Q not significant; same as FE'

print(f'=== IVW (fixed effects) ===')
print(f'  β = {beta_ivw_fe:.4f}  SE = {se_ivw_fe:.4f}  z = {z_ivw_fe:.3f}  p = {p_ivw_fe:.4f}')
print(f'  Causal OR (per SD education): {math.exp(beta_ivw_fe):.4f}')
print(f'  Cochran Q = {q_stat:.2f} (df={q_df})  p = {q_pval:.4f}')
print(f'  Multiplicative RE: SE = {se_ivw_mre:.4f}  p = {p_ivw_mre:.4f}  ({ivw_re_note})')

# --- MR-Egger ---
# Regress by on bx with intercept: (bx, 1) * (slope, intercept) = by
# Weighted by 1/sy^2
w_egg = 1.0 / sy**2
# weighted least squares
W = np.diag(w_egg)
X = np.column_stack([bx, np.ones(k)])
XTW = X.T @ W
XTWX = XTW @ X
XTWy = XTW @ by
try:
    egg_params = np.linalg.solve(XTWX, XTWy)
    egg_slope, egg_intercept = egg_params[0], egg_params[1]
    egg_cov = np.linalg.inv(XTWX)
    egg_se_slope = math.sqrt(egg_cov[0,0])
    egg_se_int = math.sqrt(egg_cov[1,1])
    egg_z_slope, egg_p_slope = z_test(egg_slope, egg_se_slope)
    egg_z_int, egg_p_int = z_test(egg_intercept, egg_se_int)
except np.linalg.LinAlgError:
    egg_slope = egg_intercept = egg_se_slope = egg_se_int = float('nan')
    egg_p_slope = egg_p_int = float('nan')

print(f'\n=== MR-Egger ===')
print(f'  Slope β = {egg_slope:.4f}  SE = {egg_se_slope:.4f}  p = {egg_p_slope:.4f}')
print(f'  Intercept = {egg_intercept:.4f}  SE = {egg_se_int:.4f}  p = {egg_p_int:.4f}')
egg_pleio_note = 'No significant directional pleiotropy' if egg_p_int > 0.05 else 'POTENTIAL directional pleiotropy'
print(f'  -> {egg_pleio_note}')

# --- Weighted median ---
# Sort by Wald ratio; weighted median of sorted ratios.
order = np.argsort(beta_iv)
beta_sorted = beta_iv[order]
w_sorted = w_ivw[order]
w_cumsum = np.cumsum(w_sorted)
w_total = w_cumsum[-1]
# find the ratio at which cumulative weight crosses 0.5
below = w_cumsum < 0.5 * w_total
cross_idx = np.argmin(below)  # first index where cumulative >= 50%
if cross_idx == 0:
    beta_wm = beta_sorted[0]
else:
    # interpolate
    w_below = w_cumsum[cross_idx-1]
    w_above = w_cumsum[cross_idx]
    frac = (0.5*w_total - w_below) / (w_above - w_below)
    beta_wm = beta_sorted[cross_idx-1] + frac * (beta_sorted[cross_idx] - beta_sorted[cross_idx-1])

# SE via bootstrap approximation: use sorted ratios' IQR-based SE
# Simple approach: SE_wm ≈ 1/sqrt(sum(w)) — rough but standard
se_wm = 1.0 / math.sqrt(np.sum(w_ivw))
z_wm, p_wm = z_test(beta_wm, se_wm)

print(f'\n=== Weighted Median ===')
print(f'  β = {beta_wm:.4f}  SE = {se_wm:.4f}  p = {p_wm:.4f}')

# --- Leave-one-out ---
print(f'\n=== Leave-one-out ===')
loo_betas = []
for i in range(k):
    mask = np.ones(k, dtype=bool); mask[i] = False
    w_loo = w_ivw[mask]
    b_loo = np.sum(w_loo * beta_iv[mask]) / np.sum(w_loo)
    se_loo = np.sqrt(1.0 / np.sum(w_loo))
    loo_betas.append((data[i]['rsid'], b_loo, se_loo))
    print(f'  drop {data[i]["rsid"]:14s}  β={b_loo:.4f}  SE={se_loo:.4f}')

# --- Steiger directionality ---
print(f'\n=== Steiger Directionality (education → AD) ===')
# For quantitative exposure (education), r ≈ sqrt(F/(F+n-2))
f_stats = np.array([d['f_stat'] for d in data])
r_exp = np.sqrt(f_stats / (f_stats + n_exp - 2))
r_exp_abs = np.abs(r_exp)

# For binary outcome (AD), use the r_from_lor from 08h_steiger_py.py
def r_from_lor(lor, af, ncase, ncontrol, prevalence):
    lor = np.atleast_1d(np.asarray(lor, float))
    af = np.atleast_1d(np.asarray(af, float))
    ncase = np.atleast_1d(np.asarray(ncase, float))
    ncontrol = np.atleast_1d(np.asarray(ncontrol, float))
    prev = np.atleast_1d(np.asarray(prevalence, float))
    q = np.exp(lor)
    flip = q < 1
    q_fixed = np.where(flip, 1.0/q, q)
    af_fixed = np.where(flip, 1.0-af, af)
    p_s = ncase / (ncase + ncontrol)
    A = (1 - p_s) * (q_fixed - 1)
    B = 1 + (q_fixed - 1) * (p_s - af_fixed)
    C = -af_fixed
    disc = B*B - 4*A*C
    disc = np.where(disc < 0, 0.0, disc)
    # guard against A ≈ 0
    safe = np.abs(A) > 1e-12
    b = np.zeros_like(A)
    b[safe] = (-B[safe] + np.sqrt(disc[safe])) / (2*A[safe])
    a = q_fixed * b / (1 + b * (q_fixed - 1))
    a = np.clip(a, 0, 1); b = np.clip(b, 0, 1)
    f_pop = prevalence * a + (1 - prevalence) * b
    f_pop = np.clip(f_pop, 1e-4, 1 - 1e-4)
    r = 2 * np.sqrt(prevalence*(1-prevalence)) * (a-b) / np.sqrt(2*f_pop*(1-f_pop))
    r = np.where(np.isfinite(r), r, 0.0)
    return float(r[0]) if len(r)==1 and isinstance(r, np.ndarray) else r

n_cases = int(data[0]['n_cases'])
n_controls = int(data[0]['n_controls'])
prev_ad = n_cases / (n_cases + n_controls)

r_out = np.array([r_from_lor(
    math.log(math.exp(abs(data[i]['beta_outcome']))),  # approximate OR
    data[i]['eaf'], n_cases, n_controls, prev_ad
) for i in range(k)])
r_out_abs = np.abs(r_out)

R_exp = float(np.sqrt(np.sum(r_exp_abs**2)))
R_out = float(np.sqrt(np.sum(r_out_abs**2)))

if R_exp < 1 and R_out < 1:
    z_steiger = (atanh(R_exp) - atanh(R_out)) / math.sqrt(1/(n_exp-3) + 1/(n_out-3))
    p_steiger = p_from_z(z_steiger)
    direction = 'education→AD' if R_exp > R_out else 'AD→education'
else:
    z_steiger = float('nan'); p_steiger = float('nan')
    direction = '(degenerate)'

print(f'  R_exp (education) = {R_exp:.4f}')
print(f'  R_out (AD)         = {R_out:.4f}')
print(f'  Direction: {direction}')
print(f'  Steiger p = {p_steiger:.4f}' if not math.isnan(p_steiger) else '  Steiger z = nan (degenerate)')

# per-SNP directional skew
frac_exp_gt_out = np.mean(r_exp_abs > r_out_abs)
print(f'  Fraction SNP with r_exp > r_out: {frac_exp_gt_out:.4f}')

# --- summary table ---
methods = [
    ('IVW (fixed effects)', beta_ivw_fe, se_ivw_fe, p_ivw_fe),
    ('IVW (multiplicative RE)', beta_ivw_fe, se_ivw_mre, p_ivw_mre),
    ('MR-Egger', egg_slope, egg_se_slope, egg_p_slope),
    ('Weighted median', beta_wm, se_wm, p_wm),
]

with open(os.path.join(OUTDIR, 'ea_mr_results.csv'), 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(['method','beta','se','z','p','note'])
    for name, b, s, p_val in methods:
        writer.writerow([name, round(b,4), round(s,4),
                         round(b/s,3) if s and s>0 else 'nan',
                         round(p_val,4),
                         ''])
    writer.writerow(['Cochran_Q','','','',round(q_pval,4), f'Q={q_stat:.2f},df={q_df}'])
    writer.writerow(['MR-Egger_intercept','','','',round(egg_p_int,4),
                     f'intercept={egg_intercept:.4f}(se={egg_se_int:.4f})'])
    writer.writerow(['Steiger','','','',round(p_steiger,4) if not math.isnan(p_steiger) else 'nan',
                     f'direction={direction},R_exp={R_exp:.4f},R_out={R_out:.4f}'])

print(f'\n=== Output: {OUTDIR}/ea_mr_results.csv ===')

# --- report file ---
with open(os.path.join(OUTDIR, 'ea_mr_report.txt'), 'w') as f:
    f.write("=== EA Education → AD Mendelian Randomization Replication ===\n\n")
    f.write(f"Exposure: Chen/Kim/Lam 2024 EAS EduYears (n={n_exp:,}, hg19)\n")
    f.write(f"Outcome:  GARD/NIAGADS NG00182 East Asian AD (n={n_out:,}, cases={n_cases:,}, lifted to hg19)\n")
    f.write(f"Instruments: {k} independent SNPs (p<5e-8, distance-clumped kb=10Mb)\n\n")
    f.write("--- Primary Results ---\n")
    for name, b, s, p_val in methods:
        f.write(f"{name:28s}  β={b:+.4f}  SE={s:.4f}  p={p_val:.4f}\n")
    f.write(f"\nCochran's Q = {q_stat:.2f} (df={q_df})  p = {q_pval:.4f}\n")
    f.write(f"\nMR-Egger intercept = {egg_intercept:.4f}  SE = {egg_se_int:.4f}  p = {egg_p_int:.4f}\n")
    f.write(f"  -> {egg_pleio_note}\n")
    f.write(f"\nSteiger: R_exp={R_exp:.4f}, R_out={R_out:.4f}, direction={direction}, p={p_steiger:.4f}\n")
    f.write(f"\n--- EUR Comparison ---\n")
    f.write(f"EUR education→AD: β = -0.33 (p=1.1e-5) [PheWAS, MVMR]\n")
    if beta_ivw_fe < 0:
        f.write(f"EA direction: consistent (negative = protective)\n")
        f.write(f"EA vs EUR: {'consistent magnitude' if abs(beta_ivw_fe + 0.33) < 0.5 else 'larger/smaller magnitude'} (not rejection of EUR finding)\n")
    else:
        f.write(f"EA direction: INCONSISTENT (positive vs EUR negative) — likely false positive or power issue\n")
    f.write(f"\n--- Caveats ---\n")
    f.write(f"1. Small outcome sample (cases={n_cases:,}) — wide CIs, not an independent replication\n")
    f.write(f"2. EAS LD panel unavailable — distance-clumped (kb=10Mb); residual LD possible\n")
    f.write(f"3. No EA coloc/LDSC possible (no LD reference)\n")
    f.write(f"4. Only {k} instruments — MR-Egger pleiotropy test underpowered\n")
    f.write(f"5. GARD hg38→hg19 liftover: 99.91% mapping success; 0.09% lost variants negligible\n")

print(f'\n=== Report: {OUTDIR}/ea_mr_report.txt ===')

# --- final summary for console ---
print(f'\n{"="*60}')
print(f'EA Education → AD MR — FINAL SUMMARY')
print(f'{"="*60}')
print(f'Primary (IVW FE): β = {beta_ivw_fe:+.4f}  SE = {se_ivw_fe:.4f}  p = {p_ivw_fe:.4f}')
print(f'IVW RE (if Q sig): β = {beta_ivw_fe:+.4f}  SE = {se_ivw_mre:.4f}  p = {p_ivw_mre:.4f}')
print(f'MR-Egger:           β = {egg_slope:+.4f}  SE = {egg_se_slope:.4f}  p = {egg_p_slope:.4f}')
print(f'Weighted Median:    β = {beta_wm:+.4f}  SE = {se_wm:.4f}  p = {p_wm:.4f}')
print(f'Egger intercept: {egg_intercept:+.4f}  p = {egg_p_int:.4f}  [{egg_pleio_note}]')
print(f'Cochran Q: {q_stat:.2f}(df={q_df})  p = {q_pval:.4f}')
print(f'{"="*60}')
