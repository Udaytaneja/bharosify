import { lazy, Suspense } from 'react'
import { Routes, Route } from 'react-router-dom'
import ProtectedRoute from '@/components/ProtectedRoute'
import Loading from '@/components/Loading'

// Pages
const LandingPage = lazy(() => import('@/pages/LandingPage'))
const RoleSelectionPage = lazy(() => import('@/pages/RoleSelectionPage'))
const LoginPage = lazy(() => import('@/pages/auth/LoginPage'))
const RegisterPage = lazy(() => import('@/pages/auth/RegisterPage'))

// User Pages
const UserDashboard = lazy(() => import('@/pages/user/Dashboard'))
const UserFinancialHealth = lazy(() => import('@/pages/user/FinancialHealth'))
const UserTrust = lazy(() => import('@/pages/user/Trust'))
const UserTransactions = lazy(() => import('@/pages/user/Transactions'))
const UserGoals = lazy(() => import('@/pages/user/Goals'))
const UserApplications = lazy(() => import('@/pages/user/Applications'))
const UserLoans = lazy(() => import('@/pages/user/Loans'))
const UserRepayments = lazy(() => import('@/pages/user/Repayments'))
const UserAgents = lazy(() => import('@/pages/user/Agents'))
const UserNotifications = lazy(() => import('@/pages/user/Notifications'))
const UserSettings = lazy(() => import('@/pages/user/Settings'))
const UserAI = lazy(() => import('@/pages/user/AIAssistant'))

// Banker Pages
const BankerDashboard = lazy(() => import('@/pages/banker/Dashboard'))
const BankerCustomers = lazy(() => import('@/pages/banker/Customers'))
const BankerApplications = lazy(() => import('@/pages/banker/Applications'))
const BankerUnderwriting = lazy(() => import('@/pages/banker/Underwriting'))
const BankerLoans = lazy(() => import('@/pages/banker/Loans'))
const BankerRisk = lazy(() => import('@/pages/banker/Risk'))
const BankerFraud = lazy(() => import('@/pages/banker/Fraud'))
const BankerNotifications = lazy(() => import('@/pages/banker/Notifications'))
const BankerSettings = lazy(() => import('@/pages/banker/Settings'))

// Error Pages
const NotFound = lazy(() => import('@/pages/NotFound'))
const Unauthorized = lazy(() => import('@/pages/Unauthorized'))

const RouteLoader = () => <Loading fullScreen />

export const router = (
  <Routes>
    {/* Public Routes */}
    <Route index element={<Suspense fallback={<RouteLoader />}><LandingPage /></Suspense>} />
    <Route path="role-selection" element={<Suspense fallback={<RouteLoader />}><RoleSelectionPage /></Suspense>} />
    <Route path="login" element={<Suspense fallback={<RouteLoader />}><LoginPage /></Suspense>} />
    <Route path="register" element={<Suspense fallback={<RouteLoader />}><RegisterPage /></Suspense>} />

    {/* User Routes */}
    <Route path="user" element={<ProtectedRoute allowedRoles={['user']} />}>
      <Route index element={<Suspense fallback={<RouteLoader />}><UserDashboard /></Suspense>} />
      <Route path="dashboard" element={<Suspense fallback={<RouteLoader />}><UserDashboard /></Suspense>} />
      <Route path="financial-health" element={<Suspense fallback={<RouteLoader />}><UserFinancialHealth /></Suspense>} />
      <Route path="trust" element={<Suspense fallback={<RouteLoader />}><UserTrust /></Suspense>} />
      <Route path="transactions" element={<Suspense fallback={<RouteLoader />}><UserTransactions /></Suspense>} />
      <Route path="goals" element={<Suspense fallback={<RouteLoader />}><UserGoals /></Suspense>} />
      <Route path="applications" element={<Suspense fallback={<RouteLoader />}><UserApplications /></Suspense>} />
      <Route path="loans" element={<Suspense fallback={<RouteLoader />}><UserLoans /></Suspense>} />
      <Route path="repayments" element={<Suspense fallback={<RouteLoader />}><UserRepayments /></Suspense>} />
      <Route path="repayment" element={<Suspense fallback={<RouteLoader />}><UserRepayments /></Suspense>} />
      <Route path="agents" element={<Suspense fallback={<RouteLoader />}><UserAgents /></Suspense>} />
      <Route path="ai" element={<Suspense fallback={<RouteLoader />}><UserAI /></Suspense>} />
      <Route path="ai-assistant" element={<Suspense fallback={<RouteLoader />}><UserAI /></Suspense>} />
      <Route path="notifications" element={<Suspense fallback={<RouteLoader />}><UserNotifications /></Suspense>} />
      <Route path="settings" element={<Suspense fallback={<RouteLoader />}><UserSettings /></Suspense>} />
    </Route>

    {/* Banker Routes */}
    <Route path="banker" element={<ProtectedRoute allowedRoles={['banker']} />}>
      <Route index element={<Suspense fallback={<RouteLoader />}><BankerDashboard /></Suspense>} />
      <Route path="dashboard" element={<Suspense fallback={<RouteLoader />}><BankerDashboard /></Suspense>} />
      <Route path="customers" element={<Suspense fallback={<RouteLoader />}><BankerCustomers /></Suspense>} />
      <Route path="applications" element={<Suspense fallback={<RouteLoader />}><BankerApplications /></Suspense>} />
      <Route path="underwriting" element={<Suspense fallback={<RouteLoader />}><BankerUnderwriting /></Suspense>} />
      <Route path="loans" element={<Suspense fallback={<RouteLoader />}><BankerLoans /></Suspense>} />
      <Route path="risk" element={<Suspense fallback={<RouteLoader />}><BankerRisk /></Suspense>} />
      <Route path="fraud" element={<Suspense fallback={<RouteLoader />}><BankerFraud /></Suspense>} />
      <Route path="notifications" element={<Suspense fallback={<RouteLoader />}><BankerNotifications /></Suspense>} />
      <Route path="settings" element={<Suspense fallback={<RouteLoader />}><BankerSettings /></Suspense>} />
    </Route>

    {/* Error Routes */}
    <Route path="unauthorized" element={<Suspense fallback={<RouteLoader />}><Unauthorized /></Suspense>} />
    <Route path="*" element={<Suspense fallback={<RouteLoader />}><NotFound /></Suspense>} />
  </Routes>
)
