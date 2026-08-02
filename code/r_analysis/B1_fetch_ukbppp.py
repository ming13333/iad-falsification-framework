#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
B1_fetch_ukbppp.py — UKB-PPP 蛋白 pQTL 取数 (Synapse syn51364943)
====================================================================
依赖: managed venv  C:/Users/lm962/.workbuddy/binaries/python/envs/default
      (已 pip install synapseclient==4.13.0)

用法:
    set SYNAPSE_AUTH_TOKEN=xxxx        # Synapse 账号 auth token (推荐, 非交互)
    C:/Users/lm962/.workbuddy/binaries/python/envs/default/Scripts/python.exe B1_fetch_ukbppp.py

说明:
    - syn51364943 为中国区 GEO_RESTRICTED 受控数据。需先 (1) 注册 Synapse 账号
      (2) 申请该数据集的数据访问 (Data Access Request 获批) (3) 生成 Personal Access Token。
    - 本脚本递归遍历项目树, 仅下载 PRIORITY 关键词命中的蛋白摘要统计文件
      (默认 GFAP / NEFL / CRP / IL6), 避免全量 ~2923 蛋白 (~10GB+) 的盲目下载。
    - 下载后输出到 OUT_DIR, 并生成 manifest.json。

验证门 (落盘后由下游 B1_verify.py 执行):
    - 每文件含列:  SNP/CHR/BP/A1/A2/BETA/SE/PVAL + 至少一个等位基因频率列
      (AF / EAF / effect_allele_frequency), 用于 G2 coloc 方差与 eaf 重抽。
    - 重点蛋白在册 (GFAP/NEFL/CRP/IL6 各自至少 1 个文件)。
    - build = GRCh38 (UKB-PPP 2023 原生), 后续 B2 降 liftover 到 GRCh37。
"""
import os
import sys
import json
import argparse

from synapseclient import Synapse
import synapseutils

SYN_ID = "syn51364943"
OUT_DIR = "C:/Temp/iad_g1/data/ukbppp"
# 重点蛋白 (Olink target 关键词, 实际文件名以项目树为准)
PRIORITY = ["GFAP", "NEFL", "CRP", "IL6"]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--priority", nargs="*", default=PRIORITY,
                    help="蛋白关键词列表 (默认 GFAP NEFL CRP IL6)")
    ap.add_argument("--out", default=OUT_DIR)
    ap.add_argument("--all", action="store_true",
                    help="下载项目内全部文件 (谨慎, ~10GB+)")
    args = ap.parse_args()

    syn = Synapse()
    token = os.environ.get("SYNAPSE_AUTH_TOKEN")
    if token:
        print("[B1] login via SYNAPSE_AUTH_TOKEN env")
        syn.login(authToken=token)
    else:
        print("[B1] login via cached credentials / interactive")
        syn.login()
    print("[B1] connected as:", syn.username)

    os.makedirs(args.out, exist_ok=True)
    priority = [p.lower() for p in args.priority]

    downloaded = []
    skipped = 0
    for dirpath, dirnames, filenames in synapseutils.walk(syn, SYN_ID):
        for fname, fid in filenames:
            low = fname.lower()
            if args.all or any(k in low for k in priority):
                print("[B1] downloading:", fname, "(", fid, ")")
                try:
                    f = syn.get(fid, downloadLocation=args.out)
                    downloaded.append(f.path)
                except Exception as e:
                    print("  !! download failed:", e)
            else:
                skipped += 1

    man = {
        "syn_id": SYN_ID,
        "priority": args.priority,
        "all_mode": args.all,
        "n_downloaded": len(downloaded),
        "n_skipped": skipped,
        "downloaded": downloaded,
    }
    with open(os.path.join(args.out, "manifest.json"), "w", encoding="utf-8") as fh:
        json.dump(man, fh, indent=2, ensure_ascii=False)
    print("[B1] manifest ->", os.path.join(args.out, "manifest.json"))
    print(f"[B1] done. downloaded={len(downloaded)} skipped={skipped}")


if __name__ == "__main__":
    main()
