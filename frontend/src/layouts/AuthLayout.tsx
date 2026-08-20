import React from 'react'
import { useTranslation } from 'react-i18next'

interface AuthLayoutProps {
  children: React.ReactNode
  title: string
  subtitle?: string
  footerText?: string
}

const AuthLayout: React.FC<AuthLayoutProps> = ({ children, title, subtitle, footerText }) => {
  const { i18n } = useTranslation()

  const toggleLanguage = () => {
    const newLang = i18n.language === 'en' ? 'hi' : 'en'
    i18n.changeLanguage(newLang)
    localStorage.setItem('language', newLang)
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-brand-900 via-brand-800 to-brand-700 flex flex-col">
      {/* Language Toggle */}
      <div className="absolute top-4 right-4">
        <button
          onClick={toggleLanguage}
          className="px-4 py-2 bg-white bg-opacity-20 text-white rounded-lg hover:bg-opacity-30 transition-colors text-sm font-medium"
        >
          {i18n.language === 'en' ? 'हिन्दी' : 'English'}
        </button>
      </div>

      {/* Main Content */}
      <div className="flex-1 flex items-center justify-center px-4">
        <div className="w-full max-w-md">
          <div className="text-center mb-8">
            <h1 className="text-4xl font-bold text-white mb-2">AGENTTRUST</h1>
            <p className="text-brand-100">Trusted financial intelligence</p>
          </div>

          <div className="bg-bg-surface rounded-lg shadow-lg p-8">
            <div className="mb-6">
              <h2 className="text-2xl font-bold text-text-primary mb-2">{title}</h2>
              {subtitle && <p className="text-text-muted text-sm">{subtitle}</p>}
            </div>

            {children}

            {footerText && (
              <p className="text-center text-text-muted text-sm mt-6">{footerText}</p>
            )}
          </div>
        </div>
      </div>

      {/* Footer */}
      <div className="bg-black bg-opacity-20 text-center py-4 text-white text-sm">
        <p>© 2024 AgentTrust OS. All rights reserved.</p>
      </div>
    </div>
  )
}

export default AuthLayout
