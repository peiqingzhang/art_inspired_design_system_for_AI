import React, { useState, useId } from 'react';
import './theme.css';

interface InputProps {
  label?: string;
  variant?: 'outlined' | 'filled';
  supportingText?: string;
  error?: boolean;
  value?: string;
  onChange?: React.ChangeEventHandler<HTMLInputElement>;
  id?: string;
  [key: string]: unknown;
}

export default function Input({ label, variant = 'outlined', supportingText, error, value, onChange, id, ...props }: InputProps) {
  const [focused, setFocused] = useState(false);
  const generatedId = useId();
  const inputId = id || generatedId;
  const helperId = `${inputId}-helper`;
  const hasValue = value && value.length > 0;

  const containerStyle = variant === 'filled' ? {
    backgroundColor: 'var(--color-surface-container-highest)',
    borderRadius: 'var(--radius-extra-small) var(--radius-extra-small) 0 0',
    borderBottom: focused
      ? '2px solid var(--color-primary)'
      : error ? '2px solid var(--color-error)' : '1px solid var(--color-on-surface-variant)',
    padding: '8px var(--spacing-4) 8px',
    position: 'relative',
    minHeight: '56px',
    display: 'flex',
    flexDirection: 'column',
    justifyContent: 'flex-end',
  } : {
    backgroundColor: 'transparent',
    border: focused
      ? '2px solid var(--color-primary)'
      : error ? '2px solid var(--color-error)' : '1px solid var(--color-outline)',
    borderRadius: 'var(--radius-extra-small)',
    padding: '8px var(--spacing-4) 8px',
    position: 'relative',
    minHeight: '56px',
    display: 'flex',
    flexDirection: 'column',
    justifyContent: 'flex-end',
  };

  const labelStyle = {
    position: 'absolute',
    top: (focused || hasValue) ? '8px' : '18px',
    fontSize: (focused || hasValue) ? '12px' : '16px',
    color: focused ? 'var(--color-primary)' : error ? 'var(--color-error)' : 'var(--color-on-surface-variant)',
    transition: 'all 0.15s ease',
    pointerEvents: 'none',
    fontFamily: 'var(--font-plain)',
  };

  const inputStyle = {
    border: 'none',
    outline: 'none',
    background: 'transparent',
    fontSize: '16px',
    fontFamily: 'var(--font-plain)',
    color: 'var(--color-on-surface)',
    width: '100%',
    padding: 0,
    marginTop: '12px',
  };

  return (
    <div>
      <div style={containerStyle}>
        {label && <label htmlFor={inputId} style={labelStyle}>{label}</label>}
        <input
          id={inputId}
          style={inputStyle}
          value={value}
          onChange={onChange}
          onFocus={() => setFocused(true)}
          onBlur={() => setFocused(false)}
          aria-invalid={!!error}
          aria-describedby={supportingText ? helperId : undefined}
          {...props}
        />
      </div>
      {supportingText && (
        <p id={helperId} style={{
          fontSize: '12px',
          color: error ? 'var(--color-error)' : 'var(--color-on-surface-variant)',
          margin: '4px var(--spacing-4) 0',
          fontFamily: 'var(--font-plain)',
        }}>
          {supportingText}
        </p>
      )}
    </div>
  );
}
