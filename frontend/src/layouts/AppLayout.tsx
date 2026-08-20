import React, { useState } from 'react'
import { Link, useLocation } from 'react-router-dom'
import { useTranslation } from 'react-i18next'
import { useLogout } from '@/hooks'
import { useAuth } from '@/hooks'
import Button from '@/components/Button'

interface NavItem {
  label: string
  href: string
  icon?: string
}

interface AppLayoutProps {
  children: React.ReactNode
  navItems: NavItem[]
  title?: string
}

const AppLayout: React.FC<AppLayoutProps> = ({ children, navItems, title }) => {
  const { t } = useTranslation()
  const { user } = useAuth()
  const { mutate: logout } = useLogout()
  const [sidebarOpen, setSidebarOpen] = useState(true)
  const [languageOpen, setLanguageOpen] = useState(false)
  const location = useLocation()
  const { i18n } = useTranslation()

  const toggleLanguage = (lang: string) => {
    i18n.changeLanguage(lang)
    localStorage.setItem('language', lang)
    setLanguageOpen(false)
  }

  return (
    <div className="min-h-screen bg-bg-page">
      {/* Top Navigation */}
      <nav className="sticky top-0 z-40 bg-bg-surface border-b border-border">
        <div className="container-custom flex items-center justify-between py-4">
          <div className="flex items-center gap-4">
            <button
              onClick={() => setSidebarOpen(!sidebarOpen)}
              className="lg:hidden p-2 hover:bg-bg-page rounded"
            >
              ☰
            </button>
            <Link to={`/${user?.role}`} className="text-xl font-bold text-brand-700">
              AGENTTRUST
            </Link>
          </div>

          <div className="flex items-center gap-4">
            <div className="relative">
              <button
                onClick={() => setLanguageOpen(!languageOpen)}
                className="px-3 py-2 text-sm border border-border rounded-lg hover:bg-bg-page"
              >
                {i18n.language === 'en' ? 'EN' : 'HI'}
              </button>
              {languageOpen && (
                <div className="absolute right-0 mt-2 w-24 bg-bg-surface border border-border rounded-lg shadow-lg z-50">
                  <button
                    onClick={() => toggleLanguage('en')}
                    className="block w-full text-left px-4 py-2 hover:bg-bg-page text-sm"
                  >
                    English
                  </button>
                  <button
                    onClick={() => toggleLanguage('hi')}
                    className="block w-full text-left px-4 py-2 hover:bg-bg-page text-sm border-t border-border"
                  >
                    हिन्दी
                  </button>
                </div>
              )}
            </div>

            <div className="flex items-center gap-2 pl-4 border-l border-border">
              <div>
                <p className="text-sm font-medium text-text-primary">{user?.name}</p>
                <p className="text-xs text-text-muted capitalize">{user?.role}</p>
              </div>
              <Button variant="secondary" size="sm" onClick={() => logout()}>
                {t('common.logout')}
              </Button>
            </div>
          </div>
        </div>
      </nav>

      <div className="flex">
        {/* Sidebar */}
        <aside
          className={`${
            sidebarOpen ? 'w-64' : 'w-0'
          } hidden lg:block bg-bg-surface border-r border-border transition-all duration-300 overflow-hidden`}
        >
          <nav className="p-6 space-y-2">
            {navItems.map((item) => (
              <Link
                key={item.href}
                to={item.href}
                className={`flex items-center gap-3 px-4 py-3 rounded-lg transition-colors ${
                  location.pathname === item.href
                    ? 'bg-brand-100 text-brand-700 font-medium'
                    : 'text-text-secondary hover:bg-bg-page'
                }`}
              >
                {item.icon && <span className="text-lg">{item.icon}</span>}
                <span>{item.label}</span>
              </Link>
            ))}
          </nav>
        </aside>

        {/* Main Content */}
        <main className="flex-1 overflow-auto">
          <div className="container-custom py-8">
            {title && (
              <div className="mb-8">
                <h1 className="text-3xl font-bold text-text-primary">{title}</h1>
              </div>
            )}
            {children}
          </div>
        </main>
      </div>
    </div>
  )
}

export default AppLayout
