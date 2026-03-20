import React from 'react';
import './theme.css';

interface DividerProps {
  inset?: boolean;
  vertical?: boolean;
}

export default function Divider({ inset, vertical }: DividerProps) {
  if (vertical) {
    return <div role="separator" aria-orientation="vertical" style={{ width: '1px', alignSelf: 'stretch', backgroundColor: 'var(--color-outline-variant)' }} />;
  }
  return <hr role="separator" style={{ border: 'none', height: '1px', backgroundColor: 'var(--color-outline-variant)', margin: 0, marginLeft: inset ? 'var(--spacing-4)' : 0 }} />;
}
