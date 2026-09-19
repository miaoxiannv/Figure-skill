# Backend Selection

This skill is **Python-only**. All plotting, previewing, exporting, and visual QA
happen in Python (matplotlib / seaborn / cnsplots / scanpy). Do not offer R, do not
ask "Python or R?", and do not draw any figure in R — even when the user's data or
statistics come from R pipelines (DESeq2, Seurat, limma, survival models).

## Handling R-origin data

R-origin inputs are welcome — as data, not as a plotting backend:

- R scripts, RDS/RData, Seurat objects, DESeq2/limma tables → first **export the
  source data to CSV/TSV with stable column names** (any non-visual tool may do
  this conversion, including R itself), then draw the figure in Python from the
  exported file.
- Keep the exported source-data file next to the plotting script for
  reproducibility.
- Never import plotting libraries in R, never open an R graphics device, never
  save a figure (PDF/PNG/SVG) from R. Statistics must be re-runnable in Python
  (`scipy.stats` / `statsmodels` / `pingouin`) or already summarized in the
  exported table.

## Missing dependency rule

If a required Python package is missing: stop, report the exact blocker, provide
the script and `pip install ...` instructions, or ask permission to install. No
silent fallback to another package for a mandated chart type.

## Missing font blocker

If **Arial** is not installed on the machine that renders the figure, stop — it
is a delivery blocker on the same level as a missing package. Check with
`python scripts/figure_qa.py font.check`. Never substitute lookalikes
(Liberation Sans, Helvetica clones, DejaVu Sans) — they change letterforms and
are rejected by `figure_qa.py verify` anyway. Windows ships Arial; on Linux/HPC
install `ttf-mscorefonts-installer` (accept the EULA) or copy a licensed
`Arial.ttf` into `~/.fonts` and clear the matplotlib font cache
(`~/.cache/matplotlib`) so it is picked up.

## Python stack (the only stack)

- Core plotting (basic charts): **`cnsplots` — mandatory** for bar / grouped bar,
  scatter, line, box, violin, strip, histogram, KDE, regression
  (`import cnsplots as cns`; missing install = reported blocker, offer
  `pip install cnsplots`, never a silent seaborn fallback)
- Charts cnsplots does not cover: `seaborn` (heatmap, locked house style in
  `references/chart-types.md`), `scanpy` / `umap-learn` / `openTSNE` /
  `scikit-learn` (embeddings)
- Statistics: `scipy.stats`, `statsmodels`, `pingouin`; on-figure significance
  marks via cnsplots `pairs=` (runs Welch's t-test internally; `test=`/`p_adjust=`
  kwargs crash on 0.6.0)
- Label repel: `adjustText` on the axes cnsplots returns
- Export: `cns.savefig("中文文件名.pdf")` (editable text) or
  `fig.savefig(...pdf)` with `pdf.fonttype = 42` for non-cnsplots charts

## Utility use of other languages

Non-Python tools (including R) remain allowed for **non-visual utility work
only** — listing files, checking CSV dimensions, converting data files,
decompressing archives. They must not import plotting libraries, open graphics
devices, save image/vector files, or decide visual layout.
