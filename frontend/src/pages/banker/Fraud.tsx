import React, { useState } from 'react'
import { useTranslation } from 'react-i18next'
import AppLayout from '@/layouts/AppLayout'
import { riskApi, bankerApi } from '@/api'
import { useQuery } from '@tanstack/react-query'
import { PageHeader, Loading, Card, Table, Badge, EmptyState, Select, MetricCard } from '@/components'

const BankerFraud: React.FC = () => {
  const { t } = useTranslation()
  const [selectedCustomerId, setSelectedCustomerId] = useState('')

  const { data: customers } = useQuery({
    queryKey: ['banker', 'customers', 'all'],
    queryFn: () => bankerApi.getCustomers(0, 100),
  })

  const { data: fraudSignals, isLoading } = useQuery({
    queryKey: ['banker', 'fraud', selectedCustomerId],
    queryFn: () => (selectedCustomerId ? riskApi.getFraudSignals(selectedCustomerId) : Promise.resolve([])),
    enabled: !!selectedCustomerId,
  })

  const severityVariant = (severity: string) => {
    switch (severity) {
      case 'critical':
      case 'high':
        return 'danger'
      case 'medium':
        return 'warning'
      default:
        return 'info'
    }
  }

  const columns = [
    { key: 'id', label: 'Signal ID', width: '15%' },
    { key: 'type', label: 'Fraud Type', width: '20%' },
    { key: 'severity', label: 'Severity', width: '15%' },
    { key: 'score', label: 'Score', width: '15%' },
    { key: 'status', label: 'Status', width: '15%' },
    { key: 'evidence', label: 'Evidence', width: '20%' },
  ]

  const rows = (fraudSignals || []).map((sig) => ({
    ...sig,
    severity: <Badge variant={severityVariant(sig.severity)}>{sig.severity}</Badge>,
    score: <span className="font-bold text-brand-700">{sig.score}</span>,
    status: <Badge variant="default">{sig.status}</Badge>,
  }))

  return (
    <AppLayout>
      <PageHeader
        title={t('nav.fraud')}
        subtitle="Real-time fraud signal monitoring & anomalous transaction detection"
      />

      <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
        <MetricCard label="Active Fraud Cases" value="0" icon="🚨" />
        <MetricCard label="High-Risk Signals" value="0" icon="⚠️" />
        <MetricCard label="Resolved Alerts" value="0" icon="✅" />
      </div>

      <Card className="mb-6">
        <div className="max-w-md">
          <label className="block text-xs font-semibold text-text-muted uppercase tracking-wider mb-1">
            Select Customer to Inspect Signals
          </label>
          <Select
            value={selectedCustomerId}
            onChange={(e) => setSelectedCustomerId(e.target.value)}
            options={[
              { value: '', label: '-- Select Customer Account --' },
              ...(customers?.items?.map((c) => ({
                value: c.id,
                label: `${c.name} (${c.email})`,
              })) || []),
            ]}
          />
        </div>
      </Card>

      <Card>
        <h2 className="text-lg font-semibold text-text-primary mb-4">Detected Fraud Signals</h2>
        {isLoading ? (
          <Loading />
        ) : rows.length > 0 ? (
          <Table columns={columns} rows={rows} rowKey="id" />
        ) : (
          <EmptyState
            title="No Fraud Signals Detected"
            description={
              selectedCustomerId
                ? "No anomaly signals have been triggered for this customer account."
                : "Select a customer account above to inspect active fraud detection signals."
            }
          />
        )}
      </Card>
    </AppLayout>
  )
}

export default BankerFraud
