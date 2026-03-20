#!/usr/bin/env python3
"""
Generate W3C DTCG-compliant design token files from extracted colors and typography choices.

Expressive Painting variant: captures a painting's full color richness with
dark-mode surface overrides, extended color tokens, and a color role map
in the design brief.

Usage:
    python generate_tokens.py \
        --colors '{"primary":"#5c5ea1","secondary":"#8b6e4e","tertiary":"#4e8b6e","neutral":"#7a7a78","error":"#ba1a1a"}' \
        --proportions '{"primary":0.55,"secondary":0.25,"tertiary":0.15,"neutral":0.05}' \
        --surfaces '{"bg":"#hexval","card":"#hexval","text":"#hexval","muted":"#hexval","border":"#hexval"}' \
        --surfaces-dark '{"bg":"#1a2a1a","card":"#2a3a2a","text":"#d0e0c0","muted":"#8a9a7a","border":"#4a5a3a"}' \
        --extended '{"wheat-gold":"#c8a830","cloud-cream":"#f0ece0","deep-teal":"#1e4a3a"}' \
        --color-roles '{"wheat-gold":"badges, star ratings","cloud-cream":"warm card surfaces","deep-teal":"dark accents, footers"}' \
        --font-display "Cormorant Garamond" \
        --font-body "Source Serif 4" \
        --corner-style rounded \
        --name "monet-waterlilies" \
        --mood "serene, cool, impressionist" \
        --rationale "This palette targets a calm, reflective emotional response." \
        --output-dir ./output
"""

import argparse
import colorsys
import json
import math
import os
import re
import sys


def hex_to_hsl(hex_color: str):
    """Convert hex color to HSL (0-360, 0-100, 0-100)."""
    hex_color = hex_color.lstrip('#')
    r, g, b = int(hex_color[0:2], 16) / 255, int(hex_color[2:4], 16) / 255, int(hex_color[4:6], 16) / 255
    h, l, s = colorsys.rgb_to_hls(r, g, b)
    return h * 360, s * 100, l * 100


def hsl_to_hex(h: float, s: float, l: float) -> str:
    """Convert HSL (0-360, 0-100, 0-100) to hex string."""
    h, s, l = h / 360, s / 100, l / 100
    r, g, b = colorsys.hls_to_rgb(h, l, s)
    return f"#{int(r*255):02x}{int(g*255):02x}{int(b*255):02x}"


def generate_tonal_ramp(hex_color: str) -> dict:
    """Generate a tonal ramp from a source color using HSL approximation.

    Applies a lightness correction at tone 40 for high-saturation colors:
    HSL L=40% with high saturation (especially greens/cyans) produces higher
    perceived luminance than expected, causing WCAG failures against white.
    We darken tone 40 proportionally to saturation to compensate.
    """
    h, s, l = hex_to_hsl(hex_color)
    tones = [0, 4, 6, 10, 12, 17, 20, 22, 24, 30, 40, 50, 60, 70, 80, 87, 90, 92, 94, 95, 96, 98, 99, 100]
    ramp = {}
    for tone in tones:
        # Adjust saturation: reduce at extremes to avoid neon
        if tone <= 10:
            sat = s * 0.6
        elif tone >= 90:
            sat = s * 0.7
        else:
            sat = s
        # Clamp saturation
        sat = max(0, min(100, sat))
        # Lightness correction for WCAG: darken tone 40 for saturated colors
        # HSL L=40% with high saturation looks lighter than expected, especially
        # for yellows/greens (high luminance coefficient in sRGB). Apply a
        # hue-aware correction: yellows (H=30-90) need ~2x more darkening.
        actual_l = tone
        if tone == 30 and s > 20 and 30 <= h <= 90:
            # Yellow containers (dark theme tone 30) also need correction
            actual_l = 30 - (s - 20) * 0.10
        elif tone == 40 and s > 20:
            # Yellow/green hues (30-90) have higher perceived luminance
            hue_factor = 1.0
            if 30 <= h <= 90:
                hue_factor = 1.8  # yellows need much more darkening
            elif 90 < h <= 150:
                hue_factor = 1.3  # greens need moderate extra
            actual_l = 40 - (s - 20) * 0.18 * hue_factor
        elif tone == 50 and s > 30:
            hue_factor = 1.0
            if 30 <= h <= 90:
                hue_factor = 1.6
            elif 90 < h <= 150:
                hue_factor = 1.2
            actual_l = 50 - (s - 30) * 0.12 * hue_factor
        ramp[str(tone)] = {
            "$value": hsl_to_hex(h, sat, actual_l),
            "$type": "color"
        }
    return ramp


def generate_neutral_ramp(hex_color: str, saturation_pct: float = 10) -> dict:
    """Generate a neutral tonal ramp: same hue, very low saturation."""
    h, s, l = hex_to_hsl(hex_color)
    tones = [0, 4, 6, 10, 12, 17, 20, 22, 24, 30, 40, 50, 60, 70, 80, 87, 90, 92, 94, 95, 96, 98, 99, 100]
    ramp = {}
    for tone in tones:
        sat = saturation_pct if tone > 5 and tone < 95 else saturation_pct * 0.5
        ramp[str(tone)] = {
            "$value": hsl_to_hex(h, sat, tone),
            "$type": "color"
        }
    return ramp


def _hsl_distance(hex1: str, hex2: str) -> float:
    """Compute perceptual distance between two colors in HSL space.

    Uses the same formula as the palette review warning logic:
    hue difference is scaled by 1/3.6 so that a 360° sweep maps to 0-100,
    then Euclidean distance with saturation and lightness (both 0-100).
    """
    h1, s1, l1 = hex_to_hsl(hex1)
    h2, s2, l2 = hex_to_hsl(hex2)
    hue_diff = min(abs(h1 - h2), 360 - abs(h1 - h2))
    return math.sqrt((hue_diff / 3.6) ** 2 + (s1 - s2) ** 2 + (l1 - l2) ** 2)


def filter_extended_by_m3_similarity(extended: dict, colors: dict,
                                     color_roles: dict,
                                     threshold: float = 15) -> tuple:
    """Drop extended colors that are too similar to M3 roles.

    Returns (filtered_extended, filtered_color_roles) with entries removed
    for any extended color whose HSL distance to primary, secondary, or
    tertiary is below *threshold*.
    """
    m3_roles = {role: colors[role] for role in ("primary", "secondary", "tertiary")
                if role in colors}
    filtered_ext = {}
    filtered_roles = dict(color_roles)
    for name, hex_val in extended.items():
        dropped = False
        for role, role_hex in m3_roles.items():
            dist = _hsl_distance(hex_val, role_hex)
            if dist < threshold:
                print(f"NOTE: Dropped extended color '{name}' — too similar to {role}")
                dropped = True
                break
        if not dropped:
            filtered_ext[name] = hex_val
        else:
            filtered_roles.pop(name, None)
    return filtered_ext, filtered_roles


def find_dominant_color(colors: dict, proportions: dict) -> tuple:
    """Find which color has the highest proportion in the painting.

    Returns (hex_color, role_name, proportion_value).
    The dominant color may be secondary or tertiary, not just primary --
    e.g. a painting's background color (secondary) may cover more area
    than its subject (primary).
    """
    if not proportions:
        return (colors.get("primary", "#808080"), "primary", 0)

    # Map proportion keys to color dict keys
    best_role = max(proportions, key=proportions.get)
    best_prop = proportions[best_role]
    best_hex = colors.get(best_role, colors.get("primary", "#808080"))
    return (best_hex, best_role, best_prop)


def generate_painting_surface_ramp(dominant_hex: str, proportion: float) -> dict:
    """Generate surfaces directly from the dominant painting color.

    KEY INSIGHT: In standard M3, tone = lightness (tone 98 -> L=98% -> near-white).
    This means surfaces always wash out to gray regardless of saturation.
    A bold painting background at L=55% is impossible to achieve with tone 98.

    Solution: REMAP lightness for surface tones. Instead of tone=lightness,
    compress the light end so surface tones carry real color:

      tone 98 (page bg):      L~80%, S~70%  -> recognizably the painting's color
      tone 96 (container-low): L~86%, S~55%  -> lighter card surface
      tone 94 (container):     L~89%, S~45%  -> cream card
      tone 92 (container-high): L~91%, S~38% -> light cream
      tone 90 (highest):       L~93%, S~30%  -> lightest cream
      tone 100:                L=100%          -> white

    This inverts the visual hierarchy to match paintings: bold bg -> cream cards.

    For dark tones (text), use HIGH saturation to make text thematic:
      tone 10 (on-surface):    L~10%, S~70%  -> deep colored text carrying the painting's hue
      tone 30 (on-surf-var):   L~30%, S~60%  -> muted colored text for labels/captions
    """
    h, s, l = hex_to_hsl(dominant_hex)

    # Intensity scales with proportion: 0.40 -> 0.80x, 0.50+ -> 1.0x
    intensity = min(proportion / 0.50, 1.0)

    tones = [0, 4, 6, 10, 12, 17, 20, 22, 24, 30, 40, 50, 60, 70, 80, 87, 90, 92, 94, 95, 96, 98, 99, 100]

    # Non-linear lightness remap for surface tones (90-100)
    # Standard M3: tone 98 -> L98 (near-white, no color possible)
    # Bold painting: tone 98 -> L72 (recognizably the painting's color)
    #
    # This inverts the visual hierarchy to match paintings:
    #   page bg (tone 98) = BOLDEST (painting's dominant color)
    #   cards (tone 90-96) = LIGHTER (cream/white cards floating on bold bg)
    lightness_remap = {
        100: 100,
        99:  97,
        98:  72,   # page bg -- bold painting color
        96:  80,   # container-low -- lighter
        95:  83,
        94:  86,   # container -- cream card
        92:  89,   # container-high
        90:  92,   # container-highest -- lightest cream
        87:  87,
    }

    ramp = {}
    for tone in tones:
        # Remap lightness for surface tones
        actual_lightness = lightness_remap.get(tone, tone)

        if tone >= 99:
            sat = s * 0.15 * intensity  # barely tinted white
        elif tone >= 96:
            # Page bg: bold, recognizably the painting's color
            sat = s * 0.95 * intensity
        elif tone >= 90:
            # Cards: lighter cream, less saturated than bg
            # Gradient: 50% at 90 rising to ~80% at 96
            t = (tone - 90) / 6.0  # 0 at 90, 1 at 96
            sat = s * (0.50 + t * 0.30) * intensity
        elif tone >= 50:
            # Mid tones: full painting character
            sat = s * 0.95 * intensity
        elif tone <= 5:
            # Near-black: strong hue presence
            sat = s * 0.60 * intensity
        else:
            # Dark tones (6-49): HIGH saturation for thematic text
            # This makes on-surface (tone 10) deeply colored like the painting
            # This makes text deeply colored, carrying the painting's hue
            sat = s * 0.95 * intensity

        sat = max(0, min(100, sat))
        ramp[str(tone)] = {
            "$value": hsl_to_hex(h, sat, actual_lightness),
            "$type": "color"
        }
    return ramp


def generate_painting_outline_ramp(dominant_hex: str, proportion: float) -> dict:
    """Generate outline/variant ramp from the dominant color.

    Outlines use the dominant hue at moderate saturation.
    Muted text (on-surface-variant, tone 30) should be a clear dark shade
    of the dominant color, carrying the painting's hue.
    """
    h, s, l = hex_to_hsl(dominant_hex)
    intensity = min(proportion / 0.50, 1.0)

    tones = [0, 4, 6, 10, 12, 17, 20, 22, 24, 30, 40, 50, 60, 70, 80, 87, 90, 92, 94, 95, 96, 98, 99, 100]
    ramp = {}
    for tone in tones:
        if tone >= 90:
            sat = s * (0.50 - (tone - 90) * 0.03) * intensity
        elif tone >= 50:
            # Outline (tone 50): clearly colored, carrying the painting's hue
            sat = s * 0.80 * intensity
        elif tone <= 5:
            sat = s * 0.50 * intensity
        else:
            # Dark tones including on-surface-variant (tone 30):
            # strongly colored muted text for labels/captions
            sat = s * 0.85 * intensity

        sat = max(0, min(100, sat))
        ramp[str(tone)] = {
            "$value": hsl_to_hex(h, sat, tone),
            "$type": "color"
        }
    return ramp


# ── Component role slots that extended colors can fill ──────────────────────
_COMPONENT_SLOTS = [
    "badge",
    "chip-selected",
    "card-accent",
    "sidebar-active",
    "fab",
    "banner",
    "tag",
    "highlight",
]

# Keywords in color_roles hints that map to specific component slots
_ROLE_KEYWORDS = {
    "badge": "badge",
    "tag": "tag",
    "chip": "chip-selected",
    "card": "card-accent",
    "sidebar": "sidebar-active",
    "nav": "sidebar-active",
    "fab": "fab",
    "banner": "banner",
    "accent": "card-accent",
    "highlight": "highlight",
    "star": "badge",
    "rating": "badge",
    "status": "badge",
    "surface": "card-accent",
    "footer": "sidebar-active",
}


def _build_color_component_map(extended: dict, color_roles: dict) -> dict:
    """Map extended painting colors to component slots.

    Uses keyword hints from color_roles when available, otherwise assigns
    colors to slots in order. Returns a dict like:
        {"badge": "vase-ochre", "chip-selected": "iris-mauve", ...}
    """
    assigned = {}       # slot -> color name
    used_colors = set()
    available_slots = list(_COMPONENT_SLOTS)

    # Pass 1: keyword-based assignment from color_roles hints
    for color_name, role_desc in color_roles.items():
        if color_name not in extended:
            continue
        desc_lower = role_desc.lower()
        for keyword, slot in _ROLE_KEYWORDS.items():
            if keyword in desc_lower and slot in available_slots:
                assigned[slot] = color_name
                used_colors.add(color_name)
                available_slots.remove(slot)
                break

    # Pass 2: assign remaining extended colors to remaining slots by order
    remaining_colors = [c for c in extended if c not in used_colors]
    for color_name in remaining_colors:
        if not available_slots:
            break
        slot = available_slots.pop(0)
        assigned[slot] = color_name
        used_colors.add(color_name)

    return assigned


def build_color_tokens(colors: dict, proportions: dict = None,
                       surfaces: dict = None, extended: dict = None,
                       surfaces_dark: dict = None,
                       color_roles: dict = None) -> dict:
    """Build the complete color.tokens.json structure.

    The `surfaces` dict is the key to evoking the source painting. When provided,
    surface/text system tokens are set to hex values picked directly from the
    painting -- the background color becomes the page background, the light areas
    become card surfaces, dark areas become text. No tonal ramp computation.

    surfaces keys (all optional):
      bg:     page background (-> surface)
      card:   card/container surface (-> surface-container, surface-container-low/high)
      text:   main text color (-> on-surface)
      muted:  secondary/label text (-> on-surface-variant)
      border: outline/divider color (-> outline)

    surfaces_dark keys (all optional, same structure as surfaces):
      bg:     dark mode page background (-> surface)
      card:   dark mode card surface (-> surface-container levels)
      text:   dark mode text color (-> on-surface)
      muted:  dark mode secondary text (-> on-surface-variant)
      border: dark mode outline color (-> outline)

    Falls back to tonal ramp computation when surfaces are not provided.
    """
    if proportions is None:
        proportions = {}
    if surfaces is None:
        surfaces = {}
    if extended is None:
        extended = {}
    if surfaces_dark is None:
        surfaces_dark = {}
    if color_roles is None:
        color_roles = {}

    primary_hex = colors["primary"]
    secondary_hex = colors["secondary"]
    tertiary_hex = colors["tertiary"]
    neutral_hex = colors.get("neutral", primary_hex)
    raw_error = colors.get("error", "#ba1a1a")
    eh, es, el = hex_to_hsl(raw_error)
    ph, _, _ = hex_to_hsl(primary_hex)
    hue_diff = (ph - eh + 180) % 360 - 180  # shortest arc
    error_h = (eh + hue_diff * 0.15) % 360
    error_hex = hsl_to_hex(error_h, es, el)

    # Always generate neutral ramps (needed for dark theme, fallback tones)
    dominant_hex, dominant_role, dominant_prop = find_dominant_color(colors, proportions)

    if dominant_prop >= 0.40:
        neutral_ramp = generate_painting_surface_ramp(dominant_hex, dominant_prop)
        neutral_variant_ramp = generate_painting_outline_ramp(dominant_hex, dominant_prop)
    elif dominant_prop > 0:
        neutral_ramp = generate_neutral_ramp(dominant_hex, 18 + dominant_prop * 30)
        neutral_variant_ramp = generate_neutral_ramp(dominant_hex, 22 + dominant_prop * 20)
    else:
        neutral_ramp = generate_neutral_ramp(neutral_hex, 10)
        neutral_variant_ramp = generate_neutral_ramp(neutral_hex, 18)

    ref = {
        "$description": "Reference palette -- tonal scales derived from source image",
        "primary": generate_tonal_ramp(primary_hex),
        "secondary": generate_tonal_ramp(secondary_hex),
        "tertiary": generate_tonal_ramp(tertiary_hex),
        "neutral": neutral_ramp,
        "neutral-variant": neutral_variant_ramp,
        "error": generate_tonal_ramp(error_hex)
    }

    # Extended color tonal ramps (painting colors beyond M3's 3 slots)
    for ext_name, ext_hex in extended.items():
        ref[ext_name] = generate_tonal_ramp(ext_hex)

    # Store proportions, dominant surface color, and color-component-map as metadata
    extensions = {}
    if proportions:
        extensions["painting-proportions"] = proportions
        extensions["dominant-surface-color"] = dominant_hex
        extensions["dominant-surface-role"] = dominant_role

    # Build color-component-map: maps extended colors to component roles
    # Auto-assign extended colors to component slots based on color_roles hints
    # or by order if no hints are provided
    if extended:
        component_map = _build_color_component_map(extended, color_roles)
        extensions["color-component-map"] = component_map

    if extensions:
        extensions["$description"] = (
            "Color area proportions from source painting (0-1 scale). "
            "Dominant surface color is used to generate surface tokens. "
            "color-component-map assigns extended painting colors to component roles "
            "for expressive rendering in tokens-to-components."
        )
        ref["$extensions"] = extensions

    def alias(palette, tone):
        return {"$value": f"{{color.ref.{palette}.{tone}}}", "$type": "color"}

    sys_light = {
        "primary": alias("primary", 40),
        "on-primary": alias("primary", 100),
        "primary-container": alias("primary", 90),
        "on-primary-container": alias("primary", 10),
        "primary-fixed": alias("primary", 90),
        "primary-fixed-dim": alias("primary", 80),
        "on-primary-fixed": alias("primary", 10),
        "on-primary-fixed-variant": alias("primary", 30),
        "secondary": alias("secondary", 40),
        "on-secondary": alias("secondary", 100),
        "secondary-container": alias("secondary", 90),
        "on-secondary-container": alias("secondary", 10),
        "tertiary": alias("tertiary", 40),
        "on-tertiary": alias("tertiary", 100),
        "tertiary-container": alias("tertiary", 90),
        "on-tertiary-container": alias("tertiary", 10),
        "error": alias("error", 40),
        "on-error": alias("error", 100),
        "error-container": alias("error", 90),
        "on-error-container": alias("error", 10),
        "surface": alias("neutral", 98),
        "on-surface": alias("neutral", 10),
        "surface-variant": alias("neutral-variant", 90),
        "on-surface-variant": alias("neutral-variant", 30),
        "surface-container-lowest": alias("neutral", 100),
        "surface-container-low": alias("neutral", 96),
        "surface-container": alias("neutral", 94),
        "surface-container-high": alias("neutral", 92),
        "surface-container-highest": alias("neutral", 90),
        "outline": alias("neutral-variant", 50),
        "outline-variant": alias("neutral-variant", 80),
        "inverse-surface": alias("neutral", 20),
        "inverse-on-surface": alias("neutral", 95),
        "inverse-primary": alias("primary", 80),
        "scrim": alias("neutral", 0),
        "shadow": alias("neutral", 0),
    }

    # Extended color semantic roles (light theme)
    for ext_name in extended:
        sys_light[ext_name] = alias(ext_name, 40)
        sys_light[f"on-{ext_name}"] = alias(ext_name, 100)
        sys_light[f"{ext_name}-container"] = alias(ext_name, 90)
        sys_light[f"on-{ext_name}-container"] = alias(ext_name, 10)

    # Apply direct surface overrides from painting color picks.
    # These bypass tonal ramp computation -- the painting's actual colors
    # are used directly as system token values.
    if surfaces:
        def hex_token(hex_val):
            return {"$value": hex_val, "$type": "color"}

        if "bg" in surfaces:
            sys_light["surface"] = hex_token(surfaces["bg"])
        if "card" in surfaces:
            card = surfaces["card"]
            bg_hex = surfaces.get("bg")
            if bg_hex:
                # Interpolate 5 levels between card (lightest) and bg (boldest)
                ch, cs, cl = hex_to_hsl(card)
                bh, bs, bl = hex_to_hsl(bg_hex)
                steps = {
                    "surface-container-lowest":  0.0,   # = card (lightest)
                    "surface-container-low":     0.2,
                    "surface-container":         0.4,
                    "surface-container-high":    0.6,
                    "surface-container-highest": 0.8,   # close to bg (boldest)
                }
                for role, t in steps.items():
                    h = ch + (bh - ch) * t
                    s = cs + (bs - cs) * t
                    l = cl + (bl - cl) * t
                    sys_light[role] = hex_token(hsl_to_hex(h, s, l))
            else:
                # No bg pick -- set all to card
                for role in ["surface-container-lowest", "surface-container-low",
                              "surface-container", "surface-container-high",
                              "surface-container-highest"]:
                    sys_light[role] = hex_token(card)
        if "text" in surfaces:
            sys_light["on-surface"] = hex_token(surfaces["text"])
        if "muted" in surfaces:
            sys_light["on-surface-variant"] = hex_token(surfaces["muted"])
        if "border" in surfaces:
            sys_light["outline"] = hex_token(surfaces["border"])

    sys_dark = {
        "primary": alias("primary", 80),
        "on-primary": alias("primary", 20),
        "primary-container": alias("primary", 30),
        "on-primary-container": alias("primary", 90),
        "secondary": alias("secondary", 80),
        "on-secondary": alias("secondary", 20),
        "secondary-container": alias("secondary", 30),
        "on-secondary-container": alias("secondary", 90),
        "tertiary": alias("tertiary", 80),
        "on-tertiary": alias("tertiary", 20),
        "tertiary-container": alias("tertiary", 30),
        "on-tertiary-container": alias("tertiary", 90),
        "error": alias("error", 80),
        "on-error": alias("error", 20),
        "error-container": alias("error", 30),
        "on-error-container": alias("error", 90),
        "surface": alias("neutral", 6),
        "on-surface": alias("neutral", 90),
        "surface-variant": alias("neutral-variant", 30),
        "on-surface-variant": alias("neutral-variant", 80),
        "surface-container-lowest": alias("neutral", 4),
        "surface-container-low": alias("neutral", 10),
        "surface-container": alias("neutral", 12),
        "surface-container-high": alias("neutral", 17),
        "surface-container-highest": alias("neutral", 22),
        "outline": alias("neutral-variant", 60),
        "outline-variant": alias("neutral-variant", 30),
        "inverse-surface": alias("neutral", 90),
        "inverse-on-surface": alias("neutral", 20),
        "inverse-primary": alias("primary", 40),
        "scrim": alias("neutral", 0),
        "shadow": alias("neutral", 0),
    }

    # Extended color semantic roles (dark theme)
    for ext_name in extended:
        sys_dark[ext_name] = alias(ext_name, 80)
        sys_dark[f"on-{ext_name}"] = alias(ext_name, 20)
        sys_dark[f"{ext_name}-container"] = alias(ext_name, 30)
        sys_dark[f"on-{ext_name}-container"] = alias(ext_name, 90)

    # Apply direct surface overrides for dark theme from painting's dark tones
    if surfaces_dark:
        def hex_token(hex_val):
            return {"$value": hex_val, "$type": "color"}

        if "bg" in surfaces_dark:
            sys_dark["surface"] = hex_token(surfaces_dark["bg"])
        if "card" in surfaces_dark:
            card = surfaces_dark["card"]
            bg_hex = surfaces_dark.get("bg")
            if bg_hex:
                ch, cs, cl = hex_to_hsl(card)
                bh, bs, bl = hex_to_hsl(bg_hex)
                steps = {
                    "surface-container-lowest":  0.0,
                    "surface-container-low":     0.2,
                    "surface-container":         0.4,
                    "surface-container-high":    0.6,
                    "surface-container-highest": 0.8,
                }
                for role, t in steps.items():
                    h = ch + (bh - ch) * t
                    s = cs + (bs - cs) * t
                    l = cl + (bl - cl) * t
                    sys_dark[role] = hex_token(hsl_to_hex(h, s, l))
            else:
                for role in ["surface-container-lowest", "surface-container-low",
                              "surface-container", "surface-container-high",
                              "surface-container-highest"]:
                    sys_dark[role] = hex_token(card)
        if "text" in surfaces_dark:
            sys_dark["on-surface"] = hex_token(surfaces_dark["text"])
        if "muted" in surfaces_dark:
            sys_dark["on-surface-variant"] = hex_token(surfaces_dark["muted"])
        if "border" in surfaces_dark:
            sys_dark["outline"] = hex_token(surfaces_dark["border"])

    return {
        "color": {
            "$description": "Color tokens extracted from visual reference",
            "ref": ref,
            "sys": {
                "$description": "Semantic color roles following Material Design 3",
                "light": sys_light,
                "dark": sys_dark
            }
        }
    }


def build_typography_tokens(font_display: str, font_body: str) -> dict:
    """Build the typography.tokens.json structure."""
    return {
        "typography": {
            "$description": "Typography tokens -- M3 type scale with custom font pairing",
            "ref": {
                "typeface": {
                    "brand": {"$value": font_display, "$type": "fontFamily"},
                    "plain": {"$value": font_body, "$type": "fontFamily"}
                },
                "weight": {
                    "regular": {"$value": 400, "$type": "fontWeight"},
                    "medium": {"$value": 500, "$type": "fontWeight"},
                    "bold": {"$value": 700, "$type": "fontWeight"}
                }
            },
            "sys": {
                "display-large": {"$type": "typography", "$value": {"fontFamily": "{typography.ref.typeface.brand}", "fontSize": "57px", "fontWeight": 400, "lineHeight": "64px", "letterSpacing": "-0.25px"}},
                "display-medium": {"$type": "typography", "$value": {"fontFamily": "{typography.ref.typeface.brand}", "fontSize": "45px", "fontWeight": 400, "lineHeight": "52px", "letterSpacing": "0px"}},
                "display-small": {"$type": "typography", "$value": {"fontFamily": "{typography.ref.typeface.brand}", "fontSize": "36px", "fontWeight": 400, "lineHeight": "44px", "letterSpacing": "0px"}},
                "headline-large": {"$type": "typography", "$value": {"fontFamily": "{typography.ref.typeface.brand}", "fontSize": "32px", "fontWeight": 400, "lineHeight": "40px", "letterSpacing": "0px"}},
                "headline-medium": {"$type": "typography", "$value": {"fontFamily": "{typography.ref.typeface.brand}", "fontSize": "28px", "fontWeight": 400, "lineHeight": "36px", "letterSpacing": "0px"}},
                "headline-small": {"$type": "typography", "$value": {"fontFamily": "{typography.ref.typeface.brand}", "fontSize": "24px", "fontWeight": 400, "lineHeight": "32px", "letterSpacing": "0px"}},
                "title-large": {"$type": "typography", "$value": {"fontFamily": "{typography.ref.typeface.brand}", "fontSize": "22px", "fontWeight": 400, "lineHeight": "28px", "letterSpacing": "0px"}},
                "title-medium": {"$type": "typography", "$value": {"fontFamily": "{typography.ref.typeface.plain}", "fontSize": "16px", "fontWeight": 500, "lineHeight": "24px", "letterSpacing": "0.15px"}},
                "title-small": {"$type": "typography", "$value": {"fontFamily": "{typography.ref.typeface.plain}", "fontSize": "14px", "fontWeight": 500, "lineHeight": "20px", "letterSpacing": "0.1px"}},
                "body-large": {"$type": "typography", "$value": {"fontFamily": "{typography.ref.typeface.plain}", "fontSize": "16px", "fontWeight": 400, "lineHeight": "24px", "letterSpacing": "0.5px"}},
                "body-medium": {"$type": "typography", "$value": {"fontFamily": "{typography.ref.typeface.plain}", "fontSize": "14px", "fontWeight": 400, "lineHeight": "20px", "letterSpacing": "0.25px"}},
                "body-small": {"$type": "typography", "$value": {"fontFamily": "{typography.ref.typeface.plain}", "fontSize": "12px", "fontWeight": 400, "lineHeight": "16px", "letterSpacing": "0.4px"}},
                "label-large": {"$type": "typography", "$value": {"fontFamily": "{typography.ref.typeface.plain}", "fontSize": "14px", "fontWeight": 500, "lineHeight": "20px", "letterSpacing": "0.1px"}},
                "label-medium": {"$type": "typography", "$value": {"fontFamily": "{typography.ref.typeface.plain}", "fontSize": "12px", "fontWeight": 500, "lineHeight": "16px", "letterSpacing": "0.5px"}},
                "label-small": {"$type": "typography", "$value": {"fontFamily": "{typography.ref.typeface.plain}", "fontSize": "11px", "fontWeight": 500, "lineHeight": "16px", "letterSpacing": "0.5px"}},
            }
        }
    }


def build_shape_tokens(corner_style: str) -> dict:
    """Build shape.tokens.json based on corner philosophy."""
    styles = {
        "sharp": {"extra-small": "2px", "small": "4px", "medium": "6px", "large": "8px", "extra-large": "12px"},
        "rounded": {"extra-small": "4px", "small": "8px", "medium": "12px", "large": "16px", "extra-large": "28px"},
        "organic": {"extra-small": "8px", "small": "12px", "medium": "16px", "large": "24px", "extra-large": "32px"},
    }
    radii = styles.get(corner_style, styles["rounded"])
    shape = {
        "shape": {
            "$description": f"Shape tokens -- {corner_style} corner style derived from visual mood",
            "corner": {
                "none": {"$value": "0px", "$type": "dimension"},
                "extra-small": {"$value": radii["extra-small"], "$type": "dimension"},
                "small": {"$value": radii["small"], "$type": "dimension"},
                "medium": {"$value": radii["medium"], "$type": "dimension"},
                "large": {"$value": radii["large"], "$type": "dimension"},
                "extra-large": {"$value": radii["extra-large"], "$type": "dimension"},
                "full": {"$value": "9999px", "$type": "dimension", "$description": "Pill shape"},
            }
        }
    }
    return shape


def build_spacing_tokens() -> dict:
    """Build spacing.tokens.json -- standard 4px base unit scale."""
    return {
        "spacing": {
            "$description": "Spacing tokens -- 4px base unit",
            "0": {"$value": "0px", "$type": "dimension"},
            "1": {"$value": "4px", "$type": "dimension"},
            "2": {"$value": "8px", "$type": "dimension"},
            "3": {"$value": "12px", "$type": "dimension"},
            "4": {"$value": "16px", "$type": "dimension"},
            "5": {"$value": "20px", "$type": "dimension"},
            "6": {"$value": "24px", "$type": "dimension"},
            "8": {"$value": "32px", "$type": "dimension"},
            "10": {"$value": "40px", "$type": "dimension"},
            "12": {"$value": "48px", "$type": "dimension"},
            "16": {"$value": "64px", "$type": "dimension"},
            "20": {"$value": "80px", "$type": "dimension"},
            "24": {"$value": "96px", "$type": "dimension"},
        }
    }


def relative_luminance(hex_color: str) -> float:
    """Compute WCAG relative luminance for a hex color."""
    hex_color = hex_color.lstrip('#')
    rgb = [int(hex_color[i:i+2], 16) / 255.0 for i in (0, 2, 4)]
    def linearize(c):
        return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4
    r, g, b = [linearize(c) for c in rgb]
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def contrast_ratio(hex1: str, hex2: str) -> float:
    """Compute WCAG contrast ratio between two hex colors."""
    l1 = relative_luminance(hex1)
    l2 = relative_luminance(hex2)
    lighter, darker = max(l1, l2), min(l1, l2)
    return (lighter + 0.05) / (darker + 0.05)


def resolve_color_aliases(color_tokens: dict) -> dict:
    """Resolve all {color.ref.X.Y} aliases to hex values for both light and dark."""
    ref = color_tokens["color"]["ref"]

    def resolve(alias_str):
        match = re.match(r'\{color\.ref\.([\w-]+)\.(\d+)\}', alias_str)
        if match:
            palette, tone = match.group(1), match.group(2)
            if palette in ref and tone in ref[palette]:
                return ref[palette][tone]["$value"]
        return alias_str

    result = {"light": {}, "dark": {}}
    for mode in ("light", "dark"):
        for role, token in color_tokens["color"]["sys"][mode].items():
            result[mode][role] = resolve(token["$value"])
    return result


def write_contrast_report(color_tokens: dict, output_dir: str, extended: dict = None):
    """Check WCAG contrast for semantic color pairs and write contrast-report.md."""
    if extended is None:
        extended = {}
    resolved = resolve_color_aliases(color_tokens)

    pairs = [
        ("primary", "on-primary"),
        ("primary-container", "on-primary-container"),
        ("secondary", "on-secondary"),
        ("secondary-container", "on-secondary-container"),
        ("tertiary", "on-tertiary"),
        ("tertiary-container", "on-tertiary-container"),
        ("error", "on-error"),
        ("error-container", "on-error-container"),
        ("surface", "on-surface"),
        ("surface-variant", "on-surface-variant"),
    ]

    # Extended color pairs
    for ext_name in extended:
        pairs.append((ext_name, f"on-{ext_name}"))
        pairs.append((f"{ext_name}-container", f"on-{ext_name}-container"))

    rows = []
    failures = []
    for bg_role, fg_role in pairs:
        row = {"pair": f"{bg_role} / {fg_role}"}
        for mode in ("light", "dark"):
            bg = resolved[mode].get(bg_role, "#ffffff")
            fg = resolved[mode].get(fg_role, "#000000")
            try:
                ratio = contrast_ratio(bg, fg)
            except Exception:
                ratio = 0.0
            aa = "PASS" if ratio >= 4.5 else "FAIL"
            aaa = "PASS" if ratio >= 7.0 else "FAIL"
            row[f"{mode}_ratio"] = round(ratio, 2)
            row[f"{mode}_aa"] = aa
            row[f"{mode}_aaa"] = aaa
            if ratio < 4.5:
                failures.append(f"{mode}/{bg_role}/{fg_role} ({ratio:.2f}:1)")
        rows.append(row)

    lines = [
        "# WCAG Contrast Report\n",
        "| Pair | Light Ratio | Light AA | Light AAA | Dark Ratio | Dark AA | Dark AAA |",
        "|------|-------------|----------|-----------|------------|---------|----------|",
    ]
    for r in rows:
        lines.append(
            f"| {r['pair']} | {r['light_ratio']}:1 | {r['light_aa']} | {r['light_aaa']} "
            f"| {r['dark_ratio']}:1 | {r['dark_aa']} | {r['dark_aaa']} |"
        )

    lines.append("\n## Legend\n- AA: >= 4.5:1 (normal text) -- WCAG 2.1 AA required\n- AAA: >= 7.0:1 -- WCAG 2.1 AAA enhanced")

    if failures:
        lines.append("\n## Failures\nThe following pairs fail WCAG AA and should be adjusted:")
        for f in failures:
            lines.append(f"- {f}")
        print(f"WARNING: WCAG AA failures detected: {', '.join(failures)}")
        print("   Check contrast-report.md and consider adjusting tone values.")
    else:
        lines.append("\n## All pairs pass WCAG AA")

    path = os.path.join(output_dir, "contrast-report.md")
    with open(path, "w") as f:
        f.write("\n".join(lines) + "\n")


def build_design_brief(name: str, colors: dict, font_display: str, font_body: str,
                       corner_style: str, mood: str = "", rationale: str = "",
                       proportions: dict = None, extended: dict = None,
                       color_roles: dict = None) -> str:
    """Generate a design-brief.md for downstream skill consumption."""
    if proportions is None:
        proportions = {}
    if extended is None:
        extended = {}
    if color_roles is None:
        color_roles = {}

    primary = colors.get("primary", "")
    secondary = colors.get("secondary", "")
    tertiary = colors.get("tertiary", "")
    neutral = colors.get("neutral", "")
    error = colors.get("error", "#ba1a1a")

    corner_desc = {
        "sharp": "angular corners (small radii) -- structured, precise",
        "rounded": "rounded corners (medium radii) -- friendly, approachable",
        "organic": "large flowing corners -- soft, expressive",
    }.get(corner_style, corner_style)

    lines = [
        f"# Design Brief -- {name}",
        "",
        "## Source Image Analysis",
    ]
    if mood:
        lines.append(f"- Mood: {mood}")
    lines += [
        f"- Dominant Color: {primary} (primary role)",
        f"- Secondary Colors: {secondary}, {tertiary}",
        f"- Neutral: {neutral}",
        f"- Error base: {error}",
    ]
    if proportions:
        lines.append("")
        lines.append("## Painting Color Proportions")
        lines.append("Area coverage from the source painting (used to tint UI surfaces):")
        for role, pct in sorted(proportions.items(), key=lambda x: -x[1]):
            lines.append(f"- {role}: {pct:.0%}")

    # Extended painting colors section
    if extended:
        lines.append("")
        lines.append("## Extended Painting Colors")
        lines.append("")
        lines.append("Colors beyond M3's 3 primary/secondary/tertiary slots, each with a full tonal ramp")
        lines.append("and semantic roles (base, on-*, *-container, on-*-container).")
        lines.append("")
        lines.append("| Token Name | Hex | UI Role |")
        lines.append("|---|---|---|")
        for ext_name, ext_hex in extended.items():
            ui_role = color_roles.get(ext_name, "general accent")
            lines.append(f"| {ext_name} | {ext_hex} | {ui_role} |")

        lines.append("")
        lines.append("## Painting Color Usage Guide")
        lines.append("")
        lines.append("When building components, use extended colors to evoke specific aspects of the painting:")
        lines.append("")

        # Build usage guide from the actual extended colors and their roles
        warm_accents = []
        light_surfaces = []
        deep_accents = []
        general = []

        for ext_name in extended:
            role_desc = color_roles.get(ext_name, "")
            ext_hex = extended[ext_name]
            _, _, lightness = hex_to_hsl(ext_hex)

            if lightness > 70:
                light_surfaces.append(ext_name)
            elif lightness < 30:
                deep_accents.append(ext_name)
            elif any(kw in role_desc.lower() for kw in ["badge", "star", "highlight", "accent", "rating", "notification"]):
                warm_accents.append(ext_name)
            else:
                general.append(ext_name)

        if warm_accents:
            names = ", ".join(warm_accents)
            lines.append(f"- **Highlight moments** (badges, notifications, selected states): Use warm accent colors")
            lines.append(f"  like {names} that correspond to the painting's bright pops")
        if light_surfaces:
            names = ", ".join(light_surfaces)
            lines.append(f"- **Surface warmth** (card backgrounds, hero sections): Use light extended colors")
            lines.append(f"  like {names}-container for surfaces that should feel warm/inviting")
        if deep_accents:
            names = ", ".join(deep_accents)
            lines.append(f"- **Depth and grounding** (footers, sidebars, dark sections): Use deep extended colors")
            lines.append(f"  like {names} for areas that need visual weight")
        if general:
            names = ", ".join(general)
            lines.append(f"- **Thematic accents** (decorative elements, illustrations): Use {names}")
            lines.append(f"  for elements that should carry the painting's character")

        lines.append("- **Standard actions** (buttons, links, FABs): Use M3 primary/secondary/tertiary")
        lines.append("  for interactive elements that need to be clearly actionable")

    lines += [
        "",
        "## Typography Direction",
        f"- Display Font: {font_display} -- chosen to match the image mood",
        f"- Body Font: {font_body} -- complements the display face for readability",
        "",
        "## Shape Direction",
        f"- Corner Style: {corner_desc}",
        "",
        "## Design Intent",
    ]
    if rationale:
        lines.append(rationale)
    else:
        lines.append("Generated from visual reference. See source image for full context.")
    lines += [
        "",
        "## Token Files Generated",
        "- `color.tokens.json` -- reference tonal ramps + M3 semantic roles (light & dark)",
        "- `typography.tokens.json` -- M3 type scale with selected font pairing",
        "- `shape.tokens.json` -- corner radius tokens",
        "- `spacing.tokens.json` -- 4px base unit spacing scale",
        "- `manifest.json` -- token file manifest",
        "- `theme.css` -- CSS custom properties for direct web use",
        "- `tailwind.config.snippet.js` -- Tailwind theme extension",
        "- `contrast-report.md` -- WCAG contrast validation for all semantic color pairs",
    ]
    return "\n".join(lines) + "\n"


def build_css_variables(color_tokens: dict, typography_tokens: dict, theme_name: str) -> str:
    """Generate a CSS custom properties file for direct web use."""
    lines = [f"/* {theme_name} -- generated design tokens as CSS custom properties */\n"]

    # Resolve aliases to actual hex values from ref palette
    ref = color_tokens["color"]["ref"]

    def resolve_color(alias_str):
        """Resolve {color.ref.X.Y} to actual hex."""
        match = re.match(r'\{color\.ref\.([\w-]+)\.(\d+)\}', alias_str)
        if match:
            palette, tone = match.group(1), match.group(2)
            if palette in ref and tone in ref[palette]:
                return ref[palette][tone]["$value"]
        return alias_str

    # Light theme
    lines.append(":root {")
    for role, token in color_tokens["color"]["sys"]["light"].items():
        val = resolve_color(token["$value"])
        lines.append(f"  --md-sys-color-{role}: {val};")

    # Typography
    typo_ref = typography_tokens["typography"]["ref"]
    lines.append(f"\n  --md-sys-typescale-brand-font: '{typo_ref['typeface']['brand']['$value']}';")
    lines.append(f"  --md-sys-typescale-plain-font: '{typo_ref['typeface']['plain']['$value']}';")
    lines.append("}\n")

    # Dark theme
    lines.append("@media (prefers-color-scheme: dark) {\n  :root {")
    for role, token in color_tokens["color"]["sys"]["dark"].items():
        val = resolve_color(token["$value"])
        lines.append(f"    --md-sys-color-{role}: {val};")
    lines.append("  }\n}")

    return "\n".join(lines)


def build_tailwind_snippet(color_tokens: dict) -> str:
    """Generate a Tailwind CSS theme extension snippet."""
    ref = color_tokens["color"]["ref"]

    def resolve_color(alias_str):
        match = re.match(r'\{color\.ref\.([\w-]+)\.(\d+)\}', alias_str)
        if match:
            palette, tone = match.group(1), match.group(2)
            if palette in ref and tone in ref[palette]:
                return ref[palette][tone]["$value"]
        return alias_str

    lines = [
        "// Tailwind CSS theme extension -- paste into tailwind.config.js > theme.extend",
        "module.exports = {",
        "  theme: {",
        "    extend: {",
        "      colors: {",
    ]

    for role, token in color_tokens["color"]["sys"]["light"].items():
        val = resolve_color(token["$value"])
        js_key = role.replace("-", "_")
        lines.append(f"        '{role}': '{val}',")

    lines.extend([
        "      },",
        "    },",
        "  },",
        "};",
    ])
    return "\n".join(lines)


def build_palette_review_html(colors: dict, surfaces: dict, surfaces_dark: dict,
                              extended: dict, color_roles: dict, proportions: dict,
                              name: str, mood: str,
                              font_display: str, font_body: str,
                              color_tokens: dict = None) -> str:
    """Generate a visual palette review HTML page.

    This page shows all chosen colors as large swatches so non-designers
    can evaluate the palette before tokens are generated into components.
    It also flags potential issues like colors that are too similar.
    """
    # Collect colors for similarity analysis — M3 roles + extended only
    # (surface picks are intentionally similar to each other, so skip them)
    palette_colors = {}
    for role in ("primary", "secondary", "tertiary", "neutral", "error"):
        if role in colors:
            palette_colors[role] = colors[role]
    for ext_name, ext_hex in extended.items():
        palette_colors[ext_name] = ext_hex

    # Detect similar color pairs among M3 roles + extended colors
    warnings = []
    color_names = list(palette_colors.keys())
    for i in range(len(color_names)):
        for j in range(i + 1, len(color_names)):
            n1, n2 = color_names[i], color_names[j]
            h1, s1, l1 = hex_to_hsl(palette_colors[n1])
            h2, s2, l2 = hex_to_hsl(palette_colors[n2])
            hue_diff = min(abs(h1 - h2), 360 - abs(h1 - h2))
            dist = math.sqrt((hue_diff / 3.6) ** 2 + (s1 - s2) ** 2 + (l1 - l2) ** 2)
            if dist < 15:
                warnings.append(
                    f'<div class="warning"><strong>⚠ Very similar:</strong> '
                    f'<span class="swatch-inline" style="background:{palette_colors[n1]};"></span> '
                    f'{n1} ({palette_colors[n1]}) and '
                    f'<span class="swatch-inline" style="background:{palette_colors[n2]};"></span> '
                    f'{n2} ({palette_colors[n2]}) — '
                    f'these may look indistinguishable in the UI. Consider differentiating or merging.</div>'
                )

    # Check if surface bg is too close to a role color (confusing hierarchy)
    if "bg" in surfaces:
        for role in ("primary", "secondary", "tertiary"):
            if role in colors:
                h1, s1, l1 = hex_to_hsl(surfaces["bg"])
                h2, s2, l2 = hex_to_hsl(colors[role])
                hue_diff = min(abs(h1 - h2), 360 - abs(h1 - h2))
                dist = math.sqrt((hue_diff / 3.6) ** 2 + (s1 - s2) ** 2 + (l1 - l2) ** 2)
                if dist < 15:
                    warnings.append(
                        f'<div class="warning"><strong>⚠ Surface ≈ {role}:</strong> '
                        f'<span class="swatch-inline" style="background:{surfaces["bg"]};"></span> '
                        f'Page background ({surfaces["bg"]}) is very similar to '
                        f'<span class="swatch-inline" style="background:{colors[role]};"></span> '
                        f'{role} ({colors[role]}). '
                        f'Buttons and UI accents in {role} will blend into the background.</div>'
                    )

    # Detect overly saturated surface
    if "bg" in surfaces:
        _, bg_s, bg_l = hex_to_hsl(surfaces["bg"])
        if bg_s > 60 and bg_l > 40 and bg_l < 75:
            warnings.append(
                f'<div class="warning"><strong>⚠ Bold surface:</strong> '
                f'<span class="swatch-inline" style="background:{surfaces["bg"]};"></span> '
                f'The page background ({surfaces["bg"]}) is highly saturated (S={bg_s:.0f}%). '
                f'This will dominate the UI — consider desaturating or using it as accent instead.</div>'
            )

    warnings_html = "\n".join(warnings) if warnings else '<div class="ok">✓ No color similarity issues detected.</div>'

    # Build M3 role swatches
    role_swatches = ""
    for role in ("primary", "secondary", "tertiary", "neutral", "error"):
        if role in colors:
            h, s, l = hex_to_hsl(colors[role])
            role_swatches += (
                f'<div class="swatch-card">'
                f'<div class="swatch" style="background:{colors[role]};"></div>'
                f'<div class="swatch-label">{role}</div>'
                f'<div class="swatch-hex">{colors[role]}</div>'
                f'<div class="swatch-meta">H:{h:.0f} S:{s:.0f} L:{l:.0f}</div>'
                f'</div>\n'
            )

    # Surface swatches (light)
    surface_swatches = ""
    for srf_role in ("bg", "card", "text", "muted", "border"):
        if srf_role in surfaces:
            h, s, l = hex_to_hsl(surfaces[srf_role])
            text_col = "#fff" if l < 50 else "#000"
            surface_swatches += (
                f'<div class="swatch-card">'
                f'<div class="swatch" style="background:{surfaces[srf_role]};color:{text_col};">{srf_role}</div>'
                f'<div class="swatch-label">light {srf_role}</div>'
                f'<div class="swatch-hex">{surfaces[srf_role]}</div>'
                f'<div class="swatch-meta">H:{h:.0f} S:{s:.0f} L:{l:.0f}</div>'
                f'</div>\n'
            )

    # Surface swatches (dark)
    dark_surface_swatches = ""
    for srf_role in ("bg", "card", "text", "muted", "border"):
        if srf_role in surfaces_dark:
            h, s, l = hex_to_hsl(surfaces_dark[srf_role])
            text_col = "#fff" if l < 50 else "#000"
            dark_surface_swatches += (
                f'<div class="swatch-card">'
                f'<div class="swatch" style="background:{surfaces_dark[srf_role]};color:{text_col};">{srf_role}</div>'
                f'<div class="swatch-label">dark {srf_role}</div>'
                f'<div class="swatch-hex">{surfaces_dark[srf_role]}</div>'
                f'<div class="swatch-meta">H:{h:.0f} S:{s:.0f} L:{l:.0f}</div>'
                f'</div>\n'
            )

    # Extended color swatches
    ext_swatches = ""
    for ext_name, ext_hex in extended.items():
        h, s, l = hex_to_hsl(ext_hex)
        text_col = "#fff" if l < 50 else "#000"
        role_hint = color_roles.get(ext_name, "")
        ext_swatches += (
            f'<div class="swatch-card">'
            f'<div class="swatch" style="background:{ext_hex};color:{text_col};"></div>'
            f'<div class="swatch-label">{ext_name}</div>'
            f'<div class="swatch-hex">{ext_hex}</div>'
            f'<div class="swatch-meta">H:{h:.0f} S:{s:.0f} L:{l:.0f}</div>'
            + (f'<div class="swatch-role">{role_hint}</div>' if role_hint else '') +
            f'</div>\n'
        )

    # Simulated page preview — shows how surface + text + primary look together
    bg_color = surfaces.get("bg", "#ffffff")
    card_color = surfaces.get("card", "#f5f5f5")
    text_color = surfaces.get("text", "#1a1a1a")
    muted_color = surfaces.get("muted", "#666666")
    primary_color = colors.get("primary", "#5c5ea1")
    secondary_color = colors.get("secondary", "#888888")
    tertiary_color = colors.get("tertiary", "#888888")

    dark_bg = surfaces_dark.get("bg", "#121212")
    dark_card = surfaces_dark.get("card", "#1e1e1e")
    dark_text = surfaces_dark.get("text", "#e0e0e0")
    dark_muted = surfaces_dark.get("muted", "#999999")

    # Dark mode buttons use tone 80 from the tonal ramps (matching M3 dark system tokens)
    if color_tokens and "color" in color_tokens and "ref" in color_tokens["color"]:
        ref = color_tokens["color"]["ref"]
        dark_primary = ref.get("primary", {}).get("80", {}).get("$value", primary_color)
        dark_secondary = ref.get("secondary", {}).get("80", {}).get("$value", secondary_color)
        dark_tertiary = ref.get("tertiary", {}).get("80", {}).get("$value", tertiary_color)
    else:
        dark_primary = primary_color
        dark_secondary = secondary_color
        dark_tertiary = tertiary_color

    # Proportion bar
    proportion_html = ""
    if proportions:
        segs = []
        for role, pct in sorted(proportions.items(), key=lambda x: -x[1]):
            color = colors.get(role, "#888")
            w = pct * 100
            text_c = "#fff" if hex_to_hsl(color)[2] < 50 else "#000"
            segs.append(f'<div style="width:{w}%;background:{color};color:{text_c};">{role} {w:.0f}%</div>')
        proportion_html = (
            '<div class="section"><h2>Painting Proportions</h2>'
            '<div class="proportion-bar">' + "".join(segs) + '</div></div>'
        )

    title = name.replace("-", " ").title() if name else "Palette Review"

    return f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title} — Palette Review</title>
<link href="https://fonts.googleapis.com/css2?family={font_display.replace(" ", "+")}:wght@400;700&family={font_body.replace(" ", "+")}:wght@400;500&display=swap" rel="stylesheet">
<style>
  * {{ box-sizing: border-box; margin: 0; padding: 0; }}
  body {{ font-family: '{font_body}', system-ui, sans-serif; background: #f0f0f0; color: #1a1a1a; padding: 32px; }}
  h1 {{ font-family: '{font_display}', serif; font-size: 36px; margin-bottom: 8px; }}
  h2 {{ font-family: '{font_display}', serif; font-size: 22px; margin-bottom: 16px; color: #333; }}
  .subtitle {{ font-size: 16px; color: #666; margin-bottom: 32px; }}
  .container {{ max-width: 1000px; margin: 0 auto; }}
  .section {{ background: #fff; border-radius: 12px; padding: 24px; margin-bottom: 24px; box-shadow: 0 1px 3px rgba(0,0,0,0.1); }}
  .swatch-grid {{ display: grid; grid-template-columns: repeat(auto-fill, minmax(140px, 1fr)); gap: 16px; }}
  .swatch-card {{ text-align: center; }}
  .swatch {{ width: 100%; height: 80px; border-radius: 8px; display: flex; align-items: flex-end; justify-content: center; padding: 8px; font-size: 12px; font-weight: 500; box-shadow: 0 1px 4px rgba(0,0,0,0.15); }}
  .swatch-label {{ font-size: 13px; font-weight: 600; margin-top: 8px; text-transform: capitalize; }}
  .swatch-hex {{ font-size: 12px; color: #666; font-family: monospace; }}
  .swatch-meta {{ font-size: 10px; color: #999; }}
  .swatch-role {{ font-size: 11px; color: #888; font-style: italic; margin-top: 2px; }}
  .swatch-inline {{ display: inline-block; width: 16px; height: 16px; border-radius: 3px; vertical-align: middle; box-shadow: 0 0 0 1px rgba(0,0,0,0.15); }}
  .warning {{ background: #fff8e1; border-left: 4px solid #f9a825; padding: 12px 16px; margin-bottom: 8px; border-radius: 0 8px 8px 0; font-size: 14px; line-height: 1.5; }}
  .ok {{ background: #e8f5e9; border-left: 4px solid #4caf50; padding: 12px 16px; border-radius: 0 8px 8px 0; font-size: 14px; }}
  .preview-split {{ display: grid; grid-template-columns: 1fr 1fr; gap: 16px; }}
  .preview-frame {{ border-radius: 8px; padding: 24px; min-height: 200px; }}
  .preview-card {{ border-radius: 8px; padding: 16px; margin-top: 12px; }}
  .preview-btn {{ display: inline-block; padding: 8px 20px; border-radius: 20px; font-size: 13px; font-weight: 500; margin-top: 12px; border: none; }}
  .preview-chip {{ display: inline-block; padding: 4px 12px; border-radius: 16px; font-size: 12px; margin: 4px 4px 4px 0; }}
  .proportion-bar {{ display: flex; height: 40px; border-radius: 8px; overflow: hidden; font-size: 11px; font-weight: 500; }}
  .proportion-bar > div {{ display: flex; align-items: center; justify-content: center; min-width: 40px; }}
</style>
</head>
<body>
<div class="container">
<h1>{title}</h1>
<div class="subtitle">Palette review{' — ' + mood if mood else ''} &middot; Review colors before generating components</div>

<div class="section">
<h2>Analysis</h2>
{warnings_html}
</div>

{proportion_html}

<div class="section">
<h2>M3 Color Roles</h2>
<div class="swatch-grid">
{role_swatches}
</div>
</div>

<div class="section">
<h2>Light Mode Surfaces</h2>
<div class="swatch-grid">
{surface_swatches}
</div>
</div>

<div class="section">
<h2>Dark Mode Surfaces</h2>
<div class="swatch-grid">
{dark_surface_swatches}
</div>
</div>

{"<div class='section'><h2>Extended Painting Colors</h2><div class='swatch-grid'>" + ext_swatches + "</div></div>" if ext_swatches else ""}

<div class="section">
<h2>Simulated Page Preview</h2>
<p style="font-size:14px;color:#666;margin-bottom:16px;">How these colors feel as a UI. Left: light mode. Right: dark mode.</p>
<div class="preview-split">
  <div class="preview-frame" style="background:{bg_color};color:{text_color};">
    <div style="font-family:'{font_display}',serif;font-size:24px;margin-bottom:4px;">Light Mode</div>
    <div style="font-size:14px;color:{muted_color};margin-bottom:12px;">Page background is the painting's dominant color</div>
    <div class="preview-card" style="background:{card_color};box-shadow:0 2px 8px rgba(0,0,0,0.15);">
      <div style="font-weight:500;margin-bottom:4px;">Card Title</div>
      <div style="font-size:13px;color:{muted_color};">Supporting text on card surface</div>
      <div style="margin-top:12px;display:flex;gap:8px;flex-wrap:wrap;">
        <span class="preview-btn" style="background:{primary_color};color:#fff;">Primary</span>
        <span class="preview-btn" style="background:{secondary_color};color:#fff;">Secondary</span>
        <span class="preview-btn" style="background:{tertiary_color};color:#fff;">Tertiary</span>
      </div>
      <div style="margin-top:8px;display:flex;flex-wrap:wrap;">
        ''' + "".join(
            f'<span class="preview-chip" style="background:{ext_hex};color:{"#fff" if hex_to_hsl(ext_hex)[2] < 50 else "#000"};">{ext_name.replace("-"," ").title()}</span>'
            for ext_name, ext_hex in extended.items()
        ) + f'''
      </div>
    </div>
  </div>
  <div class="preview-frame" style="background:{dark_bg};color:{dark_text};">
    <div style="font-family:'{font_display}',serif;font-size:24px;margin-bottom:4px;">Dark Mode</div>
    <div style="font-size:14px;color:{dark_muted};margin-bottom:12px;">Deep shadows from the painting</div>
    <div class="preview-card" style="background:{dark_card};box-shadow:0 2px 8px rgba(0,0,0,0.3);">
      <div style="font-weight:500;margin-bottom:4px;">Card Title</div>
      <div style="font-size:13px;color:{dark_muted};">Supporting text on card surface</div>
      <div style="margin-top:12px;display:flex;gap:8px;flex-wrap:wrap;">
        <span class="preview-btn" style="background:{dark_primary};color:#000;">Primary</span>
        <span class="preview-btn" style="background:{dark_secondary};color:#000;">Secondary</span>
        <span class="preview-btn" style="background:{dark_tertiary};color:#000;">Tertiary</span>
      </div>
    </div>
  </div>
</div>
</div>

<div style="text-align:center;margin-top:24px;padding:16px;color:#999;font-size:13px;">
  Review these colors and the simulated preview. Ask for adjustments before proceeding to component generation.
</div>
</div>
</body>
</html>'''


def main():
    parser = argparse.ArgumentParser(description="Generate DTCG design tokens (Expressive Painting)")
    parser.add_argument("--colors", required=True, help='JSON object: {"primary":"#hex","secondary":"#hex","tertiary":"#hex","neutral":"#hex","error":"#hex"}')
    parser.add_argument("--font-display", required=True, help="Display/heading font family name")
    parser.add_argument("--font-body", required=True, help="Body/text font family name")
    parser.add_argument("--corner-style", default="rounded", choices=["sharp", "rounded", "organic"], help="Corner radius philosophy")
    parser.add_argument("--name", default="custom-theme", help="Theme name for file headers")
    parser.add_argument("--output-dir", default="./tokens-output", help="Output directory")
    parser.add_argument("--mood", default="", help="Mood description from image analysis (e.g. 'serene, cool')")
    parser.add_argument("--rationale", default="", help="1-2 sentence design intent for design-brief.md")
    parser.add_argument("--no-css", action="store_true", help="Skip writing theme.css")
    parser.add_argument("--no-tailwind", action="store_true", help="Skip writing tailwind.config.snippet.js")
    parser.add_argument("--proportions", default="", help='JSON object with color area proportions from the painting, e.g. {"primary":0.55,"secondary":0.25,"tertiary":0.10,"neutral":0.05,"accent":0.05}. Used to tint surfaces and preserve the painting\'s color balance.')
    parser.add_argument("--surfaces", default="", help='JSON object with hex colors picked directly from the painting for surface roles: {"bg":"#hexval","card":"#hexval","text":"#hexval","muted":"#hexval","border":"#hexval"}. These override computed surface tokens for light theme.')
    parser.add_argument("--surfaces-dark", default="", help='JSON object with hex colors picked from the painting\'s dark areas for dark mode surface roles: {"bg":"#hexval","card":"#hexval","text":"#hexval","muted":"#hexval","border":"#hexval"}. Same structure as --surfaces but overrides dark theme tokens.')
    parser.add_argument("--extended", default="", help='JSON object of extended color tokens beyond M3 primary/secondary/tertiary, e.g. {"wheat-gold":"#c8a830","cloud-cream":"#f0ece0"}. Each gets a tonal ramp in ref and semantic roles (base, on-*, *-container, on-*-container) in sys.light/dark.')
    parser.add_argument("--color-roles", default="", help='JSON object mapping extended color names to their suggested UI usage, e.g. {"wheat-gold":"badges, star ratings","cloud-cream":"warm card surfaces"}. Included in the design brief.')
    parser.add_argument("--review-dir", default=None, help="Directory for review files (contrast-report.md, design-brief.md, palette-review.html). Defaults to --output-dir when not provided.")

    args = parser.parse_args()

    # Resolve review directory: use --review-dir if provided, otherwise fall back to --output-dir
    review_dir = args.review_dir if args.review_dir else args.output_dir
    os.makedirs(review_dir, exist_ok=True)
    colors = json.loads(args.colors)
    proportions = json.loads(args.proportions) if args.proportions else {}
    surfaces = json.loads(args.surfaces) if args.surfaces else {}
    surfaces_dark = json.loads(args.surfaces_dark) if args.surfaces_dark else {}
    extended = json.loads(args.extended) if args.extended else {}
    color_roles = json.loads(args.color_roles) if args.color_roles else {}

    # Filter out extended colors that are too similar to M3 roles (distance < 15)
    if extended:
        extended, color_roles = filter_extended_by_m3_similarity(
            extended, colors, color_roles, threshold=15
        )

    os.makedirs(args.output_dir, exist_ok=True)

    # Generate all token files
    color_tokens = build_color_tokens(colors, proportions, surfaces, extended, surfaces_dark, color_roles)
    typography_tokens = build_typography_tokens(args.font_display, args.font_body)
    shape_tokens = build_shape_tokens(args.corner_style)
    spacing_tokens = build_spacing_tokens()

    # Write DTCG JSON files
    with open(os.path.join(args.output_dir, "color.tokens.json"), "w") as f:
        json.dump(color_tokens, f, indent=2)

    with open(os.path.join(args.output_dir, "typography.tokens.json"), "w") as f:
        json.dump(typography_tokens, f, indent=2)

    with open(os.path.join(args.output_dir, "shape.tokens.json"), "w") as f:
        json.dump(shape_tokens, f, indent=2)

    with open(os.path.join(args.output_dir, "spacing.tokens.json"), "w") as f:
        json.dump(spacing_tokens, f, indent=2)

    # Write manifest
    manifest = {
        "$schema": "https://designtokens.org/schemas/manifest.json",
        "$description": f"Design tokens for {args.name}",
        "sources": [
            {"path": "color.tokens.json"},
            {"path": "typography.tokens.json"},
            {"path": "shape.tokens.json"},
            {"path": "spacing.tokens.json"}
        ]
    }
    with open(os.path.join(args.output_dir, "manifest.json"), "w") as f:
        json.dump(manifest, f, indent=2)

    # Write CSS variables (default on; skip with --no-css)
    if not args.no_css:
        css = build_css_variables(color_tokens, typography_tokens, args.name)
        with open(os.path.join(args.output_dir, "theme.css"), "w") as f:
            f.write(css)

    # Write Tailwind snippet (default on; skip with --no-tailwind)
    if not args.no_tailwind:
        tw = build_tailwind_snippet(color_tokens)
        with open(os.path.join(args.output_dir, "tailwind.config.snippet.js"), "w") as f:
            f.write(tw)

    # Write WCAG contrast report
    write_contrast_report(color_tokens, review_dir, extended)

    # Write design-brief.md
    brief = build_design_brief(
        name=args.name,
        colors=colors,
        font_display=args.font_display,
        font_body=args.font_body,
        corner_style=args.corner_style,
        mood=args.mood,
        rationale=args.rationale,
        proportions=proportions,
        extended=extended,
        color_roles=color_roles,
    )
    with open(os.path.join(review_dir, "design-brief.md"), "w") as f:
        f.write(brief)

    # Write palette review HTML
    review_html = build_palette_review_html(
        colors=colors, surfaces=surfaces, surfaces_dark=surfaces_dark,
        extended=extended, color_roles=color_roles, proportions=proportions,
        name=args.name, mood=args.mood,
        font_display=args.font_display, font_body=args.font_body,
        color_tokens=color_tokens,
    )
    with open(os.path.join(review_dir, "palette-review.html"), "w") as f:
        f.write(review_html)

    print(f"Generated {len(os.listdir(args.output_dir))} files in {args.output_dir}/")
    for fname in sorted(os.listdir(args.output_dir)):
        fpath = os.path.join(args.output_dir, fname)
        size = os.path.getsize(fpath)
        print(f"  {fname} ({size:,} bytes)")


if __name__ == "__main__":
    main()
