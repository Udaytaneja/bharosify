import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { AuthProvider } from './context/AuthContext';
import { ProtectedRoute } from './components/common/ProtectedRoute';

import { RoleSelectionPage } from './pages/auth/RoleSelectionPage';
import { BankerLoginPage } from './pages/auth/BankerLoginPage';
import { ApplicantLoginPage } from './pages/auth/ApplicantLoginPage';

import { BankerShell } from './components/layout/BankerShell';
import { BankerDashboardPage } from './pages/banker/BankerDashboardPage';
import { UnderwritingWorkspacePage } from './pages/banker/UnderwritingWorkspacePage';
import { DecisionSupportPage } from './pages/banker/DecisionSupportPage';
import { DocumentIntelligencePage } from './pages/banker/DocumentIntelligencePage';
import { AuditTrailPage } from './pages/banker/AuditTrailPage';
import { GovernancePage } from './pages/banker/GovernancePage';
import {
  BankerPortfolioPage,
  BankerCustomersPage,
  BankerTransactionsPage,
  BankerLoanApprovalsPage,
  BankerRiskReportsPage
} from './pages/banker/BankerSecondaryPages';

import { ApplicantShell } from './components/layout/ApplicantShell';
import { UserDashboardPage } from './pages/applicant/UserDashboardPage';
import { MyApplicationsPage } from './pages/applicant/MyApplicationsPage';
import { LoansRepaymentsPage } from './pages/applicant/LoansRepaymentsPage';
import { FinancialHealthPage } from './pages/applicant/FinancialHealthPage';
import { DocumentCenterPage } from './pages/applicant/DocumentCenterPage';
import { TrustSecurityPage } from './pages/applicant/TrustSecurityPage';
import {
  ApplicantNotificationsPage,
  ApplicantSettingsPage
} from './pages/applicant/ApplicantSecondaryPages';

export function App() {
  return (
    <AuthProvider>
      <Router>
        <Routes>
          {/* Public Auth Routes */}
          <Route path="/" element={<RoleSelectionPage />} />
          <Route path="/role-selection" element={<RoleSelectionPage />} />
          <Route path="/login/banker" element={<BankerLoginPage />} />
          <Route path="/login/applicant" element={<ApplicantLoginPage />} />

          {/* Protected Banker Workspace */}
          <Route
            path="/banker"
            element={
              <ProtectedRoute allowedRole="banker">
                <BankerShell />
              </ProtectedRoute>
            }
          >
            <Route index element={<Navigate to="/banker/dashboard" replace />} />
            <Route path="dashboard" element={<BankerDashboardPage />} />
            <Route path="portfolio" element={<BankerPortfolioPage />} />
            <Route path="customers" element={<BankerCustomersPage />} />
            <Route path="transactions" element={<BankerTransactionsPage />} />
            <Route path="loan-approvals" element={<BankerLoanApprovalsPage />} />
            <Route path="risk-reports" element={<BankerRiskReportsPage />} />
            <Route path="underwriting" element={<UnderwritingWorkspacePage />} />
            <Route path="underwriting/decision-support" element={<DecisionSupportPage />} />
            <Route path="document-intelligence" element={<DocumentIntelligencePage />} />
            <Route path="audit-trail" element={<AuditTrailPage />} />
            <Route path="governance" element={<GovernancePage />} />
          </Route>

          {/* Protected Applicant Workspace */}
          <Route
            path="/applicant"
            element={
              <ProtectedRoute allowedRole="applicant">
                <ApplicantShell />
              </ProtectedRoute>
            }
          >
            <Route index element={<Navigate to="/applicant/dashboard" replace />} />
            <Route path="dashboard" element={<UserDashboardPage />} />
            <Route path="applications" element={<MyApplicationsPage />} />
            <Route path="loans" element={<LoansRepaymentsPage />} />
            <Route path="financial-health" element={<FinancialHealthPage />} />
            <Route path="documents" element={<DocumentCenterPage />} />
            <Route path="trust-security" element={<TrustSecurityPage />} />
            <Route path="notifications" element={<ApplicantNotificationsPage />} />
            <Route path="settings" element={<ApplicantSettingsPage />} />
          </Route>

          {/* Fallback */}
          <Route path="*" element={<Navigate to="/" replace />} />
        </Routes>
      </Router>
    </AuthProvider>
  );
}

export default App;
