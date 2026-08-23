# !/usr/bin/env python3
"""PubMed  -> RIS (insomnia-AD )

:
  python build_references.py          # :  PubMed,  RIS
  python build_references.py --pmids  #  PMID  RIS

: ./docs/historical/references.ris
"""
import time, json, sys, re, csv
import requests
from urllib.parse import quote

BASE = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/"
TOOL = "insomnia_ad_ref_builder"
EMAIL = "research@example.com"
OUT_RIS = "./docs/historical/references.ris"

KNOWN_PMIDS = {
    "Burgess2013_IVW": 23614981,        # Burgess et al. Genet Epidemiol 2013
    "Bowden2016_WM": 27061298,          # Bowden et al. Genet Epidemiol 2016 (weighted median)
    "Bowden2015_Egger": 26050253,       # Bowden et al. IJE 2015 (MR-Egger)
    "Hartwig2017_Mode": 28938752,       # Hartwig et al. IJE 2017 (weighted mode)
    "Verbanck2018_PRESSO": 29686387,    # Verbanck et al. Nat Genet 2018 (MR-PRESSO)
    "Hemani2018_MRBase": 29846171,      # Hemani et al. Elife 2018 (MR-Base / TwoSampleMR)
    "Morrison2020_CAUSE": 32989316,     # Morrison et al. Nat Genet 2020 (CAUSE)
    "Burgess2011_MVMR": 21300989,       # Burgess & Thompson. Stat Med 2011 (MVMR)
    "Sanderson2019_MVMR": 30452641,     # Sanderson et al. Stat Med 2019 (MVMR)
    "Mounier2023_MRlap": None,          # Mounier & Kutalik 2023 - need DOI search
    "Burgess2015_MVMR": 25411351,       # Burgess et al. IJE 2015 (multivariable MR)

    # LDSC / Genetic Correlation
    "BulikSullivan2015_LDSC1": 25642630,   # Bulik-Sullivan et al. Nat Genet 2015 (LDSC)
    "BulikSullivan2015_LDSC2": 25642631,   # Bulik-Sullivan et al. Nat Genet 2015 (rg)

    "Giambartolomei2014_coloc": 24830394, # Giambartolomei et al. PLoS Genet 2014

    "Kunkle2019_AD": 30820047,             # Kunkle et al. Nat Genet 2019
    "Bellenguez2022_AD": 35379992,         # Bellenguez et al. Nat Genet 2022
    "Lambert2013_AD": 24162737,            # Lambert et al. Nat Genet 2013 (IGAP)

    "Lane2019_Insomnia": 30804566,         # Lane et al. Nat Genet 2019
    "Jansen2019_Insomnia": 30804565,       # Jansen et al. Nat Genet 2019

    "Lee2018_Edu": 30038396,               # Lee et al. Nat Genet 2018
    "Okbay2022_Edu": 35361970,             # Okbay et al. Nat Genet 2022

    "Sun2023_UKBPPP": 37794188,            # Sun et al. Nature 2023 (UKB-PPP)
    "Sun2018_INTERVAL": 29875488,          # Sun et al. Nature 2018 (INTERVAL)
    "Zheng2020_protMR": 33020668,          # Zheng et al. Nat Genet 2020

    "Lawlor2016_Triangulation": 27342221,  # Lawlor et al. IJE 2016
    "Munafo2018_Nature": 29474905,         # Munafo & Davey Smith. Nature 2018
    "DaveySmith2003_MRreview": 12689998,   # Davey Smith & Ebrahim. IJE 2003

    "STROBE_MR_2021": 34698778,            # Skrivankova et al. JAMA 2021

    # Insomnia-AD literature
    "KorologouLinden2022_AD_PheWAS": 35953482,  # AD PheWAS+MR Nat Commun 2022
    "Shi2018_insomnia_cognitive": 29445277,      # Insomnia -> cognitive decline MR
    "Henry2022_insomnia_AD_MR": None,             # need search

    "Hemani2017_Steiger": None,            # Hemani et al. 2017 Steiger

    "R_Core_2023": None,                   # R Core Team
}

SEARCH_QUERIES = {
    "insomnia_AD_MR": '("insomnia"[tiab] OR "sleep"[tiab]) AND ("Alzheimer"[tiab] OR "dementia"[tiab]) AND "Mendelian randomization"[tiab] AND (2019:2026[pdat])',
    "education_AD_protection_MR": '("educational attainment"[tiab] OR "education"[tiab]) AND ("Alzheimer"[tiab]) AND "Mendelian randomization"[tiab]',
    "comorbidity_triangulation_MR": '("comorbidity"[tiab] OR "multimorbidity"[tiab]) AND "Mendelian randomization"[tiab] AND "triangulation"[tiab]',
    "protein_mediation_MR": '("plasma protein"[tiab] OR "proteomic"[tiab]) AND "mediation"[tiab] AND "Mendelian randomization"[tiab] AND (2020:2026[pdat])',
    "APOE_genetic_overlap": '("APOE"[tiab] OR "APOE4"[tiab]) AND ("genetic correlation"[tiab] OR "pleiotropy"[tiab]) AND "Alzheimer"[tiab]',
    "LD_clump_sensitivity_MR": '("LD clump"[tiab] OR "LD prun"[tiab] OR "instrument selection"[tiab]) AND "Mendelian randomization"[tiab] AND "sensitivity"[tiab]',
    "EA_cross_ancestry_MR": '("East Asian"[tiab] OR "cross-ancestry"[tiab]) AND "education"[tiab] AND "Mendelian randomization"[tiab]',
}


def eutils(endpoint, params, retries=3):
    url = BASE + endpoint
    params["tool"] = TOOL
    params["email"] = EMAIL
    for attempt in range(retries):
        try:
            r = requests.get(url, params=params, timeout=30)
            r.raise_for_status()
            if "esearch" in endpoint:
                return r.json()
            return r.text
        except Exception as e:
            if attempt == retries - 1:
                print(f"  [ERR] {endpoint}: {e}")
                return None
            time.sleep(2 ** attempt)


def search_pubmed(query, retmax=30):
    """ESearch -> PMID """
    params = {"db": "pubmed", "term": query, "retmax": retmax,
              "retmode": "json", "sort": "relevance", "usehistory": "n"}
    data = eutils("esearch.fcgi", params)
    if not data or "esearchresult" not in data:
        return []
    return data["esearchresult"]["idlist"]


def fetch_pubmed_records(pmids):
    """EFetch -> MEDLINE """
    if not pmids:
        return ""
    params = {"db": "pubmed", "id": ",".join(str(p) for p in pmids),
              "rettype": "medline", "retmode": "text"}
    return eutils("efetch.fcgi", params) or ""


def parse_medline_to_ris(medline_text):
    """ MEDLINE  RIS """
    entries = []
    current = {}
    for line in medline_text.split("\n"):
        if line.strip() == "":
            if current:
                entries.append(current)
                current = {}
            continue
        if line.startswith(" "):  # continuation line
            continue
        tag = line[:4].strip()
        val = line[6:].strip()
        if tag == "PMID":
            current["PMID"] = val
        elif tag == "TI":
            current["TI"] = (current.get("TI", "") + " " + val).strip()
        elif tag == "AU":
            current.setdefault("AU", []).append(val)
        elif tag == "TA":
            current["JT"] = val
        elif tag == "DP":
            current["PY"] = val[:4]
        elif tag == "VI":
            current["VI"] = val
        elif tag == "IP":
            current["IP"] = val
        elif tag == "PG":
            current["PG"] = val
        elif tag == "AB":
            current["AB"] = (current.get("AB", "") + " " + val).strip()
        elif tag == "AID":
            if "[doi]" in val:
                current["DOI"] = val.replace(" [doi]", "")
    if current:
        entries.append(current)
    return entries


def ris_from_record(r):
    """ MEDLINE  RIS """
    ris = []
    ris.append("TY  - JOUR")
    ris.append(f"TI  - {r.get('TI', 'N/A')}")
    authors = r.get("AU", [])
    for au in authors:
        ris.append(f"AU  - {au}")
    ris.append(f"PY  - {r.get('PY', '')}")
    if "JT" in r:
        ris.append(f"JF  - {r['JT']}")
    if "VI" in r:
        ris.append(f"VL  - {r['VI']}")
    if "IP" in r:
        ris.append(f"IS  - {r['IP']}")
    if "PG" in r:
        ris.append(f"SP  - {r['PG']}")
    if "AB" in r:
        ab = r["AB"][:2000]  # truncate very long abstracts
        ris.append(f"AB  - {ab}")
    if "DOI" in r:
        ris.append(f"DO  - {r['DOI']}")
    ris.append(f"AN  - {r.get('PMID', '')}")
    ris.append(f"DB  - PubMed")
    ris.append("ER  - ")
    return "\n".join(ris)


def main():
    all_pmids = set()
    all_records = {}

    known = [p for p in KNOWN_PMIDS.values() if p is not None]
    print(f"Phase 1: fetching {len(known)} known PMIDs...")
    for i in range(0, len(known), 50):
        batch = known[i:i+50]
        txt = fetch_pubmed_records(batch)
        recs = parse_medline_to_ris(txt)
        for r in recs:
            all_records[r["PMID"]] = r
            all_pmids.add(r["PMID"])
        time.sleep(0.35)
    print(f"  -> {len(all_records)} records from known PMIDs")

    for label, query in SEARCH_QUERIES.items():
        print(f"Phase 2: searching '{label}'...")
        pmids = search_pubmed(query, retmax=15)
        new = [p for p in pmids if p not in all_pmids]
        print(f"  -> {len(pmids)} results, {len(new)} new")
        if new:
            for i in range(0, len(new), 20):
                batch = new[i:i+20]
                txt = fetch_pubmed_records(batch)
                recs = parse_medline_to_ris(txt)
                for r in recs:
                    all_records[r["PMID"]] = r
                    all_pmids.add(r["PMID"])
                time.sleep(0.35)

    print(f"\nTotal unique PMIDs collected: {len(all_pmids)}")

    with open(OUT_RIS, "w", encoding="utf-8") as f:
        for pmid in sorted(all_pmids, key=lambda x: int(x)):
            r = all_records[pmid]
            f.write(ris_from_record(r) + "\n")
    print(f"RIS written to {OUT_RIS}")

    missing_doi = [pmid for pmid, r in all_records.items() if "DOI" not in r]
    missing_ab = [pmid for pmid, r in all_records.items() if "AB" not in r or len(r["AB"]) < 30]
    print(f"\nQuality report:")
    print(f"  Missing DOI: {len(missing_doi)} ({', '.join(missing_doi[:10])}...)")
    print(f"  Missing/short abstract: {len(missing_ab)} ({', '.join(missing_ab[:10])}...)")
    
    print(f"\nCategory counts (known PMIDs matched):")
    for label, pmid in KNOWN_PMIDS.items():
        if pmid and str(pmid) in all_records:
            r = all_records[str(pmid)]
            print(f"  [{label}] {r.get('AU',['?'])[0] if r.get('AU') else '?'} ({r.get('PY','?')}) - {r.get('TI','N/A')[:70]}...")
        elif pmid is None:
            print(f"  [{label}] (PMID unknown - needs manual lookup)")

if __name__ == "__main__":
    main()