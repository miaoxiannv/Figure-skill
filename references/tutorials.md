# Tutorials — End-to-End Single-Figure Walkthroughs

Each tutorial produces exactly one submission PDF plus its `<中文文件名>_预览.png`
review companion (300 dpi), both from the Chinese filename. Style block and
helpers come from `references/api.md`.

---

## Tutorial 1: Grouped bar with statistics (Python, cnsplots)

**Message**: "Compound A reduces tumour weight versus vehicle."

```python
import matplotlib.pyplot as plt
import cnsplots as cns
import pandas as pd

df = pd.read_csv("tumour_weight.csv")          # columns: group, weight

cns.settings.font_sans_serif = ["Arial"]       # Arial-only, before figure()
cns.settings.savefig_bbox = "standard"         # keep the 88.9 mm canvas
cns.figure(width=252, height=170)              # Nature single column
cns.settings.pvalue_fontsize = 7
plt.rcParams.update({"font.size": 7, "axes.labelsize": 7,
                     "xtick.labelsize": 7, "ytick.labelsize": 7})

ax = cns.barplot(data=df, x="group", y="weight", hue="group", legend=False,
                 order=["Vehicle", "Compound A"],
                 palette=["#B0B0B0", "#0072B2"],      # gray control + Okabe-Ito blue
                 errorbar=("sd", 1), capsize=0.12,
                 pairs=[("Vehicle", "Compound A")])   # cnsplots runs Welch's t-test
ax.set_xlabel(""); ax.set_ylabel("Tumour weight (g)")
plt.gcf().tight_layout()
cns.savefig("化合物A对肿瘤重量的影响.pdf")     # PDF with editable text
verify_figure_pdf("化合物A对肿瘤重量的影响.pdf", width_mm=88.9)
render_preview("化合物A对肿瘤重量的影响.pdf")   # 化合物A对肿瘤重量的影响_预览.png
```

Caption records: Welch's t-test, t, p, n per group, bars = mean ± SD (significance
marks come from cnsplots `pairs=`, never hand-drawn; exact stats live in the caption).

## Tutorial 2: UMAP colored by continuous expression (Python)

**Message**: "Gene X marks a distinct epithelial subpopulation."

```python
import matplotlib as mpl
import scanpy as sc
import matplotlib.pyplot as plt

# Arial 7 pt law applies to scanpy figures too — restyle AFTER scanpy draws
mpl.rcParams.update({
    "font.family": "sans-serif", "font.sans-serif": ["Arial"],
    "mathtext.fontset": "custom", "mathtext.rm": "Arial",
    "mathtext.it": "Arial:italic", "mathtext.bf": "Arial",
    "pdf.fonttype": 42, "font.size": 7,
    "axes.labelsize": 7, "xtick.labelsize": 7, "ytick.labelsize": 7,
    "legend.fontsize": 7,
})

sc.pp.neighbors(adata, n_neighbors=15)
sc.tl.umap(adata)
fig = sc.pl.umap(adata, color="GENEX", cmap="viridis", show=False).figure
# exact single-column canvas — no tight crop
fig.set_size_inches(89/25.4, 70/25.4)
fig.savefig("基因X在UMAP上的表达分布.pdf")
plt.close(fig)
verify_figure_pdf("基因X在UMAP上的表达分布.pdf", width_mm=88.9)
render_preview("基因X在UMAP上的表达分布.pdf")   # 基因X在UMAP上的表达分布_预览.png
```

Sequential viridis + labeled colorbar; embedding computed by scanpy, never by hand.
scanpy resets rcParams on import order changes — re-apply the style block if fonts
come out wrong, and always confirm Arial-only via `verify_figure_pdf`.

## Tutorial 3: Diverging z-score heatmap (Python, house style)

**Message**: "Cluster 3 is depleted for mitochondrial genes relative to cohort mean."

Follows the locked heatmap house style from `references/chart-types.md` (square
cells, thin black borders, RdBu_r, manual inset colorbar right of the matrix):

```python
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import pandas as pd
import seaborn as sns
from matplotlib.transforms import Bbox
from mpl_toolkits.axes_grid1.inset_locator import inset_axes

Z = pd.read_csv("z_scores.csv", index_col=0)   # rows: genes, columns: samples, row z-scored

CELL = 0.125
fig, ax = plt.subplots(figsize=(1.55 + Z.shape[1] * CELL, 0.75 + Z.shape[0] * CELL))
sns.heatmap(Z, cmap="RdBu_r", center=0, vmin=-2, vmax=2, square=True,
            linewidths=0.35, linecolor="black", cbar=False, ax=ax)
ax.set_yticks([i + 0.5 for i in range(Z.shape[0])])
ax.set_yticklabels([f"${g}$" for g in Z.index], rotation=0, fontsize=7)
plt.setp(ax.set_xticklabels(Z.columns, rotation=45, ha="right"), fontsize=7)
ax.tick_params(length=0); ax.set_xlabel(""); ax.set_ylabel("")

anchor = Bbox.from_bounds(1.03, 0.60, 0.10, 0.13)
cb_ax = inset_axes(ax, width="100%", height="100%", loc="lower left",
                   bbox_to_anchor=anchor, bbox_transform=ax.transAxes, borderpad=0)
cb = mpl.colorbar.ColorbarBase(cb_ax, cmap=mpl.colormaps["RdBu_r"],
                               norm=mcolors.Normalize(vmin=-2, vmax=2), ticks=[-2, 0, 2])
cb_ax.tick_params(labelsize=5.5, length=1.4, width=0.5, pad=1.2)
for sp in cb_ax.spines.values():
    sp.set_linewidth(0.5)
cb_ax.set_ylabel("Row z-score", fontsize=5.5, labelpad=1.5)

fig.tight_layout()
fig.savefig("线粒体基因Z分数热图.pdf")
plt.close(fig)
# house-style canvas width follows the column count — verify against its own size
verify_figure_pdf("线粒体基因Z分数热图.pdf",
                  width_mm=round((1.55 + Z.shape[1] * 0.125) * 25.4, 1))
render_preview("线粒体基因Z分数热图.pdf")   # 线粒体基因Z分数热图_预览.png
```

Diverging map justified: zero (cohort mean) is a meaningful center.

---

## Common failure modes

| Failure | Fix |
|---|---|
| Two messages crammed into one chart | Split into two PDFs, two Chinese filenames |
| Basic chart drawn with raw seaborn/matplotlib (Python) | Redraw with cnsplots — the mandate forbids raw primitives for bar/scatter/line/box/violin/strip/hist/KDE/regression |
| Legend inside dense data | Move outside / direct-label with `adjustText` |
| Rainbow coloring of an ordered variable | Replace with viridis/cividis |
| P-values computed by hand | Use scipy/statsmodels/pingouin |
| Chinese characters inside the figure | Translate to English; Chinese only in filename |
| Serif font crept in | Sans-serif stack only; check `pdf.fonttype = 42` |
| Extra PNG files beyond the one `_预览.png` companion | Delete them; PDF + one preview only |
