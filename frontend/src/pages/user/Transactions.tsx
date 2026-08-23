import React, { useState, useMemo } from 'react'
import { useTranslation } from 'react-i18next'
import AppLayout from '@/layouts/AppLayout'
import { useTransactions } from '@/hooks'
import { formatCurrency, formatDate } from '@/utils'
import { PageHeader, Loading, Card, Table, Pagination, Input, Select, Badge, EmptyState } from '@/components'

const UserTransactions: React.FC = () => {
  const { t } = useTranslation()
  const [page, setPage] = useState(1)
  const [search, setSearch] = useState('')
  const [typeFilter, setTypeFilter] = useState<string>('all')
  const { data: transactions, isLoading } = useTransactions((page - 1) * 20, 20)

  const columns = [
    { key: 'merchant', label: t('transactions.merchant'), width: '25%' },
    { key: 'category', label: t('transactions.category'), width: '20%' },
    { key: 'amount', label: t('transactions.amount'), width: '20%' },
    { key: 'type', label: t('transactions.type'), width: '15%' },
    { key: 'date', label: t('transactions.date'), width: '20%' },
  ]

  const filteredItems = useMemo(() => {
    let items = transactions?.items || []
    if (search.trim()) {
      const q = search.toLowerCase()
      items = items.filter(
        (tx) =>
          tx.merchant?.toLowerCase().includes(q) ||
          tx.category?.toLowerCase().includes(q) ||
          tx.description?.toLowerCase().includes(q)
      )
    }
    if (typeFilter !== 'all') {
      items = items.filter((tx) => tx.type === typeFilter)
    }
    return items
  }, [transactions?.items, search, typeFilter])

  const rows = useMemo(() => {
    return filteredItems.map((tx) => ({
      ...tx,
      merchant: (
        <div>
          <p className="font-semibold text-text-primary">{tx.merchant}</p>
          {tx.description && <p className="text-xs text-text-muted">{tx.description}</p>}
        </div>
      ),
      amount: (
        <span className={`font-semibold ${tx.type === 'income' ? 'text-status-success' : 'text-text-primary'}`}>
          {tx.type === 'income' ? '+' : '-'} {formatCurrency(tx.amount)}
        </span>
      ),
      type: <Badge variant={tx.type === 'income' ? 'success' : tx.type === 'expense' ? 'default' : 'info'}>{tx.type}</Badge>,
      date: formatDate(tx.date),
    }))
  }, [filteredItems])

  if (isLoading) {
    return (
      <AppLayout>
        <Loading />
      </AppLayout>
    )
  }

  return (
    <AppLayout>
      <PageHeader title={t('nav.transactions')} subtitle="View and search your complete transaction history" />

      <Card className="mb-6">
        <div className="flex flex-col sm:flex-row gap-4 justify-between items-center">
          <div className="w-full sm:w-80">
            <Input
              placeholder={t('transactions.search')}
              value={search}
              onChange={(e) => setSearch(e.target.value)}
            />
          </div>
          <div className="w-full sm:w-48 flex items-center gap-2">
            <Select
              value={typeFilter}
              onChange={(e) => setTypeFilter(e.target.value)}
              options={[
                { value: 'all', label: 'All Types' },
                { value: 'income', label: t('transactions.income') },
                { value: 'expense', label: t('transactions.expense') },
                { value: 'transfer', label: t('transactions.transfer') },
              ]}
            />
          </div>
        </div>
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
            totalPages={Math.max(1, Math.ceil((transactions?.total || 0) / 20))}
            onPageChange={setPage}
          />
        </>
      ) : (
        <EmptyState title={t('transactions.noTransactions')} description="No matching financial transactions were found." />
      )}
    </AppLayout>
  )
}

export default UserTransactions
