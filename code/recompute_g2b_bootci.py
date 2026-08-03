#!/usr/bin/env python3
"""补全 G2b bootstrap 95% CI（原 R 脚本 quantile 列写入丢失）。

从已写入的 b1,se1,b2,se2 重算 5000 次 product-of-sums bootstrap 的
2.5%/97.5% 分位数，回填 G2b_curated_fdr.csv 的 boot_ci_lower/upper。
boot_mean/boot_p 已由 R 产出且有效，仅补 CI。
"""
import csv, random
import numpy as np

CSV = "C:/Temp/iad_g1/results/G2b_curated_fdr.csv"

def isnan(x):
    return x is None or x == "" or x.upper() == "NA"

rows = []
with open(CSV, newline="", encoding="utf-8") as f:
    r = csv.DictReader(f)
    cols = r.fieldnames
    rows = list(r)

rng = np.random.default_rng(42)
updated = 0
for d in rows:
    if isnan(d.get("b1")) or isnan(d.get("se1")) or isnan(d.get("b2")) or isnan(d.get("se2")):
        continue
    b1, s1, b2, s2 = (float(d["b1"]), float(d["se1"]), float(d["b2"]), float(d["se2"]))
    if s1 <= 0 or s2 <= 0:
        continue
    B = 5000
    s1s = rng.normal(b1, s1, B)
    s2s = rng.normal(b2, s2, B)
    prod = s1s * s2s
    d["boot_ci_lower"] = f"{np.quantile(prod, 0.025):.6g}"
    d["boot_ci_upper"] = f"{np.quantile(prod, 0.975):.6g}"
    updated += 1

with open(CSV, "w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=cols)
    w.writeheader()
    w.writerows(rows)
print(f"recomputed bootstrap CI for {updated} proteins -> {CSV}")
