import React from 'react'
import Button from './Button'

interface ErrorStateProps {
  message: string
  title?: string
  onRetry?: () => void
  details?: string
}

const ErrorState: React.FC<ErrorStateProps> = ({ message, title = 'Something went wrong', onRetry, details }) => {
  return (
    <div className="flex flex-col items-center justify-center py-12 px-4">
      <div className="text-5xl mb-4">⚠️</div>
      <h3 className="text-lg font-semibold text-text-primary mb-2">{title}</h3>
      <p className="text-text-muted text-center mb-4 max-w-sm">{message}</p>
      {details && <p className="text-status-danger text-sm text-center mb-4 max-w-sm">{details}</p>}
      {onRetry && (
        <Button onClick={onRetry} variant="primary">
          Try Again
        </Button>
      )}
    </div>
  )
}

export default ErrorState
