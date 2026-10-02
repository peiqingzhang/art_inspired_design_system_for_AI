#!/usr/bin/env python3
"""
Re-derive every generated file in themes/ from each theme's color/typography tokens.

The original CLI inputs (picked colors, surfaces, proportions) are not stored in
the repo, so this script works from the committed color.tokens.json instead:

  1. (optional, --fix) run the skill's contrast guard on color.tokens.json
  2. rewrite tokens/theme.css and tokens/tailwind.config.snippet.js
  3. rewrite the WCAG contrast report(s)
  4. rewrite tokens/resolved.json, components/theme.css and review/preview.html

Usage:
    python scripts/regenerate_theme_outputs.py            # regenerate only
    python scripts/regenerate_theme_outputs.py --fix      # apply contrast guard first
    python scripts/regenerate_theme_outputs.py --only matisse-red-studio
"""

import argparse
import importlib.util
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SKILLS = os.path.join(ROOT, "skills")


def load_module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


GEN = {
    "m3": load_module("m3_gen", os.path.join(SKILLS, "painting-to-m3/scripts/generate_tokens.py")),
    "theme": load_module("theme_gen", os.path.join(SKILLS, "painting-to-theme/scripts/generate_tokens.py")),
}
sys.path.insert(0, os.path.join(SKILLS, "tokens-to-components/scripts"))
PARSE = load_module("parse_tokens", os.path.join(SKILLS, "tokens-to-components/scripts/parse_tokens.py"))
COMP = load_module("generate_components", os.path.join(SKILLS, "tokens-to-components/scripts/generate_components.py"))


def read_json(path):
    with open(path) as f:
        return json.load(f)


def write_text(path, text):
    with open(path, "w") as f:
        f.write(text)


def extended_names(color_tokens):
    """Extended painting colors = ref palettes beyond the M3 core six."""
    core = {"primary", "secondary", "tertiary", "neutral", "neutral-variant", "error"}
    return {k: None for k in color_tokens["color"]["ref"] if not k.startswith("$") and k not in core}


def regenerate(variant_dir, variant, fix):
    gen = GEN[variant]
    tok_dir = os.path.join(variant_dir, "tokens")
    rev_dir = os.path.join(variant_dir, "review")
    comp_dir = os.path.join(variant_dir, "components")

    color_path = os.path.join(tok_dir, "color.tokens.json")
    color_tokens = read_json(color_path)
    typography = read_json(os.path.join(tok_dir, "typography.tokens.json"))
    manifest = read_json(os.path.join(tok_dir, "manifest.json"))
    theme_name = manifest["$description"].replace("Design tokens for ", "", 1)

    changes = []
    if fix:
        changes = gen.enforce_contrast(color_tokens, painting_surfaces=(variant == "theme"))
        with open(color_path, "w") as f:
            json.dump(color_tokens, f, indent=2)

    # tokens/theme.css + tailwind snippet
    write_text(os.path.join(tok_dir, "theme.css"), gen.build_css_variables(color_tokens, typography, theme_name))
    write_text(os.path.join(tok_dir, "tailwind.config.snippet.js"), gen.build_tailwind_snippet(color_tokens))

    # contrast report(s): review/ always, tokens/ only where a copy already lives
    if variant == "theme":
        gen.write_contrast_report(color_tokens, rev_dir, extended_names(color_tokens))
    else:
        gen.write_contrast_report(color_tokens, rev_dir)
        if os.path.exists(os.path.join(tok_dir, "contrast-report.md")):
            gen.write_contrast_report(color_tokens, tok_dir)

    # resolved.json (same as parse_tokens.py main)
    flat = PARSE.flatten_tokens(PARSE.load_all_tokens(tok_dir))
    resolved = PARSE.resolve_all(flat)
    with open(os.path.join(tok_dir, "resolved.json"), "w") as f:
        json.dump(resolved, f, indent=2)

    # components/theme.css + review/preview.html
    tokens = COMP.load_resolved_tokens(os.path.join(tok_dir, "resolved.json"))
    write_text(os.path.join(comp_dir, "theme.css"), COMP.generate_theme_css(tokens))

    preview_path = os.path.join(rev_dir, "preview.html")
    if os.path.exists(preview_path):
        with open(preview_path) as f:
            m = re.search(r"<title>(.*?) — M3 Design System Preview", f.read())
        preview_name = m.group(1) if m else theme_name
        index = open(os.path.join(comp_dir, "index.ts")).read()
        exported = re.findall(r"from '\./(\w+)'", index)
        by_display = {COMP._component_display_name(k): k for k in COMP.COMPONENT_GENERATORS}
        components = [by_display[e] for e in exported if e in by_display]
        write_text(preview_path, COMP.generate_preview_html(tokens, components, theme_name=preview_name))

    return changes


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--fix", action="store_true", help="Run the contrast guard on color.tokens.json first")
    ap.add_argument("--only", default=None, help="Only this theme folder name")
    args = ap.parse_args()

    themes_dir = os.path.join(ROOT, "themes")
    for theme in sorted(os.listdir(themes_dir)):
        if args.only and theme != args.only:
            continue
        for variant in ("m3", "theme"):
            vdir = os.path.join(themes_dir, theme, variant)
            if not os.path.isdir(os.path.join(vdir, "tokens")):
                continue
            changes = regenerate(vdir, variant, args.fix)
            print(f"{theme}/{variant}: {len(changes)} token(s) adjusted")
            for c in changes:
                print(f"    {c}")


if __name__ == "__main__":
    main()
