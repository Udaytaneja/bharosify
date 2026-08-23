import React, { useState } from 'react'
import { useTranslation } from 'react-i18next'
import AppLayout from '@/layouts/AppLayout'
import { useRepaymentSchedule, useCreatePayment, useConfirmPayment } from '@/hooks'
import { formatCurrency, formatDate } from '@/utils'
import { 
  PageHeader, 
  Loading, 
  Card, 
  Table, 
  Pagination, 
  Badge, 
  EmptyState, 
  Button, 
  ConfirmationDialog, 
  Alert,
  MetricCard 
} from '@/components'
import { Repayment } from '@/types'

const UserRepayments: React.FC = () => {
  const { t } = useTranslation()
  const [page, setPage] = useState(1)
  const [selectedRepayment, setSelectedRepayment] = useState<Repayment | null>(null)
  const [paymentStatus, setPaymentStatus] = useState<{ type: 'success' | 'danger'; message: string } | null>(null)

  const { data: repayments, isLoading } = useRepaymentSchedule((page - 1) * 20, 20)
  const createPaymentMutation = useCreatePayment()
  const confirmPaymentMutation = useConfirmPayment()

  const isProcessing = createPaymentMutation.isPending || confirmPaymentMutation.isPending

  const handleMakePayment = async () => {
    if (!selectedRepayment || isProcessing) return

    setPaymentStatus(null)
    const ref = `PAY_${Date.now()}_${Math.random().toString(36).substring(2, 6).toUpperCase()}`
    const idempotencyKey = `IDEM_${Date.now()}_${Math.random().toString(36).substring(2, 6).toUpperCase()}`

    try {
      // Step 1: Create pending payment
      const paymentResponse = await createPaymentMutation.mutateAsync({
        amount: selectedRepayment.amount,
        payment_reference: ref,
        idempotency_key: idempotencyKey,
        repayment_id: parseInt(selectedRepayment.id) || undefined,
      })

      // Step 2: Confirm payment
      await confirmPaymentMutation.mutateAsync(paymentResponse.id)

      setPaymentStatus({
        type: 'success',
        message: `${t('repayment.paymentSuccess')}! Reference: ${ref}`,
      })
      setSelectedRepayment(null)
    } catch (err: any) {
      setPaymentStatus({
        type: 'danger',
        message: err.response?.data?.detail || err.message || t('repayment.paymentFailed'),
      })
      setSelectedRepayment(null)
    }
  }

  const statusVariant = (status: string) => {
    switch (status) {
      case 'paid':
        return 'success'
      case 'upcoming':
        return 'info'
      case 'pending':
      case 'partially_paid':
        return 'warning'
      case 'overdue':
      case 'failed':
        return 'danger'
      default:
        return 'default'
    }
  }

  const upcomingRepayments = repayments?.items?.filter((r) => r.status !== 'paid') || []
  const nextPayment = upcomingRepayments[0]

  const columns = [
    { key: 'id', label: 'ID', width: '15%' },
    { key: 'amount', label: t('repayment.amount'), width: '20%' },
    { key: 'due_date', label: t('repayment.dueDate'), width: '20%' },
    { key: 'status', label: t('repayment.status'), width: '20%' },
    { key: 'paid_date', label: 'Paid Date', width: '15%' },
    { key: 'actions', label: 'Actions', width: '10%' },
  ]

  const rows = repayments?.items?.map((rep) => ({
    ...rep,
    amount: <span className="font-semibold text-text-primary">{formatCurrency(rep.amount)}</span>,
    due_date: formatDate(rep.due_date),
    paid_date: rep.paid_date ? formatDate(rep.paid_date) : '-',
    status: <Badge variant={statusVariant(rep.status)}>{rep.status}</Badge>,
    actions: rep.status !== 'paid' ? (
      <Button
        variant="primary"
        size="sm"
        disabled={isProcessing}
        onClick={() => setSelectedRepayment(rep)}
      >
        {t('repayment.makePayment')}
      </Button>
    ) : (
      <span className="text-xs text-status-success font-medium">✓ Paid</span>
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
      <PageHeader
        title={t('nav.repayment')}
        subtitle="Manage upcoming loan payments and view payment history"
      />

      {paymentStatus && (
        <div className="mb-6">
          <Alert type={paymentStatus.type} message={paymentStatus.message} />
        </div>
      )}

      {nextPayment && (
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
          <MetricCard
            label={t('repayment.nextPayment')}
            value={formatCurrency(nextPayment.amount)}
            icon="📅"
          />
          <MetricCard
            label={t('repayment.dueDate')}
            value={formatDate(nextPayment.due_date)}
            icon="⏰"
          />
          <Card className="flex flex-col justify-center items-center">
            <p className="text-xs text-text-muted mb-2">Quick Action</p>
            <Button
              variant="primary"
              disabled={isProcessing}
              onClick={() => setSelectedRepayment(nextPayment)}
            >
              💳 {t('repayment.makePayment')}
            </Button>
          </Card>
        </div>
      )}

      {rows.length > 0 ? (
        <>
          <Card className="mb-6 overflow-hidden">
            <Table columns={columns} rows={rows} rowKey="id" />
          </Card>
          <Pagination
            currentPage={page}
            totalPages={Math.max(1, Math.ceil((repayments?.total || 0) / 20))}
            onPageChange={setPage}
          />
        </>
      ) : (
        <EmptyState
          title={t('repayment.repayments')}
          description="No repayment schedule found for your active loans."
        />
      )}

      {/* Confirmation Dialog */}
      <ConfirmationDialog
        isOpen={!!selectedRepayment}
        onClose={() => setSelectedRepayment(null)}
        onConfirm={handleMakePayment}
        title={t('repayment.paymentConfirm')}
        message={`Are you sure you want to process a payment of ${
          selectedRepayment ? formatCurrency(selectedRepayment.amount) : ''
        } for repayment #${selectedRepayment?.id}?`}
        confirmLabel={t('repayment.makePayment')}
        cancelLabel={t('common.cancel')}
        isLoading={isProcessing}
      />
    </AppLayout>
  )
}

export default UserRepayments
