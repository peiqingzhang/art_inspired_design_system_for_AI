import React from 'react';
import './theme.css';

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

export default function List({ children, ...props }: ListProps) {
  return (
    <ul
      role="list"
      style={{ listStyle: 'none', margin: 0, padding: 0, fontFamily: 'var(--font-plain)' }}
      {...props}
    >
      {children}
    </ul>
  );
}

List.Item = function ListItem({ primary, secondary, leading, trailing, onClick, ...props }: ListItemProps) {
  const interactive = !!onClick;
  return (
    <li
      role={interactive ? 'button' : 'listitem'}
      tabIndex={interactive ? 0 : undefined}
      onClick={onClick}
      onKeyDown={(e) => { if (interactive && (e.key === 'Enter' || e.key === ' ')) { e.preventDefault(); onClick?.(); } }}
      className={interactive ? 'm3-interactive' : ''}
      style={{
        display: 'flex',
        alignItems: 'center',
        gap: 'var(--spacing-4)',
        padding: 'var(--spacing-2) var(--spacing-4)',
        minHeight: secondary ? '72px' : '56px',
        cursor: interactive ? 'pointer' : 'default',
        color: 'var(--color-on-surface)',
        position: 'relative',
        overflow: 'hidden',
      }}
      {...props}
    >
      {interactive && <span className="state-layer" aria-hidden="true" />}
      {leading && <div style={{ display: 'flex', alignItems: 'center', fontSize: '24px', color: 'var(--color-on-surface-variant)' }}>{leading}</div>}
      <div style={{ flex: 1, minWidth: 0 }}>
        <div style={{ fontSize: '16px', lineHeight: '24px' }}>{primary}</div>
        {secondary && <div style={{ fontSize: '14px', lineHeight: '20px', color: 'var(--color-on-surface-variant)' }}>{secondary}</div>}
      </div>
      {trailing && <div style={{ display: 'flex', alignItems: 'center', color: 'var(--color-on-surface-variant)' }}>{trailing}</div>}
    </li>
  );
};
