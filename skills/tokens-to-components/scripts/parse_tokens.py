#!/usr/bin/env python3
"""
Parse DTCG token JSON files and resolve all aliases to concrete values.

Usage:
    python parse_tokens.py --token-dir ./tokens/ --output resolved.json
    
Reads all .tokens.json files in the directory, resolves {alias.references},
and outputs a flat key-value map of all resolved tokens.
"""

import argparse
import json
import os
import re
import sys


def load_all_tokens(token_dir: str) -> dict:
    """Load and merge all .tokens.json files from a directory."""
    merged = {}
    for fname in sorted(os.listdir(token_dir)):
        if fname.endswith('.tokens.json'):
            with open(os.path.join(token_dir, fname)) as f:
                data = json.load(f)
                deep_merge(merged, data)
    return merged


def deep_merge(base: dict, overlay: dict):
    """Recursively merge overlay into base."""
    for key, value in overlay.items():
        if key in base and isinstance(base[key], dict) and isinstance(value, dict):
            deep_merge(base[key], value)
        else:
            base[key] = value


def flatten_tokens(data: dict, prefix: str = "") -> dict:
    """Flatten nested token structure into dot-notation keys.
    
    Returns dict like:
        {"color.ref.primary.40": {"$value": "#5c5ea1", "$type": "color"}, ...}
    """
    flat = {}
    for key, value in data.items():
        if key.startswith("$"):
            # Preserve $extensions metadata (e.g. color-component-map, painting-proportions)
            if key == "$extensions" and isinstance(value, dict):
                ext_key = f"{prefix}.$extensions" if prefix else "$extensions"
                flat[ext_key] = value
            continue  # skip other meta properties at group level
        full_key = f"{prefix}.{key}" if prefix else key
        if isinstance(value, dict):
            if "$value" in value:
                # This is a token (leaf node)
                flat[full_key] = value
            else:
                # This is a group, recurse
                flat.update(flatten_tokens(value, full_key))
    return flat


def resolve_alias(value_str: str, flat_tokens: dict, visited: set = None) -> str:
    """Resolve {alias.path} references recursively."""
    if visited is None:
        visited = set()
    
    if not isinstance(value_str, str):
        return value_str
    
    match = re.match(r'^\{(.+)\}$', value_str.strip())
    if not match:
        return value_str
    
    ref_path = match.group(1)
    if ref_path in visited:
        return value_str  # circular reference, bail
    
    visited.add(ref_path)
    
    if ref_path in flat_tokens:
        ref_token = flat_tokens[ref_path]
        ref_value = ref_token.get("$value", value_str)
        if isinstance(ref_value, str) and ref_value.startswith("{"):
            return resolve_alias(ref_value, flat_tokens, visited)
        return ref_value
    
    return value_str  # unresolvable


def resolve_all(flat_tokens: dict) -> dict:
    """Resolve all aliases in the flat token map."""
    resolved = {}
    for key, token in flat_tokens.items():
        # Pass through $extensions metadata as-is
        if "$extensions" in key:
            resolved[key] = token
            continue
        value = token.get("$value")
        token_type = token.get("$type", "")
        
        if isinstance(value, dict):
            # Composite type (e.g., typography)
            resolved_value = {}
            for prop, prop_val in value.items():
                resolved_value[prop] = resolve_alias(prop_val, flat_tokens) if isinstance(prop_val, str) else prop_val
            resolved[key] = {
                "$value": resolved_value,
                "$type": token_type
            }
        elif isinstance(value, str):
            resolved[key] = {
                "$value": resolve_alias(value, flat_tokens),
                "$type": token_type
            }
        else:
            resolved[key] = {
                "$value": value,
                "$type": token_type
            }
    
    return resolved


def export_css_variables(resolved: dict) -> str:
    """Generate CSS custom properties from resolved tokens."""
    lines = ["/* Auto-generated CSS custom properties from design tokens */", ":root {"]
    
    for key, token in sorted(resolved.items()):
        value = token["$value"]
        if isinstance(value, dict):
            continue  # skip composite types for CSS
        css_var = key.replace(".", "-")
        lines.append(f"  --{css_var}: {value};")
    
    lines.append("}")
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="Parse and resolve DTCG design tokens")
    parser.add_argument("--token-dir", required=True, help="Directory containing .tokens.json files")
    parser.add_argument("--output", default="resolved.json", help="Output path for resolved tokens")
    parser.add_argument("--css", help="Optional: also output CSS custom properties to this file")
    
    args = parser.parse_args()
    
    # Load all token files
    merged = load_all_tokens(args.token_dir)
    print(f"Loaded tokens from {args.token_dir}")
    
    # Flatten
    flat = flatten_tokens(merged)
    print(f"Flattened to {len(flat)} tokens")
    
    # Resolve aliases
    resolved = resolve_all(flat)
    print(f"Resolved {len(resolved)} tokens")
    
    # Write resolved JSON
    with open(args.output, "w") as f:
        json.dump(resolved, f, indent=2)
    print(f"Written to {args.output}")
    
    # Optionally write CSS
    if args.css:
        css = export_css_variables(resolved)
        with open(args.css, "w") as f:
            f.write(css)
        print(f"CSS written to {args.css}")
    
    # Summary
    types = {}
    for token in resolved.values():
        t = token.get("$type", "unknown")
        types[t] = types.get(t, 0) + 1
    print("\nToken types:")
    for t, count in sorted(types.items()):
        print(f"  {t}: {count}")


if __name__ == "__main__":
    main()
