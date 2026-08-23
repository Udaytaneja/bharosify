import React from 'react'
import { useTranslation } from 'react-i18next'
import AppLayout from '@/layouts/AppLayout'
import { useNotifications } from '@/hooks'
import { notificationApi } from '@/api'
import { formatDate } from '@/utils'
import { PageHeader, Loading, Card, Badge, EmptyState, Button } from '@/components'
import { useQueryClient } from '@tanstack/react-query'

const UserNotifications: React.FC = () => {
  const { t } = useTranslation()
  const queryClient = useQueryClient()
  const { data: notifications, isLoading } = useNotifications()

  const handleMarkAsRead = async (id: string) => {
    try {
      await notificationApi.markAsRead(id)
      queryClient.invalidateQueries({ queryKey: ['notifications'] })
    } catch (e) {
      console.error(e)
    }
  }

  const badgeVariant = (type: string) => {
    switch (type) {
      case 'success':
        return 'success'
      case 'warning':
      case 'action_required':
        return 'warning'
      default:
        return 'info'
    }
  }

  if (isLoading) {
    return (
      <AppLayout>
        <Loading />
      </AppLayout>
    )
  }

  return (
    <AppLayout>
      <PageHeader
        title={t('nav.notifications')}
        subtitle="Stay updated with loan approvals, repayment reminders, and trust alerts"
      />

      {notifications?.items && notifications.items.length > 0 ? (
        <div className="space-y-4 max-w-4xl">
          {notifications.items.map((notif) => (
            <Card
              key={notif.id}
              className={`transition-all ${
                notif.status === 'unread' ? 'border-l-4 border-l-brand-700 bg-brand-50/20' : ''
              }`}
            >
              <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4">
                <div className="flex-1">
                  <div className="flex items-center gap-2 mb-1.5">
                    <Badge variant={badgeVariant(notif.type)}>{notif.type.replace('_', ' ')}</Badge>
                    {notif.status === 'unread' && (
                      <span className="text-xs font-bold text-brand-700 bg-brand-100 px-2 py-0.5 rounded">
                        New
                      </span>
                    )}
                    <span className="text-xs text-text-muted">{formatDate(notif.created_at)}</span>
                  </div>
                  {notif.title && <h4 className="font-semibold text-text-primary text-sm mb-1">{notif.title}</h4>}
                  <p className="text-sm text-text-secondary">{notif.message}</p>
                </div>

                {notif.status === 'unread' && (
                  <Button
                    variant="secondary"
                    size="sm"
                    onClick={() => handleMarkAsRead(notif.id)}
                  >
                    Mark Read
                  </Button>
                )}
              </div>
            </Card>
          ))}
        </div>
      ) : (
        <EmptyState
          title="No Notifications"
          description="You are all caught up! No active notifications or alerts."
        />
      )}
    </AppLayout>
  )
}

export default UserNotifications
