import React from 'react';
import './theme.css';

interface AvatarProps {
  name?: string;
  src?: string;
  size?: number;
}

export default function Avatar({ name, src, size = 40 }: AvatarProps) {
  const initials = name ? name.split(' ').map((n: string) => n[0]).join('').slice(0, 2).toUpperCase() : '?';
  const fontSize = size * 0.4;
  const label = name || 'User avatar';

  if (src) {
    return (
      <img
        src={src}
        alt={label}
        aria-label={label}
        style={{
          width: size, height: size,
          borderRadius: 'var(--radius-full)',
          objectFit: 'cover',
        }}
      />
    );
  }

  return (
    <div
      aria-label={label}
      role="img"
      style={{
        width: size, height: size,
        borderRadius: 'var(--radius-full)',
        backgroundColor: 'var(--color-primary-container)',
        color: 'var(--color-on-primary-container)',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
        fontSize,
        fontWeight: 500,
        fontFamily: 'var(--font-plain)',
      }}
    >
      {initials}
    </div>
  );
}
