# Chart Types — Single-Chart Recipes

One chart per figure, from mature packages. **Python mandate: basic chart types — bar,
scatter, line, box, violin, strip, histogram, KDE, regression — MUST be drawn with
`cnsplots` (`import cnsplots as cns`). Raw seaborn/matplotlib calls for these types are
forbidden; if cnsplots is missing, stop and install/report — never fall back silently.**
seaborn/matplotlib remain allowed for chart types cnsplots does not cover (heatmap,
UMAP styling) and for fine-tuning the axes cnsplots returns. Every recipe saves one PDF
with a Chinese filename; before `cns.figure(...)` lock
`cns.settings.font_sans_serif = ["Arial"]`, `cns.settings.savefig_bbox = "standard"`,
`cns.settings.savefig_transparent = False` (the default True gives a transparent
background), and `cns.settings.axes_linewidth = 0.7` (the default 0.5 is too thin),
size the canvas in px (px = floor(mm / 25.4 × 72); Nature single column 89 mm = 252 px),
set every text element to 7 pt, and QA the export with `scripts/figure_qa.py`
(`verify` + `preview`; see `references/api.md`).

---

## Bar / grouped bar (group comparison)

```python
import cnsplots as cns

cns.settings.font_sans_serif = ["Arial"]
cns.settings.savefig_bbox = "standard"
cns.settings.savefig_transparent = False        # default True — white background
cns.settings.axes_linewidth = 0.7               # default 0.5 — mandate is 0.7 pt
cns.figure(width=252, height=170)                       # 88.9 mm Nature single column
cns.barplot(data=df, x="group", y="value", hue="group", legend=False,
            palette=["#B0B0B0", "#0072B2"],             # neutral gray control + Okabe-Ito blue
            errorbar=("sd", 1), capsize=0.12,
            pairs=[("Control", "Treated")])             # barplot pairs= -> Welch's t-test
cns.savefig("各组指标比较.pdf")
```

- Two conditions max; more conditions → simplify the question or facet into
  separate figures.
- Significance marks come from `pairs=` — in `barplot` this runs **Welch's
  t-test**; `test=`/`p_adjust=` kwargs crash on 0.6.0 — never hand-drawn
  brackets. The exact test, n per group, and error-bar meaning (SD / SEM / 95% CI)
  still go in the caption, not the figure. QA with
  `python scripts/figure_qa.py verify 各组指标比较.pdf --width-mm 88.9` (+ `preview`).

## Box / violin / strip (distribution comparison)

```python
cns.figure(width=252, height=170)   # 88.9 mm single column
cns.violinplot(data=df, x="group", y="value", hue="group", legend=False,
               palette=["#0072B2", "#D55E00"],
               pairs=[("Control", "Treated")])   # violin/box pairs= -> Mann-Whitney U
cns.savefig("各组分布比较.pdf")

# small n (n < ~10 per group): strip plot instead
cns.figure(width=252, height=170)   # 88.9 mm single column
cns.stripplot(data=df, x="group", y="value")
cns.savefig("各组单点分布.pdf")
```

- `pairs=` on `violinplot`/`boxplot` runs the **Mann-Whitney U test** (not
  Welch's t-test — that is barplot only). Name Mann-Whitney U in the caption;
  misnaming it is a statistics error. `stripplot` supports no pairs.

## Line trend (change over x)

```python
cns.figure(width=252, height=170)   # 88.9 mm single column
cns.lineplot(data=df, x="time", y="volume", hue="group")
cns.savefig("肿瘤体积随时间变化.pdf")
```

- Uncertainty band allowed; keep it light (alpha ≤ 0.25) when styling the returned axes.
- Mark intervention points with one thin vertical reference line only if meaningful
  (`ax.axvline` on the returned axes is allowed fine-tuning).

## Scatter (co-variation)

```python
from adjustText import adjust_text   # NOT adjust_texts — that name does not exist

cns.figure(width=252, height=252)   # 88.9 x 88.9 mm square
ax = cns.scatterplot(data=df, x="x", y="y", hue="cluster")
texts = [ax.text(r.x, r.y, r.gene) for r in label_rows]
adjust_text(texts, ax=ax, arrowprops=dict(arrowstyle="-", lw=0.4, color="0.4"))
cns.savefig("两指标相关性散点图.pdf")
```

- Correlation coefficient and test go in the caption (`scipy.stats.pearsonr` /
  `spearmanr`), not a box inside the axes — unless there is genuinely empty space.
- Regression with confidence band: use the cnsplots regression plot function instead
  of fitting/drawing the band by hand.

## Heatmap (two categorical axes)

**Locked house style (user-approved 2026-09-17 — apply as-is, do not re-derive per
figure).** Square cells with thin black borders, `RdBu_r` diverging fill for
z-scored rows, italic horizontal row labels, and a small manual colorbar to the
right of the matrix (vertically upper-middle) — never matplotlib's auto colorbar
strip, which reserves ugly whitespace.

**Font lock first.** This recipe draws on a raw matplotlib/seaborn canvas (no
`cns.figure()`), so the mandatory style block from `references/api.md` must be
applied before plotting — without `font.sans-serif = ["Arial"]` and
`pdf.fonttype = 42` the export embeds DejaVuSans Type 3 and fails `figure_qa.py
verify` (verified). House-style sanctioned deviations from the 7 pt law: the
manual colorbar may use 5.5 pt, row labels are italic (gene symbols), and the
canvas width follows the matrix instead of the journal column — `verify` against
the canvas's own computed size, not the column width.

```python
import matplotlib as mpl

mpl.rcParams.update({                       # mandatory style block (references/api.md)
    "font.family": "sans-serif", "font.sans-serif": ["Arial"],
    "mathtext.fontset": "custom", "mathtext.rm": "Arial",
    "mathtext.it": "Arial:italic", "mathtext.bf": "Arial",
    "pdf.fonttype": 42, "font.size": 7,
    "axes.labelsize": 7, "xtick.labelsize": 7, "ytick.labelsize": 7,
    "legend.fontsize": 7,
})
import matplotlib.colors as mcolors
import seaborn as sns
from matplotlib.transforms import Bbox
from mpl_toolkits.axes_grid1.inset_locator import inset_axes

CELL = 0.125                                   # inches per cell — square, ~3.2 mm
fig, ax = plt.subplots(figsize=(1.55 + Z.shape[1] * CELL, 0.75 + Z.shape[0] * CELL))
sns.heatmap(Z, cmap="RdBu_r", center=0, vmin=-2, vmax=2, square=True,
            linewidths=0.35, linecolor="black",           # thin BLACK borders
            cbar=False, ax=ax)                            # colorbar added manually
ax.set_yticks([i + 0.5 for i in range(Z.shape[0])])       # BEFORE set_yticklabels
ax.set_yticklabels([f"${g}$" for g in Z.index], rotation=0, fontsize=7)  # italic, horizontal
plt.setp(ax.set_xticklabels(Z.columns, rotation=45, ha="right"), fontsize=7)
ax.tick_params(length=0); ax.set_xlabel(""); ax.set_ylabel("")

# colorbar: thin vertical bar right of the matrix, vertically upper-middle
# (~0.8 cell wide, ~4 rows tall) — manual inset; auto layout misbehaves
anchor = Bbox.from_bounds(1.03, 0.60, 0.10, 0.13)         # x0, y0, w, h — axes coords
cb_ax = inset_axes(ax, width="100%", height="100%", loc="lower left",
                   bbox_to_anchor=anchor, bbox_transform=ax.transAxes, borderpad=0)
cb = mpl.colorbar.ColorbarBase(cb_ax, cmap=mpl.colormaps["RdBu_r"],
                               norm=mcolors.Normalize(vmin=-2, vmax=2), ticks=[-2, 0, 2])
cb_ax.tick_params(labelsize=5.5, length=1.4, width=0.5, pad=1.2)  # 5.5 pt: sanctioned house-style exception
for sp in cb_ax.spines.values():
    sp.set_linewidth(0.5)                      # inset colorbar has no .outline
cb_ax.set_ylabel("Row z-score", fontsize=5.5, labelpad=1.5)  # set_label: no fontsize
```

- Diverging map only with a meaningful center (`center=0`, symmetric vmin/vmax for
  z-scores); sequential map (`viridis`/`cividis`) for plain magnitudes.
- Relative inset width/height require a 4-tuple/Bbox `bbox_to_anchor` — a plain
  (x, y) pair crashes.
- Clustered heatmaps: prefer the cnsplots clustered-heatmap function, else
  `seaborn.clustermap`; keep the locked cell,
  border, and colorbar styling on top.

## UMAP / t-SNE embedding

```python
# scanpy path (recommended for single-cell data)
import scanpy as sc
sc.pp.neighbors(adata, n_neighbors=15)
sc.tl.umap(adata)
sc.pl.umap(adata, color="cell_type", palette="okabe_ito", save=False, show=False)
# → grab the returned axes, re-style minimal, save one PDF

# generic path: embedding coordinates already computed → cnsplots scatter
cns.figure(width=252, height=252)   # 88.9 x 88.9 mm square
cns.scatterplot(x=emb[:,0], y=emb[:,1], hue=labels)
# label axes on the returned axes: "UMAP 1" / "UMAP 2"
cns.savefig("细胞类型UMAP分布.pdf")
```

- Never implement UMAP/t-SNE/PCA yourself — `scanpy`, `umap-learn`, `openTSNE`,
  `sklearn.manifold` / `sklearn.decomposition`.
- Coloring by a continuous gene: sequential viridis/cividis + colorbar, not a rainbow.
- Equal aspect ratio (`ax.set_aspect("equal")` on the returned axes).

## Volcano plot (Immunity house style)

**Standard name:** volcano plot. The single message: **which genes are
significantly up- or down-regulated, and how strongly.** Modeled on
Immunity/Cell Press volcano panels (e.g. PMC7368915 Fig 3B): gray null mass,
blue down / vermillion up, dashed thresholds, a handful of gene callouts.

`cnsplots.volcanoplot` exists but cannot express the locked house style (cap
staggering, flank label slots); drawing on a bare matplotlib axes is sanctioned
here, exactly like the heatmap house style.

### Encoding spec (locked — do not re-derive per figure)

| Element | Encoding | Rule |
|---|---|---|
| Dot color | NS / down / up | NS = neutral `"0.78"`; down = Okabe-Ito blue `#0072B2`; up = Okabe-Ito vermillion `#D55E00`. Red-green pairs are forbidden |
| DE call | `padj < 0.05` AND `|log2FC| >= 1` | thresholds drawn as 0.5 pt gray dashed lines (`(0, (4, 3))`), both verticals + the horizontal |
| y axis | −log10(adjusted P) | **capped** (`CAP = 40`); genes beyond the cap are **rank-staggered** inside the cap band (0.12 pt steps by true significance) — disclose in the caption, never let one outlier flatten the cloud |
| Gene labels | ≤2 per side inside the crowded cap zone at **fixed flank slots** with leader lines; 2–3 per side in open space via `adjustText` | gene symbols plain Arial 7 pt; never label more than ~9 genes total |
| Axes | left+bottom spines only | x = log2 fold change; no gridlines, no in-figure title, no legend box |

```python
# Volcano plot (Immunity house style) — which genes are significantly
# up- or down-regulated, and how strongly.
import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

mpl.rcParams.update({                    # mandatory style block (references/api.md)
    "font.family": "sans-serif", "font.sans-serif": ["Arial"],
    "mathtext.fontset": "custom", "mathtext.rm": "Arial",
    "mathtext.it": "Arial:italic", "mathtext.bf": "Arial",
    "pdf.fonttype": 42, "font.size": 7,
    "axes.spines.right": False, "axes.spines.top": False,
    "axes.linewidth": 0.7, "legend.frameon": False,
    "xtick.major.width": 0.7, "ytick.major.width": 0.7,
})

SRC = "DE.csv"
# map onto the source table (DESeq2: gene_name/log2FoldChange/padj;
# clusterProfiler or limma exports differ — adapt the three names)
COL = {"gene": "gene_name", "lfc": "log2FoldChange", "p": "padj"}
OUT = "差异表达火山图"
LFC, ALPHA, CAP = 1.0, 0.05, 40.0
N_SLOTS, N_OPEN = 2, 2                  # labels per side: cap zone / open space

d = pd.read_csv(SRC)
n_na = int(d[COL["p"]].isna().sum())
d = d.dropna(subset=[COL["p"]]).copy()
d["nlp"] = -np.log10(pd.to_numeric(d[COL["p"]], errors="coerce"))
up = (d.nlp > -np.log10(ALPHA)) & (d[COL["lfc"]] >= LFC)
dn = (d.nlp > -np.log10(ALPHA)) & (d[COL["lfc"]] <= -LFC)
beyond = d.nlp > CAP
d["nlp_c"] = d.nlp.clip(upper=CAP)      # sort the capped band by true significance
order = d.loc[beyond, "nlp"].sort_values(ascending=False)
d.loc[order.index, "nlp_c"] = CAP - 0.12 * np.arange(len(order))

NS_C, UP_C, DN_C = "0.78", "#D55E00", "#0072B2"   # Okabe-Ito vermillion / blue
fig, ax = plt.subplots(figsize=(252 / 72, 2.85), facecolor="white")  # 88.9 mm single col
fig.subplots_adjust(left=0.155, right=0.985, top=0.97, bottom=0.155)
ax.scatter(d.loc[~(up | dn), COL["lfc"]], d.loc[~(up | dn), "nlp_c"],
           s=4, color=NS_C, rasterized=True, zorder=2)
ax.scatter(d.loc[dn, COL["lfc"]], d.loc[dn, "nlp_c"], s=9, color=DN_C, zorder=3)
ax.scatter(d.loc[up, COL["lfc"]], d.loc[up, "nlp_c"], s=9, color=UP_C, zorder=3)
ax.axhline(-np.log10(ALPHA), color="0.45", lw=0.5, ls=(0, (4, 3)), zorder=1)
for xv in (-LFC, LFC):
    ax.axvline(xv, color="0.45", lw=0.5, ls=(0, (4, 3)), zorder=1)

# cap-zone genes: fixed flank slots + short leader lines (adjustText cannot
# separate labels that start stacked at the same clamped position)
def slot_labels(rows, side):
    for i, (_, r) in enumerate(rows.iterrows()):
        ly = CAP + (2.6 if i == 0 else -0.4)      # two stacked slots per side
        lx = r[COL["lfc"]] + (2.6 if side == "up" else -2.6)
        ax.plot([r[COL["lfc"]], lx - (0.25 if side == "up" else -0.25)],
                [r.nlp_c, ly], color="0.55", lw=0.4, zorder=4)
        ax.text(lx, ly, r[COL["gene"]], fontsize=7, zorder=5,
                ha="left" if side == "up" else "right", va="center")

slot_labels(d[dn & beyond].nsmallest(N_SLOTS, COL["p"]), "dn")
slot_labels(d[up & beyond].nsmallest(N_SLOTS, COL["p"]), "up")

# open-space genes: adjustText handles them freely
open_pick = pd.concat([d[dn & ~beyond].nsmallest(N_OPEN, COL["p"]),
                       d[up & ~beyond].nsmallest(N_OPEN + 1, COL["p"])])
texts = [ax.text(r[COL["lfc"]], r.nlp_c, r[COL["gene"]], fontsize=7, zorder=5)
         for _, r in open_pick.iterrows()]
from adjustText import adjust_text
adjust_text(texts, ax=ax, expand=(1.2, 1.5),
            arrowprops=dict(arrowstyle="-", lw=0.4, color="0.45"))

ax.set_xlim(-7.6, 7.6)                  # widen to the data range if needed
ax.set_ylim(-3, CAP + 6)
ax.set_xlabel("$\\log_{2}$ fold change", fontsize=7)
ax.set_ylabel("$-\\log_{10}$ adjusted $P$", fontsize=7)
ax.tick_params(labelsize=7)
plt.tight_layout(pad=0.1)
fig.savefig(f"{OUT}.pdf")               # exact 88.9 mm canvas, no tight crop
plt.close(fig)
print(f"QA: up {int(up.sum())}, down {int(dn.sum())}, capped {int(beyond.sum())}, "
      f"genes w/o adjusted P not shown: {n_na}")
```

```bash
python scripts/figure_qa.py verify 差异表达火山图.pdf --width-mm 88.9
python scripts/figure_qa.py preview 差异表达火山图.pdf
python scripts/figure_qa.py audit-text 差异表达火山图.pdf
```

**Caption must state:** DE method and model (e.g. DESeq2, Wald test), thresholds
(`padj < 0.05`, `|log2FC| >= 1`), numbers of up/down genes, that −log10(adjusted
P) is capped at 40 with beyond-cap genes staggered by true rank (not to scale),
and how many genes lack an adjusted P and are therefore not shown.

---

## Forest / effect-size plot

```python
# prefer the dedicated cnsplots forest-plot function; fallback on the returned axes:
ax.errorbar(effect, y=labels, xerr=[lo, hi], fmt="o", ms=3,
            color=OKABE_ITO["blue"], ecolor="0.3", elinewidth=0.7, capsize=1.5)
ax.axvline(0, lw=0.5, color="0.6")
```

Effect sizes and CIs from `statsmodels` / `pingouin`, never hand-computed.

## Proportions / composition

Single stacked bar or 100% bar via the cnsplots stacked-bar function
(`cns.stackplot`); prefer a simple stacked bar over pies. Pie charts: avoid
(angle decoding is weak); use only when composition with very few parts is the
entire message.

## GSEA running-enrichment plot (GseaVis, R render)

**Standard name:** GSEA running-enrichment plot (enrichplot::gseaplot2 family).
The single message: **one gene set's enrichment score sweeps up through the
ranked list and peaks at the leading edge.** Use for visualizing a single
pathway's prerank-GSEA result (gseapy/fgsea/clusterProfiler output).

**The one sanctioned R render.** No Python package draws this curve well
(gseapy's plots are the ceiling — surveyed 2026-09); the field standard is the
R package **GseaVis**. Everything else in the figure stays Python. Render via
`scripts/render_gseavis.R` (single source — do not hand-roll); set up R once
with `scripts/install_gseavis.R`, which installs GseaVis with three local
patches for upstream bugs:

| Patch | Upstream bug | Fix |
|---|---|---|
| P1 | DOSE ≥ 4.6 declares `get_organism` as an export but never defines it — GseaVis crashes at load | lazy shim in `00-funcs-from-others.R` |
| P2 | rank panel's unparenthesized `if/else` scale swallowed the rest of the ggplot chain | parenthesized + new `rank_ylim` / `rank_fc_lim` parameters |
| P3 | strip/fill gradient auto-limits took ±30 extremes, washing the mid-band to pastel | `rank_fc_lim` windows the colour scale |

Install gotchas: keep every path ASCII (Chinese usernames get mangled inside
R's env handling); install sequentially — parallel source installs race on
GO.db. The script encodes all of this.

### Style spec (locked)

| Element | Encoding | Rule |
|---|---|---|
| ES curve | single accent element | **monochrome lightness ramp** of one hue: `#7A2A00 → #D55E00 → #F0A57C` (vermillion), lw 1.2 — never a cross-hue RGB gradient (references/color-scheme-design.md rule 1) |
| Strip + ranked fill | per-gene Wald statistic | **pure RdBu 11-class ramp** (ColorBrewer, endpoints #053061 ↔ #67001F), limits = the rank window, alpha = 1 |
| Rank panel y window | `rank_ylim = ±k` | `k = max(1.5, ceil(q97.5(abs(stat)) × 1.25, to 0.5))` — covers the central band; extreme tails zoomed out via coord_cartesian (disclose in caption) |
| Colour window | `rank_fc_lim = ±k` | same window as y — visible data spans the full gradient, beyond squishes to the saturated ends |
| x-tick step | `rankSeq = nice_step(N/4)` | adaptive ~4 intervals, snapped to 1/2/2.5/5×10^k (N=20k → 5000; N=60k → 20000; N=80k → 20000) |
| Title | pathway name | sanctioned exception: a single-pathway GSEA plot identifies itself |
| P values | on-figure italic (`addPval = TRUE`) | GSEA convention; numbers come from the object's own test |
| Canvas | 89 × 76 mm, `cairo_pdf`, `family = "Arial"` | OUT stem stays ASCII; rename to Chinese in the shell |

### Usage

```r
# edit CONFIG in scripts/render_gseavis.R: SRC_DE, SRC_GMT, SRC_GSEA, TERM, OUT
Rscript render_gseavis.R
# then rename OUT.pdf -> <中文描述>.pdf and QA:
#   python scripts/figure_qa.py verify <中文名>.pdf --width-mm 88.9
#   python scripts/figure_qa.py preview <中文名>.pdf
```

**Caption must state:** rank metric provenance (e.g. DESeq2 Wald statistic),
gene-set source and size, hits / leading-edge count, ES / NES / p / FDR (from
the object's own test), and the rank window ±k with the beyond-window tail
count.

---

## GO enrichment dotplot (Immunity house style)

**Standard name:** GO/KEGG enrichment dotplot (clusterProfiler `dotPlot` family,
Cell Press / Immunity house style). The single message: **which pathways are
enriched, how significant each is, and how many genes drive it.** Rows may be
individual GO terms or merged pathway groups — the recipe is identical.

### Encoding spec (locked — "画富集图" means this, do not re-derive)

| Element | Encoding | Rule |
|---|---|---|
| Rows | pathways, sorted by −log10(P) | most significant always on top |
| x position | gene ratio | plotted in **percent** with one decimal (0.0067 → "0.7"); limit = max × 1.15 |
| Dot size | gene count | `(10 + 1.8 * count)` pt² — largest dot ≈ 12 pt diameter |
| Dot color | −log10(P) | ColorBrewer **Oranges**, sequential `Normalize(0, VMAX)` with `VMAX = max(3, ceil(max))`; **no dot edges**; a diverging red-blue scale for P values is forbidden (no meaningful center) |
| Colorbar | thin, top-right | width 0.012 of the figure, ticks at 0 / mid / max only |
| Size key | 3 reference dots | **filled with the data palette (#FD8D3C), not gray**, below the colorbar; values = 5th percentile / median / max of the counts |
| Text | Arial 7 pt everywhere, labels wrapped at 24 chars | legend block stays in the top-right corner and must never dominate the panel |

```python
# GO enrichment dotplot (Immunity house style) — one message: which pathways
# are enriched, how significant, and how many genes drive each.
import textwrap

import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

mpl.rcParams.update({                    # mandatory style block (references/api.md)
    "font.family": "sans-serif", "font.sans-serif": ["Arial"],
    "mathtext.fontset": "custom", "mathtext.rm": "Arial",
    "mathtext.it": "Arial:italic", "mathtext.bf": "Arial",
    "pdf.fonttype": 42, "font.size": 7,
    "axes.spines.right": False, "axes.spines.top": False,
    "axes.linewidth": 0.7, "legend.frameon": False,
    "xtick.major.width": 0.7, "ytick.major.width": 0.7,
})

SRC = "enrichment.csv"
# map the recipe's canonical fields onto the source file's columns
# (clusterProfiler exports Description/GeneRatio/P.adjust/Count; Enrichr differs)
COL = {"term": "Description", "ratio": "GeneRatio", "p": "P_value", "count": "GeneCount_overlap"}
OUT = "GO富集点图"

d = pd.read_csv(SRC)
d["nlp"] = -np.log10(pd.to_numeric(d[COL["p"]], errors="coerce").fillna(1))
d = d.sort_values("nlp").reset_index(drop=True)   # sort FIRST so rows/x/size/color stay aligned

r = d[COL["ratio"]]
if r.dtype == object:  # clusterProfiler exports gene ratio as the string "k/n"
    r = r.map(lambda v: float(v.split("/")[0]) / float(v.split("/")[1])
              if isinstance(v, str) and "/" in v else float(v))
ratio = r.to_numpy(float)
count = pd.to_numeric(d[COL["count"]], errors="coerce").fillna(0).to_numpy(int)
nlp = d["nlp"].to_numpy(float)
labels = [textwrap.fill(t, 24) for t in d[COL["term"]]]

SIZE = lambda c: 10 + c * 1.8                  # count -> pt²; largest dot ≈ 12 pt diameter
VMAX = max(3.0, float(np.ceil(nlp.max())))     # round color cap — state it in the caption

fig, ax = plt.subplots(figsize=(340 / 72, 2.9), facecolor="white")  # 340 px = 119.9 mm
fig.subplots_adjust(left=0.435, right=0.815, top=0.97, bottom=0.16)

sc = ax.scatter(ratio, range(len(d)), s=SIZE(count), c=nlp, cmap="Oranges",
                norm=mpl.colors.Normalize(vmin=0, vmax=VMAX), zorder=3)   # no dot edges
ax.set_yticks(range(len(d)), labels, fontsize=7, linespacing=0.95)
ax.set_xlabel("Gene ratio (%)", fontsize=7)
ax.set_xlim(0, ratio.max() * 1.15)
ax.xaxis.set_major_formatter(mpl.ticker.FuncFormatter(lambda v, _: f"{v*100:.1f}"))
ax.tick_params(labelsize=7)
ax.margins(y=0.06)

# compact Immunity-style legend block, top-right corner
cax = fig.add_axes([0.845, 0.62, 0.012, 0.30])
cb = fig.colorbar(sc, cax=cax)
cb.set_ticks(np.linspace(0, VMAX, 3))
cb.ax.tick_params(labelsize=7, length=1.0, width=0.4, pad=0.8)
cb.outline.set_linewidth(0.4)
cb.set_label("$-\\log_{10}P$", fontsize=7, labelpad=1.5)

lax = fig.add_axes([0.825, 0.13, 0.155, 0.33]); lax.set_axis_off()
lax.text(0.5, 1.0, "Gene count", ha="center", va="top", fontsize=7, color="black")
refs = [int(np.percentile(count, 5)), int(np.percentile(count, 50)), int(count.max())]
for i, c in enumerate(refs):
    lax.scatter([i], [0], s=SIZE(c), facecolor="#FD8D3C", edgecolor="0.45", linewidth=0.3)
    lax.text(i, -0.85, str(c), ha="center", va="top", fontsize=7, color="black")
lax.set_xlim(-0.5, 2.5); lax.set_ylim(-1.9, 0.85)

fig.savefig(f"{OUT}.pdf")            # exact 119.9 mm canvas, no tight crop
plt.close(fig)
```

```bash
python scripts/figure_qa.py verify GO富集点图.pdf --width-mm 119.9
python scripts/figure_qa.py preview GO富集点图.pdf
python scripts/figure_qa.py audit-text GO富集点图.pdf
```

**Caption must state:** enrichment test and source (e.g. Enrichr Fisher exact /
clusterProfiler hypergeometric), number of pathways, dot size = gene count,
dot color = −log10(P) with the VMAX cap, and that rows are sorted by
significance. Reference style: Immunity/Cell Press enrichment dotplots
(compact data-colored legend, sequential scale).

---

## GO gene-concept network (cnetplot style)

**Standard name:** Gene-Concept Network — clusterProfiler's `cnetplot`. The single
message: **which enriched pathways the gene set hits, and which shared genes glue
those pathways together.** Use for Enrichr / clusterProfiler / clusterMagellan
output with ~30 terms or fewer; with more terms, merge by gene-set similarity or
take the TopN first (state the cut in the caption).

### Encoding spec (locked — do not re-derive per figure)

| Element | Encoding | Rule |
|---|---|---|
| Term circle size | `n_genes` (genes enriched in the term) | `(210 + 2.7 * n_genes) * S²` pt² |
| Term circle color | `-log10(P)` | ColorBrewer **Oranges**, floor at 0.35, ceiling at `-log10(P) = 8`; a **labeled colorbar is mandatory** — a continuous encoding without one is undecodable |
| Specific gene dot | belongs to exactly one term | `#FDD0A2` (ColorBrewer Oranges 5-class, bin 2), size `38 * S²` |
| Shared gene dot | in ≥2 terms (the hubs) | `#E6550D` (Oranges 5-class, bin 4), size `76 * S²` — hubs must read at a glance |
| Edges | term ↔ gene membership | neutral gray `"0.55"`, width `0.42 * S`, alpha 0.42 |
| Term labels | pathway name + GO ID, `textwrap` at 25 chars | Arial 7 pt on a translucent white chip; pairwise box repulsion (≤140 rounds); leader line only when displaced > 0.045 |
| Gene labels | **none in the figure** | hundreds of 7 pt labels cannot survive; gene semantics go in the caption |

### Layout (deterministic — same input, same figure)

1. **Bipartite graph**: term nodes + gene nodes, edges = membership; a gene in
   ≥2 terms is flagged `shared`.
2. **Term skeleton**: spring layout on pairwise gene-set **Jaccard similarity**
   (+0.008 base weight so isolated terms do not fly away), `seed=17`, `k=0.24`,
   800 iterations — similar pathways cluster automatically.
3. **Gene placement**: shared genes sit near the centroid of their terms with
   jitter that grows with the number of terms (σ = 0.025 + 0.008·min(k, 4));
   specific genes form a satellite ring (radius 0.06–0.13). Jitter seeds come
   from the gene name's **MD5**, so the same gene always lands in the same place.
4. **Labels**: anchored radially outside the node cloud, repelled pairwise in
   display coordinates; leader lines only when a label moved far.

```python
# GO gene-concept network (cnetplot style) — one message: which pathways the
# gene set hits, and which shared genes glue pathways together.
import hashlib
import itertools
import textwrap

import matplotlib as mpl
import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
import pandas as pd

mpl.rcParams.update({                    # mandatory style block (references/api.md)
    "font.family": "sans-serif", "font.sans-serif": ["Arial"],
    "mathtext.fontset": "custom", "mathtext.rm": "Arial",
    "mathtext.it": "Arial:italic", "mathtext.bf": "Arial",
    "pdf.fonttype": 42, "font.size": 7,
})

SRC = "GO富集图.txt"        # Enrichr TSV: Library, Term, n_genes, P-value, Odds Ratio, Genes
OUT = "GO富集基因概念网络图"  # Chinese filename -> OUT.pdf + OUT_预览.png
SEED = 17                   # layout seed — fixed for reproducibility
WIDTH_IN = 17.0             # canvas follows content (see exemption note below)
S = WIDTH_IN / 17.0         # ink scale: node areas scale S², line widths S

df = pd.read_csv(SRC, sep="\t", encoding="utf-8-sig", usecols=range(6))
df["n_genes"] = pd.to_numeric(df["n_genes"], errors="coerce").fillna(1)
df["P-value"] = pd.to_numeric(df["P-value"], errors="coerce").fillna(1)
gene_sets = [set(str(g).split(";")) - {"nan", ""} for g in df["Genes"]]
freq = {g: sum(g in s for s in gene_sets) for g in set().union(*gene_sets)}

# bipartite graph: terms (circles) + genes (dots)
G = nx.Graph()
for i, row in df.iterrows():
    G.add_node(i, kind="term", label=row["Term"], n=row["n_genes"], p=row["P-value"])
    for gene in gene_sets[i]:
        node = f"gene:{gene}"
        G.add_node(node, kind="gene", label=gene, shared=freq[gene] > 1)
        G.add_edge(i, node)

# term skeleton: spring layout on gene-set Jaccard similarity
sim = nx.Graph()
sim.add_nodes_from(list(range(len(df))))
for i, j in itertools.combinations(range(len(df)), 2):
    union = len(gene_sets[i] | gene_sets[j])
    sim.add_edge(i, j, weight=(len(gene_sets[i] & gene_sets[j]) / union if union else 0) + 0.008)
term_pos = nx.spring_layout(sim, seed=SEED, k=0.24, iterations=800, scale=0.56,
                            weight="weight")

# gene placement: shared genes near their terms' centroid, specific genes ring out
pos = {i: np.asarray(term_pos[i], float) for i in range(len(df))}
for node, d in G.nodes(data=True):
    if d["kind"] != "gene":
        continue
    members = list(G.neighbors(node))
    base = np.mean([pos[t] for t in members], axis=0)
    rng = np.random.default_rng(
        int.from_bytes(hashlib.md5(d["label"].encode()).digest()[:4], "little"))
    if len(members) > 1:
        offset = rng.normal(0, 0.025 + 0.008 * min(len(members), 4), 2)
    else:
        a, r = rng.uniform(0, 2 * np.pi), rng.uniform(0.06, 0.13)
        offset = r * np.array([np.cos(a), np.sin(a)])
    pos[node] = base + offset

fig, ax = plt.subplots(figsize=(WIDTH_IN, WIDTH_IN * 15 / 17), facecolor="white")
nx.draw_networkx_edges(G, pos, ax=ax, edge_color="0.55", width=0.42 * S, alpha=0.42)

genes = [n for n, d in G.nodes(data=True) if d["kind"] == "gene"]
specific = [n for n in genes if not G.nodes[n]["shared"]]
shared = [n for n in genes if G.nodes[n]["shared"]]
# ColorBrewer Oranges 5-class: #FEEDDE #FDD0A2 #FD8D3C #E6550D #A63603
nx.draw_networkx_nodes(G, pos, nodelist=specific, node_color="#FDD0A2",
                       node_size=38 * S * S, edgecolors="white", linewidths=0.45,
                       alpha=0.9, ax=ax)
nx.draw_networkx_nodes(G, pos, nodelist=shared, node_color="#E6550D",
                       node_size=76 * S * S, edgecolors="white", linewidths=0.55,
                       alpha=0.96, ax=ax)
terms = list(range(len(df)))
term_color = [plt.cm.Oranges(0.35 + 0.55 * min(-np.log10(max(G.nodes[t]["p"], 1e-300)) / 8, 1))
              for t in terms]
term_size = [(210 + G.nodes[t]["n"] * 2.7) * S * S for t in terms]
nx.draw_networkx_nodes(G, pos, nodelist=terms, node_color=term_color,
                       node_size=term_size, edgecolors="white", linewidths=0.9,
                       alpha=0.98, ax=ax)

# labeled colorbar for the continuous encoding (doctrine requirement)
sm = mpl.cm.ScalarMappable(norm=mpl.colors.Normalize(vmin=0, vmax=8), cmap="Oranges")
cbar = fig.colorbar(sm, ax=ax, fraction=0.03, pad=0.015, location="right")
cbar.set_label("$-\\log_{10}P$", fontsize=7)
cbar.ax.tick_params(labelsize=7, length=1.4, width=0.5, pad=1.2)
cbar.outline.set_linewidth(0.5)

# term labels: radial anchor + pairwise box repulsion + leader lines
center = np.mean([pos[t] for t in terms], axis=0)
label_artists = []
for t in terms:
    direction = pos[t] - center
    norm = np.linalg.norm(direction)
    direction = direction / norm if norm else np.array([0.0, 1.0])
    artist = ax.text(*(pos[t] + direction * 0.095), textwrap.fill(G.nodes[t]["label"], 25),
                     ha="center", va="center", fontsize=7, color="black",
                     linespacing=0.90, alpha=0.0, zorder=8, clip_on=False,
                     bbox=dict(facecolor="white", edgecolor="none", alpha=0.90, pad=0.6))
    label_artists.append((t, artist))

ax.set_axis_off()
ax.set_xlim(-0.82, 0.82)
ax.set_ylim(-0.82, 0.82)
fig.canvas.draw()
renderer = fig.canvas.get_renderer()
inverse = ax.transData.inverted()
for _ in range(140):
    changed = False
    boxes = {t: a.get_window_extent(renderer).expanded(1.10, 1.18) for t, a in label_artists}
    items = list(label_artists)
    for i in range(len(items)):
        ta, aa = items[i]
        for tb, ab in items[i + 1:]:
            ba, bb = boxes[ta], boxes[tb]
            ox = min(ba.x1, bb.x1) - max(ba.x0, bb.x0)
            oy = min(ba.y1, bb.y1) - max(ba.y0, bb.y0)
            if ox <= 0 or oy <= 0:
                continue
            ca = np.array([(ba.x0 + ba.x1) / 2, (ba.y0 + ba.y1) / 2])
            cb_ = np.array([(bb.x0 + bb.x1) / 2, (bb.y0 + bb.y1) / 2])
            delta = ca - cb_
            if np.linalg.norm(delta) < 1e-6:
                delta = np.array([1.0, 0.0])
            axis = np.array([1.0, 0.0]) if ox < oy else np.array([0.0, 1.0])
            if np.dot(delta, axis) < 0:
                axis = -axis
            shift = axis * (min(ox, oy) / 2 + 3.5)
            for artist, amount in ((aa, shift), (ab, -shift)):
                x, y = artist.get_position()
                artist.set_position(inverse.transform(ax.transData.transform((x, y)) + amount))
            changed = True
    if not changed:
        break
    fig.canvas.draw()

for t, artist in label_artists:      # leader lines only when a label moved far
    artist.set_alpha(1.0)
    x, y = pos[t]
    lx, ly = artist.get_position()
    if np.hypot(lx - x, ly - y) > 0.045:
        ax.plot([x, lx], [y, ly], color="0.6", linewidth=0.45 * S, alpha=0.6, zorder=7)

plt.tight_layout(pad=0.1)
fig.savefig(f"{OUT}.pdf")            # bounded canvas, no tight crop
plt.close(fig)
```

### Canvas exemption, QA, and caption

**Canvas exemption (house-style sanctioned).** The canvas follows the network:
`WIDTH_IN = 17.0` reproduces the reference figure (≈432 mm wide — poster/PPT
scale, not a journal column). For a journal, either trim to ≤12 terms and set
`WIDTH_IN = 7.2` (183 mm double column) or keep the content canvas and say so.
Node areas scale with `S²`, line widths with `S`; the font stays 7 pt. Do not
export with `bbox_inches="tight"` — `set_xlim`/`set_ylim` already bound the
content. `verify` against the canvas's own width (17 in → `--width-mm 431.8`).

```bash
python scripts/figure_qa.py verify GO富集基因概念网络图.pdf --width-mm 431.8
python scripts/figure_qa.py preview GO富集基因概念网络图.pdf
python scripts/figure_qa.py audit-text GO富集基因概念网络图.pdf   # 7 pt law (mathtext 4.9 pt allowed)
```

**Caption must state:** enrichment method and source (e.g. Enrichr, Fisher exact),
number of terms, dot = gene (light = single term, dark orange = shared hub),
circle size = n_genes, circle color = −log₁₀(P) (cap 8), layout seed 17 for
reproducibility.

---

## Forbidden chart types (do not suggest, do not draw)

- **Dumbbell / 杠铃图** (two dots + connecting segment per row) and
  **lollipop / 棒棒糖图** (stem + dot per row) are **forbidden** — never use
  these, even as
  "compact alternatives" to bars, slopes, or forest plots. When the urge to draw
  one appears, use the established form instead: grouped bar / paired slope via
  `cns.lineplot`, a plain `cns.scatterplot`, or the forest-plot recipe above.
- Never propose them in figure brainstorming and never hand-roll their primitives
  (hlines + scatter) on cnsplots axes — the prohibition covers the workaround.

---

## Universal prohibitions

- No multi-panel composition, no subplot grids — one chart per file. This also
  forbids cnsplots' own composite helpers (`cns.multipanel()`,
  `cns.add_panel_label()`): the doctrine bans the output, not just the tooling.
- No hand-rolled statistical tests, dimensionality reduction, or layout math that a
  mature package already provides.
- No raw seaborn/matplotlib calls for basic chart types (bar, scatter, line, box,
  violin, strip, histogram, KDE, regression) that cnsplots provides — Python mandate.
- No rainbow/jet/turbo, no red-green sole encoding, no decorative gradients.
- No dumbbell/lollipop charts (see Forbidden chart types above).
- No Chinese text inside the figure; filename in Chinese.
- No gridlines, top/right spines, figure borders, or background fills.
