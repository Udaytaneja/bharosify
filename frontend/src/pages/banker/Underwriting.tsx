import React, { useState } from 'react'
import { useTranslation } from 'react-i18next'
import AppLayout from '@/layouts/AppLayout'
import { useApplications } from '@/hooks'
import { aiApi } from '@/api/financial'
import { formatCurrency } from '@/utils'
import { 
  PageHeader, 
  Loading, 
  Card, 
  Table, 
  Badge, 
  EmptyState, 
  Button, 
  Modal,
  Alert
} from '@/components'
import { LoanApplication, AIResponse } from '@/types'

const BankerUnderwriting: React.FC = () => {
  const { t, i18n } = useTranslation()
  const { data: applications, isLoading } = useApplications(0, 50)
  const [selectedApp, setSelectedApp] = useState<LoanApplication | null>(null)
  const [aiAnalysis, setAiAnalysis] = useState<AIResponse | null>(null)
  const [isAnalyzing, setIsAnalyzing] = useState(false)
  const [errorMsg, setErrorMsg] = useState('')

  const underwritingQueue = applications?.items?.filter(
    (app) => ['submitted', 'under_review', 'underwriting'].includes(app.status)
  ) || []

  const handleRunUnderwriting = async (app: LoanApplication) => {
    setSelectedApp(app)
    setAiAnalysis(null)
    setErrorMsg('')
    setIsAnalyzing(true)

    try {
      const inputPrompt = `Perform automated credit underwriting for application #${app.id}, requested amount: ₹${app.amount}, purpose: "${app.purpose}".`
      const result = await aiApi.underwriting(inputPrompt, i18n.language, {
        application_id: app.id,
        amount: app.amount,
        purpose: app.purpose,
      })
      setAiAnalysis(result)
    } catch (err: any) {
      setErrorMsg(err.response?.data?.detail || err.message || 'Underwriting analysis failed')
    } finally {
      setIsAnalyzing(false)
    }
  }

  const columns = [
    { key: 'id', label: 'App ID', width: '15%' },
    { key: 'customer_id', label: 'Customer ID', width: '20%' },
    { key: 'amount', label: 'Requested Amount', width: '20%' },
    { key: 'status', label: 'Status', width: '20%' },
    { key: 'actions', label: 'Actions', width: '25%' },
  ]

  const rows = underwritingQueue.map((app) => ({
    ...app,
    amount: <span className="font-semibold text-text-primary">{formatCurrency(app.amount)}</span>,
    status: <Badge variant="info">{app.status.replace('_', ' ')}</Badge>,
    actions: (
      <Button variant="primary" size="sm" onClick={() => handleRunUnderwriting(app)}>
        🔍 AI Underwriting Review
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
      <PageHeader
        title={t('nav.underwriting')}
        subtitle="AI-assisted credit underwriting & human review decision engine"
      />

      <Card className="mb-6">
        <h2 className="text-lg font-semibold text-text-primary mb-4">
          Underwriting Application Queue
        </h2>
        {rows.length > 0 ? (
          <Table columns={columns} rows={rows} rowKey="id" />
        ) : (
          <EmptyState
            title="No Applications in Queue"
            description="All pending loan applications have been evaluated or processed."
          />
        )}
      </Card>

      {/* Underwriting Analysis Modal */}
      {selectedApp && (
        <Modal
          isOpen={!!selectedApp}
          onClose={() => setSelectedApp(null)}
          title={`AI Underwriting Report #${selectedApp.id}`}
        >
          <div className="space-y-6">
            <div className="bg-bg-page p-4 rounded-lg border border-border grid grid-cols-2 gap-4">
              <div>
                <p className="text-xs text-text-muted">Applicant ID</p>
                <p className="text-sm font-semibold text-text-primary">{selectedApp.customer_id}</p>
              </div>
              <div>
                <p className="text-xs text-text-muted">Loan Principal</p>
                <p className="text-lg font-bold text-brand-700">{formatCurrency(selectedApp.amount)}</p>
              </div>
            </div>

            {errorMsg && <Alert type="danger" message={errorMsg} />}

            {isAnalyzing ? (
              <div className="p-8 text-center">
                <Loading />
                <p className="text-sm text-text-muted mt-4">Running AI risk scoring & evidence synthesis...</p>
              </div>
            ) : aiAnalysis ? (
              <div className="space-y-4">
                <div className="p-4 bg-brand-50/40 rounded-xl border border-brand-100 flex items-center justify-between">
                  <div>
                    <p className="text-xs text-text-muted uppercase tracking-wider mb-1">AI Recommendation</p>
                    <p className="text-lg font-extrabold text-brand-700 uppercase">{aiAnalysis.recommendation}</p>
                  </div>
                  <div className="text-right">
                    <p className="text-xs text-text-muted uppercase tracking-wider mb-1">Model Confidence</p>
                    <Badge variant="info">{(aiAnalysis.confidence * 100).toFixed(0)}% Confidence</Badge>
                  </div>
                </div>

                <div className="p-4 bg-bg-page rounded-lg border border-border">
                  <h4 className="text-xs font-semibold text-text-muted uppercase tracking-wider mb-2">Reasoning Summary</h4>
                  <p className="text-sm text-text-primary leading-relaxed">{aiAnalysis.response}</p>
                  {aiAnalysis.reasoning_summary && (
                    <p className="text-xs text-text-secondary mt-2 italic">{aiAnalysis.reasoning_summary}</p>
                  )}
                </div>

                {aiAnalysis.requires_human_review && (
                  <Alert
                    type="warning"
                    message="⚠️ Human Banker Sign-off Required: This application involves factors requiring manual verification."
                  />
                )}
              </div>
            ) : null}

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

export default BankerUnderwriting
