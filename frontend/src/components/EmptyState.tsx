import React from 'react'

interface EmptyStateProps {
  icon?: string
  title: string
  message?: string
  action?: React.ReactNode
}

const EmptyState: React.FC<EmptyStateProps> = ({ icon = '📭', title, message, action }) => {
  return (
    <div className="flex flex-col items-center justify-center py-12 px-4">
      <div className="text-5xl mb-4">{icon}</div>
      <h3 className="text-lg font-semibold text-text-primary mb-2">{title}</h3>
      {message && <p className="text-text-muted text-center mb-4 max-w-sm">{message}</p>}
      {action && <div>{action}</div>}
    </div>
  )
}

export default EmptyState
