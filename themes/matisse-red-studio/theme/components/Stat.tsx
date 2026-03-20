import React from 'react';
import './theme.css';

interface StatProps {
  label: string;
  value: string | number;
  description?: string;
  [key: string]: unknown;
}

export default function Stat({ label, value, description, ...props }: StatProps) {
  return (
    <div
      style={{
        fontFamily: 'var(--font-plain)',
        color: 'var(--color-on-surface)',
        textAlign: 'center',
        padding: 'var(--spacing-4)',
      }}
      {...props}
    >
      <div style={{ fontSize: '12px', fontWeight: 500, letterSpacing: '0.5px', color: 'var(--color-on-surface-variant)', marginBottom: 'var(--spacing-1)' }}>
        {label}
      </div>
      <div style={{ fontSize: '45px', fontWeight: 400, fontFamily: 'var(--font-brand)', lineHeight: '52px' }}>
        {value}
      </div>
      {description && (
        <div style={{ fontSize: '14px', color: 'var(--color-on-surface-variant)', marginTop: 'var(--spacing-1)' }}>
          {description}
        </div>
      )}
    </div>
  );
}
