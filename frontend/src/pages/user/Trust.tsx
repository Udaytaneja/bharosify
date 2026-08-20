import React from 'react'
import { useTranslation } from 'react-i18next'
import AppLayout from '@/layouts/AppLayout'
import { useTrustProfile } from '@/hooks'
import { PageHeader, Loading, Card, TrustScore, EmptyState } from '@/components'

const UserTrust: React.FC = () => {
  const { t } = useTranslation()
  const { data: trust, isLoading } = useTrustProfile()

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

  if (isLoading) return <AppLayout navItems={navItems}><Loading /></AppLayout>
  if (!trust) return <AppLayout navItems={navItems}><EmptyState title="No trust data" /></AppLayout>

  return (
    <AppLayout navItems={navItems}>
      <PageHeader title={t('nav.trust')} />

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6 mb-8">
        <Card>
          <div className="text-center">
            <TrustScore score={trust.score} level={trust.level} size="md" />
            <p className="text-text-muted text-sm mt-4">Change: {trust.change > 0 ? '+' : ''}{trust.change}</p>
          </div>
        </Card>

        <Card className="lg:col-span-2">
          <h3 className="font-semibold text-text-primary mb-4">Positive Factors</h3>
          {trust.factors
            ?.filter((f) => f.impact > 0)
            .map((factor, i) => (
              <div key={i} className="mb-3">
                <div className="flex justify-between items-center">
                  <p className="font-medium text-text-primary">{factor.name}</p>
                  <span className="text-status-success">+{factor.impact}</span>
                </div>
                <p className="text-text-muted text-sm">{factor.description}</p>
              </div>
            ))}
        </Card>
      </div>

      <Card>
        <h3 className="font-semibold text-text-primary mb-4">Areas for Improvement</h3>
        {trust.factors
          ?.filter((f) => f.impact < 0)
          .map((factor, i) => (
            <div key={i} className="mb-3">
              <div className="flex justify-between items-center">
                <p className="font-medium text-text-primary">{factor.name}</p>
                <span className="text-status-danger">{factor.impact}</span>
              </div>
              <p className="text-text-muted text-sm">{factor.description}</p>
            </div>
          ))}
      </Card>
    </AppLayout>
  )
}

export default UserTrust
