import React from 'react';
import './theme.css';

interface ContainerProps {
  maxWidth?: 'sm' | 'md' | 'lg' | 'xl' | 'full';
  children?: React.ReactNode;
  style?: React.CSSProperties;
  [key: string]: unknown;
}

const maxWidths = {
  sm: '640px',
  md: '768px',
  lg: '1024px',
  xl: '1280px',
  full: '100%',
};

export default function Container({ maxWidth = 'lg', children, style, ...props }: ContainerProps) {
  return (
    <div
      style={{
        maxWidth: maxWidths[maxWidth],
        marginLeft: 'auto',
        marginRight: 'auto',
        paddingLeft: 'var(--spacing-4)',
        paddingRight: 'var(--spacing-4)',
        width: '100%',
        ...style,
      }}
      {...props}
    >
      {children}
    </div>
  );
}
