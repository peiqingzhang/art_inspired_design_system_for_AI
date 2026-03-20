import React from 'react';
import './theme.css';

interface ButtonProps {
  variant?: 'filled' | 'outlined' | 'tonal' | 'text';
  disabled?: boolean;
  onClick?: () => void;
  children: React.ReactNode;
  [key: string]: unknown;
}

const buttonBase = {
  display: 'inline-flex',
  alignItems: 'center',
  justifyContent: 'center',
  gap: 'var(--spacing-2)',
  height: '40px',
  border: 'none',
  cursor: 'pointer',
  fontFamily: 'var(--font-plain)',
  fontSize: '14px',
  fontWeight: 500,
  letterSpacing: '0.1px',
  lineHeight: '20px',
  position: 'relative',
  overflow: 'hidden',
};

const variants = {
  filled: {
    ...buttonBase,
    backgroundColor: 'var(--color-primary)',
    color: 'var(--color-on-primary)',
    borderRadius: 'var(--radius-full)',
    padding: '0 var(--spacing-6)',
  },
  outlined: {
    ...buttonBase,
    backgroundColor: 'transparent',
    color: 'var(--color-primary)',
    border: '1px solid var(--color-outline)',
    borderRadius: 'var(--radius-full)',
    padding: '0 var(--spacing-6)',
  },
  tonal: {
    ...buttonBase,
    backgroundColor: 'var(--color-secondary-container)',
    color: 'var(--color-on-secondary-container)',
    borderRadius: 'var(--radius-full)',
    padding: '0 var(--spacing-6)',
  },
  text: {
    ...buttonBase,
    backgroundColor: 'transparent',
    color: 'var(--color-primary)',
    borderRadius: 'var(--radius-full)',
    padding: '0 var(--spacing-3)',
  },
};

export default function Button({ variant = 'filled', children, disabled, ...props }: ButtonProps): React.FC<ButtonProps> {
  const handleKeyDown = (e: React.KeyboardEvent<HTMLButtonElement>) => {
    if ((e.key === 'Enter' || e.key === ' ') && props.onClick) props.onClick();
  };
  return (
    <button
      style={{
        ...variants[variant ?? 'filled'],
        ...(disabled ? { opacity: 0.38, pointerEvents: 'none' } : {}),
      }}
      disabled={disabled}
      aria-disabled={disabled}
      className="m3-interactive"
      onKeyDown={handleKeyDown}
      {...props}
    >
      <span className="state-layer" aria-hidden="true" />
      {children}
    </button>
  );
}

Button.Filled = (props: Omit<ButtonProps, "variant">) => <Button variant="filled" {...props} />;
Button.Outlined = (props: Omit<ButtonProps, "variant">) => <Button variant="outlined" {...props} />;
Button.Tonal = (props: Omit<ButtonProps, "variant">) => <Button variant="tonal" {...props} />;
Button.Text = (props: Omit<ButtonProps, "variant">) => <Button variant="text" {...props} />;
