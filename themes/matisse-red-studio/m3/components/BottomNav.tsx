import React from 'react';
import './theme.css';

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

export default function BottomNav({ items, ...props }: BottomNavProps) {
  return (
    <nav
      role="navigation"
      style={{
        display: 'flex',
        backgroundColor: 'var(--color-surface-container)',
        height: '80px',
        borderTop: '1px solid var(--color-outline-variant)',
      }}
      {...props}
    >
      {items.map((item: BottomNavItem, i: number) => (
        <button
          key={i}
          onClick={item.onClick}
          className="m3-interactive"
          aria-current={item.active ? 'page' : undefined}
          style={{
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
          }}
        >
          <span className="state-layer" aria-hidden="true" />
          <span
            style={{
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
            }}
          >
            {item.icon}
          </span>
          <span>{item.label}</span>
        </button>
      ))}
    </nav>
  );
}
