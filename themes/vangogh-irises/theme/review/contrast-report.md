# WCAG Contrast Report

| Pair | Light Ratio | Light AA | Light AAA | Dark Ratio | Dark AA | Dark AAA |
|------|-------------|----------|-----------|------------|---------|----------|
| primary / on-primary | 9.13:1 | PASS | PASS | 8.01:1 | PASS | PASS |
| primary-container / on-primary-container | 13.92:1 | PASS | PASS | 8.1:1 | PASS | PASS |
| secondary / on-secondary | 4.9:1 | PASS | FAIL | 7.57:1 | PASS | PASS |
| secondary-container / on-secondary-container | 13.9:1 | PASS | PASS | 5.89:1 | PASS | FAIL |
| tertiary / on-tertiary | 7.89:1 | PASS | PASS | 8.1:1 | PASS | PASS |
| tertiary-container / on-tertiary-container | 13.87:1 | PASS | PASS | 8.05:1 | PASS | PASS |
| error / on-error | 9.59:1 | PASS | PASS | 7.34:1 | PASS | PASS |
| error-container / on-error-container | 13.65:1 | PASS | PASS | 7.37:1 | PASS | PASS |
| surface / on-surface | 5.9:1 | PASS | FAIL | 12.41:1 | PASS | PASS |
| surface-variant / on-surface-variant | 3.49:1 | FAIL | FAIL | 2.82:1 | FAIL | FAIL |
| petal-highlight / on-petal-highlight | 8.42:1 | PASS | PASS | 7.95:1 | PASS | PASS |
| petal-highlight-container / on-petal-highlight-container | 13.92:1 | PASS | PASS | 7.64:1 | PASS | PASS |
| vase-ochre / on-vase-ochre | 5.96:1 | PASS | FAIL | 7.48:1 | PASS | PASS |
| vase-ochre-container / on-vase-ochre-container | 13.94:1 | PASS | PASS | 5.73:1 | PASS | FAIL |

## Legend
- AA: >= 4.5:1 (normal text) -- WCAG 2.1 AA required
- AAA: >= 7.0:1 -- WCAG 2.1 AAA enhanced

## Failures
The following pairs fail WCAG AA and should be adjusted:
- light/surface-variant/on-surface-variant (3.49:1)
- dark/surface-variant/on-surface-variant (2.82:1)
