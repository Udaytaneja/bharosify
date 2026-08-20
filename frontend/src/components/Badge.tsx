import React from 'react'

interface BadgeProps {
  children: React.ReactNode
  variant?: 'default' | 'success' | 'warning' | 'danger' | 'info'
  className?: string
}

const Badge: React.FC<BadgeProps> = ({ children, variant = 'default', className }) => {
  const variants = {
    default: 'bg-text-muted bg-opacity-10 text-text-muted',
    success: 'bg-status-success bg-opacity-10 text-status-success',
    warning: 'bg-status-warning bg-opacity-10 text-status-warning',
    danger: 'bg-status-danger bg-opacity-10 text-status-danger',
    info: 'bg-status-info bg-opacity-10 text-status-info',
  }

  return (
    <span className={`px-2.5 py-0.5 rounded-full text-xs font-medium ${variants[variant]} ${className || ''}`}>
      {children}
    </span>
  )
}

export default Badge
