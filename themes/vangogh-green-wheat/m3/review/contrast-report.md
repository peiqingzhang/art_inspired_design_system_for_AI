# WCAG Contrast Report

| Pair | Light Ratio | Light AA | Light AAA | Dark Ratio | Dark AA | Dark AAA |
|------|-------------|----------|-----------|------------|---------|----------|
| primary / on-primary | 4.7:1 | pass | --- | 7.19:1 | pass | pass |
| primary-container / on-primary-container | 13.89:1 | pass | pass | 5.06:1 | pass | --- |
| secondary / on-secondary | 6.23:1 | pass | --- | 7.86:1 | pass | pass |
| secondary-container / on-secondary-container | 13.95:1 | pass | pass | 6.84:1 | pass | --- |
| tertiary / on-tertiary | 4.09:1 | FAIL | --- | 7.13:1 | pass | pass |
| tertiary-container / on-tertiary-container | 13.94:1 | pass | pass | 4.74:1 | pass | --- |
| error / on-error | 8.03:1 | pass | pass | 7.53:1 | pass | pass |
| error-container / on-error-container | 13.82:1 | pass | pass | 6.46:1 | pass | --- |
| surface / on-surface | 16.53:1 | pass | pass | 15.39:1 | pass | pass |
| surface-variant / on-surface-variant | 6.16:1 | pass | --- | 4.94:1 | pass | --- |

## Legend
- AA: >= 4.5:1 (normal text) — WCAG 2.1 AA required
- AAA: >= 7.0:1 — WCAG 2.1 AAA enhanced

## Failures
The following pairs fail WCAG AA and should be adjusted:
- light/tertiary/on-tertiary (4.09:1)
