import React from 'react'
import { useTranslation } from 'react-i18next'
import AppLayout from '@/layouts/AppLayout'
import { PageHeader, Card, MetricCard, Badge, TrustScore } from '@/components'

interface Agent {
  id: string
  name: string
  status: 'active' | 'pending' | 'suspended' | 'revoked'
  trustScore: number
  capabilities: string[]
  permissions: string[]
}

const UserAgents: React.FC = () => {
  const { t } = useTranslation()

  const agents: Agent[] = [
    {
      id: 'agent_dt_001',
      name: 'Financial Health Digital Twin Agent',
      status: 'active',
      trustScore: 92,
      capabilities: ['Income/Expense Tracking', 'Cash Flow Analysis', 'Budget Optimization'],
      permissions: ['Read Financial Profile', 'Generate Health Reports'],
    },
    {
      id: 'agent_underwriting_002',
      name: 'Credit Risk & Underwriting Assister',
      status: 'active',
      trustScore: 88,
      capabilities: ['Loan Eligibility Pre-Check', 'Repayment Capacity Estimation'],
      permissions: ['Read Credit Scores', 'Formulate Loan Proposals'],
    },
  ]

  return (
    <AppLayout>
      <PageHeader
        title={t('nav.agents')}
        subtitle="Manage autonomous AI agents, digital twin capabilities, and trust permissions"
      />

      <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
        <MetricCard label="Active Autonomous Agents" value={agents.length.toString()} icon="🤖" />
        <MetricCard label="Average Agent Trust Score" value="90 / 100" icon="🛡️" />
        <MetricCard label="Permission Boundary" value="Restricted" icon="🔒" />
      </div>

      <div className="space-y-6">
        {agents.map((agent) => (
          <Card key={agent.id} className="p-6">
            <div className="flex flex-col md:flex-row justify-between items-start md:items-center gap-4 mb-4">
              <div>
                <div className="flex items-center gap-2 mb-1">
                  <h3 className="text-lg font-bold text-text-primary">{agent.name}</h3>
                  <Badge variant={agent.status === 'active' ? 'success' : 'default'}>{agent.status}</Badge>
                </div>
                <p className="text-xs text-text-muted">Agent ID: {agent.id}</p>
              </div>

              <div className="flex items-center gap-3">
                <span className="text-xs text-text-muted">Trust Score:</span>
                <TrustScore score={agent.trustScore} level="trusted" size="sm" />
              </div>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-4 pt-4 border-t border-border">
              <div>
                <p className="text-xs font-semibold text-text-muted uppercase tracking-wider mb-2">Capabilities</p>
                <div className="flex flex-wrap gap-1.5">
                  {agent.capabilities.map((cap, idx) => (
                    <span key={idx} className="text-xs font-medium bg-brand-50 text-brand-700 px-2.5 py-1 rounded-md border border-brand-100">
                      ⚡ {cap}
                    </span>
                  ))}
                </div>
              </div>

              <div>
                <p className="text-xs font-semibold text-text-muted uppercase tracking-wider mb-2">Authorized Permissions</p>
                <div className="flex flex-wrap gap-1.5">
                  {agent.permissions.map((perm, idx) => (
                    <span key={idx} className="text-xs font-medium bg-bg-page text-text-secondary px-2.5 py-1 rounded-md border border-border">
                      🔒 {perm}
                    </span>
                  ))}
                </div>
              </div>
            </div>
          </Card>
        ))}
      </div>
    </AppLayout>
  )
}

export default UserAgents
