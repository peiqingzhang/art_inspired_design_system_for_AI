import React from 'react';
import './theme.css';

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

export default function Sidebar({ items, header, ...props }: SidebarProps) {
  return (
    <nav
      style={{
        width: '280px',
        backgroundColor: 'var(--color-surface-container)',
        padding: 'var(--spacing-3)',
        fontFamily: 'var(--font-plain)',
        display: 'flex',
        flexDirection: 'column',
        gap: 'var(--spacing-1)',
      }}
      role="navigation"
      {...props}
    >
      {header && <div style={{ padding: 'var(--spacing-4)', marginBottom: 'var(--spacing-2)' }}>{header}</div>}
      {items.map((item: SidebarItem, i: number) => (
        <button
          key={i}
          onClick={item.onClick}
          className="m3-interactive"
          style={{
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
          }}
        >
          <span className="state-layer" aria-hidden="true" />
          {item.icon && <span style={{ fontSize: '24px', display: 'flex' }}>{item.icon}</span>}
          <span>{item.label}</span>
        </button>
      ))}
    </nav>
  );
}
