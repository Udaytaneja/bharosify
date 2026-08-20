import React from 'react'

interface LoadingProps {
  fullScreen?: boolean
  message?: string
}

const Loading: React.FC<LoadingProps> = ({ fullScreen, message }) => {
  const content = (
    <div className="flex flex-col items-center justify-center gap-4">
      <div className="w-12 h-12 border-4 border-brand-100 border-t-brand-700 rounded-full animate-spin" />
      {message && <p className="text-text-secondary">{message}</p>}
    </div>
  )

  if (fullScreen) {
    return (
      <div className="fixed inset-0 flex items-center justify-center bg-bg-page z-50">
        {content}
      </div>
    )
  }

  return <div className="flex justify-center py-8">{content}</div>
}

export default Loading
