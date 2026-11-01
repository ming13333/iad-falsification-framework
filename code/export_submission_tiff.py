# -*- coding: utf-8 -*-
"""Build submission-ready TIFFs and the 5-TIFF upload bundle from the
authoritative PNGs in manuscript/figures/.

Why this script exists
----------------------
The TIFFs in 课题设计阶段/figures_final/ were hand-exported in September and
drifted from the manuscript: the Figure 2 and Figure 5 TIFFs still carried the
pre-correction panels after the figures were redrawn. Regenerating them from
manuscript/figures/*.png keeps one source of truth and makes the physical size
a computed quantity rather than a value baked into whatever tool was used.

Spec (matches the figure set that shipped with the first submission)
--------------------------------------------------------------------
  pixels      identical to the authoritative PNG (alpha flattened on white)
  colour      RGB, 8 bits per channel, PhotometricInterpretation = 2
  compression LZW
  resolution  inch units, physical width pinned to TARGET_WIDTH_CM, so
              dpi = round(pixel_width / (TARGET_WIDTH_CM / 2.54))
              and every figure is at least 300 dpi at that width

Run
---
  python code/export_submission_tiff.py                  # all five figures
  python code/export_submission_tiff.py --figs Fig2,Fig5 # only these two

Outputs
-------
  课题设计阶段/figures_final/Fig{1..5}_*.tiff
  课题设计阶段/figures_final/Frontiers_Figures_upload.zip
  课题设计阶段/figures_final/TIFF_manifest.csv   (source -> tiff provenance)
"""

import argparse
import csv
import hashlib
import os
import zipfile

from PIL import Image

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(HERE, "manuscript", "figures")
OUT = os.path.join(HERE, "课题设计阶段", "figures_final")
ZIP_NAME = "Frontiers_Figures_upload.zip"

TARGET_WIDTH_CM = 18.0           # 180 mm, the two-column width Frontiers specifies.
                                 # The September set was 19.05 cm (7.5 in), which is
                                 # 10.6 mm wider than the journal allows; every figure
                                 # is now drawn at 180 mm and exported at 180 mm.
MIN_DPI = 300

FIGURES = [
    ("Fig1", "Fig1_six_gate_framework"),
    ("Fig2", "Fig2_simulation_operating"),
    ("Fig3", "Fig3_case_study_MR"),
    ("Fig4", "Fig4_apoe_shared_liability"),
    ("Fig5", "Fig5_validation_grading"),
]


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def flatten(im):
    """Return an RGB image; alpha, if any, is composited onto white."""
    if im.mode in ("RGBA", "LA", "P"):
        im = im.convert("RGBA")
        bg = Image.new("RGB", im.size, (255, 255, 255))
        bg.paste(im, mask=im.split()[-1])
        return bg
    return im.convert("RGB")


def export(fig_key, stem):
    png = os.path.join(SRC, stem + ".png")
    tif = os.path.join(OUT, stem + ".tiff")
    with Image.open(png) as raw:
        px_w, px_h = raw.size
        im = flatten(raw)
    dpi = int(round(px_w / (TARGET_WIDTH_CM / 2.54)))
    if dpi < MIN_DPI:
        raise SystemExit(f"{stem}: {dpi} dpi at {TARGET_WIDTH_CM} cm is below {MIN_DPI}")
    im.save(tif, format="TIFF", compression="tiff_lzw", dpi=(dpi, dpi),
            tiffinfo={296: 2})          # 296 = ResolutionUnit, 2 = inch
    with Image.open(tif) as chk:
        got_dpi = tuple(int(round(v)) for v in chk.info.get("dpi"))
        assert chk.size == (px_w, px_h), f"{stem}: pixel size changed on export"
        assert chk.mode == "RGB", f"{stem}: not RGB ({chk.mode})"
        unit = chk.tag_v2.get(296)
        comp = chk.tag_v2.get(259)
    width_cm = px_w / got_dpi[0] * 2.54
    height_cm = px_h / got_dpi[0] * 2.54
    return dict(
        figure=fig_key, source_png=os.path.relpath(png, HERE).replace("\\", "/"),
        source_sha256=sha256(png), tiff=os.path.relpath(tif, HERE).replace("\\", "/"),
        tiff_sha256=sha256(tif), px_width=px_w, px_height=px_h,
        dpi=got_dpi[0], width_cm=round(width_cm, 2), height_cm=round(height_cm, 2),
        bytes=os.path.getsize(tif), compression="LZW" if comp == 5 else comp,
        resolution_unit=unit,
    )


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--figs", default="", help="comma separated subset, e.g. Fig2,Fig5")
    args = ap.parse_args()
    wanted = {s.strip() for s in args.figs.split(",") if s.strip()}
    todo = [f for f in FIGURES if not wanted or f[0] in wanted]
    os.makedirs(OUT, exist_ok=True)

    rows = [export(k, s) for k, s in todo]

    print(f"{'figure':7} {'px':>12} {'dpi':>5} {'WxH cm':>13} {'MB':>6}")
    for r in rows:
        print(f"{r['figure']:7} {r['px_width']}x{r['px_height']:<6} {r['dpi']:>5} "
              f"{r['width_cm']:>6}x{r['height_cm']:<5} {r['bytes']/1e6:>6.2f}")

    # bundle every TIFF present in OUT, not just the ones rebuilt in this run
    members = [os.path.join(OUT, stem + ".tiff") for _, stem in FIGURES]
    missing = [m for m in members if not os.path.exists(m)]
    if missing:
        raise SystemExit("refusing to zip, missing: " + ", ".join(missing))
    zip_path = os.path.join(OUT, ZIP_NAME)
    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zf:
        for m in members:
            zf.write(m, os.path.basename(m))
    print(f"\nbundle: {os.path.relpath(zip_path, HERE)} "
          f"({os.path.getsize(zip_path)/1e6:.2f} MB, {len(members)} TIFF)")

    # manifest: one row per TIFF in the final set, rebuilt or not
    all_rows = {r["figure"]: r for r in rows}
    for k, stem in FIGURES:
        if k in all_rows:
            continue
        tif = os.path.join(OUT, stem + ".tiff")
        png = os.path.join(SRC, stem + ".png")
        with Image.open(tif) as it:
            dpi = int(round(it.info["dpi"][0]))
            pw, ph = it.size
        all_rows[k] = dict(
            figure=k, source_png=os.path.relpath(png, HERE).replace("\\", "/"),
            source_sha256=sha256(png), tiff=os.path.relpath(tif, HERE).replace("\\", "/"),
            tiff_sha256=sha256(tif), px_width=pw, px_height=ph, dpi=dpi,
            width_cm=round(pw / dpi * 2.54, 2), height_cm=round(ph / dpi * 2.54, 2),
            bytes=os.path.getsize(tif), compression="LZW",
            resolution_unit=Image.open(tif).tag_v2.get(296),
        )
    man = os.path.join(OUT, "TIFF_manifest.csv")
    fields = list(rows[0].keys())
    tmp = man + ".tmp"
    with open(tmp, "w", encoding="utf-8-sig", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=fields)
        w.writeheader()
        for k, _ in FIGURES:
            w.writerow(all_rows[k])
    # the manifest is often open in a preview pane, which on Windows blocks the
    # destination path; os.replace needs delete access, so fall back to an
    # in-place rewrite (works when the holder only denies delete), then warn
    try:
        os.replace(tmp, man)
        print("manifest:", os.path.relpath(man, HERE))
    except PermissionError:
        try:
            with open(tmp, "rb") as src, open(man, "wb") as dst:
                dst.write(src.read())
            os.remove(tmp)
            print("manifest (in place):", os.path.relpath(man, HERE))
        except PermissionError:
            print(f"WARNING: {os.path.basename(man)} is locked by another process "
                  f"(preview pane?). Fresh copy left at "
                  f"{os.path.relpath(tmp, HERE)}; close the file and rerun, or rename it.")


if __name__ == "__main__":
    main()
