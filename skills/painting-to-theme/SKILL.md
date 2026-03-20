---
name: painting-to-theme
description: Generate an expressive design token system that captures a painting's full color richness. Maps EVERY significant painting color to a UI role — bold surfaces, extended color tokens, painting-faithful atmosphere. Use when the UI should feel like being inside the painting. Triggers on "expressive theme", "painting atmosphere", "all painting colors", "rich palette", "evoke the painting", "painting-faithful", or any request where the user wants maximum color expressiveness from a visual reference.
---

# Painting to Expressive Theme

Generate a design token system that captures a painting's **full color richness** -- not just three M3 slots, but every significant color story in the image. The goal is a UI that feels like being inside the painting: bold surfaces pulled directly from the canvas, extended color tokens for every accent and atmospheric tone, and dark mode surfaces drawn from the painting's shadows.

Standard M3 theming reduces a painting to 3 color roles (primary/secondary/tertiary) and washes surfaces to near-white. This skill goes further. It catalogs 8-12 distinct color stories, maps each to a UI role, picks surface colors directly from the painting for both light and dark modes, and creates extended tokens for colors that do not fit the M3 model. The result is a theme where every component carries the painting's atmosphere.

## Workflow Overview

```
Image -> Deep Color Census (8-12 colors) -> M3 Roles + Extended Tokens ->
Surface Picks (light & dark) -> DTCG JSON -> CSS / Tailwind -> WCAG Report -> Design Brief
```

## Step 1: Deep Painting Analysis

When the user provides an image, perform a thorough analysis that goes well beyond "dominant + secondary + accent."

### Color Analysis

- Identify the dominant color (largest visual area)
- Identify 2-3 secondary colors (supporting areas)
- Identify 1-2 accent colors (small but high-contrast pops)
- **Estimate color proportions**: What percentage of the canvas does each color family occupy? Express as decimals summing to ~1.0. These proportions drive how strongly the dominant color tints UI surfaces.
- Note the overall temperature (warm/cool/neutral)
- Note the value range (high contrast vs low contrast vs muted)
- Note saturation characteristics (vivid vs desaturated vs mixed)

### Color Census (target 8-12 colors)

Go beyond "dominant + secondary + accent." Catalog every distinct color story in the painting by its compositional role:

| Compositional Role | What to Look For | UI Mapping |
|---|---|---|
| Background expanse | Largest area, sets atmosphere | Page background (--surfaces bg) |
| Foreground subject | Most active/vibrant area | Primary actions |
| Second mass | Supporting area | Secondary actions |
| Receding/atmospheric | Distance, depth, sky | Tertiary, muted elements |
| Highlights/light catch | Brightest spots, reflections | Card surfaces (--surfaces card) |
| Deep shadows | Darkest areas | Text color (--surfaces text) -- must carry painting's hue |
| Mid-tones | Transition areas | Muted text, borders (--surfaces muted/border) |
| Accent pop 1 | Small bright details | Extended token (e.g. wildflower gold) |
| Accent pop 2 | Secondary detail color | Extended token |
| Shadow accent | Dark areas with different hue | Extended token (e.g. deep shadow teal) |

For each color, note:
- Hex value (pick directly from the painting)
- Approximate area coverage (as decimal, e.g. 0.15)
- Compositional role (from table above)
- Suggested UI usage (1-2 phrases)

### Mood & Texture Analysis
- Overall mood: serene, dramatic, playful, austere, luxurious, industrial, organic, etc.
- Texture qualities: smooth, rough, layered, flat, glossy, matte
- Spatial qualities: dense, airy, structured, organic, geometric

### Typography Direction (inferred from mood, not literal)
- A painting with bold brushstrokes -> strong geometric sans-serif
- Soft watercolors -> elegant serif or humanist sans
- Hard-edge geometric abstraction -> monospace or technical fonts
- Impressionist -> classical serif with generous spacing
- Map the mood to 2-3 Google Fonts candidates for display + body

### Surface Color Picks (MANDATORY)

Pick specific hex values directly from the painting for these functional UI roles.
These are what make the UI feel like the painting. ALL 5 are required for both light and dark modes.

**Light mode surfaces:**
- **bg**: The painting's background/dominant area color -> becomes page background. Use the ACTUAL color from the painting, not a lightened version. If the background is bold yellow, the page bg should be bold yellow.
- **card**: The painting's lightest/highlight areas -> becomes 5 container surface levels, interpolated between card (lightest) and bg (boldest) for visual hierarchy. Often a cream, white, or pale tint found in the painting's highlights.
- **text**: A very dark shade found in the painting (darkest shadows, outlines) -> becomes main body text. MUST share the primary color's hue family -- if primary is green, text should be deep forest green (#2C522F), not generic black (#1a1a1a) or neutral gray. Pick from the painting's darkest area that carries the dominant hue. This is what makes the UI feel cohesive; generic dark text breaks the painting's atmosphere. Exception: when the bg surface is itself very dark/saturated (e.g. Matisse's red), text must be light to contrast -- pick a light tone from the painting's highlights that still carries warmth.
- **muted**: A medium-dark shade from the painting's dominant family -> becomes secondary text, labels, captions. Like a darker version of the background color.
- **border**: A medium shade from the painting's dominant family -> becomes outlines and dividers.

**Dark mode surfaces:**
For dark mode surfaces, pick from the painting's darkest areas -- deep shadows, underpainting, night-sky tones. These should carry the painting's hue at low lightness.
- **bg**: The painting's deepest shadow color -> dark mode page background
- **card**: A slightly lighter dark tone from the painting -> dark mode card surfaces
- **text**: A light tone from the painting's highlight areas -> dark mode text. MUST carry the painting's hue at high lightness -- if the painting is green, use a light sage (#D0E4D0), not generic white (#f0f0f0). Pick from the painting's lightest areas that still show color.
- **muted**: A mid-light tone from the painting -> dark mode secondary text
- **border**: A dark mid-tone from the painting -> dark mode outlines

### Extended Color Tokens (target 3-6)

Identify painting colors that don't fit primary/secondary/tertiary and propose them as extended tokens with painting-descriptive names and suggested UI roles.

Name them after what they represent in the painting (wheat-gold, cloud-cream, deep-teal), not generic labels (extended-1) or abstract semantics (accent-warm). The names flow to CSS variables like --color-wheat-gold -- they should be self-documenting.

For each extended color, also specify its suggested UI usage:
- "wheat-gold -> badges, star ratings, highlight accents"
- "cloud-cream -> warm card surfaces, hero section backgrounds"
- "deep-teal -> rich dark accents, footer backgrounds, sidebar emphasis"

Extended tokens are first-class citizens in this skill, not an optional afterthought. Every painting has colors beyond the M3 three-slot model -- find them and give them roles.

### Present Analysis to User

Show the full color census, surface picks (light and dark), extended tokens with proposed names and roles, and proportions breakdown. Ask:
1. Does this capture what you see in the image?
2. Do the surface picks feel right -- especially the page background?
3. Do the extended token names resonate with the painting?
4. Any colors I should emphasize more or tone down?
5. What's the intended use? (web app, mobile app, marketing site, dashboard, presentation)
6. Light theme, dark theme, or both?

## Step 2: Build the Token Architecture

Follow an M3-inspired three-tier model, adapted to preserve the painting's full character. When M3 conventions would wash out the painting's mood (e.g. near-white surfaces), the painting wins.

### Tier 1: Reference Tokens (raw palette)
The script generates 24-step tonal ramps for each color (including extended colors) using HSL approximation of HCT. Neutral ramps use proportion-based saturation scaling from the primary hue.

### Tier 2: System Tokens (semantic roles)
Map the reference palette to M3 semantic roles for light and dark themes, plus extended token roles. See `references/m3-color-roles.md` for the complete tone mapping tables.

**Key differences from standard M3 theming:**
- **Surfaces come from painting picks, not tonal computation.** The `--surfaces` and `--surfaces-dark` flags inject actual painting colors as surface tokens.
- **Inverted surface hierarchy**: The page background is the BOLDEST surface (painting's dominant color), and cards are LIGHTER (highlights). This inverts standard M3.
- **Dark surfaces from painting shadows**: Drawn from the painting's actual shadow areas, carrying the painting's hue at low lightness.
- **Extended tokens are first-class**: They get the same semantic treatment as M3 roles (base, on-*, container, on-container) in both light and dark themes.

Typography, shape, and spacing follow the same M3 conventions as painting-to-m3 — font pairing from mood analysis, corner radius from image mood, 4px spacing base.

## Step 3: Generate Output

Use the Python script at `scripts/generate_tokens.py` to produce all token files in W3C DTCG format:

```bash
python scripts/generate_tokens.py \
  --colors '{"primary":"#hexval","secondary":"#hexval","tertiary":"#hexval","neutral":"#hexval","error":"#hexval"}' \
  --proportions '{"primary":0.45,"secondary":0.20,"tertiary":0.12,"neutral":0.08}' \
  --surfaces '{"bg":"#hexval","card":"#hexval","text":"#hexval","muted":"#hexval","border":"#hexval"}' \
  --surfaces-dark '{"bg":"#hexval","card":"#hexval","text":"#hexval","muted":"#hexval","border":"#hexval"}' \
  --extended '{"wheat-gold":"#c8a830","cloud-cream":"#f0ece0","deep-teal":"#1e4a3a"}' \
  --color-roles '{"wheat-gold":"badges, star ratings","cloud-cream":"warm card surfaces","deep-teal":"dark accents, footers"}' \
  --font-display "Font Name" \
  --font-body "Font Name" \
  --corner-style organic \
  --name "theme-name" \
  --mood "serene, luminous, impressionist" \
  --rationale "This palette captures the painting's full atmosphere." \
  --output-dir ./themes/{painting-name}/theme/tokens
```

Use `--review-dir` to write review files (contrast-report.md, design-brief.md, palette-review.html) to a separate directory. When omitted, they go to `--output-dir`.

**Always provide `--surfaces`, `--surfaces-dark`, and `--extended`.** Without them, the output is a standard M3 theme that does not capture the painting's expressiveness.

The script automatically generates all output files (token JSON, theme.css, tailwind config, contrast report, design brief, palette review HTML) and prints any WCAG AA failures to stdout. Report any failures to the user and offer to adjust tones before finalizing. **Do not silently ignore contrast failures.**

`design-brief.md` is the handoff contract for the `tokens-to-components` skill — it includes the extended color usage guide so downstream skills know how to apply extended colors to UI roles.

If the script is unavailable, generate the palette review HTML manually following the template in `references/palette-review-template.html`.

## Step 4: Present to the User

Show the user the palette-review.html and a summary of the color census, extended tokens, surface picks, and any WCAG AA failures from the script output.

Note: For a standards-compliant M3 theme with fewer extended colors, try the `painting-to-m3` skill instead.

Ask if they want adjustments before finalizing.

## Asking the Human

This skill benefits enormously from human input at two key moments:

1. **After color census** (Step 1): The user knows their brand and intent better than any algorithm. Ask them to validate or adjust the palette mapping, especially extended token names and surface picks, before generating tokens.

2. **After initial token generation** (Step 4): Show the output and ask if the color roles feel right, if the extended tokens capture the painting's character, and if they want any adjustments.

Don't skip these checkpoints -- they're the difference between a generic palette extractor and a painting-faithful design system.

## Reference Files

- `references/dtcg-template.json` -- Complete DTCG output structure template
- `references/m3-color-roles.md` -- Material 3 color role definitions and tone mappings
- `references/font-mood-map.md` -- Mapping from visual moods to Google Fonts recommendations
- `scripts/generate_tokens.py` -- Token generation script (expressive variant with --surfaces-dark, --color-roles; also generates palette-review.html)
- `references/palette-review-template.html` -- Fallback template for palette-review.html if the script is unavailable
