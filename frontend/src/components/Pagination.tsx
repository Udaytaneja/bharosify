import React from 'react'

interface PaginationProps {
  currentPage: number
  totalPages: number
  onPageChange: (page: number) => void
  maxVisible?: number
}

const Pagination: React.FC<PaginationProps> = ({ currentPage, totalPages, onPageChange, maxVisible = 5 }) => {
  const startPage = Math.max(1, currentPage - Math.floor(maxVisible / 2))
  const endPage = Math.min(totalPages, startPage + maxVisible - 1)
  const adjustedStartPage = Math.max(1, endPage - maxVisible + 1)

  const pages = Array.from({ length: Math.min(maxVisible, totalPages) }, (_, i) => adjustedStartPage + i)

  return (
    <div className="flex items-center justify-center gap-2 mt-6">
      <button
        onClick={() => onPageChange(currentPage - 1)}
        disabled={currentPage === 1}
        className="px-3 py-2 border border-border rounded-lg text-sm font-medium text-text-primary hover:bg-bg-page disabled:opacity-50 disabled:cursor-not-allowed"
      >
        Previous
      </button>

      {adjustedStartPage > 1 && (
        <>
          <button
            onClick={() => onPageChange(1)}
            className="px-3 py-2 border border-border rounded-lg text-sm font-medium text-text-primary hover:bg-bg-page"
          >
            1
          </button>
          {adjustedStartPage > 2 && <span className="text-text-muted">...</span>}
        </>
      )}

      {pages.map((page) => (
        <button
          key={page}
          onClick={() => onPageChange(page)}
          className={`px-3 py-2 rounded-lg text-sm font-medium transition-colors ${
            currentPage === page
              ? 'bg-brand-700 text-white'
              : 'border border-border text-text-primary hover:bg-bg-page'
          }`}
        >
          {page}
        </button>
      ))}

      {endPage < totalPages && (
        <>
          {endPage < totalPages - 1 && <span className="text-text-muted">...</span>}
          <button
            onClick={() => onPageChange(totalPages)}
            className="px-3 py-2 border border-border rounded-lg text-sm font-medium text-text-primary hover:bg-bg-page"
          >
            {totalPages}
          </button>
        </>
      )}

      <button
        onClick={() => onPageChange(currentPage + 1)}
        disabled={currentPage === totalPages}
        className="px-3 py-2 border border-border rounded-lg text-sm font-medium text-text-primary hover:bg-bg-page disabled:opacity-50 disabled:cursor-not-allowed"
      >
        Next
      </button>
    </div>
  )
}

export default Pagination
