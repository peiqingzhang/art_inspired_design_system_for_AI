# Design Brief -- vangogh-irises-theme

## Source Image Analysis
- Mood: vibrant, impasto, impressionist energy
- Dominant Color: #2B4A8C (primary role)
- Secondary Colors: #4C7F51, #9070B0
- Neutral: #7A7A5A
- Error base: #b3261e

## Painting Color Proportions
Area coverage from the source painting (used to tint UI surfaces):
- primary: 30%
- secondary: 25%
- neutral: 15%
- tertiary: 10%

## Extended Painting Colors

Colors beyond M3's 3 primary/secondary/tertiary slots, each with a full tonal ramp
and semantic roles (base, on-*, *-container, on-*-container).

| Token Name | Hex | UI Role |
|---|---|---|
| petal-highlight | #7A9DD4 | card accents, hero backgrounds |
| vase-ochre | #C4873A | badges, star ratings, warm highlights |

## Painting Color Usage Guide

When building components, use extended colors to evoke specific aspects of the painting:

- **Highlight moments** (badges, notifications, selected states): Use warm accent colors
  like petal-highlight, vase-ochre that correspond to the painting's bright pops
- **Standard actions** (buttons, links, FABs): Use M3 primary/secondary/tertiary
  for interactive elements that need to be clearly actionable

## Typography Direction
- Display Font: Archivo Black -- chosen to match the image mood
- Body Font: Work Sans -- complements the display face for readability

## Shape Direction
- Corner Style: large flowing corners -- soft, expressive

## Design Intent
Cobalt blues from iris petals, lush greens from stems, mauve purples from flower hearts, and a bold gold ground

## Token Files Generated
- `color.tokens.json` -- reference tonal ramps + M3 semantic roles (light & dark)
- `typography.tokens.json` -- M3 type scale with selected font pairing
- `shape.tokens.json` -- corner radius tokens
- `spacing.tokens.json` -- 4px base unit spacing scale
- `manifest.json` -- token file manifest
- `theme.css` -- CSS custom properties for direct web use
- `tailwind.config.snippet.js` -- Tailwind theme extension
- `contrast-report.md` -- WCAG contrast validation for all semantic color pairs
