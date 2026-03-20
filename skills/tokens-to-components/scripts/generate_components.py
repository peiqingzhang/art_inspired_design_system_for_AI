#!/usr/bin/env python3
"""
Generate React component library from resolved design tokens.

Usage:
    python generate_components.py \
        --resolved-tokens ./resolved.json \
        --components button,card,input,chip,badge,avatar,divider \
        --output-dir ./components
"""

import argparse
import json
import os
import sys


def load_resolved_tokens(path: str) -> dict:
    with open(path) as f:
        return json.load(f)


def get_val(tokens: dict, key: str, fallback: str = "") -> str:
    """Get a resolved token value."""
    if key in tokens:
        v = tokens[key].get("$value", fallback)
        return v if isinstance(v, str) else str(v)
    return fallback


STATE_LAYER_CSS = """
/* M3 State Layers — hover 8%, focus 12%, pressed 12%, disabled 38% */
.m3-interactive {
  position: relative;
  overflow: hidden;
}
.m3-interactive .state-layer {
  position: absolute;
  inset: 0;
  border-radius: inherit;
  pointer-events: none;
  background: currentColor;
  opacity: 0;
  transition: opacity 0.2s ease;
}
.m3-interactive:hover .state-layer { opacity: 0.08; }
.m3-interactive:focus-visible .state-layer { opacity: 0.12; }
.m3-interactive:active .state-layer { opacity: 0.12; }
.m3-interactive:disabled .state-layer,
.m3-interactive[aria-disabled="true"] .state-layer { opacity: 0; }
"""


def generate_theme_css(tokens: dict) -> str:
    """Generate the theme.css file with all CSS custom properties."""
    lines = [
        "/* Design System Theme — Auto-generated from design tokens */",
        "/* Import Google Fonts */",
    ]

    brand_font = get_val(tokens, "typography.ref.typeface.brand", "sans-serif")
    plain_font = get_val(tokens, "typography.ref.typeface.plain", "sans-serif")

    # Google Fonts import
    brand_url = brand_font.replace(" ", "+")
    plain_url = plain_font.replace(" ", "+")
    lines.append(f"@import url('https://fonts.googleapis.com/css2?family={brand_url}:wght@400;500;700&family={plain_url}:wght@400;500;700&display=swap');")
    lines.append("")

    # Light theme
    lines.append(":root {")
    lines.append(f"  --font-brand: '{brand_font}', sans-serif;")
    lines.append(f"  --font-plain: '{plain_font}', sans-serif;")
    lines.append("")

    # Color tokens
    for key, token in sorted(tokens.items()):
        if key.startswith("color.sys.light."):
            role = key.replace("color.sys.light.", "")
            val = token.get("$value", "")
            if isinstance(val, str):
                lines.append(f"  --color-{role}: {val};")

    lines.append("")

    # Shape tokens
    for key, token in sorted(tokens.items()):
        if key.startswith("shape.corner."):
            name = key.replace("shape.corner.", "")
            val = token.get("$value", "")
            if isinstance(val, str):
                lines.append(f"  --radius-{name}: {val};")

    lines.append("")

    # Spacing tokens
    for key, token in sorted(tokens.items()):
        if key.startswith("spacing."):
            name = key.replace("spacing.", "")
            val = token.get("$value", "")
            if isinstance(val, str):
                lines.append(f"  --spacing-{name}: {val};")

    lines.append("")

    # Typography tokens
    prop_map = {
        "fontFamily": "font-family",
        "fontSize": "font-size",
        "fontWeight": "font-weight",
        "lineHeight": "line-height",
        "letterSpacing": "letter-spacing",
    }
    for key, token in sorted(tokens.items()):
        if key.startswith("typography.sys."):
            name = key.replace("typography.sys.", "")
            val = token.get("$value", {})
            if isinstance(val, dict):
                for prop, css_prop in prop_map.items():
                    if prop in val:
                        lines.append(f"  --type-{name}-{css_prop}: {val[prop]};")

    lines.append("}")
    lines.append("")

    # Dark theme
    lines.append("@media (prefers-color-scheme: dark) {")
    lines.append("  :root {")
    for key, token in sorted(tokens.items()):
        if key.startswith("color.sys.dark."):
            role = key.replace("color.sys.dark.", "")
            val = token.get("$value", "")
            if isinstance(val, str):
                lines.append(f"    --color-{role}: {val};")
    lines.append("  }")
    lines.append("}")
    lines.append(STATE_LAYER_CSS)

    return "\n".join(lines)


def generate_button_jsx(typescript: bool = False) -> str:
    props_interface = """
interface ButtonProps {
  variant?: 'filled' | 'outlined' | 'tonal' | 'text';
  disabled?: boolean;
  onClick?: () => void;
  children: React.ReactNode;
  [key: string]: unknown;
}
""" if typescript else ""

    comp_sig = "Button({ variant = 'filled', children, disabled, ...props }: ButtonProps)" if typescript else "Button({ variant = 'filled', children, disabled, ...props })"
    fc_type = ": React.FC<ButtonProps>" if typescript else ""

    return f'''import React from 'react';
import './theme.css';
{props_interface}
const buttonBase = {{
  display: 'inline-flex',
  alignItems: 'center',
  justifyContent: 'center',
  gap: 'var(--spacing-2)',
  height: '40px',
  border: 'none',
  cursor: 'pointer',
  fontFamily: 'var(--font-plain)',
  fontSize: '14px',
  fontWeight: 500,
  letterSpacing: '0.1px',
  lineHeight: '20px',
  position: 'relative',
  overflow: 'hidden',
}};

const variants = {{
  filled: {{
    ...buttonBase,
    backgroundColor: 'var(--color-primary)',
    color: 'var(--color-on-primary)',
    borderRadius: 'var(--radius-full)',
    padding: '0 var(--spacing-6)',
  }},
  outlined: {{
    ...buttonBase,
    backgroundColor: 'transparent',
    color: 'var(--color-primary)',
    border: '1px solid var(--color-outline)',
    borderRadius: 'var(--radius-full)',
    padding: '0 var(--spacing-6)',
  }},
  tonal: {{
    ...buttonBase,
    backgroundColor: 'var(--color-secondary-container)',
    color: 'var(--color-on-secondary-container)',
    borderRadius: 'var(--radius-full)',
    padding: '0 var(--spacing-6)',
  }},
  text: {{
    ...buttonBase,
    backgroundColor: 'transparent',
    color: 'var(--color-primary)',
    borderRadius: 'var(--radius-full)',
    padding: '0 var(--spacing-3)',
  }},
}};

export default function {comp_sig}{fc_type} {{
  const handleKeyDown = (e{': React.KeyboardEvent<HTMLButtonElement>' if typescript else ''}) => {{
    if ((e.key === 'Enter' || e.key === ' ') && props.onClick) props.onClick();
  }};
  return (
    <button
      style={{{{
        ...variants[variant ?? 'filled'],
        ...(disabled ? {{ opacity: 0.38, pointerEvents: 'none' }} : {{}}),
      }}}}
      disabled={{disabled}}
      aria-disabled={{disabled}}
      className="m3-interactive"
      onKeyDown={{handleKeyDown}}
      {{...props}}
    >
      <span className="state-layer" aria-hidden="true" />
      {{children}}
    </button>
  );
}}

Button.Filled = (props{': Omit<ButtonProps, "variant">' if typescript else ''}) => <Button variant="filled" {{...props}} />;
Button.Outlined = (props{': Omit<ButtonProps, "variant">' if typescript else ''}) => <Button variant="outlined" {{...props}} />;
Button.Tonal = (props{': Omit<ButtonProps, "variant">' if typescript else ''}) => <Button variant="tonal" {{...props}} />;
Button.Text = (props{': Omit<ButtonProps, "variant">' if typescript else ''}) => <Button variant="text" {{...props}} />;
'''


def generate_card_jsx(typescript: bool = False) -> str:
    props_interface = """
interface CardProps {
  variant?: 'elevated' | 'filled' | 'outlined';
  children?: React.ReactNode;
  style?: React.CSSProperties;
  [key: string]: unknown;
}
interface CardHeaderProps { title: string; subtitle?: string; }
interface CardBodyProps { children?: React.ReactNode; }
interface CardActionsProps { children?: React.ReactNode; }
""" if typescript else ""

    comp_sig = "Card({ variant = 'elevated', children, style: userStyle, ...props }: CardProps)" if typescript else "Card({ variant = 'elevated', children, style: userStyle, ...props })"
    header_sig = "({ title, subtitle }: CardHeaderProps)" if typescript else "({ title, subtitle })"
    body_sig = "({ children }: CardBodyProps)" if typescript else "({ children })"
    actions_sig = "({ children }: CardActionsProps)" if typescript else "({ children })"

    return f'''import React from 'react';
import './theme.css';
{props_interface}
const cardBase = {{
  borderRadius: 'var(--radius-medium)',
  padding: 'var(--spacing-4)',
  fontFamily: 'var(--font-plain)',
  color: 'var(--color-on-surface)',
  transition: 'box-shadow 0.2s ease',
  position: 'relative',
  overflow: 'hidden',
}};

const variants = {{
  elevated: {{
    ...cardBase,
    backgroundColor: 'var(--color-surface-container-low)',
    boxShadow: '0 1px 3px rgba(0,0,0,0.12), 0 1px 2px rgba(0,0,0,0.08)',
  }},
  filled: {{
    ...cardBase,
    backgroundColor: 'var(--color-surface-container-highest)',
  }},
  outlined: {{
    ...cardBase,
    backgroundColor: 'var(--color-surface)',
    border: '1px solid var(--color-outline-variant)',
  }},
}};

export default function {comp_sig} {{
  return (
    <div role="article" style={{{{ ...variants[variant ?? 'elevated'], ...userStyle }}}} {{...props}}>
      <span className="state-layer" aria-hidden="true" />
      {{children}}
    </div>
  );
}}

Card.Header = {header_sig} => (
  <div style={{{{ marginBottom: 'var(--spacing-3)' }}}}>
    <h3 style={{{{ fontFamily: 'var(--font-brand)', fontSize: '22px', margin: 0, lineHeight: '28px' }}}}>{{title}}</h3>
    {{subtitle && <p style={{{{ fontSize: '14px', color: 'var(--color-on-surface-variant)', margin: '4px 0 0' }}}}>{{subtitle}}</p>}}
  </div>
);

Card.Body = {body_sig} => (
  <div style={{{{ fontSize: '14px', lineHeight: '20px', color: 'var(--color-on-surface-variant)' }}}}>
    {{children}}
  </div>
);

Card.Actions = {actions_sig} => (
  <div style={{{{ display: 'flex', gap: 'var(--spacing-2)', marginTop: 'var(--spacing-4)', justifyContent: 'flex-end' }}}}>
    {{children}}
  </div>
);
'''


def generate_input_jsx(typescript: bool = False) -> str:
    props_interface = """
interface InputProps {
  label?: string;
  variant?: 'outlined' | 'filled';
  supportingText?: string;
  error?: boolean;
  value?: string;
  onChange?: React.ChangeEventHandler<HTMLInputElement>;
  id?: string;
  [key: string]: unknown;
}
""" if typescript else ""

    comp_sig = "Input({ label, variant = 'outlined', supportingText, error, value, onChange, id, ...props }: InputProps)" if typescript else "Input({ label, variant = 'outlined', supportingText, error, value, onChange, id, ...props })"

    return f'''import React, {{ useState, useId }} from 'react';
import './theme.css';
{props_interface}
export default function {comp_sig} {{
  const [focused, setFocused] = useState(false);
  const generatedId = useId();
  const inputId = id || generatedId;
  const helperId = `${{inputId}}-helper`;
  const hasValue = value && value.length > 0;

  const containerStyle = variant === 'filled' ? {{
    backgroundColor: 'var(--color-surface-container-highest)',
    borderRadius: 'var(--radius-extra-small) var(--radius-extra-small) 0 0',
    borderBottom: focused
      ? '2px solid var(--color-primary)'
      : error ? '2px solid var(--color-error)' : '1px solid var(--color-on-surface-variant)',
    padding: '8px var(--spacing-4) 8px',
    position: 'relative',
    minHeight: '56px',
    display: 'flex',
    flexDirection: 'column',
    justifyContent: 'flex-end',
  }} : {{
    backgroundColor: 'transparent',
    border: focused
      ? '2px solid var(--color-primary)'
      : error ? '2px solid var(--color-error)' : '1px solid var(--color-outline)',
    borderRadius: 'var(--radius-extra-small)',
    padding: '8px var(--spacing-4) 8px',
    position: 'relative',
    minHeight: '56px',
    display: 'flex',
    flexDirection: 'column',
    justifyContent: 'flex-end',
  }};

  const labelStyle = {{
    position: 'absolute',
    top: (focused || hasValue) ? '8px' : '18px',
    fontSize: (focused || hasValue) ? '12px' : '16px',
    color: focused ? 'var(--color-primary)' : error ? 'var(--color-error)' : 'var(--color-on-surface-variant)',
    transition: 'all 0.15s ease',
    pointerEvents: 'none',
    fontFamily: 'var(--font-plain)',
  }};

  const inputStyle = {{
    border: 'none',
    outline: 'none',
    background: 'transparent',
    fontSize: '16px',
    fontFamily: 'var(--font-plain)',
    color: 'var(--color-on-surface)',
    width: '100%',
    padding: 0,
    marginTop: '12px',
  }};

  return (
    <div>
      <div style={{containerStyle}}>
        {{label && <label htmlFor={{inputId}} style={{labelStyle}}>{{label}}</label>}}
        <input
          id={{inputId}}
          style={{inputStyle}}
          value={{value}}
          onChange={{onChange}}
          onFocus={{() => setFocused(true)}}
          onBlur={{() => setFocused(false)}}
          aria-invalid={{!!error}}
          aria-describedby={{supportingText ? helperId : undefined}}
          {{...props}}
        />
      </div>
      {{supportingText && (
        <p id={{helperId}} style={{{{
          fontSize: '12px',
          color: error ? 'var(--color-error)' : 'var(--color-on-surface-variant)',
          margin: '4px var(--spacing-4) 0',
          fontFamily: 'var(--font-plain)',
        }}}}>
          {{supportingText}}
        </p>
      )}}
    </div>
  );
}}
'''


def generate_chip_jsx(typescript: bool = False) -> str:
    props_interface = """
interface ChipProps {
  label: string;
  selected?: boolean;
  onClose?: () => void;
  onClick?: () => void;
  variant?: 'assist' | 'filter' | 'input' | 'suggestion';
}
""" if typescript else ""

    comp_sig = "Chip({ label, selected, onClose, onClick, variant = 'assist', ...props }: ChipProps)" if typescript else "Chip({ label, selected, onClose, onClick, variant = 'assist', ...props })"

    return f'''import React from 'react';
import './theme.css';
{props_interface}
export default function {comp_sig} {{
  const style = {{
    display: 'inline-flex',
    alignItems: 'center',
    height: '32px',
    padding: '0 var(--spacing-4)',
    gap: 'var(--spacing-2)',
    borderRadius: 'var(--radius-small)',
    fontFamily: 'var(--font-plain)',
    fontSize: '14px',
    fontWeight: 500,
    cursor: 'pointer',
    transition: 'all 0.15s ease',
    border: selected ? 'none' : '1px solid var(--color-outline)',
    backgroundColor: selected ? 'var(--color-secondary-container)' : 'transparent',
    color: selected ? 'var(--color-on-secondary-container)' : 'var(--color-on-surface)',
    position: 'relative',
    overflow: 'hidden',
  }};

  const handleKeyDown = (e{': React.KeyboardEvent<HTMLDivElement>' if typescript else ''}) => {{
    if (e.key === 'Enter' || e.key === ' ') {{
      e.preventDefault();
      onClick?.();
    }}
  }};

  return (
    <div
      style={{style}}
      role="option"
      aria-selected={{!!selected}}
      aria-label={{label}}
      tabIndex={{0}}
      onClick={{onClick}}
      onKeyDown={{handleKeyDown}}
      className="m3-interactive"
      {{...props}}
    >
      <span className="state-layer" aria-hidden="true" />
      <span>{{label}}</span>
      {{onClose && (
        <span
          onClick={{(e{': React.MouseEvent' if typescript else ''}) => {{ e.stopPropagation(); onClose(); }}}}
          aria-label="Remove"
          style={{{{ cursor: 'pointer', fontSize: '18px', lineHeight: 1 }}}}
        >&times;</span>
      )}}
    </div>
  );
}}
'''


def generate_badge_jsx(typescript: bool = False) -> str:
    props_interface = """
interface BadgeProps {
  count?: number;
  children?: React.ReactNode;
}
""" if typescript else ""

    comp_sig = "Badge({ count, children }: BadgeProps)" if typescript else "Badge({ count, children })"

    return f'''import React from 'react';
import './theme.css';
{props_interface}
export default function {comp_sig} {{
  const showCount = count !== undefined && count > 0;
  const ariaLabel = count !== undefined && count > 0
    ? `${{count > 99 ? '99+' : count}} notifications`
    : undefined;
  return (
    <div style={{{{ position: 'relative', display: 'inline-flex' }}}}>
      {{children}}
      <span
        aria-label={{ariaLabel}}
        aria-live="polite"
        style={{{{
          position: 'absolute',
          top: '-4px',
          right: '-4px',
          minWidth: showCount ? '24px' : '8px',
          height: showCount ? '24px' : '8px',
          borderRadius: 'var(--radius-full)',
          backgroundColor: 'var(--color-error)',
          color: 'var(--color-on-error)',
          fontSize: '11px',
          fontWeight: 500,
          fontFamily: 'var(--font-plain)',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
          padding: showCount ? '0 4px' : 0,
        }}}}
      >
        {{showCount ? ({'count!' if typescript else 'count'} > 99 ? '99+' : count) : ''}}
      </span>
    </div>
  );
}}
'''


def generate_avatar_jsx(typescript: bool = False) -> str:
    props_interface = """
interface AvatarProps {
  name?: string;
  src?: string;
  size?: number;
}
""" if typescript else ""

    comp_sig = "Avatar({ name, src, size = 40 }: AvatarProps)" if typescript else "Avatar({ name, src, size = 40 })"

    return f'''import React from 'react';
import './theme.css';
{props_interface}
export default function {comp_sig} {{
  const initials = name ? name.split(' ').map((n{': string' if typescript else ''}) => n[0]).join('').slice(0, 2).toUpperCase() : '?';
  const fontSize = size * 0.4;
  const label = name || 'User avatar';

  if (src) {{
    return (
      <img
        src={{src}}
        alt={{label}}
        aria-label={{label}}
        style={{{{
          width: size, height: size,
          borderRadius: 'var(--radius-full)',
          objectFit: 'cover',
        }}}}
      />
    );
  }}

  return (
    <div
      aria-label={{label}}
      role="img"
      style={{{{
        width: size, height: size,
        borderRadius: 'var(--radius-full)',
        backgroundColor: 'var(--color-primary-container)',
        color: 'var(--color-on-primary-container)',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
        fontSize,
        fontWeight: 500,
        fontFamily: 'var(--font-plain)',
      }}}}
    >
      {{initials}}
    </div>
  );
}}
'''


def generate_divider_jsx(typescript: bool = False) -> str:
    props_interface = """
interface DividerProps {
  inset?: boolean;
  vertical?: boolean;
}
""" if typescript else ""

    comp_sig = "Divider({ inset, vertical }: DividerProps)" if typescript else "Divider({ inset, vertical })"

    return f'''import React from 'react';
import './theme.css';
{props_interface}
export default function {comp_sig} {{
  if (vertical) {{
    return <div role="separator" aria-orientation="vertical" style={{{{ width: '1px', alignSelf: 'stretch', backgroundColor: 'var(--color-outline-variant)' }}}} />;
  }}
  return <hr role="separator" style={{{{ border: 'none', height: '1px', backgroundColor: 'var(--color-outline-variant)', margin: 0, marginLeft: inset ? 'var(--spacing-4)' : 0 }}}} />;
}}
'''


def generate_appbar_jsx(typescript: bool = False) -> str:
    props_interface = """
interface AppBarProps {
  title: string;
  leading?: React.ReactNode;
  trailing?: React.ReactNode;
  elevated?: boolean;
  children?: React.ReactNode;
  [key: string]: unknown;
}
""" if typescript else ""

    comp_sig = "AppBar({ title, leading, trailing, elevated, children, ...props }: AppBarProps)" if typescript else "AppBar({ title, leading, trailing, elevated, children, ...props })"

    return f'''import React from 'react';
import './theme.css';
{props_interface}
export default function {comp_sig} {{
  return (
    <header
      style={{{{
        display: 'flex',
        alignItems: 'center',
        height: '64px',
        padding: '0 var(--spacing-4)',
        backgroundColor: elevated ? 'var(--color-surface-container)' : 'var(--color-surface)',
        color: 'var(--color-on-surface)',
        fontFamily: 'var(--font-brand)',
        gap: 'var(--spacing-2)',
        transition: 'background-color 0.2s ease',
      }}}}
      role="banner"
      {{...props}}
    >
      {{leading && <div style={{{{ display: 'flex', alignItems: 'center', color: 'var(--color-on-surface-variant)' }}}}>{{leading}}</div>}}
      <h1 style={{{{ fontSize: '22px', lineHeight: '28px', fontWeight: 400, margin: 0, flex: 1 }}}}>{{title}}</h1>
      {{trailing && <div style={{{{ display: 'flex', alignItems: 'center', gap: 'var(--spacing-2)', color: 'var(--color-on-surface-variant)' }}}}>{{trailing}}</div>}}
      {{children}}
    </header>
  );
}}
'''


def generate_tabs_jsx(typescript: bool = False) -> str:
    props_interface = """
interface Tab {
  label: string;
  icon?: React.ReactNode;
}

interface TabsProps {
  tabs: Tab[];
  activeIndex?: number;
  onChange?: (index: number) => void;
  [key: string]: unknown;
}
""" if typescript else ""

    comp_sig = "Tabs({ tabs, activeIndex: controlledIndex, onChange, ...props }: TabsProps)" if typescript else "Tabs({ tabs, activeIndex: controlledIndex, onChange, ...props })"

    return f'''import React, {{ useState }} from 'react';
import './theme.css';
{props_interface}
export default function {comp_sig} {{
  const [internalIndex, setInternalIndex] = useState(0);
  const activeIndex = controlledIndex ?? internalIndex;

  const handleSelect = (i{': number' if typescript else ''}) => {{
    setInternalIndex(i);
    onChange?.(i);
  }};

  return (
    <div
      role="tablist"
      style={{{{
        display: 'flex',
        backgroundColor: 'var(--color-surface-container)',
        borderBottom: '1px solid var(--color-outline-variant)',
      }}}}
      {{...props}}
    >
      {{tabs.map((tab{': Tab' if typescript else ''}, i{': number' if typescript else ''}) => (
        <button
          key={{i}}
          role="tab"
          aria-selected={{i === activeIndex}}
          tabIndex={{i === activeIndex ? 0 : -1}}
          onClick={{() => handleSelect(i)}}
          onKeyDown={{(e) => {{
            if (e.key === 'ArrowRight') handleSelect((i + 1) % tabs.length);
            if (e.key === 'ArrowLeft') handleSelect((i - 1 + tabs.length) % tabs.length);
          }}}}
          className="m3-interactive"
          style={{{{
            flex: 1,
            display: 'flex',
            flexDirection: 'column',
            alignItems: 'center',
            justifyContent: 'center',
            gap: 'var(--spacing-1)',
            height: tab.icon ? '64px' : '48px',
            padding: '0 var(--spacing-4)',
            border: 'none',
            cursor: 'pointer',
            backgroundColor: 'transparent',
            color: i === activeIndex ? 'var(--color-on-surface)' : 'var(--color-on-surface-variant)',
            fontFamily: 'var(--font-plain)',
            fontSize: '14px',
            fontWeight: 500,
            letterSpacing: '0.1px',
            position: 'relative',
            overflow: 'hidden',
            borderBottom: i === activeIndex ? '3px solid var(--color-primary)' : '3px solid transparent',
          }}}}
        >
          <span className="state-layer" aria-hidden="true" />
          {{tab.icon && <span>{{tab.icon}}</span>}}
          <span>{{tab.label}}</span>
        </button>
      ))}}
    </div>
  );
}}
'''


def generate_sidebar_jsx(typescript: bool = False) -> str:
    props_interface = """
interface SidebarItem {
  label: string;
  icon?: React.ReactNode;
  active?: boolean;
  onClick?: () => void;
}

interface SidebarProps {
  items: SidebarItem[];
  header?: React.ReactNode;
  [key: string]: unknown;
}
""" if typescript else ""

    comp_sig = "Sidebar({ items, header, ...props }: SidebarProps)" if typescript else "Sidebar({ items, header, ...props })"

    return f'''import React from 'react';
import './theme.css';
{props_interface}
export default function {comp_sig} {{
  return (
    <nav
      style={{{{
        width: '280px',
        backgroundColor: 'var(--color-surface-container)',
        padding: 'var(--spacing-3)',
        fontFamily: 'var(--font-plain)',
        display: 'flex',
        flexDirection: 'column',
        gap: 'var(--spacing-1)',
      }}}}
      role="navigation"
      {{...props}}
    >
      {{header && <div style={{{{ padding: 'var(--spacing-4)', marginBottom: 'var(--spacing-2)' }}}}>{{header}}</div>}}
      {{items.map((item{': SidebarItem' if typescript else ''}, i{': number' if typescript else ''}) => (
        <button
          key={{i}}
          onClick={{item.onClick}}
          className="m3-interactive"
          style={{{{
            display: 'flex',
            alignItems: 'center',
            gap: 'var(--spacing-3)',
            padding: '0 var(--spacing-6) 0 var(--spacing-4)',
            height: '56px',
            border: 'none',
            cursor: 'pointer',
            borderRadius: 'var(--radius-full)',
            backgroundColor: item.active ? 'var(--color-secondary-container)' : 'transparent',
            color: item.active ? 'var(--color-on-secondary-container)' : 'var(--color-on-surface-variant)',
            fontFamily: 'var(--font-plain)',
            fontSize: '14px',
            fontWeight: item.active ? 700 : 500,
            letterSpacing: '0.1px',
            position: 'relative',
            overflow: 'hidden',
            width: '100%',
            textAlign: 'left',
          }}}}
        >
          <span className="state-layer" aria-hidden="true" />
          {{item.icon && <span style={{{{ fontSize: '24px', display: 'flex' }}}}>{{item.icon}}</span>}}
          <span>{{item.label}}</span>
        </button>
      ))}}
    </nav>
  );
}}
'''


def generate_breadcrumb_jsx(typescript: bool = False) -> str:
    props_interface = """
interface BreadcrumbItem {
  label: string;
  href?: string;
  onClick?: () => void;
}

interface BreadcrumbProps {
  items: BreadcrumbItem[];
  separator?: string;
  [key: string]: unknown;
}
""" if typescript else ""

    comp_sig = "Breadcrumb({ items, separator = '/', ...props }: BreadcrumbProps)" if typescript else "Breadcrumb({ items, separator = '/', ...props })"

    return f'''import React from 'react';
import './theme.css';
{props_interface}
export default function {comp_sig} {{
  return (
    <nav aria-label="Breadcrumb" {{...props}}>
      <ol
        style={{{{
          display: 'flex',
          alignItems: 'center',
          gap: 'var(--spacing-2)',
          listStyle: 'none',
          margin: 0,
          padding: 0,
          fontFamily: 'var(--font-plain)',
          fontSize: '14px',
          lineHeight: '20px',
        }}}}
      >
        {{items.map((item{': BreadcrumbItem' if typescript else ''}, i{': number' if typescript else ''}) => (
          <li key={{i}} style={{{{ display: 'flex', alignItems: 'center', gap: 'var(--spacing-2)' }}}}>
            {{i > 0 && <span style={{{{ color: 'var(--color-on-surface-variant)' }}}}>{{separator}}</span>}}
            {{i < items.length - 1 ? (
              <a
                href={{item.href || '#'}}
                onClick={{(e{': React.MouseEvent' if typescript else ''}) => {{ if (item.onClick) {{ e.preventDefault(); item.onClick(); }} }}}}
                style={{{{
                  color: 'var(--color-primary)',
                  textDecoration: 'none',
                  fontWeight: 500,
                }}}}
              >
                {{item.label}}
              </a>
            ) : (
              <span
                aria-current="page"
                style={{{{ color: 'var(--color-on-surface)', fontWeight: 500 }}}}
              >
                {{item.label}}
              </span>
            )}}
          </li>
        ))}}
      </ol>
    </nav>
  );
}}
'''


def generate_bottomnav_jsx(typescript: bool = False) -> str:
    props_interface = """
interface BottomNavItem {
  label: string;
  icon: React.ReactNode;
  active?: boolean;
  onClick?: () => void;
}

interface BottomNavProps {
  items: BottomNavItem[];
  [key: string]: unknown;
}
""" if typescript else ""

    comp_sig = "BottomNav({ items, ...props }: BottomNavProps)" if typescript else "BottomNav({ items, ...props })"

    return f'''import React from 'react';
import './theme.css';
{props_interface}
export default function {comp_sig} {{
  return (
    <nav
      role="navigation"
      style={{{{
        display: 'flex',
        backgroundColor: 'var(--color-surface-container)',
        height: '80px',
        borderTop: '1px solid var(--color-outline-variant)',
      }}}}
      {{...props}}
    >
      {{items.map((item{': BottomNavItem' if typescript else ''}, i{': number' if typescript else ''}) => (
        <button
          key={{i}}
          onClick={{item.onClick}}
          className="m3-interactive"
          aria-current={{item.active ? 'page' : undefined}}
          style={{{{
            flex: 1,
            display: 'flex',
            flexDirection: 'column',
            alignItems: 'center',
            justifyContent: 'center',
            gap: 'var(--spacing-1)',
            border: 'none',
            cursor: 'pointer',
            backgroundColor: 'transparent',
            color: item.active ? 'var(--color-on-surface)' : 'var(--color-on-surface-variant)',
            fontFamily: 'var(--font-plain)',
            fontSize: '12px',
            fontWeight: item.active ? 700 : 500,
            letterSpacing: '0.5px',
            position: 'relative',
            overflow: 'hidden',
          }}}}
        >
          <span className="state-layer" aria-hidden="true" />
          <span
            style={{{{
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              width: '64px',
              height: '32px',
              borderRadius: 'var(--radius-full)',
              backgroundColor: item.active ? 'var(--color-secondary-container)' : 'transparent',
              color: item.active ? 'var(--color-on-secondary-container)' : 'inherit',
              fontSize: '24px',
              transition: 'all 0.2s ease',
            }}}}
          >
            {{item.icon}}
          </span>
          <span>{{item.label}}</span>
        </button>
      ))}}
    </nav>
  );
}}
'''


def generate_table_jsx(typescript: bool = False) -> str:
    props_interface = """
interface TableColumn {
  key: string;
  header: string;
  align?: 'left' | 'center' | 'right';
}

interface TableProps {
  columns: TableColumn[];
  data: Record<string, React.ReactNode>[];
  striped?: boolean;
  [key: string]: unknown;
}
""" if typescript else ""

    comp_sig = "Table({ columns, data, striped, ...props }: TableProps)" if typescript else "Table({ columns, data, striped, ...props })"

    return f'''import React from 'react';
import './theme.css';
{props_interface}
export default function {comp_sig} {{
  return (
    <div style={{{{ overflowX: 'auto', borderRadius: 'var(--radius-medium)', border: '1px solid var(--color-outline-variant)' }}}}>
      <table
        style={{{{
          width: '100%',
          borderCollapse: 'collapse',
          fontFamily: 'var(--font-plain)',
          fontSize: '14px',
          lineHeight: '20px',
          color: 'var(--color-on-surface)',
        }}}}
        {{...props}}
      >
        <thead>
          <tr style={{{{ backgroundColor: 'var(--color-surface-container)' }}}}>
            {{columns.map((col{': TableColumn' if typescript else ''}) => (
              <th
                key={{col.key}}
                style={{{{
                  padding: 'var(--spacing-3) var(--spacing-4)',
                  textAlign: col.align || 'left',
                  fontWeight: 500,
                  fontSize: '12px',
                  letterSpacing: '0.5px',
                  color: 'var(--color-on-surface-variant)',
                  borderBottom: '1px solid var(--color-outline-variant)',
                }}}}
              >
                {{col.header}}
              </th>
            ))}}
          </tr>
        </thead>
        <tbody>
          {{data.map((row, i{': number' if typescript else ''}) => (
            <tr
              key={{i}}
              style={{{{
                backgroundColor: striped && i % 2 === 1 ? 'var(--color-surface-container-lowest)' : 'var(--color-surface)',
                borderBottom: '1px solid var(--color-outline-variant)',
              }}}}
            >
              {{columns.map((col{': TableColumn' if typescript else ''}) => (
                <td
                  key={{col.key}}
                  style={{{{
                    padding: 'var(--spacing-3) var(--spacing-4)',
                    textAlign: col.align || 'left',
                  }}}}
                >
                  {{row[col.key]}}
                </td>
              ))}}
            </tr>
          ))}}
        </tbody>
      </table>
    </div>
  );
}}
'''


def generate_list_jsx(typescript: bool = False) -> str:
    props_interface = """
interface ListItemProps {
  primary: string;
  secondary?: string;
  leading?: React.ReactNode;
  trailing?: React.ReactNode;
  onClick?: () => void;
  [key: string]: unknown;
}

interface ListProps {
  children?: React.ReactNode;
  [key: string]: unknown;
}
""" if typescript else ""

    comp_sig = "List({ children, ...props }: ListProps)" if typescript else "List({ children, ...props })"
    item_sig = "({ primary, secondary, leading, trailing, onClick, ...props }: ListItemProps)" if typescript else "({ primary, secondary, leading, trailing, onClick, ...props })"

    return f'''import React from 'react';
import './theme.css';
{props_interface}
export default function {comp_sig} {{
  return (
    <ul
      role="list"
      style={{{{ listStyle: 'none', margin: 0, padding: 0, fontFamily: 'var(--font-plain)' }}}}
      {{...props}}
    >
      {{children}}
    </ul>
  );
}}

List.Item = function ListItem{item_sig} {{
  const interactive = !!onClick;
  return (
    <li
      role={{interactive ? 'button' : 'listitem'}}
      tabIndex={{interactive ? 0 : undefined}}
      onClick={{onClick}}
      onKeyDown={{(e) => {{ if (interactive && (e.key === 'Enter' || e.key === ' ')) {{ e.preventDefault(); onClick?.(); }} }}}}
      className={{interactive ? 'm3-interactive' : ''}}
      style={{{{
        display: 'flex',
        alignItems: 'center',
        gap: 'var(--spacing-4)',
        padding: 'var(--spacing-2) var(--spacing-4)',
        minHeight: secondary ? '72px' : '56px',
        cursor: interactive ? 'pointer' : 'default',
        color: 'var(--color-on-surface)',
        position: 'relative',
        overflow: 'hidden',
      }}}}
      {{...props}}
    >
      {{interactive && <span className="state-layer" aria-hidden="true" />}}
      {{leading && <div style={{{{ display: 'flex', alignItems: 'center', fontSize: '24px', color: 'var(--color-on-surface-variant)' }}}}>{{leading}}</div>}}
      <div style={{{{ flex: 1, minWidth: 0 }}}}>
        <div style={{{{ fontSize: '16px', lineHeight: '24px' }}}}>{{primary}}</div>
        {{secondary && <div style={{{{ fontSize: '14px', lineHeight: '20px', color: 'var(--color-on-surface-variant)' }}}}>{{secondary}}</div>}}
      </div>
      {{trailing && <div style={{{{ display: 'flex', alignItems: 'center', color: 'var(--color-on-surface-variant)' }}}}>{{trailing}}</div>}}
    </li>
  );
}};
'''


def generate_datacard_jsx(typescript: bool = False) -> str:
    props_interface = """
interface DataCardProps {
  title: string;
  value: string | number;
  subtitle?: string;
  trend?: 'up' | 'down' | 'neutral';
  trendValue?: string;
  icon?: React.ReactNode;
  [key: string]: unknown;
}
""" if typescript else ""

    comp_sig = "DataCard({ title, value, subtitle, trend, trendValue, icon, ...props }: DataCardProps)" if typescript else "DataCard({ title, value, subtitle, trend, trendValue, icon, ...props })"

    return f'''import React from 'react';
import './theme.css';
{props_interface}
export default function {comp_sig} {{
  const trendColor = trend === 'up' ? 'var(--color-tertiary)' : trend === 'down' ? 'var(--color-error)' : 'var(--color-on-surface-variant)';
  const trendArrow = trend === 'up' ? '\\u2191' : trend === 'down' ? '\\u2193' : '';

  return (
    <div
      role="article"
      style={{{{
        backgroundColor: 'var(--color-surface-container-low)',
        borderRadius: 'var(--radius-medium)',
        padding: 'var(--spacing-4)',
        fontFamily: 'var(--font-plain)',
        color: 'var(--color-on-surface)',
        boxShadow: '0 1px 3px rgba(0,0,0,0.12)',
      }}}}
      {{...props}}
    >
      <div style={{{{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', marginBottom: 'var(--spacing-3)' }}}}>
        <span style={{{{ fontSize: '14px', fontWeight: 500, color: 'var(--color-on-surface-variant)' }}}}>{{title}}</span>
        {{icon && <span style={{{{ fontSize: '24px', color: 'var(--color-primary)' }}}}>{{icon}}</span>}}
      </div>
      <div style={{{{ fontSize: '32px', fontWeight: 700, fontFamily: 'var(--font-brand)', lineHeight: '40px' }}}}>{{value}}</div>
      <div style={{{{ display: 'flex', alignItems: 'center', gap: 'var(--spacing-2)', marginTop: 'var(--spacing-1)' }}}}>
        {{trendValue && (
          <span style={{{{ fontSize: '14px', fontWeight: 500, color: trendColor }}}}>
            {{trendArrow}} {{trendValue}}
          </span>
        )}}
        {{subtitle && <span style={{{{ fontSize: '14px', color: 'var(--color-on-surface-variant)' }}}}>{{subtitle}}</span>}}
      </div>
    </div>
  );
}}
'''


def generate_stat_jsx(typescript: bool = False) -> str:
    props_interface = """
interface StatProps {
  label: string;
  value: string | number;
  description?: string;
  [key: string]: unknown;
}
""" if typescript else ""

    comp_sig = "Stat({ label, value, description, ...props }: StatProps)" if typescript else "Stat({ label, value, description, ...props })"

    return f'''import React from 'react';
import './theme.css';
{props_interface}
export default function {comp_sig} {{
  return (
    <div
      style={{{{
        fontFamily: 'var(--font-plain)',
        color: 'var(--color-on-surface)',
        textAlign: 'center',
        padding: 'var(--spacing-4)',
      }}}}
      {{...props}}
    >
      <div style={{{{ fontSize: '12px', fontWeight: 500, letterSpacing: '0.5px', color: 'var(--color-on-surface-variant)', marginBottom: 'var(--spacing-1)' }}}}>
        {{label}}
      </div>
      <div style={{{{ fontSize: '45px', fontWeight: 400, fontFamily: 'var(--font-brand)', lineHeight: '52px' }}}}>
        {{value}}
      </div>
      {{description && (
        <div style={{{{ fontSize: '14px', color: 'var(--color-on-surface-variant)', marginTop: 'var(--spacing-1)' }}}}>
          {{description}}
        </div>
      )}}
    </div>
  );
}}
'''


def generate_dialog_jsx(typescript: bool = False) -> str:
    props_interface = """
interface DialogProps {
  open: boolean;
  onClose: () => void;
  headline: string;
  children?: React.ReactNode;
  actions?: React.ReactNode;
  [key: string]: unknown;
}
""" if typescript else ""

    comp_sig = "Dialog({ open, onClose, headline, children, actions, ...props }: DialogProps)" if typescript else "Dialog({ open, onClose, headline, children, actions, ...props })"
    ref_type = "<HTMLDialogElement>" if typescript else ""

    return f'''import React, {{ useEffect, useRef }} from 'react';
import './theme.css';
{props_interface}
export default function {comp_sig} {{
  const dialogRef = useRef{ref_type}(null);

  useEffect(() => {{
    const el = dialogRef.current;
    if (!el) return;
    if (open && !el.open) el.showModal();
    else if (!open && el.open) el.close();
  }}, [open]);

  return (
    <dialog
      ref={{dialogRef}}
      onClose={{onClose}}
      style={{{{
        backgroundColor: 'var(--color-surface-container-high)',
        color: 'var(--color-on-surface)',
        borderRadius: 'var(--radius-extra-large)',
        padding: 'var(--spacing-6)',
        border: 'none',
        maxWidth: '560px',
        width: '100%',
        fontFamily: 'var(--font-plain)',
        boxShadow: '0 8px 32px rgba(0,0,0,0.24)',
      }}}}
      {{...props}}
    >
      <h2 style={{{{
        fontFamily: 'var(--font-brand)',
        fontSize: '24px',
        lineHeight: '32px',
        fontWeight: 400,
        margin: '0 0 var(--spacing-4)',
        color: 'var(--color-on-surface)',
      }}}}>
        {{headline}}
      </h2>
      <div style={{{{
        fontSize: '14px',
        lineHeight: '20px',
        color: 'var(--color-on-surface-variant)',
        marginBottom: actions ? 'var(--spacing-6)' : '0',
      }}}}>
        {{children}}
      </div>
      {{actions && (
        <div style={{{{ display: 'flex', justifyContent: 'flex-end', gap: 'var(--spacing-2)' }}}}>
          {{actions}}
        </div>
      )}}
    </dialog>
  );
}}
'''


def generate_snackbar_jsx(typescript: bool = False) -> str:
    props_interface = """
interface SnackbarProps {
  message: string;
  action?: { label: string; onClick: () => void };
  onClose?: () => void;
  [key: string]: unknown;
}
""" if typescript else ""

    comp_sig = "Snackbar({ message, action, onClose, ...props }: SnackbarProps)" if typescript else "Snackbar({ message, action, onClose, ...props })"

    return f'''import React from 'react';
import './theme.css';
{props_interface}
export default function {comp_sig} {{
  return (
    <div
      role="status"
      aria-live="polite"
      style={{{{
        display: 'flex',
        alignItems: 'center',
        gap: 'var(--spacing-2)',
        padding: 'var(--spacing-3) var(--spacing-4)',
        backgroundColor: 'var(--color-inverse-surface)',
        color: 'var(--color-inverse-on-surface)',
        borderRadius: 'var(--radius-extra-small)',
        fontFamily: 'var(--font-plain)',
        fontSize: '14px',
        lineHeight: '20px',
        minHeight: '48px',
        boxShadow: '0 4px 12px rgba(0,0,0,0.2)',
      }}}}
      {{...props}}
    >
      <span style={{{{ flex: 1 }}}}>{{message}}</span>
      {{action && (
        <button
          onClick={{action.onClick}}
          style={{{{
            border: 'none',
            background: 'none',
            color: 'var(--color-inverse-primary)',
            fontFamily: 'var(--font-plain)',
            fontSize: '14px',
            fontWeight: 500,
            letterSpacing: '0.1px',
            cursor: 'pointer',
            padding: '0 var(--spacing-2)',
          }}}}
        >
          {{action.label}}
        </button>
      )}}
      {{onClose && (
        <button
          onClick={{onClose}}
          aria-label="Dismiss"
          style={{{{
            border: 'none',
            background: 'none',
            color: 'var(--color-inverse-on-surface)',
            cursor: 'pointer',
            fontSize: '18px',
            padding: '0 var(--spacing-1)',
          }}}}
        >
          &times;
        </button>
      )}}
    </div>
  );
}}
'''


def generate_tooltip_jsx(typescript: bool = False) -> str:
    props_interface = """
interface TooltipProps {
  content: string;
  children: React.ReactElement;
  position?: 'top' | 'bottom' | 'left' | 'right';
}
""" if typescript else ""

    comp_sig = "Tooltip({ content, children, position = 'top' }: TooltipProps)" if typescript else "Tooltip({ content, children, position = 'top' })"

    pos_type = ": Record<string, React.CSSProperties>" if typescript else ""

    return f'''import React, {{ useState }} from 'react';
import './theme.css';
{props_interface}
const positionStyles{pos_type} = {{
  top: {{ bottom: '100%', left: '50%', transform: 'translateX(-50%)', marginBottom: '8px' }},
  bottom: {{ top: '100%', left: '50%', transform: 'translateX(-50%)', marginTop: '8px' }},
  left: {{ right: '100%', top: '50%', transform: 'translateY(-50%)', marginRight: '8px' }},
  right: {{ left: '100%', top: '50%', transform: 'translateY(-50%)', marginLeft: '8px' }},
}};

export default function {comp_sig} {{
  const [visible, setVisible] = useState(false);

  return (
    <div
      style={{{{ position: 'relative', display: 'inline-flex' }}}}
      onMouseEnter={{() => setVisible(true)}}
      onMouseLeave={{() => setVisible(false)}}
      onFocus={{() => setVisible(true)}}
      onBlur={{() => setVisible(false)}}
    >
      {{children}}
      {{visible && (
        <div
          role="tooltip"
          style={{{{
            position: 'absolute',
            ...positionStyles[position],
            backgroundColor: 'var(--color-inverse-surface)',
            color: 'var(--color-inverse-on-surface)',
            padding: '4px var(--spacing-2)',
            borderRadius: 'var(--radius-extra-small)',
            fontFamily: 'var(--font-plain)',
            fontSize: '12px',
            lineHeight: '16px',
            fontWeight: 500,
            whiteSpace: 'nowrap',
            pointerEvents: 'none',
            zIndex: 1000,
          }}}}
        >
          {{content}}
        </div>
      )}}
    </div>
  );
}}
'''


def generate_progress_jsx(typescript: bool = False) -> str:
    props_interface = """
interface ProgressProps {
  value?: number;
  variant?: 'linear' | 'circular';
  indeterminate?: boolean;
  [key: string]: unknown;
}
""" if typescript else ""

    comp_sig = "Progress({ value = 0, variant = 'linear', indeterminate, ...props }: ProgressProps)" if typescript else "Progress({ value = 0, variant = 'linear', indeterminate, ...props })"

    return f'''import React from 'react';
import './theme.css';
{props_interface}
export default function {comp_sig} {{
  if (variant === 'circular') {{
    const size = 48;
    const stroke = 4;
    const radius = (size - stroke) / 2;
    const circumference = 2 * Math.PI * radius;
    const offset = indeterminate ? circumference * 0.75 : circumference * (1 - value / 100);

    return (
      <div role="progressbar" aria-valuenow={{indeterminate ? undefined : value}} aria-valuemin={{0}} aria-valuemax={{100}} {{...props}}>
        <svg
          width={{size}}
          height={{size}}
          viewBox={{`0 0 ${{size}} ${{size}}`}}
          style={{indeterminate ? {{ animation: 'spin 1.4s linear infinite' }} : undefined}}
        >
          <circle cx={{size / 2}} cy={{size / 2}} r={{radius}} fill="none" stroke="var(--color-surface-container-highest)" strokeWidth={{stroke}} />
          <circle
            cx={{size / 2}}
            cy={{size / 2}}
            r={{radius}}
            fill="none"
            stroke="var(--color-primary)"
            strokeWidth={{stroke}}
            strokeDasharray={{circumference}}
            strokeDashoffset={{offset}}
            strokeLinecap="round"
            transform={{`rotate(-90 ${{size / 2}} ${{size / 2}})`}}
            style={{{{ transition: indeterminate ? 'none' : 'stroke-dashoffset 0.3s ease' }}}}
          />
        </svg>
        <style>{{`@keyframes spin {{ to {{ transform: rotate(360deg); }} }}`}}</style>
      </div>
    );
  }}

  return (
    <div
      role="progressbar"
      aria-valuenow={{indeterminate ? undefined : value}}
      aria-valuemin={{0}}
      aria-valuemax={{100}}
      style={{{{
        width: '100%',
        height: '4px',
        backgroundColor: 'var(--color-surface-container-highest)',
        borderRadius: 'var(--radius-full)',
        overflow: 'hidden',
      }}}}
      {{...props}}
    >
      <div
        style={{{{
          height: '100%',
          backgroundColor: 'var(--color-primary)',
          borderRadius: 'var(--radius-full)',
          width: indeterminate ? '30%' : `${{value}}%`,
          transition: indeterminate ? 'none' : 'width 0.3s ease',
          animation: indeterminate ? 'indeterminate 1.5s ease-in-out infinite' : 'none',
        }}}}
      />
      {{indeterminate && (
        <style>{{`@keyframes indeterminate {{ 0% {{ margin-left: -30%; }} 100% {{ margin-left: 100%; }} }}`}}</style>
      )}}
    </div>
  );
}}
'''


def generate_skeleton_jsx(typescript: bool = False) -> str:
    props_interface = """
interface SkeletonProps {
  variant?: 'text' | 'rectangular' | 'circular';
  width?: string | number;
  height?: string | number;
  lines?: number;
  [key: string]: unknown;
}
""" if typescript else ""

    comp_sig = "Skeleton({ variant = 'text', width, height, lines = 1, ...props }: SkeletonProps)" if typescript else "Skeleton({ variant = 'text', width, height, lines = 1, ...props })"
    css_type = ": React.CSSProperties" if typescript else ""

    return f'''import React from 'react';
import './theme.css';
{props_interface}
export default function {comp_sig} {{
  const baseStyle{css_type} = {{
    backgroundColor: 'var(--color-surface-container-highest)',
    animation: 'skeleton-pulse 1.5s ease-in-out infinite',
  }};

  if (variant === 'circular') {{
    const size = width || height || '40px';
    return (
      <>
        <div style={{{{ ...baseStyle, width: size, height: size, borderRadius: 'var(--radius-full)' }}}} aria-hidden="true" {{...props}} />
        <style>{{`@keyframes skeleton-pulse {{ 0%, 100% {{ opacity: 1; }} 50% {{ opacity: 0.4; }} }}`}}</style>
      </>
    );
  }}

  if (variant === 'rectangular') {{
    return (
      <>
        <div
          style={{{{ ...baseStyle, width: width || '100%', height: height || '120px', borderRadius: 'var(--radius-medium)' }}}}
          aria-hidden="true"
          {{...props}}
        />
        <style>{{`@keyframes skeleton-pulse {{ 0%, 100% {{ opacity: 1; }} 50% {{ opacity: 0.4; }} }}`}}</style>
      </>
    );
  }}

  return (
    <>
      <div style={{{{ display: 'flex', flexDirection: 'column', gap: 'var(--spacing-2)', width: width || '100%' }}}} aria-hidden="true" {{...props}}>
        {{Array.from({{ length: lines }}).map((_, i) => (
          <div
            key={{i}}
            style={{{{
              ...baseStyle,
              height: height || '16px',
              borderRadius: 'var(--radius-extra-small)',
              width: i === lines - 1 && lines > 1 ? '75%' : '100%',
            }}}}
          />
        ))}}
      </div>
      <style>{{`@keyframes skeleton-pulse {{ 0%, 100% {{ opacity: 1; }} 50% {{ opacity: 0.4; }} }}`}}</style>
    </>
  );
}}
'''


def generate_container_jsx(typescript: bool = False) -> str:
    props_interface = """
interface ContainerProps {
  maxWidth?: 'sm' | 'md' | 'lg' | 'xl' | 'full';
  children?: React.ReactNode;
  style?: React.CSSProperties;
  [key: string]: unknown;
}
""" if typescript else ""

    comp_sig = "Container({ maxWidth = 'lg', children, style, ...props }: ContainerProps)" if typescript else "Container({ maxWidth = 'lg', children, style, ...props })"

    return f'''import React from 'react';
import './theme.css';
{props_interface}
const maxWidths = {{
  sm: '640px',
  md: '768px',
  lg: '1024px',
  xl: '1280px',
  full: '100%',
}};

export default function {comp_sig} {{
  return (
    <div
      style={{{{
        maxWidth: maxWidths[maxWidth],
        marginLeft: 'auto',
        marginRight: 'auto',
        paddingLeft: 'var(--spacing-4)',
        paddingRight: 'var(--spacing-4)',
        width: '100%',
        ...style,
      }}}}
      {{...props}}
    >
      {{children}}
    </div>
  );
}}
'''


def generate_grid_jsx(typescript: bool = False) -> str:
    props_interface = """
interface GridProps {
  columns?: number | string;
  gap?: string;
  children?: React.ReactNode;
  style?: React.CSSProperties;
  [key: string]: unknown;
}
""" if typescript else ""

    comp_sig = "Grid({ columns = 12, gap = 'var(--spacing-4)', children, style, ...props }: GridProps)" if typescript else "Grid({ columns = 12, gap = 'var(--spacing-4)', children, style, ...props })"

    item_interface = """
interface GridItemProps {
  span?: number;
  children?: React.ReactNode;
  style?: React.CSSProperties;
  [key: string]: unknown;
}
""" if typescript else ""

    item_sig = "({ span = 1, children, style, ...props }: GridItemProps)" if typescript else "({ span = 1, children, style, ...props })"

    return f'''import React from 'react';
import './theme.css';
{props_interface}{item_interface}
export default function {comp_sig} {{
  const gridTemplate = typeof columns === 'number' ? `repeat(${{columns}}, 1fr)` : columns;

  return (
    <div
      style={{{{
        display: 'grid',
        gridTemplateColumns: gridTemplate,
        gap,
        ...style,
      }}}}
      {{...props}}
    >
      {{children}}
    </div>
  );
}}

Grid.Item = function GridItem{item_sig} {{
  return (
    <div style={{{{ gridColumn: `span ${{span}}`, ...style }}}} {{...props}}>
      {{children}}
    </div>
  );
}};
'''


def generate_stack_jsx(typescript: bool = False) -> str:
    props_interface = """
interface StackProps {
  direction?: 'row' | 'column';
  gap?: string;
  align?: React.CSSProperties['alignItems'];
  justify?: React.CSSProperties['justifyContent'];
  wrap?: boolean;
  children?: React.ReactNode;
  style?: React.CSSProperties;
  [key: string]: unknown;
}
""" if typescript else ""

    comp_sig = "Stack({ direction = 'column', gap = 'var(--spacing-4)', align, justify, wrap, children, style, ...props }: StackProps)" if typescript else "Stack({ direction = 'column', gap = 'var(--spacing-4)', align, justify, wrap, children, style, ...props })"

    return f'''import React from 'react';
import './theme.css';
{props_interface}
export default function {comp_sig} {{
  return (
    <div
      style={{{{
        display: 'flex',
        flexDirection: direction,
        gap,
        alignItems: align,
        justifyContent: justify,
        flexWrap: wrap ? 'wrap' : undefined,
        ...style,
      }}}}
      {{...props}}
    >
      {{children}}
    </div>
  );
}}
'''


def generate_surface_jsx(typescript: bool = False) -> str:
    props_interface = """
interface SurfaceProps {
  level?: 0 | 1 | 2 | 3 | 4 | 5;
  children?: React.ReactNode;
  style?: React.CSSProperties;
  [key: string]: unknown;
}
""" if typescript else ""

    comp_sig = "Surface({ level = 0, children, style, ...props }: SurfaceProps)" if typescript else "Surface({ level = 0, children, style, ...props })"
    map_type = ": Record<number, string>" if typescript else ""

    return f'''import React from 'react';
import './theme.css';
{props_interface}
const levelMap{map_type} = {{
  0: 'var(--color-surface)',
  1: 'var(--color-surface-container-lowest)',
  2: 'var(--color-surface-container-low)',
  3: 'var(--color-surface-container)',
  4: 'var(--color-surface-container-high)',
  5: 'var(--color-surface-container-highest)',
}};

export default function {comp_sig} {{
  return (
    <div
      style={{{{
        backgroundColor: levelMap[level],
        color: 'var(--color-on-surface)',
        borderRadius: 'var(--radius-medium)',
        padding: 'var(--spacing-4)',
        fontFamily: 'var(--font-plain)',
        ...style,
      }}}}
      {{...props}}
    >
      {{children}}
    </div>
  );
}}
'''


# ── Component sets and filename mappings ──

COMPONENT_SETS = {
    'core': ['button', 'card', 'input', 'chip', 'badge', 'avatar', 'divider'],
    'navigation': ['appbar', 'tabs', 'sidebar', 'breadcrumb', 'bottomnav'],
    'data': ['table', 'list', 'datacard', 'stat'],
    'feedback': ['dialog', 'snackbar', 'tooltip', 'progress', 'skeleton'],
    'layout': ['container', 'grid', 'stack', 'surface'],
}

COMPONENT_FILENAMES = {
    'appbar': 'AppBar',
    'bottomnav': 'BottomNav',
    'datacard': 'DataCard',
}


def _component_display_name(name: str) -> str:
    """Return the PascalCase filename for a component."""
    if name in COMPONENT_FILENAMES:
        return COMPONENT_FILENAMES[name]
    return name.capitalize()


def generate_index_js(components: list, typescript: bool = False) -> str:
    ext = "tsx" if typescript else "jsx"
    lines = ["// Design System Components — Auto-generated"]
    set_order = ['core', 'navigation', 'data', 'feedback', 'layout']
    comp_set = set(components)
    for s in set_order:
        members = [c for c in COMPONENT_SETS.get(s, []) if c in comp_set]
        if members:
            lines.append(f"// {s.capitalize()}")
            for comp in members:
                display = _component_display_name(comp)
                lines.append(f"export {{ default as {display} }} from './{display}';")
    # Any remaining components not in a set
    covered = set()
    for s in set_order:
        covered.update(COMPONENT_SETS.get(s, []))
    extras = [c for c in components if c not in covered]
    for comp in extras:
        display = _component_display_name(comp)
        lines.append(f"export {{ default as {display} }} from './{display}';")
    return "\n".join(lines) + "\n"


STORYBOOK_VARIANTS = {
    "button": ["Filled", "Outlined", "Tonal", "Text"],
    "card": ["Elevated", "Filled", "Outlined"],
    "input": ["Outlined", "Filled"],
    "chip": ["Default", "Selected"],
    "badge": ["Dot", "WithCount"],
    "avatar": ["Initials", "Image"],
    "divider": ["Horizontal", "Vertical"],
    "appbar": ["Default", "Elevated"],
    "tabs": ["Default"],
    "sidebar": ["Default"],
    "breadcrumb": ["Default"],
    "bottomnav": ["Default"],
    "table": ["Default", "Striped"],
    "list": ["Default"],
    "datacard": ["Default", "WithTrend"],
    "stat": ["Default"],
    "dialog": ["Default"],
    "snackbar": ["Default", "WithAction"],
    "tooltip": ["Top", "Bottom"],
    "progress": ["Linear", "Circular", "Indeterminate"],
    "skeleton": ["Text", "Rectangular", "Circular"],
    "container": ["Default"],
    "grid": ["Default"],
    "stack": ["Row", "Column"],
    "surface": ["Default"],
}

STORYBOOK_STORY_ARGS = {
    "button": {
        "Filled": "args={{ variant: 'filled', children: 'Click me' }}",
        "Outlined": "args={{ variant: 'outlined', children: 'Click me' }}",
        "Tonal": "args={{ variant: 'tonal', children: 'Click me' }}",
        "Text": "args={{ variant: 'text', children: 'Click me' }}",
    },
    "card": {
        "Elevated": "args={{ variant: 'elevated', children: 'Card content' }}",
        "Filled": "args={{ variant: 'filled', children: 'Card content' }}",
        "Outlined": "args={{ variant: 'outlined', children: 'Card content' }}",
    },
    "chip": {
        "Default": "args={{ label: 'Chip', selected: false }}",
        "Selected": "args={{ label: 'Chip', selected: true }}",
    },
    "badge": {
        "Dot": "args={{ children: <span>Icon</span> }}",
        "WithCount": "args={{ count: 5, children: <span>Icon</span> }}",
    },
    "avatar": {
        "Initials": "args={{ name: 'Ada Lovelace' }}",
        "Image": "args={{ name: 'Ada Lovelace', src: 'https://i.pravatar.cc/80' }}",
    },
    "input": {
        "Outlined": "args={{ label: 'Email', variant: 'outlined' }}",
        "Filled": "args={{ label: 'Email', variant: 'filled' }}",
    },
    "divider": {
        "Horizontal": "args={{}}",
        "Vertical": "args={{ vertical: true }}",
    },
    "appbar": {
        "Default": "args={{ title: 'Page Title' }}",
        "Elevated": "args={{ title: 'Page Title', elevated: true }}",
    },
    "table": {
        "Default": "args={{ columns: [{ key: 'name', header: 'Name' }], data: [{ name: 'Row 1' }] }}",
        "Striped": "args={{ columns: [{ key: 'name', header: 'Name' }], data: [{ name: 'Row 1' }, { name: 'Row 2' }], striped: true }}",
    },
    "datacard": {
        "Default": "args={{ title: 'Metric', value: '1,234' }}",
        "WithTrend": "args={{ title: 'Metric', value: '1,234', trend: 'up', trendValue: '12%' }}",
    },
    "snackbar": {
        "Default": "args={{ message: 'Item saved' }}",
        "WithAction": "args={{ message: 'Item saved', action: { label: 'Undo', onClick: () => {} } }}",
    },
    "progress": {
        "Linear": "args={{ value: 65, variant: 'linear' }}",
        "Circular": "args={{ value: 65, variant: 'circular' }}",
        "Indeterminate": "args={{ indeterminate: true }}",
    },
    "skeleton": {
        "Text": "args={{ variant: 'text', lines: 3 }}",
        "Rectangular": "args={{ variant: 'rectangular' }}",
        "Circular": "args={{ variant: 'circular' }}",
    },
    "stack": {
        "Row": "args={{ direction: 'row', children: 'Items' }}",
        "Column": "args={{ direction: 'column', children: 'Items' }}",
    },
}


def generate_story(component_name: str, typescript: bool = False) -> str:
    name = _component_display_name(component_name)
    variants = STORYBOOK_VARIANTS.get(component_name, ["Default"])
    story_args = STORYBOOK_STORY_ARGS.get(component_name, {})
    ext = "tsx" if typescript else "jsx"

    story_lines = [
        f"import type {{ Meta, StoryObj }} from '@storybook/react';" if typescript else "",
        f"import {name} from './{name}';",
        "",
        f"const meta{'  : Meta<typeof ' + name + '>' if typescript else ''} = {{",
        f"  title: 'Components/{name}',",
        f"  component: {name},",
        "  tags: ['autodocs'],",
        "};",
        "",
        "export default meta;",
    ]
    if typescript:
        story_lines.append(f"type Story = StoryObj<typeof {name}>;")
    story_lines.append("")

    for variant in variants:
        args_str = story_args.get(variant, "args={{}}")
        if typescript:
            story_lines.append(f"export const {variant}: Story = {{ {args_str} }};")
        else:
            story_lines.append(f"export const {variant} = {{ {args_str} }};")

    return "\n".join(l for l in story_lines if l is not None) + "\n"


def generate_readme(theme_name: str, components: list, typescript: bool = False) -> str:
    ext = "tsx" if typescript else "jsx"
    index_ext = "ts" if typescript else "js"
    comp_set = set(components)

    # Build grouped tables
    sections = []
    set_order = ['core', 'navigation', 'data', 'feedback', 'layout']
    set_labels = {'core': 'Core', 'navigation': 'Navigation', 'data': 'Data', 'feedback': 'Feedback', 'layout': 'Layout'}
    for s in set_order:
        members = [c for c in COMPONENT_SETS.get(s, []) if c in comp_set]
        if members:
            rows = []
            for comp in members:
                name = _component_display_name(comp)
                variants = ", ".join(STORYBOOK_VARIANTS.get(comp, ["Default"]))
                rows.append(f"| {name} | {variants} |")
            sections.append(f"### {set_labels[s]}\n| Component | Variants |\n|-----------|----------|\n" + "\n".join(rows))

    component_tables = "\n\n".join(sections)

    import_names = [_component_display_name(c) for c in components[:4]]
    import_example = ", ".join(import_names)

    return f"""# {theme_name} Component Library

Strict Material Design 3 token set. Generated by the `tokens-to-components` skill from DTCG design tokens.

## Setup

1. Include `theme.css` in your app root:
   ```js
   import './components/theme.css';
   ```
2. Install peer dependencies: `react`, `react-dom`{"`, `typescript`" if typescript else ""}

## Usage

```{"tsx" if typescript else "jsx"}
import {{ {import_example} }} from './components';

<Button variant="filled" onClick={{() => {{}}}}>Save</Button>
<Card variant="elevated"><Card.Header title="Hello" /></Card>
```

## Token Requirements

This library requires the following CSS custom properties (from `theme.css`):
- `--color-*` — from `color.sys.light.*` / `color.sys.dark.*` token groups
- `--font-brand`, `--font-plain` — from `typography.ref.typeface.*`
- `--radius-*` — from `shape.corner.*`
- `--spacing-*` — from `spacing.*`

## Components

{component_tables}

## Files

- `theme.css` — CSS custom properties + M3 state layer classes + Google Fonts import
- `index.{index_ext}` — barrel export of all {len(components)} components
- `preview.html` — visual catalog, open in browser for QA
{"- `*.stories.tsx` — Storybook stories for each component" if typescript else ""}

## Design Token Source

Token files in the parent directory (`color.tokens.json`, `typography.tokens.json`, etc.)
are in W3C DTCG format.
"""


def generate_preview_html(tokens: dict, components: list, theme_name: str = "") -> str:
    """Generate an M3-compliant HTML preview showing all generated components."""
    brand_font = get_val(tokens, "typography.ref.typeface.brand", "sans-serif")
    plain_font = get_val(tokens, "typography.ref.typeface.plain", "sans-serif")

    # Collect light/dark colors
    light_colors = {}
    for key, token in tokens.items():
        if key.startswith("color.sys.light."):
            role = key.replace("color.sys.light.", "")
            val = token.get("$value", "")
            if isinstance(val, str):
                light_colors[role] = val

    dark_colors = {}
    for key, token in tokens.items():
        if key.startswith("color.sys.dark."):
            role = key.replace("color.sys.dark.", "")
            val = token.get("$value", "")
            if isinstance(val, str):
                dark_colors[role] = val

    shape_tokens = {}
    for key, token in tokens.items():
        if key.startswith("shape.corner."):
            name = key.replace("shape.corner.", "")
            val = token.get("$value", "")
            if isinstance(val, str):
                shape_tokens[name] = val

    spacing_tokens = {}
    for key, token in tokens.items():
        if key.startswith("spacing."):
            name = key.replace("spacing.", "")
            val = token.get("$value", "")
            if isinstance(val, str):
                spacing_tokens[name] = val

    # Detect extended colors
    m3_standard_roles = {
        "primary", "on-primary", "primary-container", "on-primary-container",
        "primary-fixed", "primary-fixed-dim", "on-primary-fixed", "on-primary-fixed-variant",
        "secondary", "on-secondary", "secondary-container", "on-secondary-container",
        "tertiary", "on-tertiary", "tertiary-container", "on-tertiary-container",
        "error", "on-error", "error-container", "on-error-container",
        "surface", "on-surface", "surface-variant", "on-surface-variant",
        "surface-container-lowest", "surface-container-low", "surface-container",
        "surface-container-high", "surface-container-highest",
        "outline", "outline-variant",
        "inverse-surface", "inverse-on-surface", "inverse-primary",
        "scrim", "shadow",
    }
    extended_names = set()
    for role in light_colors:
        if role not in m3_standard_roles and not role.startswith("on-") and not role.endswith("-container"):
            if f"{role}-container" in light_colors:
                extended_names.add(role)

    comp_set = set(components)

    # Detect expressive mode via color-component-map in token metadata ($extensions)
    color_component_map = {}
    for key, token in tokens.items():
        if "$extensions" in key and isinstance(token, dict):
            ccm = token.get("color-component-map", {})
            if isinstance(ccm, dict):
                color_component_map = {k: v for k, v in ccm.items()
                                       if isinstance(v, str) and not k.startswith("$")}
    is_expressive = bool(extended_names) and bool(color_component_map)

    # Helper: get extended color CSS var for a component slot, with fallback
    def ext_color(slot, fallback_base="secondary"):
        """Return (base, on, container, on-container) CSS var names for a slot."""
        if is_expressive and slot in color_component_map:
            name = color_component_map[slot]
            return (f"var(--color-{name})", f"var(--color-on-{name})",
                    f"var(--color-{name}-container)", f"var(--color-on-{name}-container)")
        return (f"var(--color-{fallback_base})", f"var(--color-on-{fallback_base})",
                f"var(--color-{fallback_base}-container)", f"var(--color-on-{fallback_base}-container)")

    # Build CSS vars
    light_vars = "\n".join(f"    --color-{k}: {v};" for k, v in sorted(light_colors.items()))
    dark_vars = "\n".join(f"    --color-{k}: {v};" for k, v in sorted(dark_colors.items()))
    shape_vars = "\n".join(f"    --radius-{k}: {v};" for k, v in sorted(shape_tokens.items()))
    spacing_vars = "\n".join(f"    --spacing-{k}: {v};" for k, v in sorted(spacing_tokens.items()))

    title = theme_name or "Design System Preview"
    mode_label = "Expressive" if is_expressive else "M3"
    subtitle = f"{len(components)} components" if not theme_name else f"{mode_label} design system &middot; {len(components)} components &middot; Light &amp; Dark"

    # Proportion bar (stored inside $extensions metadata)
    proportions = {}
    for key, token in tokens.items():
        if "$extensions" in key and isinstance(token, dict):
            pp = token.get("painting-proportions", {})
            if isinstance(pp, dict):
                proportions = {k: v for k, v in pp.items() if isinstance(v, (int, float))}
    proportion_html = ""
    if proportions:
        role_to_color = {"primary": "var(--color-primary)", "secondary": "var(--color-secondary)", "tertiary": "var(--color-tertiary)", "neutral": "var(--color-outline)", "accent": "var(--color-tertiary-container)"}
        segs = []
        for role, pct in sorted(proportions.items(), key=lambda x: -x[1]):
            color = role_to_color.get(role, "var(--color-outline)")
            w = pct * 100
            segs.append(f'<div style="width:{w}%;background:{color};height:100%;display:flex;align-items:center;justify-content:center;font-size:11px;font-weight:500;color:white;text-shadow:0 1px 2px rgba(0,0,0,0.5);min-width:40px;" title="{role}: {w:.0f}%">{role}<br>{w:.0f}%</div>')
        proportion_html = '\n  <div class="section" style="grid-column:1/-1;">\n    <h2>Painting Color Proportions</h2>\n    <div style="display:flex;height:48px;border-radius:var(--radius-medium);overflow:hidden;border:1px solid var(--color-outline-variant);">\n      ' + "".join(segs) + '\n    </div>\n  </div>'

    # Extended colors HTML
    extended_html = ""
    if extended_names:
        ext_cards = []
        for ext in sorted(extended_names):
            label = ext.replace("-", " ").title()
            ext_cards.append(f'<div style="border-radius:var(--radius-small);overflow:hidden;"><div style="background:var(--color-{ext});color:var(--color-on-{ext});padding:12px;font-size:13px;font-weight:500;">{label}</div><div style="background:var(--color-{ext}-container);color:var(--color-on-{ext}-container);padding:8px 12px;font-size:10px;">Container</div></div>')
        extended_html = '\n  <div class="section" style="grid-column:1/-1;">\n    <h2>Extended Painting Colors</h2>\n    <div style="display:grid;grid-template-columns:repeat(auto-fill,minmax(140px,1fr));gap:12px;">\n      ' + "\n      ".join(ext_cards) + '\n    </div>\n  </div>'

    # Build component sections conditionally
    sections = []

    if 'button' in comp_set:
        sections.append("""
  <div class="section">
    <h2>Buttons</h2>
    <div class="section-label">Primary</div>
    <div class="component-row">
      <button class="btn btn-filled m3-interactive"><span class="material-symbols-outlined" style="font-size:18px;">add</span> Filled</button>
      <button class="btn btn-outlined m3-interactive">Outlined</button>
      <button class="btn btn-text m3-interactive">Text</button>
    </div>
    <div class="section-label">Secondary</div>
    <div class="component-row">
      <button class="btn m3-interactive" style="background:var(--color-secondary);color:var(--color-on-secondary);"><span class="material-symbols-outlined" style="font-size:18px;">eco</span> Filled</button>
      <button class="btn m3-interactive" style="background:transparent;color:var(--color-secondary);border:1px solid var(--color-secondary);">Outlined</button>
      <button class="btn btn-tonal m3-interactive">Tonal</button>
    </div>
    <div class="section-label">Tertiary</div>
    <div class="component-row">
      <button class="btn m3-interactive" style="background:var(--color-tertiary);color:var(--color-on-tertiary);"><span class="material-symbols-outlined" style="font-size:18px;">palette</span> Filled</button>
      <button class="btn m3-interactive" style="background:transparent;color:var(--color-tertiary);border:1px solid var(--color-tertiary);">Outlined</button>
      <button class="btn m3-interactive" style="background:var(--color-tertiary-container);color:var(--color-on-tertiary-container);">Tonal</button>
    </div>
    <div class="section-label">States</div>
    <div class="component-row">
      <button class="btn btn-filled m3-interactive">Enabled</button>
      <button class="btn btn-filled" disabled>Disabled</button>
    </div>
  </div>""")

    if 'card' in comp_set:
        card_accent, _, _, _ = ext_color("card-accent", "primary")
        accent_stripe = f'style="border-left:4px solid {card_accent};"' if is_expressive else ''
        sections.append(f"""
  <div class="section">
    <h2>Cards</h2>
    <div style="display:flex;flex-direction:column;gap:12px;">
      <div class="card card-elevated m3-interactive" {accent_stripe}><h3>Elevated Card</h3><p>Surface-container-low with M3 level 1 shadow.</p><div class="card-actions"><button class="btn btn-text m3-interactive">Learn More</button><button class="btn btn-filled m3-interactive">Action</button></div></div>
      <div class="card card-filled m3-interactive"><h3>Filled Card</h3><p>Surface-container-highest for a contained feel.</p></div>
      <div class="card card-outlined m3-interactive"><h3>Outlined Card</h3><p>Surface with outline-variant border.</p></div>
    </div>
  </div>""")

    if 'input' in comp_set:
        sections.append("""
  <div class="section" style="grid-column:1/-1;">
    <h2>Text Inputs</h2>
    <div style="display:grid;grid-template-columns:1fr 1fr;gap:24px;">
      <div><div class="section-label">Outlined</div><div class="input-outlined-wrap"><input class="input-field" placeholder=" " id="i-o1" /><label class="input-label-float" for="i-o1">Label</label></div><div class="input-supporting">Supporting text</div></div>
      <div><div class="section-label">Filled</div><div class="input-filled-wrap"><input class="input-field" placeholder=" " id="i-f1" /><label class="input-label-float" for="i-f1">Label</label></div><div class="input-supporting">Supporting text</div></div>
      <div><div class="section-label">With value</div><div class="input-outlined-wrap"><input class="input-field" placeholder=" " value="user@example.com" id="i-o2" /><label class="input-label-float" for="i-o2">Email</label></div></div>
      <div><div class="section-label">Error</div><div class="input-outlined-wrap input-error"><input class="input-field" placeholder=" " value="bad" id="i-e1" aria-invalid="true" aria-describedby="i-e1-h" /><label class="input-label-float" for="i-e1">Email</label></div><div class="input-supporting input-error-text" id="i-e1-h"><span class="material-symbols-outlined" style="font-size:14px;vertical-align:-2px;">error</span> Invalid email</div></div>
    </div>
  </div>""")

    if 'chip' in comp_set:
        _, _, chip_container, chip_on_container = ext_color("chip-selected", "secondary")
        sections.append(f"""
  <div class="section">
    <h2>Chips</h2>
    <div class="section-label">Click to toggle</div>
    <div class="component-row">
      <div class="chip chip-unselected m3-interactive" role="option" aria-selected="false" tabindex="0" onclick="toggleChip(this)" onkeydown="if(event.key==='Enter'||event.key===' '){{event.preventDefault();toggleChip(this);}}"><span class="material-symbols-outlined" style="font-size:18px;">palette</span> Category A</div>
      <div class="chip chip-selected m3-interactive" role="option" aria-selected="true" tabindex="0" onclick="toggleChip(this)" onkeydown="if(event.key==='Enter'||event.key===' '){{event.preventDefault();toggleChip(this);}}" style="background:{chip_container};color:{chip_on_container};border-color:transparent;"><span class="material-symbols-outlined" style="font-size:18px;">check</span> Category B</div>
      <div class="chip chip-unselected m3-interactive" role="option" aria-selected="false" tabindex="0" onclick="toggleChip(this)" onkeydown="if(event.key==='Enter'||event.key===' '){{event.preventDefault();toggleChip(this);}}"><span class="material-symbols-outlined" style="font-size:18px;">brush</span> Category C</div>
    </div>
  </div>""")

    # Avatar, Badge, Tooltip combined
    ab_items = []
    ab_titles = []
    if 'avatar' in comp_set:
        ab_titles.append("Avatar")
        ab_items += ['<div class="avatar avatar-sm">A</div>', '<div class="avatar">VG</div>', '<div class="avatar avatar-lg" style="background:var(--color-secondary-container);color:var(--color-on-secondary-container);">CM</div>', '<div class="avatar" style="background:var(--color-tertiary-container);color:var(--color-on-tertiary-container);">DK</div>']
    if 'badge' in comp_set:
        ab_titles.append("Badge")
        badge_base, badge_on, _, _ = ext_color("badge", "error")
        ab_items += [
            f'<div class="badge-wrap"><div class="avatar">EF</div><span class="badge-dot" style="background:{badge_base};"></span></div>',
            f'<div class="badge-wrap"><div class="avatar">GH</div><span class="badge-count" style="background:{badge_base};color:{badge_on};">3</span></div>'
        ]
    if 'tooltip' in comp_set:
        ab_titles.append("Tooltip")
        ab_items.append('<div class="tooltip-wrap" tabindex="0"><div class="avatar" style="background:var(--color-tertiary-container);color:var(--color-on-tertiary-container);"><span class="material-symbols-outlined" style="font-size:20px;">info</span></div><div class="tooltip-bubble">Hover or focus for tooltip</div></div>')
    if ab_items:
        sections.append(f'''\n  <div class="section">\n    <h2>{" &amp; ".join(ab_titles)}</h2>\n    <div class="component-row">\n      {' '.join(ab_items)}\n    </div>\n  </div>''')

    if 'divider' in comp_set:
        sections.append("""
  <div class="section">
    <h2>Divider</h2>
    <div style="display:flex;flex-direction:column;gap:16px;">
      <p style="font-size:14px;color:var(--color-on-surface-variant);">Content above</p>
      <hr style="border:none;height:1px;background:var(--color-outline-variant);">
      <p style="font-size:14px;color:var(--color-on-surface-variant);">Content below</p>
      <hr style="border:none;height:1px;background:var(--color-outline-variant);margin-left:var(--spacing-4);">
      <p style="font-size:14px;color:var(--color-on-surface-variant);">Inset divider (16px)</p>
    </div>
  </div>""")

    if 'appbar' in comp_set:
        sections.append("""
  <div class="section" style="grid-column:1/-1;">
    <h2>App Bar</h2>
    <div style="border-radius:var(--radius-medium);overflow:hidden;border:1px solid var(--color-outline-variant);">
      <div style="display:flex;align-items:center;height:64px;padding:0 var(--spacing-4);gap:var(--spacing-2);background:var(--color-surface);">
        <button class="m3-interactive" style="border:none;background:none;cursor:pointer;padding:8px;border-radius:var(--radius-full);color:var(--color-on-surface-variant);display:flex;"><span class="material-symbols-outlined">menu</span></button>
        <span style="flex:1;font-family:var(--font-brand);font-size:22px;line-height:28px;">Page Title</span>
        <button class="m3-interactive" style="border:none;background:none;cursor:pointer;padding:8px;border-radius:var(--radius-full);color:var(--color-on-surface-variant);display:flex;"><span class="material-symbols-outlined">search</span></button>
        <button class="m3-interactive" style="border:none;background:none;cursor:pointer;padding:8px;border-radius:var(--radius-full);color:var(--color-on-surface-variant);display:flex;"><span class="material-symbols-outlined">more_vert</span></button>
      </div>
    </div>
  </div>""")

    if 'tabs' in comp_set:
        sections.append("""
  <div class="section" style="grid-column:1/-1;">
    <h2>Tabs</h2>
    <div class="section-label">Click to switch</div>
    <div style="display:flex;background:var(--color-surface-container);border-radius:var(--radius-medium);overflow:hidden;" role="tablist">
      <button class="tab-btn m3-interactive" role="tab" aria-selected="true" onclick="selectTab(this)"><span class="material-symbols-outlined" style="font-size:20px;">palette</span> Gallery</button>
      <button class="tab-btn m3-interactive" role="tab" aria-selected="false" onclick="selectTab(this)"><span class="material-symbols-outlined" style="font-size:20px;">brush</span> Studio</button>
      <button class="tab-btn m3-interactive" role="tab" aria-selected="false" onclick="selectTab(this)"><span class="material-symbols-outlined" style="font-size:20px;">sell</span> Auction</button>
    </div>
  </div>""")

    if 'sidebar' in comp_set:
        _, _, sidebar_container, sidebar_on_container = ext_color("sidebar-active", "secondary")
        sidebar_active_style = f'background:{sidebar_container};color:{sidebar_on_container};' if is_expressive else ''
        sections.append(f"""
  <div class="section">
    <h2>Sidebar</h2>
    <nav style="background:var(--color-surface-container);border-radius:var(--radius-medium);padding:var(--spacing-3);display:flex;flex-direction:column;gap:var(--spacing-1);max-width:280px;">
      <button class="sidebar-item m3-interactive" aria-selected="true" onclick="selectSidebar(this)" {'style="' + sidebar_active_style + '"' if sidebar_active_style else ''}><span class="material-symbols-outlined">dashboard</span> Dashboard</button>
      <button class="sidebar-item m3-interactive" aria-selected="false" onclick="selectSidebar(this)"><span class="material-symbols-outlined">folder</span> Projects</button>
      <button class="sidebar-item m3-interactive" aria-selected="false" onclick="selectSidebar(this)"><span class="material-symbols-outlined">settings</span> Settings</button>
    </nav>
  </div>""")

    if 'breadcrumb' in comp_set:
        sections.append("""
  <div class="section">
    <h2>Breadcrumb</h2>
    <nav aria-label="Breadcrumb">
      <ol style="display:flex;align-items:center;gap:var(--spacing-2);list-style:none;font-size:14px;">
        <li><a href="#" style="color:var(--color-primary);text-decoration:none;font-weight:500;" onclick="event.preventDefault();">Home</a></li>
        <li style="color:var(--color-on-surface-variant);">/</li>
        <li><a href="#" style="color:var(--color-primary);text-decoration:none;font-weight:500;" onclick="event.preventDefault();">Gallery</a></li>
        <li style="color:var(--color-on-surface-variant);">/</li>
        <li><span style="color:var(--color-on-surface);font-weight:500;" aria-current="page">Current Page</span></li>
      </ol>
    </nav>
  </div>""")

    if 'bottomnav' in comp_set:
        sections.append("""
  <div class="section" style="grid-column:1/-1;">
    <h2>Bottom Navigation</h2>
    <div style="display:flex;background:var(--color-surface-container);border-radius:var(--radius-medium);height:80px;overflow:hidden;">
      <button class="bnav-item m3-interactive" aria-selected="true" onclick="selectBnav(this)"><div class="bnav-pill"><span class="material-symbols-outlined">home</span></div><span>Home</span></button>
      <button class="bnav-item m3-interactive" aria-selected="false" onclick="selectBnav(this)"><div class="bnav-pill"><span class="material-symbols-outlined">search</span></div><span>Search</span></button>
      <button class="bnav-item m3-interactive" aria-selected="false" onclick="selectBnav(this)"><div class="bnav-pill"><span class="material-symbols-outlined">favorite</span></div><span>Favorites</span></button>
      <button class="bnav-item m3-interactive" aria-selected="false" onclick="selectBnav(this)"><div class="bnav-pill"><span class="material-symbols-outlined">settings</span></div><span>Settings</span></button>
    </div>
  </div>""")

    if 'table' in comp_set:
        sections.append("""
  <div class="section" style="grid-column:1/-1;">
    <h2>Table</h2>
    <div style="border-radius:var(--radius-medium);overflow:hidden;border:1px solid var(--color-outline-variant);">
      <table class="data-table"><thead><tr style="background:var(--color-surface-container);"><th>Name</th><th>Category</th><th style="text-align:right;">Value</th></tr></thead>
      <tbody><tr><td>Item Alpha</td><td><span style="display:inline-flex;align-items:center;gap:6px;"><span style="width:10px;height:10px;border-radius:50%;background:var(--color-primary);"></span> Primary</span></td><td style="text-align:right;">$1,234</td></tr><tr><td>Item Beta</td><td><span style="display:inline-flex;align-items:center;gap:6px;"><span style="width:10px;height:10px;border-radius:50%;background:var(--color-secondary);"></span> Secondary</span></td><td style="text-align:right;">$5,678</td></tr><tr><td>Item Gamma</td><td><span style="display:inline-flex;align-items:center;gap:6px;"><span style="width:10px;height:10px;border-radius:50%;background:var(--color-tertiary);"></span> Tertiary</span></td><td style="text-align:right;">$9,012</td></tr></tbody></table>
    </div>
  </div>""")

    if 'list' in comp_set:
        sections.append("""
  <div class="section">
    <h2>List</h2>
    <div style="border-radius:var(--radius-medium);overflow:hidden;">
      <div class="list-item" style="cursor:pointer;"><div class="avatar">AB</div><div style="flex:1;min-width:0;"><div style="font-size:16px;">Primary Text</div><div style="font-size:14px;color:var(--color-on-surface-variant);">Secondary text</div></div><span class="material-symbols-outlined" style="color:var(--color-on-surface-variant);">chevron_right</span></div>
      <hr style="border:none;height:1px;background:var(--color-outline-variant);margin:0 var(--spacing-4);">
      <div class="list-item" style="cursor:pointer;"><div class="avatar" style="background:var(--color-secondary-container);color:var(--color-on-secondary-container);">CD</div><div style="flex:1;min-width:0;"><div style="font-size:16px;">Another Item</div><div style="font-size:14px;color:var(--color-on-surface-variant);">Description</div></div><span class="material-symbols-outlined" style="color:var(--color-on-surface-variant);">chevron_right</span></div>
    </div>
  </div>""")

    # DataCard & Stat
    dc_parts = []
    dc_titles = []
    if 'datacard' in comp_set:
        dc_titles.append("Data Card")
        dc_parts.append('<div style="background:var(--color-surface-container-low);border-radius:var(--radius-medium);padding:var(--spacing-4);box-shadow:0 1px 2px rgba(0,0,0,0.3),0 1px 3px 1px rgba(0,0,0,0.15);"><div style="display:flex;justify-content:space-between;align-items:flex-start;margin-bottom:var(--spacing-3);"><span style="font-size:14px;font-weight:500;color:var(--color-on-surface-variant);">Metric</span><span class="material-symbols-outlined" style="color:var(--color-primary);">analytics</span></div><div style="font-size:32px;font-weight:700;font-family:var(--font-brand);line-height:40px;">2,100+</div><div style="display:flex;align-items:center;gap:var(--spacing-2);margin-top:var(--spacing-1);"><span style="font-size:14px;font-weight:500;color:var(--color-tertiary);"><span class="material-symbols-outlined" style="font-size:16px;vertical-align:-3px;">trending_up</span> 12%</span><span style="font-size:14px;color:var(--color-on-surface-variant);">from last period</span></div></div>')
    if 'stat' in comp_set:
        dc_titles.append("Stat")
        dc_parts.append('<div style="text-align:center;padding:var(--spacing-4);"><div style="font-size:12px;font-weight:500;color:var(--color-on-surface-variant);letter-spacing:0.5px;">TOTAL USERS</div><div style="font-size:45px;font-family:var(--font-brand);line-height:52px;">8.2M</div><div style="font-size:14px;color:var(--color-on-surface-variant);">Annual average</div></div>')
    if dc_parts:
        sections.append(f'''\n  <div class="section">\n    <h2>{" &amp; ".join(dc_titles)}</h2>\n    <div style="display:flex;flex-direction:column;gap:16px;">\n      {chr(10).join(dc_parts)}\n    </div>\n  </div>''')

    if 'dialog' in comp_set:
        sections.append("""
  <div class="section">
    <h2>Dialog</h2>
    <button class="btn btn-filled m3-interactive" onclick="document.getElementById('demo-dialog').classList.add('open');"><span class="material-symbols-outlined" style="font-size:18px;">open_in_new</span> Open Dialog</button>
    <div style="margin-top:16px;background:var(--color-surface-container-high);border-radius:var(--radius-extra-large);padding:var(--spacing-6);box-shadow:0 8px 32px rgba(0,0,0,0.16);max-width:400px;">
      <h3 style="font-family:var(--font-brand);font-size:24px;font-weight:400;margin-bottom:var(--spacing-4);"><span class="material-symbols-outlined" style="font-size:24px;vertical-align:-4px;color:var(--color-primary);margin-right:var(--spacing-2);">delete</span> Confirm Action</h3>
      <p style="font-size:14px;color:var(--color-on-surface-variant);line-height:20px;margin-bottom:var(--spacing-6);">Are you sure? This action cannot be undone.</p>
      <div style="display:flex;justify-content:flex-end;gap:var(--spacing-2);"><button class="btn btn-text m3-interactive">Cancel</button><button class="btn btn-filled m3-interactive" style="background:var(--color-error);color:var(--color-on-error);">Delete</button></div>
    </div>
  </div>""")

    if 'snackbar' in comp_set:
        sections.append("""
  <div class="section">
    <h2>Snackbar</h2>
    <button class="btn btn-outlined m3-interactive" onclick="showSnackbar()" style="margin-bottom:16px;"><span class="material-symbols-outlined" style="font-size:18px;">notifications</span> Show Snackbar</button>
    <div class="snackbar" id="demo-snackbar"><span class="material-symbols-outlined" style="font-size:20px;">check_circle</span><span style="flex:1;">Item saved successfully</span><button style="border:none;background:none;color:var(--color-inverse-primary);font-size:14px;font-weight:500;cursor:pointer;" onclick="hideSnackbar()">Undo</button><button style="border:none;background:none;color:var(--color-inverse-on-surface);cursor:pointer;display:flex;" onclick="hideSnackbar()" aria-label="Dismiss"><span class="material-symbols-outlined" style="font-size:20px;">close</span></button></div>
  </div>""")

    if 'progress' in comp_set:
        sections.append("""
  <div class="section">
    <h2>Progress</h2>
    <div style="display:flex;flex-direction:column;gap:24px;">
      <div><div class="section-label">Primary &mdash; 65%</div><div class="progress-track"><div class="progress-bar" style="width:65%;"></div></div></div>
      <div><div class="section-label">Secondary &mdash; 40%</div><div class="progress-track"><div class="progress-bar" style="width:40%;background:var(--color-secondary);"></div></div></div>
      <div><div class="section-label">Tertiary &mdash; 80%</div><div class="progress-track"><div class="progress-bar" style="width:80%;background:var(--color-tertiary);"></div></div></div>
      <div style="display:flex;align-items:center;gap:32px;">
        <div><div class="section-label">Circular &mdash; 65%</div><svg width="48" height="48" viewBox="0 0 48 48"><circle cx="24" cy="24" r="20" fill="none" stroke="var(--color-surface-container-highest)" stroke-width="4"/><circle cx="24" cy="24" r="20" fill="none" stroke="var(--color-primary)" stroke-width="4" stroke-dasharray="125.66" stroke-dashoffset="44" stroke-linecap="round" transform="rotate(-90 24 24)"/></svg></div>
        <div><div class="section-label">Circular &mdash; Indeterminate</div><svg width="48" height="48" viewBox="0 0 48 48" style="animation:spin 1.4s linear infinite;"><circle cx="24" cy="24" r="20" fill="none" stroke="var(--color-surface-container-highest)" stroke-width="4"/><circle cx="24" cy="24" r="20" fill="none" stroke="var(--color-primary)" stroke-width="4" stroke-dasharray="125.66" stroke-dashoffset="94" stroke-linecap="round" transform="rotate(-90 24 24)"/></svg></div>
      </div>
    </div>
  </div>""")

    if 'skeleton' in comp_set:
        sections.append("""
  <div class="section">
    <h2>Skeleton</h2>
    <div style="display:flex;gap:var(--spacing-4);align-items:flex-start;"><div class="skeleton" style="width:40px;height:40px;border-radius:50%;flex-shrink:0;"></div><div style="flex:1;display:flex;flex-direction:column;gap:var(--spacing-2);"><div class="skeleton" style="height:16px;width:40%;border-radius:var(--radius-extra-small);"></div><div class="skeleton" style="height:16px;width:100%;border-radius:var(--radius-extra-small);"></div><div class="skeleton" style="height:16px;width:75%;border-radius:var(--radius-extra-small);"></div></div></div>
    <div style="margin-top:var(--spacing-4);"><div class="skeleton" style="height:120px;width:100%;border-radius:var(--radius-medium);"></div></div>
  </div>""")

    if 'surface' in comp_set:
        sections.append("""
  <div class="section" style="grid-column:1/-1;">
    <h2>Surface Levels</h2>
    <div style="display:grid;grid-template-columns:repeat(6,1fr);gap:12px;">
      <div style="background:var(--color-surface);border-radius:var(--radius-medium);padding:var(--spacing-4);text-align:center;border:1px solid var(--color-outline-variant);"><div style="font-size:12px;font-weight:500;color:var(--color-on-surface-variant);">Level 0</div><div style="font-size:14px;">Surface</div></div>
      <div style="background:var(--color-surface-container-lowest);border-radius:var(--radius-medium);padding:var(--spacing-4);text-align:center;"><div style="font-size:12px;font-weight:500;color:var(--color-on-surface-variant);">Level 1</div><div style="font-size:14px;">Lowest</div></div>
      <div style="background:var(--color-surface-container-low);border-radius:var(--radius-medium);padding:var(--spacing-4);text-align:center;"><div style="font-size:12px;font-weight:500;color:var(--color-on-surface-variant);">Level 2</div><div style="font-size:14px;">Low</div></div>
      <div style="background:var(--color-surface-container);border-radius:var(--radius-medium);padding:var(--spacing-4);text-align:center;"><div style="font-size:12px;font-weight:500;color:var(--color-on-surface-variant);">Level 3</div><div style="font-size:14px;">Container</div></div>
      <div style="background:var(--color-surface-container-high);border-radius:var(--radius-medium);padding:var(--spacing-4);text-align:center;"><div style="font-size:12px;font-weight:500;color:var(--color-on-surface-variant);">Level 4</div><div style="font-size:14px;">High</div></div>
      <div style="background:var(--color-surface-container-highest);border-radius:var(--radius-medium);padding:var(--spacing-4);text-align:center;"><div style="font-size:12px;font-weight:500;color:var(--color-on-surface-variant);">Level 5</div><div style="font-size:14px;">Highest</div></div>
    </div>
  </div>""")

    component_sections = "".join(sections)

    # "In Context" composition — shows a mini app layout using extended colors
    in_context_html = ""
    if is_expressive and len(extended_names) >= 2:
        badge_base, badge_on, _, _ = ext_color("badge", "error")
        _, _, chip_c, chip_on_c = ext_color("chip-selected", "secondary")
        card_accent_c, _, _, _ = ext_color("card-accent", "primary")
        _, _, sidebar_c, sidebar_on_c = ext_color("sidebar-active", "secondary")
        ext_list = sorted(extended_names)
        # Build small tag chips from extended colors
        tag_chips = ""
        for i, ext in enumerate(ext_list[:4]):
            label = ext.replace("-", " ").title()
            tag_chips += f'<span style="display:inline-flex;align-items:center;height:26px;padding:0 10px;border-radius:var(--radius-full);background:var(--color-{ext}-container);color:var(--color-on-{ext}-container);font-size:11px;font-weight:500;gap:4px;">{label}</span>\n          '

        in_context_html = f'''
  <div class="section" style="grid-column:1/-1;">
    <h2>In Context &mdash; Expressive Colors</h2>
    <p style="font-size:14px;color:var(--color-on-surface-variant);margin-bottom:16px;">A mini app layout showing how extended painting colors enrich the UI beyond standard M3 roles.</p>
    <div style="display:grid;grid-template-columns:200px 1fr;gap:0;border-radius:var(--radius-medium);overflow:hidden;border:1px solid var(--color-outline-variant);min-height:320px;">
      <!-- Sidebar -->
      <div style="background:var(--color-surface-container);padding:var(--spacing-3);display:flex;flex-direction:column;gap:var(--spacing-1);">
        <div style="font-family:var(--font-brand);font-size:18px;padding:var(--spacing-2) var(--spacing-3);margin-bottom:var(--spacing-2);">Gallery</div>
        <div style="display:flex;align-items:center;gap:8px;padding:8px 12px;border-radius:var(--radius-full);background:{sidebar_c};color:{sidebar_on_c};font-size:13px;font-weight:600;"><span class="material-symbols-outlined" style="font-size:18px;">palette</span> Collection</div>
        <div style="display:flex;align-items:center;gap:8px;padding:8px 12px;border-radius:var(--radius-full);color:var(--color-on-surface-variant);font-size:13px;"><span class="material-symbols-outlined" style="font-size:18px;">brush</span> Studio</div>
        <div style="display:flex;align-items:center;gap:8px;padding:8px 12px;border-radius:var(--radius-full);color:var(--color-on-surface-variant);font-size:13px;"><span class="material-symbols-outlined" style="font-size:18px;">favorite</span> Favorites</div>
      </div>
      <!-- Main content -->
      <div style="padding:var(--spacing-4);display:flex;flex-direction:column;gap:var(--spacing-4);">
        <!-- Header with badge -->
        <div style="display:flex;justify-content:space-between;align-items:center;">
          <h3 style="font-family:var(--font-brand);font-size:22px;">Collection</h3>
          <div style="position:relative;display:inline-flex;">
            <span class="material-symbols-outlined" style="font-size:24px;color:var(--color-on-surface-variant);">notifications</span>
            <span style="position:absolute;top:-4px;right:-6px;min-width:16px;height:16px;border-radius:8px;background:{badge_base};color:{badge_on};font-size:10px;font-weight:600;display:flex;align-items:center;justify-content:center;padding:0 4px;">5</span>
          </div>
        </div>
        <!-- Filter chips -->
        <div style="display:flex;gap:8px;flex-wrap:wrap;">
          {tag_chips}
        </div>
        <!-- Content cards -->
        <div style="display:grid;grid-template-columns:1fr 1fr;gap:12px;">
          <div style="background:var(--color-surface-container-low);border-radius:var(--radius-medium);padding:var(--spacing-4);border-left:4px solid {card_accent_c};box-shadow:0 1px 2px rgba(0,0,0,0.15);">
            <div style="font-size:16px;font-weight:500;margin-bottom:4px;">Featured Work</div>
            <div style="font-size:13px;color:var(--color-on-surface-variant);line-height:18px;">Extended painting colors bring depth and atmosphere to every surface.</div>
          </div>
          <div style="background:var(--color-surface-container-low);border-radius:var(--radius-medium);padding:var(--spacing-4);box-shadow:0 1px 2px rgba(0,0,0,0.15);">
            <div style="font-size:16px;font-weight:500;margin-bottom:4px;">Recent Addition</div>
            <div style="font-size:13px;color:var(--color-on-surface-variant);line-height:18px;">Each color traced back to the source painting's palette.</div>
          </div>
        </div>
      </div>
    </div>
  </div>'''

    # Dialog overlay
    dialog_overlay = ""
    if 'dialog' in comp_set:
        dialog_overlay = """
<div class="dialog-scrim" id="demo-dialog" onclick="if(event.target===this)this.classList.remove('open');">
  <div class="dialog-surface" role="dialog" aria-labelledby="dialog-title" aria-modal="true">
    <h2 id="dialog-title" style="font-family:var(--font-brand);font-size:24px;font-weight:400;margin-bottom:var(--spacing-4);"><span class="material-symbols-outlined" style="font-size:24px;vertical-align:-4px;color:var(--color-primary);margin-right:var(--spacing-2);">info</span> About This Theme</h2>
    <p style="font-size:14px;color:var(--color-on-surface-variant);line-height:20px;margin-bottom:var(--spacing-6);">This design system preview shows all generated components using your design tokens.</p>
    <div style="display:flex;justify-content:flex-end;gap:var(--spacing-2);"><button class="btn btn-text m3-interactive" onclick="document.getElementById('demo-dialog').classList.remove('open');">Close</button><button class="btn btn-filled m3-interactive" onclick="document.getElementById('demo-dialog').classList.remove('open');">Got It</button></div>
  </div>
</div>"""

    # Combined shape + spacing showcase (condensed)
    shape_spacing_showcase = ""
    shape_items_html = ""
    spacing_items_html = ""
    if shape_tokens:
        items = []
        for name, val in sorted(shape_tokens.items()):
            items.append(f'<div style="text-align:center;"><div class="shape-sample" style="border-radius:var(--radius-{name});">{name[:2].upper()}</div><div style="font-size:10px;color:var(--color-on-surface-variant);margin-top:4px;">{name} {val}</div></div>')
        shape_items_html = '<div class="section-label">Shape</div><div style="display:flex;flex-wrap:wrap;gap:12px;margin-bottom:16px;">' + "".join(items) + '</div>'
    if spacing_tokens:
        rows = []
        def sort_key(x):
            try:
                return float(x[1].replace('px', ''))
            except ValueError:
                return 0
        for name, val in sorted(spacing_tokens.items(), key=sort_key):
            if name == '0': continue
            px = val.replace('px', '')
            rows.append(f'<div style="display:flex;align-items:center;gap:8px;"><div style="font-size:10px;color:var(--color-on-surface-variant);min-width:50px;font-variant-numeric:tabular-nums;">{name} &middot; {val}</div><div style="background:var(--color-primary);border-radius:2px;height:12px;width:{px}px;"></div></div>')
        spacing_items_html = '<div class="section-label">Spacing</div><div style="display:flex;flex-direction:column;gap:3px;">' + "".join(rows) + '</div>'
    if shape_items_html or spacing_items_html:
        shape_spacing_showcase = f'\n  <div class="section">\n    {shape_items_html}\n    {spacing_items_html}\n  </div>'

    # JavaScript
    js_parts = ["""
  function toggleTheme(btn) {
    var d = document.documentElement;
    if (d.getAttribute('data-theme') === 'dark') {
      d.removeAttribute('data-theme');
      btn.innerHTML = '<span class="material-symbols-outlined" style="font-size:18px;">dark_mode</span> Dark';
    } else {
      d.setAttribute('data-theme', 'dark');
      btn.innerHTML = '<span class="material-symbols-outlined" style="font-size:18px;">light_mode</span> Light';
    }
  }"""]

    if 'chip' in comp_set:
        if is_expressive:
            _, _, chip_c_js, chip_on_c_js = ext_color("chip-selected", "secondary")
            js_parts.append(f"""
  function toggleChip(el) {{
    var selected = el.getAttribute('aria-selected') === 'true';
    el.setAttribute('aria-selected', String(!selected));
    if (selected) {{
      el.classList.remove('chip-selected'); el.classList.add('chip-unselected');
      el.style.background = ''; el.style.color = ''; el.style.borderColor = '';
    }} else {{
      el.classList.remove('chip-unselected'); el.classList.add('chip-selected');
      el.style.background = '{chip_c_js}'; el.style.color = '{chip_on_c_js}'; el.style.borderColor = 'transparent';
    }}
  }}""")
        else:
            js_parts.append("""
  function toggleChip(el) {
    var selected = el.getAttribute('aria-selected') === 'true';
    el.setAttribute('aria-selected', String(!selected));
    if (selected) { el.classList.remove('chip-selected'); el.classList.add('chip-unselected'); }
    else { el.classList.remove('chip-unselected'); el.classList.add('chip-selected'); }
  }""")

    if 'tabs' in comp_set:
        js_parts.append("""
  function selectTab(el) {
    el.parentElement.querySelectorAll('[role="tab"]').forEach(function(t) { t.setAttribute('aria-selected', 'false'); });
    el.setAttribute('aria-selected', 'true');
  }""")

    if 'sidebar' in comp_set:
        if is_expressive:
            _, _, sb_c_js, sb_on_c_js = ext_color("sidebar-active", "secondary")
            js_parts.append(f"""
  function selectSidebar(el) {{
    el.parentElement.querySelectorAll('.sidebar-item').forEach(function(s) {{
      s.setAttribute('aria-selected', 'false');
      s.style.background = ''; s.style.color = '';
    }});
    el.setAttribute('aria-selected', 'true');
    el.style.background = '{sb_c_js}'; el.style.color = '{sb_on_c_js}';
  }}""")
        else:
            js_parts.append("""
  function selectSidebar(el) {
    el.parentElement.querySelectorAll('.sidebar-item').forEach(function(s) { s.setAttribute('aria-selected', 'false'); });
    el.setAttribute('aria-selected', 'true');
  }""")

    if 'bottomnav' in comp_set:
        js_parts.append("""
  function selectBnav(el) {
    el.parentElement.querySelectorAll('.bnav-item').forEach(function(b) { b.setAttribute('aria-selected', 'false'); });
    el.setAttribute('aria-selected', 'true');
  }""")

    if 'snackbar' in comp_set:
        js_parts.append("""
  function showSnackbar() {
    var sb = document.getElementById('demo-snackbar');
    sb.classList.remove('hidden');
    clearTimeout(sb._timer);
    sb._timer = setTimeout(function() { sb.classList.add('hidden'); }, 5000);
  }
  function hideSnackbar() {
    var sb = document.getElementById('demo-snackbar');
    sb.classList.add('hidden');
    clearTimeout(sb._timer);
  }""")

    js_block = "\n".join(js_parts)
    return f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title} — M3 Design System Preview</title>
<link href="https://fonts.googleapis.com/css2?family={brand_font.replace(" ", "+")}:wght@400;500;700&family={plain_font.replace(" ", "+")}:wght@400;500;700&display=swap" rel="stylesheet">
<link href="https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:opsz,wght,FILL,GRAD@24,400,0,0" rel="stylesheet">
<style>
  :root {{
    --font-brand: '{brand_font}', sans-serif;
    --font-plain: '{plain_font}', sans-serif;
{light_vars}
{shape_vars}
{spacing_vars}
  }}
  [data-theme="dark"] {{
{dark_vars}
  }}
  * {{ box-sizing: border-box; margin: 0; padding: 0; }}
  body {{ font-family: var(--font-plain); background: var(--color-surface); color: var(--color-on-surface); padding: 32px; transition: background-color 0.3s, color 0.3s; }}
  .material-symbols-outlined {{ font-family: 'Material Symbols Outlined'; font-weight: normal; font-style: normal; font-size: 24px; line-height: 1; letter-spacing: normal; text-transform: none; display: inline-block; white-space: nowrap; word-wrap: normal; direction: ltr; -webkit-font-smoothing: antialiased; font-variation-settings: 'FILL' 0, 'wght' 400, 'GRAD' 0, 'opsz' 24; vertical-align: middle; }}
  .preview-grid {{ display: grid; grid-template-columns: 1fr 1fr; gap: 32px; max-width: 1200px; margin: 0 auto; }}
  .section {{ background: var(--color-surface-container-low); border-radius: var(--radius-medium); padding: 24px; }}
  .section h2 {{ font-family: var(--font-brand); font-size: 22px; margin-bottom: 16px; color: var(--color-on-surface); }}
  .component-row {{ display: flex; gap: 12px; flex-wrap: wrap; align-items: center; margin-bottom: 16px; }}
  .section-label {{ font-size: 12px; color: var(--color-on-surface-variant); margin-bottom: 8px; font-weight: 500; text-transform: uppercase; letter-spacing: 0.5px; }}
  .m3-interactive {{ position: relative; overflow: hidden; cursor: pointer; }}
  .m3-interactive::after {{ content: ''; position: absolute; inset: 0; border-radius: inherit; pointer-events: none; background: currentColor; opacity: 0; transition: opacity 0.2s ease; }}
  .m3-interactive:hover::after {{ opacity: 0.08; }}
  .m3-interactive:focus-visible::after {{ opacity: 0.12; }}
  .m3-interactive:active::after {{ opacity: 0.12; }}
  .m3-interactive:focus-visible {{ outline: 2px solid var(--color-primary); outline-offset: 2px; }}
  .m3-interactive[disabled]::after, .m3-interactive[aria-disabled="true"]::after {{ opacity: 0; }}
  .btn {{ display: inline-flex; align-items: center; justify-content: center; gap: var(--spacing-2); height: 40px; padding: 0 24px; border: none; cursor: pointer; font-family: var(--font-plain); font-size: 14px; font-weight: 500; letter-spacing: 0.1px; line-height: 20px; border-radius: var(--radius-full); transition: box-shadow 0.2s ease; }}
  .btn-filled {{ background: var(--color-primary); color: var(--color-on-primary); }}
  .btn-filled:hover {{ box-shadow: 0 1px 3px 1px rgba(0,0,0,0.15), 0 1px 2px rgba(0,0,0,0.3); }}
  .btn-outlined {{ background: transparent; color: var(--color-primary); border: 1px solid var(--color-outline); }}
  .btn-tonal {{ background: var(--color-secondary-container); color: var(--color-on-secondary-container); }}
  .btn-tonal:hover {{ box-shadow: 0 1px 3px 1px rgba(0,0,0,0.15), 0 1px 2px rgba(0,0,0,0.3); }}
  .btn-text {{ background: transparent; color: var(--color-primary); padding: 0 12px; }}
  .btn[disabled] {{ opacity: 0.38; pointer-events: none; cursor: default; box-shadow: none; }}
  .card {{ border-radius: var(--radius-medium); padding: 16px; color: var(--color-on-surface); }}
  .card-elevated {{ background: var(--color-surface-container-low); box-shadow: 0 1px 2px rgba(0,0,0,0.3), 0 1px 3px 1px rgba(0,0,0,0.15); }}
  .card-filled {{ background: var(--color-surface-container-highest); }}
  .card-outlined {{ background: var(--color-surface); border: 1px solid var(--color-outline-variant); }}
  .card h3 {{ font-family: var(--font-brand); font-size: 22px; line-height: 28px; margin-bottom: 8px; }}
  .card p {{ font-size: 14px; color: var(--color-on-surface-variant); line-height: 20px; }}
  .card-actions {{ display: flex; gap: var(--spacing-2); margin-top: var(--spacing-4); justify-content: flex-end; }}
  .chip {{ display: inline-flex; align-items: center; height: 32px; padding: 0 16px; gap: var(--spacing-2); border-radius: var(--radius-small); font-size: 14px; font-weight: 500; cursor: pointer; user-select: none; transition: background-color 0.15s, color 0.15s; }}
  .chip-unselected {{ border: 1px solid var(--color-outline); background: transparent; color: var(--color-on-surface); }}
  .chip-selected {{ border: 1px solid transparent; background: var(--color-secondary-container); color: var(--color-on-secondary-container); }}
  .input-outlined-wrap {{ border: 1px solid var(--color-outline); border-radius: var(--radius-extra-small); padding: 8px var(--spacing-4); position: relative; min-height: 56px; display: flex; flex-direction: column; justify-content: flex-end; transition: border-color 0.15s; }}
  .input-outlined-wrap:focus-within {{ border: 2px solid var(--color-primary); padding: 7px calc(var(--spacing-4) - 1px); }}
  .input-outlined-wrap.input-error {{ border-color: var(--color-error); }}
  .input-filled-wrap {{ background: var(--color-surface-container-highest); border-radius: var(--radius-extra-small) var(--radius-extra-small) 0 0; border-bottom: 1px solid var(--color-on-surface-variant); padding: 8px var(--spacing-4); position: relative; min-height: 56px; display: flex; flex-direction: column; justify-content: flex-end; }}
  .input-filled-wrap:focus-within {{ border-bottom: 2px solid var(--color-primary); }}
  .input-label-float {{ position: absolute; top: 18px; left: var(--spacing-4); font-size: 16px; color: var(--color-on-surface-variant); transition: all 0.15s ease; pointer-events: none; }}
  .input-field:focus ~ .input-label-float, .input-field:not(:placeholder-shown) ~ .input-label-float {{ top: 8px; font-size: 12px; }}
  .input-outlined-wrap:focus-within .input-label-float {{ color: var(--color-primary); }}
  .input-error .input-label-float {{ color: var(--color-error) !important; }}
  .input-field {{ border: none; outline: none; background: transparent; font-size: 16px; font-family: var(--font-plain); color: var(--color-on-surface); width: 100%; padding: 0; margin-top: 12px; }}
  .input-supporting {{ font-size: 12px; margin: 4px var(--spacing-4) 0; color: var(--color-on-surface-variant); }}
  .input-supporting.input-error-text {{ color: var(--color-error); }}
  .avatar {{ width: 40px; height: 40px; border-radius: 50%; display: inline-flex; align-items: center; justify-content: center; font-weight: 500; font-size: 16px; background: var(--color-primary-container); color: var(--color-on-primary-container); flex-shrink: 0; }}
  .avatar-sm {{ width: 24px; height: 24px; font-size: 11px; }}
  .avatar-lg {{ width: 56px; height: 56px; font-size: 22px; }}
  .badge-wrap {{ position: relative; display: inline-flex; }}
  .badge-dot {{ position: absolute; top: -2px; right: -2px; width: 6px; height: 6px; border-radius: 50%; background: var(--color-error); }}
  .badge-count {{ position: absolute; top: -4px; right: -8px; min-width: 16px; height: 16px; border-radius: 8px; background: var(--color-error); color: var(--color-on-error); font-size: 11px; font-weight: 500; display: flex; align-items: center; justify-content: center; padding: 0 4px; }}
  .color-group {{ display: flex; flex-direction: column; gap: 2px; }}
  .color-group-label {{ font-size: 11px; font-weight: 600; text-transform: uppercase; letter-spacing: 0.5px; color: var(--color-on-surface-variant); margin-bottom: 4px; }}
  .color-pair {{ border-radius: var(--radius-small); overflow: hidden; }}
  .color-pair-main {{ padding: 14px 12px 6px; font-size: 12px; font-weight: 500; }}
  .color-pair-on {{ padding: 6px 12px 10px; font-size: 10px; }}
  .surface-ramp {{ display: flex; border-radius: var(--radius-small); overflow: hidden; height: 48px; }}
  .surface-ramp-step {{ flex: 1; display: flex; align-items: flex-end; justify-content: center; padding: 4px 2px; font-size: 8px; font-weight: 500; }}
  .type-row {{ display: flex; align-items: baseline; gap: 16px; padding: 6px 0; border-bottom: 1px solid var(--color-outline-variant); }}
  .type-row:last-child {{ border-bottom: none; }}
  .type-meta {{ min-width: 130px; font-size: 11px; color: var(--color-on-surface-variant); font-weight: 500; text-transform: uppercase; letter-spacing: 0.5px; flex-shrink: 0; }}
  .type-sample {{ flex: 1; min-width: 0; }}
  .sidebar-item {{ display: flex; align-items: center; gap: 12px; padding: 0 24px 0 16px; height: 56px; border-radius: var(--radius-full); border: none; width: 100%; font-family: var(--font-plain); font-size: 14px; font-weight: 500; text-align: left; background: transparent; color: var(--color-on-surface-variant); transition: background-color 0.15s, color 0.15s; }}
  .sidebar-item[aria-selected="true"] {{ background: var(--color-secondary-container); color: var(--color-on-secondary-container); font-weight: 700; }}
  .tab-btn {{ flex: 1; display: flex; flex-direction: column; align-items: center; justify-content: center; gap: var(--spacing-1); height: 48px; padding: 0 var(--spacing-4); border: none; cursor: pointer; background: transparent; font-family: var(--font-plain); font-size: 14px; font-weight: 500; letter-spacing: 0.1px; color: var(--color-on-surface-variant); border-bottom: 3px solid transparent; transition: color 0.15s, border-color 0.15s; }}
  .tab-btn[aria-selected="true"] {{ color: var(--color-on-surface); border-bottom-color: var(--color-primary); }}
  .bnav-item {{ flex: 1; display: flex; flex-direction: column; align-items: center; justify-content: center; gap: var(--spacing-1); border: none; cursor: pointer; background: transparent; font-family: var(--font-plain); font-size: 12px; font-weight: 500; color: var(--color-on-surface-variant); letter-spacing: 0.5px; }}
  .bnav-item[aria-selected="true"] {{ color: var(--color-on-surface); font-weight: 700; }}
  .bnav-pill {{ width: 64px; height: 32px; border-radius: var(--radius-full); display: flex; align-items: center; justify-content: center; transition: background-color 0.2s; }}
  .bnav-item[aria-selected="true"] .bnav-pill {{ background: var(--color-secondary-container); color: var(--color-on-secondary-container); }}
  .data-table {{ width: 100%; border-collapse: collapse; font-size: 14px; }}
  .data-table th {{ padding: 12px 16px; text-align: left; font-size: 12px; font-weight: 500; color: var(--color-on-surface-variant); border-bottom: 1px solid var(--color-outline-variant); }}
  .data-table td {{ padding: 12px 16px; }}
  .data-table tbody tr {{ border-bottom: 1px solid var(--color-outline-variant); transition: background-color 0.15s; }}
  .data-table tbody tr:hover {{ background-color: var(--color-surface-container); }}
  .list-item {{ display: flex; align-items: center; gap: var(--spacing-4); padding: var(--spacing-2) var(--spacing-4); min-height: 72px; transition: background-color 0.15s; }}
  .list-item:hover {{ background-color: var(--color-surface-container); }}
  .dialog-scrim {{ display: none; position: fixed; inset: 0; background: rgba(0,0,0,0.32); z-index: 200; align-items: center; justify-content: center; }}
  .dialog-scrim.open {{ display: flex; }}
  .dialog-surface {{ background: var(--color-surface-container-high); border-radius: var(--radius-extra-large); padding: var(--spacing-6); max-width: 560px; width: 90%; box-shadow: 0 8px 32px rgba(0,0,0,0.24); animation: dialog-enter 0.2s ease; }}
  @keyframes dialog-enter {{ from {{ opacity: 0; transform: scale(0.95); }} to {{ opacity: 1; transform: scale(1); }} }}
  .snackbar {{ display: flex; align-items: center; gap: var(--spacing-2); padding: var(--spacing-3) var(--spacing-4); background: var(--color-inverse-surface); color: var(--color-inverse-on-surface); border-radius: var(--radius-extra-small); font-size: 14px; line-height: 20px; box-shadow: 0 4px 12px rgba(0,0,0,0.2); transition: opacity 0.3s, transform 0.3s; }}
  .snackbar.hidden {{ opacity: 0; transform: translateY(16px); pointer-events: none; }}
  .tooltip-wrap {{ position: relative; display: inline-flex; }}
  .tooltip-bubble {{ position: absolute; bottom: 100%; left: 50%; transform: translateX(-50%); margin-bottom: 8px; padding: 4px var(--spacing-2); background: var(--color-inverse-surface); color: var(--color-inverse-on-surface); border-radius: var(--radius-extra-small); font-size: 12px; font-weight: 500; white-space: nowrap; pointer-events: none; opacity: 0; transition: opacity 0.15s; }}
  .tooltip-wrap:hover .tooltip-bubble, .tooltip-wrap:focus-within .tooltip-bubble {{ opacity: 1; }}
  .progress-track {{ width: 100%; height: 4px; background: var(--color-surface-container-highest); border-radius: var(--radius-full); overflow: hidden; }}
  .progress-bar {{ height: 100%; background: var(--color-primary); border-radius: var(--radius-full); transition: width 0.4s ease; }}
  @keyframes indeterminate {{ 0% {{ left: -30%; }} 100% {{ left: 100%; }} }}
  @keyframes spin {{ to {{ transform: rotate(360deg); }} }}
  @keyframes skeleton-pulse {{ 0%, 100% {{ opacity: 1; }} 50% {{ opacity: 0.4; }} }}
  .skeleton {{ background: var(--color-surface-container-highest); animation: skeleton-pulse 1.5s ease-in-out infinite; }}
  .shape-sample {{ width: 64px; height: 64px; background: var(--color-primary-container); display: flex; align-items: center; justify-content: center; font-size: 10px; font-weight: 500; color: var(--color-on-primary-container); }}
  .spacing-bar {{ background: var(--color-primary); border-radius: 2px; height: 16px; }}
  .spacing-row {{ display: flex; align-items: center; gap: 12px; }}
  .spacing-label {{ font-size: 11px; color: var(--color-on-surface-variant); min-width: 70px; font-weight: 500; font-variant-numeric: tabular-nums; }}
  .theme-toggle {{ position: fixed; top: 16px; right: 16px; z-index: 100; }}
  .header {{ text-align: center; margin-bottom: 48px; }}
  .header h1 {{ font-family: var(--font-brand); font-size: 45px; line-height: 52px; margin-bottom: 8px; }}
  .header p {{ font-size: 16px; color: var(--color-on-surface-variant); }}
</style>
</head>
<body>
<button class="btn btn-outlined m3-interactive theme-toggle" onclick="toggleTheme(this)"><span class="material-symbols-outlined" style="font-size:18px;">dark_mode</span> Dark</button>
<div class="header"><h1>{title}</h1><p>{subtitle}</p></div>
<div class="preview-grid">
{proportion_html}
  <div class="section" style="grid-column:1/-1;">
    <h2>M3 Color Roles</h2>
    <div style="display:grid;grid-template-columns:repeat(4,1fr);gap:12px;">
      <div class="color-group"><div class="color-group-label">Primary</div><div class="color-pair"><div class="color-pair-main" style="background:var(--color-primary);color:var(--color-on-primary);">Primary</div><div class="color-pair-on" style="background:var(--color-on-primary);color:var(--color-primary);">On Primary</div></div><div class="color-pair" style="margin-top:4px;"><div class="color-pair-main" style="background:var(--color-primary-container);color:var(--color-on-primary-container);">Container</div><div class="color-pair-on" style="background:var(--color-on-primary-container);color:var(--color-primary-container);">On Container</div></div></div>
      <div class="color-group"><div class="color-group-label">Secondary</div><div class="color-pair"><div class="color-pair-main" style="background:var(--color-secondary);color:var(--color-on-secondary);">Secondary</div><div class="color-pair-on" style="background:var(--color-on-secondary);color:var(--color-secondary);">On Secondary</div></div><div class="color-pair" style="margin-top:4px;"><div class="color-pair-main" style="background:var(--color-secondary-container);color:var(--color-on-secondary-container);">Container</div><div class="color-pair-on" style="background:var(--color-on-secondary-container);color:var(--color-secondary-container);">On Container</div></div></div>
      <div class="color-group"><div class="color-group-label">Tertiary</div><div class="color-pair"><div class="color-pair-main" style="background:var(--color-tertiary);color:var(--color-on-tertiary);">Tertiary</div><div class="color-pair-on" style="background:var(--color-on-tertiary);color:var(--color-tertiary);">On Tertiary</div></div><div class="color-pair" style="margin-top:4px;"><div class="color-pair-main" style="background:var(--color-tertiary-container);color:var(--color-on-tertiary-container);">Container</div><div class="color-pair-on" style="background:var(--color-on-tertiary-container);color:var(--color-tertiary-container);">On Container</div></div></div>
      <div class="color-group"><div class="color-group-label">Error</div><div class="color-pair"><div class="color-pair-main" style="background:var(--color-error);color:var(--color-on-error);">Error</div><div class="color-pair-on" style="background:var(--color-on-error);color:var(--color-error);">On Error</div></div><div class="color-pair" style="margin-top:4px;"><div class="color-pair-main" style="background:var(--color-error-container);color:var(--color-on-error-container);">Container</div><div class="color-pair-on" style="background:var(--color-on-error-container);color:var(--color-error-container);">On Container</div></div></div>
    </div>
    <div class="color-group-label" style="margin-top:20px;">Surface Hierarchy</div>
    <div class="surface-ramp" style="margin-top:6px;"><div class="surface-ramp-step" style="background:var(--color-surface-container-lowest);color:var(--color-on-surface);">Lowest</div><div class="surface-ramp-step" style="background:var(--color-surface-container-low);color:var(--color-on-surface);">Low</div><div class="surface-ramp-step" style="background:var(--color-surface-container);color:var(--color-on-surface);">Base</div><div class="surface-ramp-step" style="background:var(--color-surface-container-high);color:var(--color-on-surface);">High</div><div class="surface-ramp-step" style="background:var(--color-surface-container-highest);color:var(--color-on-surface);">Highest</div><div class="surface-ramp-step" style="background:var(--color-surface);color:var(--color-on-surface);font-weight:700;">Surface</div></div>
    <div style="display:flex;gap:4px;margin-top:8px;"><div style="flex:1;padding:8px;border-radius:var(--radius-extra-small);background:var(--color-on-surface);color:var(--color-surface);font-size:10px;text-align:center;">On Surface</div><div style="flex:1;padding:8px;border-radius:var(--radius-extra-small);background:var(--color-on-surface-variant);color:var(--color-surface);font-size:10px;text-align:center;">On Srf Var</div><div style="flex:1;padding:8px;border-radius:var(--radius-extra-small);background:var(--color-outline);color:white;font-size:10px;text-align:center;">Outline</div><div style="flex:1;padding:8px;border-radius:var(--radius-extra-small);border:1px solid var(--color-outline-variant);color:var(--color-on-surface);font-size:10px;text-align:center;">Outline Var</div></div>
  </div>
{extended_html}
  <div class="section">
    <h2>Typography</h2>
    <div style="display:flex;flex-direction:column;">
      <div class="type-row"><div class="type-meta">Display L<br>57/64</div><div class="type-sample" style="font-family:var(--font-brand);font-size:57px;line-height:64px;letter-spacing:-0.25px;">Aa</div></div>
      <div class="type-row"><div class="type-meta">Headline L<br>32/40</div><div class="type-sample" style="font-family:var(--font-brand);font-size:32px;line-height:40px;">Headline</div></div>
      <div class="type-row"><div class="type-meta">Title L<br>22/28</div><div class="type-sample" style="font-family:var(--font-brand);font-size:22px;line-height:28px;">Title Large</div></div>
      <div class="type-row"><div class="type-meta">Body L<br>16/24</div><div class="type-sample" style="font-family:var(--font-plain);font-size:16px;line-height:24px;letter-spacing:0.5px;color:var(--color-on-surface-variant);">The quick brown fox jumps over the lazy dog.</div></div>
      <div class="type-row"><div class="type-meta">Body S<br>12/16</div><div class="type-sample" style="font-family:var(--font-plain);font-size:12px;line-height:16px;letter-spacing:0.4px;color:var(--color-on-surface-variant);">Captions and metadata.</div></div>
      <div class="type-row"><div class="type-meta">Label L<br>14/20 M500</div><div class="type-sample" style="font-family:var(--font-plain);font-size:14px;line-height:20px;font-weight:500;letter-spacing:0.1px;">Button Labels &amp; Navigation</div></div>
    </div>
  </div>
{shape_spacing_showcase}
{component_sections}
{in_context_html}
</div>
{dialog_overlay}
<div style="text-align:center;margin-top:48px;padding:24px;color:var(--color-on-surface-variant);font-size:14px;">Generated from design tokens &middot; M3 Architecture &middot; DTCG Compatible &middot; WCAG AA</div>
<script>
{js_block}
</script>
</body>
</html>'''


COMPONENT_GENERATORS = {
    # Core
    'button': generate_button_jsx,
    'card': generate_card_jsx,
    'input': generate_input_jsx,
    'chip': generate_chip_jsx,
    'badge': generate_badge_jsx,
    'avatar': generate_avatar_jsx,
    'divider': generate_divider_jsx,
    # Navigation
    'appbar': generate_appbar_jsx,
    'tabs': generate_tabs_jsx,
    'sidebar': generate_sidebar_jsx,
    'breadcrumb': generate_breadcrumb_jsx,
    'bottomnav': generate_bottomnav_jsx,
    # Data
    'table': generate_table_jsx,
    'list': generate_list_jsx,
    'datacard': generate_datacard_jsx,
    'stat': generate_stat_jsx,
    # Feedback
    'dialog': generate_dialog_jsx,
    'snackbar': generate_snackbar_jsx,
    'tooltip': generate_tooltip_jsx,
    'progress': generate_progress_jsx,
    'skeleton': generate_skeleton_jsx,
    # Layout
    'container': generate_container_jsx,
    'grid': generate_grid_jsx,
    'stack': generate_stack_jsx,
    'surface': generate_surface_jsx,
}


def main():
    all_set_names = list(COMPONENT_SETS.keys())
    parser = argparse.ArgumentParser(description="Generate component library from resolved tokens")
    parser.add_argument("--resolved-tokens", required=True, help="Path to resolved.json from parse_tokens.py")
    parser.add_argument("--components", default=None,
                        help="Comma-separated component names to generate (merged with --sets)")
    parser.add_argument("--sets", default="core",
                        help=f"Comma-separated component sets ({', '.join(all_set_names)}) or 'all' (default: core)")
    parser.add_argument("--output-dir", default="./components", help="Output directory")
    parser.add_argument("--typescript", action="store_true", default=True,
                        help="Generate .tsx files with TypeScript prop interfaces (default: on)")
    parser.add_argument("--no-typescript", action="store_true",
                        help="Generate plain .jsx files instead of TypeScript")
    parser.add_argument("--storybook", action="store_true",
                        help="Generate .stories.tsx files for each component")
    parser.add_argument("--theme-name", default="Custom Theme",
                        help="Theme name used in README and preview")
    parser.add_argument("--review-dir", default=None,
                        help="Directory for preview.html (defaults to --output-dir)")

    args = parser.parse_args()
    typescript = args.typescript and not args.no_typescript
    tokens = load_resolved_tokens(args.resolved_tokens)

    # Resolve component list from --sets and --components
    component_names = []
    sets_arg = args.sets.strip().lower()
    if sets_arg == 'all':
        for s in all_set_names:
            component_names.extend(COMPONENT_SETS[s])
    else:
        for s in sets_arg.split(','):
            s = s.strip()
            if s in COMPONENT_SETS:
                component_names.extend(COMPONENT_SETS[s])
            else:
                print(f"  ⚠ Unknown set: {s} (available: {', '.join(all_set_names)})")

    # Merge with --components if provided
    if args.components:
        for c in args.components.split(','):
            c = c.strip().lower()
            if c and c not in component_names:
                component_names.append(c)

    # Deduplicate while preserving order
    seen = set()
    unique_names = []
    for n in component_names:
        if n not in seen:
            seen.add(n)
            unique_names.append(n)
    component_names = unique_names

    ext = "tsx" if typescript else "jsx"

    os.makedirs(args.output_dir, exist_ok=True)

    # Generate theme.css
    css = generate_theme_css(tokens)
    css_path = os.path.join(args.output_dir, "theme.css")
    with open(css_path, "w") as f:
        f.write(css)
    print(f"  ✓ theme.css")

    # Generate components
    generated = []
    for name in component_names:
        if name in COMPONENT_GENERATORS:
            code = COMPONENT_GENERATORS[name](typescript=typescript)
            display = _component_display_name(name)
            fname = f"{display}.{ext}"
            with open(os.path.join(args.output_dir, fname), "w") as f:
                f.write(code)
            generated.append(name)
            print(f"  ✓ {fname}")

            # Storybook story
            if args.storybook:
                story = generate_story(name, typescript=typescript)
                story_fname = f"{display}.stories.{ext}"
                with open(os.path.join(args.output_dir, story_fname), "w") as f:
                    f.write(story)
                print(f"  ✓ {story_fname}")
        else:
            print(f"  ⚠ Unknown component: {name}")

    # Generate index
    index_ext = "ts" if typescript else "js"
    index = generate_index_js(generated, typescript=typescript)
    with open(os.path.join(args.output_dir, f"index.{index_ext}"), "w") as f:
        f.write(index)
    print(f"  ✓ index.{index_ext}")

    # Generate preview
    preview = generate_preview_html(tokens, generated, theme_name=args.theme_name)
    review_dir = args.review_dir or args.output_dir
    os.makedirs(review_dir, exist_ok=True)
    preview_path = os.path.join(review_dir, "preview.html")
    with open(preview_path, "w") as f:
        f.write(preview)
    print(f"  ✓ preview.html -> {review_dir}/")

    # Generate README
    readme = generate_readme(args.theme_name, generated, typescript=typescript)
    with open(os.path.join(review_dir, "README.md"), "w") as f:
        f.write(readme)
    print(f"  ✓ README.md")

    print(f"\n✓ Generated {len(generated)} components + theme + preview in {args.output_dir}/")


if __name__ == "__main__":
    main()
