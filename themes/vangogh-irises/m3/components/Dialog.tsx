import React, { useEffect, useRef } from 'react';
import './theme.css';

interface DialogProps {
  open: boolean;
  onClose: () => void;
  headline: string;
  children?: React.ReactNode;
  actions?: React.ReactNode;
  [key: string]: unknown;
}

export default function Dialog({ open, onClose, headline, children, actions, ...props }: DialogProps) {
  const dialogRef = useRef<HTMLDialogElement>(null);

  useEffect(() => {
    const el = dialogRef.current;
    if (!el) return;
    if (open && !el.open) el.showModal();
    else if (!open && el.open) el.close();
  }, [open]);

  return (
    <dialog
      ref={dialogRef}
      onClose={onClose}
      style={{
        backgroundColor: 'var(--color-surface-container-high)',
        color: 'var(--color-on-surface)',
        borderRadius: 'var(--radius-extra-large)',
        padding: 'var(--spacing-6)',
        border: 'none',
        maxWidth: '560px',
        width: '100%',
        fontFamily: 'var(--font-plain)',
        boxShadow: '0 8px 32px rgba(0,0,0,0.24)',
      }}
      {...props}
    >
      <h2 style={{
        fontFamily: 'var(--font-brand)',
        fontSize: '24px',
        lineHeight: '32px',
        fontWeight: 400,
        margin: '0 0 var(--spacing-4)',
        color: 'var(--color-on-surface)',
      }}>
        {headline}
      </h2>
      <div style={{
        fontSize: '14px',
        lineHeight: '20px',
        color: 'var(--color-on-surface-variant)',
        marginBottom: actions ? 'var(--spacing-6)' : '0',
      }}>
        {children}
      </div>
      {actions && (
        <div style={{ display: 'flex', justifyContent: 'flex-end', gap: 'var(--spacing-2)' }}>
          {actions}
        </div>
      )}
    </dialog>
  );
}
