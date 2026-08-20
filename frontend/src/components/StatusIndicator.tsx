import React from 'react'

interface StatusIndicatorProps {
  status: 'success' | 'warning' | 'danger' | 'pending' | 'info'
  text?: string
}

const StatusIndicator: React.FC<StatusIndicatorProps> = ({ status, text }) => {
  const colors = {
    success: 'bg-status-success',
    warning: 'bg-status-warning',
    danger: 'bg-status-danger',
    pending: 'bg-status-info',
    info: 'bg-status-info',
  }

  return (
    <div className="flex items-center gap-2">
      <div className={`w-2 h-2 rounded-full ${colors[status]}`} />
      {text && <span className="text-sm text-text-secondary">{text}</span>}
    </div>
  )
}

export default StatusIndicator
