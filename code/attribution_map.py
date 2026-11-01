#!/usr/bin/env python3
"""
Attribution of every difference between the submitted manuscript and the
revision to a specific reviewer comment.

Two rules govern the map:

  REV    the difference answers a numbered comment (R1-1 ... R3-12), and the
         response letter names this location in that comment's "Changes:" line
         or describes this content in its response body.
  FMT    the difference is a journal/technical requirement (Frontiers first-page
         counts, AI-use declaration, figure width note, contact details). Not a
         reviewer request, so it must not be highlighted as a reply.
  ED     the difference is editorial: wording tightened, a heading split out, a
         cross-reference added. Nothing asked for it. This is the category to
         look at if the revision is to be narrowed to reviewer-driven changes
         only, because each entry can be reverted without losing an answer.
  NOISE  the difference is an artefact of the markdown -> docx conversion
         (list numbering, bullet glyphs, escaped markup, superscript flattened
         to plain digits, double hyphen to en dash) or of block alignment.
         Nothing to answer, nothing to show.

Keys are paragraph indices in `manuscript_Frontiers_Methods_v2.docx`. Each
entry carries the paragraph's leading text so that the map fails loudly if the
document is rebuilt and the indices move.

Comment topics are copied from reviews/Response_to_Reviewers_Frontiers.md so
the index can be read without opening the response letter.
"""

TOPIC = {
    "R1-1": "Scoring rules inconsistent across text, Table 1 and S8; G2 failure could still reach Grade A",
    "R1-2": "Archived simulation code differs from the described workflow",
    "R1-3": "What the framework adds beyond routine LD handling",
    "R1-4": "Sensitivity/specificity definitions; Grade C; uncertainty; the 0.20 threshold; effect mix",
    "R1-5": "Insufficient evidence is not evidence against",
    "R1-6": "Chromosome 19 is not the APOE region; region definition; how 32 and 47 were selected",
    "R1-7": "'Three null results' contradicts a negative direct effect; CAUSE inputs",
    "R1-8": "Conditional instrument strength; confounder handling; mediation details",
    "R1-9": "Evidence behind the external-validation scores; kappa is not causal accuracy",
    "R1-10": "From risk factors to drug targets",
    "R3-1": "Harmonise terminology for directional and causal claims",
    "R3-2": "What 'precise' means",
    "R3-3": "European LD reference panel applied to East Asian data",
    "R3-4": "Rationale for r2 < 0.001 with a 10,000-kb window (Methods corrected)",
    "R3-5": "Do the three corrections act in sequence on the variant set",
    "R3-6": "How confounders were chosen; why F > 10 sits at G4",
    "R3-7": "Power comparability across ancestries; cross-ancestry bias",
    "R3-8": "Where MR-Egger, Cochran's Q, MRlap and CAUSE sit in the framework",
    "R3-9": "Justification of the simulation parameter grid",
    "R3-10": "Definition and algorithm of trans-ethnic re-clumping",
    "R3-11": "Do not describe a null r_g as 'unchanged'",
    "R3-12": "Three-line tables without vertical rules",
}

# index -> (category, payload, why)
#   REV:  payload is a tuple of comment ids
#   FMT:  payload is None
#   NOISE: payload is None
# `head` is asserted against the paragraph's opening characters.
MAP = {
    0:   ("REV", ("R1-2",), "Title: '43,200-simulation validation' -> 'a 43,200-replicate benchmark of its scoring rule'; 'Correcting' -> 'diagnosing'", "A six-gate"),
    2:   ("NOISE", None, "affiliation line: one whitespace character", "1 Department"),
    4:   ("NOISE", None, "correspondence line: escaped asterisk lost in conversion", "Correspondence:"),
    5:   ("FMT", None, "first-page word/figure/table count required by the Frontiers author guidelines", "Word count:"),
    6:   ("FMT", None, "article type declaration required by the submission system", "Article type:"),
    8:   ("REV", ("R1-2", "R3-1", "R3-2"), "Abstract: claims narrowed to 'the scoring rule', 'precise' replaced, association/causal claim separated", "Mendelian randomization (MR) uses germline"),
    9:   ("REV", ("R1-2", "R1-4"), "Abstract: benchmark characterised as proxy gate implementations; operating-characteristic language aligned", "We evaluated the framework"),
    12:  ("REV", ("R3-1", "R3-2"), "Introduction: 'precise' unpacked into statistical significance vs information; causal-claim terminology", "Mendelian randomization uses germline"),
    14:  ("REV", ("R1-2", "R1-4"), "Introduction: what is characterised is the scoring rule under proxy gates; specificity/sensitivity named as the operating characteristics", "Addressing this problem"),
    15:  ("REV", ("R1-2",), "Introduction: 'its operating characteristics' -> 'the operating characteristics of its scoring rule'", "Two structural properties"),
    16:  ("REV", ("R1-2",), "Introduction: 'LD concentration' -> granularity of the clumping partition, which is what the simulation actually varies", "We benchmark the framework"),
    19:  ("REV", ("R1-2",), "Software environment: pinned requirement set with versions, as asked under the reproducibility comment", "Software environment."),
    21:  ("NOISE", None, "bullet glyph inserted by the markdown converter", "\u2022"),
    22:  ("NOISE", None, "bullet glyph inserted by the markdown converter", "\u2022"),
    23:  ("NOISE", None, "bullet glyph inserted by the markdown converter", "\u2022"),
    24:  ("NOISE", None, "bullet glyph inserted by the markdown converter", "\u2022"),
    25:  ("NOISE", None, "bullet glyph inserted by the markdown converter", "\u2022"),
    26:  ("NOISE", None, "bullet glyph inserted; underscore dropped", "\u2022"),
    27:  ("NOISE", None, "bullet glyph inserted by the markdown converter", "\u2022"),
    28:  ("NOISE", None, "bullet glyph inserted by the markdown converter", "\u2022"),
    32:  ("REV", ("R1-2",), "Archived framework: version DOI 10.5281/zenodo.21858125 -> 23733172 (v1.2.1)", "Archived framework."),
    35:  ("REV", ("R3-1",), "New Methods paragraph defining causal claim / association / directed effect", "Terminology."),
    36:  ("REV", ("R1-2", "R3-1"), "Framing: benchmark 'through proxy gate implementations', score-to-grade mapping, causal-claim wording", "The framework converts"),
    39:  ("REV", ("R1-1",), "Gate G1: stated as a binary screening gate with no partial credit", "Gate G1"),
    40:  ("REV", ("R3-4", "R1-3", "R1-9"), "Gate G2: primary clumping tier corrected to r2 < 0.1 with the stricter tier as sensitivity; instrument-tier sensitivity and the exploratory height->AD run introduced", "Gate G2"),
    41:  ("REV", ("R1-7", "R3-5", "R3-8"), "New paragraph: only clumping changes the instrument set; Egger/Q/median/mode are diagnostics on the clumped set", "What each correction operates on."),
    42:  ("REV", ("R1-1",), "Gate G3: scoring rule for the not-evaluable case (1 when rg is direction-consistent but colocalization was not run)", "Gate G3"),
    43:  ("REV", ("R1-8", "R3-6"), "Gate G4: conditional vs unconditional F separated, confounder selection and the reporting gap stated", "Gate G4"),
    44:  ("REV", ("R1-8",), "Gate G5: 36 versus 25 proteins, the clumping rule and the scope of the null result", "Gate G5"),
    45:  ("REV", ("R1-9", "R3-3", "R3-7"), "Gate G6: direction concordance alone is not validation; no ancestry-matched panel; power not comparable", "Gate G6"),
    46:  ("REV", ("R3-3", "R3-7", "R3-10"), "New paragraph: trans-ethnic re-clumping algorithm and what happens without an ancestry-matched panel", "Trans-ethnic re-clumping."),
    48:  ("REV", ("R1-1",), "Grading rubric: single 0/1/2 scheme, binary G1/G6, decisive-failure cap, not-evaluable scores 0", "Cumulative scores range"),
    51:  ("NOISE", None, "list number and superscript flattened by the converter", "1."),
    52:  ("NOISE", None, "list item reflow after the numbering was added", "2."),
    53:  ("REV", ("R3-4",), "Protocol step 3: clumping threshold corrected from r2 < 0.001 to r2 < 0.1", "3."),
    54:  ("NOISE", None, "list item reflow after the numbering was added", "4."),
    55:  ("NOISE", None, "list item reflow after the numbering was added", "5."),
    56:  ("NOISE", None, "list item reflow after the numbering was added", "6."),
    57:  ("NOISE", None, "list item reflow after the numbering was added", "7."),
    59:  ("REV", ("R1-2", "R3-9"), "Simulation: actual data-generating process stated, G3/G4 degeneracy and absent methods declared; parameter grid justified", "Because the framework is prescriptive"),
    60:  ("REV", ("R1-2", "R3-9"), "Simulation: archived-code pointer and parameter provenance", "The full data-generating process"),
    62:  ("REV", ("R1-2",), "Results subheading: '43,200-simulation benchmark' -> 'the scoring rule'", "Operating characteristics of the scoring rule"),
    63:  ("REV", ("R1-2", "R1-4"), "Operating characteristics: scoring rule rather than framework; D-only convention named", "At the null"),
    68:  ("REV", ("R1-7", "R3-5", "R3-4"), "Results G2: three analyses separated instead of pooled as 'null'; CAUSE/MRlap inputs; clumping tier", "G2: robustness."),
    69:  ("REV", ("R1-3", "R3-2", "R3-4"), "New Results subsection: three instrument tiers, SE inflation, what LD correction changes", "What LD correction changes"),
    70:  ("REV", ("R1-6", "R3-11"), "Results G3: APOE region defined, chromosome-19 exclusion withdrawn as APOE-specific; r_g described as null, not unchanged", "G3: genetic architecture."),
    71:  ("REV", ("R1-8",), "Results G4: conditional F gap declared, first-stage statistics reported, mediation denominators", "G4: direct effect."),
    72:  ("REV", ("R1-8",), "Results G5: 25 evaluable proteins, both path estimates, 9.5% mediation, scope of the null", "G5: biological mediation."),
    73:  ("REV", ("R1-9", "R3-3", "R3-7"), "Results G6: evidence per score, withdrawn points, European panel on East Asian data, power", "G6: external validation."),
    76:  ("REV", ("R1-2",), "'framework' -> 'scoring rule' in the precision sentence", "The benchmarked operating characteristics"),
    77:  ("REV", ("R1-5",), "New Results subsection: insufficient evidence versus evidence against", "Insufficient evidence versus evidence against."),
    78:  ("NOISE", None, "lead-in sentence split out of the preceding paragraph by the converter", "Principal operational challenges"),
    79:  ("NOISE", None, "list number inserted by the converter", "1."),
    80:  ("NOISE", None, "list number inserted by the converter", "2."),
    81:  ("NOISE", None, "list number inserted by the converter", "3."),
    82:  ("NOISE", None, "list number inserted by the converter", "4."),
    83:  ("NOISE", None, "list number inserted by the converter", "5."),
    85:  ("REV", ("R1-2",), "Discussion: 'operating characteristics derived from' -> 'of its scoring rule'", "The insomnia\u2013AD findings"),
    86:  ("REV", ("R1-2", "R1-4"), "Discussion: scoring rule rather than framework; FDR figures updated after the cap was applied", "The APOE result"),
    87:  ("ED", None, "section heading split out and a STROBE-MR cross-reference added; neither reviewer asked for it", "Complementarity with reporting standards."),
    88:  ("ED", None, "section heading split out and the wording tightened; neither reviewer asked for it", "Generalizability of the template."),
    89:  ("REV", ("R1-10",), "Discussion: trait-level claim -> target requires cis-pQTL, tissue, direction of modulation, safety", "Implications for drug-target prioritization."),
    90:  ("REV", ("R1-2", "R1-4", "R1-5", "R1-8", "R1-9", "R3-3", "R3-7"), "Limitations: proxy implementation, FDR vs null fraction, insufficient vs against, conditional F gap, G6 evidence, LD mismatch, power", "Limitations."),
    91:  ("REV", ("R1-2",), "Conclusions: claim narrowed to the scoring rule under proxy gates", "Conclusions."),
    93:  ("REV", ("R1-2",), "Data availability: version DOI 10.5281/zenodo.21858125 -> 23733172", "Data availability statement."),
    98:  ("FMT", None, "AI-use declaration: tool names and version removed per the journal policy; not requested by either reviewer", "Use of AI."),
    99:  ("REV", ("R1-1", "R1-3"), "Supplementary material: new tables S10-S12 listed", "Supplementary material."),
    144: ("FMT", None, "Figure 1 legend: note on the 180 mm width and the generator script; journal figure specification, not a reviewer request", "Figure 1."),
    145: ("REV", ("R1-4", "R1-2"), "Figure 2 legend: both specificity conventions, recomputed under the decisive-failure cap", "Figure 2."),
    146: ("FMT", None, "Figure 3 legend: expanded panel description after the figure was redrawn for the 180 mm specification", "Figure 3."),
    147: ("FMT", None, "Figure 4 legend: expanded panel description after the figure was redrawn for the 180 mm specification", "Figure 4."),
    148: ("FMT", None, "Figure 5 legend: expanded panel description after the figure was redrawn for the 180 mm specification", "Figure 5."),
    150: ("REV", ("R1-1",), "Table 1 caption: two-layer gate specification", "Table 1."),
    152: ("REV", ("R1-1", "R1-2", "R1-7", "R3-8"), "Table 1 footnote: scoring tiers, decisive failure, CAUSE as diagnostic not scoring input", "All gates apply fixed a priori thresholds"),
    153: ("REV", ("R1-2", "R1-4"), "Table 2 caption: scoring rule under proxy gate implementations", "Table 2."),
    155: ("REV", ("R1-2", "R1-4"), "Table 2 footnote: recomputation under the cap, Wilson intervals, both specificity conventions", "Values are marginal"),
}

# table index (0-based) -> default attribution for every changed cell
TABLE_MAP = {
    0: (("R1-1",), "Table 1 rebuilt as a six-column, two-layer table (empirical criterion + proxy implementation)"),
    1: (("R1-4", "R1-2"), "Table 2: specificity added under both conventions, interval columns, values recomputed under the decisive-failure cap"),
}
# table index -> {(row, col): (ids, why)} for individual cells
TABLE_CELL_MAP = {
    3: {(3, 2): (("R3-4",), "Table 4 step 3: clumping threshold corrected to r2 < 0.1 with the stricter tier as sensitivity")},
}

# per-column refinement, so that a recomputed number is not filed under the
# comment that asked for a formatting change and vice versa. Falls back to
# TABLE_MAP when the column is not listed.
TABLE_COL_MAP = {
    # Table 2 columns (0-based): 2 sensitivity, 3 specificity D-only,
    # 4 specificity C+D (new), 5 P(Grade A), 6 FDR
    1: {2: ("R1-2",), 3: ("R1-4",), 4: ("R1-4",), 6: ("R1-2",)},
}

# Findings that came out of building the map, reported with the index so they
# are not lost between sessions. These are observations about the pair of
# documents, not attributions.
NOTES = [
    "R1-6 is answered in the Results G3 paragraph only. The response letter's "
    "Changes line also claims a Discussion change, but the Discussion contains no "
    "sentence withdrawing the APOE-specific reading - either add one or correct "
    "the letter.",

    "The markdown converter flattens typography the submitted .docx had right: "
    "r2 for r-squared, rg for r_g, 10-8 for 10^-8, and -- for an en dash. These "
    "are not revisions and are therefore not highlighted, but they read as "
    "regressions in a resubmission and should be repaired in the source.",

    "Table 1 (4 to 6 columns) and Table 2 (6 to 7 columns) are attributed to the "
    "comments that asked for the restructure, R1-1 and R1-4. In Table 2 the value "
    "columns are attributed to R1-2 instead, because the numbers moved when the "
    "benchmark was re-scored with the decisive-failure rule.",

    "R3-12 leaves no highlighted text: it is satisfied by the three-line cell "
    "borders that md_to_docx_frontiers.py already draws, which this build checks "
    "on all five tables rather than re-applies.",
]
