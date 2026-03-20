# Design Brief — matisse-red-studio-m3

## Source Image Analysis
- Primary: #a83020
- Secondary: #3a7a50
- Tertiary: #4a60a0
- Neutral: #7a5a4a
- Error base: #b3261e

## Considered Colors (not assigned to M3 slots)

These painting colors were identified but did not receive a primary/secondary/tertiary role.
Use the `painting-to-theme` skill for a richer palette that includes these colors.

- hot-pink (#d868a0) — 8% area — nude painting canvas
- ochre-gold (#c8a040) — 8% area — picture frames and furniture
- cream-white (#e8e0d0) — 4% area — plate and small details

## Selection Rationale
3 maximally-distinct colors selected from the painting for strict M3 compliance.
Colors were chosen to maximize hue separation, visual significance, and temperature contrast.

## Typography Direction
- Display Font: Libre Baskerville — chosen to match the image mood
- Body Font: Work Sans — complements the display face for readability

## Shape Direction
- Corner Style: angular corners (small radii) — structured, precise

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
