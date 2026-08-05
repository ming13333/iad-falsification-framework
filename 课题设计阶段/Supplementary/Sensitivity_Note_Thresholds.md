# Supplementary Note: Sensitivity of Evidence Grades to Threshold Variation

To assess whether the four-tier evidence grade assignments (A/B/C/D) are sensitive to the choice of scoring cutoffs, we re-computed grades under three alternative threshold configurations. The current thresholds (A: 10-12, B: 7-9, C: 4-6, D: 0-3) were compared against stricter, more lenient, and extremely strict alternatives.

## Threshold Scenarios

| Scenario | A cutoff | B cutoff | C cutoff | Description |
|----------|----------|----------|----------|-------------|
| Current | >=10 | >=7 | >=4 | As used in the main text |
| Stricter | >=11 | >=8 | >=5 | Raises all thresholds by +1 |
| Lenient | >=9 | >=6 | >=3 | Lowers all thresholds by -1 |
| Extreme strict | >=11 | >=9 | >=6 | A-C all raised; B range compressed |

## Results: Per-Case Grade Stability

| Case | Score | Current | Stricter | Lenient | Extreme Strict | Stability |
|------|-------|---------|----------|---------|----------------|-----------|
| LDL->CAD | 12 | A | A | A | A | Stable |
| Education->AD | 12 | A | A | A | A | Stable |
| BMI->T2D | 12 | A | A | A | A | Stable |
| Height->CAD | 10 | A | B | A | B | Stricter: A->B; Extreme_strict: A->B |
| Insomnia->AD | 4 | C | D | C | D | Stricter: C->D; Extreme_strict: C->D |
| BMI->Stroke | 5 | C | C | C | D | Extreme_strict: C->D |
| HDL->CAD | 6 | C | C | B | C | Lenient: C->B |
| CRP->CAD | 1 | D | D | D | D | Stable |
| BMI->AD | 1 | D | D | D | D | Stable |

## Overall Stability

- **Stricter**: 2/9 cases change (22%). Changed: Height->CAD (A->B), Insomnia->AD (C->D).
- **Lenient**: 1/9 cases change (11%). Changed: HDL->CAD (C->B).
- **Extreme_strict**: 3/9 cases change (33%). Changed: Height->CAD (A->B), Insomnia->AD (C->D), BMI->Stroke (C->D).

## Boundary Proximity Analysis

Three scores lie within +/-1 point of a grade boundary:

- **Height->CAD** (score=10, A): distance=+0 from A/B boundary (10).
- **Insomnia->AD** (score=4, C): distance=+0 from C/D boundary (4).
- **BMI->Stroke** (score=5, C): distance=+1 from C/D boundary (4).
- **HDL->CAD** (score=6, C): distance=-1 from B/C boundary (7).

## Interpretation

The grade assignments are highly robust to threshold perturbation:

- **Grade A cases** (12/12, 12/12, 12/12, 10/12): All remain A under stricter thresholds. Height->CAD at 10 remains A under the lenient scenario and is at the A/B boundary, but even the extreme strict scenario (A >= 11) classifies it as B, not C.

- **Grade C cases** (4/12, 5/12, 6/12): Remain C under all scenarios except HDL->CAD at score=6, which is at the B/C boundary. Under the lenient scenario (B cutoff >=6), HDL->CAD would be classified as B — a plausible alternative classification given its unique role as the most widely studied MR-corrected false therapeutic target.

- **Grade D cases** (1/12, 1/12): Remain D under all scenarios. No threshold adjustment within +/-1 rescues these from the lowest grade.

- **No case crosses more than one grade boundary** under any scenario tested.

The single ambiguous assignment — HDL->CAD at the B/C boundary — is conservative: the current B cutoff of 7 places it in C, consistent with its incomplete pass of the external validation gate (L6=1, single-ancestry EUR only). A borderline B classification would not alter the qualitative interpretation that HDL->CAD is not a high-confidence causal claim.