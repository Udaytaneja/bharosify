import React, { useState } from 'react'
import { useTranslation } from 'react-i18next'
import AppLayout from '@/layouts/AppLayout'
import { useLoans } from '@/hooks'
import { formatCurrency, formatDate } from '@/utils'
import { PageHeader, Loading, Card, Table, Pagination, Badge, EmptyState, MetricCard, Button, Modal } from '@/components'
import { Loan } from '@/types'

const UserLoans: React.FC = () => {
  const { t } = useTranslation()
  const [page, setPage] = useState(1)
  const [selectedLoan, setSelectedLoan] = useState<Loan | null>(null)
  const { data: loans, isLoading } = useLoans((page - 1) * 20, 20)

  const columns = [
    { key: 'id', label: 'Loan ID', width: '15%' },
    { key: 'principal', label: t('loans.principal'), width: '20%' },
    { key: 'outstanding_amount', label: t('loans.outstanding'), width: '20%' },
    { key: 'interest_rate', label: t('loans.interestRate'), width: '15%' },
    { key: 'status', label: t('loans.status'), width: '15%' },
    { key: 'actions', label: 'Actions', width: '15%' },
  ]

  const totalPrincipal = loans?.items?.reduce((sum, l) => sum + (l.principal || 0), 0) || 0
  const totalOutstanding = loans?.items?.reduce((sum, l) => sum + (l.outstanding_amount || 0), 0) || 0
  const activeLoansCount = loans?.items?.filter((l) => l.status === 'active').length || 0

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

  const rows = loans?.items?.map((loan) => ({
    ...loan,
    principal: <span className="font-semibold text-text-primary">{formatCurrency(loan.principal)}</span>,
    outstanding_amount: (
      <span className="font-semibold text-brand-700">{formatCurrency(loan.outstanding_amount)}</span>
    ),
    interest_rate: `${(loan.interest_rate * 100).toFixed(2)}%`,
    status: <Badge variant={statusVariant(loan.status)}>{loan.status}</Badge>,
    actions: (
      <Button variant="secondary" size="sm" onClick={() => setSelectedLoan(loan)}>
        {t('applications.view')}
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
      <PageHeader title={t('nav.loans')} subtitle="Overview of your active and past loan facilities" />

      {loans?.items && loans.items.length > 0 && (
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
          <MetricCard label="Total Borrowed" value={formatCurrency(totalPrincipal)} icon="💰" />
          <MetricCard label="Total Outstanding" value={formatCurrency(totalOutstanding)} icon="⚠️" />
          <MetricCard label="Active Loans" value={activeLoansCount.toString()} icon="📄" />
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
        <EmptyState
          title="No Active Loans"
          description="You currently have no active or historical loans."
        />
      )}

      {/* Loan Details Modal */}
      {selectedLoan && (
        <Modal
          isOpen={!!selectedLoan}
          onClose={() => setSelectedLoan(null)}
          title={`Loan Details #${selectedLoan.id}`}
        >
          <div className="space-y-4">
            <div className="grid grid-cols-2 gap-4 bg-bg-page p-4 rounded-lg border border-border">
              <div>
                <p className="text-xs text-text-muted">Principal Amount</p>
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
                <p className="text-xs text-text-muted">Tenure / Duration</p>
                <p className="text-sm font-semibold text-text-primary">{selectedLoan.duration} months</p>
              </div>
              <div>
                <p className="text-xs text-text-muted">Start Date</p>
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

export default UserLoans
