import React, { useState } from 'react'
import { useTranslation } from 'react-i18next'
import AppLayout from '@/layouts/AppLayout'
import { useApplications, useCreateApplication } from '@/hooks'
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
  Input, 
  Textarea,
  Timeline,
  Alert
} from '@/components'
import { LoanApplication } from '@/types'

const UserApplications: React.FC = () => {
  const { t } = useTranslation()
  const [page, setPage] = useState(1)
  const [isModalOpen, setIsModalOpen] = useState(false)
  const [selectedApp, setSelectedApp] = useState<LoanApplication | null>(null)
  
  // Form state
  const [amount, setAmount] = useState('')
  const [purpose, setPurpose] = useState('')
  const [formError, setFormError] = useState('')

  const { data: applications, isLoading } = useApplications((page - 1) * 20, 20)
  const createMutation = useCreateApplication()

  const handleCreateSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setFormError('')

    const numAmount = parseFloat(amount)
    if (isNaN(numAmount) || numAmount <= 0) {
      setFormError('Please enter a valid positive loan amount.')
      return
    }

    if (!purpose.trim()) {
      setFormError('Please describe the purpose of your loan.')
      return
    }

    try {
      await createMutation.mutateAsync({
        amount: numAmount,
        purpose: purpose.trim(),
      })
      setIsModalOpen(false)
      setAmount('')
      setPurpose('')
    } catch (err: any) {
      setFormError(err.response?.data?.detail || err.message || 'Failed to submit application')
    }
  }

  const statusVariant = (status: string) => {
    switch (status) {
      case 'approved':
      case 'completed':
        return 'success'
      case 'rejected':
      case 'withdrawn':
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
    { key: 'id', label: 'ID', width: '15%' },
    { key: 'amount', label: t('applications.amount'), width: '15%' },
    { key: 'purpose', label: t('applications.purpose'), width: '25%' },
    { key: 'status', label: t('applications.status'), width: '20%' },
    { key: 'created_at', label: t('applications.createdOn'), width: '15%' },
    { key: 'actions', label: 'Actions', width: '10%' },
  ]

  const rows = applications?.items?.map((app) => ({
    ...app,
    amount: <span className="font-semibold text-text-primary">{formatCurrency(app.amount)}</span>,
    created_at: formatDate(app.created_at),
    status: <Badge variant={statusVariant(app.status)}>{app.status.replace('_', ' ')}</Badge>,
    actions: (
      <Button variant="secondary" size="sm" onClick={() => setSelectedApp(app)}>
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
      <PageHeader
        title={t('nav.applications')}
        subtitle="Manage and track your loan applications"
        action={
          <Button variant="primary" onClick={() => setIsModalOpen(true)}>
            + {t('applications.newApplication')}
          </Button>
        }
      />

      {rows.length > 0 ? (
        <>
          <Card className="mb-6 overflow-hidden">
            <Table columns={columns} rows={rows} rowKey="id" emptyMessage={t('applications.applications')} />
          </Card>
          <Pagination
            currentPage={page}
            totalPages={Math.max(1, Math.ceil((applications?.total || 0) / 20))}
            onPageChange={setPage}
          />
        </>
      ) : (
        <EmptyState
          title="No Loan Applications"
          description="You haven't submitted any loan applications yet. Click below to apply."
          action={
            <Button variant="primary" onClick={() => setIsModalOpen(true)}>
              + {t('applications.newApplication')}
            </Button>
          }
        />
      )}

      {/* New Application Modal */}
      <Modal
        isOpen={isModalOpen}
        onClose={() => setIsModalOpen(false)}
        title={t('applications.newApplication')}
      >
        <form onSubmit={handleCreateSubmit} className="space-y-4">
          {formError && <Alert type="danger" message={formError} />}

          <div>
            <label className="block text-sm font-medium text-text-primary mb-1">
              Loan Amount (₹)
            </label>
            <Input
              type="number"
              placeholder="e.g. 50000"
              value={amount}
              onChange={(e) => setAmount(e.target.value)}
              disabled={createMutation.isPending}
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-text-primary mb-1">
              Purpose of Loan
            </label>
            <Textarea
              placeholder="Explain the purpose of this loan application..."
              value={purpose}
              onChange={(e) => setPurpose(e.target.value)}
              rows={3}
              disabled={createMutation.isPending}
            />
          </div>

          <div className="flex justify-end gap-3 pt-4 border-t border-border">
            <Button
              type="button"
              variant="secondary"
              onClick={() => setIsModalOpen(false)}
              disabled={createMutation.isPending}
            >
              {t('common.cancel')}
            </Button>
            <Button
              type="submit"
              variant="primary"
              isLoading={createMutation.isPending}
            >
              {t('common.submit')}
            </Button>
          </div>
        </form>
      </Modal>

      {/* Application Details Modal */}
      {selectedApp && (
        <Modal
          isOpen={!!selectedApp}
          onClose={() => setSelectedApp(null)}
          title={`Application Details #${selectedApp.id}`}
        >
          <div className="space-y-6">
            <div className="grid grid-cols-2 gap-4 bg-bg-page p-4 rounded-lg border border-border">
              <div>
                <p className="text-xs text-text-muted">Amount Requested</p>
                <p className="text-lg font-bold text-brand-700">{formatCurrency(selectedApp.amount)}</p>
              </div>
              <div>
                <p className="text-xs text-text-muted">Current Status</p>
                <Badge variant={statusVariant(selectedApp.status)}>
                  {selectedApp.status.replace('_', ' ')}
                </Badge>
              </div>
              <div className="col-span-2">
                <p className="text-xs text-text-muted">Purpose</p>
                <p className="text-sm font-medium text-text-primary mt-0.5">{selectedApp.purpose}</p>
              </div>
            </div>

            <div>
              <h4 className="text-sm font-semibold text-text-primary mb-3">Application Progress</h4>
              <Timeline
                items={[
                  { title: 'Application Submitted', date: formatDate(selectedApp.created_at), completed: true },
                  { title: 'Document Verification', date: 'Under Review', completed: ['submitted', 'under_review', 'underwriting', 'approved'].includes(selectedApp.status) },
                  { title: 'Underwriting & Risk Decision', date: 'Automated Decision', completed: ['underwriting', 'approved'].includes(selectedApp.status) },
                  { title: 'Final Approval & Disbursal', date: selectedApp.status === 'approved' ? 'Approved' : 'Pending', completed: selectedApp.status === 'approved' },
                ]}
              />
            </div>

            <div className="flex justify-end pt-4 border-t border-border">
              <Button variant="secondary" onClick={() => setSelectedApp(null)}>
                {t('common.close')}
              </Button>
            </div>
          </div>
        </Modal>
      )}
    </AppLayout>
  )
}

export default UserApplications
