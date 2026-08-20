import React from 'react'

interface RiskBadgeProps {
  level: 'low' | 'medium' | 'high' | 'critical'
  label?: string
}

const RiskBadge: React.FC<RiskBadgeProps> = ({ level, label }) => {
  const styles = {
    low: 'bg-status-success bg-opacity-10 text-status-success',
    medium: 'bg-status-warning bg-opacity-10 text-status-warning',
    high: 'bg-status-danger bg-opacity-10 text-status-danger',
    critical: 'bg-status-danger bg-opacity-20 text-status-danger border border-status-danger',
  }

  return (
    <span className={`px-3 py-1 rounded-full text-sm font-medium ${styles[level]}`}>
      {label || level.toUpperCase()}
    </span>
  )
}

export default RiskBadge
