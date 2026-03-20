# Design Brief -- wang-ximeng-rivers-mountains-theme

## Source Image Analysis
- Mood: majestic, classical Chinese landscape, serene grandeur, mineral brilliance
- Dominant Color: #3A8A7A (primary role)
- Secondary Colors: #B8A050, #8A6030
- Neutral: #5A6858
- Error base: #b3261e

## Painting Color Proportions
Area coverage from the source painting (used to tint UI surfaces):
- primary: 30%
- secondary: 30%
- tertiary: 12%
- neutral: 10%

## Extended Painting Colors

Colors beyond M3's 3 primary/secondary/tertiary slots, each with a full tonal ramp
and semantic roles (base, on-*, *-container, on-*-container).

| Token Name | Hex | UI Role |
|---|---|---|
| pale-jade | #90C8B0 | card highlights, success states |
| dark-umber | #4A3820 | footer backgrounds, grounding elements |
| mist-white | #B8B8A0 | card surfaces, overlays |

## Painting Color Usage Guide

When building components, use extended colors to evoke specific aspects of the painting:

- **Highlight moments** (badges, notifications, selected states): Use warm accent colors
  like pale-jade that correspond to the painting's bright pops
- **Depth and grounding** (footers, sidebars, dark sections): Use deep extended colors
  like dark-umber for areas that need visual weight
- **Thematic accents** (decorative elements, illustrations): Use mist-white
  for elements that should carry the painting's character
- **Standard actions** (buttons, links, FABs): Use M3 primary/secondary/tertiary
  for interactive elements that need to be clearly actionable

## Typography Direction
- Display Font: Noto Serif Display -- chosen to match the image mood
- Body Font: Noto Sans -- complements the display face for readability

## Shape Direction
- Corner Style: large flowing corners -- soft, expressive

## Design Intent
Captures the mineral blue-green brilliance of Wang Ximeng s panoramic landscape against aged silk gold

## Token Files Generated
- `color.tokens.json` -- reference tonal ramps + M3 semantic roles (light & dark)
- `typography.tokens.json` -- M3 type scale with selected font pairing
- `shape.tokens.json` -- corner radius tokens
- `spacing.tokens.json` -- 4px base unit spacing scale
- `manifest.json` -- token file manifest
- `theme.css` -- CSS custom properties for direct web use
- `tailwind.config.snippet.js` -- Tailwind theme extension
- `contrast-report.md` -- WCAG contrast validation for all semantic color pairs
