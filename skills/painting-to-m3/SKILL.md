---
name: painting-to-m3
description: Generate a strict Material Design 3 token set from a painting. Picks 3 maximally-distinct colors to fill M3's primary/secondary/tertiary slots, with standard near-white surfaces. Use when you need M3-compliant tokens that work with any M3-consuming framework (MUI, Jetpack Compose, Flutter). Triggers on "strict M3", "standard Material", "M3 compliant", "professional app theme from painting".
---

# Painting to Strict M3 Tokens

Generate a strict Material Design 3 compliant token set from any visual reference image — paintings, photographs, mood boards, or brand collateral. Picks exactly 3 maximally-distinct colors from the painting to fill M3's primary/secondary/tertiary slots, producing standard near-white surfaces and clean, professional themes.

## Why this matters

M3 is the lingua franca of modern design systems. MUI, Jetpack Compose, Flutter, and dozens of other frameworks consume M3 tokens natively. This skill produces tokens that drop into any M3-consuming framework without modification — no custom surface overrides, no extended color slots, just the standard 3-color M3 model done right.

## Workflow Overview

```
Image -> Color Extraction -> 3 Maximally-Distinct Picks -> Palette Roles -> Typography Direction ->
Spacing & Shape -> DTCG JSON -> CSS Variables / Tailwind Config -> WCAG Report -> Design Brief
```

## Step 1: Analyze the Image

When the user provides an image, study it carefully for:

**Color Analysis**
- Identify ALL distinct color families in the painting (there may be 4-8+)
- For each color family, estimate area coverage as a percentage of the canvas
- Note the overall temperature (warm/cool/neutral)
- Note the value range (high contrast vs low contrast vs muted)
- Note saturation characteristics (vivid vs desaturated vs mixed)

**Mood & Texture Analysis**
- Overall mood: serene, dramatic, playful, austere, luxurious, industrial, organic, etc.
- Texture qualities: smooth, rough, layered, flat, glossy, matte
- Spatial qualities: dense, airy, structured, organic, geometric

**Typography Direction** (inferred from mood, not literal)
- A painting with bold brushstrokes -> strong geometric sans-serif
- Soft watercolors -> elegant serif or humanist sans
- Hard-edge geometric abstraction -> monospace or technical fonts
- Impressionist -> classical serif with generous spacing
- Map the mood to 2-3 Google Fonts candidates for display + body

### Select 3 Maximally-Distinct Colors

M3 has exactly 3 color slots. The goal is to pick 3 colors that look as DIFFERENT as possible from each other, so the resulting theme has clear visual contrast between primary, secondary, and tertiary roles.

**Selection criteria (in order of importance):**

1. **Hue separation**: Maximize angular distance on the color wheel. Three colors at 120 degrees apart is ideal. Two greens 30 degrees apart will produce nearly identical tonal ramps — merge them and pick a more distant color instead.

2. **Visual significance**: Each color must be clearly visible in the painting and contribute to its character. Don't pick a color that covers <5% of the canvas or appears only in tiny details — it won't feel "from this painting" when used as a primary/secondary/tertiary role. The color should be something a viewer would name when describing the painting.

3. **Temperature contrast**: If the primary is warm (reds, oranges, yellows, warm greens), prefer a cool secondary (blues, teals, cool greens). This creates natural visual hierarchy.

4. **Saturation diversity**: Avoid picking 3 equally muted or 3 equally vivid colors. One vivid + one moderate + one muted creates depth.

**The "two similar colors" problem:**
When two candidate colors have hue distance < 30 degrees:
- Pick the one with more area coverage AND reasonable saturation
- Document the other in --considered-colors
- Example: warm-green (#8baa22, 15%) and cool-green (#6d9b2e, 45%) -> pick the 45% one, document the other

**Role assignment:**
- Primary: Most prominent AND most saturated color. If two colors tie in area (~15% difference), prefer the more saturated one — it produces a more distinctive M3 tonal ramp.
- Secondary: The color with most temperature contrast from primary.
- Tertiary: The remaining pick — this is M3's "surprise accent" slot.

**Present to the user:**
"I found N color families in this painting. For strict M3, I'm selecting these 3:
- Primary: [color] — [why]
- Secondary: [color] — [why]
- Tertiary: [color] — [why]
The remaining colors ([list]) are documented as considered-but-not-used. If you want ALL painting colors represented, try the painting-to-theme skill instead."

Present this analysis to the user conversationally. Ask them:
1. Does this capture what you see in the image?
2. Do the 3 color picks feel right for primary/secondary/tertiary?
3. Any colors I should swap in or out?
4. What's the intended use? (web app, mobile app, marketing site, dashboard, presentation)
5. Light theme, dark theme, or both?

## Step 2: Build the Token Architecture

Follow the standard M3 three-tier model. This skill produces strictly compliant M3 tokens — no custom surface overrides, no extended color slots.

### Tier 1: Reference Tokens (raw palette)
The script generates 24-step tonal ramps for each color (primary, secondary, tertiary, neutral, error) using HSL approximation of HCT. Neutral ramps use low saturation (8-12%) from the primary hue, producing clean near-white surfaces with a subtle tint.

### Tier 2: System Tokens (semantic roles)
Map the reference palette to standard M3 semantic roles. See `references/m3-color-roles.md` for the complete light/dark tone mapping tables.

Key points:
- `error` -> always derive from red, but tinted ~15 degrees toward the painting's primary hue
- Typography: M3 type scale (57/45/36, 32/28/24, 22/16/14, 16/14/12, 14/12/11) with font pairing from mood analysis
- Shape: derive corner radius from the image (geometric -> sharp, organic -> rounded, mixed -> medium)
- Spacing: 4px base unit, scale: 4, 8, 12, 16, 20, 24, 32, 40, 48, 64

## Step 3: Generate DTCG JSON Output

Use the Python script at `scripts/generate_tokens.py` to produce all token files in W3C DTCG format:

```bash
python scripts/generate_tokens.py \
  --colors '{"primary":"#hexval","secondary":"#hexval","tertiary":"#hexval","neutral":"#hexval","error":"#hexval"}' \
  --considered-colors '{"wheat-gold":{"hex":"#c8a830","area":0.08,"note":"warm accent pops"},"cloud-cream":{"hex":"#f0ece0","area":0.05,"note":"highlight areas"}}' \
  --font-display "Font Name" \
  --font-body "Font Name" \
  --corner-style "rounded|sharp|organic" \
  --name "theme-name" \
  --output-dir ./themes/{painting-name}/m3/tokens
```

Use `--review-dir` to write review files (contrast-report.md, design-brief.md, palette-review.html) to a separate directory. When omitted, they go to `--output-dir`.

The `--considered-colors` flag documents painting colors that were identified but not assigned to M3's 3 slots. These appear in the design brief so downstream skills and users know what was available.

The script automatically generates all output files (token JSON, theme.css, tailwind config, contrast report, design brief, palette review HTML) and prints any WCAG AA failures to stdout. Report any failures to the user and offer to adjust tones before finalizing. **Do not silently ignore contrast failures.**

**Contrast guard.** Before writing files, the script runs `enforce_contrast()`, which also checks body/muted text on every surface container and `primary` used as text on the page. Near-miss pairs are nudged up to 4.5:1 by adjusting HSL lightness only. Adjustments are printed as `contrast guard: light/role: #old -> #new`.

`design-brief.md` is the handoff contract for the `tokens-to-components` skill — it carries mood, typography rationale, considered colors, and design intent.

If the script is unavailable, generate the JSON manually following the template in `references/dtcg-template.json`.

If the script is unavailable, generate the palette review HTML manually following the template in `references/palette-review-template.html`.

## Step 4: Present to the User

Show the user the palette-review.html and a summary of the 3 selected colors, considered colors, font pairing, and any WCAG AA failures from the script output.

Mention: "If you want the painting's bold colors in surfaces and more color variety, try the painting-to-theme skill."

Ask if they want adjustments before finalizing.

## Step 5: Optional Additional Outputs

If the user needs platform-specific formats beyond the standard outputs:
- **Style Dictionary config** for multi-platform output
- **Flutter ThemeData** snippet
- **SwiftUI Color extension** snippet

## Asking the Human

This skill benefits enormously from human input at two key moments:

1. **After color extraction** (Step 1): The user knows their brand and intent better than any algorithm. Ask them to validate or adjust the 3 color picks before generating 500+ tokens from them. Show what colors were considered but not selected.

2. **After initial token generation** (Step 4): Show the output and ask if the color roles feel right, if the typography captures the mood, and if they want any adjustments.

Don't skip these checkpoints — they're the difference between a generic palette extractor and a thoughtful design system.

## Reference Files

- `references/dtcg-template.json` — Complete DTCG output structure template
- `references/m3-color-roles.md` — Material 3 color role definitions and tone mappings
- `references/font-mood-map.md` — Mapping from visual moods to Google Fonts recommendations
- `scripts/generate_tokens.py` — Token generation script (strict M3, no extended colors or surface overrides; also generates palette-review.html)
- `references/palette-review-template.html` — Fallback template for palette-review.html if the script is unavailable
