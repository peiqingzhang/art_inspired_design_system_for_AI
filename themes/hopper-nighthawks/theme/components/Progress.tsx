import React from 'react';
import './theme.css';

interface ProgressProps {
  value?: number;
  variant?: 'linear' | 'circular';
  indeterminate?: boolean;
  [key: string]: unknown;
}

export default function Progress({ value = 0, variant = 'linear', indeterminate, ...props }: ProgressProps) {
  if (variant === 'circular') {
    const size = 48;
    const stroke = 4;
    const radius = (size - stroke) / 2;
    const circumference = 2 * Math.PI * radius;
    const offset = indeterminate ? circumference * 0.75 : circumference * (1 - value / 100);

    return (
      <div role="progressbar" aria-valuenow={indeterminate ? undefined : value} aria-valuemin={0} aria-valuemax={100} {...props}>
        <svg
          width={size}
          height={size}
          viewBox={`0 0 ${size} ${size}`}
          style={indeterminate ? { animation: 'spin 1.4s linear infinite' } : undefined}
        >
          <circle cx={size / 2} cy={size / 2} r={radius} fill="none" stroke="var(--color-surface-container-highest)" strokeWidth={stroke} />
          <circle
            cx={size / 2}
            cy={size / 2}
            r={radius}
            fill="none"
            stroke="var(--color-primary)"
            strokeWidth={stroke}
            strokeDasharray={circumference}
            strokeDashoffset={offset}
            strokeLinecap="round"
            transform={`rotate(-90 ${size / 2} ${size / 2})`}
            style={{ transition: indeterminate ? 'none' : 'stroke-dashoffset 0.3s ease' }}
          />
        </svg>
        <style>{`@keyframes spin { to { transform: rotate(360deg); } }`}</style>
      </div>
    );
  }

  return (
    <div
      role="progressbar"
      aria-valuenow={indeterminate ? undefined : value}
      aria-valuemin={0}
      aria-valuemax={100}
      style={{
        width: '100%',
        height: '4px',
        backgroundColor: 'var(--color-surface-container-highest)',
        borderRadius: 'var(--radius-full)',
        overflow: 'hidden',
      }}
      {...props}
    >
      <div
        style={{
          height: '100%',
          backgroundColor: 'var(--color-primary)',
          borderRadius: 'var(--radius-full)',
          width: indeterminate ? '30%' : `${value}%`,
          transition: indeterminate ? 'none' : 'width 0.3s ease',
          animation: indeterminate ? 'indeterminate 1.5s ease-in-out infinite' : 'none',
        }}
      />
      {indeterminate && (
        <style>{`@keyframes indeterminate { 0% { margin-left: -30%; } 100% { margin-left: 100%; } }`}</style>
      )}
    </div>
  );
}
