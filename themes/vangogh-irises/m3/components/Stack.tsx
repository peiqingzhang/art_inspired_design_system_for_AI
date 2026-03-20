import React from 'react';
import './theme.css';

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

export default function Stack({ direction = 'column', gap = 'var(--spacing-4)', align, justify, wrap, children, style, ...props }: StackProps) {
  return (
    <div
      style={{
        display: 'flex',
        flexDirection: direction,
        gap,
        alignItems: align,
        justifyContent: justify,
        flexWrap: wrap ? 'wrap' : undefined,
        ...style,
      }}
      {...props}
    >
      {children}
    </div>
  );
}
