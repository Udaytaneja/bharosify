import React, { useState } from 'react'
import { useTranslation } from 'react-i18next'
import AppLayout from '@/layouts/AppLayout'
import { useLoans } from '@/hooks'
import { formatCurrency } from '@/utils'
import { PageHeader, Loading, Card, Table, Pagination, Badge, EmptyState } from '@/components'

const BankerLoans: React.FC = () => {
  const { t } = useTranslation()
  const [page, setPage] = useState(1)
  const { data: loans, isLoading } = useLoans((page - 1) * 20, 20)

  const navItems = [
    { label: t('nav.bankerDashboard'), href: '/banker', icon: '📊' },
    { label: t('nav.loans'), href: '/banker/loans', icon: '💰' },
  ]

  const columns = [
    { key: 'id', label: 'ID', width: '15%' },
    { key: 'principal', label: 'Principal', width: '20%' },
    { key: 'outstanding_amount', label: 'Outstanding', width: '20%' },
    { key: 'status', label: 'Status', width: '20%' },
    { key: 'interest_rate', label: 'Rate', width: '25%' },
  ]

  const rows = loans?.items?.map((loan) => ({
    ...loan,
    principal: formatCurrency(loan.principal),
    outstanding_amount: formatCurrency(loan.outstanding_amount),
    interest_rate: `${(loan.interest_rate * 100).toFixed(2)}%`,
    status: <Badge>{loan.status}</Badge>,
  })) || []

  if (isLoading) return <AppLayout navItems={navItems}><Loading /></AppLayout>

  return (
    <AppLayout navItems={navItems}>
      <PageHeader title={t('nav.loans')} />

      {rows.length > 0 ? (
        <>
          <Card className="mb-6 overflow-hidden">
            <Table columns={columns} rows={rows} rowKey="id" />
          </Card>
          <Pagination
            currentPage={page}
            totalPages={Math.ceil((loans?.total || 0) / 20)}
            onPageChange={setPage}
          />
        </>
      ) : (
        <EmptyState title="No loans" />
      )}
    </AppLayout>
  )
}

export default BankerLoans
