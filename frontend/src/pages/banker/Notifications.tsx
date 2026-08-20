import React from 'react'
import { useTranslation } from 'react-i18next'
import AppLayout from '@/layouts/AppLayout'
import { useNotifications } from '@/hooks'
import { formatDate } from '@/utils'
import { PageHeader, Loading, Card, Badge, EmptyState } from '@/components'

const BankerNotifications: React.FC = () => {
  const { t } = useTranslation()
  const { data: notifications, isLoading } = useNotifications()

  const navItems = [
    { label: t('nav.bankerDashboard'), href: '/banker', icon: '📊' },
    { label: t('nav.notifications'), href: '/banker/notifications', icon: '🔔' },
  ]

  if (isLoading) return <AppLayout navItems={navItems}><Loading /></AppLayout>

  return (
    <AppLayout navItems={navItems}>
      <PageHeader title={t('nav.notifications')} />

      {notifications?.items && notifications.items.length > 0 ? (
        <div className="space-y-4">
          {notifications.items.map((notif) => (
            <Card key={notif.id}>
              <div className="flex justify-between items-start">
                <div>
                  <div className="flex items-center gap-2 mb-2">
                    <Badge variant={notif.type as any}>{notif.type}</Badge>
                    <p className="text-xs text-text-muted">{formatDate(notif.created_at)}</p>
                  </div>
                  <p className="font-medium text-text-primary">{notif.message}</p>
                </div>
              </div>
            </Card>
          ))}
        </div>
      ) : (
        <EmptyState title={t('common.noData')} />
      )}
    </AppLayout>
  )
}

export default BankerNotifications
