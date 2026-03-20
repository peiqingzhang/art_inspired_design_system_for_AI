# Design Brief -- hokusai-great-wave-theme

## Source Image Analysis
- Mood: dramatic, powerful, ukiyo-e precision
- Dominant Color: #1A3A6A (primary role)
- Secondary Colors: #3A6A8A, #C8B078
- Neutral: #6A6A6A
- Error base: #b3261e

## Painting Color Proportions
Area coverage from the source painting (used to tint UI surfaces):
- primary: 35%
- secondary: 20%
- tertiary: 15%
- neutral: 10%

## Extended Painting Colors

Colors beyond M3's 3 primary/secondary/tertiary slots, each with a full tonal ramp
and semantic roles (base, on-*, *-container, on-*-container).

| Token Name | Hex | UI Role |
|---|---|---|
| foam-white | #E8E8E0 | card surfaces, hero highlights |

## Painting Color Usage Guide

When building components, use extended colors to evoke specific aspects of the painting:

- **Surface warmth** (card backgrounds, hero sections): Use light extended colors
  like foam-white-container for surfaces that should feel warm/inviting
- **Standard actions** (buttons, links, FABs): Use M3 primary/secondary/tertiary
  for interactive elements that need to be clearly actionable

## Typography Direction
- Display Font: Noto Serif JP -- chosen to match the image mood
- Body Font: Inter -- complements the display face for readability

## Shape Direction
- Corner Style: angular corners (small radii) -- structured, precise

## Design Intent
Deep indigo power, foaming white crests, warm tan sky, and teal depth

## Token Files Generated
- `color.tokens.json` -- reference tonal ramps + M3 semantic roles (light & dark)
- `typography.tokens.json` -- M3 type scale with selected font pairing
- `shape.tokens.json` -- corner radius tokens
- `spacing.tokens.json` -- 4px base unit spacing scale
- `manifest.json` -- token file manifest
- `theme.css` -- CSS custom properties for direct web use
- `tailwind.config.snippet.js` -- Tailwind theme extension
- `contrast-report.md` -- WCAG contrast validation for all semantic color pairs
