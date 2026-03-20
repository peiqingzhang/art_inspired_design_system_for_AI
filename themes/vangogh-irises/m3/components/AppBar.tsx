import React from 'react';
import './theme.css';

interface AppBarProps {
  title: string;
  leading?: React.ReactNode;
  trailing?: React.ReactNode;
  elevated?: boolean;
  children?: React.ReactNode;
  [key: string]: unknown;
}

export default function AppBar({ title, leading, trailing, elevated, children, ...props }: AppBarProps) {
  return (
    <header
      style={{
        display: 'flex',
        alignItems: 'center',
        height: '64px',
        padding: '0 var(--spacing-4)',
        backgroundColor: elevated ? 'var(--color-surface-container)' : 'var(--color-surface)',
        color: 'var(--color-on-surface)',
        fontFamily: 'var(--font-brand)',
        gap: 'var(--spacing-2)',
        transition: 'background-color 0.2s ease',
      }}
      role="banner"
      {...props}
    >
      {leading && <div style={{ display: 'flex', alignItems: 'center', color: 'var(--color-on-surface-variant)' }}>{leading}</div>}
      <h1 style={{ fontSize: '22px', lineHeight: '28px', fontWeight: 400, margin: 0, flex: 1 }}>{title}</h1>
      {trailing && <div style={{ display: 'flex', alignItems: 'center', gap: 'var(--spacing-2)', color: 'var(--color-on-surface-variant)' }}>{trailing}</div>}
      {children}
    </header>
  );
}
