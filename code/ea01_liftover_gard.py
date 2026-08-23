# !/usr/bin/env python3
"""
ea01_liftover_gard.py
Liftover GARD EA AD summary stats from GRCh38 (hg38) to GRCh37 (hg19).
Input:  data/GARD_NG00182/gard_ea_ad_hg38_poskey.tsv.gz
Output: data/processed/gard_ea_ad_hg19.tsv.gz
"""

import gzip, sys, os, time

PROJ = r'.'
INFILE = os.path.join(PROJ, 'data/GARD_NG00182/gard_ea_ad_hg38_poskey.tsv.gz')
OUTDIR = os.path.join(PROJ, 'data/processed')
CHAIN  = os.path.join(PROJ, 'data/ref/hg38ToHg19.over.chain.gz')
OUTFILE = os.path.join(OUTDIR, 'gard_ea_ad_hg19.tsv.gz')

os.makedirs(OUTDIR, exist_ok=True)

from pyliftover import LiftOver
print('Loading chain from', CHAIN)
lo = LiftOver(CHAIN)
print('Chain loaded.')

with gzip.open(INFILE, 'rt') as f:
    header = f.readline().rstrip('\n').split('\t')
print('Input header:', header)
# Expected: SNP, CHR, BP, A1, A2, beta, se, p, N, N_cases, N_controls

n_total = 0; n_mapped = 0; n_failed = 0; n_multiple = 0
# Build known chromosome map autosomes + X + Y + MT
known_chroms = set(str(i) for i in range(1,23)) | {'X','Y','MT','M'}
count_on_chrom = {}  # per-chromosome stats

t0 = time.time()
with gzip.open(INFILE, 'rt') as fin, gzip.open(OUTFILE, 'wt') as fout:
    # write new header: add lift columns
    new_header = ['SNP_hg19','CHR_hg19','BP_hg19'] + header
    fout.write('\t'.join(new_header) + '\n')
    fin.readline()  # skip input header

    for line in fin:
        n_total += 1
        if n_total % 500000 == 0:
            elapsed = time.time() - t0
            rate = n_total / elapsed
            print(f'  [{n_total/1e6:.1f}M] {n_total/1e6:.1f}M rows, '
                  f'{rate:.0f} rows/s, mapped={n_mapped} failures={n_failed} multi={n_multiple}')
        parts = line.rstrip('\n').split('\t')
        # parts: SNPchr:pos_hg38, CHR, BP, ...
        chrom = parts[1]   # numeric chr
        bp_hg38 = int(parts[2])
        # prepare chr prefix for chain
        if chrom not in known_chroms:
            n_failed += 1
            continue
        chr_key = 'chr' + chrom
        res = lo.convert_coordinate(chr_key, bp_hg38)

        if not res:
            n_failed += 1
            fout.write('\t'.join(['NA',chrom,str(bp_hg38)] + parts) + '\n')  # keep original
            continue

        if len(res) > 1:
            n_multiple += 1
        # take first mapping primary assembly
        _, bp_hg19, strand, _ = res[0]
        if strand != '+':
            # negative strand mapping is extremely rare for chain; discard
            n_failed += 1
            fout.write('\t'.join(['NA',chrom,str(bp_hg38)] + parts) + '\n')
            continue

        n_mapped += 1
        snp_hg19 = f'{chrom}:{bp_hg19}'
        fout.write('\t'.join([snp_hg19, chrom, str(bp_hg19)] + parts) + '\n')
        count_on_chrom[chrom] = count_on_chrom.get(chrom, 0) + 1

elapsed = time.time() - t0
print(f'\n=== Liftover complete ({elapsed:.0f}s) ===')
print(f'  Total rows:     {n_total:,}')
print(f'  Mapped (hg19):  {n_mapped:,}  ({100*n_mapped/n_total:.2f}%)')
print(f'  Failed:         {n_failed:,}  ({100*n_failed/n_total:.2f}%)')
print(f'  Multiple hits:  {n_multiple:,}')
print(f'  Output:         {OUTFILE}')

# quick sanity: check APOE region conversion
with gzip.open(OUTFILE, 'rt') as f:
    f.readline()  # header
    for line in f:
        parts = line.rstrip('\n').split('\t')
        if len(parts) < 4: continue
        chrom19 = parts[1]; bp19 = parts[2]
        if chrom19 == '19' and 45400000 <= int(bp19) <= 45500000:
            print(f'\nAPOE sanity check: hg19 chr19:{bp19}  orig={parts[5]} beta={parts[7]} p={parts[9]}')
            break

sys.exit(0)