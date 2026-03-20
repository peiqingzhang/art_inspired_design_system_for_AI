# Design Brief -- cezanne-mont-sainte-victoire-theme

## Source Image Analysis
- Mood: structured, contemplative, proto-cubist warmth
- Dominant Color: #4A6A9A (primary role)
- Secondary Colors: #3A6A38, #C8923A
- Neutral: #7A7A60
- Error base: #b3261e

## Painting Color Proportions
Area coverage from the source painting (used to tint UI surfaces):
- primary: 25%
- secondary: 25%
- tertiary: 20%
- neutral: 15%

## Typography Direction
- Display Font: Bitter -- chosen to match the image mood
- Body Font: Nunito Sans -- complements the display face for readability

## Shape Direction
- Corner Style: rounded corners (medium radii) -- friendly, approachable

## Design Intent
Cool blue mountain and sky, lush green foliage, warm ochre and terracotta buildings

## Token Files Generated
- `color.tokens.json` -- reference tonal ramps + M3 semantic roles (light & dark)
- `typography.tokens.json` -- M3 type scale with selected font pairing
- `shape.tokens.json` -- corner radius tokens
- `spacing.tokens.json` -- 4px base unit spacing scale
- `manifest.json` -- token file manifest
- `theme.css` -- CSS custom properties for direct web use
- `tailwind.config.snippet.js` -- Tailwind theme extension
- `contrast-report.md` -- WCAG contrast validation for all semantic color pairs
