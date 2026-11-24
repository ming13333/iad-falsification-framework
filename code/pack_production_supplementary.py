"""Assemble and verify the supplementary set re-uploaded at the production stage.

Frontiers production asked for the supplementary files in ready-to-publish
condition and asked whether the remaining tables should be uploaded. This script
copies the six files out of the revision package into a dated folder, writes a
SHA256 manifest, zips the folder, then re-extracts the zip and re-checks every
hash so that the manifest and the archive describe the same bytes.

Usage:  python code/pack_production_supplementary.py
"""

from __future__ import annotations

import csv
import hashlib
import os
import shutil
import sys
import zipfile

SRC = os.path.join("submissions", "Frontiers_1986036_revision_20261103", "05_Supplementary")
PKG = os.path.join("submissions", "Frontiers_1986036_production_20261124")

FILES = [
    "Supplementary_Note_1.docx",
    "Supplementary_Note_2.docx",
    "Supplementary_Table_S5_STROBE-MR_checklist.docx",
    "Supplementary_Table_S8_scoring_with_footnotes.docx",
    "Supplementary_Table_S12_threshold_robustness.docx",
    "Supplementary_Tables_S1-S12.xlsx",
]


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def main():
    if not os.path.isdir(SRC):
        sys.exit("run from the project root; %s not found" % SRC)
    if os.path.isdir(PKG):
        shutil.rmtree(PKG)
    os.makedirs(PKG)

    rows = []
    for name in FILES:
        src = os.path.join(SRC, name)
        if not os.path.isfile(src):
            sys.exit("missing: %s" % src)
        dst = os.path.join(PKG, name)
        shutil.copy2(src, dst)
        rows.append((name, os.path.getsize(dst), sha256(dst)))

    man = os.path.join(PKG, "MANIFEST_sha256.csv")
    with open(man, "w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh)
        w.writerow(["file", "bytes", "sha256"])
        for r in rows:
            w.writerow(r)

    zpath = PKG + ".zip"
    if os.path.isfile(zpath):
        os.remove(zpath)
    with zipfile.ZipFile(zpath, "w", zipfile.ZIP_DEFLATED) as z:
        for name in FILES + ["MANIFEST_sha256.csv"]:
            z.write(os.path.join(PKG, name), name)

    # verify: re-extract and compare every hash against the manifest
    expect = {r[0]: (r[1], r[2]) for r in rows}
    ok = 0
    with zipfile.ZipFile(zpath) as z:
        names = z.namelist()
        for n in names:
            if n == "MANIFEST_sha256.csv":
                continue
            data = z.read(n)
            digest = hashlib.sha256(data).hexdigest()
            if n in expect and expect[n] == (len(data), digest):
                ok += 1
            else:
                sys.exit("hash mismatch inside zip: %s" % n)

    print("packaged %d files + manifest" % len(FILES))
    for name, size, digest in rows:
        print("  %-56s %9d  %s" % (name, size, digest[:16]))
    print("zip: %s (%d bytes, %d members, %d/%d hashes verified)"
          % (zpath, os.path.getsize(zpath), len(names), ok, len(FILES)))


if __name__ == "__main__":
    main()
