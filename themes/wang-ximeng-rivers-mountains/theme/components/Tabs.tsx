import React, { useState } from 'react';
import './theme.css';

interface Tab {
  label: string;
  icon?: React.ReactNode;
}

interface TabsProps {
  tabs: Tab[];
  activeIndex?: number;
  onChange?: (index: number) => void;
  [key: string]: unknown;
}

export default function Tabs({ tabs, activeIndex: controlledIndex, onChange, ...props }: TabsProps) {
  const [internalIndex, setInternalIndex] = useState(0);
  const activeIndex = controlledIndex ?? internalIndex;

  const handleSelect = (i: number) => {
    setInternalIndex(i);
    onChange?.(i);
  };

  return (
    <div
      role="tablist"
      style={{
        display: 'flex',
        backgroundColor: 'var(--color-surface-container)',
        borderBottom: '1px solid var(--color-outline-variant)',
      }}
      {...props}
    >
      {tabs.map((tab: Tab, i: number) => (
        <button
          key={i}
          role="tab"
          aria-selected={i === activeIndex}
          tabIndex={i === activeIndex ? 0 : -1}
          onClick={() => handleSelect(i)}
          onKeyDown={(e) => {
            if (e.key === 'ArrowRight') handleSelect((i + 1) % tabs.length);
            if (e.key === 'ArrowLeft') handleSelect((i - 1 + tabs.length) % tabs.length);
          }}
          className="m3-interactive"
          style={{
            flex: 1,
            display: 'flex',
            flexDirection: 'column',
            alignItems: 'center',
            justifyContent: 'center',
            gap: 'var(--spacing-1)',
            height: tab.icon ? '64px' : '48px',
            padding: '0 var(--spacing-4)',
            border: 'none',
            cursor: 'pointer',
            backgroundColor: 'transparent',
            color: i === activeIndex ? 'var(--color-on-surface)' : 'var(--color-on-surface-variant)',
            fontFamily: 'var(--font-plain)',
            fontSize: '14px',
            fontWeight: 500,
            letterSpacing: '0.1px',
            position: 'relative',
            overflow: 'hidden',
            borderBottom: i === activeIndex ? '3px solid var(--color-primary)' : '3px solid transparent',
          }}
        >
          <span className="state-layer" aria-hidden="true" />
          {tab.icon && <span>{tab.icon}</span>}
          <span>{tab.label}</span>
        </button>
      ))}
    </div>
  );
}
