import React from 'react'
import { useNavigate } from 'react-router-dom'
import { useTranslation } from 'react-i18next'
import Button from '@/components/Button'

const LandingPage: React.FC = () => {
  const navigate = useNavigate()
  const { t, i18n } = useTranslation()

  return (
    <div className="min-h-screen bg-gradient-to-br from-brand-900 via-brand-800 to-brand-700 flex items-center justify-center px-4">
      {/* Language Toggle */}
      <div className="absolute top-4 right-4">
        <button
          onClick={() => {
            const newLang = i18n.language === 'en' ? 'hi' : 'en'
            i18n.changeLanguage(newLang)
            localStorage.setItem('language', newLang)
          }}
          className="px-4 py-2 bg-white bg-opacity-20 text-white rounded-lg hover:bg-opacity-30 transition-colors text-sm font-medium"
        >
          {i18n.language === 'en' ? 'हिन्दी' : 'English'}
        </button>
      </div>

      <div className="text-center max-w-md">
        <h1 className="text-5xl md:text-6xl font-bold text-white mb-3">AGENTTRUST</h1>
        <p className="text-brand-100 text-lg md:text-xl mb-12">
          {t('auth.selectRole') || 'Trusted financial intelligence'}
        </p>

        <div className="space-y-4">
          <Button
            fullWidth
            size="lg"
            variant="primary"
            onClick={() => navigate('/role-selection')}
            className="bg-white text-brand-900 hover:bg-brand-50 font-semibold"
          >
            {i18n.language === 'en' ? '👤 Continue' : '👤 जारी रखें'}
          </Button>
        </div>

        <div className="mt-12 pt-8 border-t border-white border-opacity-20 text-white text-sm">
          <p>© 2024 AgentTrust OS. Trusted financial intelligence platform.</p>
        </div>
      </div>
    </div>
  )
}

export default LandingPage
