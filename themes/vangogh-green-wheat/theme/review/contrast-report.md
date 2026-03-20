# WCAG Contrast Report

| Pair | Light Ratio | Light AA | Light AAA | Dark Ratio | Dark AA | Dark AAA |
|------|-------------|----------|-----------|------------|---------|----------|
| primary / on-primary | 4.88:1 | PASS | FAIL | 7.57:1 | PASS | PASS |
| primary-container / on-primary-container | 13.9:1 | PASS | PASS | 5.88:1 | PASS | FAIL |
| secondary / on-secondary | 4.77:1 | PASS | FAIL | 7.54:1 | PASS | PASS |
| secondary-container / on-secondary-container | 13.9:1 | PASS | PASS | 5.78:1 | PASS | FAIL |
| tertiary / on-tertiary | 6.82:1 | PASS | FAIL | 7.99:1 | PASS | PASS |
| tertiary-container / on-tertiary-container | 13.94:1 | PASS | PASS | 7.44:1 | PASS | PASS |
| error / on-error | 7.66:1 | PASS | PASS | 7.51:1 | PASS | PASS |
| error-container / on-error-container | 13.92:1 | PASS | PASS | 6.25:1 | PASS | FAIL |
| surface / on-surface | 6.25:1 | PASS | FAIL | 12.87:1 | PASS | PASS |
| surface-variant / on-surface-variant | 4.0:1 | FAIL | FAIL | 2.29:1 | FAIL | FAIL |
| wheat-chartreuse / on-wheat-chartreuse | 4.2:1 | FAIL | FAIL | 6.98:1 | PASS | FAIL |
| wheat-chartreuse-container / on-wheat-chartreuse-container | 13.87:1 | PASS | PASS | 4.47:1 | FAIL | FAIL |

## Legend
- AA: >= 4.5:1 (normal text) -- WCAG 2.1 AA required
- AAA: >= 7.0:1 -- WCAG 2.1 AAA enhanced

## Failures
The following pairs fail WCAG AA and should be adjusted:
- light/surface-variant/on-surface-variant (4.00:1)
- dark/surface-variant/on-surface-variant (2.29:1)
- light/wheat-chartreuse/on-wheat-chartreuse (4.20:1)
- dark/wheat-chartreuse-container/on-wheat-chartreuse-container (4.47:1)
