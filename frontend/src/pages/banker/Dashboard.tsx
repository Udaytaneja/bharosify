import React from 'react'
import { useTranslation } from 'react-i18next'
import AppLayout from '@/layouts/AppLayout'
import { PageHeader, Card, EmptyState, MetricCard } from '@/components'

const BankerDashboard: React.FC = () => {
  const { t } = useTranslation()

  const navItems = [
    { label: t('nav.bankerDashboard'), href: '/banker', icon: '📊' },
    { label: t('nav.customers'), href: '/banker/customers', icon: '👥' },
    { label: t('nav.applications'), href: '/banker/applications', icon: '📋' },
    { label: t('nav.underwriting'), href: '/banker/underwriting', icon: '🔍' },
    { label: t('nav.loans'), href: '/banker/loans', icon: '💰' },
    { label: t('nav.risk'), href: '/banker/risk', icon: '⚠️' },
    { label: t('nav.fraud'), href: '/banker/fraud', icon: '🚨' },
    { label: t('nav.notifications'), href: '/banker/notifications', icon: '🔔' },
    { label: t('nav.settings'), href: '/banker/settings', icon: '⚙️' },
  ]

  return (
    <AppLayout navItems={navItems}>
      <PageHeader
        title="Banker Dashboard"
        subtitle="Manage applications, customers, and risk"
      />

      <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
        <MetricCard label="Pending Applications" value="12" icon="📋" />
        <MetricCard label="Active Loans" value="234" icon="💰" />
        <MetricCard label="Risk Alerts" value="3" icon="⚠️" />
        <MetricCard label="Fraud Cases" value="1" icon="🚨" />
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <Card>
          <h2 className="text-lg font-semibold text-text-primary mb-4">
            Applications Requiring Attention
          </h2>
          <EmptyState title="No pending applications" />
        </Card>

        <Card>
          <h2 className="text-lg font-semibold text-text-primary mb-4">
            Recent Risk Alerts
          </h2>
          <EmptyState title="No alerts" />
        </Card>
      </div>
    </AppLayout>
  )
}

export default BankerDashboard
