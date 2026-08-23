import React from 'react'
import { useTranslation } from 'react-i18next'
import { useNavigate } from 'react-router-dom'
import AppLayout from '@/layouts/AppLayout'
import {
  useFinancialHealth,
  useTrustProfile,
  useTransactions,
  useNotifications,
  useAuth,
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
  Button,
} from '@/components'

const UserDashboard: React.FC = () => {
  const { t } = useTranslation()
  const navigate = useNavigate()
  const { user } = useAuth()
  const { data: health, isLoading: healthLoading } = useFinancialHealth()
  const { data: trust, isLoading: trustLoading } = useTrustProfile()
  const { data: transactions } = useTransactions(0, 5)
  const { data: notifications } = useNotifications(0, 5)

  if (healthLoading || trustLoading) {
    return (
      <AppLayout>
        <Loading />
      </AppLayout>
    )
  }

  return (
    <AppLayout>
      <PageHeader
        title={`${t('dashboard.welcome')}, ${user?.name || 'User'}!`}
        subtitle="Here is your financial status and recommended next steps"
      />

      {/* Metric Overview */}
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

      {/* Quick Action Banner */}
      <Card className="mb-8 bg-gradient-to-r from-brand-900 to-brand-700 text-white p-6 rounded-2xl shadow-md border-0">
        <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4">
          <div>
            <h3 className="text-xl font-bold text-white mb-1">Financial Quick Actions</h3>
            <p className="text-brand-100 text-sm">Apply for loans, view repayment schedules, or ask your AI advisor.</p>
          </div>
          <div className="flex flex-wrap gap-3">
            <Button
              variant="secondary"
              onClick={() => navigate('/user/applications')}
            >
              📋 Apply for Loan
            </Button>
            <Button
              variant="secondary"
              onClick={() => navigate('/user/repayments')}
            >
              💳 Repayments
            </Button>
            <Button
              variant="primary"
              onClick={() => navigate('/user/ai-assistant')}
            >
              🤖 AI Advisor
            </Button>
          </div>
        </div>
      </Card>

      {/* Trust, Transactions, Alerts */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6 mb-8">
        <Card className="flex flex-col items-center justify-center">
          <p className="text-text-muted text-xs uppercase tracking-wider mb-4">{t('trust.currentScore')}</p>
          <TrustScore
            score={trust?.score || 0}
            level={trust?.level || 'unknown'}
            size="md"
          />
          <Button
            variant="secondary"
            size="sm"
            className="mt-4"
            onClick={() => navigate('/user/trust')}
          >
            View Trust Drivers →
          </Button>
        </Card>

        <Card>
          <div className="flex justify-between items-center mb-4">
            <h3 className="font-semibold text-text-primary">{t('dashboard.recentTransactions')}</h3>
            <button
              onClick={() => navigate('/user/transactions')}
              className="text-xs font-semibold text-brand-700 hover:underline"
            >
              {t('dashboard.viewAll')}
            </button>
          </div>
          {transactions?.items && transactions.items.length > 0 ? (
            <div className="space-y-3">
              {transactions.items.slice(0, 4).map((tx) => (
                <div key={tx.id} className="flex justify-between items-center text-sm py-1 border-b border-border/50 last:border-0">
                  <div>
                    <p className="font-medium text-text-primary">{tx.merchant}</p>
                    <p className="text-text-muted text-xs">{formatDate(tx.date)}</p>
                  </div>
                  <p className={`font-semibold ${tx.type === 'income' ? 'text-status-success' : 'text-text-primary'}`}>
                    {tx.type === 'income' ? '+' : '-'}{formatCurrency(tx.amount)}
                  </p>
                </div>
              ))}
            </div>
          ) : (
            <EmptyState title="No transactions" description="No recent transactions recorded." />
          )}
        </Card>

        <Card>
          <div className="flex justify-between items-center mb-4">
            <h3 className="font-semibold text-text-primary">{t('dashboard.alerts')}</h3>
            <button
              onClick={() => navigate('/user/notifications')}
              className="text-xs font-semibold text-brand-700 hover:underline"
            >
              {t('dashboard.viewAll')}
            </button>
          </div>
          {notifications?.items && notifications.items.length > 0 ? (
            <div className="space-y-3">
              {notifications.items.slice(0, 4).map((notif) => (
                <div key={notif.id} className="text-sm p-2 rounded-lg bg-bg-page border border-border">
                  <div className="flex items-center gap-2 mb-1">
                    <Badge variant={notif.type as any}>{notif.type}</Badge>
                    <span className="text-xs text-text-muted">{formatDate(notif.created_at)}</span>
                  </div>
                  <p className="text-text-secondary text-xs">{notif.message}</p>
                </div>
              ))}
            </div>
          ) : (
            <EmptyState title="No alerts" description="Everything looks clean! No pending notifications." />
          )}
        </Card>
      </div>
    </AppLayout>
  )
}

export default UserDashboard
