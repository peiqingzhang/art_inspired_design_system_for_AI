# WCAG Contrast Report

| Pair | Light Ratio | Light AA | Light AAA | Dark Ratio | Dark AA | Dark AAA |
|------|-------------|----------|-----------|------------|---------|----------|
| primary / on-primary | 9.11:1 | pass | pass | 8.12:1 | pass | pass |
| primary-container / on-primary-container | 13.84:1 | pass | pass | 8.46:1 | pass | pass |
| secondary / on-secondary | 4.83:1 | pass | --- | 6.92:1 | pass | --- |
| secondary-container / on-secondary-container | 13.92:1 | pass | pass | 4.41:1 | FAIL | --- |
| tertiary / on-tertiary | 4.83:1 | pass | --- | 7.46:1 | pass | pass |
| tertiary-container / on-tertiary-container | 13.86:1 | pass | pass | 5.62:1 | pass | --- |
| error / on-error | 9.62:1 | pass | pass | 7.34:1 | pass | pass |
| error-container / on-error-container | 13.64:1 | pass | pass | 7.39:1 | pass | pass |
| surface / on-surface | 17.01:1 | pass | pass | 15.07:1 | pass | pass |
| surface-variant / on-surface-variant | 7.53:1 | pass | pass | 5.68:1 | pass | --- |

## Legend
- AA: >= 4.5:1 (normal text) — WCAG 2.1 AA required
- AAA: >= 7.0:1 — WCAG 2.1 AAA enhanced

## Failures
The following pairs fail WCAG AA and should be adjusted:
- dark/secondary-container/on-secondary-container (4.41:1)
