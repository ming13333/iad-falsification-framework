**What is already known**  
Mendelian randomization (MR) can produce precise and statistically significant estimates that do not reflect a true causal effect. This is a particular concern when a single high-effect locus, such as *APOE* in Alzheimer's disease, accounts for much of the genetic signal. In such settings, conventional MR may capture locus-level pleiotropy and linkage disequilibrium rather than evidence of upstream causality.

**The knowledge gap**  
Current pleiotropy-robust methods handle distributed horizontal pleiotropy but do not systematically detect or falsify artifacts driven by one dominant locus. Researchers using automated pipelines cannot tell genuine druggable targets from locus-driven confounding.

**What this study adds**  
We present a six-gate falsification framework scoring any directional MR claim into a fixed a-priori grade (A–D, 0–12 points). Across 43,200 simulated scenarios it reaches 100% specificity under the null (false discovery rate 0%), holds marginal FDR near 0.08 under balanced pleiotropy, and 0.97 sensitivity for large effects. Applied to published signals, it reclassifies "insomnia raises Alzheimer's disease risk" as shared *APOE*-locus liability (Grade C): the unclumped positive estimate (β=0.10, P=9.3×10⁻⁴) collapses to null after clumping (β=−0.13, P=0.52), genome-wide correlation is null (r_g=−0.028, P=0.57), and colocalization shows reverse *APOE* sharing (18/32 vs 1/47 loci). By triaging Grade A–B targets (e.g., LDL→coronary artery disease) from non-causal Grade C–D traits, this reproducible pipeline (R 4.5.2; Zenodo 10.5281/zenodo.21858125; GitHub ming13333/iad-falsification-framework) curbs wasted interventional investment.

