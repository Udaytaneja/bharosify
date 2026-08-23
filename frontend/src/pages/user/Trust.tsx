import React from 'react'
import { useTranslation } from 'react-i18next'
import AppLayout from '@/layouts/AppLayout'
import { useTrustProfile } from '@/hooks'
import { PageHeader, Loading, Card, TrustScore, EmptyState, Badge } from '@/components'

const UserTrust: React.FC = () => {
  const { t } = useTranslation()
  const { data: trust, isLoading } = useTrustProfile()

  if (isLoading) {
    return (
      <AppLayout>
        <Loading />
      </AppLayout>
    )
  }

  if (!trust) {
    return (
      <AppLayout>
        <EmptyState title="No Trust Profile Data" description="Your credit and trust score is currently being compiled." />
      </AppLayout>
    )
  }

  const positiveFactors = trust.factors?.filter((f) => f.impact > 0) || []
  const negativeFactors = trust.factors?.filter((f) => f.impact < 0) || []

  return (
    <AppLayout>
      <PageHeader
        title={t('nav.trust')}
        subtitle="Transparent evaluation of your financial trust rating and key drivers"
      />

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6 mb-8">
        <Card className="flex flex-col items-center justify-center p-6">
          <p className="text-text-muted text-xs uppercase tracking-wider mb-4">{t('trust.currentScore')}</p>
          <TrustScore score={trust.score} level={trust.level} size="lg" />
          <div className="mt-4 text-center">
            <p className="text-sm font-semibold text-text-secondary">
              Score Change: {' '}
              <span className={trust.change >= 0 ? 'text-status-success' : 'text-status-danger'}>
                {trust.change > 0 ? `+${trust.change}` : trust.change} pts
              </span>
            </p>
            <p className="text-xs text-text-muted mt-1">Updated {new Date(trust.updated_at).toLocaleDateString()}</p>
          </div>
        </Card>

        <Card className="lg:col-span-2">
          <h3 className="font-semibold text-text-primary mb-4 flex items-center gap-2">
            <span>✅</span> {t('trust.positiveFactors')}
          </h3>
          {positiveFactors.length > 0 ? (
            <div className="space-y-3">
              {positiveFactors.map((factor, i) => (
                <div key={i} className="p-3 bg-bg-page rounded-lg border border-border">
                  <div className="flex justify-between items-center mb-1">
                    <p className="font-semibold text-text-primary text-sm">{factor.name}</p>
                    <Badge variant="success">+{factor.impact} pts</Badge>
                  </div>
                  <p className="text-text-secondary text-xs">{factor.description}</p>
                </div>
              ))}
            </div>
          ) : (
            <p className="text-text-muted text-sm italic">No positive factors logged yet.</p>
          )}
        </Card>
      </div>

      <Card>
        <h3 className="font-semibold text-text-primary mb-4 flex items-center gap-2">
          <span>💡</span> {t('trust.negativeFactors')}
        </h3>
        {negativeFactors.length > 0 ? (
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            {negativeFactors.map((factor, i) => (
              <div key={i} className="p-3 bg-bg-page rounded-lg border border-border">
                <div className="flex justify-between items-center mb-1">
                  <p className="font-semibold text-text-primary text-sm">{factor.name}</p>
                  <Badge variant="danger">{factor.impact} pts</Badge>
                </div>
                <p className="text-text-secondary text-xs">{factor.description}</p>
              </div>
            ))}
          </div>
        ) : (
          <p className="text-text-muted text-sm italic">No negative risk factors identified.</p>
        )}
      </Card>
    </AppLayout>
  )
}

export default UserTrust
