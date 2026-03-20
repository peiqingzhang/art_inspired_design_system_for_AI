# Design Brief -- hopper-nighthawks-theme

## Source Image Analysis
- Mood: urban, noir, late-night melancholy
- Dominant Color: #1A4A4A (primary role)
- Secondary Colors: #8A3020, #C8AA40
- Neutral: #5A5A50
- Error base: #b3261e

## Painting Color Proportions
Area coverage from the source painting (used to tint UI surfaces):
- primary: 35%
- neutral: 20%
- secondary: 15%
- tertiary: 15%

## Extended Painting Colors

Colors beyond M3's 3 primary/secondary/tertiary slots, each with a full tonal ramp
and semantic roles (base, on-*, *-container, on-*-container).

| Token Name | Hex | UI Role |
|---|---|---|
| counter-mahogany | #6A3828 | card accents, sidebar active, warm anchors |
| neon-green | #38A868 | badges, highlights, active states |

## Painting Color Usage Guide

When building components, use extended colors to evoke specific aspects of the painting:

- **Highlight moments** (badges, notifications, selected states): Use warm accent colors
  like neon-green that correspond to the painting's bright pops
- **Depth and grounding** (footers, sidebars, dark sections): Use deep extended colors
  like counter-mahogany for areas that need visual weight
- **Standard actions** (buttons, links, FABs): Use M3 primary/secondary/tertiary
  for interactive elements that need to be clearly actionable

## Typography Direction
- Display Font: DM Sans -- chosen to match the image mood
- Body Font: IBM Plex Sans -- complements the display face for readability

## Shape Direction
- Corner Style: angular corners (small radii) -- structured, precise

## Design Intent
Deep teal darkness, warm yellow interior glow, mahogany counter, and eerie green fluorescent edge

## Token Files Generated
- `color.tokens.json` -- reference tonal ramps + M3 semantic roles (light & dark)
- `typography.tokens.json` -- M3 type scale with selected font pairing
- `shape.tokens.json` -- corner radius tokens
- `spacing.tokens.json` -- 4px base unit spacing scale
- `manifest.json` -- token file manifest
- `theme.css` -- CSS custom properties for direct web use
- `tailwind.config.snippet.js` -- Tailwind theme extension
- `contrast-report.md` -- WCAG contrast validation for all semantic color pairs
