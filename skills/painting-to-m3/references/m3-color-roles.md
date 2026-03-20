# Material Design 3 Color Roles Reference

## Token Architecture

M3 uses a 3-tier token system:

### Tier 1: Reference Tokens
Raw color values. Generated as tonal ramps from source colors.
Each source color produces a scale of 24 tones from 0 (black) to 100 (white).

### Tier 2: System Tokens  
Semantic roles that reference specific tones from Tier 1.
These are what components actually use.

### Tier 3: Component Tokens
Component-specific overrides (optional). Usually the system tokens are sufficient.

## Light Theme Tone Mappings

| Role                         | Source Palette    | Tone |
|------------------------------|-------------------|------|
| primary                      | primary           | 40   |
| onPrimary                    | primary           | 100  |
| primaryContainer             | primary           | 90   |
| onPrimaryContainer           | primary           | 10   |
| secondary                    | secondary         | 40   |
| onSecondary                  | secondary         | 100  |
| secondaryContainer           | secondary         | 90   |
| onSecondaryContainer         | secondary         | 10   |
| tertiary                     | tertiary          | 40   |
| onTertiary                   | tertiary          | 100  |
| tertiaryContainer            | tertiary          | 90   |
| onTertiaryContainer          | tertiary          | 10   |
| error                        | error             | 40   |
| onError                      | error             | 100  |
| errorContainer               | error             | 90   |
| onErrorContainer             | error             | 10   |
| surface                      | neutral           | 98   |
| onSurface                    | neutral           | 10   |
| surfaceVariant               | neutral-variant   | 90   |
| onSurfaceVariant             | neutral-variant   | 30   |
| surfaceContainerLowest       | neutral           | 100  |
| surfaceContainerLow          | neutral           | 96   |
| surfaceContainer             | neutral           | 94   |
| surfaceContainerHigh         | neutral           | 92   |
| surfaceContainerHighest      | neutral           | 90   |
| outline                      | neutral-variant   | 50   |
| outlineVariant               | neutral-variant   | 80   |
| inverseSurface               | neutral           | 20   |
| inverseOnSurface             | neutral           | 95   |
| inversePrimary               | primary           | 80   |
| scrim                        | neutral           | 0    |
| shadow                       | neutral           | 0    |

## Dark Theme Tone Mappings

| Role                         | Source Palette    | Tone |
|------------------------------|-------------------|------|
| primary                      | primary           | 80   |
| onPrimary                    | primary           | 20   |
| primaryContainer             | primary           | 30   |
| onPrimaryContainer           | primary           | 90   |
| secondary                    | secondary         | 80   |
| onSecondary                  | secondary         | 20   |
| secondaryContainer           | secondary         | 30   |
| onSecondaryContainer         | secondary         | 90   |
| tertiary                     | tertiary          | 80   |
| onTertiary                   | tertiary          | 20   |
| tertiaryContainer            | tertiary          | 30   |
| onTertiaryContainer          | tertiary          | 90   |
| error                        | error             | 80   |
| onError                      | error             | 20   |
| errorContainer               | error             | 30   |
| onErrorContainer             | error             | 90   |
| surface                      | neutral           | 6    |
| onSurface                    | neutral           | 90   |
| surfaceVariant               | neutral-variant   | 30   |
| onSurfaceVariant             | neutral-variant   | 80   |
| surfaceContainerLowest       | neutral           | 4    |
| surfaceContainerLow          | neutral           | 10   |
| surfaceContainer             | neutral           | 12   |
| surfaceContainerHigh         | neutral           | 17   |
| surfaceContainerHighest      | neutral           | 22   |
| outline                      | neutral-variant   | 60   |
| outlineVariant               | neutral-variant   | 30   |
| inverseSurface               | neutral           | 90   |
| inverseOnSurface             | neutral           | 20   |
| inversePrimary               | primary           | 40   |
| scrim                        | neutral           | 0    |
| shadow                       | neutral           | 0    |

## Generating Tonal Ramps (Approximation)

When the full HCT algorithm is not available, approximate tonal ramps from a source hex color:

1. Convert source hex to HSL
2. For each target tone T (0-100):
   - Lightness = T% (directly maps tone → lightness as a starting point)
   - Saturation: reduce by ~20% at extreme tones (0-10 and 90-100) to avoid neon artifacts
   - Hue: keep constant (or shift by ±2° toward neutral at extreme lightness)
3. Convert back to hex

For the neutral palette:
- Use the primary hue with saturation fixed at ~10% — standard M3 low saturation
- This produces clean, near-white surfaces with a subtle primary tint

For neutral-variant:
- Use the primary hue with saturation fixed at ~18% — slightly more chromatic
- Creates subtle outlines and dividers with a hint of the primary hue
