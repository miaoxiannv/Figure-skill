# One-time setup for the GSEA house recipe: R deps + patched GseaVis.
# Windows-oriented. Keep every path ASCII — Chinese usernames get mangled
# inside R's environment handling (three real install failures traced here).
# Three upstream GseaVis bugs are patched locally (details in
# references/chart-types.md, section "GSEA running-enrichment plot"):
#   P1 DOSE >= 4.6 declares get_organism as an export but never defines it
#      -> load-time crash; fixed with a lazy shim in 00-funcs-from-others.R
#   P2 the rank panel's `if/else` scale was unparenthesized inside the ggplot
#      chain, swallowing theme/labels -> parenthesized + rank_ylim/rank_fc_lim
#      parameters added
#   P3 the strip/fill gradient auto-limits took ±30 extremes, washing the
#      mid-band to pastel -> rank_fc_lim windows the colour scale

LIB <- "D:/Rlib"                 # ASCII path; adapt per machine if needed
TMP <- "D:/gsea-work/tmp"
dir.create(LIB, showWarnings = FALSE)
dir.create(TMP, showWarnings = FALSE)
Sys.setenv(TMPDIR = TMP, TEMP = TMP, TMP = TMP)
.libPaths(c(LIB, .libPaths()))

if (!requireNamespace("BiocManager", quietly = TRUE))
  install.packages("BiocManager", repos = "https://cloud.r-project.org", lib = LIB)
if (!requireNamespace("remotes", quietly = TRUE))
  install.packages("remotes", repos = "https://cloud.r-project.org", lib = LIB)

# clusterProfiler provides the GSEAResult object gseaNb expects;
# the rest are GseaVis Imports (pure R or Bioc binaries — no Rtools needed)
BiocManager::install(c("AnnotationDbi", "aplot", "circlize", "clusterProfiler",
                       "cols4all", "DOSE", "ggpp", "ggrepel", "ggridges",
                       "ggsci", "GO.db"),
                     ask = FALSE, update = FALSE)
remotes::install_github("davidsjoberg/ggsankey", lib = LIB, upgrade = "never")

# GseaVis master + patches
tarball <- file.path(TMP, "GseaVis-master.tar.gz")
download.file("https://codeload.github.com/junjunlab/GseaVis/tar.gz/refs/heads/master",
              tarball, mode = "wb")
untar(tarball, exdir = TMP)
rdir <- file.path(TMP, "GseaVis-master", "R")

# P1: lazy shim for DOSE's phantom export
old_f <- file.path(rdir, "funcs-from-others.R")
code <- readLines(old_f, warn = FALSE)
code <- sub('get_organism <- getFromNamespace("get_organism", "DOSE")',
            'get_organism <- function(OrgDb) getFromNamespace("get_organism", "DOSE")(OrgDb)',
            code)
writeLines(code, file.path(rdir, "00-funcs-from-others.R"))   # 00- prefix: bind first
file.remove(old_f)

# P2: parenthesize the rank-panel scale branch + add rank_ylim / rank_fc_lim
nb <- file.path(rdir, "gseaNb.R")
src <- paste(readLines(nb, warn = FALSE), collapse = "\n")
src <- sub("rankSeq = 5000,", "rankSeq = 5000,\n                   rank_ylim = NULL,\n                   rank_fc_lim = NULL,", src)
src <- gsub("ggplot2::coord_cartesian\\(expand = 0\\) \\+\n      ggplot2::ylab\\(\"Ranked List\"\\)",
            "ggplot2::coord_cartesian(expand = 0, ylim = rank_ylim) +\n      ggplot2::ylab(\"Ranked List\")", src)
src <- sub("high = rankCol\\[3\\], midpoint = 0\\) \\+",
           "high = rankCol[3], midpoint = 0, limits = rank_fc_lim, oob = scales::squish) +", src)
src <- sub("if \\(length\\(rankCol\\) > 3\\) ggplot2::scale_fill_gradientn",
           "(if (length(rankCol) > 3) ggplot2::scale_fill_gradientn", src, fixed = FALSE)
# wrap the if/else tail with a closing paren before the following '+'
src <- sub("(oob = scales::squish) \\+\n      ggplot2::geom_hline",
           "oob = scales::squish)) +\n      ggplot2::geom_hline", src)
writeLines(src, nb)

install.packages(file.path(TMP, "GseaVis-master"), repos = NULL,
                 type = "source", lib = LIB)
library(GseaVis)
cat("GseaVis ready — patched install complete\n")
