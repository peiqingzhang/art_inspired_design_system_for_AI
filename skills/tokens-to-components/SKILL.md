---
name: tokens-to-components
description: Generate a full design component library from DTCG design tokens. Use this skill when the user has design tokens (from the painting-to-m3 or painting-to-theme skills, from Tokens Studio, from any DTCG JSON file, or from a CSS variables file) and wants to generate UI components, a component library, or a design system implementation from them. Triggers on phrases like "build components from these tokens", "create a UI kit from my tokens", "generate a component library", "turn these tokens into components", "make a design system from these colors", "apply these tokens to Material components", "create components from my design tokens". Also triggers when the user has already generated tokens and wants the next step — turning abstract tokens into usable UI building blocks. Outputs React components styled entirely by the token system.
---

# Tokens to Components

Generate a complete, production-ready component library from DTCG design tokens. The output is a set of React components styled entirely by the token system.

## Why this matters

Design tokens alone don't ship products — components do. This skill bridges the gap between a token JSON file and actual usable UI. Every color, font, radius, and spacing value in the output traces back to a named token, so changing a token cascades everywhere. No magic numbers, no hardcoded hex values.

## Prerequisites

This skill expects design tokens in one of these formats:
1. **DTCG JSON** (`.tokens.json` files) — preferred, output by the `painting-to-m3` or `painting-to-theme` skills
2. **CSS custom properties** (`theme.css` file with `--color-*` variables)
3. **Raw JSON** with at minimum: primary/secondary/tertiary colors, font names, spacing scale

If the user doesn't have tokens yet, suggest the `painting-to-m3` skill (strict M3) or `painting-to-theme` skill (expressive/painting-faithful) first.

## Step 0: Check for Design Brief

Before parsing tokens, check if a `design-brief.md` file exists in the token directory or its sibling review directory:

```bash
ls <theme-dir>/tokens/design-brief.md   # before review files are moved
ls <theme-dir>/review/design-brief.md   # after review files are moved
```

If found, read it. Extract:
- **Theme name** — use in preview HTML title, README heading, and component output directory name
- **Mood** — reference in preview page subtitle and README description
- **Design intent** — use as the README's introductory sentence
- **Intended use case** — helps decide which component preset to recommend in Step 2

The design brief is the handoff contract from the `painting-to-m3` or `painting-to-theme` skill. It carries the reasoning behind the token choices that is not visible in raw JSON. Using it makes your component output more coherent with the design intent.

Also check for a **Painting Color Proportions** section in the brief. When proportions are present, the token system has already tinted surface/neutral palettes to match the dominant painting color's atmospheric presence. The preview HTML will automatically render a proportion bar showing the painting's color balance alongside the components, helping users see the visual connection between their source painting and the generated UI.

## Workflow Overview

```
Tokens → Parse → Generate Component CSS → Build React Components → Present to User
```

## Step 1: Parse the Tokens

Read the token files and resolve all aliases to concrete values. Build an internal lookup:

```
resolved = {
  "color.sys.light.primary": "#5c5ea1",
  "color.sys.light.on-primary": "#ffffff",
  ...
  "typography.sys.body-large.fontFamily": "Source Serif 4",
  "typography.sys.body-large.fontSize": "16px",
  ...
  "shape.corner.medium": "12px",
  "spacing.4": "16px",
  ...
}
```

Use the parsing script at `scripts/parse_tokens.py` to do this:

```bash
python scripts/parse_tokens.py --token-dir ./themes/{painting-name}/{variant}/tokens/ --output ./themes/{painting-name}/{variant}/tokens/resolved.json
```

Optionally, pass `--css` to also output CSS custom properties directly.

## Step 2: Ask the Human What They Need

Before generating 25 components the user doesn't need, ask:

1. **What kind of project?** This determines which components to prioritize.
   - Web app / dashboard → buttons, cards, inputs, tables, navigation, dialogs
   - Marketing site → hero sections, CTAs, testimonial cards, feature grids
   - Mobile-first → bottom sheets, FABs, compact cards, swipe actions
   
2. **Which component set?** Offer these presets:
   - **Core** (always recommended): Button, Card, Input, Chip, Badge, Avatar, Divider
   - **Navigation**: AppBar, Tabs, Sidebar, Breadcrumb, Bottom Navigation
   - **Data**: Table, List, DataCard, Stat
   - **Feedback**: Dialog, Snackbar, Tooltip, Progress, Skeleton
   - **Layout**: Container, Grid, Stack, Surface
   - **All** — generates everything

3. **TypeScript or JavaScript?**
   - **TypeScript** (default for new projects) — generates `.tsx` files with `Props` interfaces, typed sub-components, and `index.ts`
   - **JavaScript** — generates `.jsx` files with `index.js`

4. **Storybook?**
   - Yes — generates `[Component].stories.tsx` alongside each component, with named exports per variant
   - No (default) — skip story files

5. **Framework target?**
   - React + Tailwind (default — generates .tsx/.jsx with CSS variables mapped to tokens)
   - React + CSS Modules (generates component + .module.css)
   - Plain HTML + CSS (generates .html + .css)

## Step 3: Generate the Component Library

For each component, follow this pattern:

### Component Generation Rules

1. **Token-first styling**: Every visual property MUST reference a token. Never hardcode:
   - Colors → `var(--color-*)` from color tokens
   - Font → `var(--font-brand)` / `var(--font-plain)` from typography tokens
   - Radius → `var(--radius-*)` from shape tokens
   - Spacing → `var(--spacing-*)` from spacing tokens

2. **M3 component anatomy**: Follow Material Design 3 component specs:
   - Button: container + label + optional icon, uses primary/onPrimary roles
   - Card: surface container + content area, uses surface-container roles  
   - Input: container + label + supporting text, uses outline/surface-variant roles
   - etc.

3. **Variants per component**: Generate at minimum:
   - **Filled** variant (uses primary container color)
   - **Outlined** variant (uses outline color with transparent fill)
   - **Text/Tonal** variant (uses primary-container with on-primary-container text)

4. **State layers**: All interactive components include M3 state layers via `.m3-interactive` + `.state-layer` CSS classes defined in `theme.css`. Do not use `filter: brightness()` as a substitute. The state layer is a `<span className="state-layer" aria-hidden="true" />` inside a `position: relative` container:
   - Hover: 8% opacity
   - Focus-visible: 12% opacity
   - Pressed (active): 12% opacity
   - Disabled: no overlay (component uses 38% opacity on content instead)

5. **Accessibility**: All interactive components MUST meet WCAG 2.1 AA keyboard accessibility:
   - Focusable via Tab (`tabIndex={0}` on non-native-interactive elements)
   - Activatable via Enter/Space (`onKeyDown` handler)
   - Correct ARIA roles (`role="option"` for chips, `role="article"` for cards, etc.)
   - Proper label associations (`htmlFor`/`id` pairing for inputs)
   - `aria-invalid`, `aria-describedby` for form elements
   - `aria-label` on icon-only elements (badges, avatars)

### Component Templates

Read the component templates in `references/component-specs.md` for detailed specifications of each M3 component's anatomy, variants, and token mappings.

## Step 4: Generate the Output Files

### For React + Tailwind (default)

Run the script:

```bash
python scripts/generate_components.py \
  --resolved-tokens ./themes/{painting-name}/{variant}/tokens/resolved.json \
  --output-dir ./themes/{painting-name}/{variant}/components \
  --review-dir ./themes/{painting-name}/{variant}/review \
  --theme-name "Van Gogh — Green Wheat Fields" \
  --sets all \
  [--no-typescript]              # default is TypeScript on
  [--storybook]                  # off by default
```

**CLI parameters:**
- `--resolved-tokens` (required): Path to resolved.json from parse_tokens.py
- `--output-dir`: Component output directory (default: `./components`)
- `--review-dir`: Directory for preview.html and README.md (defaults to `--output-dir`)
- `--theme-name`: Theme name used in README and preview title
- `--sets`: Comma-separated set names (`core`, `navigation`, `data`, `feedback`, `layout`) or `all` (default: `core`)
- `--components`: Optional comma-separated individual component names, merged with `--sets`
- `--no-typescript`: Generate plain .jsx files instead of TypeScript
- `--storybook`: Generate .stories.tsx files for each component

The script automatically generates all output: component files, theme.css, index.ts, preview.html, and README.md. Review files (preview.html, README.md) go to `--review-dir` when specified.

If the script is unavailable, generate the preview HTML manually following the template in `references/preview-template.html`.

## Step 5: Present and Iterate

Show the user:
1. The preview HTML (render it or share the file)
2. A summary: "Generated X components with Y variants using your [theme name] tokens"
3. The component files ready for download, including `README.md`
4. If Storybook was generated, note which story files were created

Ask:
- Do the components feel right with these colors and typography?
- Any components you want to add or modify?
- Should I adjust any token mappings (e.g., make cards use a different surface level)?
- Do you want Storybook stories generated for any components?

## Reference Files

- `references/component-specs.md` — Detailed M3 component anatomy and token mappings
- `scripts/parse_tokens.py` — Token parser and alias resolver
- `references/preview-template.html` — Fallback template for preview.html if the script is unavailable
- `scripts/generate_components.py` — Component code generator (also generates preview.html and README.md)
