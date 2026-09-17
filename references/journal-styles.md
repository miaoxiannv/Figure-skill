# Journal Style Specs: Nature / Science / Immunity

Specifications below are from the journals' published author guidelines. Always
confirm against the journal's current guide before final submission, as numbers are
revised periodically.

## Size (final print dimensions)

| Journal | Single column | 1.5 column | Double column | Max height |
|---|---|---|---|---|
| Nature | 89 mm | 120 mm | 183 mm | ~170 mm |
| Science | 5.5 cm (55 mm) | 12.0 cm | 18.2 cm | ~22 cm |
| Immunity (Cell Press) | 85 mm | 114 mm | 174 mm | ~234 mm |

**Default choice for this skill: single-column width.** A single-message figure
almost never needs double-column width. Choose double column only when the chart
genuinely cannot stay legible at single-column size.

cnsplots canvases are sized in **pixels at 72 px/in** (`inches = px / 72`):

| Journal | Single column | 1.5 column | Double column |
|---|---|---|---|
| Nature 89 / 120 / 183 mm | 252 px | 340 px | 516 px |
| Science 55 / 120 / 182 mm | 155 px | 340 px | 516 px |
| Immunity 85 / 114 / 174 mm | 240 px | 323 px | 491 px |

Export with `cns.settings.savefig_bbox = "standard"` (never `"tight"`, which crops
the canvas below the column width) and verify the final PDF physical size with
`verify_figure_pdf` (`references/api.md`).

## Typography

**This skill's mandate (tighter than any journal minimum): every character is
Arial 7 pt — one family, one base size.**

| Journal | Journal requirement | This skill mandates |
|---|---|---|
| Nature | Sans-serif, 5–7 pt | Arial, 7 pt |
| Science | Helvetica/Arial, ~6–8 pt | Arial, 7 pt |
| Immunity (Cell Press) | Arial/Helvetica, 6–8 pt, min 5 pt | Arial, 7 pt |

Universal rules:

- **Arial only.** Not "sans-serif in general": lock
  `cns.settings.font_sans_serif = ["Arial"]` (cnsplots) or
  `font.sans-serif: ["Arial"]` (raw matplotlib). Helvetica, DejaVu Sans, Liberation
  Sans and every other fallback family are forbidden in the exported PDF.
- Keep label strings ASCII-only; superscripts via mathtext (`mm$^3$`) — any
  non-ASCII character makes cnsplots swap the whole string to DejaVuSans.
- One font family per figure; vary only weight (regular/bold), never size.
- Embed fonts as editable text (`pdf.fonttype = 42`), and
  verify the embedded font list before delivery.

## Format

- Vector PDF for all line art and text.
- Raster image data (microscopy, blots) at ≥300 dpi at final size when embedded.
- RGB color mode (all three journals accept/convert RGB; Cell Press prefers RGB).
- No borders or boxes around the figure; no background shading.

## Style ethos shared by all three

- Maximum data-ink ratio: remove anything that does not encode data.
- No gridlines by default; if a reference line is meaningful, use one thin gray line.
- Direct labels preferred over legends when marks are spatially stable.
- Color used sparingly and accessibly (see `color-maps.md`); figures must survive
  grayscale printing.
- Statistics (test, n, error-bar definition) reported in the caption, not cluttered
  inside the plotting area.

## This skill's defaults derived from the above

```text
width_mm        = 89          # Nature single column; override per target journal
canvas_px       = 252         # = width_mm / 25.4 * 72 (cnsplots figure width)
font.family     = Arial (only; no fallback families in the exported PDF)
font.size       = 7 pt (uniform: labels, ticks, legend, annotations)
spines          = left + bottom only, 0.7 pt
legend          = frameless, 7 pt
background      = pure white, axes and figure
output          = PDF (submission) + _预览.png (300 dpi review), verify_figure_pdf must pass
```
