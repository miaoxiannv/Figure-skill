# Figure Contract — One Figure, One Message

Use this reference before writing any plotting code. The figure exists to prove exactly
one thing.

## Privacy rule

Keep the figure contract user-facing, but keep the working trail private. Do not mention
private paths, source filenames, internal reference documents, or template provenance
unless the user explicitly asks.

## Required contract

Create this short contract in working notes or the reply:

```text
Core message:      one sentence with a verb — "Treatment X reduces Y by 40%"
Journal target:    Nature / Science / Immunity / other
Backend:           Python (only)
Final size:        single-column by default (Nature 89 mm = 252 px; see references/journal-styles.md)
Font:              Arial, 7 pt, one family (verified in the exported PDF)
Chart type:        ONE chart type — bar / line / scatter / heatmap / UMAP / violin / ...
Data class:        sequential / diverging / cyclic / categorical
Color map:         palette NAME from the whitelist (references/color-maps.md), matching the data class
Statistics:        test name, package used, n per group, error-bar meaning
Chinese filename:  e.g. 治疗组肿瘤体积变化.pdf
```

If any line cannot be filled, ask the user before plotting.

## Core message rules

- The core message is one sentence with a verb: "Compound A halves tumour volume",
  not "Treatment results".
- The chart type must be the simplest one that displays this single message.
- No panel map, no panel labels: a single-figure output has no `a/b/c` labels.
- If the user asks for a multi-panel or composite figure, **split it**: propose one
  minimal single-chart PDF per message, each with its own Chinese filename. Never
  merge independent figures into one page.
- If the user provides data but no claim, infer a provisional claim from the data and
  ask for confirmation before final styling.

## Choosing the single chart type

| The message is... | Use |
|---|---|
| Group A differs from group B on one metric | bar or box/violin |
| Y changes over time/x | line |
| Two continuous variables co-vary | scatter |
| One continuous variable's structure in 2-D embedding | UMAP/t-SNE scatter |
| Values across two categorical axes | heatmap |
| Distribution shape matters | violin or histogram |
| Enrichment/depletion vs a reference | diverging heatmap |

When two chart types both work, pick the simpler one. Never resolve the choice as
dumbbell (杠铃图) or lollipop (棒棒糖图) — both are forbidden chart types
(references/chart-types.md, "Forbidden chart types"); use bar, line, scatter, or
forest instead.

## Statistics rules

- Use mature statistics packages only — never hand-implement a test:
  `scipy.stats` / `statsmodels` / `pingouin`.
- Name the exact test in the caption (e.g. two-sided Welch t-test, Kruskal–Wallis
  with Dunn's correction, Benjamini–Hochberg FDR).
- State n per group and what error bars show (SD, SEM, or 95% CI).
- Statistics text lives in the external caption or QA record — not inside the figure.

## Aesthetic constraints (from SKILL.md, restated)

- English text inside the figure only; Chinese filename only.
- White background, no top/right spines, no gridlines, frameless legend.
- Arial only, 7 pt uniform, verified in the exported PDF; ASCII-only label strings.
- PDF for submission (one file per figure, exact journal canvas, no tight crop)
  plus one review companion `<中文文件名>_预览.png` (300 dpi, rendered from the PDF).

## Self-check before styling

1. Can the core message be read from the chart alone in under 10 seconds?
2. Is there exactly one visual encoding carrying the message (position, length,
   color, or shape — not several competing)?
3. Would removing any element lose information? If not, remove it.
