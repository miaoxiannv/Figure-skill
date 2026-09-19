# nature-figure-pdf

Submission-grade **single-message scientific figures** for Nature, Science, Immunity
and other high-impact journals, in Python.

## Core doctrine

1. **一图一义 (one figure, one message)** — every figure answers exactly one
   scientific question. Multi-panel composites are forbidden; multiple points mean
   multiple separate PDFs.
2. **简洁第一 (simplicity first)** — white background, no chartjunk, no gridlines,
   no borders.
3. **Arial 7 pt** — every character is Arial at 7 pt, one family, one base size;
   Helvetica and every other fallback family are forbidden; verify the exported PDF
   embeds Arial-only fonts.
4. **Scientific color maps, whitelist only** — colors come from mature documented
   palettes (viridis/cividis/Crameri/cmocean/ColorBrewer/Okabe-Ito and cnsplots
   Nature/Cell/Science/Ecotyper presets via `cns.palettes()`); rainbow/jet/turbo,
   red-green sole encodings, and ad-hoc hexes are forbidden.
5. **Mature packages only** — Python basic charts (bar, scatter, line, box, violin,
   strip, histogram, KDE, regression) **must use [cnsplots](https://github.com/faridrashidi/cnsplots)**;
   seaborn/matplotlib only for chart types cnsplots does not cover (heatmap, UMAP
   styling). Statistics from scipy/statsmodels/pingouin. Never hand-rolled.
6. **Language policy** — English inside the figure; **Chinese filenames** for saved
   PDFs (e.g. `化合物A对肿瘤重量的影响.pdf`).
7. **PDF for submission, PNG preview for review** — one PDF per figure, exact journal
   canvas (no tight crop), editable text (`pdf.fonttype = 42`); QA with
   `scripts/figure_qa.py` (`verify` + `preview` + `audit-text`), which renders one
   `<中文文件名>_预览.png` (300 dpi) review companion.
8. **Python-only backend** — never plot in R; R-origin data (Seurat, DESeq2, RDS)
   must be exported to CSV/TSV first, then plotted in Python.

## Workflow

1. Backend rule: Python-only — never ask "Python or R?" →
   `references/backend-selection.md`
2. Figure contract: core message, chart type, data class, color map, statistics,
   Chinese filename → `references/figure-contract.md`
3. Journal specs: single-column default (Nature 89 mm / Science 55 mm /
   Immunity 85 mm), Arial 7 pt → `references/journal-styles.md`
4. Plot with mature packages — Python basic charts via **cnsplots** (mandatory),
   minimal style → `references/chart-types.md`, `references/api.md`
5. QA: grayscale, CVD, checklist → `references/qa-contract.md`

## File structure

```
nature-figure-pdf/
├── SKILL.md                     ← skill trigger & doctrine
├── README.md                    ← this file
├── evals/evals.json             ← behavior evals
├── scripts/
│   └── figure_qa.py             ← single-source QA: verify / preview / audit-text / font.check
└── references/
    ├── figure-contract.md       ← one-message contract template
    ├── journal-styles.md        ← Nature / Science / Immunity specs
    ├── color-maps.md            ← scientific color map selection & audit
    ├── backend-selection.md     ← Python-only backend rules
    ├── design-theory.md         ← minimalism, typography, export policy
    ├── api.md                   ← Python constants & helpers
    ├── chart-types.md           ← single-chart recipes (bar/UMAP/heatmap/...)
    ├── tutorials.md             ← end-to-end walkthroughs
    └── qa-contract.md           ← pre-submission checklist
```

## Quick-start (Python — basic charts, cnsplots)

```python
import matplotlib.pyplot as plt
import cnsplots as cns

cns.settings.font_sans_serif = ["Arial"]   # Arial-only, before figure()
cns.settings.savefig_bbox = "standard"     # keep the exact journal canvas
cns.settings.savefig_transparent = False   # default True — force white background
cns.settings.axes_linewidth = 0.7          # default 0.5 — mandate is 0.7 pt
cns.figure(width=252, height=170)          # 252 px = 88.9 mm Nature single column
cns.settings.pvalue_fontsize = 7
plt.rcParams.update({"font.size": 7, "axes.labelsize": 7,
                     "xtick.labelsize": 7, "ytick.labelsize": 7, "legend.fontsize": 7,
                     "xtick.major.width": 0.7, "ytick.major.width": 0.7})
cns.barplot(data=df, x="group", y="value", hue="group", legend=False,
            palette=["#B0B0B0", "#0072B2"], pairs=[("Control", "Treated")])
cns.savefig("各组指标比较.pdf")

# then QA (from the skill directory):
#   python scripts/figure_qa.py verify 各组指标比较.pdf --width-mm 88.9
#   python scripts/figure_qa.py preview 各组指标比较.pdf
```

Chart types cnsplots does not cover (heatmap, UMAP styling, …) use the rcParams style
block from `references/api.md`. Missing cnsplots? Stop and `pip install cnsplots` —
never fall back to seaborn for mandated chart types.

## Quick-start (Python — non-cnsplots charts)

```python
import matplotlib as mpl
import matplotlib.pyplot as plt

mpl.rcParams.update({
    "font.family": "sans-serif",
    "font.sans-serif": ["Arial"],   # Arial only — no fallback families
    "mathtext.fontset": "custom", "mathtext.rm": "Arial",
    "mathtext.it": "Arial:italic", "mathtext.bf": "Arial",
    "pdf.fonttype": 42, "font.size": 7,
    "axes.labelsize": 7, "xtick.labelsize": 7, "ytick.labelsize": 7,
    "legend.fontsize": 7,
    "axes.spines.right": False, "axes.spines.top": False,
    "axes.linewidth": 0.7, "legend.frameon": False,
})

# ... one chart, one message ...
fig.set_size_inches(89 / 25.4, 60 / 25.4)      # exact journal canvas, no tight crop
fig.savefig("中文描述性文件名.pdf")
plt.close(fig)
# then run scripts/figure_qa.py verify + preview  — references/api.md
```

## Scope

**Use for**: single scientific charts (bar, violin, scatter, line, heatmap, UMAP,
volcano, forest, survival) targeting Nature / Science / Immunity / Cell / NeurIPS
venues; GO/KEGG enrichment dotplots and gene-concept networks (locked house
recipes); auditing or simplifying existing figures.

**Not for**: multi-panel composite figures (forbidden by doctrine), interactive web
plots, EDA without a publication target, Illustrator/Figma infographics.
