import React from 'react'

interface InputProps extends React.InputHTMLAttributes<HTMLInputElement> {
  label?: string
  error?: string
  helperText?: string
}

const Input = React.forwardRef<HTMLInputElement, InputProps>(
  ({ label, error, helperText, className, id, ...props }, ref) => {
    const inputId = id || label?.toLowerCase().replace(/\s+/g, '_')

    return (
      <div className="w-full">
        {label && (
          <label htmlFor={inputId} className="block text-sm font-medium text-text-primary mb-2">
            {label}
          </label>
        )}
        <input
          ref={ref}
          id={inputId}
          className={`w-full px-4 py-2 border rounded-lg text-text-primary placeholder-text-muted focus:outline-none focus:ring-2 focus:ring-brand-500 focus:border-transparent transition-colors ${
            error ? 'border-status-danger bg-red-50' : 'border-border bg-white'
          } ${className || ''}`}
          {...props}
        />
        {error && <p className="text-status-danger text-sm mt-1">{error}</p>}
        {helperText && !error && <p className="text-text-muted text-sm mt-1">{helperText}</p>}
      </div>
    )
  }
)

Input.displayName = 'Input'
export default Input
