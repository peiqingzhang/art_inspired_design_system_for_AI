import React from 'react';
import './theme.css';

interface BreadcrumbItem {
  label: string;
  href?: string;
  onClick?: () => void;
}

interface BreadcrumbProps {
  items: BreadcrumbItem[];
  separator?: string;
  [key: string]: unknown;
}

export default function Breadcrumb({ items, separator = '/', ...props }: BreadcrumbProps) {
  return (
    <nav aria-label="Breadcrumb" {...props}>
      <ol
        style={{
          display: 'flex',
          alignItems: 'center',
          gap: 'var(--spacing-2)',
          listStyle: 'none',
          margin: 0,
          padding: 0,
          fontFamily: 'var(--font-plain)',
          fontSize: '14px',
          lineHeight: '20px',
        }}
      >
        {items.map((item: BreadcrumbItem, i: number) => (
          <li key={i} style={{ display: 'flex', alignItems: 'center', gap: 'var(--spacing-2)' }}>
            {i > 0 && <span style={{ color: 'var(--color-on-surface-variant)' }}>{separator}</span>}
            {i < items.length - 1 ? (
              <a
                href={item.href || '#'}
                onClick={(e: React.MouseEvent) => { if (item.onClick) { e.preventDefault(); item.onClick(); } }}
                style={{
                  color: 'var(--color-primary)',
                  textDecoration: 'none',
                  fontWeight: 500,
                }}
              >
                {item.label}
              </a>
            ) : (
              <span
                aria-current="page"
                style={{ color: 'var(--color-on-surface)', fontWeight: 500 }}
              >
                {item.label}
              </span>
            )}
          </li>
        ))}
      </ol>
    </nav>
  );
}
