import React from 'react'

interface BreadcrumbProps {
  items: { label: string; href?: string }[]
}

const Breadcrumb: React.FC<BreadcrumbProps> = ({ items }) => {
  return (
    <nav className="flex items-center gap-2 mb-6">
      {items.map((item, index) => (
        <React.Fragment key={index}>
          {index > 0 && <span className="text-text-muted">/</span>}
          {item.href ? (
            <a href={item.href} className="text-brand-700 hover:underline">
              {item.label}
            </a>
          ) : (
            <span className="text-text-primary">{item.label}</span>
          )}
        </React.Fragment>
      ))}
    </nav>
  )
}

export default Breadcrumb
