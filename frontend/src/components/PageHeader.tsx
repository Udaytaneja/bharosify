import React from 'react'

interface PageHeaderProps {
  title: string
  subtitle?: string
  actions?: React.ReactNode
  action?: React.ReactNode
}

const PageHeader: React.FC<PageHeaderProps> = ({ title, subtitle, actions, action }) => {
  const displayActions = actions || action
  return (
    <div className="mb-8 flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4">
      <div>
        <h1 className="text-2xl lg:text-3xl font-bold text-text-primary mb-1">{title}</h1>
        {subtitle && <p className="text-text-secondary text-sm">{subtitle}</p>}
      </div>
      {displayActions && <div className="flex gap-2 flex-shrink-0">{displayActions}</div>}
    </div>
  )
}

export default PageHeader
