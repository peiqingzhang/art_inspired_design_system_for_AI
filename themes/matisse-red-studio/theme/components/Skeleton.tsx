import React from 'react';
import './theme.css';

interface SkeletonProps {
  variant?: 'text' | 'rectangular' | 'circular';
  width?: string | number;
  height?: string | number;
  lines?: number;
  [key: string]: unknown;
}

export default function Skeleton({ variant = 'text', width, height, lines = 1, ...props }: SkeletonProps) {
  const baseStyle: React.CSSProperties = {
    backgroundColor: 'var(--color-surface-container-highest)',
    animation: 'skeleton-pulse 1.5s ease-in-out infinite',
  };

  if (variant === 'circular') {
    const size = width || height || '40px';
    return (
      <>
        <div style={{ ...baseStyle, width: size, height: size, borderRadius: 'var(--radius-full)' }} aria-hidden="true" {...props} />
        <style>{`@keyframes skeleton-pulse { 0%, 100% { opacity: 1; } 50% { opacity: 0.4; } }`}</style>
      </>
    );
  }

  if (variant === 'rectangular') {
    return (
      <>
        <div
          style={{ ...baseStyle, width: width || '100%', height: height || '120px', borderRadius: 'var(--radius-medium)' }}
          aria-hidden="true"
          {...props}
        />
        <style>{`@keyframes skeleton-pulse { 0%, 100% { opacity: 1; } 50% { opacity: 0.4; } }`}</style>
      </>
    );
  }

  return (
    <>
      <div style={{ display: 'flex', flexDirection: 'column', gap: 'var(--spacing-2)', width: width || '100%' }} aria-hidden="true" {...props}>
        {Array.from({ length: lines }).map((_, i) => (
          <div
            key={i}
            style={{
              ...baseStyle,
              height: height || '16px',
              borderRadius: 'var(--radius-extra-small)',
              width: i === lines - 1 && lines > 1 ? '75%' : '100%',
            }}
          />
        ))}
      </div>
      <style>{`@keyframes skeleton-pulse { 0%, 100% { opacity: 1; } 50% { opacity: 0.4; } }`}</style>
    </>
  );
}
