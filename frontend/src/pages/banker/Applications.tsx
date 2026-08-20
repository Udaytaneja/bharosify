import React, { useState } from 'react'
import { useTranslation } from 'react-i18next'
import AppLayout from '@/layouts/AppLayout'
import { useApplications } from '@/hooks'
import { formatCurrency, formatDate } from '@/utils'
import { PageHeader, Loading, Card, Table, Pagination, Badge, EmptyState } from '@/components'

const BankerApplications: React.FC = () => {
  const { t } = useTranslation()
  const [page, setPage] = useState(1)
  const { data: applications, isLoading } = useApplications((page - 1) * 20, 20)

  const navItems = [
    { label: t('nav.bankerDashboard'), href: '/banker', icon: '📊' },
    { label: t('nav.applications'), href: '/banker/applications', icon: '📋' },
  ]

  const columns = [
    { key: 'id', label: 'ID', width: '15%' },
    { key: 'amount', label: 'Amount', width: '15%' },
    { key: 'purpose', label: 'Purpose', width: '25%' },
    { key: 'status', label: 'Status', width: '20%' },
    { key: 'created_at', label: 'Date', width: '25%' },
  ]

  const rows = applications?.items?.map((app) => ({
    ...app,
    amount: formatCurrency(app.amount),
    created_at: formatDate(app.created_at),
    status: <Badge>{app.status}</Badge>,
  })) || []

  if (isLoading) return <AppLayout navItems={navItems}><Loading /></AppLayout>

  return (
    <AppLayout navItems={navItems}>
      <PageHeader title={t('nav.applications')} />

      {rows.length > 0 ? (
        <>
          <Card className="mb-6 overflow-hidden">
            <Table columns={columns} rows={rows} rowKey="id" />
          </Card>
          <Pagination
            currentPage={page}
            totalPages={Math.ceil((applications?.total || 0) / 20)}
            onPageChange={setPage}
          />
        </>
      ) : (
        <EmptyState title="No applications" />
      )}
    </AppLayout>
  )
}

export default BankerApplications
