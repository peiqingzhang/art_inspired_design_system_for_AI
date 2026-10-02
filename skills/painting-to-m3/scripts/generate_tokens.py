#!/usr/bin/env python3
"""
Generate strict Material Design 3 compliant DTCG design token files from 3 maximally-distinct
painting colors. Strict M3 token generator — picks 3 maximally-distinct colors for
primary/secondary/tertiary slots.

Usage:
    python generate_tokens.py \
        --colors '{"primary":"#5c5ea1","secondary":"#8b6e4e","tertiary":"#4e8b6e","neutral":"#7a7a78","error":"#ba1a1a"}' \
        --considered-colors '{"wheat-gold":{"hex":"#c8a830","area":0.08,"note":"warm accent in foreground"}}' \
        --font-display "Cormorant Garamond" \
        --font-body "Source Serif 4" \
        --corner-style rounded \
        --name "monet-waterlilies" \
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
        # Hue-aware: yellows (H=30-90) need ~2x more darkening than blues
        actual_l = tone
        if tone == 30 and s > 20 and 30 <= h <= 90:
            actual_l = 30 - (s - 20) * 0.10
        elif tone == 40 and s > 20:
            hue_factor = 1.0
            if 30 <= h <= 90:
                hue_factor = 1.8
            elif 90 < h <= 150:
                hue_factor = 1.3
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


def build_color_tokens(colors: dict, considered_colors: dict = None) -> dict:
    """Build the complete color.tokens.json structure.

    Strict M3 compliance: neutral ramps use standard low saturation from the
    primary hue. No surface overrides, no extended colors, no proportion-based
    tinting. Surfaces map tone directly to lightness — tone 98 = near-white.
    """
    if considered_colors is None:
        considered_colors = {}

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

    # Standard M3 neutral ramps: low saturation from primary hue
    neutral_ramp = generate_neutral_ramp(primary_hex, 10)
    neutral_variant_ramp = generate_neutral_ramp(primary_hex, 18)

    ref = {
        "$description": "Reference palette — tonal scales derived from source image",
        "primary": generate_tonal_ramp(primary_hex),
        "secondary": generate_tonal_ramp(secondary_hex),
        "tertiary": generate_tonal_ramp(tertiary_hex),
        "neutral": neutral_ramp,
        "neutral-variant": neutral_variant_ramp,
        "error": generate_tonal_ramp(error_hex)
    }

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
            "$description": "Typography tokens — M3 type scale with custom font pairing",
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
            "$description": f"Shape tokens — {corner_style} corner style derived from visual mood",
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
    """Build spacing.tokens.json — standard 4px base unit scale."""
    return {
        "spacing": {
            "$description": "Spacing tokens — 4px base unit",
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


# ── Contrast guard ──────────────────────────────────────────────────────────
# Tonal ramps alone don't guarantee contrast once painting-picked surfaces are
# mixed in (e.g. a mid-tone red page with pale M3 panels). This pass checks the
# pairs components actually render and nudges HSL lightness -- keeping hue and
# saturation -- until each pair reaches WCAG AA (4.5:1).

WCAG_AA = 4.5

# Backgrounds that carry on-surface / on-surface-variant text in the components
TEXT_HOSTS = [
    "surface",
    "surface-variant",
    "surface-container-lowest",
    "surface-container-low",
    "surface-container",
    "surface-container-high",
    "surface-container-highest",
]

# Extra pairs reported on top of the role / on-role pairs
EXTRA_REPORT_PAIRS = [
    ("surface", "on-surface-variant"),
    ("surface", "primary"),
    ("surface-container-lowest", "on-surface"),
    ("surface-container-lowest", "on-surface-variant"),
    ("surface-container-highest", "on-surface"),
    ("surface-container-highest", "on-surface-variant"),
]


def _push_lightness(hex_color: str, against: list, direction: int,
                    target: float = WCAG_AA, hue_sat: tuple = None):
    """Move hex_color's HSL lightness in `direction` (+1 lighter, -1 darker) until it
    reaches `target` contrast against every color in `against`. Returns the new hex,
    or None if even pure white/black isn't enough. `hue_sat` overrides the hue and
    saturation used while moving (handy for tinting pure white/black)."""
    h, s, l = hex_to_hsl(hex_color)
    if hue_sat:
        h, s = hue_sat
    step = 0.5
    cur = l
    while 0 <= cur <= 100:
        candidate = hsl_to_hex(h, s, cur)
        if all(contrast_ratio(candidate, a) >= target for a in against):
            return candidate
        cur += step * direction
    return None


def _direction_away(color: str, reference: str) -> int:
    """+1 if color is lighter than reference (keep going lighter), else -1."""
    return 1 if relative_luminance(color) >= relative_luminance(reference) else -1


def _fix_foreground(fg: str, against: list, prefer: int, target: float = WCAG_AA):
    """Fix a text/foreground color against backgrounds, trying `prefer` first."""
    if all(contrast_ratio(fg, a) >= target for a in against):
        return fg
    for direction in (prefer, -prefer):
        fixed = _push_lightness(fg, against, direction, target)
        if fixed:
            return fixed
    return None


def enforce_contrast(color_tokens: dict, painting_surfaces: bool = False) -> list:
    """Adjust sys tokens in place so every rendered text pair passes WCAG AA.

    Order matters -- foregrounds move before backgrounds so the painting's
    surfaces are preserved whenever possible:
      0. (painting surfaces only) if surface-variant fights its text, re-derive it
         from the painting background (surface-variant := surface-container-highest,
         as in current M3) instead of the generic pale/dark M3 tone
      1. on-surface / on-surface-variant vs every text host; if a host can't be
         satisfied by moving text alone, the host's lightness is moved instead
      2. primary vs surface (primary is used as text: text buttons, active tabs,
         focused labels, links), then on-primary vs primary
      3. every role / on-role pair, including extended painting colors

    Returns a list of human-readable change descriptions.
    """
    resolved = resolve_color_aliases(color_tokens)
    changes = []

    for mode in ("light", "dark"):
        sys_tokens = color_tokens["color"]["sys"][mode]
        vals = dict(resolved[mode])
        original = dict(vals)

        def ratio(a, b):
            return contrast_ratio(vals[a], vals[b])

        # 0. surface-variant from the painting's own background, but only when
        #    no muted-text color could work on both the page and the panel
        #    (e.g. pale text on a red page vs. a pale generated panel)
        if (painting_surfaces
                and not sys_tokens["surface"]["$value"].startswith("{")
                and ratio("surface-variant", "on-surface-variant") < WCAG_AA):
            side = _direction_away(vals["on-surface"], vals["surface"])
            if _push_lightness(vals["on-surface-variant"],
                               [vals["surface"], vals["surface-variant"]], side) is None:
                vals["surface-variant"] = vals["surface-container-highest"]

        # 1. text on surfaces
        hosts = [r for r in TEXT_HOSTS if r in vals]
        polarity = _direction_away(vals["on-surface"], vals["surface"])
        for fg in ("on-surface", "on-surface-variant"):
            # must pass on the page itself
            fixed = _fix_foreground(vals[fg], [vals["surface"]], polarity)
            vals[fg] = fixed or ("#ffffff" if polarity > 0 else "#000000")
            polarity = _direction_away(vals["on-surface"], vals["surface"])
            # then try to pass on every host by moving the text only
            fixed = _push_lightness(vals[fg], [vals[h] for h in hosts], polarity) \
                if any(ratio(h, fg) < WCAG_AA for h in hosts) else vals[fg]
            if fixed:
                vals[fg] = fixed
        # hosts that text alone couldn't satisfy: move the host away from the text
        texts = [vals["on-surface"], vals["on-surface-variant"]]
        for host in hosts:
            if host == "surface":
                continue
            if min(contrast_ratio(vals[host], t) for t in texts) < WCAG_AA:
                fixed = _push_lightness(vals[host], texts, -polarity)
                if fixed:
                    vals[host] = fixed

        # 2. primary as text on the page, then its on-color
        if "primary" in vals:
            prefer = _direction_away(vals["primary"], vals["surface"])
            fixed = _fix_foreground(vals["primary"], [vals["surface"]], prefer)
            if fixed:
                vals["primary"] = fixed

        # 3. role / on-role pairs
        for role in list(vals):
            on_role = f"on-{role}"
            if role.startswith("on-") or on_role not in vals:
                continue
            if ratio(role, on_role) >= WCAG_AA:
                continue
            prefer = _direction_away(vals[on_role], vals[role])
            hue_sat = None
            if hex_to_hsl(vals[on_role])[1] < 5:
                # white/black on-colors would turn gray when nudged -- tint them
                # with the role's own hue instead (like an M3 tone 10/100 pair)
                rh, rs, _ = hex_to_hsl(vals[role])
                hue_sat = (rh, rs * 0.6)
            # a) push the on-color further in its own direction
            fixed = _push_lightness(vals[on_role], [vals[role]], prefer, hue_sat=hue_sat)
            if fixed:
                vals[on_role] = fixed
                continue
            # b) move the role color away from its on-color (keeps white-on-color
            #    buttons); primary must also keep passing on the page (step 2)
            keep = [vals[on_role]] + ([vals["surface"]] if role == "primary" else [])
            fixed = _push_lightness(vals[role], keep, -prefer)
            if fixed:
                vals[role] = fixed
                continue
            # c) last resort: flip the on-color to the other side
            fixed = _push_lightness(vals[on_role], [vals[role]], -prefer, hue_sat=hue_sat)
            if fixed:
                vals[on_role] = fixed

        for role, new_hex in vals.items():
            if new_hex.lower() != original[role].lower():
                sys_tokens[role] = {"$value": new_hex, "$type": "color"}
                before = original[role]
                changes.append(f"{mode}/{role}: {before} -> {new_hex}")

    return changes


def write_contrast_report(color_tokens: dict, output_dir: str):
    """Check WCAG contrast for standard M3 semantic color pairs and write contrast-report.md."""
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
    pairs += EXTRA_REPORT_PAIRS

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
            aa = "pass" if ratio >= 4.5 else "FAIL"
            aaa = "pass" if ratio >= 7.0 else "---"
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

    lines.append("\n## Legend\n- AA: >= 4.5:1 (normal text) — WCAG 2.1 AA required\n- AAA: >= 7.0:1 — WCAG 2.1 AAA enhanced")

    if failures:
        lines.append("\n## Failures\nThe following pairs fail WCAG AA and should be adjusted:")
        for f in failures:
            lines.append(f"- {f}")
        print(f"WCAG AA failures detected: {', '.join(failures)}")
        print("   Check contrast-report.md and consider adjusting tone values.")
    else:
        lines.append("\n## All pairs pass WCAG AA")

    path = os.path.join(output_dir, "contrast-report.md")
    with open(path, "w") as f:
        f.write("\n".join(lines) + "\n")


def build_design_brief(name: str, colors: dict, font_display: str, font_body: str,
                       corner_style: str, mood: str = "", rationale: str = "",
                       considered_colors: dict = None) -> str:
    """Generate a design-brief.md for downstream skill consumption.

    The considered_colors dict documents painting colors that were identified but
    not assigned to M3 primary/secondary/tertiary slots.
    """
    if considered_colors is None:
        considered_colors = {}
    primary = colors.get("primary", "")
    secondary = colors.get("secondary", "")
    tertiary = colors.get("tertiary", "")
    neutral = colors.get("neutral", "")
    error = colors.get("error", "#ba1a1a")

    corner_desc = {
        "sharp": "angular corners (small radii) — structured, precise",
        "rounded": "rounded corners (medium radii) — friendly, approachable",
        "organic": "large flowing corners — soft, expressive",
    }.get(corner_style, corner_style)

    lines = [
        f"# Design Brief — {name}",
        "",
        "## Source Image Analysis",
    ]
    if mood:
        lines.append(f"- Mood: {mood}")
    lines += [
        f"- Primary: {primary}",
        f"- Secondary: {secondary}",
        f"- Tertiary: {tertiary}",
        f"- Neutral: {neutral}",
        f"- Error base: {error}",
    ]

    if considered_colors:
        lines.append("")
        lines.append("## Considered Colors (not assigned to M3 slots)")
        lines.append("")
        lines.append("These painting colors were identified but did not receive a primary/secondary/tertiary role.")
        lines.append("Use the `painting-to-theme` skill for a richer palette that includes these colors.")
        lines.append("")
        for cname, cinfo in considered_colors.items():
            chex = cinfo.get("hex", "")
            carea = cinfo.get("area", 0)
            cnote = cinfo.get("note", "")
            area_pct = f"{carea:.0%}" if carea else "?"
            lines.append(f"- {cname} ({chex}) — {area_pct} area — {cnote}")

    lines.append("")
    lines.append("## Selection Rationale")
    if rationale:
        lines.append(rationale)
    else:
        lines.append("3 maximally-distinct colors selected from the painting for strict M3 compliance.")
        lines.append("Colors were chosen to maximize hue separation, visual significance, and temperature contrast.")

    lines += [
        "",
        "## Typography Direction",
        f"- Display Font: {font_display} — chosen to match the image mood",
        f"- Body Font: {font_body} — complements the display face for readability",
        "",
        "## Shape Direction",
        f"- Corner Style: {corner_desc}",
        "",
        "## Design Intent",
        "Strict Material Design 3 token set. Surfaces use standard near-white tones",
        "derived from the primary hue at low saturation. Compatible with any M3-consuming",
        "framework (MUI, Jetpack Compose, Flutter).",
        "",
        "## Token Files Generated",
        "- `color.tokens.json` — reference tonal ramps + M3 semantic roles (light & dark)",
        "- `typography.tokens.json` — M3 type scale with selected font pairing",
        "- `shape.tokens.json` — corner radius tokens",
        "- `spacing.tokens.json` — 4px base unit spacing scale",
        "- `manifest.json` — token file manifest",
        "- `theme.css` — CSS custom properties for direct web use",
        "- `tailwind.config.snippet.js` — Tailwind theme extension",
        "- `contrast-report.md` — WCAG contrast validation for standard M3 color pairs",
    ]
    return "\n".join(lines) + "\n"


def build_palette_review_html(color_tokens: dict, colors: dict,
                              considered_colors: dict, name: str,
                              mood: str, font_display: str, font_body: str) -> str:
    """Generate a visual palette review HTML page for strict M3 tokens.

    Shows M3 color role swatches, light/dark surfaces resolved from tonal ramps,
    a simulated page preview, considered (but unassigned) painting colors, and
    analysis warnings for colors that are too similar.
    """
    resolved = resolve_color_aliases(color_tokens)
    ref = color_tokens["color"]["ref"]

    # --- Analysis: detect similar color pairs among M3 roles ---
    palette_colors = {}
    for role in ("primary", "secondary", "tertiary", "neutral", "error"):
        if role in colors:
            palette_colors[role] = colors[role]

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
                    f'<div class="warning"><strong>Warning — Very similar:</strong> '
                    f'<span class="swatch-inline" style="background:{palette_colors[n1]};"></span> '
                    f'{n1} ({palette_colors[n1]}) and '
                    f'<span class="swatch-inline" style="background:{palette_colors[n2]};"></span> '
                    f'{n2} ({palette_colors[n2]}) — '
                    f'these may look indistinguishable in the UI. Consider differentiating or merging.</div>'
                )

    # Check if surface bg is too close to a role color
    light_surface = resolved["light"].get("surface", "#ffffff")
    for role in ("primary", "secondary", "tertiary"):
        if role in colors:
            h1, s1, l1 = hex_to_hsl(light_surface)
            h2, s2, l2 = hex_to_hsl(colors[role])
            hue_diff = min(abs(h1 - h2), 360 - abs(h1 - h2))
            dist = math.sqrt((hue_diff / 3.6) ** 2 + (s1 - s2) ** 2 + (l1 - l2) ** 2)
            if dist < 15:
                warnings.append(
                    f'<div class="warning"><strong>Warning — Surface approx {role}:</strong> '
                    f'<span class="swatch-inline" style="background:{light_surface};"></span> '
                    f'Page surface ({light_surface}) is very similar to '
                    f'<span class="swatch-inline" style="background:{colors[role]};"></span> '
                    f'{role} ({colors[role]}). '
                    f'Buttons and UI accents in {role} will blend into the background.</div>'
                )

    warnings_html = "\n".join(warnings) if warnings else '<div class="ok">No color similarity issues detected.</div>'

    # --- M3 role swatches ---
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

    # --- Light mode surface swatches (from resolved M3 tokens) ---
    light_surface_roles = [
        ("surface", "Surface"), ("surface-variant", "Surface Variant"),
        ("surface-container-lowest", "Container Lowest"), ("surface-container-low", "Container Low"),
        ("surface-container", "Container"), ("surface-container-high", "Container High"),
        ("surface-container-highest", "Container Highest"),
        ("on-surface", "On Surface"), ("on-surface-variant", "On Srf Variant"),
        ("outline", "Outline"), ("outline-variant", "Outline Variant"),
    ]
    light_surface_swatches = ""
    for token_name, display_name in light_surface_roles:
        hex_val = resolved["light"].get(token_name, "#888888")
        h, s, l = hex_to_hsl(hex_val)
        text_col = "#fff" if l < 50 else "#000"
        light_surface_swatches += (
            f'<div class="swatch-card">'
            f'<div class="swatch" style="background:{hex_val};color:{text_col};">{display_name}</div>'
            f'<div class="swatch-label">{token_name}</div>'
            f'<div class="swatch-hex">{hex_val}</div>'
            f'<div class="swatch-meta">H:{h:.0f} S:{s:.0f} L:{l:.0f}</div>'
            f'</div>\n'
        )

    # --- Dark mode surface swatches ---
    dark_surface_swatches = ""
    for token_name, display_name in light_surface_roles:
        hex_val = resolved["dark"].get(token_name, "#888888")
        h, s, l = hex_to_hsl(hex_val)
        text_col = "#fff" if l < 50 else "#000"
        dark_surface_swatches += (
            f'<div class="swatch-card">'
            f'<div class="swatch" style="background:{hex_val};color:{text_col};">{display_name}</div>'
            f'<div class="swatch-label">{token_name}</div>'
            f'<div class="swatch-hex">{hex_val}</div>'
            f'<div class="swatch-meta">H:{h:.0f} S:{s:.0f} L:{l:.0f}</div>'
            f'</div>\n'
        )

    # --- Considered colors (identified but not assigned to M3 slots) ---
    considered_html = ""
    if considered_colors:
        considered_swatches = ""
        for cname, cinfo in considered_colors.items():
            chex = cinfo.get("hex", "#888888")
            carea = cinfo.get("area", 0)
            cnote = cinfo.get("note", "")
            h, s, l = hex_to_hsl(chex)
            text_col = "#fff" if l < 50 else "#000"
            area_str = f"{carea:.0%}" if carea else "?"
            considered_swatches += (
                f'<div class="swatch-card">'
                f'<div class="swatch" style="background:{chex};color:{text_col};"></div>'
                f'<div class="swatch-label">{cname}</div>'
                f'<div class="swatch-hex">{chex}</div>'
                f'<div class="swatch-meta">H:{h:.0f} S:{s:.0f} L:{l:.0f} | {area_str} area</div>'
                + (f'<div class="swatch-role">{cnote}</div>' if cnote else '') +
                f'</div>\n'
            )
        considered_html = (
            '<div class="section"><h2>Considered Colors (not assigned to M3 slots)</h2>'
            '<p style="font-size:14px;color:#666;margin-bottom:16px;">These painting colors were identified but did not receive a primary/secondary/tertiary role. '
            'Use the painting-to-theme skill for a richer palette that includes these colors.</p>'
            '<div class="swatch-grid">' + considered_swatches + '</div></div>'
        )

    # --- Simulated page preview ---
    bg_color = resolved["light"].get("surface", "#ffffff")
    card_color = resolved["light"].get("surface-container-low", "#f5f5f5")
    text_color = resolved["light"].get("on-surface", "#1a1a1a")
    muted_color = resolved["light"].get("on-surface-variant", "#666666")
    primary_color = resolved["light"].get("primary", "#5c5ea1")
    secondary_color = resolved["light"].get("secondary", "#888888")
    tertiary_color = resolved["light"].get("tertiary", "#888888")

    dark_bg = resolved["dark"].get("surface", "#121212")
    dark_card = resolved["dark"].get("surface-container-low", "#1e1e1e")
    dark_text = resolved["dark"].get("on-surface", "#e0e0e0")
    dark_muted = resolved["dark"].get("on-surface-variant", "#999999")
    dark_primary = resolved["dark"].get("primary", primary_color)
    dark_secondary = resolved["dark"].get("secondary", secondary_color)
    dark_tertiary = resolved["dark"].get("tertiary", tertiary_color)

    title = name.replace("-", " ").title() if name else "Palette Review"

    return f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title} — M3 Palette Review</title>
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
</style>
</head>
<body>
<div class="container">
<h1>{title}</h1>
<div class="subtitle">M3 Palette Review{' — ' + mood if mood else ''} &middot; Strict Material Design 3 &middot; Review colors before generating components</div>

<div class="section">
<h2>Analysis</h2>
{warnings_html}
</div>

<div class="section">
<h2>M3 Color Roles</h2>
<div class="swatch-grid">
{role_swatches}
</div>
</div>

<div class="section">
<h2>Light Mode Surfaces</h2>
<div class="swatch-grid">
{light_surface_swatches}
</div>
</div>

<div class="section">
<h2>Dark Mode Surfaces</h2>
<div class="swatch-grid">
{dark_surface_swatches}
</div>
</div>

{considered_html}

<div class="section">
<h2>Simulated Page Preview</h2>
<p style="font-size:14px;color:#666;margin-bottom:16px;">How these colors feel as a UI. Left: light mode. Right: dark mode.</p>
<div class="preview-split">
  <div class="preview-frame" style="background:{bg_color};color:{text_color};">
    <div style="font-family:'{font_display}',serif;font-size:24px;margin-bottom:4px;">Light Mode</div>
    <div style="font-size:14px;color:{muted_color};margin-bottom:12px;">Standard M3 surface from primary hue</div>
    <div class="preview-card" style="background:{card_color};box-shadow:0 2px 8px rgba(0,0,0,0.15);">
      <div style="font-weight:500;margin-bottom:4px;">Card Title</div>
      <div style="font-size:13px;color:{muted_color};">Supporting text on card surface</div>
      <div style="margin-top:12px;display:flex;gap:8px;flex-wrap:wrap;">
        <span class="preview-btn" style="background:{primary_color};color:#fff;">Primary</span>
        <span class="preview-btn" style="background:{secondary_color};color:#fff;">Secondary</span>
        <span class="preview-btn" style="background:{tertiary_color};color:#fff;">Tertiary</span>
      </div>
    </div>
  </div>
  <div class="preview-frame" style="background:{dark_bg};color:{dark_text};">
    <div style="font-family:'{font_display}',serif;font-size:24px;margin-bottom:4px;">Dark Mode</div>
    <div style="font-size:14px;color:{dark_muted};margin-bottom:12px;">M3 dark surface tones</div>
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


def build_css_variables(color_tokens: dict, typography_tokens: dict, theme_name: str) -> str:
    """Generate a CSS custom properties file for direct web use."""
    lines = [f"/* {theme_name} — generated design tokens as CSS custom properties */\n"]

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
        "// Tailwind CSS theme extension — paste into tailwind.config.js > theme.extend",
        "module.exports = {",
        "  theme: {",
        "    extend: {",
        "      colors: {",
    ]

    for role, token in color_tokens["color"]["sys"]["light"].items():
        val = resolve_color(token["$value"])
        lines.append(f"        '{role}': '{val}',")

    lines.extend([
        "      },",
        "    },",
        "  },",
        "};",
    ])
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="Generate strict M3 DTCG design tokens")
    parser.add_argument("--colors", required=True, help='JSON object: {"primary":"#hex","secondary":"#hex","tertiary":"#hex","neutral":"#hex","error":"#hex"}')
    parser.add_argument("--considered-colors", default="", help='JSON object of painting colors not assigned to M3 slots: {"name":{"hex":"#hexval","area":0.08,"note":"description"}}')
    parser.add_argument("--font-display", required=True, help="Display/heading font family name")
    parser.add_argument("--font-body", required=True, help="Body/text font family name")
    parser.add_argument("--corner-style", default="rounded", choices=["sharp", "rounded", "organic"], help="Corner radius philosophy")
    parser.add_argument("--name", default="custom-theme", help="Theme name for file headers")
    parser.add_argument("--output-dir", default="./tokens-output", help="Output directory")
    parser.add_argument("--mood", default="", help="Mood description from image analysis (e.g. 'serene, cool')")
    parser.add_argument("--rationale", default="", help="1-2 sentence selection rationale for why these 3 colors were chosen")
    parser.add_argument("--no-css", action="store_true", help="Skip writing theme.css")
    parser.add_argument("--no-tailwind", action="store_true", help="Skip writing tailwind.config.snippet.js")
    parser.add_argument("--review-dir", default=None, help="Directory for review files (contrast-report.md, design-brief.md, palette-review.html). Defaults to --output-dir.")

    args = parser.parse_args()
    colors = json.loads(args.colors)
    considered_colors = json.loads(args.considered_colors) if args.considered_colors else {}

    os.makedirs(args.output_dir, exist_ok=True)
    review_dir = args.review_dir if args.review_dir else args.output_dir
    if args.review_dir:
        os.makedirs(review_dir, exist_ok=True)

    # Generate all token files
    color_tokens = build_color_tokens(colors, considered_colors)
    # Nudge any near-miss pairs up to WCAG AA before writing
    adjustments = enforce_contrast(color_tokens)
    for change in adjustments:
        print(f"  contrast guard: {change}")
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

    # Write WCAG contrast report (standard M3 pairs only)
    write_contrast_report(color_tokens, review_dir)

    # Write design-brief.md
    brief = build_design_brief(
        name=args.name,
        colors=colors,
        font_display=args.font_display,
        font_body=args.font_body,
        corner_style=args.corner_style,
        mood=args.mood,
        rationale=args.rationale,
        considered_colors=considered_colors,
    )
    with open(os.path.join(review_dir, "design-brief.md"), "w") as f:
        f.write(brief)

    # Write palette review HTML
    review_html = build_palette_review_html(
        color_tokens=color_tokens,
        colors=colors,
        considered_colors=considered_colors,
        name=args.name,
        mood=args.mood,
        font_display=args.font_display,
        font_body=args.font_body,
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
