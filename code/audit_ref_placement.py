"""逐条引文→稿件段落映射 + 位置合理性审计"""
import re, collections

RIS = "C:/D/workbuddy/科研/共病分析/课题设计阶段/references.ris"
MANUSCRIPT = "C:/D/workbuddy/科研/共病分析/课题设计阶段/Phase2A_abstract_discussion_rewrite.md"

def parse_ris(path):
    entries = []
    current = {}
    for line in open(path, encoding='utf-8'):
        line = line.rstrip('\n')
        if line.startswith('ER  -'):
            if current: entries.append(current); current = {}
            continue
        if line.startswith('TY  -'): continue
        m = re.match(r'^(\w{2})\s{2}-\s(.+)$', line)
        if m:
            tag, val = m.group(1), m.group(2).strip()
            if tag in ('AU','AF'): current.setdefault('AU',[]).append(val)
            elif tag == 'TI': current['TI'] = (current.get('TI','') + ' ' + val).strip()
            elif tag == 'AB': current['AB'] = (current.get('AB','') + ' ' + val).strip()
            else: current[tag] = val
    return entries

# ── 分类规则 ──
# Keywords → section mapping
SECTION_RULES = collections.OrderedDict([
    ("Methods / Statistics", [
        "mendelian randomi","instrumental variable","ivw","weighted median","egger regress",
        "mr presso","cause","mr-base","twosamplemr","summary data","genetic variant",
        "multivariable mendelian","mr-mega","ld score","ldsc","genetic correlation",
        "colocali","steiger","statistical power","power calculation","genomic sem",
        "genomicsem","strobo","reporting guideline","reference panel","1000 genomes",
        "LD reference","pharma proteomics resource","uk biobank","ukb","interval",
        "cohort profile","mrlap","weighted mode","horizontal pleiotrop","sensitivity analy",
        "two.step","mediation framework","pqtl","fine.mapping","credible set",
        "software","r package","r core","ieugwasr"
    ]),
    ("Introduction / Background", [
        "comorbid","multimorbidity","co-occur","overlap","sleep disorder","insomnia",
        "alzheimer disease","alzheimer's disease","dementia","epidemiolog",
        "public health","risk factor","modifiable","observational",
        "genome.wide association","gwas","polygenic","heritab",
        "triangulat","robust research","many lines",
        "causal infer","causal evidence","causal relationship",
        "review","meta.analysis","consensus","guideline","recommend",
    ]),
    ("Results — GWAS / genetic architecture", [
        "genome.wide association","gwas meta","meta.analysis","ld score",
        "genetic correlation","genetic architecture","rg","heritab",
        "loci","susceptibility loci","novel loci","risk loci",
        "insomnia","sleep","alzheimer","education","cognitive","educational attainment",
        "parkinson","multiple sclerosis","neurodegener",
        "apoe","shared genetic","pleiotrop","genetic overlap",
    ]),
    ("Results — MR / mediation", [
        "causal effect","mendelian randomi","mr estimate","causal associat",
        "mediation","indirect effect","indirect","mediator",
        "protein","proteom","pqtl","plasma","metabol","lipid","triglyceride",
        "crp","interleukin","complement","chemokine","nfl","neurofilament","gfap",
        "biomarker","blood.based","blood biomarker","tau","p-tau",
        "drug target","therapeutic target",
        "cross.ancestry","east asian","replicat","trans.ethnic",
    ]),
    ("Discussion / implications", [
        "mechanism","pathway","clinical","intervention","prevent","treatment",
        "translat","public health","policy","framework","paradigm",
        "future direction","limitation","caution","interpret",
        "cognitive reserve","neuroprotect","neurodegener","brain reserve",
        "shared liability","causal upstream","downstream",
        "recalibrat","re-evaluat","reassess",
    ]),
])

def classify(entry):
    ti = (entry.get('TI','') + ' ' + entry.get('AB','')).lower()
    scores = {}
    for section, keywords in SECTION_RULES.items():
        score = sum(1 for kw in keywords if kw in ti)
        if score > 0:
            scores[section] = score
    if not scores:
        return "Unclassified (may not fit this paper)"
    best = max(scores, key=scores.get)
    # If top is close to second, mark as "could fit multiple"
    sorted_s = sorted(scores.items(), key=lambda x: -x[1])
    if len(sorted_s) >= 2 and sorted_s[0][1] == sorted_s[1][1]:
        return f"{best} / {sorted_s[1][0]}"
    return best

entries = parse_ris(RIS)
print(f"Total references: {len(entries)}")
print()

section_counts = collections.Counter()
mapping = []

for i, e in enumerate(entries):
    sec = classify(e)
    section_counts[sec] += 1
    au = e.get('AU',['?'])[0].split(',')[0].strip() if e.get('AU') else '?'
    yr = e.get('PY','?')
    jt = e.get('JF','?')
    ti = e.get('TI','')[:70]
    mapping.append((i+1, sec, au, yr, jt, ti, e.get('DO','?')))

# Print by section
for section in SECTION_RULES:
    entries_in_sec = [m for m in mapping if section in m[1]]
    if not entries_in_sec:
        continue
    print(f"## {section} ({len(entries_in_sec)} refs)")
    print("-" * 80)
    for idx, sec, au, yr, jt, ti, doi in entries_in_sec:
        print(f"  [{idx:2d}] {au} ({yr}) {jt:25s} | {ti:.65s}")
    print()

# Unclassified
uncl = [m for m in mapping if "Unclassified" in m[1] or m[1] not in SECTION_RULES]
if uncl:
    print(f"## UNCLASSIFIED / NEEDS REVIEW ({len(uncl)} refs)")
    print("-" * 80)
    for idx, sec, au, yr, jt, ti, doi in uncl:
        print(f"  [{idx:2d}] {au} ({yr}) {jt:25s} | {ti:.65s}")

print()
print("=" * 80)
print(f"SUMMARY: Methods {section_counts.get('Methods / Statistics',0)}, "
      f"Intro/Background {section_counts.get('Introduction / Background',0)}, "
      f"GWAS Results {section_counts.get('Results — GWAS / genetic architecture',0)}, "
      f"MR/Mediation {section_counts.get('Results — MR / mediation',0)}, "
      f"Discussion {section_counts.get('Discussion / implications',0)}")
