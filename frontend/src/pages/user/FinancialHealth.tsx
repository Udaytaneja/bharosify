import React from 'react'
import { useTranslation } from 'react-i18next'
import AppLayout from '@/layouts/AppLayout'
import { useFinancialHealth } from '@/hooks'
import { formatCurrency } from '@/utils'
import { PageHeader, Loading, Card, MetricCard, EmptyState } from '@/components'

const UserFinancialHealth: React.FC = () => {
  const { t } = useTranslation()
  const { data: health, isLoading } = useFinancialHealth()

  const navItems = [
    { label: t('nav.home'), href: '/user', icon: '🏠' },
    { label: t('nav.financialHealth'), href: '/user/financial-health', icon: '📊' },
    { label: t('nav.trust'), href: '/user/trust', icon: '🛡️' },
    { label: t('nav.transactions'), href: '/user/transactions', icon: '💳' },
    { label: t('nav.applications'), href: '/user/applications', icon: '📋' },
    { label: t('nav.loans'), href: '/user/loans', icon: '💰' },
    { label: t('nav.repayment'), href: '/user/repayment', icon: '📅' },
    { label: t('nav.aiAssistant'), href: '/user/ai-assistant', icon: '🤖' },
    { label: t('nav.notifications'), href: '/user/notifications', icon: '🔔' },
    { label: t('nav.settings'), href: '/user/settings', icon: '⚙️' },
  ]

  if (isLoading) {
    return (
      <AppLayout navItems={navItems}>
        <Loading />
      </AppLayout>
    )
  }

  if (!health) {
    return (
      <AppLayout navItems={navItems}>
        <EmptyState title="No financial data available" />
      </AppLayout>
    )
  }

  return (
    <AppLayout navItems={navItems}>
      <PageHeader
        title={t('nav.financialHealth')}
        subtitle="Your complete financial overview"
      />

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 mb-8">
        <MetricCard
          label={t('financial.income')}
          value={formatCurrency(health.income)}
          icon="📈"
        />
        <MetricCard
          label={t('financial.expenses')}
          value={formatCurrency(health.expenses)}
          icon="📉"
        />
        <MetricCard
          label={t('financial.savings')}
          value={formatCurrency(health.savings)}
          icon="💎"
        />
        <MetricCard
          label={t('financial.debt')}
          value={formatCurrency(health.debt)}
          icon="⚠️"
        />
        <MetricCard
          label={t('financial.repaymentBurden')}
          value={`${(health.repayment_burden * 100).toFixed(1)}%`}
          icon="📊"
        />
        <MetricCard
          label={t('financial.financialStability')}
          value={health.status}
          icon="🎯"
        />
      </div>

      <Card>
        <h2 className="text-lg font-semibold text-text-primary mb-4">Details</h2>
        <div className="grid grid-cols-2 gap-4">
          <div>
            <p className="text-text-muted text-sm">Score</p>
            <p className="text-2xl font-bold text-text-primary">{health.score}</p>
          </div>
          <div>
            <p className="text-text-muted text-sm">Status</p>
            <p className="text-2xl font-bold text-brand-700">{health.status}</p>
          </div>
        </div>
      </Card>
    </AppLayout>
  )
}

export default UserFinancialHealth
