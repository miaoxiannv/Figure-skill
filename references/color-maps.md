# Scientific Color Maps

Treat color as a quantitative axis, not decoration. Preserve the structure of the data,
make the mapping interpretable, and keep it readable under common color-vision
deficiencies (CVD) and grayscale reproduction. For organizing palettes into a
figure-level scheme (主/辅/强调 roles, hue-wheel angles), see
`references/color-scheme-design.md`.

## Workflow

1. Inspect the data and the figure's single message before choosing colors.
2. Identify whether color is the primary quantitative channel or only reinforces
   position, length, height, or labels.
3. Classify the variable and select the matching map class.
4. Decide whether hue changes have a defensible semantic or perceptual purpose.
5. Choose a documented perceptually uniform palette.
6. Implement the scale, normalization, limits, and color bar together.
7. Validate under grayscale and CVD simulation against the final white background.
8. Report the exact palette and mapping decisions for reproducibility.

## Classify the data

| Class | Use when | Examples | Recommended maps |
|---|---|---|---|
| Sequential | Ordered values low → high | expression, density, correlation magnitude | viridis, cividis, magma, cmocean thermal, Crameri batik, ColorBrewer sequential |
| Diverging | A **meaningful center** separates two directions | z-score vs mean, log2 fold change, anomaly | RdBu_r, cmocean balance, Crameri vik/roma |
| Cyclic | Periodic values whose endpoints are equivalent | phase, angle, time of day | twilight, cmocean phase, Crameri romaO |
| Categorical | Unordered groups | clusters, genotypes, treatments | Okabe-Ito, ColorBrewer qualitative |

Rules:

- Use a diverging map **only** when a meaningful reference value separates two
  directions (zero, an anomaly, a target). Place the visual midpoint at that value.
  Do **not** pick diverging merely because data contain positive and negative values.
- Do not use a categorical palette for continuous measurements.
- For binned values, use a discrete form of the appropriate ordered map and keep bin
  boundaries explicit.

## Decide whether hue carries meaning

- When position, length, height, area, or text already carries the value, color is
  redundant reinforcement: prefer **one fixed hue with monotonic lightness/saturation**.
- Only when color is the primary quantitative channel (dense heatmap, scalar field,
  UMAP colored by expression) may a perceptually uniform sequential map vary in hue —
  provided lightness stays ordered and transitions create no false boundaries.
- Distinct categorical hues only for genuinely unordered identities.
- Opposing hues only for diverging data with a meaningful center.
- Cyclic hue progression only for periodic variables.
- Never map arbitrary low/medium/high bands to unrelated hues (e.g. blue-amber-green)
  unless those bands are documented, named operational states with thresholds.

## Hard prohibitions

- **No rainbow, jet, or turbo** for quantitative data — uneven lightness invents
  boundaries and hides variation.
- **No red-green encoding at similar lightness.** Never rely on hue alone for a
  critical distinction.
- No decorative gradients inside bars, areas, or other quantitative marks.
- Do not squeeze, stretch, splice, or reorder sections of a validated palette.
- Do not claim warm = heavy / red = heaviest / yellow = lightest; lightness,
  saturation, area, background, and task all interact.

## Trusted palette families (whitelist — no ad-hoc hexes)

Every color must come from one of these documented families, **by name**. Hand-picked
hex values outside these sets are forbidden.

- **Matplotlib perceptually uniform**: viridis, cividis, magma, inferno, plasma.
- **Fabio Crameri Scientific Colour Maps** (`cmcrameri`): sequential,
  diverging, cyclic, discrete, categorical, with versioned releases.
- **cmocean**: parameter-oriented sequential/diverging/cyclic maps.
- **ColorBrewer**: discrete sequential, diverging, qualitative.
- **Okabe-Ito**: color-universal-design categorical palette — the default for groups.
- **cnsplots journal palettes** (`cns.palettes(...)`): `'Nature'`, `'Cell'`,
  `'Science'`, `'Ecotyper1'`–`'Ecotyper6'` (cell-type/subtype categorical),
  `'Set1'/'Set2'/'Set3'/'Dark2'/'Paired'/'Tableau'` (qualitative), `'parula'`,
  `'BuRd_custom'`, `'WhYlOrRd_custom'`, `'OrBu_custom'`, `'YlGnBu_custom'`
  (ordered maps).

```python
import cnsplots as cns

cycle   = cns.palettes("Nature")     # categorical list for color_cycle=/palette=
div_map = cns.palettes("BuRd_custom")  # LinearSegmentedColormap for continuous
```

Two-group convention: control/vehicle = neutral gray `#B0B0B0`, one treatment =
Okabe-Ito blue `#0072B2`.

A reputable palette from the wrong class is still misleading — match class first.

## Implementation rules

- Keep palette sampling uniform; use nonlinear normalization only when justified,
  label it explicitly, and make the color bar use the same transform.
- Set limits from a defensible rule; disclose clipping, winsorization, log transforms,
  and asymmetric ranges.
- Every continuous or ordered color encoding needs a visible, labeled color bar
  unless values are directly labeled on the marks.
- Keep the same entity mapped to the same color across all figures in a manuscript;
  record palette name/version, normalization, limits, center, and missing-data color.
- Missing/out-of-domain values get a visually separate neutral treatment (e.g. light
  gray), never a palette color.

## Validate before delivery

- Convert to grayscale: ordering, extrema, and structure must remain legible.
- Simulate deuteranopia, protanopia, tritanopia when tools permit
  (Python: `colorspacious`).
- Equal data steps must not produce conspicuously unequal visual steps.
- Every hue transition must have a data-semantic or perceptual justification.
- The most visually salient point must correspond to a meaningful value, not an
  accidental bright band.
- Center, endpoints, limits, ticks, units, and missing-data color must be unambiguous.
- If only a raster image is available for an audit, label findings as visual
  heuristics — do not claim measured perceptual uniformity.

## Deliver

When creating a figure, state: map class, palette name, normalization, limits,
center (if diverging), missing-data treatment, and validation performed. When
auditing, distinguish definite defects from likely risks requiring source data, and
give concrete replacements with code-level changes.
