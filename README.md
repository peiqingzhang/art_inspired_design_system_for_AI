# Painting to Design System

Turn classic paintings into production-ready design systems — using AI agent skills. Three skills form a pipeline: analyze a painting's colors, generate design tokens, then build a full React component library. Every color, radius, and spacing value traces back to the source artwork.

The tokens and components are structured for AI agents to consume and build with. An agent can read the design tokens, apply them to new UI, or extend the component library — no manual design handoff needed.

## Skills

Three self-contained skills in `skills/`. Each has a `SKILL.md` (instructions any LLM agent can follow), reference files, and Python scripts that do the heavy lifting.

| Skill | What it does |
|-------|-------------|
| **painting-to-m3** | Strict Material Design 3 tokens. Picks 3 maximally-distinct colors for primary/secondary/tertiary, standard near-white surfaces. Drop-in compatible with MUI, Jetpack Compose, Flutter. |
| **painting-to-theme** | Expressive tokens that capture the painting's full color richness. Bold surfaces pulled from the canvas, extended color tokens for every accent, dark mode from the painting's shadows. |
| **tokens-to-components** | 25 React components (TypeScript + CSS variables) generated from the tokens. Includes Storybook stories, visual preview HTML, and WCAG AA contrast compliance. |

These skills work with Claude Code (as local plugins), but the `SKILL.md` format is plain markdown — any AI coding agent (Cursor, Windsurf, Copilot, etc.) can follow the instructions and run the scripts.

### Pipeline

```
Painting image
  → painting-to-m3  or  painting-to-theme
    → .tokens.json (W3C DTCG format)
      → tokens-to-components
        → React components + preview.html
```

## Themes

Eight paintings, each with both an M3 (strict) and Theme (expressive) variant — 16 complete design systems.

| Theme | Painting | Mood |
|-------|----------|------|
| `vangogh-irises` | Van Gogh — Irises (1889) | Vibrant, impasto, impressionist energy |
| `vangogh-green-wheat` | Van Gogh — Green Wheat Fields (1890) | Serene, pastoral, luminous |
| `monet-water-lilies` | Monet — Water Lilies (1906) | Serene, ethereal, impressionist reverie |
| `hokusai-great-wave` | Hokusai — The Great Wave (1831) | Dramatic, powerful, ukiyo-e precision |
| `hopper-nighthawks` | Hopper — Nighthawks (1942) | Urban, noir, late-night melancholy |
| `matisse-red-studio` | Matisse — The Red Studio (1911) | Bold, expressive, Fauvist energy |
| `cezanne-mont-sainte-victoire` | Cezanne — Mont Sainte-Victoire (1887) | Structured, contemplative, proto-cubist |
| `wang-ximeng-rivers-mountains` | Wang Ximeng — A Thousand Li (1113) | Majestic, classical Chinese landscape |

### Theme structure

```
themes/{painting-name}/
├── source/painting.jpg          # Source painting
├── m3/                          # Strict M3 variant
│   ├── tokens/                  # .tokens.json, theme.css, tailwind config
│   ├── components/              # 25 React components + Storybook stories
│   └── review/                  # preview.html, palette-review.html, contrast-report.md
└── theme/                       # Expressive variant
    ├── tokens/
    ├── components/
    └── review/
```

## Usage

### With an AI coding agent

Point your agent at a skill's `SKILL.md` and give it a painting. The instructions and scripts handle the rest.

In Claude Code, install as a local plugin and use the slash commands:

```
> /painting-to-theme path/to/painting.jpg
> /tokens-to-components path/to/tokens/
```

### Using the tokens directly

The `.tokens.json` files follow the W3C DTCG spec. Use `theme.css` for CSS custom properties, or `tailwind.config.snippet.js` for Tailwind.

### Using the components

Each theme's `components/` folder is a self-contained React library:

```tsx
import { Button, Card, Input } from './components';
import './components/theme.css';

<Button variant="filled">Primary Action</Button>
<Card variant="elevated">Content here</Card>
```

## Component sets

25 components across 5 sets:

| Set | Components |
|-----|-----------|
| **Core** | Button, Card, Input, Chip, Badge, Avatar, Divider |
| **Navigation** | AppBar, Tabs, Sidebar, Breadcrumb, BottomNav |
| **Data** | Table, List, DataCard, Stat |
| **Feedback** | Dialog, Snackbar, Tooltip, Progress, Skeleton |
| **Layout** | Container, Grid, Stack, Surface |

All components follow M3 spec with filled/outlined/tonal variants, state layers, and WCAG AA keyboard accessibility.

## License

The skills and generated code are provided as-is. Source paintings are public domain.
