import React, { useState } from 'react'
import { Link, useLocation } from 'react-router-dom'
import { useTranslation } from 'react-i18next'
import { useLogout, useAuth } from '@/hooks'
import Button from '@/components/Button'

export interface NavItem {
  label: string
  href: string
  icon?: string
}

interface AppLayoutProps {
  children: React.ReactNode
  navItems?: NavItem[]
  title?: string
}

const AppLayout: React.FC<AppLayoutProps> = ({ children, navItems, title }) => {
  const { t, i18n } = useTranslation()
  const { user } = useAuth()
  const { mutate: logout } = useLogout()
  const [sidebarOpen, setSidebarOpen] = useState(true)
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false)
  const [languageOpen, setLanguageOpen] = useState(false)
  const location = useLocation()

  const toggleLanguage = (lang: string) => {
    i18n.changeLanguage(lang)
    localStorage.setItem('language', lang)
    setLanguageOpen(false)
  }

  const defaultUserNavItems: NavItem[] = [
    { label: t('nav.home'), href: '/user', icon: '🏠' },
    { label: t('nav.financialHealth'), href: '/user/financial-health', icon: '📊' },
    { label: t('nav.trust'), href: '/user/trust', icon: '🛡️' },
    { label: t('nav.transactions'), href: '/user/transactions', icon: '💳' },
    { label: t('nav.goals'), href: '/user/goals', icon: '🎯' },
    { label: t('nav.applications'), href: '/user/applications', icon: '📋' },
    { label: t('nav.loans'), href: '/user/loans', icon: '💰' },
    { label: t('nav.repayment'), href: '/user/repayments', icon: '📅' },
    { label: t('nav.agents'), href: '/user/agents', icon: '🤖' },
    { label: t('nav.aiAssistant'), href: '/user/ai-assistant', icon: '💬' },
    { label: t('nav.notifications'), href: '/user/notifications', icon: '🔔' },
    { label: t('nav.settings'), href: '/user/settings', icon: '⚙️' },
  ]


  const defaultBankerNavItems: NavItem[] = [
    { label: t('nav.bankerDashboard'), href: '/banker', icon: '📊' },
    { label: t('nav.customers'), href: '/banker/customers', icon: '👥' },
    { label: t('nav.applications'), href: '/banker/applications', icon: '📋' },
    { label: t('nav.underwriting'), href: '/banker/underwriting', icon: '🔍' },
    { label: t('nav.loans'), href: '/banker/loans', icon: '💰' },
    { label: t('nav.risk'), href: '/banker/risk', icon: '⚠️' },
    { label: t('nav.fraud'), href: '/banker/fraud', icon: '🚨' },
    { label: t('nav.notifications'), href: '/banker/notifications', icon: '🔔' },
    { label: t('nav.settings'), href: '/banker/settings', icon: '⚙️' },
  ]

  const itemsToRender =
    navItems && navItems.length > 5
      ? navItems
      : user?.role === 'banker'
      ? defaultBankerNavItems
      : defaultUserNavItems

  return (
    <div className="min-h-screen bg-bg-page flex flex-col">
      {/* Top Navigation */}
      <nav className="sticky top-0 z-40 bg-bg-surface border-b border-border shadow-sm">
        <div className="container-custom flex items-center justify-between py-3">
          <div className="flex items-center gap-3">
            <button
              onClick={() => setSidebarOpen(!sidebarOpen)}
              className="hidden lg:flex p-2 hover:bg-bg-page rounded-lg text-text-secondary transition-colors"
              title="Toggle sidebar"
              aria-label="Toggle sidebar"
            >
              <span className="text-xl">☰</span>
            </button>
            <button
              onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
              className="lg:hidden p-2 hover:bg-bg-page rounded-lg text-text-secondary transition-colors"
              title="Toggle menu"
              aria-label="Toggle menu"
            >
              <span className="text-xl">☰</span>
            </button>
            <Link to={`/${user?.role}`} className="flex items-center gap-2">
              <div className="w-8 h-8 rounded-lg bg-brand-700 text-white font-bold flex items-center justify-center text-sm shadow-sm">
                AT
              </div>
              <span className="text-xl font-extrabold text-brand-700 tracking-tight">
                AGENTTRUST <span className="text-xs uppercase px-1.5 py-0.5 rounded bg-brand-100 text-brand-700 font-semibold">OS</span>
              </span>
            </Link>
          </div>

          <div className="flex items-center gap-3">
            <div className="relative">
              <button
                onClick={() => setLanguageOpen(!languageOpen)}
                className="flex items-center gap-1.5 px-3 py-1.5 text-xs font-semibold border border-border rounded-lg hover:bg-bg-page text-text-primary transition-colors"
              >
                <span>🌐</span>
                <span>{i18n.language === 'hi' ? 'हिन्दी' : 'English'}</span>
              </button>
              {languageOpen && (
                <div className="absolute right-0 mt-2 w-32 bg-bg-surface border border-border rounded-lg shadow-lg z-50 overflow-hidden">
                  <button
                    onClick={() => toggleLanguage('en')}
                    className={`block w-full text-left px-4 py-2 text-xs font-medium hover:bg-bg-page transition-colors ${
                      i18n.language === 'en' ? 'bg-brand-50 text-brand-700 font-semibold' : 'text-text-primary'
                    }`}
                  >
                    English
                  </button>
                  <button
                    onClick={() => toggleLanguage('hi')}
                    className={`block w-full text-left px-4 py-2 text-xs font-medium hover:bg-bg-page transition-colors border-t border-border ${
                      i18n.language === 'hi' ? 'bg-brand-50 text-brand-700 font-semibold' : 'text-text-primary'
                    }`}
                  >
                    हिन्दी
                  </button>
                </div>
              )}
            </div>

            <div className="flex items-center gap-3 pl-3 border-l border-border">
              <div className="hidden sm:block text-right">
                <p className="text-sm font-semibold text-text-primary leading-tight">{user?.name || 'User'}</p>
                <p className="text-xs text-text-muted capitalize">{user?.role || 'Guest'}</p>
              </div>
              <Button variant="secondary" size="sm" onClick={() => logout()}>
                {t('common.logout')}
              </Button>
            </div>
          </div>
        </div>
      </nav>

      <div className="flex flex-1">
        {/* Desktop Sidebar */}
        <aside
          className={`${
            sidebarOpen ? 'w-64' : 'w-16'
          } hidden lg:block bg-bg-surface border-r border-border transition-all duration-300 overflow-y-auto`}
        >
          <nav className="p-3 space-y-1">
            {itemsToRender.map((item) => {
              const isActive = location.pathname === item.href
              return (
                <Link
                  key={item.href}
                  to={item.href}
                  title={item.label}
                  className={`flex items-center gap-3 px-3.5 py-2.5 rounded-lg transition-colors text-sm font-medium ${
                    isActive
                      ? 'bg-brand-100 text-brand-700 font-semibold shadow-xs'
                      : 'text-text-secondary hover:bg-bg-page hover:text-text-primary'
                  }`}
                >
                  <span className="text-base flex-shrink-0">{item.icon || '📌'}</span>
                  {sidebarOpen && <span className="truncate">{item.label}</span>}
                </Link>
              )
            })}
          </nav>
        </aside>

        {/* Mobile Drawer */}
        {mobileMenuOpen && (
          <div className="lg:hidden fixed inset-0 z-50 flex">
            <div
              className="fixed inset-0 bg-black/40 backdrop-blur-xs"
              onClick={() => setMobileMenuOpen(false)}
            />
            <div className="relative w-64 max-w-xs bg-bg-surface h-full shadow-xl flex flex-col z-10">
              <div className="p-4 border-b border-border flex items-center justify-between">
                <span className="font-bold text-brand-700">Navigation</span>
                <button
                  onClick={() => setMobileMenuOpen(false)}
                  className="p-1 text-text-secondary hover:text-text-primary"
                >
                  ✕
                </button>
              </div>
              <nav className="p-3 space-y-1 flex-1 overflow-y-auto">
                {itemsToRender.map((item) => {
                  const isActive = location.pathname === item.href
                  return (
                    <Link
                      key={item.href}
                      to={item.href}
                      onClick={() => setMobileMenuOpen(false)}
                      className={`flex items-center gap-3 px-3.5 py-2.5 rounded-lg transition-colors text-sm font-medium ${
                        isActive
                          ? 'bg-brand-100 text-brand-700 font-semibold'
                          : 'text-text-secondary hover:bg-bg-page hover:text-text-primary'
                      }`}
                    >
                      <span className="text-base flex-shrink-0">{item.icon || '📌'}</span>
                      <span className="truncate">{item.label}</span>
                    </Link>
                  )
                })}
              </nav>
            </div>
          </div>
        )}

        {/* Main Content */}
        <main className="flex-1 overflow-y-auto min-w-0">
          <div className="container-custom py-8">
            {title && (
              <div className="mb-6">
                <h1 className="text-2xl lg:text-3xl font-bold text-text-primary">{title}</h1>
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
