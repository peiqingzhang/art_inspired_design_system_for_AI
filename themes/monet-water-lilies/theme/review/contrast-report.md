# WCAG Contrast Report

| Pair | Light Ratio | Light AA | Light AAA | Dark Ratio | Dark AA | Dark AAA |
|------|-------------|----------|-----------|------------|---------|----------|
| primary / on-primary | 7.22:1 | PASS | PASS | 8.05:1 | PASS | PASS |
| primary-container / on-primary-container | 13.94:1 | PASS | PASS | 7.72:1 | PASS | PASS |
| secondary / on-secondary | 5.15:1 | PASS | FAIL | 7.72:1 | PASS | PASS |
| secondary-container / on-secondary-container | 14.0:1 | PASS | PASS | 6.28:1 | PASS | FAIL |
| tertiary / on-tertiary | 6.92:1 | PASS | FAIL | 8.05:1 | PASS | PASS |
| tertiary-container / on-tertiary-container | 13.88:1 | PASS | PASS | 7.63:1 | PASS | PASS |
| error / on-error | 9.61:1 | PASS | PASS | 7.34:1 | PASS | PASS |
| error-container / on-error-container | 13.65:1 | PASS | PASS | 7.38:1 | PASS | PASS |
| surface / on-surface | 7.67:1 | PASS | PASS | 12.42:1 | PASS | PASS |
| surface-variant / on-surface-variant | 3.79:1 | FAIL | FAIL | 2.54:1 | FAIL | FAIL |
| lily-peach / on-lily-peach | 6.05:1 | PASS | FAIL | 7.62:1 | PASS | PASS |
| lily-peach-container / on-lily-peach-container | 13.94:1 | PASS | PASS | 6.15:1 | PASS | FAIL |
| cloud-cream / on-cloud-cream | 5.43:1 | PASS | FAIL | 7.54:1 | PASS | PASS |
| cloud-cream-container / on-cloud-cream-container | 13.93:1 | PASS | PASS | 5.82:1 | PASS | FAIL |

## Legend
- AA: >= 4.5:1 (normal text) -- WCAG 2.1 AA required
- AAA: >= 7.0:1 -- WCAG 2.1 AAA enhanced

## Failures
The following pairs fail WCAG AA and should be adjusted:
- light/surface-variant/on-surface-variant (3.79:1)
- dark/surface-variant/on-surface-variant (2.54:1)
