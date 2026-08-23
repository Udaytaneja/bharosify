import React, { useState, useMemo } from 'react'
import { useTranslation } from 'react-i18next'
import AppLayout from '@/layouts/AppLayout'
import { bankerApi } from '@/api'
import { useQuery } from '@tanstack/react-query'
import { PageHeader, Loading, Card, Table, Pagination, EmptyState, Badge, Input, Button, Modal, TrustScore } from '@/components'
import { Customer } from '@/types'

const BankerCustomers: React.FC = () => {
  const { t } = useTranslation()
  const [page, setPage] = useState(1)
  const [search, setSearch] = useState('')
  const [selectedCustomer, setSelectedCustomer] = useState<Customer | null>(null)

  const { data: customers, isLoading } = useQuery({
    queryKey: ['banker', 'customers', page],
    queryFn: () => bankerApi.getCustomers((page - 1) * 20, 20),
  })

  const filteredCustomers = useMemo(() => {
    let items = customers?.items || []
    if (search.trim()) {
      const q = search.toLowerCase()
      items = items.filter(
        (c) =>
          c.name?.toLowerCase().includes(q) ||
          c.email?.toLowerCase().includes(q) ||
          c.phone?.includes(q)
      )
    }
    return items
  }, [customers?.items, search])

  const statusVariant = (status: string) => {
    switch (status) {
      case 'active':
        return 'success'
      case 'suspended':
      case 'blocked':
        return 'danger'
      default:
        return 'default'
    }
  }

  const columns = [
    { key: 'name', label: 'Customer Name', width: '20%' },
    { key: 'email', label: 'Email', width: '25%' },
    { key: 'phone', label: 'Phone', width: '15%' },
    { key: 'account_status', label: 'Account Status', width: '15%' },
    { key: 'trust_score', label: 'Trust Score', width: '15%' },
    { key: 'actions', label: 'Actions', width: '10%' },
  ]

  const rows = filteredCustomers.map((c) => ({
    ...c,
    name: <span className="font-semibold text-text-primary">{c.name}</span>,
    account_status: <Badge variant={statusVariant(c.account_status)}>{c.account_status}</Badge>,
    trust_score: c.trust_profile?.score !== undefined ? (
      <span className="font-bold text-brand-700">{c.trust_profile.score}</span>
    ) : (
      '-'
    ),
    actions: (
      <Button variant="secondary" size="sm" onClick={() => setSelectedCustomer(c)}>
        View
      </Button>
    ),
  }))

  if (isLoading) {
    return (
      <AppLayout>
        <Loading />
      </AppLayout>
    )
  }

  return (
    <AppLayout>
      <PageHeader title={t('nav.customers')} subtitle="Search and inspect customer profiles & risk scores" />

      <Card className="mb-6">
        <div className="w-full sm:w-80">
          <Input
            placeholder="Search by name, email or phone..."
            value={search}
            onChange={(e) => setSearch(e.target.value)}
          />
        </div>
      </Card>

      {rows.length > 0 ? (
        <>
          <Card className="mb-6 overflow-hidden">
            <Table columns={columns} rows={rows} rowKey="id" />
          </Card>
          <Pagination
            currentPage={page}
            totalPages={Math.max(1, Math.ceil((customers?.total || 0) / 20))}
            onPageChange={setPage}
          />
        </>
      ) : (
        <EmptyState title="No Customers Found" description="No customer accounts match your search query." />
      )}

      {/* Customer Detail Inspection Modal */}
      {selectedCustomer && (
        <Modal
          isOpen={!!selectedCustomer}
          onClose={() => setSelectedCustomer(null)}
          title={`Customer File: ${selectedCustomer.name}`}
        >
          <div className="space-y-6">
            <div className="grid grid-cols-2 gap-4 bg-bg-page p-4 rounded-lg border border-border">
              <div>
                <p className="text-xs text-text-muted">Customer ID</p>
                <p className="text-sm font-semibold text-text-primary">{selectedCustomer.id}</p>
              </div>
              <div>
                <p className="text-xs text-text-muted">Account Status</p>
                <Badge variant={statusVariant(selectedCustomer.account_status)}>
                  {selectedCustomer.account_status}
                </Badge>
              </div>
              <div>
                <p className="text-xs text-text-muted">Email Address</p>
                <p className="text-sm text-text-primary">{selectedCustomer.email}</p>
              </div>
              <div>
                <p className="text-xs text-text-muted">Phone Number</p>
                <p className="text-sm text-text-primary">{selectedCustomer.phone || '-'}</p>
              </div>
            </div>

            {selectedCustomer.trust_profile && (
              <Card className="flex flex-col items-center justify-center p-4 bg-brand-50/30">
                <p className="text-xs text-text-muted uppercase tracking-wider mb-2">Trust Profile</p>
                <TrustScore
                  score={selectedCustomer.trust_profile.score}
                  level={selectedCustomer.trust_profile.level}
                  size="md"
                />
              </Card>
            )}

            <div className="flex justify-end pt-4 border-t border-border">
              <Button variant="secondary" onClick={() => setSelectedCustomer(null)}>
                {t('common.close')}
              </Button>
            </div>
          </div>
        </Modal>
      )}
    </AppLayout>
  )
}

export default BankerCustomers
