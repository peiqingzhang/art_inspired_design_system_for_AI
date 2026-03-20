# WCAG Contrast Report

| Pair | Light Ratio | Light AA | Light AAA | Dark Ratio | Dark AA | Dark AAA |
|------|-------------|----------|-----------|------------|---------|----------|
| primary / on-primary | 4.45:1 | FAIL | FAIL | 7.03:1 | PASS | PASS |
| primary-container / on-primary-container | 13.97:1 | PASS | PASS | 4.75:1 | PASS | FAIL |
| secondary / on-secondary | 8.66:1 | PASS | PASS | 7.65:1 | PASS | PASS |
| secondary-container / on-secondary-container | 13.79:1 | PASS | PASS | 7.24:1 | PASS | PASS |
| tertiary / on-tertiary | 4.84:1 | PASS | FAIL | 7.15:1 | PASS | PASS |
| tertiary-container / on-tertiary-container | 13.97:1 | PASS | PASS | 4.86:1 | PASS | FAIL |
| error / on-error | 6.79:1 | PASS | FAIL | 7.39:1 | PASS | PASS |
| error-container / on-error-container | 13.91:1 | PASS | PASS | 5.69:1 | PASS | FAIL |
| surface / on-surface | 5.13:1 | PASS | FAIL | 11.68:1 | PASS | PASS |
| surface-variant / on-surface-variant | 4.75:1 | PASS | FAIL | 1.5:1 | FAIL | FAIL |
| counter-mahogany / on-counter-mahogany | 7.34:1 | PASS | PASS | 7.8:1 | PASS | PASS |
| counter-mahogany-container / on-counter-mahogany-container | 13.94:1 | PASS | PASS | 7.1:1 | PASS | PASS |
| neon-green / on-neon-green | 4.64:1 | PASS | FAIL | 7.06:1 | PASS | PASS |
| neon-green-container / on-neon-green-container | 13.86:1 | PASS | PASS | 4.86:1 | PASS | FAIL |

## Legend
- AA: >= 4.5:1 (normal text) -- WCAG 2.1 AA required
- AAA: >= 7.0:1 -- WCAG 2.1 AAA enhanced

## Failures
The following pairs fail WCAG AA and should be adjusted:
- light/primary/on-primary (4.45:1)
- dark/surface-variant/on-surface-variant (1.50:1)
