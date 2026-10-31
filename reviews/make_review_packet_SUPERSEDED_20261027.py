#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""SUPERSEDED 2026-10-27 -- do not run this file.

The authoritative builder is code/make_review_packet.py (31 KB, 2026-10-30).
This earlier copy (13 KB) predates the data-card sections, the S8/S9/S10/S11
anchors and the --check verifier, so running it silently produces a stale
packet. Kept only for history.

Original docstring follows.

Render the reviewer-response handoff packet + prompt from disk.

Inputs (all read live, nothing hand-copied):
  - 审稿人意见.docx                      -> reviewer text, split into numbered items
  - 课题设计阶段/manuscript_Frontiers_Methods_v2_humanized.md
                                        -> heading line ranges, word counts, number presence check
  - reviews/作者初判_审稿意见分析.md      -> author-side triage (static, authored once)

Outputs:
  - reviews/审稿应答_review_packet.md
  - reviews/审稿应答_prompt_round1.md
  - reviews/审稿应答_prompt_round2.md

Re-run after any manuscript edit: line ranges and word counts are always re-derived.
"""
import os
import re
import sys
import zipfile
from datetime import datetime

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DOCX = os.path.join(ROOT, "审稿人意见.docx")
MS = os.path.join(ROOT, "课题设计阶段", "manuscript_Frontiers_Methods_v2_humanized.md")
ANALYSIS = os.path.join(ROOT, "reviews", "作者初判_审稿意见分析.md")
OUT_PACKET = os.path.join(ROOT, "reviews", "审稿应答_review_packet.md")
OUT_P1 = os.path.join(ROOT, "reviews", "审稿应答_prompt_round1.md")
OUT_P2 = os.path.join(ROOT, "reviews", "审稿应答_prompt_round2.md")

JOURNAL = "Frontiers in Genetics"

# ---------------------------------------------------------------- reviewer docx


def docx_paragraphs(path):
    """Paragraph texts only. NOTE: <w:t must not be matched by <w:tbl>/<w:tc>."""
    with zipfile.ZipFile(path) as z:
        xml = z.read("word/document.xml").decode("utf-8")
    paras = re.findall(r"<w:p(?:\s[^>]*)?>(.*?)</w:p>", xml, re.S)
    out = []
    for p in paras:
        p = re.sub(r"<w:tab/>", " ", p)
        p = re.sub(r"<w:br/>", "\n", p)
        runs = re.findall(r"<w:t(?:\s[^>]*)?>(.*?)</w:t>", p, re.S)
        t = "".join(runs)
        t = re.sub(r"<[^>]+>", "", t)
        for a, b in (("&amp;", "&"), ("&lt;", "<"), ("&gt;", ">"),
                     ("&quot;", '"'), ("&apos;", "'")):
            t = t.replace(a, b)
        out.append(t.strip())
    return out


def split_items(block, expected):
    """Sequential scan for 'N.' anchors; self-validating against expected count."""
    anchors = []
    want = 1
    for m in re.finditer(r"(?<!\d)(?<!\d\.)(\d{1,2})\.\s+", block):
        n = int(m.group(1))
        if n == want:
            anchors.append((m.start(), m.end(), n))
            want += 1
            if want > expected:
                break
    if want <= expected:
        return None, "only found items 1..%d of %d" % (want - 1, expected)
    items = []
    for i, (s, e, n) in enumerate(anchors):
        stop = anchors[i + 1][0] if i + 1 < len(anchors) else len(block)
        items.append((n, re.sub(r"\s+", " ", block[e:stop]).strip()))
    return items, None


def load_reviewers():
    paras = [p for p in docx_paragraphs(DOCX) if p]
    heads = {}
    for i, p in enumerate(paras):
        m = re.match(r"Reviewer\s+(\d+)\s*\|", p)
        if m:
            heads[int(m.group(1))] = i
    if not heads:
        sys.exit("FATAL: no 'Reviewer N |' header found in docx")
    order = sorted(heads)
    blocks = {}
    for k, rn in enumerate(order):
        s = heads[rn] + 1
        e = heads[order[k + 1]] if k + 1 < len(order) else len(paras)
        body = "\n".join(paras[s:e])
        body = re.sub(r"^#\d+\s*", "", body.strip())
        blocks[rn] = body
    return order, blocks


# ------------------------------------------------------------------- manuscript

SUMMARIES = [
    ("A six-gate falsification framework", "标题行 + 作者 + 单位 + 通讯（行 1–9）"),
    ("Abstract", "背景 → 六门 → 43,200 模拟操作特征 → 失眠-AD 判 Grade C；约 305 词"),
    ("Introduction", "MR 三假设失效路径；locus-driven confounding 的四种畸变；框架定位（与 STROBE-MR 互补）"),
    ("Materials and Equipment", "软件与版本清单（`ieugwasr` v1.1.0 + 1000G **EUR** 面板）、输入要求、数据 accession（Table 3）"),
    ("Methods", "方法总纲"),
    ("Objectives and validation of the method", "两部分验证：模拟（已知真值）+ 实证（失眠-AD 边界案例）；阈值预注册且固定"),
    ("The six gates", "G1–G6 逐门定义与计分。**R1#1/#4、R3#4/#6/#8 的主战场**"),
    ("Grading rubric", "0–12 → A(10–12)/B(7–9)/C(4–6)/D(0–3)；双人评分 72 items，Cohen's κ"),
    ("Step-by-step execution protocol", "7 步 + 5 个 pause point + 工时估计（含 CAUSE MCMC）"),
    ("Simulation-based validation: design and data-generating process",
     "网格 3 效应量 × 3 LD 浓度 × 3 多效性 × 2 overlap × 2 工具数 × 400 = 43,200；"
     "DGP 仅一段**定性**描述。**R1#2 的核心地带**"),
    ("Results", "结果总纲"),
    ("Operating characteristics of the framework (43,200-simulation benchmark)",
     "Table 2 数值；Grade A 频率 0→0.88；FDR 0.20 决策阈；单调校准"),
    ("Example of application: the insomnia–AD proof-of-concept",
     "G1–G6 逐门实证 + 工具数链条 2,462→54→44→38→33 + 功效 24%。**R1#5/#6/#7、R3#11 的主战场**"),
    ("Precision, limits of detection, pitfalls, and troubleshooting",
     "检测下限（OR ≥ 1.25/SD）与 5 条排障（Table 5）"),
    ("Discussion", "APOE 模式普适性；与 STROBE-MR 互补；药物靶点转化；Limitations 六条；结论"),
    ("Declarations", "数据/伦理/贡献/基金/COI/AI 使用声明"),
    ("References", "42 条，全含 DOI（投喂时应丢弃）"),
    ("Figure legends", "Fig1 框架 a/b；Fig2 43,200 操作特征；Fig3 案例 MR + coloc 不对称；Fig4 APOE 共享负债；Fig5 12 例分级 + 跨祖先"),
    ("Tables", "Table 1 门判定矩阵；Table 2 模拟操作特征；Table 3 数据清单；Table 4 执行步骤；Table 5 排障"),
]

NUMBER_PROBES = [
    "43,200", "2,462", "0.104", "9.3", "0.130", "0.203", "0.094", "118",
    "0.028", "0.031", "18 of 32", "1 of 47", "1.29", "0.57", "0.91",
    "5.7", "0.84", "0.76", "24%", "0.226", "0.97", "0.0022", "63,926",
]

S8 = os.path.join(ROOT, "课题设计阶段", "Supplementary_final",
                  "S8_twelve_case_validation.csv")


def load_s8():
    import csv
    rows = []
    with open(S8, encoding="utf-8-sig", newline="") as f:
        for r in csv.DictReader(f):
            rows.append(r)
    out = ["| Case | L1 | L2 | L3 | L4 | L5 | L6 | Score | Grade | 备注 |",
           "|---|---|---|---|---|---|---|---|---|---|"]
    for r in rows:
        out.append("| %s | %s | %s | %s | %s | %s | %s | %s | %s | %s |" % (
            r["Case"], r["L1"], r["L2"], r["L3"], r["L4"], r["L5"], r["L6"],
            r["Score"], r["Grade"], (r.get("Notes") or "").replace("|", "/")))
    return "\n".join(out), len(rows)


def wordcount(txt):
    txt = re.sub(r"\$[^$]*\$", " ", txt)
    txt = re.sub(r"[#*_|`>]", " ", txt)
    return len(re.findall(r"[A-Za-z][A-Za-z'\-]*", txt))


def load_manuscript():
    raw = open(MS, encoding="utf-8").read()
    lines = raw.split("\n")
    heads = [(i + 1, re.sub(r"^#+\s*", "", l).strip())
             for i, l in enumerate(lines) if re.match(r"^#{1,3}\s", l)]
    sections, warn = [], []
    for idx, (ln, txt) in enumerate(heads):
        end = heads[idx + 1][0] - 1 if idx + 1 < len(heads) else len(lines)
        hits = [k for k in SUMMARIES if txt.startswith(k[0])]
        if hits:
            key = max(hits, key=lambda k: len(k[0]))
            sections.append((txt, ln, end, key[1]))
        else:
            sections.append((txt, ln, end, "_摘要未登记_"))
            warn.append(txt)
    body = next(i for i, l in enumerate(lines) if l.startswith("## Abstract"))
    refs = next(i for i, l in enumerate(lines) if l.startswith("## References"))
    wc_body = wordcount("\n".join(lines[body:refs]))
    wc_all = wordcount(raw)
    missing = [p for p in NUMBER_PROBES if p not in raw]
    return dict(lines=len(lines), chars=len(raw), sections=sections, warn=warn,
                wc_body=wc_body, wc_all=wc_all, missing=missing, raw=raw)


# ------------------------------------------------------------------- assembly

def demote(md_text):
    lines = md_text.split("\n")
    if lines and lines[0].startswith("# "):
        lines = lines[1:]
    out = []
    for line in lines:
        if line.startswith("# "):
            line = "### " + line[2:]
        elif line.startswith("## "):
            line = "#### " + line[3:]
        out.append(line)
    return "\n".join(out)


def tok(chars):
    return max(1, round(chars / 4))


def main():
    order, blocks = load_reviewers()
    ms = load_manuscript()

    details = {}
    for rn in order:
        block = blocks[rn]
        expected = 10 if "recommend major revision" in block else 12
        items, err = split_items(block, expected)
        if err:
            sys.exit("FATAL: Reviewer %d split failed: %s" % (rn, err))
        details[rn] = items

    analysis = open(ANALYSIS, encoding="utf-8").read()

    tpl_path = os.path.join(ROOT, "reviews", "_packet_body.tpl")
    if not os.path.exists(tpl_path):
        sys.exit("FATAL: missing template %s" % tpl_path)
    tpl = open(tpl_path, encoding="utf-8").read()

    skel = "\n".join(
        "| %s | L%d–L%d | %s |" % (t.replace("|", "/"), a, b, s)
        for t, a, b, s in ms["sections"])

    rev_md = []
    for rn in order:
        rev_md.append("\n#### Reviewer %d —— 逐字原文（%d 条）\n" % (rn, len(details[rn])))
        for n, txt in details[rn]:
            rev_md.append("\n**R%d#%d**\n\n> %s\n" % (rn, n, txt))
    rev_md = "\n".join(rev_md)

    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    s8_md, s8_n = load_s8()
    rev_chars = sum(len(b) for b in blocks.values())
    packet = (tpl
              .replace("{{NOW}}", now)
              .replace("{{JOURNAL}}", JOURNAL)
              .replace("{{MS_PATH}}", MS.replace("\\", "/"))
              .replace("{{MS_LINES}}", str(ms["lines"]))
              .replace("{{MS_CHARS}}", "{:,}".format(ms["chars"]))
              .replace("{{MS_TOKENS}}", "{:,}".format(tok(ms["chars"])))
              .replace("{{WC_BODY}}", "{:,}".format(ms["wc_body"]))
              .replace("{{WC_ALL}}", "{:,}".format(ms["wc_all"]))
              .replace("{{SKELETON}}", skel)
              .replace("{{REVIEWERS}}", rev_md)
              .replace("{{ANALYSIS}}", demote(analysis))
              .replace("{{S8_TABLE}}", s8_md)
              .replace("{{S8_N}}", str(s8_n))
              .replace("{{SZ_MS}}", "{:.1f} KB".format(len(ms["raw"].encode("utf-8")) / 1024))
              .replace("{{SZ_REV}}", "{:.1f} KB".format(len(("".join(blocks.values())).encode("utf-8")) / 1024))
              .replace("{{SZ_ANALYSIS}}", "{:.1f} KB".format(len(analysis.encode("utf-8")) / 1024))
              .replace("{{PACKET_PATH}}", OUT_PACKET.replace("\\", "/"))
              .replace("{{MS_LINES_N}}", str(ms["lines"])))

    packet = packet.replace("SZPACKET", "{:.1f} KB".format(len(packet.encode("utf-8")) / 1024))

    with open(OUT_PACKET, "w", encoding="utf-8") as f:
        f.write(packet)

    p1 = open(os.path.join(ROOT, "reviews", "_prompt_round1.tpl"), encoding="utf-8").read()
    p1 = p1.replace("{{PACKET_PATH}}", OUT_PACKET.replace("\\", "/")).replace("{{JOURNAL}}", JOURNAL)
    with open(OUT_P1, "w", encoding="utf-8") as f:
        f.write(p1)

    p2 = open(os.path.join(ROOT, "reviews", "_prompt_round2.tpl"), encoding="utf-8").read()
    p2 = (p2.replace("{{MS_PATH}}", MS.replace("\\", "/"))
            .replace("{{JOURNAL}}", JOURNAL))
    with open(OUT_P2, "w", encoding="utf-8") as f:
        f.write(p2)

    # ------------------------------------------------------------ verification
    print("=" * 68)
    print("稿件      :", MS)
    print("  lines %d | chars %s | tokens ~%s" % (ms["lines"], "{:,}".format(ms["chars"]),
                                                  "{:,}".format(tok(ms["chars"]))))
    print("  words  Abstract->before References = %s" % "{:,}".format(ms["wc_body"]))
    print("  words  whole file                  = %s" % "{:,}".format(ms["wc_all"]))
    print("  sections rendered = %d" % len(ms["sections"]))
    if ms["warn"]:
        print("  [WARN] summary not registered for:", "; ".join(ms["warn"]))
    else:
        print("  [OK] every heading matched a registered summary")
    if ms["missing"]:
        print("  [WARN] numbers NOT found in manuscript:", ", ".join(ms["missing"]))
    else:
        print("  [OK] all %d load-bearing numbers present" % len(NUMBER_PROBES))
    print("  S8 twelve-case rows = %d" % s8_n)
    for rn in order:
        print("Reviewer %d : %d items" % (rn, len(details[rn])))
        for n, txt in details[rn]:
            print("   R%d#%-2d %s" % (rn, n, txt[:58].replace("\n", " ")))
    for p in (OUT_PACKET, OUT_P1, OUT_P2):
        sz = os.path.getsize(p) if os.path.exists(p) else -1
        print("OUT %-46s %8s bytes  ~%s tok" % (os.path.basename(p), "{:,}".format(sz),
                                                "{:,}".format(tok(sz))))
    print("=" * 68)


if __name__ == "__main__":
    main()
