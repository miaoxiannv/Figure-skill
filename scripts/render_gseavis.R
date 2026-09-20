# GSEA running-enrichment plot via GseaVis — house recipe (single source).
# Pipeline: clusterProfiler::GSEA (GSEAResult object) -> GseaVis::gseaNb.
# Requires the patched GseaVis install: run scripts/install_gseavis.R once.
#
# Usage: edit the CONFIG block, then
#   Rscript render_gseavis.R
# Keep OUT ASCII — R on Windows may mangle non-ASCII filenames; rename the
# PDF to its Chinese name afterwards in the shell.

suppressMessages({
  library(GseaVis)
  library(clusterProfiler)
})

## CONFIG ----------------------------------------------------------------
SRC_DE   <- "DE.csv"                          # columns: gene_name, stat (rank metric)
SRC_GMT  <- "geneset.gmt"                     # Enrichr-style GMT (upper-case symbols)
TERM     <- "Cytoplasmic Translation (GO:0002181)"  # GMT first-column name (matching is punctuation/case-insensitive)
OUT      <- "gsea_plot"                       # ASCII stem; rename to Chinese after
WIDTH_MM <- 89; HEIGHT_MM <- 76

## ranked vector (dedupe by symbol, upper-case to match GMT naming) --------
de <- read.csv(SRC_DE)
de <- de[!is.na(de$stat) & !is.na(de$gene_name) & de$gene_name != "", ]
de <- de[order(-abs(de$stat)), ]
de <- de[!duplicated(toupper(de$gene_name)), ]
ranks <- de$stat
names(ranks) <- toupper(de$gene_name)
ranks <- sort(ranks, decreasing = TRUE)
N <- length(ranks)

## term2gene from GMT ------------------------------------------------------
lines <- readLines(SRC_GMT)
term2gene <- do.call(rbind, lapply(lines, function(l) {
  p <- strsplit(l, "\t")[[1]]
  if (length(p) > 2) data.frame(term = p[1], gene = toupper(p[3:length(p)])) else NULL
}))

## GSEA -> GSEAResult object (what gseaNb expects) -------------------------
set.seed(1)
ego <- GSEA(ranks, TERM2GENE = term2gene, minGSSize = 10, maxGSSize = 500,
            pvalueCutoff = 1, eps = 0, verbose = FALSE)

# TERM matching is punctuation/case-insensitive (GMT names vary: GO:/Go:)
norm_id <- function(x) toupper(gsub("[^A-Za-z0-9]", "", x))
idx <- which(norm_id(ego@result$ID) == norm_id(TERM))
if (length(idx) == 0)
  stop("TERM not found in GSEA result. Closest IDs: ",
       paste(utils::head(ego@result$ID[agrep(TERM, ego@result$ID,
                                             max.distance = 0.2)], 3), collapse = " | "))
TERM_ID <- ego@result$ID[idx]

## adaptive x-tick step: ~4 intervals, snapped to 1/2/2.5/5 x 10^k --------
## (N=20k -> 5000; N=60k -> 20000; N=80k -> 20000)
nice_step <- function(x) {
  mag <- 10^floor(log10(x))
  m <- x / mag
  step <- if (m <= 1) 1 else if (m <= 2) 2 else if (m <= 2.5) 2.5 else if (m <= 5) 5 else 10
  step * mag
}
rankSeq <- nice_step(N / 4)

## locked style: y/colour window from the 97.5% quantile ------------------
## k = max(1.5, ceil(q97.5 * 1.25, to 0.5)) — covers the central band while
## the coord_cartesian zoom keeps extreme tails out of the panel (disclose).
k <- max(1.5, ceiling(quantile(abs(ranks), 0.975) * 1.25 * 2) / 2)

p <- gseaNb(object    = ego,
            geneSetID = TERM_ID,
            subPlot   = 3,
            addPval   = TRUE,
            markTopgene = TRUE,
            rank_ylim  = c(-k, k),
            rank_fc_lim = c(-k, k),
            curveCol  = c("#7A2A00", "#D55E00", "#F0A57C"),  # 单色明度阶梯 (vermillion)
            lineSize  = 1.2,
            rankSeq   = rankSeq,
            base_size = 7)
p <- p + ggplot2::theme(text = ggplot2::element_text(family = "Arial"))

ggplot2::ggsave(paste0(OUT, ".pdf"), p, width = WIDTH_MM, height = HEIGHT_MM,
                units = "mm", device = grDevices::cairo_pdf, family = "Arial")
cat("RENDER_DONE:", paste0(OUT, ".pdf"), "| rank window: ±", k, "\n")
