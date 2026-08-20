import React from 'react'
import { useNavigate } from 'react-router-dom'
import { useTranslation } from 'react-i18next'
import Button from '@/components/Button'

const RoleSelectionPage: React.FC = () => {
  const navigate = useNavigate()
  const { t } = useTranslation()

  return (
    <div className="min-h-screen bg-gradient-to-br from-brand-900 via-brand-800 to-brand-700 flex items-center justify-center px-4">
      <div className="w-full max-w-2xl">
        <div className="text-center mb-12">
          <h1 className="text-4xl font-bold text-white mb-2">AGENTTRUST</h1>
          <p className="text-brand-100">{t('auth.selectRole')}</p>
        </div>

        <div className="grid md:grid-cols-2 gap-6">
          {/* User Role */}
          <div
            className="bg-bg-surface rounded-lg p-8 cursor-pointer hover:shadow-lg transition-all"
            onClick={() => navigate('/login?role=user')}
          >
            <div className="text-4xl mb-4">👤</div>
            <h2 className="text-xl font-bold text-text-primary mb-2">{t('auth.user')}</h2>
            <p className="text-text-muted text-sm mb-6">
              Manage your finances, track trust, and apply for loans
            </p>
            <Button fullWidth variant="primary" className="w-full">
              {t('auth.login')}
            </Button>
          </div>

          {/* Banker Role */}
          <div
            className="bg-bg-surface rounded-lg p-8 cursor-pointer hover:shadow-lg transition-all"
            onClick={() => navigate('/login?role=banker')}
          >
            <div className="text-4xl mb-4">🏦</div>
            <h2 className="text-xl font-bold text-text-primary mb-2">{t('auth.banker')}</h2>
            <p className="text-text-muted text-sm mb-6">
              Review applications, analyze risk, and manage customers
            </p>
            <Button fullWidth variant="primary" className="w-full">
              {t('auth.login')}
            </Button>
          </div>
        </div>
      </div>
    </div>
  )
}

export default RoleSelectionPage
