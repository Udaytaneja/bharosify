import React from 'react'

interface TrustScoreProps {
  score: number
  level: string
  size?: 'sm' | 'md' | 'lg'
}

const TrustScore: React.FC<TrustScoreProps> = ({ score, level, size = 'md' }) => {
  const getColor = () => {
    if (score >= 90) return 'text-status-success'
    if (score >= 70) return 'text-brand-500'
    if (score >= 40) return 'text-status-warning'
    return 'text-status-danger'
  }

  const sizes = {
    sm: 'w-16 h-16 text-lg',
    md: 'w-24 h-24 text-3xl',
    lg: 'w-32 h-32 text-4xl',
  }

  return (
    <div className="flex flex-col items-center gap-2">
      <div
        className={`flex items-center justify-center rounded-full border-4 border-brand-100 ${sizes[size]} ${getColor()}`}
      >
        {score}
      </div>
      <span className="text-sm font-medium text-text-secondary capitalize">{level}</span>
    </div>
  )
}

export default TrustScore
