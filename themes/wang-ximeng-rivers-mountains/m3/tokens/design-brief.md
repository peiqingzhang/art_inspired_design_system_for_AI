# Design Brief — wang-ximeng-rivers-mountains-m3

## Source Image Analysis
- Primary: #3A8A7A
- Secondary: #B8A050
- Tertiary: #8A6030
- Neutral: #5A6858
- Error base: #b3261e

## Considered Colors (not assigned to M3 slots)

These painting colors were identified but did not receive a primary/secondary/tertiary role.
Use the `painting-to-theme` skill for a richer palette that includes these colors.

- pale-jade (#90C8B0) — 8% area — bright mountain crests
- coral-sun (#C06848) — 2% area — iconic red sun disc
- dark-umber (#4A3820) — 8% area — architecture and pathways
- mist-white (#D0D0B8) — 5% area — atmospheric haze

## Selection Rationale
3 maximally-distinct colors selected from the painting for strict M3 compliance.
Colors were chosen to maximize hue separation, visual significance, and temperature contrast.

## Typography Direction
- Display Font: Noto Serif Display — chosen to match the image mood
- Body Font: Noto Sans — complements the display face for readability

## Shape Direction
- Corner Style: large flowing corners — soft, expressive

## Design Intent
Strict Material Design 3 token set. Surfaces use standard near-white tones
derived from the primary hue at low saturation. Compatible with any M3-consuming
framework (MUI, Jetpack Compose, Flutter).

## Token Files Generated
- `color.tokens.json` — reference tonal ramps + M3 semantic roles (light & dark)
- `typography.tokens.json` — M3 type scale with selected font pairing
- `shape.tokens.json` — corner radius tokens
- `spacing.tokens.json` — 4px base unit spacing scale
- `manifest.json` — token file manifest
- `theme.css` — CSS custom properties for direct web use
- `tailwind.config.snippet.js` — Tailwind theme extension
- `contrast-report.md` — WCAG contrast validation for standard M3 color pairs
