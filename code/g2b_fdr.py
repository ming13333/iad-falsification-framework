#!/usr/bin/env python3
"""G2b 靶向蛋白教育->蛋白->AD 两步 MR 中介: BH/FDR 校正 + 汇总.

输入: C:/Temp/iad_g1/results/G2b_curated_mediation.csv
输出: C:/Temp/iad_g1/results/G2b_curated_fdr.csv (含 q 值)
      stdout: 关键统计量
"""
import csv, math

SRC = "C:/Temp/iad_g1/results/G2b_curated_mediation.csv"
OUT = "C:/Temp/iad_g1/results/G2b_curated_fdr.csv"

def isnan(x):
    return x is None or x == "" or x.upper() == "NA"

rows = []
with open(SRC, newline="", encoding="utf-8") as f:
    r = csv.DictReader(f)
    cols = r.fieldnames
    for d in r:
        rows.append(d)

# 计入的: 有 p_ind 的 (34 个已评估)
eval_rows = [d for d in rows if not isnan(d.get("p_ind"))]
excl_rows = [d for d in rows if isnan(d.get("p_ind"))]

# BH FDR
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

# 写回带 q 值 (评估行) + 排除行 (q=NA)
out_rows = list(eval_rows)
for d in excl_rows:
    d2 = dict(d); d2["q_ind"] = "NA"; out_rows.append(d2)

with open(OUT, "w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=cols + ["q_ind"])
    w.writeheader()
    for d in out_rows:
        w.writerow(d)

print(f"总靶向蛋白: {len(rows)}")
print(f"已评估 (有 p_ind): {len(eval_rows)}")
print(f"排除 (器械不足 Step2 无 AD 工具): {len(excl_rows)} -> " +
      ", ".join(d['protein'] for d in excl_rows))
print(f"FDR<0.05 显著数: {len(sig)}")
print(f"最小 p_ind = {min_p:.4g} ({min_row['protein']} {min_row['target']})")
print(f"boot_p 最小 = {min(float(d['boot_p']) for d in eval_rows):.4g}")
print(f"输出: {OUT}")

# top10 按 |indirect| 排序预览
def fnum(x):
    return float(x) if not isnan(x) else float('nan')
top = sorted(eval_rows, key=lambda d: abs(fnum(d['indirect'])), reverse=True)[:10]
print("\nTop10 |indirect| (protein | target | b1(p1) | b2(p2) | indirect(p_ind) | boot_p):")
for d in top:
    print(f"  {d['protein']} | {d['target']} | {fnum(d['b1']):.3f}({fnum(d['p1']):.3f}) | "
          f"{fnum(d['b2']):.3f}({fnum(d['p2']):.3f}) | {fnum(d['indirect']):.4f}({fnum(d['p_ind']):.3f}) | {fnum(d['boot_p']):.3f}")
