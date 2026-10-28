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
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MANIFEST = os.path.join(ROOT, "MANIFEST_sha256.csv")

# Files and directories that make up the release payload, relative to ROOT.
# The payload is the whole archived tree: anything tracked and shipped has a
# hash here, so a reader can verify the deposit without trusting the archive.
PAYLOAD = [
    ".gitignore",
    ".zenodo.json",
    "CITATION.cff",
    "LICENSE",
    "README.md",
    "renv.lock",
    "code",
    "docs",
    "manuscript",
    "results",
]

# Never hashed even if they appear under a payload path.
SKIP_DIRS = {"__pycache__", ".ipynb_checkpoints", ".git"}
SKIP_FILES = {"MANIFEST_sha256.csv", ".DS_Store", "Thumbs.db"}


def _walk_fs():
    """Filesystem fallback: every payload file, relative to ROOT, in stable order."""
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


def _tracked():
    """Tracked paths, so the manifest matches what `git archive` actually ships."""
    out = subprocess.run(["git", "-C", ROOT, "ls-files", "-z"],
                         capture_output=True, check=True).stdout
    return [p for p in out.decode("utf-8", "replace").split("\0") if p]


def walk():
    try:
        files = sorted(_tracked())
    except (OSError, subprocess.CalledProcessError):
        yield from _walk_fs()
        return
    for rel in files:
        if rel in SKIP_FILES or os.path.basename(rel) in SKIP_FILES:
            continue
        if not any(rel == e or rel.startswith(e.rstrip("/") + "/") for e in PAYLOAD):
            continue
        if os.path.exists(os.path.join(ROOT, rel)):
            yield rel


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def sha256_blob(rel):
    """SHA-256 and size of the git blob, which is what the archive contains.

    Hashing the working file instead would encode the local line-ending
    conversion: with core.autocrlf the checkout has CRLF while the blob and the
    zip have LF, so 125 of 159 files mismatched in the first v1.2.0 manifest.
    """
    blob = subprocess.run(["git", "-C", ROOT, "cat-file", "blob", ":" + rel],
                          capture_output=True, check=True).stdout
    return hashlib.sha256(blob).hexdigest(), len(blob)


def build():
    rows = []
    try:
        subprocess.run(["git", "-C", ROOT, "rev-parse", "--git-dir"],
                       capture_output=True, check=True)
        use_git = True
    except (OSError, subprocess.CalledProcessError):
        use_git = False
    for rel in walk():
        full = os.path.join(ROOT, rel)
        if use_git:
            digest, size = sha256_blob(rel)
        else:
            digest, size = sha256(full), os.path.getsize(full)
        rows.append({"path": rel, "bytes": size, "sha256": digest})
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
