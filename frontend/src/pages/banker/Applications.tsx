import React, { useState } from 'react'
import { useTranslation } from 'react-i18next'
import AppLayout from '@/layouts/AppLayout'
import { useApplications, useUpdateApplication } from '@/hooks'
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
  Modal, 
  ConfirmationDialog, 
  Alert 
} from '@/components'
import { LoanApplication } from '@/types'

const BankerApplications: React.FC = () => {
  const { t } = useTranslation()
  const [page, setPage] = useState(1)
  const [selectedApp, setSelectedApp] = useState<LoanApplication | null>(null)
  const [pendingAction, setPendingAction] = useState<{
    type: 'approved' | 'rejected' | 'documents_required'
    app: LoanApplication
  } | null>(null)
  const [feedback, setFeedback] = useState<{ type: 'success' | 'danger'; message: string } | null>(null)

  const { data: applications, isLoading } = useApplications((page - 1) * 20, 20)
  const updateMutation = useUpdateApplication()

  const handleDecision = async () => {
    if (!pendingAction) return
    setFeedback(null)

    try {
      await updateMutation.mutateAsync({
        id: pendingAction.app.id,
        data: { status: pendingAction.type },
      })
      setFeedback({
        type: 'success',
        message: `Application #${pendingAction.app.id} status updated to ${pendingAction.type.replace('_', ' ')}.`,
      })
      setPendingAction(null)
      setSelectedApp(null)
    } catch (err: any) {
      setFeedback({
        type: 'danger',
        message: err.response?.data?.detail || err.message || 'Failed to update application status',
      })
      setPendingAction(null)
    }
  }

  const statusVariant = (status: string) => {
    switch (status) {
      case 'approved':
      case 'completed':
        return 'success'
      case 'rejected':
        return 'danger'
      case 'underwriting':
      case 'under_review':
        return 'info'
      case 'documents_required':
        return 'warning'
      default:
        return 'default'
    }
  }

  const columns = [
    { key: 'id', label: 'App ID', width: '15%' },
    { key: 'customer_id', label: 'Customer ID', width: '15%' },
    { key: 'amount', label: 'Amount', width: '15%' },
    { key: 'purpose', label: 'Purpose', width: '25%' },
    { key: 'status', label: 'Status', width: '15%' },
    { key: 'actions', label: 'Actions', width: '15%' },
  ]

  const rows = applications?.items?.map((app) => ({
    ...app,
    amount: <span className="font-semibold text-text-primary">{formatCurrency(app.amount)}</span>,
    status: <Badge variant={statusVariant(app.status)}>{app.status.replace('_', ' ')}</Badge>,
    created_at: formatDate(app.created_at),
    actions: (
      <Button variant="secondary" size="sm" onClick={() => setSelectedApp(app)}>
        Review
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
      <PageHeader title={t('nav.applications')} subtitle="Review and process incoming loan applications" />

      {feedback && (
        <div className="mb-6">
          <Alert type={feedback.type} message={feedback.message} />
        </div>
      )}

      {rows.length > 0 ? (
        <>
          <Card className="mb-6 overflow-hidden">
            <Table columns={columns} rows={rows} rowKey="id" />
          </Card>
          <Pagination
            currentPage={page}
            totalPages={Math.max(1, Math.ceil((applications?.total || 0) / 20))}
            onPageChange={setPage}
          />
        </>
      ) : (
        <EmptyState title="No Applications" description="There are no loan applications submitted for review." />
      )}

      {/* Review Modal */}
      {selectedApp && (
        <Modal
          isOpen={!!selectedApp}
          onClose={() => setSelectedApp(null)}
          title={`Review Application #${selectedApp.id}`}
        >
          <div className="space-y-6">
            <div className="grid grid-cols-2 gap-4 bg-bg-page p-4 rounded-lg border border-border">
              <div>
                <p className="text-xs text-text-muted">Requested Amount</p>
                <p className="text-lg font-bold text-brand-700">{formatCurrency(selectedApp.amount)}</p>
              </div>
              <div>
                <p className="text-xs text-text-muted">Current Status</p>
                <Badge variant={statusVariant(selectedApp.status)}>
                  {selectedApp.status.replace('_', ' ')}
                </Badge>
              </div>
              <div>
                <p className="text-xs text-text-muted">Customer ID</p>
                <p className="text-sm font-semibold text-text-primary">{selectedApp.customer_id}</p>
              </div>
              <div>
                <p className="text-xs text-text-muted">Submission Date</p>
                <p className="text-sm text-text-primary">{formatDate(selectedApp.created_at)}</p>
              </div>
              <div className="col-span-2">
                <p className="text-xs text-text-muted">Purpose</p>
                <p className="text-sm font-medium text-text-primary mt-0.5">{selectedApp.purpose}</p>
              </div>
            </div>

            <div className="flex flex-wrap gap-3 justify-end pt-4 border-t border-border">
              <Button
                variant="secondary"
                onClick={() => setPendingAction({ type: 'documents_required', app: selectedApp })}
                disabled={updateMutation.isPending}
              >
                📝 Request Documents
              </Button>
              <Button
                variant="danger"
                onClick={() => setPendingAction({ type: 'rejected', app: selectedApp })}
                disabled={updateMutation.isPending}
              >
                ❌ Reject
              </Button>
              <Button
                variant="primary"
                onClick={() => setPendingAction({ type: 'approved', app: selectedApp })}
                disabled={updateMutation.isPending}
              >
                ✅ Approve Application
              </Button>
            </div>
          </div>
        </Modal>
      )}

      {/* Action Confirmation Dialog */}
      {pendingAction && (
        <ConfirmationDialog
          isOpen={!!pendingAction}
          onClose={() => setPendingAction(null)}
          onConfirm={handleDecision}
          title={`Confirm Application Decision`}
          message={`Are you sure you want to change the status of application #${pendingAction.app.id} to "${pendingAction.type.replace('_', ' ')}"?`}
          confirmLabel="Confirm Decision"
          cancelLabel={t('common.cancel')}
          isLoading={updateMutation.isPending}
        />
      )}
    </AppLayout>
  )
}

export default BankerApplications
