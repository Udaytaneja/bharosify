import React from 'react'
import { useTranslation } from 'react-i18next'
import AppLayout from '@/layouts/AppLayout'
import { useFinancialHealth } from '@/hooks'
import { formatCurrency } from '@/utils'
import { PageHeader, Loading, Card, MetricCard, EmptyState, Badge } from '@/components'

const UserFinancialHealth: React.FC = () => {
  const { t } = useTranslation()
  const { data: health, isLoading } = useFinancialHealth()

  if (isLoading) {
    return (
      <AppLayout>
        <Loading />
      </AppLayout>
    )
  }

  if (!health) {
    return (
      <AppLayout>
        <EmptyState title="No financial data available" description="Your financial health record is being initialized." />
      </AppLayout>
    )
  }

  return (
    <AppLayout>
      <PageHeader
        title={t('nav.financialHealth')}
        subtitle="Your complete financial assessment and balance breakdown"
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
        <h2 className="text-lg font-semibold text-text-primary mb-4">Financial Health Assessment</h2>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 p-4 bg-bg-page rounded-xl border border-border">
          <div>
            <p className="text-text-muted text-xs uppercase tracking-wider mb-1">Financial Score</p>
            <p className="text-3xl font-extrabold text-brand-700">{health.score} / 100</p>
          </div>
          <div>
            <p className="text-text-muted text-xs uppercase tracking-wider mb-1">Stability Rating</p>
            <Badge variant={health.score >= 70 ? 'success' : health.score >= 50 ? 'warning' : 'danger'}>
              {health.status}
            </Badge>
          </div>
          <div>
            <p className="text-text-muted text-xs uppercase tracking-wider mb-1">Last Evaluation</p>
            <p className="text-sm font-medium text-text-primary">{new Date(health.updated_at).toLocaleDateString()}</p>
          </div>
        </div>
      </Card>
    </AppLayout>
  )
}

export default UserFinancialHealth
