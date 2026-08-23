# !/usr/bin/env python3
"""
B1_fetch_ukbppp.py - UKB-PPP  pQTL  (Synapse syn51364943)
====================================================================
: managed venv  <python_venv>/envs/default
      ( pip install synapseclient==4.13.0)

:
    set SYNAPSE_AUTH_TOKEN=xxxx        # Synapse  auth token (, )
    <python_venv>/envs/default/Scripts/python.exe B1_fetch_ukbppp.py

:
    - syn51364943  GEO_RESTRICTED .  (1)  Synapse 
      (2)  (Data Access Request ) (3)  Personal Access Token. 
    - ,  PRIORITY 
      ( GFAP / NEFL / CRP / IL6),  ~2923  (~10GB+) . 
    -  OUT_DIR,  manifest.json. 

 ( B1_verify.py ):
    - :  SNP/CHR/BP/A1/A2/BETA/SE/PVAL + 
      (AF / EAF / effect_allele_frequency),  G2 coloc  eaf . 
    -  (GFAP/NEFL/CRP/IL6  1 ). 
    - build = GRCh38 (UKB-PPP 2023 ),  B2  liftover  GRCh37. 
"""
import os
import sys
import json
import argparse

from synapseclient import Synapse
import synapseutils

SYN_ID = "syn51364943"
OUT_DIR = "./output/data/ukbppp"
PRIORITY = ["GFAP", "NEFL", "CRP", "IL6"]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--priority", nargs="*", default=PRIORITY,
                    help=" ( GFAP NEFL CRP IL6)")
    ap.add_argument("--out", default=OUT_DIR)
    ap.add_argument("--all", action="store_true",
                    help=" (, ~10GB+)")
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