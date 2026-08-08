import xml.etree.ElementTree as ET, os, re

SRC = "课题设计阶段/GM_reference/Leyden2025_GenomeMed_model_fulltext.xml"
OUT = "课题设计阶段/GM_reference/Leyden2025_GenomeMed_model_READABLE.md"

def ln(t): return t.tag.split('}')[-1]

def text_of(el):
    # full text of an element excluding nested <sec>/<title> children-of-sec
    # We collect direct text + descendant text but skip <sec> subtrees (handled recursively)
    parts = []
    # direct text before children
    if el.text:
        parts.append(el.text)
    for ch in list(el):
        if ln(ch) in ('sec',):
            # do not descend into nested secs here
            if ch.tail:
                parts.append(ch.tail)
            continue
        if ln(ch) == 'title':
            # include title text only when explicitly wanted (handled by caller)
            if ch.tail:
                parts.append(ch.tail)
            continue
        parts.append(text_of(ch))
        if ch.tail:
            parts.append(ch.tail)
    s = "".join(parts)
    # normalize whitespace
    s = re.sub(r'\s+', ' ', s).strip()
    return s

def sec_title(sec):
    t = sec.find('title')
    if t is None:
        return None
    return text_of(t)

def emit_sec(sec, depth, out):
    title = sec_title(sec)
    hashes = '#' * (2 + depth)
    if title:
        out.append(f"{hashes} {title}\n")
    else:
        out.append(f"{hashes} (untitled section)\n")
    # paragraphs directly under this sec (not inside sub-sec)
    for ch in list(sec):
        if ln(ch) == 'p':
            txt = text_of(ch)
            if txt:
                out.append(f"{txt}\n")
        elif ln(ch) in ('fig','table-wrap','disp-formula','boxed-text','supplementary-material'):
            cap = ch.find('.//caption')
            if cap is not None:
                out.append(f"*[Figure/Table]*: {text_of(cap)}\n")
    out.append("")
    for sub in sec.findall('sec'):
        emit_sec(sub, depth+1, out)

tree = ET.parse(SRC)
root = tree.getroot()
art = root if ln(root)=='article' else root.find('article')
fm = art.find('front/article-meta')

out = []
# Title
title_el = fm.find('title-group/article-title')
if title_el is not None:
    out.append(f"# {text_of(title_el)}\n")
art_type = art.get('article-type')
out.append(f"*(Genome Medicine model article — article-type: **{art_type}**; DOI 10.1186/s13073-025-01472-2; PMID 40375348; PMCID PMC12079859)*\n")

# Authors
contribs = fm.findall('.//contrib[@contrib-type="author"]/name')
names = []
for c in contribs:
    gn = c.findtext('given-names','')
    sn = c.findtext('surname','')
    if gn or sn:
        names.append(f"{gn} {sn}".strip())
if names:
    out.append(f"**Authors:** {', '.join(names)}\n")

# Abstract
ab = art.find('.//abstract')
if ab is not None:
    out.append("## Abstract\n")
    secs = ab.findall('sec')
    if secs:
        for s in secs:
            emit_sec(s, 0, out)
    else:
        for p in ab.findall('p'):
            out.append(text_of(p)+"\n\n")

# Keywords
kw = fm.find('kwd-group')
if kw is not None:
    kws = [text_of(k) for k in kw.findall('kwd')]
    kws = [k for k in kws if k]
    if kws:
        out.append(f"**Keywords:** {', '.join(kws)}\n")

# Body
body = art.find('.//body')
if body is not None:
    for sec in body.findall('sec'):
        emit_sec(sec, 0, out)

# Back: declarations, acknowledgements, funding, availability, authors contributions, references
back = art.find('.//back')
if back is not None:
    for sec in back.findall('sec'):
        emit_sec(sec, 0, out)
    # references
    reflist = back.find('ref-list')
    if reflist is not None:
        out.append("## References\n")
        for i, ref in enumerate(reflist.findall('ref'), 1):
            # mixed citation
            cit = ref.find('mixed-citation') or ref.find('element-citation')
            if cit is not None:
                txt = text_of(cit)
            else:
                txt = text_of(ref)
            out.append(f"{i}. {txt}\n")

text = "\n".join(out)
# collapse excessive blank lines
text = re.sub(r'\n{3,}', '\n\n', text)
with open(OUT, 'w', encoding='utf-8') as f:
    f.write(text)
print("Wrote", OUT, "chars=", len(text))
