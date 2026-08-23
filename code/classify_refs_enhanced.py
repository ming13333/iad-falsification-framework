"""Enhanced classifier: use full abstract + title to assign all 86 refs to sections.
Output: classified RIS with section tags in N2 field, plus placement map."""
import re, collections

RIS = "./docs/historical/references.ris"

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

# ── Section definitions with weighted keywords ──
SECTIONS = collections.OrderedDict([
    ("1_Methods_STATS", {
        "weight": 2.0,
        "high": [
            "statistical power","power calculation","power calculat","bias correction",
            "weighted median estimator","weighted mode","mr presso","mr- presso",
            "egger regression","inverse variance","ivw","fixed effect",
            "leave-one-out","heterogeneity test","cochran","pleiotropy test",
            "mrlap","sample overlap","sensitivity analys","robustness",
            "harmonis","harmoniz","ld clump","ld prun","instrument select",
            "genomic sem","genomicsem","structural equation",
            "steiger","directionality test","false discovery"
        ],
        "med": [
            "method","methodolog","framework","approach","pipeline",
            "software","package","workflow","tool","protocol",
            "two-sample","two sample","summary statistics","summarized data",
            "mendelian randomi","instrumental variable","genetic variant","genetic instr",
            "strobe","reporting guideline",
            "fine.mapping","fine mapping","credible set",
        ],
    }),
    ("2_Methods_DATA", {
        "weight": 1.5,
        "high": [
            "uk biobank","ukb","biobank","pharma proteomics","ukb-ppp",
            "interval","blood donor","cohort profile","cohort description",
            "reference panel","1000 genomes","ld reference","ld score",
            "gwas catalog","open gwas","ieu open",
            "data source","data availab","data access","resource",
            "deep phenotyp","imaging","repeat imagin",
        ],
        "med": [
            "cohort","participant","sample","population","volunteer",
            "database","repository","registry",
        ],
    }),
    ("3_Intro_Background", {
        "weight": 1.8,
        "high": [
            "comorbid","multimorbidity","co-occur","coexist","complication",
            "sleep disorder","sleep disturbance","sleep problem","insomnia",
            "alzheimer disease","alzheimer's disease","dementia","cognitive decline",
            "neurodegener","brain health","cognitive impair","memory",
            "observational stud","epidemiolog","risk factor","modifiable risk",
            "public health burden","global burden","prevalence","incidence",
            "triangulat","many lines of evidence","robust research",
            "recalibrat","re-evaluat","reassess","methodolog","framework",
            "mendelian randomiz","genetic epidemiolog","causal infer",
            "review","meta.analysis","consensus","recommend",
            "controvers","conflict","inconsistent","discrepan",
        ],
        "med": [
            "background","introduction","overview","context",
            "association","link","relationship","connection",
            "hypothes","propose","suggest","may","might",
            "prior","previous","existing","established",
        ],
    }),
    ("4_Results_GWAS", {
        "weight": 1.5,
        "high": [
            "genome.wide association","gwas","gwas meta","meta.analysis",
            "genetic correlation","genetic architecture","genetic overlap",
            "ld score","ldsc","rg","heritab","snp heritab",
            "loci","susceptibility loci","novel loci","risk loci","locus",
            "polygenic risk","polygenic score","prs",
            "shared genetic","genetic sharing","genetic liability",
            "apoe","apoe4","apolipoprotein e","chromosome 19","chr19",
            "pleiotrop","cross-trait","cross trait","cross-phenotype",
            "genomic structural equation",
        ],
        "med": [
            "genetic","genomic","genome","variant","locus",
            "chromosome","gene","allele",
            "significant","p value","p.value","association",
            "discovery","identified","detected","found",
        ],
    }),
    ("5_Results_MR", {
        "weight": 1.5,
        "high": [
            "mendelian randomiz","mr estim","causal effect","causal relationship",
            "causal associat","causal link","bidirectional",
            "two.step","mediation","indirect effect","indirect",
            "mediator","mediated","mediating",
            "protein","proteom","pqtl","plasma prote","plasma level",
            "metabol","lipid","triglyceride","cholesterol","hdl","ldl",
            "inflammatory","inflammation","crp","interleukin","complement",
            "chemokine","cytokine","biomarker",
            "nfl","neurofilament","gfap","glial fibrillary",
            "tau","p-tau","p.tau","amyloid","a.beta",
            "drug target","therapeutic target","drug repurpos",
            "cross.ancestry","east asian","trans.ethnic","replicat",
            "education","educational attainment","cognitive",
            "protect","protective","risk","causal upstream",
        ],
        "med": [
            "mendelian","randomiz","mr","effect","estimate",
            "exposure","outcome","instrument",
            "plasma","blood","serum","biomarker",
            "mediation","indirect","pathway","mechanism",
        ],
    }),
    ("6_Results_Education_PheWAS", {
        "weight": 1.3,
        "high": [
            "education","educational attainment","school","years of education",
            "cognitive reserve","brain reserve","cognitive function",
            "phewas","phenome.wide","phewas","cross-phenotype",
            "parkinson","pd","multiple sclerosis","ms",
            "neuroprotect","protective factor","protective effect",
            "socioeconomic","ses","social","income",
        ],
        "med": [
            "education","cognitive","intelligence","iq",
            "protect","risk","associat",
        ],
    }),
    ("7_Discussion", {
        "weight": 1.6,
        "high": [
            "mechanism","pathway","biolog","molecular",
            "clinical","intervention","prevent","treatment","therap",
            "translat","translation","public health","policy",
            "implication","significance","meaning",
            "future direction","future research","remaining",
            "limitation","caution","interpret","careful",
            "cognitive reserve","neuroprotect","brain health",
            "shared liability","causal upstream","downstream",
            "recalibrat","revised","overturn","challenge existing",
            "generalizab","replicab","external valid",
            "population","general population","real.world",
            "biological","biology","clinical insigh",
        ],
        "med": [
            "discuss","conclusion","implication",
            "future","next step","remaining",
            "clinical","patient","treatment",
            "prevent","protect","intervention",
        ],
    }),
])

def classify(entry):
    text = (entry.get('TI','') + ' ' + entry.get('AB','')).lower()
    scores = {}
    for sec, rules in SECTIONS.items():
        w = rules.get('weight', 1.0)
        high_score = sum(2.0 for kw in rules.get('high',[]) if kw in text)
        med_score = sum(0.8 for kw in rules.get('med',[]) if kw in text)
        scores[sec] = w * (high_score + med_score)

    if max(scores.values()) == 0:
        return "8_Unclassified", 0.0

    best = max(scores, key=scores.get)
    best_score = scores[best]

    # Check if second-best is close
    sorted_s = sorted(scores.items(), key=lambda x: -x[1])
    if len(sorted_s) >= 2:
        second_score = sorted_s[1][1]
        if second_score > 0 and best_score / second_score < 1.3:
            # Close call - show dual assignment
            return f"{best}/{sorted_s[1][0]}", best_score

    return best, best_score

entries = parse_ris(RIS)

placement = []
for i, e in enumerate(entries):
    sec, score = classify(e)
    au = e.get('AU',['?'])[0].split(',')[0].strip() if e.get('AU') else '?'
    yr = e.get('PY','?')
    jt = e.get('JF','?')
    ti = e.get('TI','')[:75]
    doi = e.get('DO','?')
    placement.append((i+1, sec, score, au, yr, jt, ti, doi))

# Print by section
section_short = {
    "1_Methods_STATS": "Methods - Statistics",
    "2_Methods_DATA": "Methods - Data sources",
    "3_Intro_Background": "Introduction / Background",
    "4_Results_GWAS": "Results - GWAS / Genetic architecture",
    "5_Results_MR": "Results - MR / Mediation",
    "6_Results_Education_PheWAS": "Results - Education PheWAS",
    "7_Discussion": "Discussion / Implications",
    "8_Unclassified": "UNCLASSIFIED",
}

for sec_key in SECTIONS:
    sec_title = section_short.get(sec_key, sec_key)
    sec_entries = [p for p in placement if sec_key in p[1] and "Unclassified" not in p[1]]
    if not sec_entries:
        print(f"## {sec_title}: 0 refs")
        continue
    print(f"## {sec_title}: {len(sec_entries)} refs")
    print("-" * 90)
    for idx, s, score, au, yr, jt, ti, doi in sec_entries:
        dual = " [also: " + s.split("/")[1].replace("_"," ")[:4] + "..." + "]" if "/" in s else ""
        print(f"  [{idx:2d}] {au} ({yr}) {jt[:22]:22s} score={score:.1f}{dual}")
        print(f"       {ti}")
    print()

uncl = [p for p in placement if "Unclassified" in p[1]]
if uncl:
    print(f"## UNCLASSIFIED: {len(uncl)} refs")
    print("-" * 90)
    for idx, s, score, au, yr, jt, ti, doi in uncl:
        print(f"  [{idx:2d}] {au} ({yr}) {jt[:22]:22s}")
        print(f"       {ti}")
else:
    print("## UNCLASSIFIED: 0 - ALL REFERENCES CLASSIFIED ✓")

print()
counts = collections.Counter()
for p in placement:
    main_sec = p[1].split("/")[0]
    counts[section_short.get(main_sec, main_sec)] += 1

print("=" * 90)
print("FINAL SUMMARY:")
for sec in SECTIONS:
    st = section_short.get(sec, sec)
    print(f"  {st}: {counts.get(st, 0)} refs")
print(f"  TOTAL: {sum(counts.values())}")