import React, { useState } from 'react'
import { useTranslation } from 'react-i18next'
import AppLayout from '@/layouts/AppLayout'
import { useLoans } from '@/hooks'
import { formatCurrency, formatDate } from '@/utils'
import { PageHeader, Loading, Card, Table, Pagination, Badge, EmptyState } from '@/components'

const UserLoans: React.FC = () => {
  const { t } = useTranslation()
  const [page, setPage] = useState(1)
  const { data: loans, isLoading } = useLoans((page - 1) * 20, 20)

  const navItems = [
    { label: t('nav.home'), href: '/user', icon: '🏠' },
    { label: t('nav.loans'), href: '/user/loans', icon: '💰' },
  ]

  const columns = [
    { key: 'id', label: 'ID', width: '15%' },
    { key: 'principal', label: t('loans.principal'), width: '15%' },
    { key: 'outstanding_amount', label: t('loans.outstanding'), width: '15%' },
    { key: 'interest_rate', label: t('loans.interestRate'), width: '15%' },
    { key: 'status', label: t('loans.status'), width: '20%' },
    { key: 'maturity_date', label: 'Maturity', width: '20%' },
  ]

  const rows = loans?.items?.map((loan) => ({
    ...loan,
    principal: formatCurrency(loan.principal),
    outstanding_amount: formatCurrency(loan.outstanding_amount),
    interest_rate: `${(loan.interest_rate * 100).toFixed(2)}%`,
    status: <Badge variant={loan.status === 'active' ? 'info' : 'default'}>{loan.status}</Badge>,
    maturity_date: formatDate(loan.maturity_date),
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
        <EmptyState title={t('loans.loans')} />
      )}
    </AppLayout>
  )
}

export default UserLoans
