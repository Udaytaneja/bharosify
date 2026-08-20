import React, { useState } from 'react'
import { useTranslation } from 'react-i18next'
import AppLayout from '@/layouts/AppLayout'
import { useTransactions } from '@/hooks'
import { formatCurrency, formatDate } from '@/utils'
import { PageHeader, Loading, Card, Table, Pagination, Input, EmptyState } from '@/components'

const UserTransactions: React.FC = () => {
  const { t } = useTranslation()
  const [page, setPage] = useState(1)
  const [search, setSearch] = useState('')
  const { data: transactions, isLoading } = useTransactions((page - 1) * 20, 20)

  const navItems = [
    { label: t('nav.home'), href: '/user', icon: '🏠' },
    { label: t('nav.transactions'), href: '/user/transactions', icon: '💳' },
  ]

  const columns = [
    { key: 'merchant', label: t('transactions.merchant'), width: '25%' },
    { key: 'category', label: t('transactions.category'), width: '20%' },
    { key: 'amount', label: t('transactions.amount'), width: '20%' },
    { key: 'type', label: t('transactions.type'), width: '15%' },
    { key: 'date', label: t('transactions.date'), width: '20%' },
  ]

  const rows = transactions?.items?.map((tx) => ({
    ...tx,
    amount: formatCurrency(tx.amount),
    date: formatDate(tx.date),
  })) || []

  if (isLoading) return <AppLayout navItems={navItems}><Loading /></AppLayout>

  return (
    <AppLayout navItems={navItems}>
      <PageHeader title={t('nav.transactions')} />

      <Card className="mb-6">
        <Input
          placeholder={t('transactions.search')}
          value={search}
          onChange={(e) => setSearch(e.target.value)}
        />
      </Card>

      {rows.length > 0 ? (
        <>
          <Card className="mb-6 overflow-hidden">
            <Table
              columns={columns}
              rows={rows}
              rowKey="id"
              isLoading={isLoading}
              emptyMessage={t('transactions.noTransactions')}
            />
          </Card>
          <Pagination
            currentPage={page}
            totalPages={Math.ceil((transactions?.total || 0) / 20)}
            onPageChange={setPage}
          />
        </>
      ) : (
        <EmptyState title={t('transactions.noTransactions')} />
      )}
    </AppLayout>
  )
}

export default UserTransactions
