import React from 'react'

interface SelectProps extends React.SelectHTMLAttributes<HTMLSelectElement> {
  label?: string
  error?: string
  helperText?: string
  options: { value: string; label: string }[]
}

const Select = React.forwardRef<HTMLSelectElement, SelectProps>(
  ({ label, error, helperText, options, className, id, ...props }, ref) => {
    const selectId = id || label?.toLowerCase().replace(/\s+/g, '_')

    return (
      <div className="w-full">
        {label && (
          <label htmlFor={selectId} className="block text-sm font-medium text-text-primary mb-2">
            {label}
          </label>
        )}
        <select
          ref={ref}
          id={selectId}
          className={`w-full px-4 py-2 border rounded-lg text-text-primary bg-white focus:outline-none focus:ring-2 focus:ring-brand-500 focus:border-transparent transition-colors ${
            error ? 'border-status-danger bg-red-50' : 'border-border'
          } ${className || ''}`}
          {...props}
        >
          {options.map((opt) => (
            <option key={opt.value} value={opt.value}>
              {opt.label}
            </option>
          ))}
        </select>
        {error && <p className="text-status-danger text-sm mt-1">{error}</p>}
        {helperText && !error && <p className="text-text-muted text-sm mt-1">{helperText}</p>}
      </div>
    )
  }
)

Select.displayName = 'Select'
export default Select
