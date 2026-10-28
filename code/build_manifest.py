#!/usr/bin/env python3
"""Build or verify the SHA-256 manifest of the release payload.

The payload is the set of paths a reader is expected to be able to inspect and
re-run: the analysis code, the supplementary tables, the figures and the frozen
results. Working directories that never leave the author's machine (raw GWAS
downloads, intermediate `output/`, manuscript drafts) are deliberately outside
the payload — they are either too large to deposit or not part of the claim.

Usage
    python code/build_manifest.py            # write MANIFEST_sha256.csv
    python code/build_manifest.py --check    # verify the tree against it

`--check` exits 1 on any added, removed or altered file, so it can be used as a
pre-upload gate: a deposit whose manifest does not verify must not be published.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MANIFEST = os.path.join(ROOT, "MANIFEST_sha256.csv")

# Files and directories that make up the release payload, relative to ROOT.
PAYLOAD = [
    ".zenodo.json",
    "CITATION.cff",
    "LICENSE",
    "README.md",
    "renv.lock",
    "code",
    "manuscript/figures",
    "manuscript/supplementary",
    "results",
]

# Never hashed even if they appear under a payload path.
SKIP_DIRS = {"__pycache__", ".ipynb_checkpoints", ".git"}
SKIP_FILES = {"MANIFEST_sha256.csv", ".DS_Store", "Thumbs.db"}


def walk():
    """Yield every payload file path, relative to ROOT, in stable order."""
    for entry in PAYLOAD:
        full = os.path.join(ROOT, entry)
        if os.path.isfile(full):
            yield entry
            continue
        for dirpath, dirnames, filenames in os.walk(full):
            dirnames[:] = sorted(d for d in dirnames if d not in SKIP_DIRS)
            for name in sorted(filenames):
                if name in SKIP_FILES or name.startswith("~$"):
                    continue
                yield os.path.relpath(os.path.join(dirpath, name), ROOT).replace("\\", "/")


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def build():
    rows = []
    for rel in walk():
        full = os.path.join(ROOT, rel)
        rows.append({"path": rel, "bytes": os.path.getsize(full), "sha256": sha256(full)})
    return rows


def write(rows):
    with open(MANIFEST, "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=["path", "bytes", "sha256"])
        w.writeheader()
        w.writerows(rows)
    total = sum(r["bytes"] for r in rows)
    print(f"wrote {os.path.basename(MANIFEST)}: {len(rows)} files, {total/1e6:.1f} MB")
    return 0


def check():
    if not os.path.exists(MANIFEST):
        print("manifest missing; run without --check first", file=sys.stderr)
        return 1
    with open(MANIFEST, encoding="utf-8") as fh:
        recorded = {r["path"]: r for r in csv.DictReader(fh)}
    current = {r["path"]: r for r in build()}

    added = sorted(set(current) - set(recorded))
    removed = sorted(set(recorded) - set(current))
    changed = sorted(p for p in set(current) & set(recorded)
                     if current[p]["sha256"] != recorded[p]["sha256"])

    for label, items in (("ADDED", added), ("REMOVED", removed), ("CHANGED", changed)):
        for p in items:
            print(f"{label:8} {p}")
    if not (added or removed or changed):
        print(f"manifest OK: {len(current)} files, all hashes match")
        return 0
    print(f"\n{len(added)} added, {len(removed)} removed, {len(changed)} changed",
          file=sys.stderr)
    return 1


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true", help="verify instead of write")
    args = ap.parse_args()
    return check() if args.check else write(build())


if __name__ == "__main__":
    sys.exit(main())
