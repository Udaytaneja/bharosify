import React, { useState } from 'react'
import { useTranslation } from 'react-i18next'
import AppLayout from '@/layouts/AppLayout'
import { formatCurrency } from '@/utils'
import { PageHeader, Card, MetricCard, Button, Badge, Modal, Input } from '@/components'

interface Goal {
  id: string
  title: string
  category: 'savings' | 'emergency' | 'purchase' | 'debt'
  targetAmount: number
  currentAmount: number
  targetDate: string
}

const UserGoals: React.FC = () => {
  const { t } = useTranslation()
  const [isModalOpen, setIsModalOpen] = useState(false)

  // Clean UI architecture with sample financial goal tracking
  const [goals] = useState<Goal[]>([
    {
      id: 'g1',
      title: 'Emergency Reserve Fund',
      category: 'emergency',
      targetAmount: 150000,
      currentAmount: 95000,
      targetDate: '2026-12-31',
    },
    {
      id: 'g2',
      title: 'Home Down Payment Savings',
      category: 'purchase',
      targetAmount: 500000,
      currentAmount: 210000,
      targetDate: '2027-06-30',
    },
    {
      id: 'g3',
      title: 'Personal Loan Early payoff',
      category: 'debt',
      targetAmount: 80000,
      currentAmount: 55000,
      targetDate: '2026-10-15',
    },
  ])

  const totalTarget = goals.reduce((sum, g) => sum + g.targetAmount, 0)
  const totalSaved = goals.reduce((sum, g) => sum + g.currentAmount, 0)
  const overallProgress = totalTarget > 0 ? (totalSaved / totalTarget) * 100 : 0

  return (
    <AppLayout>
      <PageHeader
        title={t('nav.goals')}
        subtitle="Set, track, and achieve your short-term and long-term financial milestones"
        action={
          <Button variant="primary" onClick={() => setIsModalOpen(true)}>
            + Add New Goal
          </Button>
        }
      />

      {/* Goal Summary Metrics */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
        <MetricCard label="Total Goal Target" value={formatCurrency(totalTarget)} icon="🎯" />
        <MetricCard label="Total Accumulated" value={formatCurrency(totalSaved)} icon="💎" />
        <MetricCard label="Overall Goal Progress" value={`${overallProgress.toFixed(1)}%`} icon="📈" />
      </div>

      <div className="space-y-6">
        {goals.map((goal) => {
          const progressPercent = Math.min(100, (goal.currentAmount / goal.targetAmount) * 100)
          return (
            <Card key={goal.id} className="p-6">
              <div className="flex flex-col md:flex-row justify-between items-start md:items-center gap-4 mb-4">
                <div>
                  <div className="flex items-center gap-2 mb-1">
                    <h3 className="text-lg font-bold text-text-primary">{goal.title}</h3>
                    <Badge variant="info">{goal.category.toUpperCase()}</Badge>
                  </div>
                  <p className="text-xs text-text-muted">Target Date: {goal.targetDate}</p>
                </div>
                <div className="text-right">
                  <p className="text-xl font-extrabold text-brand-700">
                    {formatCurrency(goal.currentAmount)}{' '}
                    <span className="text-xs text-text-muted font-normal">of {formatCurrency(goal.targetAmount)}</span>
                  </p>
                </div>
              </div>

              {/* Progress Bar */}
              <div className="w-full bg-bg-page rounded-full h-3 overflow-hidden border border-border">
                <div
                  className="bg-brand-700 h-full rounded-full transition-all duration-500"
                  style={{ width: `${progressPercent}%` }}
                />
              </div>
              <div className="flex justify-between text-xs text-text-muted mt-2">
                <span>Progress: {progressPercent.toFixed(1)}%</span>
                <span>Remaining: {formatCurrency(Math.max(0, goal.targetAmount - goal.currentAmount))}</span>
              </div>
            </Card>
          )
        })}
      </div>


      {/* New Goal Modal */}
      <Modal isOpen={isModalOpen} onClose={() => setIsModalOpen(false)} title="Create New Financial Goal">
        <div className="space-y-4">
          <p className="text-xs text-text-muted bg-brand-50 p-3 rounded-lg border border-brand-100">
            ℹ️ <strong>Backend Integration Note</strong>: Goal persistence requires future backend API expansion (`/goals`). Frontend UI architecture is complete.
          </p>

          <div>
            <label className="block text-sm font-medium text-text-primary mb-1">Goal Title</label>
            <Input placeholder="e.g. Vacation Savings" />
          </div>

          <div>
            <label className="block text-sm font-medium text-text-primary mb-1">Target Amount (₹)</label>
            <Input type="number" placeholder="100000" />
          </div>

          <div className="flex justify-end gap-3 pt-4 border-t border-border">
            <Button variant="secondary" onClick={() => setIsModalOpen(false)}>
              {t('common.cancel')}
            </Button>
            <Button variant="primary" onClick={() => setIsModalOpen(false)}>
              {t('common.save')}
            </Button>
          </div>
        </div>
      </Modal>
    </AppLayout>
  )
}

export default UserGoals
