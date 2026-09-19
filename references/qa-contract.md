# QA Contract — Pre-Submission Checklist

Run before final delivery, before a revision package, and whenever the figure carries
statistical claims or image data. Journal rules change — verify the current author
guide for the target journal before submission.

## Official references to verify

- Nature research figure guide: `https://research-figure-guide.nature.com/`
- Nature preparing figures/specifications: `https://research-figure-guide.nature.com/figures/preparing-figures-our-specifications/`
- Nature initial submission and statistics guidance: `https://www.nature.com/nature/for-authors/initial-submission`
- Cell Press (Immunity) figure guidelines: `https://www.cell.com/figure-guidelines`
- JCB figure/video guidelines (microscopy image QA): `https://rupress.org/jcb/pages/fig-vid-guidelines`

## Checklist

| Check | Pass condition |
|---|---|
| One message | The figure proves exactly one claim; no composite/multi-panel layout |
| Core message readable | Claim legible from the chart alone in ~10 seconds |
| Backend exclusivity | Python produced all plotting, previews, exports, QA — zero R/ggplot output |
| Output format | Exactly one submission PDF + one `<中文文件名>_预览.png` (300 dpi) companion; no other image files |
| Filename | Chinese, descriptive (e.g. `各组肿瘤重量比较.pdf`) |
| In-figure language | English only; zero Chinese characters inside the figure |
| Font | Arial only — embedded font list contains zero non-Arial families; no serif anywhere |
| Text size | 7 pt uniform (labels, ticks, legend, annotations); 5.5 pt allowed only in the heatmap house style colorbar; verified via `scripts/figure_qa.py audit-text` |
| Final size | Exact journal column width (Nature 89 mm / Science 55 mm / Immunity 85 mm); height within journal limit; no tight-crop shrinkage. Exception: the heatmap house style follows the matrix size — verify against the canvas's own width |
| Automated export check | `python scripts/figure_qa.py verify` passed: one page, Arial-only fonts at any nesting depth (incl. Form XObjects), exact width — a failed check blocks delivery |
| Editable text | `pdf.fonttype = 42`; text selectable, not outlined — `audit-text` fails if no `Tf` text commands exist |
| Background | Pure white; no fills, borders, chartjunk, 3D, shadows, gradients |
| Spines/grid | Left+bottom spines only; no gridlines unless reference-meaningful |
| Data class match | Color map class = variable class (sequential/diverging/cyclic/categorical) |
| Palette provenance | Named palette from the whitelist (viridis/cividis/Crameri/cmocean/ColorBrewer/Okabe-Ito/cnsplots Nature-Cell-Science-Ecotyper); zero ad-hoc hexes |
| Forbidden maps | No rainbow/jet/turbo; no red-green sole encoding |
| Forbidden chart types | No dumbbell (杠铃图) or lollipop (棒棒糖图) charts |
| Heatmap house style | Square cells, thin black borders, RdBu_r for z-scored rows, small manual inset colorbar right of matrix (upper-middle) per references/chart-types.md |
| Diverging center | Diverging map used only with a meaningful, stated center |
| Color bar | Present, labeled, with normalization/limits for every continuous encoding |
| Grayscale survival | Ordering and extrema survive grayscale conversion |
| CVD check | Deuteranopia/protanopia simulation passed (or noted as limitation) |
| Statistics | Test name + package, n per group, error-bar meaning in caption/QA record |
| Mature packages | Charts and tests from established libraries; nothing hand-rolled |
| cnsplots mandate (Python) | Bar/scatter/line/box/violin/strip/histogram/KDE/regression drawn with cnsplots; no raw seaborn/matplotlib for these types |
| Legend | Frameless, outside data or in empty space; direct labels preferred |
| Axis labels | Carry units; y-limits tightened to data range |
| Reproducibility | Palette name/version, normalization, limits, missing-data treatment recorded |
| Image integrity (raster data) | No selective enhancement; adjustments applied to whole image; uncropped originals retained |
