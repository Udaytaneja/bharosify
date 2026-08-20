import React from 'react'
import { useNavigate } from 'react-router-dom'
import { useTranslation } from 'react-i18next'
import Button from '@/components/Button'

const NotFound: React.FC = () => {
  const navigate = useNavigate()
  const { t } = useTranslation()

  return (
    <div className="min-h-screen flex items-center justify-center px-4 bg-bg-page">
      <div className="text-center">
        <h1 className="text-6xl font-bold text-brand-700 mb-4">404</h1>
        <h2 className="text-2xl font-semibold text-text-primary mb-2">{t('error.notFound')}</h2>
        <p className="text-text-muted mb-6">The page you are looking for doesn't exist.</p>
        <Button onClick={() => navigate('/')}>{t('error.goHome')}</Button>
      </div>
    </div>
  )
}

export default NotFound
