import React from 'react'

interface TableProps {
  columns: { key: string; label: string; width?: string }[]
  rows: Record<string, any>[]
  rowKey: string
  isLoading?: boolean
  emptyMessage?: string
}

const Table: React.FC<TableProps> = ({ columns, rows, rowKey, isLoading, emptyMessage }) => {
  if (isLoading) {
    return (
      <div className="flex justify-center py-8">
        <div className="animate-spin">⟳</div>
      </div>
    )
  }

  if (!rows.length) {
    return (
      <div className="flex justify-center py-8 text-text-muted">
        {emptyMessage || 'No data available'}
      </div>
    )
  }

  return (
    <div className="overflow-x-auto">
      <table className="w-full">
        <thead>
          <tr className="border-b border-border bg-bg-page">
            {columns.map((col) => (
              <th
                key={col.key}
                className="px-4 py-3 text-left text-sm font-medium text-text-primary"
                style={{ width: col.width }}
              >
                {col.label}
              </th>
            ))}
          </tr>
        </thead>
        <tbody>
          {rows.map((row) => (
            <tr key={row[rowKey]} className="border-b border-border hover:bg-bg-page transition-colors">
              {columns.map((col) => (
                <td key={`${row[rowKey]}-${col.key}`} className="px-4 py-3 text-sm text-text-secondary">
                  {row[col.key]}
                </td>
              ))}
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  )
}

export default Table
