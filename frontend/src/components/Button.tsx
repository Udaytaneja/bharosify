import React from 'react'

interface ButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: 'primary' | 'secondary' | 'outline' | 'danger'
  size?: 'sm' | 'md' | 'lg'
  isLoading?: boolean
  fullWidth?: boolean
}

const Button = React.forwardRef<HTMLButtonElement, ButtonProps>(
  (
    {
      variant = 'primary',
      size = 'md',
      isLoading = false,
      fullWidth = false,
      disabled,
      children,
      className,
      ...props
    },
    ref
  ) => {
    const baseStyles = 'font-medium rounded-lg transition-colors duration-200 flex items-center justify-center gap-2 focus:outline-none focus:ring-2 focus:ring-offset-2 disabled:opacity-50 disabled:cursor-not-allowed'

    const variants = {
      primary: 'bg-brand-700 text-white hover:bg-brand-800 focus:ring-brand-500',
      secondary: 'bg-bg-page text-text-primary border border-border hover:bg-gray-50 focus:ring-brand-500',
      outline: 'border-2 border-brand-700 text-brand-700 hover:bg-brand-50 focus:ring-brand-500',
      danger: 'bg-status-danger text-white hover:bg-red-700 focus:ring-status-danger',
    }

    const sizes = {
      sm: 'px-3 py-1.5 text-sm',
      md: 'px-4 py-2 text-base',
      lg: 'px-6 py-3 text-lg',
    }

    return (
      <button
        ref={ref}
        disabled={disabled || isLoading}
        className={`${baseStyles} ${variants[variant]} ${sizes[size]} ${fullWidth ? 'w-full' : ''} ${className || ''}`}
        {...props}
      >
        {isLoading && <span className="animate-spin">⟳</span>}
        {children}
      </button>
    )
  }
)

Button.displayName = 'Button'
export default Button
