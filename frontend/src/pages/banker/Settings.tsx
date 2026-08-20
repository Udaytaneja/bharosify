import React from 'react'
import { useTranslation } from 'react-i18next'
import AppLayout from '@/layouts/AppLayout'
import { useAuth } from '@/hooks'
import { PageHeader, Card, Input, Button } from '@/components'

const BankerSettings: React.FC = () => {
  const { t } = useTranslation()
  const { user } = useAuth()

  const navItems = [
    { label: t('nav.bankerDashboard'), href: '/banker', icon: '📊' },
    { label: t('nav.settings'), href: '/banker/settings', icon: '⚙️' },
  ]

  return (
    <AppLayout navItems={navItems}>
      <PageHeader title={t('nav.settings')} />

      <Card>
        <h2 className="text-lg font-semibold text-text-primary mb-6">Account Information</h2>

        <div className="space-y-4">
          <Input
            label="Name"
            value={user?.name || ''}
            disabled
          />

          <Input
            label="Email"
            value={user?.email || ''}
            disabled
          />

          <Input
            label="Role"
            value={user?.role || ''}
            disabled
          />

          <Button variant="secondary" disabled>
            {t('common.noData')}
          </Button>
        </div>
      </Card>
    </AppLayout>
  )
}

export default BankerSettings
