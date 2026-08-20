import React from 'react'

interface TextareaProps extends React.TextareaHTMLAttributes<HTMLTextAreaElement> {
  label?: string
  error?: string
  helperText?: string
}

const Textarea = React.forwardRef<HTMLTextAreaElement, TextareaProps>(
  ({ label, error, helperText, className, id, ...props }, ref) => {
    const textareaId = id || label?.toLowerCase().replace(/\s+/g, '_')

    return (
      <div className="w-full">
        {label && (
          <label htmlFor={textareaId} className="block text-sm font-medium text-text-primary mb-2">
            {label}
          </label>
        )}
        <textarea
          ref={ref}
          id={textareaId}
          className={`w-full px-4 py-2 border rounded-lg text-text-primary placeholder-text-muted focus:outline-none focus:ring-2 focus:ring-brand-500 focus:border-transparent transition-colors resize-none ${
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

Textarea.displayName = 'Textarea'
export default Textarea
