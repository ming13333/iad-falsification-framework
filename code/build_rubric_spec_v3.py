# -*- coding: utf-8 -*-
"""
Emit the single authoritative rubric specification (v3).

Two layers per gate:
  empirical_*  the pre-specified operational criterion applied to real data
  sim_proxy_*  what the 43,200-replicate simulation actually implements
               (a proxy; the benchmark validates the scoring-to-grade mapping,
                not LDSC / coloc / MVMR / CAUSE / MRlap themselves)

Any residual discrepancy between the two layers is disclosed in the
manuscript footnote rather than resolved by changing scores.

Run: python code/build_rubric_spec_v3.py
"""

import csv
import os

OUT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                   "output", "results", "Validation")
os.makedirs(OUT, exist_ok=True)

ROWS = [
    dict(
        gate="G1", name="Association screening", failure_mode="No association / instrument-count artefact",
        empirical_2="Unclumped IVW nominally significant (P<0.05) in the claimed direction",
        empirical_1="not used - gate is strictly binary in v3",
        empirical_0="P>=0.05, or significant in the opposite direction",
        not_evaluable="<3 instruments: score 0",
        cascade="L1=0 -> G2-G6 uninformative -> total score 0, Grade D",
        sim_proxy_2="IVW P<0.05 and |b|>1e-4",
        sim_proxy_1="0.05<=P<0.20",
        sim_proxy_0="P>=0.20",
        sim_gap="Simulation does not test the direction of the estimate and retains a 1-point tier (the version originally coded).",
        code_ref="sim_framework_operating_chars.py L127-131",
    ),
    dict(
        gate="G2", name="Robustness to LD / overlap / pleiotropy", failure_mode="LD-driven precision; directional pleiotropy",
        empirical_2="Clumped IVW significant in claimed direction AND MR-Egger intercept P>=0.05 AND Cochran Q P>=0.05",
        empirical_1="Clumped IVW significant in claimed direction, but >=1 of {Egger intercept, Cochran Q, weighted median concordance} fails",
        empirical_0="Clumped IVW null or directionally reversed; or all diagnostics fail",
        not_evaluable="<3 clumped instruments: score 0",
        cascade="None",
        sim_proxy_2="Clumped IVW P<0.05 and Egger intercept P>0.05",
        sim_proxy_1="Clumped IVW P<0.05 (intercept fails)",
        sim_proxy_0="Clumped IVW P>=0.05",
        sim_gap="Cochran Q and weighted median are not computed in the simulation; only the intercept and clumped P drive the proxy score.",
        code_ref="sim_framework_operating_chars.py L133-141",
    ),
    dict(
        gate="G3", name="Genetic architecture", failure_mode="Locus-confined sharing masquerading as systemic causality",
        empirical_2="Genome-wide r_g direction-consistent with the claim (or null) AND coloc PP.H4>=0.80 at the expected region",
        empirical_1="r_g direction-consistent (or null) but colocalization not performed or PP.H4<0.80",
        empirical_0="r_g significant in the opposite direction, or architecture contradicts the claim",
        not_evaluable="LDSC or coloc not runnable (insufficient SNP overlap / no regional data): score 0",
        cascade="None",
        sim_proxy_2=">=50% of LD blocks retained after clumping and >=5 independent instruments",
        sim_proxy_1=">=30% of LD blocks retained",
        sim_proxy_0="<30% of LD blocks retained",
        sim_gap="Proxy measures signal spread across simulated blocks only; it is not LDSC r_g or coloc and cannot detect APOE-type confinement.",
        code_ref="sim_framework_operating_chars.py L143-146",
    ),
    dict(
        gate="G4", name="Direct effect", failure_mode="Effect mediated by a correlated exposure",
        empirical_2="MVMR direct effect significant in the claimed direction with conditional F>10 (where conditional F was not retrieved, the score rests on effect significance and direction; flagged in the case table)",
        empirical_1="MVMR informative but the direct effect is not significant, is directionally reversed, or the model was not reported (labelled per cell in S8-v3)",
        empirical_0="Conditional F<=10 (weak instruments) with no usable direct effect; or direct effect absent",
        not_evaluable="Conditional F<=10: score 0",
        cascade="None",
        sim_proxy_2="Clumped IVW P<0.05 and leave-one-out spread <0.50",
        sim_proxy_1="Clumped IVW P<0.05",
        sim_proxy_0="Clumped IVW P>=0.05",
        sim_gap="Leave-one-out stability is used as a proxy; no confounder adjustment and no conditional F are simulated, so G4 is collinear with G2 in the benchmark.",
        code_ref="sim_framework_operating_chars.py L148-158",
    ),
    dict(
        gate="G5", name="Biological mediation", failure_mode="Claim rests on a mediator that is not on the causal path",
        empirical_2="FDR-corrected indirect effect consistent with the claim (bootstrap CI excluding 0)",
        empirical_1="Only one of the two mediation steps is significant",
        empirical_0="Neither step significant, or the indirect effect runs opposite to the claim",
        not_evaluable="No evaluable mediator after instrument filtering: score 0",
        cascade="None",
        sim_proxy_2="Both exposure->mediator and mediator->outcome P<0.05",
        sim_proxy_1="Exactly one of the two steps P<0.05",
        sim_proxy_0="Neither step P<0.05",
        sim_gap="Simulated mediator effects are drawn from the same genotype, so mediation is generated rather than inferred; no FDR control or bootstrap is applied.",
        code_ref="sim_framework_operating_chars.py L160-165",
    ),
    dict(
        gate="G6", name="External validation", failure_mode="Signal not reproducible outside the discovery sample",
        empirical_2="Cross-ancestry replication that is directionally consistent in the claimed direction AND nominally significant (P<0.05) at achieved power >= 80%",
        empirical_1="not used - gate is strictly binary in v3",
        empirical_0="No independent-ancestry replication, direction inconsistent, null replication at adequate power, or achieved power < 80%",
        not_evaluable="Power <80% or no independent-ancestry data: score 0 (directional screen only). A null replication at adequate power is a failed replication, not a partial success.",
        cascade="None",
        sim_proxy_2="Independent-sample IVW P<0.05 and direction concordant with the clumped estimate",
        sim_proxy_1="not used - gate is strictly binary",
        sim_proxy_0="P>=0.05 or direction discordant",
        sim_gap="Simulation draws a second independent sample from the same population; it cannot represent cross-ancestry replication or power thresholds.",
        code_ref="sim_framework_operating_chars.py L167-171",
    ),
]

MAPPING = [
    dict(item="grade_A", rule="total score >= 10", note="boundary sensitivity reported in S8-v3 summary"),
    dict(item="grade_B", rule="7 <= total score <= 9", note=""),
    dict(item="grade_C", rule="4 <= total score <= 6", note=""),
    dict(item="grade_D", rule="total score <= 3", note=""),
    dict(item="max_score", rule="12 (six gates x 2)", note="0/1/2 per gate in the empirical layer"),
    dict(item="benchmark_scope", rule="proxy DGP", note="validates the scoring-to-grading map, not the gate implementations"),
]

path = os.path.join(OUT, "rubric_spec_v3.csv")
with open(path, "w", newline="", encoding="utf-8-sig") as f:
    w = csv.DictWriter(f, fieldnames=list(ROWS[0].keys()))
    w.writeheader()
    w.writerows(ROWS)

path2 = os.path.join(OUT, "rubric_grade_mapping_v3.csv")
with open(path2, "w", newline="", encoding="utf-8-sig") as f:
    w = csv.DictWriter(f, fieldnames=list(MAPPING[0].keys()))
    w.writeheader()
    w.writerows(MAPPING)

print("wrote", path)
print("wrote", path2)
for r in ROWS:
    print(f"  {r['gate']}: 2-point = {r['empirical_2'][:70]}...")
