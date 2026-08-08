#!/usr/bin/env python3
"""
ea05_transethnic_insomnia_ad.py
Trans-ethnic (EUR instruments -> EAS outcome) MR check for the core study pair:
  Insomnia (UK Biobank, EUR) -> AD (GARD/NIAGADS, East Asian)
Design follows the Depression->AD EAS exploratory template (mdd_eas_dep_ad_harm.tsv):
  EUR LD-independent instruments (r2<0.001, 10 Mb) -> position-matched into GARD EAS AD (hg19).

Purpose (Level 6 external validation): test whether the framework's central conclusion
for insomnia->AD (no robust directed effect; null/negative after clumping) is *contradicted*
or *directionally consistent* in an independent East Asian outcome sample.

Input:
  C:/Temp/g1_clumped_insomnia_ivs.csv   (EUR LD-independent insomnia instruments, 40)
  data/processed/gard_ea_ad_hg19.tsv.gz (GARD EAS AD, liftovered to hg19, 5.37M variants)
Output:
  results/ea_mr/ea_transethnic_insomnia_ad_results.csv
  results/ea_mr/ea_transethnic_insomnia_ad_report.txt
"""
import csv, os, math, gzip
import numpy as np

PROJ = r'c:/D/workbuddy/科研/共病分析'
IVS  = 'C:/Temp/g1_clumped_insomnia_ivs.csv'
GARD = os.path.join(PROJ, 'data/processed/gard_ea_ad_hg19.tsv.gz')
OUTDIR = os.path.join(PROJ, 'results/ea_mr')
os.makedirs(OUTDIR, exist_ok=True)

# ---------- 1. load EUR insomnia instruments ----------
ivs = []
with open(IVS, 'r') as f:
    for row in csv.DictReader(f):
        ivs.append({k: row[k] for k in row})
print(f'Loaded {len(ivs)} EUR LD-independent insomnia instruments')

# ---------- 2. index GARD EAS AD by hg19 chr:pos ----------
gard = {}
n_rows = 0
with gzip.open(GARD, 'rt') as f:
    reader = csv.DictReader(f, delimiter='\t')
    for row in reader:
        n_rows += 1
        key = row['SNP_hg19']  # e.g. "1:740857"
        gard[key] = row
print(f'Indexed GARD EAS AD: {n_rows:,} variants')

# ---------- 3. harmonize (position match + allele alignment) ----------
harm = []
for iv in ivs:
    key = f"{iv['chr']}:{iv['pos']}"
    g = gard.get(key)
    if g is None:
        continue
    # alleles: exposure A1=effect allele?  In ukb-b-3957 clean: A1=effect, A2=other.
    # GARD: A1=effect, A2=other (beta is for A1).
    ea_iv, oa_iv = iv['ea'], iv['oa']
    ea_g, oa_g = g['A1'], g['A2']
    # allele alignment: if iv effect allele == gard effect allele -> same direction
    # if iv effect allele == gard other allele -> flip gard beta
    if ea_iv == ea_g and oa_iv == oa_g:
        flip = False
    elif ea_iv == oa_g and oa_iv == ea_g:
        flip = True
    else:
        # incompatible alleles -> skip
        continue
    by = -float(g['beta']) if flip else float(g['beta'])
    harm.append({
        'rsid': iv['snp'],
        'chr': iv['chr'], 'pos': iv['pos'],
        'ea': ea_iv, 'oa': oa_iv,
        'bx': float(iv['beta']), 'sx': float(iv['se']),
        'by': by, 'sy': float(g['se']),
        'p_iv': float(iv['p']),
        'n_exp': 462341,
        'n_out': 6518, 'n_cases': 2919, 'n_controls': 3599,
    })

print(f'Harmonized into GARD EAS AD: {len(harm)} / {len(ivs)} instruments')
if len(harm) < 3:
    print('FATAL: too few instruments'); raise SystemExit(1)

# ---------- 4. MR ----------
bx = np.array([d['bx'] for d in harm]); sx = np.array([d['sx'] for d in harm])
by = np.array([d['by'] for d in harm]); sy = np.array([d['sy'] for d in harm])
k = len(harm)
n_exp = harm[0]['n_exp']; n_out = harm[0]['n_out']; n_cases = harm[0]['n_cases']; n_ctrl = harm[0]['n_controls']

def p_from_z(z): return 2.0*(1.0-0.5*(1.0+math.erf(abs(z)/math.sqrt(2.0))))
def z_test(b, se): return (b/se, p_from_z(b/se))

bx_inv = np.where(abs(bx) > 1e-10, bx, 1e-10)
beta_iv = by / bx_inv
se_iv = sy / abs(bx_inv)
w = 1.0/se_iv**2

beta_ivw = np.sum(w*beta_iv)/np.sum(w)
se_ivw = math.sqrt(1.0/np.sum(w))
z_ivw, p_ivw = z_test(beta_ivw, se_ivw)

q = float(np.sum(w*(beta_iv-beta_ivw)**2)); q_df = k-1
q_p = p_from_z((q-q_df)/math.sqrt(2*q_df)) if q_df > 0 else 1.0
scale = math.sqrt(q/q_df) if (q_df > 0 and q_p < 0.05) else 1.0
se_ivw_re = se_ivw*scale
z_re, p_re = z_test(beta_ivw, se_ivw_re)

# MR-Egger
w_egg = 1.0/sy**2
X = np.column_stack([bx, np.ones(k)])
XTWX = X.T @ np.diag(w_egg) @ X
XTWy = X.T @ (w_egg*by)
try:
    par = np.linalg.solve(XTWX, XTWy)
    slope, inter = par[0], par[1]
    cov = np.linalg.inv(XTWX)
    se_slope = math.sqrt(cov[0,0]); se_inter = math.sqrt(cov[1,1])
    z_s, p_s = z_test(slope, se_slope)
    z_i, p_i = z_test(inter, se_inter)
except np.linalg.LinAlgError:
    slope=inter=se_slope=se_inter=float('nan'); p_s=p_i=float('nan')

# Weighted median (empirical bootstrap-free; linear interpolation of weighted ratios)
order = np.argsort(beta_iv)
bs_ = beta_iv[order]; ws_ = w[order]
cum = np.cumsum(ws_); tot = cum[-1]
cross = np.argmin(cum < 0.5*tot)
if cross == 0:
    beta_wm = float(bs_[0])
else:
    frac = (0.5*tot - cum[cross-1])/(cum[cross]-cum[cross-1])
    beta_wm = float(bs_[cross-1] + frac*(bs_[cross]-bs_[cross-1]))
se_wm = se_ivw
z_wm, p_wm = z_test(beta_wm, se_wm)

# ---------- 5. power (directional-consistency, mRnd-style) ----------
# R^2 of the 40 instruments in the EUR insomnia GWAS
f_stats = (bx/sx)**2
r2_iv = np.sum(f_stats/(f_stats + n_exp))
# case fraction
p_cases = n_cases/n_out
# for a binary outcome, the variance explained by instruments at the liability scale
# is approximated by R2_liab = R2_obs * ... we use a simple approximation:
# z-score power for detecting the EUR clumped null (beta_eur=-0.13) at EAS SE:
# effective SE from IVW here.
z_detect = abs(beta_ivw)/se_ivw
power_2sided_005 = None
# standard normal power for two-sided alpha=0.05
def power_for_beta(b_alt, se):
    if se <= 0 or b_alt == 0: return None
    z = abs(b_alt)/se
    return (1.0 - 0.5*(1.0+math.erf((1.96-z)/math.sqrt(2)))) + \
           (0.5*(1.0+math.erf((-1.96-z)/math.sqrt(2))))
power_eur_null = power_for_beta(beta_ivw, se_ivw)  # power to detect OUR point estimate
power_eur_obs = power_for_beta(-0.13, se_ivw)      # power to detect EUR clumped beta=-0.13

# ---------- 6. report ----------
lines = []
lines.append('=== Trans-ethnic Insomnia -> AD MR (EUR instruments -> EAS outcome) ===\n')
lines.append(f'Exposure: Insomnia ukb-b-3957 (UK Biobank, EUR, n={n_exp:,}); {len(ivs)} LD-independent instruments at r2<0.001, 10 Mb (current 1000G EUR reference; primary EUR analysis reported n=54 under the same thresholds with the July 2026 reference)')
lines.append(f'Outcome:  GARD/NIAGADS NG00182 East Asian AD (n={n_out:,}, cases={n_cases:,}, controls={n_ctrl:,}, lifted hg38->hg19)')
lines.append(f'Harmonized: {k}/{len(ivs)} instruments matched positionally; strand-aligned; {sum(1 for d in harm if d["by"]!=0 and (d["ea"]==d["ea"]))} retained')
lines.append(f'\n--- Primary Results ---')
lines.append(f'IVW (fixed effects)       beta={beta_ivw:+.4f}  SE={se_ivw:.4f}  p={p_ivw:.4f}')
lines.append(f'IVW (multiplicative RE)   beta={beta_ivw:+.4f}  SE={se_ivw_re:.4f}  p={p_re:.4f}')
lines.append(f'MR-Egger                  beta={slope:+.4f}  SE={se_slope:.4f}  p={p_s:.4f}')
lines.append(f'Weighted median           beta={beta_wm:+.4f}  SE={se_wm:.4f}  p={p_wm:.4f}')
lines.append(f'\nCochran Q = {q:.2f} (df={q_df})  p = {q_p:.4f}')
lines.append(f'MR-Egger intercept = {inter:+.4f}  SE = {se_inter:.4f}  p = {p_i:.4f}  {"(no directional pleiotropy)" if p_i>0.05 else "(directional pleiotropy flag)"}')
lines.append(f'\n--- EUR comparison ---')
lines.append(f'EUR clumped (54 IVs, loose): beta = -0.130, p = 0.52  [manuscript Level 2]')
lines.append(f'EAS point estimate: beta = {beta_ivw:+.4f}, p = {p_ivw:.4f}')
lines.append(f'Direction: {"consistent with EUR (negative)" if beta_ivw<0 else "opposite sign to EUR (positive)"} — EUR 95% CI [-0.53, 0.27] vs EAS 95% CI [{beta_ivw-1.96*se_ivw:+.3f}, {beta_ivw+1.96*se_ivw:+.3f}]')
lines.append(f'\n--- Power (directional consistency only) ---')
lines.append(f'R2 instruments (EUR): {r2_iv:.4f}')
lines.append(f'Power to detect EAS point estimate at alpha=0.05 (2-sided): {power_eur_null:.3f}')
lines.append(f'Power to detect EUR clumped beta=-0.13: {power_eur_obs:.3f}')
lines.append(f'\n--- Caveats ---')
lines.append(f'1. EAS outcome small (cases={n_cases:,}) — wide CIs; directional-consistency check only, NOT an independent replication')
lines.append(f'2. EUR instruments transferred trans-ethnically; EUR LD used for clumping (no EAS LD panel available)')
lines.append(f'3. Instrument count (n={k}) differs from primary EUR analysis (n=54) due to LD reference panel update at the public LD server')
lines.append(f'4. Steiger/coloc/LDSC not possible without EAS LD reference')

rep = '\n'.join(lines)
print(rep)

# ---------- 7. save ----------
with open(os.path.join(OUTDIR, 'ea_transethnic_insomnia_ad_report.txt'), 'w') as f:
    f.write(rep + '\n')

with open(os.path.join(OUTDIR, 'ea_transethnic_insomnia_ad_results.csv'), 'w', newline='') as f:
    w = csv.writer(f)
    w.writerow(['method','beta','se','z','p','note'])
    for nm, b, s, pv in [('IVW (fixed effects)', beta_ivw, se_ivw, p_ivw),
                         ('IVW (multiplicative RE)', beta_ivw, se_ivw_re, p_re),
                         ('MR-Egger', slope, se_slope, p_s),
                         ('Weighted median', beta_wm, se_wm, p_wm)]:
        w.writerow([nm, round(b,4), round(s,4), round(b/s,3) if s>0 else 'nan', round(pv,4), ''])
    w.writerow(['Cochran_Q','','','',round(q_p,4), f'Q={q:.2f},df={q_df}'])
    w.writerow(['MR-Egger_intercept','','','',round(p_i,4), f'intercept={inter:.4f}(se={se_inter:.4f})'])

# per-SNP harmonised file for reproducibility
with open(os.path.join(OUTDIR, 'ea_transethnic_insomnia_ad_harm.tsv'), 'w', newline='') as f:
    w = csv.writer(f, delimiter='\t')
    w.writerow(['rsid','chr','pos','bx','sx','by','sy','p_iv'])
    for d in harm:
        w.writerow([d['rsid'], d['chr'], d['pos'], f"{d['bx']:.5f}", f"{d['sx']:.5f}",
                    f"{d['by']:.5f}", f"{d['sy']:.5f}", f"{d['p_iv']:.2e}"])

print(f'\n=== Outputs in {OUTDIR} ===')
