import React from 'react'
import { useTranslation } from 'react-i18next'
import { useNavigate } from 'react-router-dom'
import AppLayout from '@/layouts/AppLayout'
import { useApplications, useLoans } from '@/hooks'
import { bankerApi } from '@/api'
import { useQuery } from '@tanstack/react-query'
import { formatCurrency, formatDate } from '@/utils'
import { PageHeader, Loading, Card, EmptyState, MetricCard, Button, Badge } from '@/components'

const BankerDashboard: React.FC = () => {
  const { t } = useTranslation()
  const navigate = useNavigate()

  const { data: applications, isLoading: appsLoading } = useApplications(0, 50)
  const { data: loans, isLoading: loansLoading } = useLoans(0, 50)
  const { data: customers, isLoading: customersLoading } = useQuery({
    queryKey: ['banker', 'customers', 'dashboard'],
    queryFn: () => bankerApi.getCustomers(0, 50),
  })

  const pendingApps = applications?.items?.filter(
    (app) => ['submitted', 'under_review', 'underwriting', 'documents_required'].includes(app.status)
  ) || []

  const activeLoans = loans?.items?.filter((l) => l.status === 'active') || []
  const totalCustomers = customers?.items?.length || 0

  if (appsLoading || loansLoading || customersLoading) {
    return (
      <AppLayout>
        <Loading />
      </AppLayout>
    )
  }

  return (
    <AppLayout>
      <PageHeader
        title={t('nav.bankerDashboard')}
        subtitle="Overview of customer applications, loan portfolio, underwriting queues & risk monitoring"
      />

      {/* Metrics */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
        <MetricCard label="Pending Applications" value={pendingApps.length.toString()} icon="📋" />
        <MetricCard label="Active Loan Facilities" value={activeLoans.length.toString()} icon="💰" />
        <MetricCard label="Total Customer Accounts" value={totalCustomers.toString()} icon="👥" />
        <MetricCard label="Underwriting Queue" value={pendingApps.filter(a => a.status === 'underwriting').length.toString()} icon="🔍" />
      </div>

      {/* Quick Action Navigation */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
        <Card className="hover:border-brand-500 transition-colors cursor-pointer" onClick={() => navigate('/banker/underwriting')}>
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 rounded-lg bg-brand-100 text-brand-700 flex items-center justify-center text-xl font-bold">
              🔍
            </div>
            <div>
              <h3 className="font-semibold text-text-primary">AI Underwriting Engine</h3>
              <p className="text-xs text-text-muted">Evaluate applications with automated risk scoring.</p>
            </div>
          </div>
        </Card>

        <Card className="hover:border-brand-500 transition-colors cursor-pointer" onClick={() => navigate('/banker/customers')}>
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 rounded-lg bg-brand-100 text-brand-700 flex items-center justify-center text-xl font-bold">
              👥
            </div>
            <div>
              <h3 className="font-semibold text-text-primary">Customer Directory</h3>
              <p className="text-xs text-text-muted">Inspect trust scores & financial profiles.</p>
            </div>
          </div>
        </Card>

        <Card className="hover:border-brand-500 transition-colors cursor-pointer" onClick={() => navigate('/banker/risk')}>
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 rounded-lg bg-brand-100 text-brand-700 flex items-center justify-center text-xl font-bold">
              ⚠️
            </div>
            <div>
              <h3 className="font-semibold text-text-primary">Risk Analytics</h3>
              <p className="text-xs text-text-muted">Run portfolio risk assessments and stress tests.</p>
            </div>
          </div>
        </Card>
      </div>

      {/* Pending Applications List */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <Card>
          <div className="flex justify-between items-center mb-4">
            <h2 className="text-lg font-semibold text-text-primary">
              Applications Requiring Attention ({pendingApps.length})
            </h2>
            <Button variant="secondary" size="sm" onClick={() => navigate('/banker/applications')}>
              View All
            </Button>
          </div>

          {pendingApps.length > 0 ? (
            <div className="space-y-3">
              {pendingApps.slice(0, 5).map((app) => (
                <div key={app.id} className="p-3 bg-bg-page rounded-lg border border-border flex justify-between items-center">
                  <div>
                    <div className="flex items-center gap-2 mb-1">
                      <span className="font-semibold text-text-primary text-sm">App #{app.id}</span>
                      <Badge variant="info">{app.status.replace('_', ' ')}</Badge>
                    </div>
                    <p className="text-xs text-text-muted">Customer: {app.customer_id} • {formatDate(app.created_at)}</p>
                  </div>
                  <div className="text-right">
                    <p className="font-bold text-brand-700 text-sm mb-1">{formatCurrency(app.amount)}</p>
                    <Button variant="primary" size="sm" onClick={() => navigate('/banker/applications')}>
                      Review
                    </Button>
                  </div>
                </div>
              ))}
            </div>
          ) : (
            <EmptyState title="No pending applications" description="All loan applications have been reviewed." />
          )}
        </Card>

        <Card>
          <div className="flex justify-between items-center mb-4">
            <h2 className="text-lg font-semibold text-text-primary">
              Recent Customer Registrations
            </h2>
            <Button variant="secondary" size="sm" onClick={() => navigate('/banker/customers')}>
              View Directory
            </Button>
          </div>

          {customers?.items && customers.items.length > 0 ? (
            <div className="space-y-3">
              {customers.items.slice(0, 5).map((c) => (
                <div key={c.id} className="p-3 bg-bg-page rounded-lg border border-border flex justify-between items-center">
                  <div>
                    <p className="font-semibold text-text-primary text-sm">{c.name}</p>
                    <p className="text-xs text-text-muted">{c.email}</p>
                  </div>
                  <div>
                    <Badge variant={c.account_status === 'active' ? 'success' : 'default'}>
                      {c.account_status}
                    </Badge>
                  </div>
                </div>
              ))}
            </div>
          ) : (
            <EmptyState title="No active customers" description="No customer accounts registered." />
          )}
        </Card>
      </div>
    </AppLayout>
  )
}

export default BankerDashboard
