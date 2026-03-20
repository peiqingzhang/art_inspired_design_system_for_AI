import React from 'react';
import './theme.css';

interface SurfaceProps {
  level?: 0 | 1 | 2 | 3 | 4 | 5;
  children?: React.ReactNode;
  style?: React.CSSProperties;
  [key: string]: unknown;
}

const levelMap: Record<number, string> = {
  0: 'var(--color-surface)',
  1: 'var(--color-surface-container-lowest)',
  2: 'var(--color-surface-container-low)',
  3: 'var(--color-surface-container)',
  4: 'var(--color-surface-container-high)',
  5: 'var(--color-surface-container-highest)',
};

export default function Surface({ level = 0, children, style, ...props }: SurfaceProps) {
  return (
    <div
      style={{
        backgroundColor: levelMap[level],
        color: 'var(--color-on-surface)',
        borderRadius: 'var(--radius-medium)',
        padding: 'var(--spacing-4)',
        fontFamily: 'var(--font-plain)',
        ...style,
      }}
      {...props}
    >
      {children}
    </div>
  );
}
