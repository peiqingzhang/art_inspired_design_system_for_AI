# Design Brief — hopper-nighthawks-m3

## Source Image Analysis
- Primary: #2a6b5e
- Secondary: #c8a040
- Tertiary: #a04030
- Neutral: #4a5a58
- Error base: #b3261e

## Considered Colors (not assigned to M3 slots)

These painting colors were identified but did not receive a primary/secondary/tertiary role.
Use the `painting-to-theme` skill for a richer palette that includes these colors.

- mahogany-counter (#5a2a1a) — 10% area — bar counter and furniture
- neon-reflection (#2a8a5a) — 3% area — green neon reflections
- cream-interior (#e8d8b0) — 8% area — warm interior wall glow

## Selection Rationale
3 maximally-distinct colors selected from the painting for strict M3 compliance.
Colors were chosen to maximize hue separation, visual significance, and temperature contrast.

## Typography Direction
- Display Font: DM Serif Display — chosen to match the image mood
- Body Font: Inter — complements the display face for readability

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
