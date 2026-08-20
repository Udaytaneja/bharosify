import React from 'react'
import Card from './Card'

interface MetricCardProps {
  label: string
  value: string | number
  change?: string
  changeType?: 'positive' | 'negative' | 'neutral'
  icon?: string
  trend?: 'up' | 'down' | 'flat'
}

const MetricCard: React.FC<MetricCardProps> = ({ label, value, change, changeType = 'neutral', icon, trend }) => {
  const changeColor = {
    positive: 'text-status-success',
    negative: 'text-status-danger',
    neutral: 'text-text-muted',
  }

  return (
    <Card>
      <div className="flex items-start justify-between">
        <div className="flex-1">
          <p className="text-text-muted text-sm mb-1">{label}</p>
          <p className="text-3xl font-bold text-text-primary">{value}</p>
          {change && (
            <p className={`text-sm mt-2 ${changeColor[changeType]}`}>
              {trend === 'up' && '↑ '}
              {trend === 'down' && '↓ '}
              {change}
            </p>
          )}
        </div>
        {icon && <div className="text-3xl">{icon}</div>}
      </div>
    </Card>
  )
}

export default MetricCard
