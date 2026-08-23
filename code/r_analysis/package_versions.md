
> : 2026-08-01 |  #4(renv.lock )
> : `packageVersion()`  R 4.5.2

## R
- R 4.5.2 (2025-10-31 ucrt)

##
|  |  |  |
|----|------|------|
| TwoSampleMR | 0.7.9 |  MR, LD-clump, harmonise, mr() |
| ieugwasr | 1.1.0 | IEU OpenGWAS API , ld_clump |
| MendelianRandomization | 0.10.0 | MVMR (mr_mvinput / mr_mvivw / mr_mvegger) |
| GenomicSEM | 0.0.5 | LDSC rg(ldsc() ) |
| cause | 1.2.0.335 | CAUSE ( monkey-patch  loo 2.6+) |
| loo | 2.10.0 | CAUSE  LOO  |
| dplyr | 1.2.1 |  |
| data.table | 1.18.4 |  clean  |

- MRInstruments: (LD  IEU API , )
- pander: (, )

##
1.  `renv::init()` + `renv::snapshot()`  `renv.lock`, . 
2.  GWAS : 
   - `ukb-b-3957.clean.tsv.gz`(196 MB, , UKB n=462,341)
   - `ieu-b-2.clean.tsv.gz`(185 MB, AD Kunkle, IGAP n=63,926)
   -  `met-d-*` full summary statistics  IEU API ( Phase2A §.3 / L10). 
3.  `set.seed(20260801)`(CAUSE  `set.seed(20240721)`). 

##
- Rscript: `C:/Program Files/R/R-4.5.2/bin/x64/Rscript.exe`
- LD scores: `./output/ld_ref/LDscore/`
- hm3: `./output/ld_ref/hm3_with_alleles.txt`
- ieugwasr ( libcurl  139). 