import React from 'react'
import { useTranslation } from 'react-i18next'
import AppLayout from '@/layouts/AppLayout'
import { PageHeader, Card, EmptyState } from '@/components'

const BankerUnderwriting: React.FC = () => {
  const { t } = useTranslation()

  const navItems = [
    { label: t('nav.bankerDashboard'), href: '/banker', icon: '📊' },
    { label: t('nav.underwriting'), href: '/banker/underwriting', icon: '🔍' },
  ]

  return (
    <AppLayout navItems={navItems}>
      <PageHeader title={t('nav.underwriting')} />

      <Card>
        <h2 className="text-lg font-semibold text-text-primary mb-4">
          Underwriting Queue
        </h2>
        <EmptyState title="No applications in queue" />
      </Card>
    </AppLayout>
  )
}

export default BankerUnderwriting
