import React, { useState } from 'react';
import './theme.css';

interface TooltipProps {
  content: string;
  children: React.ReactElement;
  position?: 'top' | 'bottom' | 'left' | 'right';
}

const positionStyles: Record<string, React.CSSProperties> = {
  top: { bottom: '100%', left: '50%', transform: 'translateX(-50%)', marginBottom: '8px' },
  bottom: { top: '100%', left: '50%', transform: 'translateX(-50%)', marginTop: '8px' },
  left: { right: '100%', top: '50%', transform: 'translateY(-50%)', marginRight: '8px' },
  right: { left: '100%', top: '50%', transform: 'translateY(-50%)', marginLeft: '8px' },
};

export default function Tooltip({ content, children, position = 'top' }: TooltipProps) {
  const [visible, setVisible] = useState(false);

  return (
    <div
      style={{ position: 'relative', display: 'inline-flex' }}
      onMouseEnter={() => setVisible(true)}
      onMouseLeave={() => setVisible(false)}
      onFocus={() => setVisible(true)}
      onBlur={() => setVisible(false)}
    >
      {children}
      {visible && (
        <div
          role="tooltip"
          style={{
            position: 'absolute',
            ...positionStyles[position],
            backgroundColor: 'var(--color-inverse-surface)',
            color: 'var(--color-inverse-on-surface)',
            padding: '4px var(--spacing-2)',
            borderRadius: 'var(--radius-extra-small)',
            fontFamily: 'var(--font-plain)',
            fontSize: '12px',
            lineHeight: '16px',
            fontWeight: 500,
            whiteSpace: 'nowrap',
            pointerEvents: 'none',
            zIndex: 1000,
          }}
        >
          {content}
        </div>
      )}
    </div>
  );
}
