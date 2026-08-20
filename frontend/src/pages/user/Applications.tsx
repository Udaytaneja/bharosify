import React, { useState } from 'react'
import { useTranslation } from 'react-i18next'
import AppLayout from '@/layouts/AppLayout'
import { useApplications } from '@/hooks'
import { formatCurrency, formatDate } from '@/utils'
import { PageHeader, Loading, Card, Table, Pagination, Badge, EmptyState } from '@/components'

const UserApplications: React.FC = () => {
  const { t } = useTranslation()
  const [page, setPage] = useState(1)
  const { data: applications, isLoading } = useApplications((page - 1) * 20, 20)

  const navItems = [
    { label: t('nav.home'), href: '/user', icon: '🏠' },
    { label: t('nav.applications'), href: '/user/applications', icon: '📋' },
  ]

  const columns = [
    { key: 'id', label: 'ID', width: '15%' },
    { key: 'amount', label: t('applications.amount'), width: '15%' },
    { key: 'purpose', label: t('applications.purpose'), width: '25%' },
    { key: 'status', label: t('applications.status'), width: '20%' },
    { key: 'created_at', label: t('applications.createdOn'), width: '25%' },
  ]

  const rows = applications?.items?.map((app) => ({
    ...app,
    amount: formatCurrency(app.amount),
    created_at: formatDate(app.created_at),
    status: <Badge variant={app.status === 'approved' ? 'success' : 'default'}>{app.status}</Badge>,
  })) || []

  if (isLoading) return <AppLayout navItems={navItems}><Loading /></AppLayout>

  return (
    <AppLayout navItems={navItems}>
      <PageHeader title={t('nav.applications')} />

      {rows.length > 0 ? (
        <>
          <Card className="mb-6 overflow-hidden">
            <Table columns={columns} rows={rows} rowKey="id" emptyMessage={t('applications.applications')} />
          </Card>
          <Pagination
            currentPage={page}
            totalPages={Math.ceil((applications?.total || 0) / 20)}
            onPageChange={setPage}
          />
        </>
      ) : (
        <EmptyState title={t('applications.applications')} />
      )}
    </AppLayout>
  )
}

export default UserApplications
