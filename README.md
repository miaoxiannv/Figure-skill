# nature-figure-pdf

**A reproducible figure-generation system for submission-grade, single-message scientific figures targeting *Nature*, *Science*, *Immunity* and comparable high-impact journals.**

The system is distributed as an agent skill (Python backend, one sanctioned R render) and encodes a fixed set of typographic, statistical and colour principles as non-negotiable doctrine. Every figure is delivered as exactly one vector PDF at the exact journal canvas, accompanied by a 300-dpi PNG review companion, and passes an automated pre-delivery check before it reaches the author.

The workflow skeleton — figure contract before plotting, the blocking backend gate, single-backend rendering with pre-delivery QA, and per-figure independent export — derives from the open-source *nature-figure* agent skill; §10 records the provenance and attribution.

---

## 1. Overview

Publication guidelines from leading journals converge on the same editorial ideal: a figure should be a minimal, self-contained visual argument that survives reproduction — grayscale printing, colour-vision deficiency, and reduction to column width. In practice, figures produced ad hoc routinely violate these constraints: composite panels that bury single claims, mixed font families, rainbow palettes, hand-drawn annotation, and raster exports with non-editable text.

`nature-figure-pdf` addresses this by encoding the guidelines as an executable workflow. Each figure is specified by a *contract* (core message, journal target, canvas, chart type, colour map, statistics, filename) before any code runs; the render then follows one of five **locked house recipes** — fully specified encodings with validated scripts — and the export is gated by an automated audit (`scripts/figure_qa.py`) that verifies page geometry, embedded fonts at any nesting depth, uniform text size, and colour availability.

## 2. Design principles

| # | Principle | Rationale |
|---|---|---|
| 1 | One figure conveys one message | multi-panel composites are rejected by the workflow by design; a multi-point story is delivered as multiple PDFs |
| 2 | Simplicity first | every surviving mark must encode data; chartjunk, 3-D effects, gradients and unnecessary gridlines are removed |
| 3 | Arial, 7 pt, one family | journal minima (5–7 pt) are tightened to one uniform size; embedded fonts are verified in the exported PDF |
| 4 | English in-figure; Chinese filenames | figure text stays ASCII-only for font fidelity; delivery filenames remain descriptive in Chinese |
| 5 | PDF for submission, PNG for review | vector PDF with editable text (`pdf.fonttype = 42`); one 300-dpi preview companion, no other image files |
| 6 | Colour from documented palettes only | ColorBrewer, Okabe–Ito, Crameri, viridis family and cnsplots journal presets; rainbow/jet/turbo and ad-hoc hexes are prohibited |
| 7 | Mature packages only; nothing hand-rolled | Python basic charts via `cnsplots`; statistics from `scipy`/`statsmodels`/`pingouin`; GSEA curves via GseaVis (the single R render) |

## 3. Locked house styles

Five figure classes are governed by fully specified encodings — colour ramps, panel windows, label strategies and canvas geometry are fixed, so identical inputs reproduce identical figures.

| Recipe | Reference convention | Entry point |
|---|---|---|
| Heatmap (house style) | square cells, thin black borders, RdBu_r for z-scores, manual inset colourbar | `references/chart-types.md` |
| GO gene-concept network (cnetplot) | deterministic Jaccard layout, Okabe–Ito gene dots, monochrome-ramp curve accents | `references/chart-types.md` |
| GO/KEGG enrichment dotplot (Immunity style) | significance-sorted rows, percent gene ratio, data-coloured size key | `references/chart-types.md` |
| Volcano plot (Immunity style) | grey null / blue down / vermillion up, dashed thresholds, capped ordinate | `references/chart-types.md` |
| GSEA running-enrichment curve (GseaVis) | monochrome lightness-ramp curve, pure RdBu 11-class data ramp, windowed panels | `scripts/render_gseavis.R` |

Two blocking gates precede any render: the backend rule (Python-only, one R exception) and the cnsplots mandate for basic chart types. Details: `references/backend-selection.md`.

## 4. Colour governance

Colour is governed in three layers:

1. **Palette whitelist** — every colour traces to a documented set: ColorBrewer, Okabe–Ito, Crameri, cmocean, viridis family, or `cnsplots` journal presets (`references/color-maps.md`).
2. **Scheme organisation** — palettes are arranged by a role framework (主色 primary / 辅色 auxiliary / 强调色 accent) and hue-wheel angle formulas: monochrome lightness ramps within single elements, complementary pairs (~180°) for diverging data, triadic spacing (120°) for elements that must jump clear (`references/color-scheme-design.md`). Gradients inside a single element never interpolate across distant hues.
3. **Validation** — grayscale survival, colour-vision-deficiency simulation, and palette-name/version reporting (`references/qa-contract.md`).

## 5. Workflow

1. Backend gate — Python-only; R-origin data (Seurat, DESeq2, RDS) is exported to CSV/TSV before plotting
2. Figure contract — core message, journal target, canvas, chart type, colour map, statistics, Chinese filename
3. Journal specification — Nature 89 mm / Science 55 mm / Immunity 85 mm defaults, Arial 7 pt
4. Render — via the locked house recipe (Python; GSEA curves via the GseaVis R render)
5. Quality assurance — `scripts/figure_qa.py`, then grayscale and CVD checks; a failed check blocks delivery

## 6. Installation and usage

```bash
# Python >= 3.10
pip install cnsplots adjustText pymupdf
# optional, one-time: patched GseaVis for GSEA curves (R >= 4.5)
Rscript scripts/install_gseavis.R
```

Each figure class is rendered through its single-source script or recipe snippet; see `references/chart-types.md` and `references/tutorials.md`. The QA gate runs on every export:

```bash
python scripts/figure_qa.py verify <figure>.pdf --width-mm 88.9
python scripts/figure_qa.py preview <figure>.pdf
python scripts/figure_qa.py audit-text <figure>.pdf
```

### Updates

The skill folder is stateless — updating replaces only its files; the R library installed by `scripts/install_gseavis.R` lives elsewhere and is untouched. Three sync paths:

| Install origin | Update command |
|---|---|
| Skills CLI (`npx skills add miaoxiannv/Figure-skill`) | re-run the same command |
| `git clone` | `git -C <skill dir> pull` |
| archive / manual copy | `python scripts/check_update.py --check` → `--update` |

`VERSION` tracks the running version; releases are tagged on GitHub.

## 7. Quality assurance and reproducibility

- `verify` asserts one page, Arial-only embedded fonts at any nesting depth (including Form XObjects), and exact physical width (±0.3 mm)
- `audit-text` scans the content stream: every text run is 7 pt (mathtext sub/superscripts 0.7×; heatmap colourbar 5.5 pt by exemption), and outlined text fails
- Deliverables are deterministic: fixed layout seeds (cnetplot), seeded simulation, and recorded palette/limit/normalisation metadata in the caption record
- 16 behavioural evaluations (`evals/evals.json`) pin the doctrine: backend exclusivity, one-message splitting, language policy, palette provenance, cnsplots mandate, locked house styles

## 8. Repository structure

```
nature-figure-pdf/
├── SKILL.md                     ← trigger description and doctrine
├── README.md                    ← this document
├── evals/evals.json             ← behavioural evaluations
├── scripts/
│   ├── figure_qa.py             ← single-source QA (verify/preview/audit-text/font.check)
│   ├── render_gseavis.R         ← GSEA running-enrichment curve (sanctioned R render)
│   └── install_gseavis.R        ← one-time patched GseaVis setup
└── references/
    ├── figure-contract.md       ← figure contract template
    ├── journal-styles.md        ← Nature / Science / Immunity specifications
    ├── color-maps.md            ← palette whitelist, selection and audit
    ├── color-scheme-design.md   ← scheme organisation: roles and hue-wheel formulas
    ├── backend-selection.md     ← backend rules and R-origin data handling
    ├── design-theory.md         ← minimalism, typography, export policy
    ├── api.md                   ← constants, helpers, cnsplots behaviour notes
    ├── chart-types.md           ← locked single-chart recipes
    ├── tutorials.md             ← end-to-end walkthroughs
    └── qa-contract.md           ← pre-submission checklist
```

## 9. Scope

**Intended use.** Single scientific charts for journal submission — bar, violin, scatter, line, heatmap, UMAP/t-SNE, volcano, forest, survival, enrichment dotplot, gene-concept network, GSEA running-enrichment curve — and audits of existing figures against the same standards.

**Out of scope.** Multi-panel composites (prohibited by principle 1), interactive or exploratory-only graphics, Illustrator/Figma-first layouts, and non-journal deliverables.

## 10. Provenance and attribution

This system is a derivative work: the *nature-figure* agent skill serves as the foundation on which the additional rules of this repository were built.

- **Foundation.** The *nature-figure* agent skill — figure contract before plotting, backend gate, single-backend render, QA before delivery, independent export — as distributed by [jing1312/nature-figure-skill](https://github.com/jing1312/nature-figure-skill) (MIT License), an independently hosted derivative snapshot of the upstream project below (baseline commit `f3941a1`, May 2026).
- **Ultimate upstream.** [Yuan1z0825/nature-skills](https://github.com/Yuan1z0825/nature-skills) (Apache-2.0), the research agent-skill collection where the *nature-figure* skill originates.

Built on that foundation, this repository adds: the Python-only backend mandate with R-origin data exported to CSV/TSV (one sanctioned GseaVis render); the cnsplots requirement for basic chart types; the one-figure-one-message doctrine with prohibition of composites; the five locked house recipes (§3); the single-source QA script `scripts/figure_qa.py` with full-depth font auditing; the PDF-plus-300-dpi-PNG deliverable contract; the colour-governance framework (§4); the Chinese-filename delivery policy; and the behavioural evaluation suite. Unmodified upstream material is not claimed as original work; redistribution of this repository should preserve the attributions above.

## References

1. Nature Portfolio. *Research figure guide.* https://research-figure-guide.nature.com/
2. Cell Press. *Figure guidelines.* https://www.cell.com/figure-guidelines
3. Harrower M, Brewer CA (2003). ColorBrewer.org: an online tool for selecting colour schemes for maps. *The Cartographic Journal* 40:27–37.
4. Okabe M, Ito K (2008). *Color universal design (colorbar)*. https://jfly.uni-koeln.de/color/
5. Crameri F, Shepard GE, Heron PJ (2020). The misuse of colour in science communication. *Nature Communications* 11:5444.
6. Subramanian A et al. (2005). Gene set enrichment analysis: a knowledge-based approach for interpreting genome-wide expression profiles. *PNAS* 102:15545–15550.
7. Wu T et al. (2021). clusterProfiler 4.0: a universal enrichment tool for interpreting omics data. *The Innovation* 2:100141.
8. Zhang J, Li H, Tao W, Zhou J (2025). GseaVis: an R package for enhanced visualization of gene set enrichment analysis in biomedicine. *Med Research.*
9. Love MI, Huber W, Anders S (2014). Moderated estimation of fold change and dispersion for RNA-seq data with DESeq2. *Genome Biology* 15:550.
10. Yuan1z0825 and contributors. *nature-skills: agent skills for research and scientific figure workflows.* https://github.com/Yuan1z0825/nature-skills (Apache-2.0).
11. jing1312 and contributors. *nature-figure-skill: independently hosted nature-figure agent skill.* https://github.com/jing1312/nature-figure-skill (MIT).
