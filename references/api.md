# API Reference — Constants and Helpers

Conventions, constants, and reusable code blocks for the Python backend (the only
backend this skill supports).

---

## cnsplots — mandatory for basic charts (Python)

Basic chart types (bar, scatter, line, box, violin, strip, histogram, KDE, regression)
are drawn with `cnsplots`, never raw seaborn/matplotlib. If the import fails, stop and
report the blocker; offer `pip install cnsplots` (Python ≥ 3.10) — no silent fallback.

Canonical setup — font, size, and export settings are NOT optional:

```python
import matplotlib.pyplot as plt
import cnsplots as cns

cns.settings.font_sans_serif = ["Arial"]   # BEFORE figure(): Arial-only family
cns.settings.savefig_bbox = "standard"     # keep the exact journal canvas (no tight crop)
cns.figure(width=252, height=170)          # 252 px / 72 = 3.5 in = 88.9 mm Nature single col
cns.settings.pvalue_fontsize = 7
cns.settings.title_fontsize = 7
cns.settings.legend_fontsize = 7
plt.rcParams.update({"font.size": 7, "axes.labelsize": 7,
                     "xtick.labelsize": 7, "ytick.labelsize": 7, "legend.fontsize": 7})

ax = cns.barplot(data=df, x="group", y="value", hue="group", legend=False,
                 palette=["#B0B0B0", "#0072B2"],      # approved palettes only
                 pairs=[("Control", "Treated")])      # built-in Welch's t-test bracket
cns.savefig("各组指标比较.pdf")
verify_figure_pdf("各组指标比较.pdf", width_mm=88.9)   # mandatory, see below
```

Verified cnsplots 0.6.0 behaviour (write code against these facts):

- `pairs=[("A", "B")]` alone runs Welch's t-test and draws the bracket. The
  `test=` / `p_adjust=` kwargs do NOT exist on `barplot`/`boxplot` in 0.6.0 —
  passing them crashes. Never hand-draw brackets or hand-compute on-figure p-values;
  exact test, n, and error-bar definitions still go in the external caption.
- `**kwargs` forward to seaborn — use `errorbar=("sd", 1)`, `capsize=0.12`,
  `palette=`, and pass `hue=<x>` + `legend=False` whenever you set `palette`
  (seaborn deprecation otherwise).
- Any non-ASCII character in a text string makes cnsplots swap the WHOLE string to
  DejaVuSans (`apply_unicode_font`). Keep labels ASCII-only and write superscripts
  as mathtext: `"Tumour volume (mm$^3$)"`, never `"mm³"`.
- `settings.savefig_bbox` defaults to `"tight"`, which crops the canvas (88.9 mm
  → ~79.6 mm). `"standard"` keeps the exact pixel canvas; pair it with
  `plt.gcf().tight_layout()` for balanced margins.
- Everything cnsplots returns is a standard matplotlib object: axis labels, limits,
  aspect, `adjustText` repel, and `mpl.rcParams` overrides are allowed fine-tuning;
  re-drawing the chart itself with seaborn/matplotlib primitives is not.
- Chart types outside this mandate (heatmap, UMAP styling, embeddings) keep the
  established packages below.

## Mandatory style block (non-cnsplots charts)

Same law as cnsplots figures: Arial 7 pt, one family, editable text.

```python
import matplotlib as mpl

mpl.rcParams.update({
    "font.family": "sans-serif",
    "font.sans-serif": ["Arial"],   # Arial only — no Helvetica/DejaVu fallback
    "mathtext.fontset": "custom",   # superscripts render in Arial too
    "mathtext.rm": "Arial", "mathtext.it": "Arial:italic", "mathtext.bf": "Arial",
    "pdf.fonttype": 42,
    "font.size": 7,
    "axes.labelsize": 7, "xtick.labelsize": 7, "ytick.labelsize": 7,
    "legend.fontsize": 7, "axes.titlesize": 7,
    "axes.spines.right": False, "axes.spines.top": False,
    "axes.linewidth": 0.7,
    "legend.frameon": False,
    "figure.facecolor": "white", "axes.facecolor": "white",
    "xtick.major.width": 0.7, "ytick.major.width": 0.7,
})
```

## Save helper (PDF + PNG preview, Chinese filename, exact size)

```python
def save_pub(fig, chinese_filename, width_mm=89, height_mm=60):
    """Save exactly one PDF at the exact journal size — no tight crop — then close."""
    fig.set_size_inches(width_mm / 25.4, height_mm / 25.4)
    fig.savefig(f"{chinese_filename}.pdf")
    plt.close(fig)
```

Never export with `bbox_inches="tight"` for journal figures: it silently crops the
canvas below the column width (88.9 mm → ~79.6 mm in practice). Size the canvas
exactly and use `fig.tight_layout()` for margins.

## Review preview PNG (mandatory companion, after verification)

After `verify_figure_pdf` passes, render the user's review companion from the
finished PDF — one PNG per figure, named `<中文文件名>_预览.png`, 300 dpi. Requires
`pip install pymupdf`.

```python
import pymupdf

def render_preview(pdf_path):
    """Render the one-page figure PDF to a 300 dpi <name>_预览.png next to it."""
    doc = pymupdf.open(pdf_path)
    assert len(doc) == 1, f"expected 1 page, got {len(doc)}"
    pix = doc[0].get_pixmap(dpi=300)
    out = pdf_path.removesuffix(".pdf") + "_预览.png"
    pix.save(out)
    return out
```

The PNG is for the user's review only; the PDF is the submission file. Do not
produce any other image files.

## Mandatory pre-delivery verification (Python)

Run on every exported PDF before delivering. Requires `pip install pymupdf` (the
same dependency the preview renderer uses — no separate install).

```python
import pymupdf

def verify_figure_pdf(path, width_mm=88.9):
    """Assert: one page, Arial-only fonts at ANY nesting depth, exact journal width."""
    doc = pymupdf.open(path)
    assert doc.page_count == 1, f"expected 1 page, got {doc.page_count}"
    page = doc[0]
    w_mm, h_mm = page.rect.width / 72 * 25.4, page.rect.height / 72 * 25.4
    fonts = {f[3] for f in page.get_fonts(full=True)}   # f[3] = BaseFont name
    non_arial = {f for f in fonts if "Arial" not in f}
    assert not non_arial, f"non-Arial fonts embedded: {non_arial} — fix font lock"
    assert abs(w_mm - width_mm) < 0.3, f"width {w_mm:.1f} mm != {width_mm} mm"
    print(f"OK: {w_mm:.1f} x {h_mm:.1f} mm, fonts = {sorted(fonts)}")
```

The font scan walks the whole page resource tree — including fonts nested inside
Form XObjects, which a naive page-level `/Resources/Font` read (e.g. a plain
pypdf one-liner) silently misses. Do not downgrade it to a shallower check.

A failure here is a delivery blocker: fix the font lock / canvas size and re-export —
never hand the figure to the user unverified.

---

## Color constants

**Palette whitelist — mature, documented sets only.** Every color in a figure must
come from one of these sources, by name — never an ad-hoc hand-picked hex:

```python
import cnsplots as cns

# Qualitative (categorical groups) — verified cnsplots 0.6.0 names:
cns.palettes("Nature")      # Nature Reviews-inspired journal palette
cns.palettes("Cell")        # Cell-inspired journal palette
cns.palettes("Science")     # Science-inspired journal palette
cns.palettes("Ecotyper1")   # …through "Ecotyper6" — cell-type/subtype palettes
cns.palettes("Set1")        # ColorBrewer qualitative: Set1/Set2/Set3, Dark2, Paired
cns.palettes("Tableau")     # Tableau 10

# Ordered (sequential / diverging):
cns.palettes("parula")          # sequential colormap object
cns.palettes("BuRd_custom")     # blue-white-red diverging
cns.palettes("WhYlOrRd_custom") # white-yellow-orange-red sequential
# matplotlib built-ins stay first choice: "viridis", "cividis", "RdBu_r"
# extended: cmcrameri ("cmc.vik", "cmc.romaO"), cmocean ("cmo.thermal", …)
```

Two-group comparison convention: control/vehicle = neutral gray `#B0B0B0`,
single treatment = Okabe-Ito blue `#0072B2` (both are whitelist constants, below).

### Categorical — Okabe-Ito (color-universal design)

```python
OKABE_ITO = {
    "black":        "#000000",
    "orange":       "#E69F00",
    "sky_blue":     "#56B4E9",
    "bluish_green": "#009E73",
    "yellow":       "#F0E442",
    "blue":         "#0072B2",
    "vermillion":   "#D55E00",
    "reddish_purple": "#CC79A7",
}
OKABE_ITO_ORDER = ["blue", "vermillion", "bluish_green", "orange",
                   "sky_blue", "reddish_purple", "yellow", "black"]
```

Rules: unordered groups only; skip yellow on white backgrounds when marks are thin;
use a maximum of ~6 groups before faceting the question instead.

### Ordered maps — named colormaps, never custom hex ramps

```python
SEQUENTIAL_MAP = "viridis"    # default ordered low→high
SEQUENTIAL_CVD = "cividis"    # use when red-green CVD safety is paramount
DIVERGING_MAP  = "RdBu_r"     # ONLY with a meaningful center (zero, baseline)
CYCLIC_MAP     = "twilight"   # periodic variables only
```

Extended families (install when needed): `cmcrameri` (Crameri scientific colour maps,
e.g. `cmc.batik`, `cmc.vik`, `cmc.romaO`), `cmocean` (e.g. `cmo.thermal`, `cmo.balance`).

### Neutral support

```python
NEUTRALS = {
    "reference_line": "#B0B0B0",   # one thin reference line if needed
    "missing_data":   "#E6E6E6",   # missing/out-of-domain, never a palette color
    "text_dark":      "#1A1A1A",
}
```

---

## Mature-package chart mapping (never hand-roll)

| Chart | Use | Never |
|---|---|---|
| Bar / grouped bar | `cns.barplot` (cnsplots — **mandatory**; `pairs=` runs Welch's t-test) | raw `seaborn.barplot` / matplotlib bars; manual offset loops |
| Box / violin / strip | `cns.boxplot` / `cns.violinplot` / `cns.stripplot` (cnsplots) | seaborn equivalents; hand-drawn whiskers |
| Scatter | `cns.scatterplot` (cnsplots — **mandatory**) | `seaborn.scatterplot` / `ax.scatter` for basic scatter |
| Regression / trend fit | cnsplots regression plot | manual fit-and-fill confidence bands |
| Scatter labels | `adjustText` on the axes cnsplots returns | manual nudging loops |
| Line trend + CI | `cns.lineplot` (cnsplots) | `seaborn.lineplot`; manual ribbons |
| Histogram / KDE / ridge | cnsplots histogram / KDE / ridge functions | hand-binned histograms |
| Heatmap | `seaborn.heatmap` (with `cmap=`, `center=` for diverging); cnsplots clustered heatmap for clustering | manual cell rectangles |
| UMAP | `scanpy.pl.umap` or `umap.UMAP` embedding + `cns.scatterplot` | implementing UMAP/t-SNE yourself |
| Dimensionality reduction | `scanpy` / `sklearn.manifold` | custom SVD-for-plot hacks |
| Statistics | `scipy.stats`, `statsmodels`, `pingouin`; on-figure marks via cnsplots `pairs=` | hand-written t-test/p-values |

## Statistics helper pattern

```python
from scipy import stats

# Always: name the test, report n, define error bars in the caption.
t_stat, p_value = stats.ttest_ind(group_a, group_b, equal_var=False)  # Welch
```

Use `pingouin` for richer output (effect sizes, paired designs, corrected post-hocs:
`pg.ttest`, `pg.anova`, `pg.pairwise_tests`).

## In-bar / in-cell text contrast

```python
def luminance_text_color(hex_color):
    c = hex_color.lstrip("#")
    r, g, b = int(c[0:2],16)/255, int(c[2:4],16)/255, int(c[4:6],16)/255
    return "white" if 0.299*r + 0.587*g + 0.114*b < 0.5 else "#333333"
```

## Color validation

- Grayscale check: `PIL.ImageOps.grayscale` on a rendered check, or reason from the
  palette's monotonic lightness (viridis/cividis guaranteed; verify custom picks).
- CVD simulation: `colorspacious` (`cspace_convert` with `"sRGB1"` → deuteranomaly
  model), or `matplotlib.colors` + manual matrix.
- When auditing palette samples, prefer measured CIELAB checks over eyeballing.

## Hard rules recap

1. One figure, one message — one PDF per figure.
2. English inside the figure; Chinese filename only.
3. **Arial 7 pt only** — one family, one base size, verified in the exported PDF.
4. PDF for submission + one `_预览.png` (300 dpi) review companion; exact journal
   canvas (no tight crop); close the figure after save.
5. Charts and statistics from mature packages only; Python basic charts via cnsplots.
6. Colors from the documented palette whitelist only; colormaps match the data class;
   no rainbow/jet/turbo; colorbar for continuous.
7. Run `verify_figure_pdf` before delivery — a failed check is a delivery blocker.
