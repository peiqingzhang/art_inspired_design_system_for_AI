# Design Brief -- vangogh-green-wheat-theme

## Source Image Analysis
- Mood: serene, pastoral, luminous impressionist
- Dominant Color: #4C7F55 (primary role)
- Secondary Colors: #4C7F72, #6A80A8
- Neutral: #7A8A70
- Error base: #b3261e

## Painting Color Proportions
Area coverage from the source painting (used to tint UI surfaces):
- primary: 35%
- secondary: 20%
- neutral: 15%
- tertiary: 10%

## Extended Painting Colors

Colors beyond M3's 3 primary/secondary/tertiary slots, each with a full tonal ramp
and semantic roles (base, on-*, *-container, on-*-container).

| Token Name | Hex | UI Role |
|---|---|---|
| wheat-chartreuse | #A0C040 | badges, highlights, star ratings |

## Painting Color Usage Guide

When building components, use extended colors to evoke specific aspects of the painting:

- **Highlight moments** (badges, notifications, selected states): Use warm accent colors
  like wheat-chartreuse that correspond to the painting's bright pops
- **Standard actions** (buttons, links, FABs): Use M3 primary/secondary/tertiary
  for interactive elements that need to be clearly actionable

## Typography Direction
- Display Font: Lora -- chosen to match the image mood
- Body Font: Source Sans 3 -- complements the display face for readability

## Shape Direction
- Corner Style: large flowing corners -- soft, expressive

## Design Intent
Vibrant chartreuse wheat, deep teal foliage, pale mint sky, and swirling lavender-grey clouds

## Token Files Generated
- `color.tokens.json` -- reference tonal ramps + M3 semantic roles (light & dark)
- `typography.tokens.json` -- M3 type scale with selected font pairing
- `shape.tokens.json` -- corner radius tokens
- `spacing.tokens.json` -- 4px base unit spacing scale
- `manifest.json` -- token file manifest
- `theme.css` -- CSS custom properties for direct web use
- `tailwind.config.snippet.js` -- Tailwind theme extension
- `contrast-report.md` -- WCAG contrast validation for all semantic color pairs
