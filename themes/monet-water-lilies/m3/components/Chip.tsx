import React from 'react';
import './theme.css';

interface ChipProps {
  label: string;
  selected?: boolean;
  onClose?: () => void;
  onClick?: () => void;
  variant?: 'assist' | 'filter' | 'input' | 'suggestion';
}

export default function Chip({ label, selected, onClose, onClick, variant = 'assist', ...props }: ChipProps) {
  const style = {
    display: 'inline-flex',
    alignItems: 'center',
    height: '32px',
    padding: '0 var(--spacing-4)',
    gap: 'var(--spacing-2)',
    borderRadius: 'var(--radius-small)',
    fontFamily: 'var(--font-plain)',
    fontSize: '14px',
    fontWeight: 500,
    cursor: 'pointer',
    transition: 'all 0.15s ease',
    border: selected ? 'none' : '1px solid var(--color-outline)',
    backgroundColor: selected ? 'var(--color-secondary-container)' : 'transparent',
    color: selected ? 'var(--color-on-secondary-container)' : 'var(--color-on-surface)',
    position: 'relative',
    overflow: 'hidden',
  };

  const handleKeyDown = (e: React.KeyboardEvent<HTMLDivElement>) => {
    if (e.key === 'Enter' || e.key === ' ') {
      e.preventDefault();
      onClick?.();
    }
  };

  return (
    <div
      style={style}
      role="option"
      aria-selected={!!selected}
      aria-label={label}
      tabIndex={0}
      onClick={onClick}
      onKeyDown={handleKeyDown}
      className="m3-interactive"
      {...props}
    >
      <span className="state-layer" aria-hidden="true" />
      <span>{label}</span>
      {onClose && (
        <span
          onClick={(e: React.MouseEvent) => { e.stopPropagation(); onClose(); }}
          aria-label="Remove"
          style={{ cursor: 'pointer', fontSize: '18px', lineHeight: 1 }}
        >&times;</span>
      )}
    </div>
  );
}
