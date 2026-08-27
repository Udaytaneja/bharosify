import React, { useRef, useState } from 'react'
import { useTranslation } from 'react-i18next'
import AppLayout from '@/layouts/AppLayout'
import { useApplications } from '@/hooks'
import { aiApi, documentApi, DocumentIntelligenceResponse } from '@/api/financial'
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
  const [documentResult, setDocumentResult] = useState<DocumentIntelligenceResponse | null>(null)
  const [documentFile, setDocumentFile] = useState<File | null>(null)
  const [isDocumentAnalyzing, setIsDocumentAnalyzing] = useState(false)
  const documentInputRef = useRef<HTMLInputElement>(null)

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

  const handleDocumentAnalyze = async (file: File) => {
    setDocumentFile(file)
    setDocumentResult(null)
    setErrorMsg('')
    setIsDocumentAnalyzing(true)
    try {
      setDocumentResult(await documentApi.analyze(file))
    } catch (err: any) {
      setErrorMsg(err.response?.data?.detail?.message || err.message || 'Document analysis failed')
    } finally {
      setIsDocumentAnalyzing(false)
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
        <div className="flex items-center justify-between gap-4 mb-4">
          <div>
            <h2 className="text-lg font-semibold text-text-primary">Experimental document perception</h2>
            <p className="text-sm text-text-muted">YOLO layout and OCR evidence only. Human review remains mandatory.</p>
          </div>
          <Button variant="secondary" onClick={() => documentInputRef.current?.click()} disabled={isDocumentAnalyzing}>
            {isDocumentAnalyzing ? 'Analyzing...' : 'Upload document'}
          </Button>
          <input
            ref={documentInputRef}
            className="hidden"
            type="file"
            accept=".pdf,.png,.jpg,.jpeg,.tiff,.bmp"
            onChange={(event) => event.target.files?.[0] && handleDocumentAnalyze(event.target.files[0])}
          />
        </div>
        {documentFile && <p className="text-xs text-text-muted mb-3">{documentFile.name}</p>}
        {documentResult && (
          <div className="grid gap-4 lg:grid-cols-[minmax(0,1fr)_minmax(280px,0.8fr)]">
            <div className="rounded-lg border border-border p-4">
              <div className="flex flex-wrap gap-2 mb-3">
                <Badge variant="info">{documentResult.model_metadata.provenance?.layout_model_status || 'EXPERIMENTAL'}</Badge>
                <Badge variant="warning">Human review required</Badge>
                <span className="text-xs text-text-muted self-center">{documentResult.layout_regions.length} layout regions</span>
              </div>
              <div className="relative overflow-auto bg-bg-page p-2">
                {documentFile && documentFile.type.startsWith('image/') ? (
                  <div className="relative inline-block min-w-full">
                    <img src={URL.createObjectURL(documentFile)} alt="Uploaded document" className="block max-w-full" />
                    {documentResult.layout_regions.map((region, index) => {
                      const [x1, y1, x2, y2] = region.bbox
                      return <div key={index} className="absolute border-2 border-brand-600" style={{ left: x1, top: y1, width: x2 - x1, height: y2 - y1 }} title={`${region.source_class || region.element_type} ${(region.confidence * 100).toFixed(1)}%`} />
                    })}
                  </div>
                ) : <p className="text-sm text-text-muted">Preview overlay is available for image uploads. PDF evidence is still returned by the API.</p>}
              </div>
            </div>
            <div className="rounded-lg border border-border p-4">
              <h3 className="text-sm font-semibold text-text-primary mb-2">Detected evidence</h3>
              <p className="text-xs text-text-muted mb-3">{documentResult.model_metadata.provenance?.indian_domain_validation ? 'Indian validation present' : 'Indian-domain validation not claimed'}</p>
              <div className="space-y-2 max-h-72 overflow-auto">
                {documentResult.ocr_lines.map((line, index) => <div key={index} className="text-xs text-text-primary"><span className="font-semibold">{line.text}</span> <span className="text-text-muted">({line.bbox.join(', ')})</span></div>)}
                {!documentResult.ocr_lines.length && <p className="text-sm text-text-muted">No OCR lines returned.</p>}
              </div>
            </div>
          </div>
        )}
      </Card>

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
