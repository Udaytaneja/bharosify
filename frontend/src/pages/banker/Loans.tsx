import React, { useState } from 'react'
import { useTranslation } from 'react-i18next'
import AppLayout from '@/layouts/AppLayout'
import { useLoans } from '@/hooks'
import { formatCurrency, formatDate } from '@/utils'
import { PageHeader, Loading, Card, Table, Pagination, Badge, EmptyState, MetricCard, Button, Modal } from '@/components'
import { Loan } from '@/types'

const BankerLoans: React.FC = () => {
  const { t } = useTranslation()
  const [page, setPage] = useState(1)
  const [selectedLoan, setSelectedLoan] = useState<Loan | null>(null)
  const { data: loans, isLoading } = useLoans((page - 1) * 20, 20)

  const totalPrincipal = loans?.items?.reduce((sum, l) => sum + (l.principal || 0), 0) || 0
  const totalOutstanding = loans?.items?.reduce((sum, l) => sum + (l.outstanding_amount || 0), 0) || 0

  const statusVariant = (status: string) => {
    switch (status) {
      case 'active':
        return 'info'
      case 'completed':
        return 'success'
      case 'defaulted':
        return 'danger'
      default:
        return 'default'
    }
  }

  const columns = [
    { key: 'id', label: 'Loan ID', width: '15%' },
    { key: 'customer_id', label: 'Customer ID', width: '15%' },
    { key: 'principal', label: 'Principal', width: '20%' },
    { key: 'outstanding_amount', label: 'Outstanding', width: '20%' },
    { key: 'status', label: 'Status', width: '15%' },
    { key: 'actions', label: 'Actions', width: '15%' },
  ]

  const rows = loans?.items?.map((loan) => ({
    ...loan,
    principal: <span className="font-semibold text-text-primary">{formatCurrency(loan.principal)}</span>,
    outstanding_amount: <span className="font-semibold text-brand-700">{formatCurrency(loan.outstanding_amount)}</span>,
    status: <Badge variant={statusVariant(loan.status)}>{loan.status}</Badge>,
    actions: (
      <Button variant="secondary" size="sm" onClick={() => setSelectedLoan(loan)}>
        Inspect
      </Button>
    ),
  })) || []

  if (isLoading) {
    return (
      <AppLayout>
        <Loading />
      </AppLayout>
    )
  }

  return (
    <AppLayout>
      <PageHeader title={t('nav.loans')} subtitle="Monitor active loan portfolio & balances across all accounts" />

      {loans?.items && loans.items.length > 0 && (
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
          <MetricCard label="Total Portfolio Principal" value={formatCurrency(totalPrincipal)} icon="💰" />
          <MetricCard label="Total Outstanding Balance" value={formatCurrency(totalOutstanding)} icon="⚠️" />
          <MetricCard label="Active Loans Portfolio" value={loans.items.length.toString()} icon="📄" />
        </div>
      )}

      {rows.length > 0 ? (
        <>
          <Card className="mb-6 overflow-hidden">
            <Table columns={columns} rows={rows} rowKey="id" />
          </Card>
          <Pagination
            currentPage={page}
            totalPages={Math.max(1, Math.ceil((loans?.total || 0) / 20))}
            onPageChange={setPage}
          />
        </>
      ) : (
        <EmptyState title="No Loans Found" description="No active or historical loans exist in the system." />
      )}

      {/* Loan Inspection Modal */}
      {selectedLoan && (
        <Modal
          isOpen={!!selectedLoan}
          onClose={() => setSelectedLoan(null)}
          title={`Loan Facility #${selectedLoan.id}`}
        >
          <div className="space-y-4">
            <div className="grid grid-cols-2 gap-4 bg-bg-page p-4 rounded-lg border border-border">
              <div>
                <p className="text-xs text-text-muted">Customer ID</p>
                <p className="text-sm font-semibold text-text-primary">{selectedLoan.customer_id}</p>
              </div>
              <div>
                <p className="text-xs text-text-muted">Facility Status</p>
                <Badge variant={statusVariant(selectedLoan.status)}>{selectedLoan.status}</Badge>
              </div>
              <div>
                <p className="text-xs text-text-muted">Principal Disbursed</p>
                <p className="text-lg font-bold text-text-primary">{formatCurrency(selectedLoan.principal)}</p>
              </div>
              <div>
                <p className="text-xs text-text-muted">Outstanding Amount</p>
                <p className="text-lg font-bold text-brand-700">{formatCurrency(selectedLoan.outstanding_amount)}</p>
              </div>
              <div>
                <p className="text-xs text-text-muted">Interest Rate</p>
                <p className="text-sm font-semibold text-text-primary">{(selectedLoan.interest_rate * 100).toFixed(2)}% p.a.</p>
              </div>
              <div>
                <p className="text-xs text-text-muted">Tenure</p>
                <p className="text-sm font-semibold text-text-primary">{selectedLoan.duration} months</p>
              </div>
              <div>
                <p className="text-xs text-text-muted">Disbursal Date</p>
                <p className="text-sm text-text-primary">{formatDate(selectedLoan.start_date)}</p>
              </div>
              <div>
                <p className="text-xs text-text-muted">Maturity Date</p>
                <p className="text-sm text-text-primary">{formatDate(selectedLoan.maturity_date)}</p>
              </div>
            </div>

            <div className="flex justify-end pt-4 border-t border-border">
              <Button variant="secondary" onClick={() => setSelectedLoan(null)}>
                {t('common.close')}
              </Button>
            </div>
          </div>
        </Modal>
      )}
    </AppLayout>
  )
}

export default BankerLoans
