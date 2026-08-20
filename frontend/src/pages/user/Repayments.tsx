import React, { useState } from 'react'
import { useTranslation } from 'react-i18next'
import AppLayout from '@/layouts/AppLayout'
import { useRepaymentSchedule } from '@/hooks'
import { formatCurrency, formatDate } from '@/utils'
import { PageHeader, Loading, Card, Table, Pagination, Badge, EmptyState } from '@/components'

const UserRepayments: React.FC = () => {
  const { t } = useTranslation()
  const [page, setPage] = useState(1)
  const { data: repayments, isLoading } = useRepaymentSchedule((page - 1) * 20, 20)

  const navItems = [
    { label: t('nav.home'), href: '/user', icon: '🏠' },
    { label: t('nav.repayment'), href: '/user/repayment', icon: '📅' },
  ]

  const columns = [
    { key: 'id', label: 'ID', width: '15%' },
    { key: 'amount', label: t('repayment.amount'), width: '20%' },
    { key: 'due_date', label: t('repayment.dueDate'), width: '20%' },
    { key: 'status', label: t('repayment.status'), width: '20%' },
    { key: 'paid_date', label: 'Paid Date', width: '25%' },
  ]

  const statusVariant = (status: string) => {
    if (['paid', 'upcoming'].includes(status)) return 'success'
    if (['pending', 'overdue'].includes(status)) return 'warning'
    return 'danger'
  }

  const rows = repayments?.items?.map((rep) => ({
    ...rep,
    amount: formatCurrency(rep.amount),
    due_date: formatDate(rep.due_date),
    paid_date: rep.paid_date ? formatDate(rep.paid_date) : '-',
    status: <Badge variant={statusVariant(rep.status)}>{rep.status}</Badge>,
  })) || []

  if (isLoading) return <AppLayout navItems={navItems}><Loading /></AppLayout>

  return (
    <AppLayout navItems={navItems}>
      <PageHeader title={t('nav.repayment')} />

      {rows.length > 0 ? (
        <>
          <Card className="mb-6 overflow-hidden">
            <Table columns={columns} rows={rows} rowKey="id" />
          </Card>
          <Pagination
            currentPage={page}
            totalPages={Math.ceil((repayments?.total || 0) / 20)}
            onPageChange={setPage}
          />
        </>
      ) : (
        <EmptyState title={t('repayment.repayments')} />
      )}
    </AppLayout>
  )
}

export default UserRepayments
