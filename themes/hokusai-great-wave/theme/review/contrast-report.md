# WCAG Contrast Report

| Pair | Light Ratio | Light AA | Light AAA | Dark Ratio | Dark AA | Dark AAA |
|------|-------------|----------|-----------|------------|---------|----------|
| primary / on-primary | 8.92:1 | PASS | PASS | 7.92:1 | PASS | PASS |
| primary-container / on-primary-container | 13.9:1 | PASS | PASS | 7.59:1 | PASS | PASS |
| secondary / on-secondary | 6.39:1 | PASS | FAIL | 7.75:1 | PASS | PASS |
| secondary-container / on-secondary-container | 13.92:1 | PASS | PASS | 6.57:1 | PASS | FAIL |
| tertiary / on-tertiary | 5.12:1 | PASS | FAIL | 7.45:1 | PASS | PASS |
| tertiary-container / on-tertiary-container | 13.93:1 | PASS | PASS | 5.54:1 | PASS | FAIL |
| error / on-error | 9.58:1 | PASS | PASS | 7.34:1 | PASS | PASS |
| error-container / on-error-container | 13.65:1 | PASS | PASS | 7.37:1 | PASS | PASS |
| surface / on-surface | 7.32:1 | PASS | PASS | 11.92:1 | PASS | PASS |
| surface-variant / on-surface-variant | 3.8:1 | FAIL | FAIL | 2.57:1 | FAIL | FAIL |
| foam-white / on-foam-white | 4.73:1 | PASS | FAIL | 7.63:1 | PASS | PASS |
| foam-white-container / on-foam-white-container | 14.04:1 | PASS | PASS | 6.0:1 | PASS | FAIL |

## Legend
- AA: >= 4.5:1 (normal text) -- WCAG 2.1 AA required
- AAA: >= 7.0:1 -- WCAG 2.1 AAA enhanced

## Failures
The following pairs fail WCAG AA and should be adjusted:
- light/surface-variant/on-surface-variant (3.80:1)
- dark/surface-variant/on-surface-variant (2.57:1)
