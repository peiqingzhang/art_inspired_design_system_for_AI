# Design Brief -- matisse-red-studio-theme

## Source Image Analysis
- Mood: bold, expressive, Fauvist energy
- Dominant Color: #A03020 (primary role)
- Secondary Colors: #2A6A3A, #C89040
- Neutral: #7A5A4A
- Error base: #b3261e

## Painting Color Proportions
Area coverage from the source painting (used to tint UI surfaces):
- primary: 55%
- neutral: 12%
- tertiary: 10%
- secondary: 8%

## Extended Painting Colors

Colors beyond M3's 3 primary/secondary/tertiary slots, each with a full tonal ramp
and semantic roles (base, on-*, *-container, on-*-container).

| Token Name | Hex | UI Role |
|---|---|---|
| hot-pink | #D868A0 | badges, highlights, accents |
| plate-blue | #4A6AAA | card accents, sidebar active, tags |

## Painting Color Usage Guide

When building components, use extended colors to evoke specific aspects of the painting:

- **Highlight moments** (badges, notifications, selected states): Use warm accent colors
  like hot-pink, plate-blue that correspond to the painting's bright pops
- **Standard actions** (buttons, links, FABs): Use M3 primary/secondary/tertiary
  for interactive elements that need to be clearly actionable

## Typography Direction
- Display Font: Space Grotesk -- chosen to match the image mood
- Body Font: DM Sans -- complements the display face for readability

## Shape Direction
- Corner Style: angular corners (small radii) -- structured, precise

## Design Intent
Overwhelming venetian red, punctuated by hot pink, emerald green, deep blue, and golden yellow accents

## Token Files Generated
- `color.tokens.json` -- reference tonal ramps + M3 semantic roles (light & dark)
- `typography.tokens.json` -- M3 type scale with selected font pairing
- `shape.tokens.json` -- corner radius tokens
- `spacing.tokens.json` -- 4px base unit spacing scale
- `manifest.json` -- token file manifest
- `theme.css` -- CSS custom properties for direct web use
- `tailwind.config.snippet.js` -- Tailwind theme extension
- `contrast-report.md` -- WCAG contrast validation for all semantic color pairs
