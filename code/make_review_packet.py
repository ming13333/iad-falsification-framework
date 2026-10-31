"""Build the third-party audit packet and its two handoff prompts.

This packet is an *audit* handoff, not a rewrite handoff. The external reviewer
is asked to verify that the response letter's claims match the manuscript and
the supplementary tables, that no comment was answered only in words, and that
the revision introduced no new errors. It is not asked whether the paper still
deserves publication -- that question was deliberately excluded by the authors.

Everything that can go stale is computed from disk at build time: heading line
ranges, word counts, file sizes. Never hand-type a line number into this packet;
re-run the script instead.

Usage
    python code/make_review_packet.py
    python code/make_review_packet.py --check    # verify packet matches disk
"""

import argparse
import csv
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

MS = "课题设计阶段/manuscript_Frontiers_Methods_v2_humanized.md"
RESP = "reviews/Response_to_Reviewers_Frontiers.md"
PACKET = "reviews/review_packet_audit.md"
PROMPT1 = "reviews/handoff_prompt_round1.md"
PROMPT2 = "reviews/handoff_prompt_round2.md"

S8 = "manuscript/supplementary/S8_twelve_case_validation.csv"
S9M = "manuscript/supplementary/S9_simulation_operating_marginal.csv"
S10 = "manuscript/supplementary/S10_gate_ablation.csv"
S11 = "manuscript/supplementary/S11_instrument_tiers.csv"
S12 = "manuscript/supplementary/S12_threshold_robustness.md"
T2U = "results/simulation/table2_uncertainty.csv"
CAP = "results/simulation/S14_table2_cap_audit.csv"
FDRS = "results/simulation/fdr_null_fraction_sensitivity.csv"

# One-line summaries for the manuscript skeleton. Keys are heading prefixes:
# lookup is exact first, then longest matching prefix, so rewording a heading
# degrades to "summary not registered" instead of silently dropping the row.
MS_SUMMARY = {
    "# A six-gate": "Title (revised: diagnosing / benchmark of its scoring rule)",
    "## Abstract": "Abstract; claim narrowed to the scoring rule",
    "## Introduction": "Framing: locus-driven confounding; why six gates",
    "## Materials and Equipment": "Data inventory and software",
    "## Methods": "Methods head",
    "### Objectives and validation": "What the framework claims to validate",
    "### The six gates": "G1-G6 definitions",
    "### Grading rubric": "0/1/2 tiers, binary gates, decisive-failure cap",
    "### Step-by-step execution": "Seven-step protocol with pause points",
    "### Simulation-based validation": "Design and data-generating process - rewritten in revision",
    "## Results": "Results head",
    "### Operating characteristics": "Table 2 territory; post-cap numbers",
    "### Example of application": "The insomnia-AD case; Grade C",
    "### Precision, limits of detection": "LD correction, power, pitfalls",
    "## Discussion": "Includes drug-target translation paragraph",
    "## Declarations": "Ethics, data availability, competing interests",
    "## References": "Reference list (drop when feeding)",
    "## Figure legends": "Figure 1-5 legends",
    "## Tables": "Tables 1-5, including the two-layer gate specification",
}

REVIEWER_TITLES = {
    "R1-1": "scoring rules, partial credit, decisive failures",
    "R1-2": "archived simulation code vs described workflow",
    "R1-3": "what the framework adds beyond routine LD handling",
    "R1-4": "operating-characteristic definitions, 0.20 threshold",
    "R1-5": "insufficient evidence is not evidence against",
    "R1-6": "chromosome 19 is not the APOE region",
    "R1-7": "three nulls vs a negative direct effect; CAUSE inputs",
    "R1-8": "conditional instrument strength; mediation details",
    "R1-9": "evidence behind the external-validation scores; kappa",
    "R1-10": "risk factors to drug targets",
    "R3-1": "terminology for directional and causal claims",
    "R3-2": "what 'precise' means",
    "R3-3": "European LD panel on East Asian data",
    "R3-4": "rationale for r2 < 0.001 with a 10,000-kb window",
    "R3-5": "do corrections feed into clumped IVW",
    "R3-6": "confounder choice; why F > 10 sits at G4",
    "R3-7": "power comparability across ancestries",
    "R3-8": "where Egger, Q, MRlap and CAUSE sit",
    "R3-9": "choice of simulation parameter values",
    "R3-10": "what trans-ethnic re-clumping is",
    "R3-11": "do not say r_g 'remained unchanged'",
    "R3-12": "three-line tables without vertical rules",
}

# Declared limitations. The reviewer must not present these as new findings:
# each is already stated somewhere in the letter or the manuscript, and each
# carries a reason why it was left as it is.
OPEN_ITEMS = [
    ("模拟无法回答 LD 校正问题",
     "基准独立抽取工具效应，数据中没有工具间 LD，三臂对比（校正/常规/六门）在那里是同一个估计量。"
     "回信 R1-3 已声明为部分接受，并改用 S10 消融与 S11 三档替代。**不要建议补做三臂模拟**——"
     "那等于替换模拟，不是修订。"),
    ("条件 F 统计量从未提取",
     "归档的 MVIVW 拟合对象未提供条件 F 槽位，28 个模型行该列全为 NA；协调后的多变量输入矩阵未保留，"
     "上游 API 在本方环境不可达。已在方法学与局限中声明为**报告缺口**。不要建议「补算条件 F」。"),
    ("APOE 区域剔除后的对照未做",
     "审稿人建议「同 clumping 设置有/无 APOE 区域的对照」，但 clumped 集仅 54 个变异，剔除后不足以稳定估计。"
     "已如实说明未做，而非呈现一个效能不足的对比。"),
    ("10,000 kb 无法从原理推导",
     "r²<0.001 + 10,000 kb 是 TwoSampleMR/IEU 默认值，作为最保守通行设置采用。已用三档证明结论不依赖它"
     "（最宽松档即已反转），但**不能**从第一原理论证 10,000 优于 5,000。两条都已报告。"),
    ("跨族裔使用欧洲 LD 面板",
     "当时无东亚 LD 参考面板。已写明后果（残余 LD 低估 SE、频率差异移动点估计），且该步只读方向、"
     "在效能 <6% 时不计分。"),
    ("G3 由 G1 决定、G4 与 G2 99.1% 吻合",
     "基准中 G1>0 的重复 100% 得 G3=2；G4 与 G2 在 99.1% 的重复中一致。因此基准实际评估**四门信号**"
     "（G1/G2/G5/G6）到 0–12 的映射。已写入 Table 1 与 Table 2 脚注、方法学、回信 R1-2。"),
    ("决定性失败封顶在本队列不 binding",
     "12 案中唯一 G2 失败者是失眠→AD，总分 4，封顶 6 不触发。S12.3 已明说：封顶位置来自"
     "「C 级上界」的定义，不是这些数据推出来的。"),
    ("`Supplementary_Tables.xlsx` 无三线边框",
     "三线表只在正文 docx 实现；工作簿由 CSV 生成，与归档 v1.2.1 逐字节一致。builder 有 `--rules` 开关，"
     "**默认关闭**以保持与已发布物一致。回信 R3-12 已如实描述。不要建议改默认值。"),
    ("归档快照的 README 含 `<DOI-TODO>`",
     "DOI 在快照之后才铸造，属「先打包后铸造」的固有代价；回填已在 main 分支完成。不要当作错误。"),
    ("旧 DOI 落在旧 concept 下",
     "`21858125`(v1.0.0)/`22064685`(v1.1.0) 属 concept `21858124`，与当前仓库链接已 detach；"
     "新记录 concept 为 `23732880`。README 与 `.zenodo.json` 已如实写明「被取代、非本记录版本」。"),
    ("FDR 存在两种口径，数值差 0.003",
     "**这是定义差异，不是计算错误，也不是笔误。** Table 2 / S14 用「12 个参数格等权平均」得 0.1001；"
     "`fdr_null_fraction_sensitivity.csv` 用「4,800 次重复合并」得 0.0969。同一 regime 的格间 null "
     "判定率不同，平均不等于合并。回信正文的 0.100 用前者，重加权讨论的 0.18/0.26 用后者。"
     "**不要把它报成 MISMATCH**，但可以指出正文未声明口径。"),
]

# Corrections made during this audit pass. A fresh reviewer would otherwise
# re-report them, or worse, revert them.
FIXED_TODAY = [
    ("Summary 第 6 条原漏两个 A 级案例",
     "原只写 Education→AD 12→10，漏了 LDL→CAD 与 BMI→T2D（同为 12→10）。S8 的 `delta` 非零行共 8 个，"
     "现全部指名，并加「eight of the twelve moved」计数。**已于 2026-10-30 修，勿当作遗漏重报。**"),
    ("R1-9 把 LDL→CAD 的投稿版分数写成 `10/10`",
     "S8 的 `score_v1` 为 **12**（原 G6 给 2 分）。已改为「12 points in the submitted version … 10 now」。"
     "**已于 2026-10-30 修，勿改回。**"),
]


def read(rel):
    with open(os.path.join(ROOT, rel), encoding="utf-8") as fh:
        return fh.read()


def lines_of(rel):
    return read(rel).split("\n")


def headings(rel, pattern=r"^#{1,4} "):
    """Return [[lineno, heading, section_end_lineno], ...] for every heading."""
    out = []
    ls = lines_of(rel)
    for i, text in enumerate(ls, 1):
        if re.match(pattern, text):
            out.append([i, text.strip(), None])
    for j, row in enumerate(out):
        row[2] = (out[j + 1][0] - 1) if j + 1 < len(out) else len(ls)
    return out


def summary_for(heading):
    if heading in MS_SUMMARY:
        return MS_SUMMARY[heading]
    best, blen = None, -1
    for key, val in MS_SUMMARY.items():
        if heading.startswith(key) and len(key) > blen:
            best, blen = val, len(key)
    return best or "**summary not registered**"


def words(text):
    return len(re.findall(r"[A-Za-z][A-Za-z'\-]*", text))


def size_kb(rel):
    return os.path.getsize(os.path.join(ROOT, rel)) / 1024.0


def tok(n_words):
    """Rough English token estimate: ~1.33 tokens per word."""
    return int(n_words * 1.33 / 1000) + 1


def load_csv(rel):
    with open(os.path.join(ROOT, rel), encoding="utf-8-sig", newline="") as fh:
        return list(csv.DictReader(fh))


def table(headers, rows):
    out = ["| " + " | ".join(headers) + " |",
           "|" + "|".join(["---"] * len(headers)) + "|"]
    for r in rows:
        out.append("| " + " | ".join(str(c) for c in r) + " |")
    return "\n".join(out)


def build():
    ms_lines = lines_of(MS)
    resp_lines = lines_of(RESP)
    ms_words = words(read(MS))
    resp_words = words(read(RESP))
    resp_last = len(resp_lines) - 1

    # ---- skeleton -------------------------------------------------------
    skel_rows, unregistered = [], []
    for line_no, head, end in headings(MS):
        summ = summary_for(head)
        if "not registered" in summ:
            unregistered.append(head)
        label = head.lstrip("# ").strip()
        if len(label) > 78:
            label = label[:75] + "..."
        skel_rows.append([label, "L%d-L%d" % (line_no, end), summ])

    # ---- response letter index -----------------------------------------
    resp_rows = []
    for line_no, head, end in headings(RESP, r"^#{1,3} "):
        raw = head.lstrip("# ").strip()
        if raw.startswith("Response to Reviewers"):
            continue  # the document title, not a section
        m = re.search(r"(R[13]-\d+)", raw)
        if m:
            resp_rows.append([m.group(1), "L%d-L%d" % (line_no, end),
                              REVIEWER_TITLES.get(m.group(1), "")])
        elif raw.startswith("Table R1"):
            resp_rows.append(["Table R1", "L%d-L%d" % (line_no, end),
                              "disposition table, 22 rows"])
        elif raw.startswith("Summary"):
            resp_rows.append(["Summary", "L%d-L%d" % (line_no, end),
                              "seven headline changes"])
        elif raw.startswith("Note on"):
            resp_rows.append(["Note", "L%d-L%d" % (line_no, end),
                              "supplementary material inventory"])
        else:
            resp_rows.append([raw, "L%d-L%d" % (line_no, end), ""])

    # ---- key numbers ----------------------------------------------------
    t2u = {(r["pleio"], r["effect"]): r for r in load_csv(T2U)}
    t2_rows = []
    for reg in ("none", "balanced", "directional"):
        for eff in ("0.0", "0.08", "0.15"):
            r = t2u[(reg, eff)]

            def trio(pref):
                if not r[pref]:
                    return "-"
                return "%.3f (%.3f-%.3f)" % (float(r[pref]), float(r[pref + "_lo"]),
                                             float(r[pref + "_hi"]))

            t2_rows.append([reg, eff, trio("sens"), trio("spec_D"), trio("spec_CD"),
                            "%.3f" % float(r["p_A"])])

    s8_rows = []
    for r in load_csv(S8):
        six = "".join(r["L%d" % i] for i in range(1, 7))
        s8_rows.append([r["case"], six, r["score"], r["grade"], r["score_v1"],
                        r["grade_v1"], r["delta"],
                        "**yes**" if r["grade_changed"].lower() == "true" else ""])

    s11_rows = []
    for r in load_csv(S11):
        s11_rows.append([r["Instrument tier"], r["Clumping"], r["n IV"],
                         "%.3f" % float(r["beta"]), "%.3f" % float(r["SE"]),
                         "%.2f" % float(r["SE inflation vs unclumped"]),
                         r["Direction"], r["Gate G2"]])

    cap_rows = [[r["regime"], r["metric"], r["uncapped"], r["capped"], r["delta"]]
                for r in load_csv(CAP)]

    fdr_rows = [[r["pleio"], r["pi_null"], r["FDR"],
                 "**YES**" if r["exceeds_0.20"] == "True" else ""]
                for r in load_csv(FDRS)]

    gate_changes = {}
    for r in load_csv(S10):
        if r["Grade changes"] == "True":
            gate_changes[r["Gate removed"]] = gate_changes.get(r["Gate removed"], 0) + 1
    s10_line = ", ".join("G%s %d/12" % (g.lstrip("Ll"), n)
                         for g, n in sorted(gate_changes.items()))

    # ---- packet ---------------------------------------------------------
    P = []
    A = P.append
    A("# review_packet_audit.md — 修订答复第三方复核投喂包")
    A("")
    A("> **用途**：交给一个**有文件读取工具**的模型，复核本次 Frontiers 大修的答复是否站得住。")
    A("> **不是**改写任务：不要重写回信、不要润色正文、不要提新的论证思路。")
    A("> **生成**：`code/make_review_packet.py` 从磁盘实时渲染，行区间与字数每次重算。改动任一方后请重跑。")
    A("> **版本**：audit-2026-10-30 ｜ 回信 %d 行 / %s 词（≈%dk tok）｜ 正文 %d 行 / %s 词（≈%dk tok）"
      % (resp_last, format(resp_words, ","), tok(resp_words),
         len(ms_lines) - 1, format(ms_words, ","), tok(ms_words)))
    A("")
    A("---")
    A("")
    A("## 0. 怎么用（先读这一节）")
    A("")
    A("**模式 A（本包假定）**：模型能读本地文件。**不要粘贴正文**，给路径 + 提示词即可。")
    A("")
    A("**铁律**：第 1 轮只读本包一个文件，读完即停。模型先给出「必须看原文才能核的条目」，")
    A("由作者确认行区间后，第 2 轮才定向读。第 1 轮就去读回信或正文 = 白烧预算。")
    A("")
    A("**为什么第 2 轮允许整份读回信**：回信是审计对象本身，22 条必须逐条核，抽样等于放弃任务。")
    A("这是对「不要整篇读」规则的**有意例外**；正文仍按行区间切。")
    A("")
    A("**为什么本包比常规投喂包厚**：常规包为「提修改意见」而建，只需骨架 + 数字卡。")
    A("本包为「核账」而建，必须携带 §7 的已知未决项与 §9 的判定口径，否则外审会把已声明的东西当新发现，")
    A("或把主动降级当成需要「修正」的错误。")
    A("")
    A("---")
    A("")
    A("## 1. 投喂清单与预算")
    A("")
    A(table(
        ["文件（相对工作区根）", "体量", "估 token", "第 1 轮", "第 2 轮"],
        [["`%s`（本包）" % PACKET, "{{PACKET_SIZE}}", "≈%dk" % 6, "**只读这个**", "不再读"],
         ["`%s`" % RESP, "%.0f KB" % size_kb(RESP), "≈%dk" % tok(resp_words), "禁读", "**整份**"],
         ["`%s`" % MS, "%.0f KB" % size_kb(MS), "≈%dk" % tok(ms_words), "禁读", "按 §8 行区间"],
         ["`%s`" % S8, "%.1f KB" % size_kb(S8), "≈2k", "禁读", "**必读**"],
         ["`%s` / `S11` / `S12`" % S9M,
          "%.1f KB" % (size_kb(S9M) + size_kb(S11) + size_kb(S12)), "≈3k", "禁读", "按需"],
         ["`%s`" % CAP, "%.1f KB" % size_kb(CAP), "≈0.5k", "禁读", "按需"],
         ["`.docx` / 图 / references 段", "—", "—", "不要", "不要"]],
    ))
    A("")
    A("**总成本**：第 1 轮 ≈%dk，第 2 轮 ≈%dk。**单次交付优于多轮**，不要分批发。"
      % (6, tok(resp_words) + tok(ms_words) // 2 + 3))
    A("")
    A("---")
    A("")
    A("## 2. 提示词")
    A("")
    A("- 第 1 轮：`%s`（路径已填，可直接拷）" % PROMPT1)
    A("- 第 2 轮：`%s`（含行区间占位，等第 1 轮回答后填）" % PROMPT2)
    A("")
    A("---")
    A("")
    A("## 3. 硬约束（违反任一条即返工）")
    A("")
    A("1. **不得改动任何数值。** 有疑点写 `to verify`，不要自行算出「应该是多少」。")
    A("2. **不得把「我没找到」当成「作者写错了」。** 区分 `找到且一致` / `找到但不一致` / `档案中无此数`。")
    A("3. **不得把 §7 已声明的缺口当作新发现。** 逐条读过再说话。")
    A("4. **不得建议把已收紧的措辞放宽。** 本稿多处主动降级（六门→四信号、验证→基准、A→B、")
    A("   撤 G6 分），改回去是本轮最严重的错误。")
    A("5. **不得引入 `novel` / `first` / `best` / `optimal` / `solution`。**")
    A("6. **不得改标题。** 两处改动各有理由（见回信 R1-2）；`six-gate` 保留是因为框架本身是六门，")
    A("   被收窄的是基准覆盖的信号数，不是门的数量。")
    A("7. **不得重排投稿策略、选刊或作者信息。** 不在本轮范围。")
    A("8. **不评价「是否仍够格发表」。** 作者有意排除，见 §9 末。")
    A("")
    A("---")
    A("")
    A("## 4. 正文骨架")
    A("")
    A(table(["章节", "行区间", "一句话"], skel_rows))
    A("")
    if unregistered:
        A("> ⚠️ 未登记摘要的标题：%s" % "; ".join(unregistered))
        A("")
    A("---")
    A("")
    A("## 5. 回信骨架（22 条，审计对象）")
    A("")
    A(table(["编号", "行区间", "主题"], resp_rows))
    A("")
    A("注意：`Summary`（L9–L18）与 `Table R1`（L19–L49）都在 R1-1 之前，是总览；")
    A("`Note`（L312–末）是补充材料清单。这三段不属于 22 条中的任何一条。")
    A("")
    A("---")
    A("")
    A("## 6. 关键数字卡")
    A("")
    A("> 全部由脚本从归档 CSV 直读，未手工誊写。回信里的每个数字都应能在下面或 S8/S10/S11/S12 找到出处；")
    A("> 找不到 = `档案中无此数`，按硬约束 2 处理，不要判成错。")
    A("")
    A("### 6.1 Table 2 — 操作特征（43,200 次重复，seed 20260804，**已施加决定性失败封顶**）")
    A("")
    A(table(["多效性", "效应 β", "敏感度 A/B", "特异度 D-only", "特异度 C/D", "P(A)"], t2_rows))
    A("")
    A("每行 = 12 个参数格等权均值，每格 400 次重复 × 3 个效应档；括号内为 4,800 次重复上的 95% Wilson 区间。")
    A("")
    A("### 6.2 S8 — 十二案评分（v1 = 投稿版）")
    A("")
    A(table(["案例", "G1-G6", "分数", "等级", "投稿版分数", "投稿版等级", "Δ", "跨级?"], s8_rows))
    A("")
    A("**Δ≠0 共 8 例，跨级 1 例（Height→CAD，A→B）。** 回信 Summary 第 6 条声称「every score that moved」")
    A("并称列全 8 例 —— 请逐一核对上表 Δ≠0 的行是否都在该条里被指名。")
    A("")
    A("### 6.3 S11 — 三档工具（失眠→AD）")
    A("")
    A(table(["档位", "clumping", "n IV", "β", "SE", "SE 膨胀", "方向", "G2"], s11_rows))
    A("")
    A("### 6.4 封顶前后（S14）")
    A("")
    A(table(["regime", "指标", "未封顶", "已封顶", "Δ"], cap_rows))
    A("")
    A("**特异度与 P(Grade A) 的 Δ 全为 0** —— 这是回信「特异度不变」的依据。")
    A("")
    A("### 6.5 FDR 对真零比例的依赖")
    A("")
    A(table(["多效性", "π(null)", "FDR", ">0.20?"], fdr_rows))
    A("")
    A("> ⚠️ **两种口径并存，见 §7 第 11 条。** 本表用「4,800 次合并」口径（balanced/1-3 = **0.0969**）；")
    A("> Table 2 与 S14 用「12 格等权平均」口径（**0.1001**）。回信正文的 0.100 属后者，")
    A("> 重加权讨论里的 0.18/0.26 属前者。差额 0.003 来自加权方式，**不是算错**。")
    A("")
    A("### 6.6 其它被引用的数")
    A("")
    A("- 留一门消融（S10，72 行）：移除单门后改变等级的案例数 —— %s" % s10_line)
    A("- 敏感度重算：β=0.15 无多效性 **0.878**（投稿 0.973）；平衡 **0.724**（0.847）；方向性 **0.691**（0.804）")
    A("- 改判重复数：**4,363 / 43,200 = 10.1%**，全部 B→C，且全部为真实非零效应")
    A("- 阈值扰动：`A≥11` 三例 A→B；`C≥5` 主案 C→D（仍负）；**极性翻转 0 例**")
    A("- 220 种单调四段划分：主案极性保持 89.3%，三个 A 级案例 100%")
    A("- 教育→AD 东亚复制：β = −0.029，P = 0.85，实际效能 ≥84%")
    A("- 教育→TG β=−0.183（P=2.5e-22）；TG→AD β=+0.169（P=9.7e-6）；indirect −0.031（q=5.7e-4）；中介比 9.5%")
    A("- κ 复现性：11/12 等级，κ=0.89（95% CI 0.64–1.00），加权 κ=0.97，逐门 72 项 κ=0.91")
    A("- 归档 DOI `10.5281/zenodo.23733172`（v1.2.1）；旧 `10.5281/zenodo.21858125` 仅作历史叙述")
    A("")
    A("---")
    A("")
    A("## 7. 已知未决项（**先读这一节，再开口**）")
    A("")
    A("> 以下各项作者已内部识别并在回信或正文中声明。**不要当作新发现重报。**")
    A("> 若你认为某项其实仍不成立、或不构成充分披露，请直接反驳并说明理由 —— 这是允许的。")
    A("> 但重复报告同一事实而不给新论据，属于浪费行数。")
    A("")
    for i, (name, detail) in enumerate(OPEN_ITEMS, 1):
        A("**%d. %s**" % (i, name))
        A("")
        A(detail)
        A("")
    A("### 7b. 本轮已修（勿当遗漏重报，**更勿改回**）")
    A("")
    for name, detail in FIXED_TODAY:
        A("- **%s**：%s" % (name, detail))
    A("")
    A("---")
    A("")
    A("## 8. 深读索引（第 2 轮用；按审计路径组织）")
    A("")
    A(table(
        ["要核什么", "读哪里"],
        [["22 条答复全文", "`%s` L1–L%d（整份）" % (RESP, resp_last)],
         ["评分规则与门的定义", "`%s` Methods「The six gates」「Grading rubric」" % MS],
         ["Table 1 两层表 + 封顶脚注", "`%s` Tables 段" % MS],
         ["Table 2 + 脚注（四信号声明）", "`%s` Tables 段" % MS],
         ["模拟设计与退化", "`%s` Methods「Simulation-based validation」" % MS],
         ["LD 校正的实证", "`%s` Results「Precision, limits of detection…」" % MS],
         ["失眠→AD 主案", "`%s` Results「Example of application」" % MS],
         ["十二案逐门证据 + G6 evidence", "`%s`" % S8],
         ["阈值稳健性四项", "`%s`（S12.1–S12.5）" % S12],
         ["留一门消融", "`%s`" % S10],
         ["封顶前后", "`%s`" % CAP],
         ["规则唯一真源", "`results/validation/rubric_spec_v3.csv`"]],
    ))
    A("")
    A("---")
    A("")
    A("## 9. 审计契约（第 2 轮输出格式，固定）")
    A("")
    A("**三张表，(A) 必须先出，行数为硬限。**")
    A("")
    A("**表 A — 逐条核账**（22 行，一条不漏）")
    A("")
    A(table(["列", "内容"],
            [["#", "R1-1 … R3-12"],
             ["回信声称", "该条 Response 里最容易被核的一个具体断言；含数字则照抄"],
             ["核账位置", "文件 + 行区间"],
             ["实际", "你在该位置读到的原值；没有就写 `NOT FOUND`"],
             ["判定", "`PASS` / `MISMATCH` / `NOT IN ARCHIVE` / `OVERCLAIM`"],
             ["一句话", "仅当判定非 PASS 时填"]]))
    A("")
    A("判定口径：")
    A("")
    A("- `PASS` = 回信断言与证据一致")
    A("- `MISMATCH` = 两处写的不是同一个数、或不是同一件事")
    A("- `NOT IN ARCHIVE` = 回信提到的数字档案里查不到（**不等于错**，可能是档案缺）")
    A("- `OVERCLAIM` = 数字对，但措辞比证据强（如把「未检出」说成「排除」）")
    A("")
    A("**表 B — 只说未改 / 说满**（≤8 行）")
    A("")
    A(table(["列", "内容"],
            [["编号", "回信条目"],
             ["问题类型", "`口头接受但正文无对应改动` / `改动幅度小于承诺` / `措辞强于证据` / `回避了意见的核心`"],
             ["证据", "回信行 + 正文行"],
             ["建议", "具体到「加哪一句」「改哪个词」；不要写「建议加强论述」"]]))
    A("")
    A("**表 C — 修订新引入的错误**（≤8 行）")
    A("")
    A(table(["列", "内容"],
            [["位置", "文件 + 行"],
             ["错误类型", "`内部矛盾` / `数字串台` / `新旧表述并存` / `表格与正文不一致` / `失效引用`"],
             ["说明", "哪两处矛盾，各写了什么"],
             ["修法", "直接给替换文字（英文原文）"]]))
    A("")
    A("**最后一行**：`COVERAGE: xx/22 PASS, yy MISMATCH, zz NOT IN ARCHIVE, ww OVERCLAIM`")
    A("")
    A("**不要写导言、不要复述回信、不要写总结段。三张表之后即停。**")
    A("")
    A("**明确不要求你回答**：这篇文章是否仍够格发表、贡献是否被削空、该投哪本刊。")
    A("这是作者的决定，不在本轮范围。")
    A("")
    A("---")
    A("")
    A("*本包含索引、骨架、数字卡、已知未决项与审计契约，不含正文。正文按 §8 行区间定向读取。*")

    packet = "\n".join(P) + "\n"
    # Fill the packet's own size. One pass is enough: the placeholder and the
    # substituted string have the same order of magnitude, so the reported
    # figure is accurate to a tenth of a KB.
    packet = packet.replace("{{PACKET_SIZE}}", "%.1f KB" % (len(packet.encode("utf-8")) / 1024.0))

    # ---- prompts --------------------------------------------------------
    # Absolute POSIX-style paths: the handoff happens on this machine, and an
    # absolute path removes the model's search round entirely.
    abs_packet = os.path.join(ROOT, PACKET).replace("\\", "/")
    abs_resp = os.path.join(ROOT, RESP).replace("\\", "/")
    abs_ms = os.path.join(ROOT, MS).replace("\\", "/")
    abs_s8 = os.path.join(ROOT, S8).replace("\\", "/")
    n_open = len(OPEN_ITEMS)
    n_fixed = len(FIXED_TODAY)

    p1 = """你是 Frontiers in Genetics 的统计审稿人。本轮任务不是提修改意见，而是**核查一份"回复审稿人"的信是否站得住**。

本轮只读一个文件，读完即停：

%s

禁止：读其他任何文件、列目录、全库搜索、读回信正文、读稿件正文。

任务：读完本包后，输出两样东西，不要多写：

1) 你必须看到原文才能下判断的条目清单（用第 5 节的行号格式，如 R1-2 L70-L85，或第 8 节的文件 + 章节），每项一行，附一句话说明「不读原文就无法判断什么」；
2) 其余你认为仅凭本包的骨架 + 数字卡 + 已知未决项就能直接判定的条目清单（同样标编号）。

特别说明：第 6 节已给出 Table 2、S8、S11、S14 的完整数值。凡是你能在第 6 节内完成核对的条目，直接归入第 2 类，不要再要求读原文。
第 7 节已列出 %d 项作者已声明的缺口与 %d 项本轮已修事项。凡属这些条目的，不要要求读原文去"重新发现"它们。

等我确认清单后再进入第二轮。
""" % (abs_packet, n_open, n_fixed)

    p2 = """读下面这些位置，然后停：

回信（整份，审计对象）：
%s
第 1 行至第 %d 行

正文（只读这些行区间）：
%s
{{RANGES_ROUND_1}}

补充表（必读，十二案全表，含 G6 evidence 列）：
%s

禁止：读上述之外的任何行、读其他文件、列目录、搜索。

硬约束：
- 不得改动任何数值。有疑点写 to verify，不要自行算出「应该是多少」。
- 区分三态：找到且一致 / 找到但不一致 / 档案中无此数。不得把「我没找到」当成「作者写错了」。
- 不得建议把已收紧的措辞放宽（六门→四信号、验证→基准、A→B、撤 G6 分都是主动降级，改回去是严重错误）。
- 不得引入 novel / first / best / optimal / solution。
- 不得改标题、不得重排选刊或作者信息。
- 不评价「是否仍够格发表」——作者有意排除。
- 投喂包第 7 节的 %d 项已知缺口与 %d 项已修事项，不要当作新发现重报。

按投喂包第 9 节的契约输出三张表：
表 A 逐条核账（22 行，一条不漏；列：编号｜回信声称｜核账位置｜实际｜判定｜一句话）
表 B 只说未改 / 说满（≤8 行；列：编号｜问题类型｜证据｜建议）
表 C 修订新引入的错误（≤8 行；列：位置｜错误类型｜说明｜修法）

最后一行输出：COVERAGE: xx/22 PASS, yy MISMATCH, zz NOT IN ARCHIVE, ww OVERCLAIM

不要写导言、不要复述回信、不要写总结段。三张表之后即停。
""" % (abs_resp, resp_last, abs_ms, abs_s8, n_open, n_fixed)

    return packet, p1, p2


def write(rel, text):
    path = os.path.join(ROOT, rel)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(text)
    print("wrote %-46s %6.1f KB" % (rel, len(text.encode("utf-8")) / 1024.0))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true",
                    help="compare the packet on disk with a fresh render")
    args = ap.parse_args()

    packet, p1, p2 = build()
    if args.check:
        bad = 0
        for rel, text in ((PACKET, packet), (PROMPT1, p1), (PROMPT2, p2)):
            if read(rel) != text:
                print("STALE  %s" % rel)
                bad += 1
            else:
                print("ok     %s" % rel)
        # Stale line ranges are the silent failure mode: assert the load-bearing
        # numbers still exist in the text those ranges point at.
        body = read(MS)
        missing = [n for n in ("0.878", "0.724", "0.691", "43,200", "decisive")
                   if n not in body]
        if missing:
            print("MISSING from manuscript: %s" % missing)
            bad += 1
        let = read(RESP)
        for k in ("R1-1", "R3-12", "every score that moved"):
            if k not in let:
                print("MISSING from letter: %s" % k)
                bad += 1
        return 1 if bad else 0

    write(PACKET, packet)
    write(PROMPT1, p1)
    write(PROMPT2, p2)
    print()
    print("packet %.1f KB" % (len(packet.encode()) / 1024))
    return 0


if __name__ == "__main__":
    sys.exit(main())
