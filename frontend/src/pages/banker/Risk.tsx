import React, { useState } from 'react'
import { useTranslation } from 'react-i18next'
import AppLayout from '@/layouts/AppLayout'
import { aiApi } from '@/api/financial'
import { bankerApi } from '@/api'
import { useQuery } from '@tanstack/react-query'
import { PageHeader, Loading, Card, Button, Input, Select, Alert, Badge } from '@/components'
import { AIResponse } from '@/types'

const BankerRisk: React.FC = () => {
  const { t, i18n } = useTranslation()
  const [selectedCustomerId, setSelectedCustomerId] = useState('')
  const [customInput, setCustomInput] = useState('')
  const [riskReport, setRiskReport] = useState<AIResponse | null>(null)
  const [isAnalyzing, setIsAnalyzing] = useState(false)
  const [errorMsg, setErrorMsg] = useState('')

  const { data: customers } = useQuery({
    queryKey: ['banker', 'customers', 'all'],
    queryFn: () => bankerApi.getCustomers(0, 100),
  })

  const handleRunRiskAnalysis = async (e: React.FormEvent) => {
    e.preventDefault()
    setRiskReport(null)
    setErrorMsg('')
    setIsAnalyzing(true)

    const queryPrompt = customInput.trim() || `Assess portfolio risk and credit rating for customer ID: ${selectedCustomerId || 'ALL_CUSTOMERS'}`

    try {
      const result = await aiApi.riskAnalysis(queryPrompt, i18n.language, {
        customer_id: selectedCustomerId,
      })
      setRiskReport(result)
    } catch (err: any) {
      setErrorMsg(err.response?.data?.detail || err.message || 'Risk analysis failed')
    } finally {
      setIsAnalyzing(false)
    }
  }

  return (
    <AppLayout>
      <PageHeader
        title={t('nav.risk')}
        subtitle="AI-driven customer risk scoring & portfolio risk assessments"
      />

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6 mb-8">
        <Card className="lg:col-span-1">
          <h3 className="font-semibold text-text-primary mb-4">Risk Evaluation Trigger</h3>
          <form onSubmit={handleRunRiskAnalysis} className="space-y-4">
            <div>
              <label className="block text-xs font-semibold text-text-muted uppercase tracking-wider mb-1">
                Select Customer (Optional)
              </label>
              <Select
                value={selectedCustomerId}
                onChange={(e) => setSelectedCustomerId(e.target.value)}
                options={[
                  { value: '', label: 'All Customers (Portfolio Level)' },
                  ...(customers?.items?.map((c) => ({
                    value: c.id,
                    label: `${c.name} (${c.email})`,
                  })) || []),
                ]}
                disabled={isAnalyzing}
              />
            </div>

            <div>
              <label className="block text-xs font-semibold text-text-muted uppercase tracking-wider mb-1">
                Risk Analysis Query
              </label>
              <Input
                placeholder="e.g. Evaluate debt-to-income ratio risk..."
                value={customInput}
                onChange={(e) => setCustomInput(e.target.value)}
                disabled={isAnalyzing}
              />
            </div>

            <Button
              type="submit"
              variant="primary"
              className="w-full"
              isLoading={isAnalyzing}
            >
              ⚡ Run Risk Assessment
            </Button>
          </form>
        </Card>

        <Card className="lg:col-span-2">
          <h3 className="font-semibold text-text-primary mb-4">Risk Analysis Report</h3>

          {errorMsg && <Alert type="danger" message={errorMsg} />}

          {isAnalyzing ? (
            <div className="p-8 text-center">
              <Loading />
              <p className="text-sm text-text-muted mt-4">Synthesizing credit factors & risk vector analysis...</p>
            </div>
          ) : riskReport ? (
            <div className="space-y-4">
              <div className="p-4 bg-brand-50/40 rounded-xl border border-brand-100 flex items-center justify-between">
                <div>
                  <p className="text-xs text-text-muted uppercase tracking-wider mb-1">Risk Decision Recommendation</p>
                  <p className="text-lg font-extrabold text-brand-700 uppercase">{riskReport.recommendation}</p>
                </div>
                <div className="text-right">
                  <p className="text-xs text-text-muted uppercase tracking-wider mb-1">AI Confidence</p>
                  <Badge variant="info">{(riskReport.confidence * 100).toFixed(0)}% Confidence</Badge>
                </div>
              </div>

              <div className="p-4 bg-bg-page rounded-lg border border-border">
                <h4 className="text-xs font-semibold text-text-muted uppercase tracking-wider mb-2">Detailed Findings</h4>
                <p className="text-sm text-text-primary leading-relaxed whitespace-pre-wrap">{riskReport.response}</p>
              </div>

              {riskReport.reasoning_summary && (
                <div className="p-3 bg-bg-page rounded-lg border border-border text-xs text-text-secondary">
                  <span className="font-semibold text-text-primary block mb-1">Summary Rationale:</span>
                  {riskReport.reasoning_summary}
                </div>
              )}
            </div>
          ) : (
            <div className="p-8 text-center text-text-muted border border-dashed border-border rounded-xl">
              <p className="text-sm">Select a customer or submit a query on the left to run live AI risk analysis.</p>
            </div>
          )}
        </Card>
      </div>
    </AppLayout>
  )
}

export default BankerRisk
