import React from 'react'
import { useTranslation } from 'react-i18next'
import AppLayout from '@/layouts/AppLayout'
import {
  useFinancialHealth,
  useTrustProfile,
  useTransactions,
  useNotifications,
} from '@/hooks'
import { formatCurrency, formatDate } from '@/utils'
import {
  PageHeader,
  Loading,
  MetricCard,
  Card,
  TrustScore,
  Badge,
  EmptyState,
} from '@/components'

const UserDashboard: React.FC = () => {
  const { t } = useTranslation()
  const { data: health, isLoading: healthLoading } = useFinancialHealth()
  const { data: trust, isLoading: trustLoading } = useTrustProfile()
  const { data: transactions } = useTransactions(0, 5)
  const { data: notifications } = useNotifications(0, 5)

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

  if (healthLoading || trustLoading) {
    return (
      <AppLayout navItems={navItems}>
        <Loading />
      </AppLayout>
    )
  }

  return (
    <AppLayout navItems={navItems}>
      <PageHeader
        title={t('dashboard.welcome')}
        subtitle="Your financial overview at a glance"
      />

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
        <MetricCard
          label={t('financial.income')}
          value={formatCurrency(health?.income || 0)}
          icon="📈"
        />
        <MetricCard
          label={t('financial.expenses')}
          value={formatCurrency(health?.expenses || 0)}
          icon="📉"
        />
        <MetricCard
          label={t('financial.savings')}
          value={formatCurrency(health?.savings || 0)}
          icon="💎"
        />
        <MetricCard
          label={t('financial.debt')}
          value={formatCurrency(health?.debt || 0)}
          icon="⚠️"
        />
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6 mb-8">
        <Card>
          <div className="text-center">
            <p className="text-text-muted text-sm mb-4">{t('trust.currentScore')}</p>
            <TrustScore
              score={trust?.score || 0}
              level={trust?.level || 'unknown'}
              size="md"
            />
          </div>
        </Card>

        <Card>
          <h3 className="font-semibold text-text-primary mb-4">{t('dashboard.recentTransactions')}</h3>
          {transactions?.items && transactions.items.length > 0 ? (
            <div className="space-y-3">
              {transactions.items.slice(0, 3).map((tx) => (
                <div key={tx.id} className="flex justify-between items-center text-sm">
                  <div>
                    <p className="font-medium text-text-primary">{tx.merchant}</p>
                    <p className="text-text-muted text-xs">{formatDate(tx.date)}</p>
                  </div>
                  <p className="font-semibold text-text-primary">
                    {tx.type === 'income' ? '+' : '-'}
                    {formatCurrency(tx.amount)}
                  </p>
                </div>
              ))}
            </div>
          ) : (
            <EmptyState title="No transactions" />
          )}
        </Card>

        <Card>
          <h3 className="font-semibold text-text-primary mb-4">{t('dashboard.alerts')}</h3>
          {notifications?.items && notifications.items.length > 0 ? (
            <div className="space-y-2">
              {notifications.items.slice(0, 3).map((notif) => (
                <div key={notif.id} className="text-sm">
                  <Badge variant={notif.type as any}>{notif.type}</Badge>
                  <p className="text-text-secondary mt-1">{notif.message}</p>
                </div>
              ))}
            </div>
          ) : (
            <EmptyState title="No alerts" />
          )}
        </Card>
      </div>
    </AppLayout>
  )
}

export default UserDashboard
