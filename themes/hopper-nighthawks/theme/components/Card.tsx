import React from 'react';
import './theme.css';

interface CardProps {
  variant?: 'elevated' | 'filled' | 'outlined';
  children?: React.ReactNode;
  style?: React.CSSProperties;
  [key: string]: unknown;
}
interface CardHeaderProps { title: string; subtitle?: string; }
interface CardBodyProps { children?: React.ReactNode; }
interface CardActionsProps { children?: React.ReactNode; }

const cardBase = {
  borderRadius: 'var(--radius-medium)',
  padding: 'var(--spacing-4)',
  fontFamily: 'var(--font-plain)',
  color: 'var(--color-on-surface)',
  transition: 'box-shadow 0.2s ease',
  position: 'relative',
  overflow: 'hidden',
};

const variants = {
  elevated: {
    ...cardBase,
    backgroundColor: 'var(--color-surface-container-low)',
    boxShadow: '0 1px 3px rgba(0,0,0,0.12), 0 1px 2px rgba(0,0,0,0.08)',
  },
  filled: {
    ...cardBase,
    backgroundColor: 'var(--color-surface-container-highest)',
  },
  outlined: {
    ...cardBase,
    backgroundColor: 'var(--color-surface)',
    border: '1px solid var(--color-outline-variant)',
  },
};

export default function Card({ variant = 'elevated', children, style: userStyle, ...props }: CardProps) {
  return (
    <div role="article" style={{ ...variants[variant ?? 'elevated'], ...userStyle }} {...props}>
      <span className="state-layer" aria-hidden="true" />
      {children}
    </div>
  );
}

Card.Header = ({ title, subtitle }: CardHeaderProps) => (
  <div style={{ marginBottom: 'var(--spacing-3)' }}>
    <h3 style={{ fontFamily: 'var(--font-brand)', fontSize: '22px', margin: 0, lineHeight: '28px' }}>{title}</h3>
    {subtitle && <p style={{ fontSize: '14px', color: 'var(--color-on-surface-variant)', margin: '4px 0 0' }}>{subtitle}</p>}
  </div>
);

Card.Body = ({ children }: CardBodyProps) => (
  <div style={{ fontSize: '14px', lineHeight: '20px', color: 'var(--color-on-surface-variant)' }}>
    {children}
  </div>
);

Card.Actions = ({ children }: CardActionsProps) => (
  <div style={{ display: 'flex', gap: 'var(--spacing-2)', marginTop: 'var(--spacing-4)', justifyContent: 'flex-end' }}>
    {children}
  </div>
);
