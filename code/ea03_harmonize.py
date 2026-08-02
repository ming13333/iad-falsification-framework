#!/usr/bin/env python3
"""
ea03_harmonize.py
Harmonize EA education instruments with liftover-GARD AD outcome.
- Match by chr:pos (both in hg19 after liftover)
- Allele alignment (effect_allele vs A1/A2)
Input:  data/processed/ea_education_instruments.csv
        data/processed/gard_ea_ad_hg19.tsv.gz
Output: data/processed/ea_harmonized.csv
"""

import csv, gzip, sys, os, math

PROJ = r'c:/D/workbuddy/科研/共病分析'
OUTDIR = os.path.join(PROJ, 'data/processed')
INSTFILE = os.path.join(OUTDIR, 'ea_education_instruments.csv')
GARDFILE = os.path.join(OUTDIR, 'gard_ea_ad_hg19.tsv.gz')
OUTFILE  = os.path.join(OUTDIR, 'ea_harmonized.csv')

# --- load instruments ---
print('Loading instruments...')
instruments = []
with open(INSTFILE, 'r') as f:
    reader = csv.DictReader(f)
    for row in reader:
        row['chromosome'] = str(row['chromosome'])
        row['position'] = int(row['position'])
        instruments.append(row)
print(f'  {len(instruments)} instruments loaded')

# --- build index: chr:pos -> GARD row ---
print('\nLoading GARD (hg19-lifted) and indexing by chr:pos...')
# We'll scan GARD once and build a dict for our 9 positions of interest
# For efficiency: build lookup set first, then scan
lookup = {}
for inst in instruments:
    key = f"{inst['chromosome']}:{inst['position']}"
    lookup[key] = inst

print(f'  Looking up {len(lookup)} positions in GARD...')
matches = {}  # instrument_key -> GARD parts

n_scanned = 0; n_matched = 0
with gzip.open(GARDFILE, 'rt') as f:
    f.readline()  # skip header
    for line in f:
        n_scanned += 1
        if n_scanned % 1000000 == 0:
            print(f'  scanned {n_scanned/1e6:.1f}M GARD rows, matched {n_matched}/9...')
        parts = line.rstrip('\n').split('\t')
        if len(parts) < 11: continue
        # parts: SNP_hg19, CHR_hg19, BP_hg19, SNP, CHR, BP, A1, A2, beta, se, p, N, N_cases, N_controls
        snp_hg19 = parts[0]
        if snp_hg19 in lookup:
            matches[snp_hg19] = parts
            n_matched += 1
            if n_matched == len(lookup):
                print(f'  all {len(lookup)} instruments matched at row {n_scanned:,}')
                break

print(f'  Scanned {n_scanned:,} GARD rows, matched {n_matched}/{len(lookup)} instruments')

# --- allele alignment ---
print('\nHarmonizing alleles...')
harmonized = []
for key, inst in lookup.items():
    if key not in matches:
        print(f'  NOT FOUND in GARD: {inst["rsid"]} ({key})')
        continue
    parts = matches[key]
    # parts[0]=SNP_hg19, [1]=CHR_hg19, [2]=BP_hg19, [3]=SNP_hg38orig, [4]=CHR, [5]=BP_hg38,
    #       [6]=A1, [7]=A2, [8]=beta, [9]=se, [10]=p, [11]=N, [12]=N_cases, [13]=N_controls
    a1_gard = parts[6].strip()
    a2_gard = parts[7].strip()
    beta_gard = float(parts[8])
    se_gard = float(parts[9])
    p_gard = float(parts[10])
    n_total = parts[11]
    n_cases = parts[12]
    n_controls = parts[13]

    ea_edu = inst['effect_allele'].strip().upper()
    oa_edu = inst['other_allele'].strip().upper()
    beta_edu = float(inst['beta'])
    se_edu = float(inst['se'])

    a1_gard_u = a1_gard.upper()
    a2_gard_u = a2_gard.upper()

    # allele alignment
    if ea_edu == a1_gard_u and oa_edu == a2_gard_u:
        # direct match
        beta_gard_align = beta_gard
        align = 'direct'
    elif ea_edu == a2_gard_u and oa_edu == a1_gard_u:
        # flip
        beta_gard_align = -beta_gard
        align = 'flip'
    else:
        # palindromic or mismatch — try matching by one allele
        if ea_edu == a1_gard_u:
            beta_gard_align = beta_gard
            align = 'partial(A1)'
        elif ea_edu == a2_gard_u:
            beta_gard_align = -beta_gard
            align = 'partial(A2)'
        else:
            print(f'  ALLELE MISMATCH: {inst["rsid"]} edu=[{ea_edu}/{oa_edu}] GARD=[{a1_gard_u}/{a2_gard_u}]')
            continue

    harmonized.append({
        'rsid': inst['rsid'],
        'chromosome': inst['chromosome'],
        'position': inst['position'],
        'effect_allele': ea_edu,
        'other_allele': oa_edu,
        'eaf': inst['eaf'],
        'beta_exposure': beta_edu,
        'se_exposure': se_edu,
        'p_exposure': inst['p_value'],
        'f_stat': inst['f_stat'],
        'n_exposure': inst['n_total'],
        'beta_outcome': beta_gard_align,
        'se_outcome': se_gard,
        'p_outcome': p_gard,
        'n_outcome': int(n_total),
        'n_cases': int(n_cases),
        'n_controls': int(n_controls),
        'align': align,
    })

print(f'  Harmonized: {len(harmonized)} / {len(lookup)} instruments')

# --- write output ---
fieldnames = ['rsid','chromosome','position','effect_allele','other_allele','eaf',
              'beta_exposure','se_exposure','p_exposure','f_stat','n_exposure',
              'beta_outcome','se_outcome','p_outcome','n_outcome','n_cases','n_controls',
              'align']
with open(OUTFILE, 'w', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames, extrasaction='ignore')
    writer.writeheader()
    for r in harmonized:
        writer.writerow(r)

print(f'\n=== Output: {OUTFILE} ({len(harmonized)} rows) ===')

# --- quick preview ---
print('\nHarmonized data preview:')
for r in harmonized:
    print(f'  {r["rsid"]:15s} {r["chromosome"]}:{r["position"]:>10,d}  '
          f'exp β={r["beta_exposure"]:.4f}(se={r["se_exposure"]:.4f})  '
          f'out β={r["beta_outcome"]:.4f}(se={r["se_outcome"]:.4f})  '
          f'align={r["align"]}')
