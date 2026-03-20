import React from 'react';
import './theme.css';

interface BadgeProps {
  count?: number;
  children?: React.ReactNode;
}

export default function Badge({ count, children }: BadgeProps) {
  const showCount = count !== undefined && count > 0;
  const ariaLabel = count !== undefined && count > 0
    ? `${count > 99 ? '99+' : count} notifications`
    : undefined;
  return (
    <div style={{ position: 'relative', display: 'inline-flex' }}>
      {children}
      <span
        aria-label={ariaLabel}
        aria-live="polite"
        style={{
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
        }}
      >
        {showCount ? (count! > 99 ? '99+' : count) : ''}
      </span>
    </div>
  );
}
