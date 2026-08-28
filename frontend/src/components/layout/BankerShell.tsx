import React from 'react';
import { NavLink, Outlet, useLocation, useNavigate } from 'react-router-dom';
import { useAuth } from '../../context/AuthContext';

export const BankerShell: React.FC = () => {
  const location = useLocation();
  const navigate = useNavigate();
  const { user, logout } = useAuth();

  const handleLogout = () => {
    logout();
    navigate('/');
  };

  const navItems = [
    { group: 'Overview', label: 'Command Center', path: '/banker/dashboard', icon: 'dashboard' },
    { group: 'Overview', label: 'Portfolio', path: '/banker/portfolio', icon: 'account_balance_wallet' },
    { group: 'Overview', label: 'Customer Records', path: '/banker/customers', icon: 'group' },
    { group: 'Overview', label: 'Transactions', path: '/banker/transactions', icon: 'receipt_long' },
    
    { group: 'Operations', label: 'Loan Approvals', path: '/banker/loan-approvals', icon: 'fact_check' },
    { group: 'Operations', label: 'Risk Reports', path: '/banker/risk-reports', icon: 'analytics' },
    { group: 'Operations', label: 'Underwriting Workspace', path: '/banker/underwriting', icon: 'account_balance' },
    { group: 'Operations', label: 'Decision Support AI', path: '/banker/underwriting/decision-support', icon: 'psychology' },
    { group: 'Operations', label: 'Document Intelligence', path: '/banker/document-intelligence', icon: 'find_in_page' },
    { group: 'Operations', label: 'Immutable Audit Trail', path: '/banker/audit-trail', icon: 'gavel' },
    { group: 'Operations', label: 'Governance & Controls', path: '/banker/governance', icon: 'admin_panel_settings' },
  ];

  return (
    <div className="min-h-screen flex bg-background text-on-surface">
      {/* Fixed 280px Deep Slate Sidebar */}
      <aside className="w-[280px] bg-[#0F172A] text-white flex flex-col fixed inset-y-0 left-0 z-30 border-r border-slate-800">
        {/* Brand Header */}
        <div className="h-16 px-6 flex items-center justify-between border-b border-slate-800">
          <div className="flex items-center gap-3">
            <div className="w-8 h-8 rounded bg-[#2563EB] flex items-center justify-center font-bold text-white shadow-sm">
              AT
            </div>
            <div>
              <div className="font-semibold text-sm tracking-tight font-display text-white">AgentTrust OS</div>
              <div className="text-[10px] text-slate-400 uppercase tracking-widest font-mono">Banker Portal</div>
            </div>
          </div>
          <span className="w-2 h-2 rounded-full bg-emerald-500 animate-pulse" title="System Operational"></span>
        </div>

        {/* System Role Indicator */}
        <div className="mx-4 my-4 p-3 bg-slate-900/90 rounded-lg border border-slate-800 flex items-center justify-between">
          <div className="flex items-center gap-2.5">
            <span className="material-symbols-outlined text-sm text-[#2563EB]">verified</span>
            <div>
              <div className="text-xs font-semibold text-slate-200">{user?.name || 'Vikram Singh'}</div>
              <div className="text-[11px] text-slate-400">{user?.title || 'Lead Underwriter'}</div>
            </div>
          </div>
          <span className="text-[10px] bg-emerald-950 text-emerald-400 font-mono px-2 py-0.5 rounded border border-emerald-800">
            L3-AUTH
          </span>
        </div>

        {/* Navigation Items */}
        <nav className="flex-1 px-3 py-2 space-y-4 overflow-y-auto custom-scrollbar">
          {['Overview', 'Operations'].map((groupName) => (
            <div key={groupName} className="space-y-1">
              <div className="px-3 py-1 text-[10px] uppercase font-semibold text-slate-400 tracking-wider">
                {groupName}
              </div>
              {navItems.filter(i => i.group === groupName).map((item) => {
                const isActive = location.pathname === item.path;
                return (
                  <NavLink
                    key={item.path}
                    to={item.path}
                    className={({ isActive: linkActive }) =>
                      `flex items-center gap-3 px-3 py-2.5 rounded-md text-sm font-medium transition-all ${
                        linkActive || isActive
                          ? 'bg-[#2563EB]/15 text-white border-l-4 border-[#2563EB] font-semibold'
                          : 'text-slate-300 hover:bg-slate-800/60 hover:text-white'
                      }`
                    }
                  >
                    <span className={`material-symbols-outlined text-lg ${isActive ? 'text-[#2563EB]' : 'text-slate-400'}`}>
                      {item.icon}
                    </span>
                    <span className="truncate">{item.label}</span>
                  </NavLink>
                );
              })}
            </div>
          ))}
        </nav>

        {/* Footer info & Logout */}
        <div className="p-4 border-t border-slate-800 text-xs text-slate-400 space-y-2">
          <div className="flex items-center justify-between">
            <span>Audit Engine:</span>
            <span className="font-mono text-[11px] text-emerald-400">SYNCED</span>
          </div>
          <button
            onClick={handleLogout}
            className="w-full mt-2 block text-center text-xs py-2 px-3 rounded bg-slate-900 hover:bg-rose-950 hover:text-rose-400 text-slate-300 transition-colors border border-slate-800 font-medium"
          >
            Sign Out (Lock Session)
          </button>
        </div>
      </aside>

      {/* Main Content Area */}
      <div className="pl-[280px] flex-1 flex flex-col min-w-0">
        {/* Top Navigation Bar */}
        <header className="h-16 bg-surface border-b border-border-subtle px-8 flex items-center justify-between sticky top-0 z-20">
          <div className="flex items-center gap-4">
            <span className="text-xs text-on-surface-variant font-medium">Banker Command Workspace</span>
            <span className="text-border-subtle">|</span>
            <div className="flex items-center gap-2 bg-surface-muted px-3 py-1 rounded-full text-xs text-on-surface-variant">
              <span className="w-2 h-2 rounded-full bg-emerald-500"></span>
              <span>Audit Chain Active: 0x8F9...A3C</span>
            </div>
          </div>

          <div className="flex items-center gap-4">
            <div className="relative">
              <span className="material-symbols-outlined absolute left-3 top-2.5 text-slate-400 text-sm">search</span>
              <input
                type="text"
                placeholder="Global Search (Ctrl + K)"
                className="pl-9 pr-4 py-1.5 bg-surface-bright border border-border-subtle rounded-md text-xs w-64 focus:outline-none focus:border-[#2563EB]"
              />
            </div>

            <button className="relative p-2 rounded-md hover:bg-surface-muted text-on-surface-variant">
              <span className="material-symbols-outlined text-lg">notifications</span>
              <span className="absolute top-1.5 right-1.5 w-2 h-2 rounded-full bg-rose-500"></span>
            </button>

            <div className="flex items-center gap-2 pl-2 border-l border-border-subtle">
              <div className="w-8 h-8 rounded-full bg-slate-800 text-white flex items-center justify-center font-semibold text-xs">
                VS
              </div>
              <div className="text-left hidden lg:block">
                <div className="text-xs font-semibold text-on-surface">{user?.name || 'Vikram Singh'}</div>
                <div className="text-[10px] text-on-surface-variant">Lead Banker</div>
              </div>
            </div>
          </div>
        </header>

        {/* Page Content */}
        <main className="flex-1 p-8 max-w-[1440px] w-full mx-auto">
          <Outlet />
        </main>
      </div>
    </div>
  );
};
