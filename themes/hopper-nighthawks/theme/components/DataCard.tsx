import React from 'react';
import './theme.css';

interface DataCardProps {
  title: string;
  value: string | number;
  subtitle?: string;
  trend?: 'up' | 'down' | 'neutral';
  trendValue?: string;
  icon?: React.ReactNode;
  [key: string]: unknown;
}

export default function DataCard({ title, value, subtitle, trend, trendValue, icon, ...props }: DataCardProps) {
  const trendColor = trend === 'up' ? 'var(--color-tertiary)' : trend === 'down' ? 'var(--color-error)' : 'var(--color-on-surface-variant)';
  const trendArrow = trend === 'up' ? '\u2191' : trend === 'down' ? '\u2193' : '';

  return (
    <div
      role="article"
      style={{
        backgroundColor: 'var(--color-surface-container-low)',
        borderRadius: 'var(--radius-medium)',
        padding: 'var(--spacing-4)',
        fontFamily: 'var(--font-plain)',
        color: 'var(--color-on-surface)',
        boxShadow: '0 1px 3px rgba(0,0,0,0.12)',
      }}
      {...props}
    >
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', marginBottom: 'var(--spacing-3)' }}>
        <span style={{ fontSize: '14px', fontWeight: 500, color: 'var(--color-on-surface-variant)' }}>{title}</span>
        {icon && <span style={{ fontSize: '24px', color: 'var(--color-primary)' }}>{icon}</span>}
      </div>
      <div style={{ fontSize: '32px', fontWeight: 700, fontFamily: 'var(--font-brand)', lineHeight: '40px' }}>{value}</div>
      <div style={{ display: 'flex', alignItems: 'center', gap: 'var(--spacing-2)', marginTop: 'var(--spacing-1)' }}>
        {trendValue && (
          <span style={{ fontSize: '14px', fontWeight: 500, color: trendColor }}>
            {trendArrow} {trendValue}
          </span>
        )}
        {subtitle && <span style={{ fontSize: '14px', color: 'var(--color-on-surface-variant)' }}>{subtitle}</span>}
      </div>
    </div>
  );
}
