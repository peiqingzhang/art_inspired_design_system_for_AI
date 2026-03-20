import React from 'react';
import './theme.css';

interface SnackbarProps {
  message: string;
  action?: { label: string; onClick: () => void };
  onClose?: () => void;
  [key: string]: unknown;
}

export default function Snackbar({ message, action, onClose, ...props }: SnackbarProps) {
  return (
    <div
      role="status"
      aria-live="polite"
      style={{
        display: 'flex',
        alignItems: 'center',
        gap: 'var(--spacing-2)',
        padding: 'var(--spacing-3) var(--spacing-4)',
        backgroundColor: 'var(--color-inverse-surface)',
        color: 'var(--color-inverse-on-surface)',
        borderRadius: 'var(--radius-extra-small)',
        fontFamily: 'var(--font-plain)',
        fontSize: '14px',
        lineHeight: '20px',
        minHeight: '48px',
        boxShadow: '0 4px 12px rgba(0,0,0,0.2)',
      }}
      {...props}
    >
      <span style={{ flex: 1 }}>{message}</span>
      {action && (
        <button
          onClick={action.onClick}
          style={{
            border: 'none',
            background: 'none',
            color: 'var(--color-inverse-primary)',
            fontFamily: 'var(--font-plain)',
            fontSize: '14px',
            fontWeight: 500,
            letterSpacing: '0.1px',
            cursor: 'pointer',
            padding: '0 var(--spacing-2)',
          }}
        >
          {action.label}
        </button>
      )}
      {onClose && (
        <button
          onClick={onClose}
          aria-label="Dismiss"
          style={{
            border: 'none',
            background: 'none',
            color: 'var(--color-inverse-on-surface)',
            cursor: 'pointer',
            fontSize: '18px',
            padding: '0 var(--spacing-1)',
          }}
        >
          &times;
        </button>
      )}
    </div>
  );
}
