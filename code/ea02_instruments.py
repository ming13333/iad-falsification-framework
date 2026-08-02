#!/usr/bin/env python3
"""
ea02_instruments.py
Extract genome-wide significant instruments from Chen 2024 EAS EduYears GWAS.
- Filter: p<5e-8, single-nucleotide (no indels), beta!=0
- Distance-based clumping (kb=10Mb greedy)
- Compute per-SNP F-statistic
Input:  GCST90296498.tsv (Chen 2024 EAS EduYears, hg19, uncompressed TSV)
Output: data/processed/ea_education_instruments.csv
"""

import csv, sys, os, heapq, math

PROJ = r'c:/D/workbuddy/科研/共病分析'
INFILE = os.path.join(PROJ, 'GCST90296498.tsv')
OUTDIR = os.path.join(PROJ, 'data/processed')
OUTFILE = os.path.join(OUTDIR, 'ea_education_instruments.csv')

os.makedirs(OUTDIR, exist_ok=True)

# --- config ---
P_THRESH = 5e-8
CLUMP_KB = 10000

# --- scan: find all GW-sig SNPs (single nucleotide, non-zero beta) ---
print('Scanning for p<5e-8, single-nucleotide, beta!=0 instruments...')
candidates = []  # list of (p, dict)
n_scanned = 0; n_gwsig = 0; n_indel = 0; n_beta0 = 0; n_total_nonan = 0

with open(INFILE, 'r') as f:
    reader = csv.DictReader(f, delimiter='\t')
    for row in reader:
        n_scanned += 1
        if n_scanned % 1000000 == 0:
            print(f'  scanned {n_scanned/1e6:.1f}M...')
        try:
            p = float(row['p_value'])
            beta = float(row['beta'])
        except (ValueError, KeyError):
            continue
        n_total_nonan += 1
        if p >= P_THRESH:
            continue
        n_gwsig += 1
        # filter indels
        ea = row.get('effect_allele', '')
        oa = row.get('other_allele', '')
        if len(ea) != 1 or len(oa) != 1:
            n_indel += 1
            continue
        # filter beta==0
        if beta == 0.0:
            n_beta0 += 1
            continue
        candidates.append((p, dict(
            chromosome=row['chromosome'],
            position=int(row['base_pair_location']),
            effect_allele=ea,
            other_allele=oa,
            beta=beta,
            se=float(row['standard_error']),
            eaf=float(row.get('effect_allele_frequency', 'nan') or 'nan'),
            p_value=p,
            variant_id=row.get('variant_id', ''),
            rsid=row.get('rsid', ''),
        )))

print(f'\n=== Scan complete ({n_scanned:,} rows) ===')
print(f'  Numeric p:       {n_total_nonan:,}')
print(f'  p<5e-8 raw:      {n_gwsig:,}')
print(f'  Indels excluded: {n_indel:,}')
print(f'  beta=0 excluded: {n_beta0:,}')
print(f'  Candidates:      {len(candidates):,}')

# --- distance-based clumping ---
print('\nClumping (kb=10Mb greedy, by p-value)...')
candidates.sort(key=lambda x: x[0])  # sort by p ascending
last_pos = {}  # chrom -> last kept bp
clumped = []

for p, rec in candidates:
    chrom = rec['chromosome']
    pos = rec['position']
    if chrom not in last_pos or abs(pos - last_pos[chrom]) > CLUMP_KB * 1000:
        # compute F-statistic
        f_stat = (rec['beta'] / rec['se']) ** 2
        rec['f_stat'] = round(f_stat, 2)
        rec['r2_approx'] = round(f_stat / (f_stat + rec.get('', 1) - 2) if f_stat > 0 else 0, 6)
        rec['n_total'] = 165232  # sample size from GWAS Catalog
        clumped.append(rec)
        last_pos[chrom] = pos

print(f'Clumped instruments: {len(clumped):,}')

# summary stats by chromosome
chr_counts = {}
for r in clumped:
    ch = r['chromosome']
    chr_counts[ch] = chr_counts.get(ch, 0) + 1
print('Per-chromosome:')
for ch in sorted(chr_counts, key=lambda x: (len(x), x)):
    print(f'  chr{ch}: {chr_counts[ch]}')

# F-stat distribution
fs = [r['f_stat'] for r in clumped]
print(f'F-stat range: {min(fs):.1f} – {max(fs):.1f}')
print(f'F-stat <10: {sum(1 for f in fs if f<10)} / {len(fs)}')
print(f'F-stat median: {sorted(fs)[len(fs)//2]:.1f}')

# top 5 instruments
print('\nTop 5 instruments (by p-value):')
for r in clumped[:5]:
    print(f'  {r["rsid"]:15s} chr{r["chromosome"]}:{r["position"]:>10,d}  '
          f'{r["effect_allele"]}>{r["other_allele"]}  '
          f'beta={r["beta"]:.4f}  se={r["se"]:.4f}  '
          f'p={r["p_value"]:.2e}  F={r["f_stat"]:.1f}  eaf={r["eaf"]:.3f}')

# --- write output ---
fieldnames = ['rsid','chromosome','position','effect_allele','other_allele',
              'beta','se','p_value','eaf','f_stat','n_total',
              'variant_id']
with open(OUTFILE, 'w', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames, extrasaction='ignore')
    writer.writeheader()
    for r in clumped:
        writer.writerow(r)

print(f'\n=== Output: {OUTFILE} ({len(clumped)} rows) ===')

# --- quality gate ---
if len(clumped) < 5:
    print('\nWARNING: <5 clumped instruments extracted. Consider p<5e-6 relaxation.')
elif len(clumped) < 10:
    print('\nCAUTION: only {} clumped instruments — MR-Egger may be underpowered.')
