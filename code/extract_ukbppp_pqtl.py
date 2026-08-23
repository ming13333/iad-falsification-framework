# !/usr/bin/env python3
""" UKB-PPP Nature  ST9/ST10  GFAP/NEFL + INTERVAL  pQTL.

: ./output/results/ukbppp_pqtl_extracted.csv
: protein, sheet, rsid, chr, pos_hg38, A1, A0, eaf, beta, se, log10p, pval, cis_trans, n_pqtls_total
"""
import openpyxl, csv, math

SRC = "./output/data/supp_tables.xlsx"
OUT = "./output/results/ukbppp_pqtl_extracted.csv"

TARGETS = {
    'NEFL': 'NEFL', 'GFAP': 'GFAP', 'CRP': 'CRP', 'IL6R': 'IL6R',
    'IL21': 'IL21', 'IL25': 'IL25',
    'C4A': 'C4A', 'C4B': 'C4B',
    'CFH': 'CFH', 'CFB': 'CFB', 'CFHR5': 'CFHR5', 'C1QTNF5': 'C1QTNF5',
    'CCL15': 'CCL15', 'CCL19': 'CCL19', 'CCL21': 'CCL21',
    'CCL25': 'CCL25', 'CCL28': 'CCL28',
    'CXCL11': 'CXCL11', 'IFI16': 'IFI16', 'MMP8': 'MMP8',
    'NCR3': 'NCR3', 'CTSF': 'CTSF', 'CTSH': 'CTSH', 'CTSZ': 'CTSZ',
    'CHI3L1': 'CHI3L1',
    'IL18R1': 'IL18R1', 'IL1R2': 'IL1R2', 'IL1RL1': 'IL1RL1', 'IL3RA': 'IL3RA',
}

wb = openpyxl.load_workbook(SRC, read_only=True)
rows_out = []

for sheet_name in ['ST9', 'ST10']:
    ws = wb[sheet_name]
    count_by_protein = {}
    for row in ws.iter_rows(min_row=6):
        assay = str(row[8].value).strip() if row[8].value else ''
        if assay not in TARGETS:
            continue
        vid = str(row[0].value) if row[0].value else ''
        parts = vid.split(':')
        if len(parts) < 4:
            continue
        chrom = parts[0]
        pos_hg37 = parts[1]
        a0, a1 = parts[2], parts[3]
        rsid_raw = str(row[10].value).strip() if row[10].value else ''
        rsid = rsid_raw[2:] if rsid_raw.startswith('rs') else rsid_raw
        if rsid in ('NA', '-', ''):
            continue
        eaf = row[11].value
        beta = row[12].value
        se = row[13].value
        log10p = row[14].value
        cistrans = str(row[19].value).strip() if row[19].value else 'NA'
        pos_hg38 = row[2].value

        if beta is None or se is None or log10p is None:
            continue

        pval = 10**(-float(log10p))
        rows_out.append({
            'protein': assay,
            'sheet': sheet_name,
            'rsid': f'rs{rsid}',
            'chr': chrom,
            'pos_hg38': pos_hg38,
            'A1': a1,
            'A0': a0,
            'eaf': float(eaf) if eaf else '',
            'beta': float(beta),
            'se': float(se),
            'log10p': float(log10p),
            'pval': pval,
            'cis_trans': cistrans,
        })
        count_by_protein[assay] = count_by_protein.get(assay, 0) + 1

    for p in sorted(count_by_protein):
        print(f'  [{sheet_name}] {p}: {count_by_protein[p]} pQTLs')

# rsID cis > trans; cis ST9
seen = {}
uniq = []
for r in sorted(rows_out, key=lambda x: (0 if x['cis_trans']=='cis' else 1, 0 if x['sheet']=='ST9' else 1)):
    key = (r['protein'], r['rsid'])
    if key not in seen:
        seen[key] = r
        uniq.append(r)

cols = ['protein', 'sheet', 'rsid', 'chr', 'pos_hg38', 'A1', 'A0',
        'eaf', 'beta', 'se', 'log10p', 'pval', 'cis_trans', 'n_total_pqtls']

from collections import Counter
cnt = Counter(r['protein'] for r in uniq)

with open(OUT, 'w', newline='', encoding='utf-8') as f:
    w = csv.DictWriter(f, fieldnames=cols)
    w.writeheader()
    for r in uniq:
        d = {k: r.get(k, '') for k in cols}
        d['n_total_pqtls'] = cnt[r['protein']]
        w.writerow(d)

print(f'\nWritten {len(uniq)} unique pQTLs for {len(cnt)} proteins -> {OUT}')
for p in sorted(cnt):
    cis_count = sum(1 for r in uniq if r['protein']==p and r['cis_trans']=='cis')
    print(f'  {p}: {cnt[p]} total, {cis_count} cis')