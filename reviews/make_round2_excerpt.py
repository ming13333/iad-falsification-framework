# -*- coding: utf-8 -*-
"""
生成「第 2 轮定向精读」自包含投喂件，并把行区间填进第 2 轮提示词。

为什么要有这个脚本：
  1. 外部模型多半没有文件读取能力（或不允许它去读整篇稿件），必须把原文
     摘录成一份可直接粘贴的投喂件；
  2. 行号来自 2026-10-27 那版 manuscript，任何改稿都会让行号漂移——
     所以区间与摘录都从磁盘实时切，不许手抄；
  3. 表 1 / 表 2 的摘录要带上表题行，否则模型看不到 "Table 1." 的编号。

用法：python reviews/make_round2_excerpt.py
"""
import io
import os
import re

MS = os.path.join("课题设计阶段", "manuscript_Frontiers_Methods_v2_humanized.md")
OUT = os.path.join("reviews", "审稿应答_精读摘录_round2.md")
PROMPT_TPL = os.path.join("reviews", "_prompt_round2.tpl")
PROMPT_OUT = os.path.join("reviews", "审稿应答_prompt_round2.md")

# (起始行, 终止行, 标签, 该段要回答哪几条意见, 模型自述的判断目标)
RANGES = [
    (11, 18, "Abstract", "R3#1、R3#2",
     "判断因果术语是否前后一致；此处 \"precise\" 指什么"),
    (30, 52, "Materials and Equipment", "R3#3、R3#4（间接）",
     "判断 LD 参考面板、EAS 数据与软件版本描述是否足以回应 R3#3"),
    (59, 78, "The six gates + Grading rubric", "R1#1、R1#4、R3#4、R3#6、R3#8",
     "判断六门定义、部分计分、Grade C 与 decisive failure 规则是否自洽"),
    (79, 90, "Step-by-step execution protocol", "R3#5、R3#8、R1#2（对照）",
     "判断 Egger/Q/MRlap/CAUSE 是筛 IV 还是敏感性检查"),
    (91, 95, "Simulation-based validation: design and DGP", "R1#2、R3#9",
     "判断 DGP 正文与 R1#2 所指代码差异的精确落点"),
    (98, 103, "Operating characteristics（结果段）", "R1#4",
     "判断 sens/spec/FDR/0.20 阈值的定义与呈现"),
    (104, 121, "Example of application: insomnia–AD", "R1#5、R1#6、R1#7、R3#7、R3#11",
     "判断 null、反向显著、CAUSE、APOE/chr19 表述"),
    (122, 130, "Precision, limits of detection, pitfalls", "R1#5",
     "判断检测下限与排障段是否已承认低功效边界"),
    (131, 146, "Discussion", "R1#3、R1#10、R3#11",
     "判断药物靶点外推、Limitations 与结论口径是否过强"),
    (210, 221, "Figure legends", "R1#6、R1#9",
     "判断图注是否与评分规则、12 例验证、APOE 叙述冲突"),
    (222, 235, "Table 1（含表题）", "R1#1",
     "判断 Table 1 是否确有\"仅 0/2 分\"脚注及需怎样改"),
    (237, 251, "Table 2（含表题）", "R1#1、R1#4",
     "判断 Table 2 是否需重算 C/D 特异度、CI 与 FDR 不确定性"),
]

# 摘录之外、模型可能需要的区域（诚实标注，不加内容）
NOT_INCLUDED = [
    ("L1–L10", "标题 / 作者 / 单位"),
    ("L19–L29", "Introduction"),
    ("L147–L164", "Declarations（数据、伦理、贡献、基金、COI、AI 声明）"),
    ("L165–L209", "References（42 条）"),
    ("L254–L293", "Table 3 数据清单、Table 4 执行步骤、Table 5 排障"),
]


def read_ms():
    with io.open(MS, encoding="utf-8") as f:
        return f.read().split("\n")


def wc(txt):
    t = re.sub(r"\$[^$]*\$", " ", txt)
    t = re.sub(r"[#*_|`>]", " ", t)
    return len(re.findall(r"[A-Za-z][A-Za-z'\-]*", t))


def tok(chars):
    return int(chars / 3.6)


def main():
    lines = read_ms()
    n = len(lines)

    # ---- 边界体检
    problems = []
    for a, b, label, _, _ in RANGES:
        if b > n:
            problems.append("%s：终止行 %d 超过文件总行数 %d" % (label, b, n))
        if a > b:
            problems.append("%s：起止行颠倒" % label)
    for a, b, label, _, _ in RANGES:
        nxt = lines[b].strip() if b < n else ""
        # 下一行是二级及以上标题、空行、或分隔线 => 视为段末（本稿正文与标题之间常无空行）
        if lines[b - 1].strip() and nxt and not nxt.startswith("#"):
            problems.append("%s：终止行 L%d 不在段末（下一行 L%d 仍有内容）" % (label, b, b + 1))
    if not lines[0].startswith("# "):
        problems.append("L1 不是一级标题，稿件可能已被改过")

    blocks = []
    for a, b, label, items, purpose in RANGES:
        body = "\n".join(lines[a - 1:b])
        blocks.append((a, b, label, items, purpose, body))

    total_chars = sum(len(x[5]) for x in blocks)

    out = []
    w = out.append
    w("# 审稿应答 · 第 2 轮定向精读（自包含投喂件）")
    w("")
    w("> 用途：把外部模型在第 1 轮点名要看、且**只有看到原文才能判断**的 12 个文段，"
      "按行号从稿件实时切下来，做成一份可直接粘贴的单文件。")
    w("> 源文件：`%s`（%d 行）；本文件由 `reviews/make_round2_excerpt.py` 生成，"
      "**改稿后必须重跑**，否则行号漂移。" % (MS.replace("\\", "/"), n))
    w("> 摘录正文共 %d 字符 ≈ %s tokens；12 段。" % (total_chars, "{:,}".format(tok(total_chars))))
    w("")
    w("---")
    w("")
    w("## 一、怎么用")
    w("")
    w("| 场景 | 做法 |")
    w("|---|---|")
    w("| 外部模型**不能**读文件（网页版） | 把「二、提示词」+「三、摘录」**整份**粘贴给它 |")
    w("| 外部模型**能**读文件（同机 agent） | 只发「二、提示词」；它自己按行号读 `%s` |"
      % MS.replace("\\", "/"))
    w("")
    w("两种方式等价：摘录内容与它自己读到的完全一致（逐字切片，未做任何删改或改写）。")
    w("")
    w("---")
    w("")
    w("## 二、提示词（原样复制）")
    w("")
    w("```text")
    prompt = io.open(PROMPT_TPL, encoding="utf-8").read()
    ranges_txt = "\n".join(
        "- L%d–L%d（%s）｜判断目标：%s" % (a, b, label, purpose)
        for a, b, label, _, purpose in RANGES
    )
    prompt_filled = prompt.replace("{{RANGES}}", ranges_txt)
    w(prompt_filled.rstrip())
    w("```")
    w("")
    w("> 上表中 12 个区间**不是**模型原话的等号复制：表 1/表 2 两处已把**表题行**"
      "（L222、L237）并入，否则切片里看不到 \"Table 1.\" / \"Table 2.\" 的编号。"
      "其余 10 段与模型自述的区间逐行一致。")
    w("")
    w("---")
    w("")
    w("## 三、逐段摘录（12 段，逐字）")
    w("")
    w("每段上方是坐标与该段的判断目标；正文未做任何省略、未加批注。")
    w("")
    for idx, (a, b, label, items, purpose, body) in enumerate(blocks, 1):
        w("### 段 %d ｜ L%d–L%d ｜ %s" % (idx, a, b, label))
        w("")
        w("**对应意见**：%s ｜ **判断目标**：%s" % (items, purpose))
        w("")
        w("````text")
        w(body.rstrip())
        w("````")
        w("")
    w("---")
    w("")
    w("## 四、摘录**没有**包含哪里（诚实标注）")
    w("")
    w("| 行区间 | 内容 | 为什么没切 |")
    w("|---|---|---|")
    for rng, what in NOT_INCLUDED:
        w("| %s | %s | 第 1 轮未点名；若你需要，直接说区间，不给也会被告知 |" % (rng, what))
    w("")
    w("> 若模型判断某条意见必须看上述某段，请在输出里用 `L起–L止` 单独提出，"
      "不要基于缺失内容猜测。")
    w("")

    with io.open(OUT, "w", encoding="utf-8") as f:
        f.write("\n".join(out))

    # ---- 同时把带行区间的提示词落盘（模式 A 用）
    with io.open(PROMPT_OUT, "w", encoding="utf-8") as f:
        f.write(prompt_filled)

    # ---- 体检输出
    print("摘录件 : %s" % OUT)
    print("提示词 : %s（已填入 12 个行区间）" % PROMPT_OUT)
    for p in (OUT, PROMPT_OUT):
        sz = os.path.getsize(p)
        print("  %-46s %8s bytes  ~%s tok" % (os.path.basename(p), "{:,}".format(sz),
                                              "{:,}".format(tok(sz))))
    print("摘录正文 %d 字符 / %d 段 / 词数约 %d" % (total_chars, len(blocks),
                                                  wc(" ".join(x[5] for x in blocks))))
    if problems:
        print("\n!! 需人工确认 %d 处：" % len(problems))
        for p in problems:
            print("   - " + p)
    else:
        print("\n边界体检：12 段全部落在段末，无越界，无段中断裂。")


if __name__ == "__main__":
    main()
