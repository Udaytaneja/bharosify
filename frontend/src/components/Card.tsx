import React from 'react'

interface CardProps {
  children: React.ReactNode
  className?: string
  hoverable?: boolean
  onClick?: () => void
}

const Card: React.FC<CardProps> = ({ children, className, hoverable, onClick }) => {
  return (
    <div
      onClick={onClick}
      className={`bg-bg-surface border border-border rounded-xl p-6 shadow-xs ${
        hoverable || onClick ? 'hover:shadow-md transition-all cursor-pointer' : ''
      } ${className || ''}`}
    >
      {children}
    </div>
  )
}

export default Card
