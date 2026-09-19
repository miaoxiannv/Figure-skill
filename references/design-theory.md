# Design Theory — Minimalism First

The governing principle: **simplicity is the first element** (简洁第一). Every element
that survives must carry data. Everything else is deleted.

## 1) Typography

### Font stack (priority order)

- **Arial only, 7 pt.** No serif fonts and no fallback families (no Helvetica,
  DejaVu Sans, Liberation Sans) anywhere, ever — including math text and annotations.
- Python: `cns.settings.font_sans_serif = ["Arial"]` (cnsplots, before `figure()`) or
  `font.sans-serif = ['Arial']` (raw matplotlib); mathtext custom-set to Arial.
- PDF editable text: always `pdf.fonttype = 42`
- One family per figure. One base size (7 pt); vary only weight (regular/bold).
- Keep label strings ASCII-only; superscripts via mathtext (`mm$^3$`).

### Font size (final print size)

| Context | Size |
|---------|------|
| Axis labels | 7 pt |
| Tick labels | 7 pt |
| Legend entries | 7 pt |
| Direct data labels | 7 pt |
| Bold emphasis (rare) | 7 pt, bold weight |

One uniform size: 7 pt Arial everywhere — hierarchy comes from weight and
placement, not from mixing sizes. Sanctioned deviations only: mathtext
sub/superscripts (0.7 × base), the heatmap house style's 5.5 pt manual colorbar,
and italic for gene symbols.

## 2) Background and ink

- Pure white background for figure and axes. No tinted panels, no alternating row
  shading, no background fills.
- Maximize data-ink ratio: ink should encode data or necessary structure only.
- Left and bottom spines only, 0.6–0.8 pt. Top and right spines always off.
- No gridlines by default. If a reference line is genuinely meaningful (zero line,
  threshold), use ONE thin light-gray line.
- No 3D effects, shadows, glows, decorative gradients, rounded chart frames, or
  figure borders.
- No panel labels (`a`, `b`, `c`): every output is a single chart, not a composite.

## 3) Legends and labels

- Frameless legends (`legend.frameon = False`), placed in genuinely empty space or
  outside the data region.
- Prefer direct labels next to marks when identities are spatially stable
  (Python: `adjustText`).
- Axis labels carry units: "Tumour volume (mm³)", not "volume".
- Y-limits tightened to the data range — never pad to round numbers when it
  wastes space or exaggerates nothing.

## 4) Color

Color follows `references/color-maps.md` in full. Summary:

- Classify the variable first: sequential / diverging / cyclic / categorical.
- Perceptually uniform palettes only (viridis family, Crameri, cmocean,
  ColorBrewer); Okabe-Ito for categorical groups.
- No rainbow/jet/turbo. No red-green at similar lightness. Color must survive
  grayscale printing.
- Color is an encoding channel, not decoration: every hue change must map to a
  data-semantic change.
- Continuous encodings need a labeled color bar with stated normalization.

## 5) Layout

- Single chart per figure; single-column width (89 mm Nature default) unless the
  chart is illegible at that width.
- Tight margins (`fig.tight_layout()` at the exact journal canvas), no wasted
  whitespace bands — but never export with `bbox_inches='tight'`, which crops the
  canvas below the column width.
- Aspect ratio follows the data: trends need width, distributions need height;
  avoid square defaults unless the data are square (correlations, embeddings).

## 6) Export policy

- PDF for submission. One PDF per figure, plus the `<中文文件名>_预览.png` review
  companion (300 dpi). No SVG/TIFF/JPEG/EPS and no other image files.
- `plt.close(fig)` after every save.
- Filename in Chinese, short and descriptive: `各组肿瘤重量比较.pdf`,
  `单细胞UMAP聚类图.pdf`.

## 7) Simplicity self-audit

Ask, in order:

1. What is the one message? (If unclear, stop — redo the contract.)
2. Does every mark encode data? Delete what does not.
3. Is the simplest viable chart type used?
4. Does it survive grayscale printing?
5. Can anything else be removed without losing the message? If yes, remove it.
