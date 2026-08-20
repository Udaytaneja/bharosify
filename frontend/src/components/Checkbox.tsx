import React from 'react'

interface CheckboxProps extends React.InputHTMLAttributes<HTMLInputElement> {
  label?: string
}

const Checkbox = React.forwardRef<HTMLInputElement, CheckboxProps>(
  ({ label, id, className, ...props }, ref) => {
    const checkboxId = id || label?.toLowerCase().replace(/\s+/g, '_')

    return (
      <div className="flex items-center gap-2">
        <input
          ref={ref}
          type="checkbox"
          id={checkboxId}
          className={`w-4 h-4 border-border rounded focus:ring-2 focus:ring-brand-500 cursor-pointer ${className || ''}`}
          {...props}
        />
        {label && (
          <label htmlFor={checkboxId} className="text-sm text-text-primary cursor-pointer">
            {label}
          </label>
        )}
      </div>
    )
  }
)

Checkbox.displayName = 'Checkbox'
export default Checkbox
