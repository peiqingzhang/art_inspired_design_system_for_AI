import React from 'react';
import './theme.css';

interface GridProps {
  columns?: number | string;
  gap?: string;
  children?: React.ReactNode;
  style?: React.CSSProperties;
  [key: string]: unknown;
}

interface GridItemProps {
  span?: number;
  children?: React.ReactNode;
  style?: React.CSSProperties;
  [key: string]: unknown;
}

export default function Grid({ columns = 12, gap = 'var(--spacing-4)', children, style, ...props }: GridProps) {
  const gridTemplate = typeof columns === 'number' ? `repeat(${columns}, 1fr)` : columns;

  return (
    <div
      style={{
        display: 'grid',
        gridTemplateColumns: gridTemplate,
        gap,
        ...style,
      }}
      {...props}
    >
      {children}
    </div>
  );
}

Grid.Item = function GridItem({ span = 1, children, style, ...props }: GridItemProps) {
  return (
    <div style={{ gridColumn: `span ${span}`, ...style }} {...props}>
      {children}
    </div>
  );
};
