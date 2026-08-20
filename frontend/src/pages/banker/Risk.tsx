import React from 'react'
import { useTranslation } from 'react-i18next'
import AppLayout from '@/layouts/AppLayout'
import { PageHeader, Card, EmptyState } from '@/components'

const BankerRisk: React.FC = () => {
  const { t } = useTranslation()

  const navItems = [
    { label: t('nav.bankerDashboard'), href: '/banker', icon: '📊' },
    { label: t('nav.risk'), href: '/banker/risk', icon: '⚠️' },
  ]

  return (
    <AppLayout navItems={navItems}>
      <PageHeader title={t('nav.risk')} subtitle="Risk assessments and alerts" />

      <Card>
        <h2 className="text-lg font-semibold text-text-primary mb-4">
          Risk Assessments
        </h2>
        <EmptyState title="No risk assessments" />
      </Card>
    </AppLayout>
  )
}

export default BankerRisk
