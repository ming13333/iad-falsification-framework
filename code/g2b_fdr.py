# !/usr/bin/env python3
"""G2b ->->AD  MR : BH/FDR  + .

: ./output/results/G2b_curated_mediation.csv
: ./output/results/G2b_curated_fdr.csv ( q )
      stdout: 
"""
import csv, math

SRC = "./output/results/G2b_curated_mediation.csv"
OUT = "./output/results/G2b_curated_fdr.csv"

def isnan(x):
    return x is None or x == "" or x.upper() == "NA"

rows = []
with open(SRC, newline="", encoding="utf-8") as f:
    r = csv.DictReader(f)
    cols = r.fieldnames
    for d in r:
        rows.append(d)

eval_rows = [d for d in rows if not isnan(d.get("p_ind"))]
excl_rows = [d for d in rows if isnan(d.get("p_ind"))]

pvals = [float(d["p_ind"]) for d in eval_rows]
m = len(pvals)
order = sorted(range(m), key=lambda i: pvals[i])
ranked = [pvals[i] for i in order]
q = [0.0]*m
prev = 1.0
for k in range(m, 0, -1):
    idx = k-1
    val = ranked[idx] * m / k
    val = min(val, prev)
    q[idx] = val
    prev = val
for i, oi in enumerate(order):
    eval_rows[oi]["q_ind"] = f"{q[i]:.4g}"

sig = [d for d in eval_rows if float(d["q_ind"]) < 0.05]
min_p = min(pvals)
min_row = eval_rows[pvals.index(min_p)]

out_rows = list(eval_rows)
for d in excl_rows:
    d2 = dict(d); d2["q_ind"] = "NA"; out_rows.append(d2)

with open(OUT, "w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=cols + ["q_ind"])
    w.writeheader()
    for d in out_rows:
        w.writerow(d)

print(f": {len(rows)}")
print(f" ( p_ind): {len(eval_rows)}")
print(f" ( Step2  AD ): {len(excl_rows)} -> " +
      ", ".join(d['protein'] for d in excl_rows))
print(f"FDR<0.05 : {len(sig)}")
print(f" p_ind = {min_p:.4g} ({min_row['protein']} {min_row['target']})")
print(f"boot_p  = {min(float(d['boot_p']) for d in eval_rows):.4g}")
print(f": {OUT}")

def fnum(x):
    return float(x) if not isnan(x) else float('nan')
top = sorted(eval_rows, key=lambda d: abs(fnum(d['indirect'])), reverse=True)[:10]
print("\nTop10 |indirect| (protein | target | b1(p1) | b2(p2) | indirect(p_ind) | boot_p):")
for d in top:
    print(f"  {d['protein']} | {d['target']} | {fnum(d['b1']):.3f}({fnum(d['p1']):.3f}) | "
          f"{fnum(d['b2']):.3f}({fnum(d['p2']):.3f}) | {fnum(d['indirect']):.4f}({fnum(d['p_ind']):.3f}) | {fnum(d['boot_p']):.3f}")