import React from 'react'

interface CardProps {
  children: React.ReactNode
  className?: string
  hoverable?: boolean
}

const Card: React.FC<CardProps> = ({ children, className, hoverable }) => {
  return (
    <div
      className={`bg-bg-surface border border-border rounded-lg p-6 shadow-sm ${
        hoverable ? 'hover:shadow-md transition-shadow cursor-pointer' : ''
      } ${className || ''}`}
    >
      {children}
    </div>
  )
}

export default Card
