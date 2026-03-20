# M3 Component Specifications

Token mappings for each Material Design 3 component. All values reference system tokens, never raw values.

## Button

### Anatomy
- Container (background)
- Label text
- Optional: leading icon, trailing icon

### Variants & Token Mappings

**Filled Button**
| Property          | Token                              |
|-------------------|------------------------------------|
| container         | color.sys.{theme}.primary          |
| label             | color.sys.{theme}.on-primary       |
| container:hover   | primary + 8% state layer           |
| container:focus   | primary + 12% state layer          |
| container:disabled| color.sys.{theme}.on-surface @ 12% |
| label:disabled    | color.sys.{theme}.on-surface @ 38% |
| corner            | shape.corner.full                  |
| height            | 40px                               |
| padding-h         | spacing.6 (24px)                   |
| label-font        | typography.sys.label-large         |

**Outlined Button**
| Property          | Token                              |
|-------------------|------------------------------------|
| container         | transparent                        |
| border            | color.sys.{theme}.outline, 1px     |
| label             | color.sys.{theme}.primary          |
| corner            | shape.corner.full                  |
| height            | 40px                               |
| padding-h         | spacing.6 (24px)                   |
| label-font        | typography.sys.label-large         |

**Tonal Button**
| Property          | Token                                    |
|-------------------|------------------------------------------|
| container         | color.sys.{theme}.secondary-container    |
| label             | color.sys.{theme}.on-secondary-container |
| corner            | shape.corner.full                        |
| height            | 40px                                     |
| padding-h         | spacing.6 (24px)                         |
| label-font        | typography.sys.label-large               |

**Text Button**
| Property          | Token                              |
|-------------------|------------------------------------|
| container         | transparent                        |
| label             | color.sys.{theme}.primary          |
| height            | 40px                               |
| padding-h         | spacing.3 (12px)                   |
| label-font        | typography.sys.label-large         |

---

## Card

### Anatomy
- Container (surface)
- Optional: media area, header, body, actions

### Variants

**Elevated Card**
| Property          | Token                                       |
|-------------------|---------------------------------------------|
| container         | color.sys.{theme}.surface-container-low     |
| shadow            | 0 1px 2px color.sys.{theme}.shadow @ 30%   |
| corner            | shape.corner.medium                         |
| padding           | spacing.4 (16px)                            |
| title-font        | typography.sys.title-large                  |
| body-font         | typography.sys.body-medium                  |

**Filled Card**
| Property          | Token                                       |
|-------------------|---------------------------------------------|
| container         | color.sys.{theme}.surface-container-highest |
| corner            | shape.corner.medium                         |
| padding           | spacing.4 (16px)                            |

**Outlined Card**
| Property          | Token                              |
|-------------------|------------------------------------|
| container         | color.sys.{theme}.surface          |
| border            | color.sys.{theme}.outline-variant  |
| corner            | shape.corner.medium                |
| padding           | spacing.4 (16px)                   |

---

## Text Input / Text Field

### Anatomy
- Container
- Label text (floating)
- Input text
- Supporting text (below)
- Optional: leading icon, trailing icon

### Variants

**Filled Input**
| Property          | Token                                       |
|-------------------|---------------------------------------------|
| container         | color.sys.{theme}.surface-container-highest |
| label (resting)   | color.sys.{theme}.on-surface-variant        |
| label (focused)   | color.sys.{theme}.primary                   |
| input-text        | color.sys.{theme}.on-surface                |
| active-indicator  | color.sys.{theme}.primary, 2px bottom       |
| corner            | shape.corner.extra-small (top only)         |
| height            | 56px                                        |
| padding-h         | spacing.4 (16px)                            |
| input-font        | typography.sys.body-large                   |
| label-font        | typography.sys.body-small (when floating)   |

**Outlined Input**
| Property          | Token                              |
|-------------------|------------------------------------|
| container         | transparent                        |
| border            | color.sys.{theme}.outline, 1px     |
| border:focused    | color.sys.{theme}.primary, 2px     |
| label             | color.sys.{theme}.on-surface-variant |
| input-text        | color.sys.{theme}.on-surface       |
| corner            | shape.corner.extra-small           |
| height            | 56px                               |
| padding-h         | spacing.4 (16px)                   |

---

## Chip

### Anatomy
- Container
- Label text
- Optional: leading icon, trailing icon (close)

### Variants

**Assist Chip**
| Property          | Token                              |
|-------------------|------------------------------------|
| container         | transparent                        |
| border            | color.sys.{theme}.outline, 1px     |
| label             | color.sys.{theme}.on-surface       |
| corner            | shape.corner.small                 |
| height            | 32px                               |
| padding-h         | spacing.4 (16px)                   |
| label-font        | typography.sys.label-large         |

**Filter Chip (selected)**
| Property          | Token                                    |
|-------------------|------------------------------------------|
| container         | color.sys.{theme}.secondary-container    |
| label             | color.sys.{theme}.on-secondary-container |
| corner            | shape.corner.small                       |
| height            | 32px                                     |

---

## Badge

| Property          | Token                              |
|-------------------|------------------------------------|
| container         | color.sys.{theme}.error            |
| label             | color.sys.{theme}.on-error         |
| corner            | shape.corner.full                  |
| min-width         | 16px (small), 24px (with number)   |
| label-font        | typography.sys.label-small         |

---

## Avatar

| Property          | Token                                    |
|-------------------|------------------------------------------|
| container         | color.sys.{theme}.primary-container      |
| text              | color.sys.{theme}.on-primary-container   |
| corner            | shape.corner.full                        |
| size              | 40px (default), 24px (small), 56px (large) |
| text-font         | typography.sys.title-medium              |

---

## Divider

| Property          | Token                              |
|-------------------|------------------------------------|
| color             | color.sys.{theme}.outline-variant  |
| thickness         | 1px                                |
| inset-start       | spacing.4 (16px), optional         |

---

## App Bar (Top)

| Property          | Token                                       |
|-------------------|---------------------------------------------|
| container         | color.sys.{theme}.surface                   |
| on-scroll         | color.sys.{theme}.surface-container         |
| title             | color.sys.{theme}.on-surface                |
| icons             | color.sys.{theme}.on-surface-variant        |
| height            | 64px                                        |
| title-font        | typography.sys.title-large                  |
| padding-h         | spacing.4 (16px)                            |

---

## Navigation Tabs

| Property          | Token                                       |
|-------------------|---------------------------------------------|
| container         | color.sys.{theme}.surface-container         |
| active-indicator  | color.sys.{theme}.secondary-container       |
| active-label      | color.sys.{theme}.on-surface                |
| inactive-label    | color.sys.{theme}.on-surface-variant        |
| active-icon       | color.sys.{theme}.on-secondary-container    |
| height            | 48px (primary), 64px (with icon+label)      |
| label-font        | typography.sys.label-large                  |

---

## Dialog

| Property          | Token                                       |
|-------------------|---------------------------------------------|
| container         | color.sys.{theme}.surface-container-high    |
| headline          | color.sys.{theme}.on-surface                |
| body              | color.sys.{theme}.on-surface-variant        |
| corner            | shape.corner.extra-large                    |
| padding           | spacing.6 (24px)                            |
| headline-font     | typography.sys.headline-small               |
| body-font         | typography.sys.body-medium                  |
| scrim             | color.sys.{theme}.scrim @ 32%               |

---

## Snackbar

| Property          | Token                              |
|-------------------|------------------------------------|
| container         | color.sys.{theme}.inverse-surface  |
| text              | color.sys.{theme}.inverse-on-surface |
| action            | color.sys.{theme}.inverse-primary  |
| corner            | shape.corner.extra-small           |
| padding           | spacing.4 (16px)                   |
| text-font         | typography.sys.body-medium         |

---

## Surface / Container (Layout)

| Property          | Token                                       |
|-------------------|---------------------------------------------|
| background-0      | color.sys.{theme}.surface                   |
| background-1      | color.sys.{theme}.surface-container-lowest  |
| background-2      | color.sys.{theme}.surface-container-low     |
| background-3      | color.sys.{theme}.surface-container         |
| background-4      | color.sys.{theme}.surface-container-high    |
| background-5      | color.sys.{theme}.surface-container-highest |
| text              | color.sys.{theme}.on-surface                |
| text-variant      | color.sys.{theme}.on-surface-variant        |

---

---

## Navigation Components

---

## Sidebar

A vertical navigation panel with a list of labeled, optionally iconic items. One item can be marked active.

### Anatomy
- Nav container (fixed width)
- Optional: header slot
- List of items (button elements with optional icon + label)
- State layer on each item

### Variants

**Default Sidebar**
| Property              | Token                                          |
|-----------------------|------------------------------------------------|
| container             | color.sys.{theme}.surface-container            |
| container-padding     | spacing.3 (12px)                               |
| item-gap              | spacing.1 (4px)                                |
| item-height           | 56px                                           |
| item-corner           | shape.corner.full                              |
| item-padding          | 0 spacing.6 (24px) 0 spacing.4 (16px)         |
| item-icon-gap         | spacing.3 (12px)                               |
| active-bg             | color.sys.{theme}.secondary-container          |
| active-text           | color.sys.{theme}.on-secondary-container       |
| inactive-text         | color.sys.{theme}.on-surface-variant           |
| active-font-weight    | 700                                            |
| inactive-font-weight  | 500                                            |
| label-font            | typography.sys.label-large (14px)              |
| icon-size             | 24px                                           |
| header-padding        | spacing.4 (16px)                               |
| header-margin-bottom  | spacing.2 (8px)                                |
| width                 | 280px                                          |
| font-family           | var(--font-plain)                              |

### States
- Hover/focus via `.m3-interactive` state layer (see State Layer Opacity Model)
- Active item: uses `secondary-container` background

### Accessibility
- `role="navigation"` on the `<nav>` container
- Each item is a `<button>` for keyboard access

---

## Breadcrumb

A horizontal trail of links showing the user's location in a hierarchy. The last item is the current page.

### Anatomy
- Nav container with `aria-label="Breadcrumb"`
- Ordered list (`<ol>`) of items
- Each item: link (`<a>`) or current-page span, with separator between items

### Variants

**Default Breadcrumb**
| Property          | Token                              |
|-------------------|------------------------------------|
| link-color        | color.sys.{theme}.primary          |
| link-font-weight  | 500                                |
| current-color     | color.sys.{theme}.on-surface       |
| current-weight    | 500                                |
| separator-color   | color.sys.{theme}.on-surface-variant |
| separator         | '/' (customizable via prop)        |
| item-gap          | spacing.2 (8px)                    |
| font-size         | 14px                               |
| line-height       | 20px                               |
| font-family       | var(--font-plain)                  |

### States
- Links have default browser hover/focus behavior
- No text-decoration on links

### Accessibility
- `<nav>` with `aria-label="Breadcrumb"`
- `aria-current="page"` on the last item (current page)
- Links are navigable via keyboard

---

## BottomNav

A horizontal bottom navigation bar for mobile-style navigation with icon and label per item.

### Anatomy
- Nav container (horizontal bar)
- Items (button elements) each containing:
  - Icon pill (with active indicator background)
  - Label text

### Variants

**Default BottomNav**
| Property              | Token                                          |
|-----------------------|------------------------------------------------|
| container             | color.sys.{theme}.surface-container            |
| container-height      | 80px                                           |
| border-top            | 1px solid color.sys.{theme}.outline-variant    |
| active-text           | color.sys.{theme}.on-surface                   |
| inactive-text         | color.sys.{theme}.on-surface-variant           |
| active-font-weight    | 700                                            |
| inactive-font-weight  | 500                                            |
| label-font-size       | 12px                                           |
| letter-spacing        | 0.5px                                          |
| icon-pill-width       | 64px                                           |
| icon-pill-height      | 32px                                           |
| icon-pill-corner      | shape.corner.full                              |
| icon-pill-active-bg   | color.sys.{theme}.secondary-container          |
| icon-pill-active-color| color.sys.{theme}.on-secondary-container       |
| icon-size             | 24px                                           |
| item-gap              | spacing.1 (4px)                                |
| font-family           | var(--font-plain)                              |

### States
- Hover/focus via `.m3-interactive` state layer
- Active item: icon pill gets `secondary-container` background, label turns bold
- Transition: all 0.2s ease on icon pill

### Accessibility
- `role="navigation"` on the `<nav>` container
- `aria-current="page"` on the active item
- Each item is a `<button>` for keyboard access

---

## Data Components

---

## Table

A data table with column headers and rows. Supports optional striped row styling and column alignment.

### Anatomy
- Scroll container (`<div>` with overflow)
- `<table>` element
- `<thead>` with header row
- `<tbody>` with data rows
- Cells: `<th>` for headers, `<td>` for data

### Variants

**Default Table**
| Property              | Token                                          |
|-----------------------|------------------------------------------------|
| container-border      | 1px solid color.sys.{theme}.outline-variant    |
| container-corner      | shape.corner.medium                            |
| header-bg             | color.sys.{theme}.surface-container            |
| header-color          | color.sys.{theme}.on-surface-variant           |
| header-font-size      | 12px                                           |
| header-font-weight    | 500                                            |
| header-letter-spacing | 0.5px                                          |
| header-padding        | spacing.3 spacing.4 (12px 16px)                |
| header-border-bottom  | 1px solid color.sys.{theme}.outline-variant    |
| row-bg                | color.sys.{theme}.surface                      |
| row-bg-striped        | color.sys.{theme}.surface-container-lowest     |
| row-border-bottom     | 1px solid color.sys.{theme}.outline-variant    |
| cell-padding          | spacing.3 spacing.4 (12px 16px)                |
| text-color            | color.sys.{theme}.on-surface                   |
| font-size             | 14px                                           |
| line-height           | 20px                                           |
| font-family           | var(--font-plain)                              |

### States
- `striped` prop alternates row backgrounds between `surface` and `surface-container-lowest`

### Accessibility
- Semantic `<table>`, `<thead>`, `<tbody>`, `<th>`, `<td>` elements
- Column `align` supported via `text-align` property
- Container provides horizontal scrolling for overflow

---

## List

A vertical list of items with primary text, optional secondary text, and optional leading/trailing elements. Items can be interactive.

### Anatomy
- `<ul>` container
- `<li>` items, each containing:
  - Optional: leading element (icon/avatar)
  - Content area (primary text + optional secondary text)
  - Optional: trailing element

### Variants

**Default List**
| Property              | Token                                          |
|-----------------------|------------------------------------------------|
| text-color            | color.sys.{theme}.on-surface                   |
| secondary-color       | color.sys.{theme}.on-surface-variant           |
| leading-color         | color.sys.{theme}.on-surface-variant           |
| trailing-color        | color.sys.{theme}.on-surface-variant           |
| item-padding          | spacing.2 spacing.4 (8px 16px)                 |
| item-gap              | spacing.4 (16px)                               |
| min-height (1-line)   | 56px                                           |
| min-height (2-line)   | 72px                                           |
| primary-font-size     | 16px                                           |
| primary-line-height   | 24px                                           |
| secondary-font-size   | 14px                                           |
| secondary-line-height | 20px                                           |
| leading-icon-size     | 24px                                           |
| font-family           | var(--font-plain)                              |

### States
- Interactive items (with `onClick`): hover/focus via `.m3-interactive` state layer
- Non-interactive items: no state layer, default cursor

### Accessibility
- `role="list"` on the `<ul>` container
- Interactive items: `role="button"`, `tabIndex={0}`
- Non-interactive items: `role="listitem"`
- Keyboard: Enter or Space triggers `onClick` on interactive items

---

## DataCard

A card displaying a key metric with title, large value, optional trend indicator, and optional icon.

### Anatomy
- Container (elevated card)
- Header row: title + optional icon
- Value (large display text)
- Footer row: optional trend indicator + optional subtitle

### Variants

**Default DataCard**
| Property              | Token                                          |
|-----------------------|------------------------------------------------|
| container-bg          | color.sys.{theme}.surface-container-low        |
| container-corner      | shape.corner.medium                            |
| container-padding     | spacing.4 (16px)                               |
| container-shadow      | 0 1px 3px rgba(0,0,0,0.12)                    |
| text-color            | color.sys.{theme}.on-surface                   |
| title-color           | color.sys.{theme}.on-surface-variant           |
| title-font-size       | 14px                                           |
| title-font-weight     | 500                                            |
| value-font-size       | 32px                                           |
| value-font-weight     | 700                                            |
| value-font-family     | var(--font-brand)                              |
| value-line-height     | 40px                                           |
| icon-color            | color.sys.{theme}.primary                      |
| icon-size             | 24px                                           |
| trend-up-color        | color.sys.{theme}.tertiary                     |
| trend-down-color      | color.sys.{theme}.error                        |
| trend-neutral-color   | color.sys.{theme}.on-surface-variant           |
| trend-font-size       | 14px                                           |
| trend-font-weight     | 500                                            |
| subtitle-color        | color.sys.{theme}.on-surface-variant           |
| subtitle-font-size    | 14px                                           |
| header-margin-bottom  | spacing.3 (12px)                               |
| footer-gap            | spacing.2 (8px)                                |
| footer-margin-top     | spacing.1 (4px)                                |
| font-family           | var(--font-plain)                              |

### States
- Static component (no interactive states)

### Accessibility
- `role="article"` on the container

---

## Stat

A minimal centered stat display with label, large value, and optional description.

### Anatomy
- Container (centered block)
- Label (small, uppercase-style)
- Value (large display text)
- Optional: description text

### Variants

**Default Stat**
| Property              | Token                                          |
|-----------------------|------------------------------------------------|
| text-color            | color.sys.{theme}.on-surface                   |
| label-color           | color.sys.{theme}.on-surface-variant           |
| label-font-size       | 12px                                           |
| label-font-weight     | 500                                            |
| label-letter-spacing  | 0.5px                                          |
| label-margin-bottom   | spacing.1 (4px)                                |
| value-font-size       | 45px                                           |
| value-font-weight     | 400                                            |
| value-font-family     | var(--font-brand)                              |
| value-line-height     | 52px                                           |
| description-color     | color.sys.{theme}.on-surface-variant           |
| description-font-size | 14px                                           |
| description-margin-top| spacing.1 (4px)                                |
| padding               | spacing.4 (16px)                               |
| text-align            | center                                         |
| font-family           | var(--font-plain)                              |

### States
- Static component (no interactive states)

### Accessibility
- Semantic structure with descriptive text; no special ARIA roles required

---

## Feedback Components

---

## Tooltip

A small popup label that appears on hover/focus to describe an element. Supports four positions.

### Anatomy
- Wrapper container (inline-flex, relative positioning)
- Trigger element (children)
- Tooltip popup (absolutely positioned)

### Variants

**Default Tooltip**
| Property          | Token                                   |
|-------------------|-----------------------------------------|
| container-bg      | color.sys.{theme}.inverse-surface       |
| text-color        | color.sys.{theme}.inverse-on-surface    |
| padding           | 4px spacing.2 (8px)                     |
| corner            | shape.corner.extra-small                |
| font-size         | 12px                                    |
| line-height       | 16px                                    |
| font-weight       | 500                                     |
| font-family       | var(--font-plain)                       |
| z-index           | 1000                                    |
| position-offset   | 8px from trigger                        |

### Positions
- `top` (default), `bottom`, `left`, `right`

### States
- Visible on hover (`mouseenter`) and focus
- Hidden on mouse leave and blur
- `pointerEvents: none` on tooltip to prevent interference

### Accessibility
- `role="tooltip"` on the popup element
- Triggered by both hover and focus for keyboard users

---

## Progress

A progress indicator showing completion status. Supports linear bar and circular (SVG) variants, with determinate and indeterminate modes.

### Anatomy

**Linear:** Track container + fill bar
**Circular:** SVG with background circle + progress arc

### Variants

**Linear Progress**
| Property          | Token                                          |
|-------------------|-------------------------------------------------|
| track-bg          | color.sys.{theme}.surface-container-highest     |
| fill-bg           | color.sys.{theme}.primary                       |
| height            | 4px                                              |
| corner            | shape.corner.full                                |

**Circular Progress**
| Property          | Token                                          |
|-------------------|-------------------------------------------------|
| track-stroke      | color.sys.{theme}.surface-container-highest     |
| fill-stroke       | color.sys.{theme}.primary                       |
| size              | 48px                                             |
| stroke-width      | 4px                                              |
| stroke-linecap    | round                                            |

### States
- Determinate: `value` prop controls fill width/arc (0-100)
- Indeterminate: animated (linear slides, circular spins at 1.4s)
- Transition: width/stroke 0.3s ease in determinate mode

### Accessibility
- `role="progressbar"` on the container
- `aria-valuenow` set to current value (omitted when indeterminate)
- `aria-valuemin={0}`, `aria-valuemax={100}`

---

## Skeleton

A placeholder loading indicator that pulses to indicate content is loading. Supports text, rectangular, and circular shapes.

### Anatomy
- One or more `<div>` elements styled as placeholders
- Pulse animation via CSS keyframes

### Variants

**Text Skeleton**
| Property          | Token                                          |
|-------------------|-------------------------------------------------|
| bg                | color.sys.{theme}.surface-container-highest     |
| height            | 16px (default)                                   |
| corner            | shape.corner.extra-small                         |
| gap (multi-line)  | spacing.2 (8px)                                  |
| last-line-width   | 75% (when lines > 1)                            |

**Rectangular Skeleton**
| Property          | Token                                          |
|-------------------|-------------------------------------------------|
| bg                | color.sys.{theme}.surface-container-highest     |
| height            | 120px (default)                                  |
| corner            | shape.corner.medium                              |

**Circular Skeleton**
| Property          | Token                                          |
|-------------------|-------------------------------------------------|
| bg                | color.sys.{theme}.surface-container-highest     |
| size              | 40px (default, set via width or height prop)     |
| corner            | shape.corner.full                                |

### States
- Animation: `skeleton-pulse` keyframes — opacity cycles 1 -> 0.4 -> 1 over 1.5s ease-in-out infinite

### Accessibility
- `aria-hidden="true"` on all skeleton elements (decorative placeholders)

---

## Layout Components

---

## Container

A centered, max-width layout wrapper with horizontal padding. Provides responsive width presets.

### Anatomy
- Single `<div>` with max-width constraint and auto margins

### Variants

**Size Presets**
| maxWidth | Value  |
|----------|--------|
| sm       | 640px  |
| md       | 768px  |
| lg       | 1024px (default) |
| xl       | 1280px |
| full     | 100%   |

**Token Mappings**
| Property          | Token                              |
|-------------------|------------------------------------|
| padding-h         | spacing.4 (16px)                   |
| margin            | auto (centered)                    |
| width             | 100%                               |

### States
- Static component (no interactive states)

### Accessibility
- No special ARIA roles required; semantic wrapper

---

## Grid

A CSS Grid layout component with configurable columns and gap. Includes a `Grid.Item` sub-component for spanning columns.

### Anatomy
- Grid container (`<div>` with `display: grid`)
- Grid items (`Grid.Item`) that can span multiple columns

### Variants

**Default Grid**
| Property          | Token                              |
|-------------------|------------------------------------|
| columns           | 12 (default, configurable)         |
| gap               | spacing.4 (16px) (default)         |
| display           | grid                               |
| grid-template     | `repeat(n, 1fr)` or custom string  |

**Grid.Item**
| Property          | Value                              |
|-------------------|------------------------------------|
| span              | 1 (default, configurable)          |
| grid-column       | `span {n}`                         |

### States
- Static component (no interactive states)

### Accessibility
- No special ARIA roles required; uses standard `<div>` elements

---

## Stack

A flexbox layout component for arranging children in a row or column with configurable gap, alignment, and wrapping.

### Anatomy
- Single `<div>` with `display: flex`

### Variants

**Default Stack**
| Property          | Token / Default                    |
|-------------------|------------------------------------|
| direction         | column (default), row              |
| gap               | spacing.4 (16px) (default)         |
| align             | alignItems (configurable)          |
| justify           | justifyContent (configurable)      |
| wrap              | false (default); true enables flexWrap: 'wrap' |
| display           | flex                               |

### States
- Static component (no interactive states)

### Accessibility
- No special ARIA roles required; uses standard `<div>` elements

---

## State Layer Opacity Model

For interactive components, overlay the relevant color at these opacities:

| State    | Opacity |
|----------|---------|
| Hover    | 8%      |
| Focus    | 12%     |
| Pressed  | 12%     |
| Dragged  | 16%     |
| Disabled (container) | 12% |
| Disabled (content)   | 38% |

Implement with CSS: `background-image: linear-gradient(rgba(r,g,b, opacity), rgba(r,g,b, opacity))`
or with a pseudo-element overlay.
