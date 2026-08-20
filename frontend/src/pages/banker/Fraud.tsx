import React from 'react'
import { useTranslation } from 'react-i18next'
import AppLayout from '@/layouts/AppLayout'
import { PageHeader, Card, EmptyState } from '@/components'

const BankerFraud: React.FC = () => {
  const { t } = useTranslation()

  const navItems = [
    { label: t('nav.bankerDashboard'), href: '/banker', icon: '📊' },
  ]

  return (
    <AppLayout navItems={navItems}>
      <PageHeader title="Fraud Detection" subtitle="Monitor fraud signals" />

      <Card>
        <h2 className="text-lg font-semibold text-text-primary mb-4">
          Fraud Signals
        </h2>
        <EmptyState title="No fraud signals detected" />
      </Card>
    </AppLayout>
  )
}

export default BankerFraud
