import React from 'react';
import './theme.css';

interface TableColumn {
  key: string;
  header: string;
  align?: 'left' | 'center' | 'right';
}

interface TableProps {
  columns: TableColumn[];
  data: Record<string, React.ReactNode>[];
  striped?: boolean;
  [key: string]: unknown;
}

export default function Table({ columns, data, striped, ...props }: TableProps) {
  return (
    <div style={{ overflowX: 'auto', borderRadius: 'var(--radius-medium)', border: '1px solid var(--color-outline-variant)' }}>
      <table
        style={{
          width: '100%',
          borderCollapse: 'collapse',
          fontFamily: 'var(--font-plain)',
          fontSize: '14px',
          lineHeight: '20px',
          color: 'var(--color-on-surface)',
        }}
        {...props}
      >
        <thead>
          <tr style={{ backgroundColor: 'var(--color-surface-container)' }}>
            {columns.map((col: TableColumn) => (
              <th
                key={col.key}
                style={{
                  padding: 'var(--spacing-3) var(--spacing-4)',
                  textAlign: col.align || 'left',
                  fontWeight: 500,
                  fontSize: '12px',
                  letterSpacing: '0.5px',
                  color: 'var(--color-on-surface-variant)',
                  borderBottom: '1px solid var(--color-outline-variant)',
                }}
              >
                {col.header}
              </th>
            ))}
          </tr>
        </thead>
        <tbody>
          {data.map((row, i: number) => (
            <tr
              key={i}
              style={{
                backgroundColor: striped && i % 2 === 1 ? 'var(--color-surface-container-lowest)' : 'var(--color-surface)',
                borderBottom: '1px solid var(--color-outline-variant)',
              }}
            >
              {columns.map((col: TableColumn) => (
                <td
                  key={col.key}
                  style={{
                    padding: 'var(--spacing-3) var(--spacing-4)',
                    textAlign: col.align || 'left',
                  }}
                >
                  {row[col.key]}
                </td>
              ))}
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
