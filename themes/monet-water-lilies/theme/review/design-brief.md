# Design Brief -- monet-water-lilies-theme

## Source Image Analysis
- Mood: serene, ethereal, impressionist reverie
- Dominant Color: #5A6A9A (primary role)
- Secondary Colors: #5A7A5A, #8A70A0
- Neutral: #7A7A7A
- Error base: #b3261e

## Painting Color Proportions
Area coverage from the source painting (used to tint UI surfaces):
- primary: 30%
- secondary: 20%
- tertiary: 15%
- neutral: 15%

## Extended Painting Colors

Colors beyond M3's 3 primary/secondary/tertiary slots, each with a full tonal ramp
and semantic roles (base, on-*, *-container, on-*-container).

| Token Name | Hex | UI Role |
|---|---|---|
| lily-peach | #D0A880 | badges, warm accents, highlights |
| cloud-cream | #E8DCC8 | card surfaces, hero backgrounds |

## Painting Color Usage Guide

When building components, use extended colors to evoke specific aspects of the painting:

- **Highlight moments** (badges, notifications, selected states): Use warm accent colors
  like lily-peach that correspond to the painting's bright pops
- **Surface warmth** (card backgrounds, hero sections): Use light extended colors
  like cloud-cream-container for surfaces that should feel warm/inviting
- **Standard actions** (buttons, links, FABs): Use M3 primary/secondary/tertiary
  for interactive elements that need to be clearly actionable

## Typography Direction
- Display Font: Lora -- chosen to match the image mood
- Body Font: Source Serif 4 -- complements the display face for readability

## Shape Direction
- Corner Style: large flowing corners -- soft, expressive

## Design Intent
Soft lavender-blue reflections, sage greens, peach-cream highlights, and deep indigo depths

## Token Files Generated
- `color.tokens.json` -- reference tonal ramps + M3 semantic roles (light & dark)
- `typography.tokens.json` -- M3 type scale with selected font pairing
- `shape.tokens.json` -- corner radius tokens
- `spacing.tokens.json` -- 4px base unit spacing scale
- `manifest.json` -- token file manifest
- `theme.css` -- CSS custom properties for direct web use
- `tailwind.config.snippet.js` -- Tailwind theme extension
- `contrast-report.md` -- WCAG contrast validation for all semantic color pairs
