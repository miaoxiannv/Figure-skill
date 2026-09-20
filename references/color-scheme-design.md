# Color Scheme Design — 色相环角色框架

How to ORGANIZE the allowed palettes into a figure-level scheme. This sits on top
of `references/color-maps.md` (which governs which palettes are permitted); this
file governs the roles, the hue-wheel geometry, and the gradient rules. Distilled
from a community color-wheel tutorial (角度公式 + 主/辅/强调 role framework), then
tied to this skill's whitelist.

## The three colour attributes

Hue (色相), saturation (饱和度), lightness (明度). **Lightness variation inside one
hue is the safest hierarchy device** — it cannot clash, and it survives grayscale.

## The three roles (per figure)

| Role | Area | Job | Examples in this skill |
|---|---|---|---|
| 主色 primary | largest coloured area | carries the data encoding | diverging RdBu fills/strip; Okabe-Ito categorical points |
| 辅色 auxiliary | structure ink | axes, thresholds, background | neutral greys `0.45`/`0.55`, white |
| 强调色 accent | small, must jump | the one element that must be found first | GSEA ES curve; peak marker; callout stems |

## Hue-wheel angle formulas

| Scheme | Angle on the wheel | Use for |
|---|---|---|
| 单色 monochrome | 0° — same hue, lightness ramp | single elements; large fills; hierarchy inside one element |
| 类似色 analogous | ~30° | related series that must feel grouped |
| 互补 complementary | ~180° | diverging data — two directions of one quantity |
| 三色 triadic | 120° apart | one element that must jump clear of a two-hue figure |
| 四色 / 五色 | 90° / 72° | multi-class composition — hues **evenly spread** |

## The rules (each traced to a real failure)

1. **One element = one hue, lightness ramp only.** Never let a gradient
   interpolate linearly in RGB between two distant hues — it crosses unrelated
   hues and reads muddy. (Failure: an ES curve gradiented blue→vermillion and
   passed through grey-purple; fixed as a vermillion lightness ramp
   `#7A2A00 → #D55E00 → #F0A57C`.)
2. **Diverging data = a complementary pair.** This skill's pair is Okabe-Ito
   blue `#0072B2` (205°) ↔ vermillion `#D55E00` (28°) — 177° apart, textbook
   complementary. The pure ColorBrewer **RdBu 11-class** ramp
   (`#053061 ↔ #67001F`) is the large-area version for heatmaps and ranked fills.
3. **Large area tolerates low saturation; small area takes full saturation.**
   Accent elements are small, so they can run at full strength; big fills stay
   mid-saturation with clearly stated limits.
4. **Accent hue must not duplicate a data hue at large area** — an accent that
   reuses the data's own colours stops being an accent.
5. **Multi-class categorical sets: hues evenly spaced on the wheel**; beyond
   ~6 classes, split the figure instead of stretching the wheel.

## Worked example — the GSEA running-enrichment figure

- 主色: RdBu 11-class ramp for the strip + ranked fill (limits = the rank window)
- 辅色: grey dashed zero line, grey axes, grey non-leading hit ticks
- 强调色: the ES curve as a vermillion lightness ramp + peak dot
- Scheme: complementary for the data, monochrome for the accent element —
  no hue competes, nothing reads muddy
