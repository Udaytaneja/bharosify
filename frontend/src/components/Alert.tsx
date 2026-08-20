import React from 'react'

interface AlertProps {
  type: 'success' | 'warning' | 'danger' | 'info'
  message: string
  title?: string
  onClose?: () => void
}

const Alert: React.FC<AlertProps> = ({ type, message, title, onClose }) => {
  const typeStyles = {
    success: 'bg-status-success bg-opacity-10 border-status-success text-status-success',
    warning: 'bg-status-warning bg-opacity-10 border-status-warning text-status-warning',
    danger: 'bg-status-danger bg-opacity-10 border-status-danger text-status-danger',
    info: 'bg-status-info bg-opacity-10 border-status-info text-status-info',
  }

  return (
    <div className={`border-l-4 rounded p-4 mb-4 ${typeStyles[type]}`}>
      <div className="flex justify-between items-start">
        <div>
          {title && <h4 className="font-medium mb-1">{title}</h4>}
          <p className="text-sm">{message}</p>
        </div>
        {onClose && (
          <button onClick={onClose} className="ml-4 opacity-60 hover:opacity-100">
            ✕
          </button>
        )}
      </div>
    </div>
  )
}

export default Alert
