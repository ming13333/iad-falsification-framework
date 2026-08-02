#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
B1_verify.py — UKB-PPP 下载产物质量验证门 (数据源验证)
=======================================================
读取 B1_fetch_ukbppp.py 生成的 manifest.json, 对每个下载文件检查:
  - 可读 (gzip tsv)
  - 含必需列 SNP/CHR/BP/A1/A2/BETA/SE/PVAL
  - 含至少一个频率列 (AF / EAF / effect_allele_frequency / MAF) —— 供 G2 coloc 方差与 eaf 重抽
  - 重点蛋白 (GFAP/NEFL/CRP/IL6) 在册
输出 verify_report.json + 打印摘要。
"""
import os
import sys
import json

OUT_DIR = "C:/Temp/iad_g1/data/ukbppp"
REQ = ["SNP", "CHR", "BP", "A1", "A2", "BETA", "SE", "PVAL"]
FREQ = ["AF", "EAF", "effect_allele_frequency", "MAF"]
PRIORITY = ["GFAP", "NEFL", "CRP", "IL6"]


def check_file(path):
    try:
        import gzip
        with gzip.open(path, "rt") as fh:
            header = fh.readline().strip().split("\t")
    except Exception as e:
        return {"file": os.path.basename(path), "ok": False, "error": str(e)[:200]}
    cols = [c.upper() for c in header]
    missing_req = [c for c in REQ if c not in cols]
    has_freq = any(f.upper() in cols for f in FREQ)
    return {
        "file": os.path.basename(path),
        "ok": (not missing_req and has_freq),
        "n_cols": len(header),
        "missing_req": missing_req,
        "has_freq": has_freq,
        "freq_cols": [f for f in FREQ if f.upper() in cols],
    }


def main():
    man_path = os.path.join(OUT_DIR, "manifest.json")
    if not os.path.exists(man_path):
        print("NO manifest.json — run B1_fetch_ukbppp.py first")
        sys.exit(1)
    man = json.load(open(man_path, encoding="utf-8"))
    results = [check_file(p) for p in man.get("downloaded", [])]
    n_ok = sum(1 for r in results if r.get("ok"))
    base_names = " ".join(os.path.basename(p).lower() for p in man.get("downloaded", []))
    pri_present = {p: (p.lower() in base_names) for p in PRIORITY}
    report = {
        "n_files": len(results),
        "n_ok": n_ok,
        "results": results,
        "priority_present": pri_present,
        "priority_missing": [p for p in PRIORITY if not pri_present[p]],
    }
    with open(os.path.join(OUT_DIR, "verify_report.json"), "w", encoding="utf-8") as fh:
        json.dump(report, fh, indent=2, ensure_ascii=False)
    print(f"verified {len(results)} files, {n_ok} OK")
    print("priority present:", pri_present)
    print("priority missing:", report["priority_missing"])
    print("report ->", os.path.join(OUT_DIR, "verify_report.json"))


if __name__ == "__main__":
    main()
