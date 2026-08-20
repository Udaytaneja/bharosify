import React, { useState } from 'react'
import { useTranslation } from 'react-i18next'
import AppLayout from '@/layouts/AppLayout'
import { bankerApi } from '@/api'
import { useQuery } from '@tanstack/react-query'
import { PageHeader, Loading, Card, Table, Pagination, EmptyState } from '@/components'

const BankerCustomers: React.FC = () => {
  const { t } = useTranslation()
  const [page, setPage] = useState(1)
  const { data: customers, isLoading } = useQuery({
    queryKey: ['customers', page],
    queryFn: () => bankerApi.getCustomers((page - 1) * 20, 20),
  })

  const navItems = [
    { label: t('nav.bankerDashboard'), href: '/banker', icon: '📊' },
    { label: t('nav.customers'), href: '/banker/customers', icon: '👥' },
  ]

  const columns = [
    { key: 'name', label: 'Name', width: '20%' },
    { key: 'email', label: 'Email', width: '25%' },
    { key: 'phone', label: 'Phone', width: '15%' },
    { key: 'account_status', label: 'Status', width: '20%' },
    { key: 'trust_score', label: 'Trust', width: '20%' },
  ]

  const rows = customers?.items?.map((c: any) => ({
    ...c,
    trust_score: c.trust_profile?.score || '-',
  })) || []

  if (isLoading) return <AppLayout navItems={navItems}><Loading /></AppLayout>

  return (
    <AppLayout navItems={navItems}>
      <PageHeader title={t('nav.customers')} />

      {rows.length > 0 ? (
        <>
          <Card className="mb-6 overflow-hidden">
            <Table columns={columns} rows={rows} rowKey="id" />
          </Card>
          <Pagination
            currentPage={page}
            totalPages={Math.ceil((customers?.total || 0) / 20)}
            onPageChange={setPage}
          />
        </>
      ) : (
        <EmptyState title="No customers" />
      )}
    </AppLayout>
  )
}

export default BankerCustomers
