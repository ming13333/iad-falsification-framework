library(TwoSampleMR)

ao <- available_outcomes()

cols <- c(
    "id",
    "trait",
    "author",
    "year",
    "sample_size",
    "ncase",
    "ncontrol",
    "consortium",
    "population",
    "pmid",
    "doi"
)

cols <- intersect(cols, names(ao))

ins <- ao[
    grepl("insomnia", ao$trait, ignore.case = TRUE),
    cols,
    drop = FALSE
]

ad <- ao[
    grepl("Alzheimer", ao$trait, ignore.case = TRUE),
    cols,
    drop = FALSE
]

# 控制台全表打印（pillar 原生打印，遇 list 列显示 <list> 不报错；n=Inf 全行、width=Inf 全列不折行）
print(ins, n = Inf, width = Inf)
cat("----\n")
print(ad, n = Inf, width = Inf)

# 同时落盘，便于复核
write.csv(ins, "INSOMNIA_all.csv", row.names = FALSE)
write.csv(ad, "ALZHEIMER_all.csv", row.names = FALSE)

cat("INSOMNIA rows:", nrow(ins), "\n")
cat("ALZHEIMER rows:", nrow(ad), "\n")
