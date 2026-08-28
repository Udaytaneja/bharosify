import React from 'react';
import { NavLink, Outlet, useLocation, useNavigate } from 'react-router-dom';
import { useAuth } from '../../context/AuthContext';

export const ApplicantShell: React.FC = () => {
  const location = useLocation();
  const navigate = useNavigate();
  const { user, logout } = useAuth();

  const handleLogout = () => {
    logout();
    navigate('/');
  };

  const navItems = [
    { label: 'Overview Dashboard', path: '/applicant/dashboard', icon: 'dashboard' },
    { label: 'My Applications', path: '/applicant/applications', icon: 'description' },
    { label: 'Loans & Repayments', path: '/applicant/loans', icon: 'payments' },
    { label: 'Financial Health', path: '/applicant/financial-health', icon: 'analytics' },
    { label: 'Document Center', path: '/applicant/documents', icon: 'folder_open' },
    { label: 'Trust & Security', path: '/applicant/trust-security', icon: 'shield' },
    { label: 'Notifications', path: '/applicant/notifications', icon: 'notifications' },
    { label: 'Settings', path: '/applicant/settings', icon: 'settings' },
  ];

  return (
    <div className="min-h-screen flex bg-background text-on-surface">
      {/* Sidebar for Applicant */}
      <aside className="w-[260px] bg-surface border-r border-border-subtle flex flex-col fixed inset-y-0 left-0 z-30">
        {/* Brand Header */}
        <div className="h-16 px-6 flex items-center justify-between border-b border-border-subtle">
          <div className="flex items-center gap-3">
            <div className="w-8 h-8 rounded bg-[#2563EB] flex items-center justify-center font-bold text-white shadow-sm">
              AT
            </div>
            <div>
              <div className="font-semibold text-sm tracking-tight font-display text-on-surface">AgentTrust OS</div>
              <div className="text-[10px] text-on-surface-variant uppercase tracking-widest font-mono">Applicant Portal</div>
            </div>
          </div>
        </div>

        {/* User Account Info */}
        <div className="p-4 m-3 bg-surface-muted rounded-xl border border-border-subtle">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 rounded-full bg-[#2563EB] text-white flex items-center justify-center font-semibold text-sm">
              AM
            </div>
            <div>
              <div className="text-xs font-semibold text-on-surface">{user?.name || 'Alex Mercer'}</div>
              <div className="text-[11px] text-on-surface-variant">ID: {user?.id || 'APP-8942-NY'}</div>
            </div>
          </div>
          <div className="mt-3 pt-2 border-t border-border-subtle flex items-center justify-between text-[11px]">
            <span className="text-on-surface-variant">Account Status:</span>
            <span className="text-emerald-700 font-semibold bg-emerald-50 px-2 py-0.5 rounded border border-emerald-200">VERIFIED</span>
          </div>
        </div>

        {/* Navigation */}
        <nav className="flex-1 px-3 py-2 space-y-1 overflow-y-auto custom-scrollbar">
          <div className="px-3 py-2 text-[10px] uppercase font-semibold text-on-surface-variant tracking-wider">
            Applicant Navigation
          </div>
          {navItems.map((item) => {
            const isActive = location.pathname === item.path;
            return (
              <NavLink
                key={item.path}
                to={item.path}
                className={({ isActive: linkActive }) =>
                  `flex items-center gap-3 px-3 py-2.5 rounded-md text-sm font-medium transition-all ${
                    linkActive || isActive
                      ? 'bg-[#2563EB]/10 text-[#2563EB] border-l-4 border-[#2563EB] font-semibold'
                      : 'text-on-surface-variant hover:bg-surface-muted hover:text-on-surface'
                  }`
                }
              >
                <span className={`material-symbols-outlined text-lg ${isActive ? 'text-[#2563EB]' : 'text-on-surface-variant'}`}>
                  {item.icon}
                </span>
                <span className="truncate">{item.label}</span>
              </NavLink>
            );
          })}
        </nav>

        {/* Exit / Logout */}
        <div className="p-4 border-t border-border-subtle">
          <button
            onClick={handleLogout}
            className="w-full block text-center text-xs py-2 px-3 rounded border border-border-subtle bg-surface hover:bg-rose-50 hover:text-rose-600 text-on-surface font-medium transition-colors"
          >
            Sign Out
          </button>
        </div>
      </aside>

      {/* Main Content Container */}
      <div className="pl-[260px] flex-1 flex flex-col min-w-0">
        {/* Header */}
        <header className="h-16 bg-surface border-b border-border-subtle px-8 flex items-center justify-between sticky top-0 z-20">
          <div className="flex items-center gap-3">
            <span className="text-xs font-medium text-on-surface-variant">Commercial Credit & Loan Governance</span>
            <span className="text-emerald-700 bg-emerald-50 border border-emerald-200 text-[11px] font-medium px-2.5 py-0.5 rounded-full flex items-center gap-1">
              <span className="w-1.5 h-1.5 rounded-full bg-emerald-500"></span>
              Secure Session Active
            </span>
          </div>

          <div className="flex items-center gap-4">
            <button className="flex items-center gap-1.5 text-xs text-secondary font-medium bg-secondary/5 px-3 py-1.5 rounded border border-secondary/20 hover:bg-secondary/10">
              <span className="material-symbols-outlined text-sm">help_outline</span>
              <span>Support & Disclosure</span>
            </button>
            <div className="flex items-center gap-2 pl-3 border-l border-border-subtle">
              <span className="text-xs font-medium text-on-surface">{user?.name || 'Alex Mercer'} (CFO)</span>
            </div>
          </div>
        </header>

        {/* Main Content */}
        <main className="flex-1 p-8 max-w-[1440px] w-full mx-auto">
          <Outlet />
        </main>
      </div>
    </div>
  );
};
