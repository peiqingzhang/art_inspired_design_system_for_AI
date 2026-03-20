# Design Brief — vangogh-green-wheat-m3

## Source Image Analysis
- Primary: #499239
- Secondary: #6a8fae
- Tertiary: #8d8d3e
- Neutral: #6A7A60
- Error base: #B3261E

## Considered Colors (not assigned to M3 slots)

These painting colors were identified but did not receive a primary/secondary/tertiary role.
Use the `painting-to-theme` skill for a richer palette that includes these colors.

- dark-teal (#2A6A5A) — 15% area — deep foreground brushstrokes
- cream (#E8E0C8) — 10% area — cloud highlights
- lavender (#8080A8) — 5% area — cloud edges

## Selection Rationale
3 maximally-distinct colors selected from the painting for strict M3 compliance.
Colors were chosen to maximize hue separation, visual significance, and temperature contrast.

## Typography Direction
- Display Font: Playfair Display — chosen to match the image mood
- Body Font: Source Serif 4 — complements the display face for readability

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
