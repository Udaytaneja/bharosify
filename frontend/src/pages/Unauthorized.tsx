import React from 'react'
import { useNavigate } from 'react-router-dom'
import { useTranslation } from 'react-i18next'
import Button from '@/components/Button'

const Unauthorized: React.FC = () => {
  const navigate = useNavigate()
  const { t } = useTranslation()

  return (
    <div className="min-h-screen flex items-center justify-center px-4 bg-bg-page">
      <div className="text-center">
        <h1 className="text-6xl font-bold text-status-danger mb-4">403</h1>
        <h2 className="text-2xl font-semibold text-text-primary mb-2">{t('error.forbidden')}</h2>
        <p className="text-text-muted mb-6">You don't have permission to access this resource.</p>
        <Button onClick={() => navigate('/')}>{t('error.goHome')}</Button>
      </div>
    </div>
  )
}

export default Unauthorized
