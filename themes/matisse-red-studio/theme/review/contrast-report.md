# WCAG Contrast Report

| Pair | Light Ratio | Light AA | Light AAA | Dark Ratio | Dark AA | Dark AAA |
|------|-------------|----------|-----------|------------|---------|----------|
| primary / on-primary | 9.0:1 | PASS | PASS | 7.55:1 | PASS | PASS |
| primary-container / on-primary-container | 13.79:1 | PASS | PASS | 7.28:1 | PASS | PASS |
| secondary / on-secondary | 4.75:1 | PASS | FAIL | 7.19:1 | PASS | PASS |
| secondary-container / on-secondary-container | 13.89:1 | PASS | PASS | 5.15:1 | PASS | FAIL |
| tertiary / on-tertiary | 5.79:1 | PASS | FAIL | 7.44:1 | PASS | PASS |
| tertiary-container / on-tertiary-container | 14.03:1 | PASS | PASS | 5.65:1 | PASS | FAIL |
| error / on-error | 9.52:1 | PASS | PASS | 7.42:1 | PASS | PASS |
| error-container / on-error-container | 13.74:1 | PASS | PASS | 7.37:1 | PASS | PASS |
| surface / on-surface | 4.54:1 | PASS | FAIL | 13.03:1 | PASS | PASS |
| surface-variant / on-surface-variant | 1.29:1 | FAIL | FAIL | 1.99:1 | FAIL | FAIL |
| hot-pink / on-hot-pink | 8.92:1 | PASS | PASS | 7.58:1 | PASS | PASS |
| hot-pink-container / on-hot-pink-container | 13.72:1 | PASS | PASS | 7.51:1 | PASS | PASS |
| plate-blue / on-plate-blue | 7.98:1 | PASS | PASS | 8.02:1 | PASS | PASS |
| plate-blue-container / on-plate-blue-container | 13.94:1 | PASS | PASS | 7.75:1 | PASS | PASS |

## Legend
- AA: >= 4.5:1 (normal text) -- WCAG 2.1 AA required
- AAA: >= 7.0:1 -- WCAG 2.1 AAA enhanced

## Failures
The following pairs fail WCAG AA and should be adjusted:
- light/surface-variant/on-surface-variant (1.29:1)
- dark/surface-variant/on-surface-variant (1.99:1)
