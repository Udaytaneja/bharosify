import React from 'react'

interface RadioProps extends React.InputHTMLAttributes<HTMLInputElement> {
  label?: string
}

const Radio = React.forwardRef<HTMLInputElement, RadioProps>(
  ({ label, id, className, ...props }, ref) => {
    const radioId = id || label?.toLowerCase().replace(/\s+/g, '_')

    return (
      <div className="flex items-center gap-2">
        <input
          ref={ref}
          type="radio"
          id={radioId}
          className={`w-4 h-4 border-border focus:ring-2 focus:ring-brand-500 cursor-pointer ${className || ''}`}
          {...props}
        />
        {label && (
          <label htmlFor={radioId} className="text-sm text-text-primary cursor-pointer">
            {label}
          </label>
        )}
      </div>
    )
  }
)

Radio.displayName = 'Radio'
export default Radio
