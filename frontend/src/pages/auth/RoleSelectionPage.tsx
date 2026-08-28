import React from 'react';
import { useNavigate } from 'react-router-dom';
import { ShaderCanvas } from '../../components/common/ShaderCanvas';

export const RoleSelectionPage: React.FC = () => {
  const navigate = useNavigate();

  return (
    <div className="relative min-h-screen w-full flex items-center justify-center bg-surface overflow-hidden p-4">
      {/* Background WebGL Shader */}
      <ShaderCanvas className="absolute inset-0 w-full h-full z-0 opacity-40" />

      {/* Main Container */}
      <div className="relative z-10 w-full max-w-2xl flex flex-col gap-6 items-center my-auto">
        {/* Session Status Pill */}
        <div className="flex items-center gap-2 bg-surface-container-high/80 backdrop-blur-md rounded-full px-4 py-2 border border-border-subtle w-fit mx-auto">
          <div className="w-2 h-2 rounded-full bg-emerald-500 animate-pulse"></div>
          <span className="font-label-md text-xs text-on-surface-variant uppercase tracking-widest">
            Session Secure & Encrypted
          </span>
        </div>

        {/* Card Box */}
        <div className="bg-surface rounded-xl border border-border-subtle shadow-sm w-full p-6 sm:p-8 flex flex-col gap-6">
          <div className="flex flex-col items-center text-center gap-4">
            <div className="w-16 h-16 rounded-xl bg-[#0F172A] text-white flex items-center justify-center font-bold text-2xl shadow-md border border-slate-700">
              AT
            </div>
            <div className="flex flex-col gap-1">
              <h1 className="font-display text-2xl sm:text-3xl text-on-surface tracking-tight font-bold">
                AgentTrust OS
              </h1>
              <p className="font-body-md text-sm sm:text-base text-on-surface-variant max-w-md mx-auto">
                Institutional-grade financial AI governance infrastructure. Select your operational role to proceed securely.
              </p>
            </div>
          </div>

          {/* Role Selection Options */}
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4 w-full">
            {/* Banker Button */}
            <button
              onClick={() => navigate('/login/banker')}
              className="group flex flex-col gap-4 p-5 bg-surface-container hover:bg-surface-container-high transition-colors duration-150 rounded-xl border border-border-subtle text-left focus:outline-none focus:ring-2 focus:ring-primary"
            >
              <div className="flex items-center justify-between w-full">
                <div className="bg-surface text-on-surface p-2.5 rounded-lg border border-border-subtle group-hover:bg-primary group-hover:text-white transition-colors">
                  <span className="material-symbols-outlined text-2xl">account_balance</span>
                </div>
                <span className="material-symbols-outlined text-on-surface-variant group-hover:text-primary opacity-0 -translate-x-2 group-hover:opacity-100 group-hover:translate-x-0 transition-all duration-150">
                  arrow_forward
                </span>
              </div>
              <div className="flex flex-col gap-1">
                <span className="font-semibold text-base text-on-surface">Sign in as Banker</span>
                <span className="text-xs text-on-surface-variant leading-relaxed">
                  Access precision auditing, multi-entity oversight, loan underwriting, and institutional risk controls.
                </span>
              </div>
            </button>

            {/* Applicant Button */}
            <button
              onClick={() => navigate('/login/applicant')}
              className="group flex flex-col gap-4 p-5 bg-surface-container hover:bg-surface-container-high transition-colors duration-150 rounded-xl border border-border-subtle text-left focus:outline-none focus:ring-2 focus:ring-secondary"
            >
              <div className="flex items-center justify-between w-full">
                <div className="bg-surface text-on-surface p-2.5 rounded-lg border border-border-subtle group-hover:bg-[#2563EB] group-hover:text-white transition-colors">
                  <span className="material-symbols-outlined text-2xl">person</span>
                </div>
                <span className="material-symbols-outlined text-on-surface-variant group-hover:text-[#2563EB] opacity-0 -translate-x-2 group-hover:opacity-100 group-hover:translate-x-0 transition-all duration-150">
                  arrow_forward
                </span>
              </div>
              <div className="flex flex-col gap-1">
                <span className="font-semibold text-base text-on-surface">Sign in as Applicant</span>
                <span className="text-xs text-on-surface-variant leading-relaxed">
                  Manage your secure loan application pipeline, upload verified financial documents, and track approval status.
                </span>
              </div>
            </button>
          </div>
        </div>

        {/* AES 256 Security Footer */}
        <div className="flex items-center gap-2 text-on-surface-variant/70 bg-surface-container/60 px-3 py-1.5 rounded-full border border-border-subtle text-xs">
          <span className="material-symbols-outlined text-sm text-emerald-600">lock</span>
          <span className="font-mono text-[11px] uppercase tracking-wider">AES-256 Encrypted Connection • FIPS 140-3 Verified</span>
        </div>
      </div>
    </div>
  );
};
