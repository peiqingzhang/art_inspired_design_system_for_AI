# WCAG Contrast Report

| Pair | Light Ratio | Light AA | Light AAA | Dark Ratio | Dark AA | Dark AAA |
|------|-------------|----------|-----------|------------|---------|----------|
| primary / on-primary | 7.22:1 | PASS | PASS | 7.97:1 | PASS | PASS |
| primary-container / on-primary-container | 13.94:1 | PASS | PASS | 7.38:1 | PASS | PASS |
| secondary / on-secondary | 4.86:1 | PASS | FAIL | 7.46:1 | PASS | PASS |
| secondary-container / on-secondary-container | 13.94:1 | PASS | PASS | 5.65:1 | PASS | FAIL |
| tertiary / on-tertiary | 5.68:1 | PASS | FAIL | 7.4:1 | PASS | PASS |
| tertiary-container / on-tertiary-container | 13.9:1 | PASS | PASS | 5.46:1 | PASS | FAIL |
| error / on-error | 9.58:1 | PASS | PASS | 7.34:1 | PASS | PASS |
| error-container / on-error-container | 13.65:1 | PASS | PASS | 7.37:1 | PASS | PASS |
| surface / on-surface | 7.34:1 | PASS | PASS | 12.08:1 | PASS | PASS |
| surface-variant / on-surface-variant | 3.97:1 | FAIL | FAIL | 2.65:1 | FAIL | FAIL |

## Legend
- AA: >= 4.5:1 (normal text) -- WCAG 2.1 AA required
- AAA: >= 7.0:1 -- WCAG 2.1 AAA enhanced

## Failures
The following pairs fail WCAG AA and should be adjusted:
- light/surface-variant/on-surface-variant (3.97:1)
- dark/surface-variant/on-surface-variant (2.65:1)
