# Chart Types — Single-Chart Recipes

One chart per figure, from mature packages. **Python mandate: basic chart types — bar,
scatter, line, box, violin, strip, histogram, KDE, regression — MUST be drawn with
`cnsplots` (`import cnsplots as cns`). Raw seaborn/matplotlib calls for these types are
forbidden; if cnsplots is missing, stop and install/report — never fall back silently.**
seaborn/matplotlib remain allowed for chart types cnsplots does not cover (heatmap,
UMAP styling) and for fine-tuning the axes cnsplots returns. Every recipe saves one PDF
with a Chinese filename; before `cns.figure(...)` lock
`cns.settings.font_sans_serif = ["Arial"]` and `cns.settings.savefig_bbox = "standard"`,
size the canvas in px (px = mm / 25.4 × 72; Nature single column 89 mm = 252 px),
set every text element to 7 pt, and verify the export with `verify_figure_pdf`
(`references/api.md`).

---

## Bar / grouped bar (group comparison)

```python
import cnsplots as cns

cns.settings.font_sans_serif = ["Arial"]
cns.settings.savefig_bbox = "standard"
cns.figure(width=252, height=170)                       # 88.9 mm Nature single column
cns.barplot(data=df, x="group", y="value", hue="group", legend=False,
            palette=["#B0B0B0", "#0072B2"],             # neutral gray control + Okabe-Ito blue
            errorbar=("sd", 1), capsize=0.12,
            pairs=[("Control", "Treated")])             # built-in Welch's t-test bracket
cns.savefig("各组指标比较.pdf")
verify_figure_pdf("各组指标比较.pdf", width_mm=88.9)     # mandatory check, references/api.md
```

- Two conditions max; more conditions → simplify the question or facet into
  separate figures.
- Significance marks come from `pairs=` (cnsplots runs Welch's t-test itself;
  `test=`/`p_adjust=` kwargs crash on 0.6.0 `barplot`) — never hand-drawn
  brackets. The exact test, n per group, and error-bar meaning (SD / SEM / 95% CI)
  still go in the caption, not the figure.

## Box / violin / strip (distribution comparison)

```python
cns.figure(width=252, height=170)   # 88.9 mm single column
cns.violinplot(data=df, x="group", y="value")
cns.savefig("各组分布比较.pdf")

# small n (n < ~10 per group): strip plot instead
cns.figure(width=252, height=170)   # 88.9 mm single column
cns.stripplot(data=df, x="group", y="value")
cns.savefig("各组单点分布.pdf")
```

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

```python
import matplotlib as mpl
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
cb_ax.tick_params(labelsize=5.5, length=1.4, width=0.5, pad=1.2)
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

## Volcano plot (differential test)

```python
# stats from mature packages only, e.g. statsmodels or scanpy rank_genes_groups
cns.figure(width=252, height=170)   # 88.9 mm single column
ax = cns.scatterplot(data=de, x="log2FC", y="neg_log10_p", hue="direction")
ax.axhline(-np.log10(0.05), lw=0.5, color="0.6"); ax.axvline(0, lw=0.5, color="0.6")
cns.savefig("差异表达基因火山图.pdf")
```

- Prefer the dedicated cnsplots volcano function when it matches the data frame;
  otherwise draw the thresholds with `axhline`/`axvline` on the cnsplots axes.

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
