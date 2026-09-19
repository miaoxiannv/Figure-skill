---
name: nature-figure-pdf
description: >-
  Submission-grade single-message scientific figures for Nature, Science, Immunity and
  other high-impact journals, in Python. Use whenever the user asks to create, revise,
  audit, or polish manuscript figures or journal-ready PDFs (出图/论文图/投稿图/house-style
  heatmap). Doctrine: ONE figure = ONE message — composites and cnsplots multipanel
  helpers forbidden. Python basic charts (bar/scatter/line/box/violin/strip/histogram/
  KDE/regression) MUST use cnsplots; raw seaborn/matplotlib for these is a
  reported blocker. Arial 7 pt only, ASCII labels; colors only from documented
  palettes (viridis/cividis/Okabe-Ito/ColorBrewer/cnsplots journal presets), never
  rainbow/jet/turbo. Dumbbell and lollipop charts forbidden. Heatmaps follow the
  locked house style in chart-types.md. No Chinese text inside figures;
  Chinese filenames. Deliver one submission PDF plus one 300-dpi _预览.png companion,
  QA'd with scripts/figure_qa.py. Python-only backend — never plot in R;
  export R-origin data to CSV/TSV first. Not for interactive/EDA plots.
---

# Nature Figure Skill — 一图一义 · 极简 · 科学配色

A workflow for producing submission-grade scientific figures where **each figure is a single,
minimal, self-contained visual argument**. The figure serves the scientific logic; simplicity
serves the figure.

## Core doctrine (non-negotiable)

1. **One figure, one message (一图一义).** Every figure answers exactly ONE scientific
   question and makes exactly ONE point. Multi-panel composite figures, merged "big figures",
   and hero-panel layouts are **forbidden** — including cnsplots' own composite helpers
   (`cns.multipanel()`, `cns.add_panel_label()`): the doctrine bans the output, not just
   the tooling. If the story needs three points, deliver three
   separate PDF files. Never combine independent figures into a composite page.
2. **Simplicity first (简洁第一).** Remove every element that does not carry data: no
   chartjunk, no 3D effects, no decorative gradients, no drop shadows, no background fills,
   no unnecessary gridlines, no borders. White background only. When in doubt, delete.
3. **Arial only, 7 pt.** Every character in every figure is **Arial at 7 pt** — one
   family, one base size. Sanctioned deviations, nothing else: mathtext
   sub/superscripts scale to 0.7 × base (`mm$^3$`), the locked heatmap house style's
   manual colorbar may use 5.5 pt (journals accept 5 pt minimum, and a 7 pt z-score
   bar dwarfs the matrix), and italic is allowed only for gene symbols.
   Helvetica and all other fallback
   families are forbidden: lock `cns.settings.font_sans_serif = ["Arial"]` before
   `cns.figure()`, and keep in-figure text ASCII-only (superscripts via mathtext)
   so no other family is ever substituted. Verify the exported PDF
   embeds Arial-only fonts before delivery.
4. **No Chinese inside figures.** All in-figure text (axis labels, ticks, legends,
   annotations, panel titles) must be English. **Saved filenames are in Chinese** —
   use a short descriptive Chinese name, e.g. `治疗组肿瘤体积随时间变化.pdf`.
5. **PDF for submission, PNG preview for review.** Save exactly one PDF per figure —
   the submission file; never write SVG, TIFF, JPEG, EPS. Additionally deliver one
   review companion `<中文文件名>_预览.png` (rendered from the PDF at 300 dpi) with
   every figure — the user reviews from the PNG; the PDF is what gets submitted.
   No other image files.
6. **Scientific color maps only, from documented sets.** Follow `references/color-maps.md`:
   classify the variable (sequential / diverging / cyclic / categorical), then pick
   colors ONLY from mature, documented palettes — cnsplots journal presets
   (`'Nature'`, `'Cell'`, `'Science'`, `'Ecotyper1'`–`'Ecotyper6'`), Okabe-Ito,
   ColorBrewer, viridis/cividis, Crameri, cmocean — via `cns.palettes("Name")`.
   Ad-hoc hand-picked hex colors are forbidden; never rainbow / jet / turbo; never
   red-green at similar lightness. Color is a quantitative axis, not decoration.
7. **Mature packages, never hand-rolled.** Bars, scatter, UMAP, heatmaps, distributions and
   all statistics must come from established libraries — cnsplots/seaborn/matplotlib,
   scanpy or umap-learn, scipy/statsmodels/pingouin. Do not re-implement dimensionality
   reduction, statistical tests, or standard chart types by hand.
8. **cnsplots mandate (Python basic charts).** When the backend is Python, every basic chart
   type — bar / grouped bar, scatter, line, box, violin, strip, histogram, KDE, regression —
   MUST be drawn with `cnsplots` (`import cnsplots as cns`). Raw seaborn or matplotlib calls
   for these chart types are forbidden. seaborn/matplotlib remain allowed only for chart types
   cnsplots does not cover (e.g. `sns.heatmap`, scanpy UMAP styling) and for fine-tuning the
   matplotlib axes that cnsplots returns.

## Backend rule (Python-only, non-negotiable)

Python is the exclusive backend for all plotting, previewing, exporting, and QA —
never ask "Python or R?" and never produce a figure with R, ggplot2, or
ComplexHeatmap, even when the data or statistics come from an R pipeline. Export
R-origin data (Seurat objects, DESeq2 tables, RDS) to CSV/TSV first, then plot in
Python from the exported file. If a Python package is missing, stop, report the
blocker, and offer the script plus install commands. See
`references/backend-selection.md`.

## cnsplots gate (blocking, Python basic charts)

When the backend is Python and the chart is a basic type — bar / grouped bar, scatter,
line, box, violin, strip, histogram, KDE, regression — the plotting code MUST use
[cnsplots](https://github.com/faridrashidi/cnsplots), with the mandatory font, size,
and export settings from `references/api.md`. Canonical pattern:

```python
import matplotlib.pyplot as plt
import cnsplots as cns

# lock BEFORE figure(): Arial-only family; never crop the journal canvas;
# cnsplots defaults violate the doctrine (transparent background, 0.5 pt axes)
cns.settings.font_sans_serif = ["Arial"]
cns.settings.savefig_bbox = "standard"          # "tight" (the default) crops the canvas
cns.settings.savefig_transparent = False        # default True — force pure white background
cns.settings.axes_linewidth = 0.7               # default 0.5 — the mandate is 0.7 pt
cns.figure(width=252, height=170)               # 252 px / 72 = 3.5 in = 88.9 mm (Nature)
cns.settings.pvalue_fontsize = 7
plt.rcParams.update({"font.size": 7, "axes.labelsize": 7,
                     "xtick.labelsize": 7, "ytick.labelsize": 7, "legend.fontsize": 7,
                     "xtick.major.width": 0.7, "ytick.major.width": 0.7})

ax = cns.barplot(data=df, x="group", y="value",
                 hue="group", legend=False,
                 palette=["#B0B0B0", "#0072B2"],   # approved sets: neutral gray + Okabe-Ito blue
                 pairs=[("Control", "Treated")])   # pairs= bracket; barplot runs Welch's t-test
cns.savefig("各组指标比较.pdf")                     # PDF with editable text

# then QA from the skill directory — single-source checks, do not re-implement:
#   python scripts/figure_qa.py verify 各组指标比较.pdf --width-mm 88.9
#   python scripts/figure_qa.py preview 各组指标比较.pdf
```

- **No silent fallback.** If `cnsplots` is not installed, stop, report the missing
  dependency, and offer `pip install cnsplots` (Python ≥ 3.10) or ask permission to
  install — do not substitute seaborn/matplotlib for a mandated chart type.
- **Font and size are not optional.** `font_sans_serif = ["Arial"]` goes before
  `cns.figure()`; every text element ends up Arial 7 pt; the exported PDF must embed
  Arial-only fonts. `scripts/figure_qa.py verify` enforces this.
- **Built-in statistics:** pass `pairs=[("A", "B")]` and cnsplots draws the bracket
  itself — never hand-annotate p-values or brackets. The test depends on the
  function (verified in 0.6.0 source): `barplot` runs **Welch's t-test**;
  `boxplot`/`violinplot` run **Mann-Whitney U**; `stripplot` runs no test. Name
  the actual test in the caption, with n and error-bar definitions. (`test=`/
  `p_adjust=` kwargs do not exist on these functions in 0.6.0 and crash.)
- **Allowed fine-tuning:** the axes cnsplots returns are standard matplotlib — axis
  labels, limits, aspect, `adjustText` label repel are fine; re-drawing the chart with
  raw seaborn/matplotlib primitives is not.
- **Out of scope of the mandate:** chart types cnsplots does not cover keep their
  established packages (`sns.heatmap`, scanpy UMAP). Where cnsplots does provide a
  scientific chart (volcano, forest, Kaplan–Meier, ROC, GSEA, clustered heatmap),
  prefer its function over hand-rolled primitives.
- The R language is allowed only for non-visual utility work (CSV export from RDS,
  file listing) — never for drawing, previewing, or exporting a figure.

## Figure contract (before any code)

Write this contract in working notes or the reply:

```text
Core message:        one sentence with a verb — the single thing this figure proves
Journal target:      Nature / Science / Immunity / other
Backend:             Python (only)
Final size:          single-column or double-column per references/journal-styles.md
                     (px = mm / 25.4 × 72; Nature single column 89 mm = 252 px)
Font:                Arial 7 pt, one family, verified in the exported PDF
Chart type:          bar / scatter / line / heatmap / UMAP / distribution / ...
Data variable class: sequential / diverging / cyclic / categorical
Color map:           palette NAME from the approved sets and why its class matches
Statistics:          test name, package, n, what the error bars show
Chinese filename:    e.g. 差异表达基因火山图.pdf
```

If any line cannot be filled, ask the user before plotting.

## Mandatory in-figure rules

- English only inside the figure; Chinese only in the filename.
- **All text is Arial 7 pt** — axis labels, ticks, legend, annotations, one uniform
  size. No in-figure titles (the caption carries the message). ASCII-only label
  strings; superscripts via mathtext (`mm$^3$`), never unicode superscripts — any
  non-ASCII character makes cnsplots swap the whole text to DejaVuSans.
- Keep only essential text: axis labels with units, tick labels, legend entries, and
  direct data labels. No explanatory small text, footnotes, method notes, or gray
  descriptive prose.
- White background; left+bottom spines only (0.7 pt); frameless legends; no
  gridlines unless they carry real reference meaning (then one 0.5 pt gray line).
- Bar charts start at y = 0 — never truncate a bar axis.
- Continuous color encodings need a labeled color bar; state normalization, limits,
  and center (for diverging maps) explicitly.
- Statistics, n, and error-bar definitions go in the external caption/QA record, not
  in the figure. Significance marks produced by cnsplots `pairs=` are the one
  allowed exception — never hand-drawn brackets; the exact test, n, and error-bar
  definitions still go in the caption.

## Privacy rule

Do not disclose private local paths, private filenames, internal reference documents, or
template provenance in user-facing output, code comments, or figure text, unless the user
explicitly asks for that audit trail.

## Quick-start

### Python (basic charts — cnsplots, mandatory)

```python
import matplotlib.pyplot as plt
import cnsplots as cns

cns.settings.font_sans_serif = ["Arial"]   # before figure(): Arial-only
cns.settings.savefig_bbox = "standard"     # keep the exact journal canvas
cns.settings.savefig_transparent = False   # default True — force white background
cns.settings.axes_linewidth = 0.7          # default 0.5 — mandate is 0.7 pt
cns.figure(width=252, height=170)          # 88.9 mm Nature single column
plt.rcParams.update({"font.size": 7, "axes.labelsize": 7,
                     "xtick.labelsize": 7, "ytick.labelsize": 7, "legend.fontsize": 7,
                     "xtick.major.width": 0.7, "ytick.major.width": 0.7})
cns.barplot(data=df, x="group", y="value", hue="group", legend=False,
            palette=["#B0B0B0", "#0072B2"], pairs=[("Control", "Treated")])
cns.savefig("各组指标比较.pdf")
# then QA (from the skill directory — single-source checks):
#   python scripts/figure_qa.py verify 各组指标比较.pdf --width-mm 88.9
#   python scripts/figure_qa.py preview 各组指标比较.pdf
```

Full settings, palette whitelist, and QA workflow: `references/api.md`. Chart types
cnsplots does not cover (heatmap, UMAP styling, …)
keep the rcParams style block below and their established packages.

### Python (non-cnsplots charts)

For chart types outside the cnsplots mandate (heatmap, UMAP styling, embeddings),
apply this style block to the matplotlib/seaborn/scanpy axes — same Arial-7 pt law:

```python
import matplotlib as mpl
import matplotlib.pyplot as plt

mpl.rcParams.update({
    "font.family": "sans-serif",
    "font.sans-serif": ["Arial"],   # Arial only — no Helvetica/DejaVu fallback
    "mathtext.fontset": "custom",   # superscripts render in Arial too
    "mathtext.rm": "Arial", "mathtext.it": "Arial:italic", "mathtext.bf": "Arial",
    "pdf.fonttype": 42,             # editable TrueType text in PDF
    "font.size": 7,
    "axes.labelsize": 7, "xtick.labelsize": 7, "ytick.labelsize": 7,
    "legend.fontsize": 7, "axes.titlesize": 7,
    "axes.spines.right": False,
    "axes.spines.top": False,
    "axes.linewidth": 0.7,
    "legend.frameon": False,
    "figure.facecolor": "white",
    "axes.facecolor": "white",
    "xtick.major.width": 0.7,
    "ytick.major.width": 0.7,
})

def save_pub(fig, chinese_filename, width_mm=89, height_mm=60):
    """Save at the exact journal size — no tight crop — then close.
    Afterwards run scripts/figure_qa.py verify + preview (references/api.md)."""
    fig.set_size_inches(width_mm / 25.4, height_mm / 25.4)
    fig.savefig(f"{chinese_filename}.pdf")
    plt.close(fig)
```

## When to load this skill

- Single scientific figures for Nature, Science, Immunity, Cell, or similar venues.
- Bar charts, scatter plots, UMAP/t-SNE embeddings, heatmaps, line trends, distributions,
  volcano plots, forest plots — one chart type per file.
- Requests to audit or simplify an existing figure for journal submission.

## When NOT to load

- Multi-panel composite figures (this skill forbids them by design).
- Interactive/web-first plotting (Plotly, Bokeh, Altair).
- EDA-only plots without a publication target.
- Illustrator/Figma-first infographic layouts.

## Reference files

| File | Open when |
|------|-----------|
| [references/figure-contract.md](references/figure-contract.md) | Converting a request into the single-message contract |
| [references/journal-styles.md](references/journal-styles.md) | Nature / Science / Immunity size, font, and format specs |
| [references/color-maps.md](references/color-maps.md) | Choosing and auditing perceptually uniform color maps |
| [references/backend-selection.md](references/backend-selection.md) | Python-only backend rules and R-origin data handling |
| [references/design-theory.md](references/design-theory.md) | Minimalism, typography, layout rationale |
| [references/api.md](references/api.md) | Python palette constants and helper signatures |
| [references/chart-types.md](references/chart-types.md) | Single-chart recipes with mature packages (bar, scatter, UMAP, heatmap, ...) |
| [references/qa-contract.md](references/qa-contract.md) | Pre-submission QA checklist |
| [scripts/figure_qa.py](scripts/figure_qa.py) | Single-source QA: `verify` / `preview` / `audit-text` / `font.check` (CLI or import) |
