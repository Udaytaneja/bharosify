import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { FinancialService } from '../../services/financial.service';
import { LoanService } from '../../services/loan.service';
import { useAuth } from '../../context/AuthContext';
import type { FinancialHealthProfile, ActiveLoanFacility } from '../../types';

export const UserDashboardPage: React.FC = () => {
  const navigate = useNavigate();
  const { user } = useAuth();
  const [viewVariant, setViewVariant] = useState<'polished' | 'institutional'>('polished');
  const [healthProfile, setHealthProfile] = useState<FinancialHealthProfile | null>(null);
  const [loanFacility, setLoanFacility] = useState<ActiveLoanFacility | null>(null);

  useEffect(() => {
    FinancialService.getFinancialHealthProfile().then(setHealthProfile);
    LoanService.getActiveFacility().then(setLoanFacility);
  }, []);

  return (
    <div className="flex flex-col w-full relative pb-8 space-y-8">
      {/* Header Greeting & View Variant Toggle */}
      <section className="flex flex-col justify-start pt-2">
        <div className="flex flex-col md:flex-row items-start md:items-end justify-between w-full gap-4">
          <div className="flex flex-col gap-1 max-w-2xl">
            <div className="text-xs font-semibold text-outline-variant uppercase tracking-widest">
              Overview • Applicant Portal
            </div>
            <h1 className="text-3xl lg:text-4xl font-bold font-display text-on-surface tracking-tight">
              Good morning, {user?.name || 'Applicant'}
            </h1>
            <p className="text-sm lg:text-base text-on-surface-variant max-w-lg mt-0.5">
              Here is the latest update on your active credit facilities and loan application progress.
            </p>
          </div>

          <div className="flex items-center gap-3">
            {/* View Variant Toggle */}
            <div className="bg-surface-muted p-1 rounded-lg border border-border-subtle flex items-center gap-1 text-xs">
              <button
                onClick={() => setViewVariant('polished')}
                className={`px-3 py-1.5 rounded-md font-medium transition-all ${
                  viewVariant === 'polished' ? 'bg-surface text-primary shadow-xs font-semibold' : 'text-on-surface-variant hover:text-on-surface'
                }`}
              >
                Polished View
              </button>
              <button
                onClick={() => setViewVariant('institutional')}
                className={`px-3 py-1.5 rounded-md font-medium transition-all ${
                  viewVariant === 'institutional' ? 'bg-[#0F172A] text-white shadow-xs font-semibold' : 'text-on-surface-variant hover:text-on-surface'
                }`}
              >
                Institutional View
              </button>
            </div>

            <button className="flex items-center gap-2 px-4 py-2 bg-surface border border-border-subtle rounded-lg hover:bg-surface-muted transition-colors text-xs font-medium text-on-surface shadow-xs">
              <span className="material-symbols-outlined text-base text-on-surface-variant">support_agent</span>
              <span>Need Help?</span>
            </button>
          </div>
        </div>
      </section>

      {/* 2-Column Main Section */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-8">
        {/* Left 8 Cols: Current Application & Financial Metrics */}
        <section className="lg:col-span-8 flex flex-col gap-8">
          {/* Current Application Progress Card */}
          <div className="bg-surface rounded-xl p-6 sm:p-8 shadow-xs border border-border-subtle relative overflow-hidden space-y-6">
            <div className="flex items-start justify-between">
              <div className="flex items-center gap-4">
                <div className="w-10 h-10 rounded-lg bg-[#2563EB]/10 flex items-center justify-center text-[#2563EB]">
                  <span className="material-symbols-outlined text-xl">real_estate_agent</span>
                </div>
                <div>
                  <h2 className="text-lg font-bold font-headline-sm text-on-surface">Home Loan Application</h2>
                  <span className="text-xs text-on-surface-variant font-mono">Application ID: HL-2023-8942</span>
                </div>
              </div>

              <div className="bg-[#2563EB]/10 border border-[#2563EB]/20 px-3 py-1 rounded-full flex items-center gap-2">
                <div className="w-1.5 h-1.5 rounded-full bg-[#2563EB] animate-pulse"></div>
                <span className="text-xs font-semibold text-[#2563EB]">In Progress</span>
              </div>
            </div>

            {/* Stage Progress Bar */}
            <div className="relative pt-6 pb-2 px-2">
              <div className="absolute top-1/2 left-4 right-4 h-[3px] bg-border-subtle -translate-y-1/2 rounded-full overflow-hidden">
                <div className="h-full bg-[#2563EB] w-[50%] transition-all duration-1000 ease-out"></div>
              </div>

              <div className="flex justify-between relative z-10 text-center">
                {/* Stage 1 */}
                <div className="flex flex-col items-center gap-2">
                  <div className="w-6 h-6 rounded-full bg-[#2563EB] text-white flex items-center justify-center shadow-xs">
                    <span className="material-symbols-outlined text-xs">check</span>
                  </div>
                  <span className="text-[11px] font-medium text-on-surface">Submitted</span>
                </div>

                {/* Stage 2 */}
                <div className="flex flex-col items-center gap-2">
                  <div className="w-6 h-6 rounded-full bg-[#2563EB] text-white flex items-center justify-center shadow-xs">
                    <span className="material-symbols-outlined text-xs">check</span>
                  </div>
                  <span className="text-[11px] font-medium text-on-surface">Verified</span>
                </div>

                {/* Stage 3 (Active) */}
                <div className="flex flex-col items-center gap-2 relative">
                  <div className="absolute -top-7 left-1/2 -translate-x-1/2 bg-surface-muted px-2 py-0.5 rounded text-[10px] font-semibold text-on-surface-variant whitespace-nowrap border border-border-subtle">
                    Current Stage
                  </div>
                  <div className="w-6 h-6 rounded-full bg-surface border-2 border-[#2563EB] text-[#2563EB] flex items-center justify-center shadow-xs">
                    <div className="w-2 h-2 bg-[#2563EB] rounded-full"></div>
                  </div>
                  <span className="text-[11px] font-semibold text-[#2563EB]">Under Review</span>
                </div>

                {/* Stage 4 */}
                <div className="flex flex-col items-center gap-2 opacity-50">
                  <div className="w-6 h-6 rounded-full bg-surface border-2 border-border-subtle text-on-surface-variant flex items-center justify-center"></div>
                  <span className="text-[11px] font-medium text-on-surface-variant">Offer Ready</span>
                </div>

                {/* Stage 5 */}
                <div className="flex flex-col items-center gap-2 opacity-50">
                  <div className="w-6 h-6 rounded-full bg-surface border-2 border-border-subtle text-on-surface-variant flex items-center justify-center"></div>
                  <span className="text-[11px] font-medium text-on-surface-variant">Approved</span>
                </div>
              </div>
            </div>

            {/* Informational Callout */}
            <div className="p-4 bg-surface-muted rounded-xl flex items-start gap-3 border border-border-subtle text-xs">
              <span className="material-symbols-outlined text-[#2563EB] text-base mt-0.5">info</span>
              <div>
                <h4 className="font-semibold text-on-surface mb-0.5">What happens next?</h4>
                <p className="text-on-surface-variant leading-relaxed">
                  Our underwriting team is currently evaluating your verified tax transcripts and property appraisal. This step typically takes 2-3 business days.
                </p>
              </div>
            </div>
          </div>

          {/* Financial Cards Grid */}
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            {/* Card 1: Available Credit Limit */}
            <div className="bg-[#0F172A] text-white rounded-xl p-6 shadow-sm relative overflow-hidden flex flex-col justify-between h-48 border border-slate-800">
              <div className="flex justify-between items-start">
                <span className="text-xs font-semibold uppercase tracking-wider text-slate-300">
                  Available Credit Limit
                </span>
                <span className="material-symbols-outlined text-slate-400">credit_card</span>
              </div>
              <div>
                <span className="text-3xl font-bold font-mono tracking-tight tnum">$250,000</span>
                <p className="text-xs text-slate-400 mt-1">Revolving commercial facility active</p>
              </div>
              <div className="pt-3 border-t border-slate-800 flex justify-between text-xs text-slate-400">
                <span>Trust Score Impact</span>
                <span className="text-emerald-400 font-mono font-bold">
                  {healthProfile ? `${healthProfile.trustIndexScore}%` : '90%'}
                </span>
              </div>
            </div>

            {/* Card 2: Active Loan Balance */}
            <div className="bg-surface rounded-xl p-6 shadow-sm border border-border-subtle flex flex-col justify-between h-48">
              <div className="flex justify-between items-start">
                <span className="text-xs font-semibold uppercase tracking-wider text-on-surface-variant">
                  Active Loan Balance
                </span>
                <span className="material-symbols-outlined text-on-surface-variant">account_balance</span>
              </div>
              <div>
                <span className="text-3xl font-bold font-mono text-on-surface tracking-tight tnum">
                  ${loanFacility ? loanFacility.principalOutstanding.toLocaleString() : '2,450,000'}
                </span>
                <div className="flex items-center gap-2 mt-1 text-xs text-on-surface-variant">
                  <span className="w-1.5 h-1.5 rounded-full bg-[#2563EB]"></span>
                  <span>{loanFacility ? loanFacility.interestRate : 'SOFR + 2.50%'}</span>
                </div>
              </div>
              <div className="pt-3 border-t border-border-subtle flex justify-between items-center text-xs">
                <div>
                  <span className="text-on-surface-variant block text-[10px] uppercase">Next Repayment</span>
                  <span className="font-bold font-mono text-on-surface text-sm tnum">
                    ${loanFacility ? loanFacility.nextPaymentAmount.toLocaleString() : '18,420'}
                  </span>
                </div>
                <span className="bg-surface-muted px-2.5 py-1 rounded text-xs font-medium text-on-surface-variant border border-border-subtle font-mono">
                  {loanFacility ? loanFacility.nextPaymentDueDate : 'Oct 1, 2026'}
                </span>
              </div>
            </div>
          </div>
        </section>

        {/* Right 4 Cols: Recent Activity Timeline */}
        <section className="lg:col-span-4 flex flex-col">
          <div className="bg-surface rounded-xl p-6 shadow-xs border border-border-subtle flex-1 flex flex-col justify-between space-y-6">
            <div className="flex items-center justify-between border-b border-border-subtle pb-4">
              <h3 className="font-bold text-base font-headline-sm text-on-surface">Recent Activity</h3>
              <button className="p-1 rounded hover:bg-surface-muted text-on-surface-variant">
                <span className="material-symbols-outlined text-lg">more_horiz</span>
              </button>
            </div>

            {/* Timeline List */}
            <div className="relative flex-1 space-y-6 pl-2">
              <div className="absolute left-[15px] top-2 bottom-2 w-[1px] bg-border-subtle"></div>

              {/* Event 1 */}
              <div className="flex gap-4 relative">
                <div className="w-7 h-7 rounded-full bg-surface border border-border-subtle flex items-center justify-center z-10 text-emerald-600 shadow-2xs">
                  <span className="material-symbols-outlined text-sm">verified_user</span>
                </div>
                <div className="flex flex-col text-xs pt-0.5">
                  <span className="font-semibold text-on-surface">Bank statements verified</span>
                  <span className="text-on-surface-variant font-mono text-[11px]">Today, 09:42 AM</span>
                </div>
              </div>

              {/* Event 2 */}
              <div className="flex gap-4 relative">
                <div className="w-7 h-7 rounded-full bg-surface border border-border-subtle flex items-center justify-center z-10 text-on-surface-variant shadow-2xs">
                  <span className="material-symbols-outlined text-sm">upload_file</span>
                </div>
                <div className="flex flex-col text-xs pt-0.5">
                  <span className="font-semibold text-on-surface">Property valuation uploaded</span>
                  <span className="text-on-surface-variant font-mono text-[11px]">Yesterday, 04:15 PM</span>
                </div>
              </div>

              {/* Event 3 */}
              <div className="flex gap-4 relative">
                <div className="w-7 h-7 rounded-full bg-surface border border-border-subtle flex items-center justify-center z-10 text-secondary shadow-2xs">
                  <span className="material-symbols-outlined text-sm">autorenew</span>
                </div>
                <div className="flex flex-col text-xs pt-0.5 space-y-1">
                  <span className="font-semibold text-on-surface">Auto-debit successful</span>
                  <span className="text-on-surface-variant font-mono text-[11px]">Oct 01, 2026</span>
                  <div className="bg-surface-muted p-2 rounded border border-border-subtle text-[11px] text-on-surface-variant font-mono tnum">
                    $18,420 processed from Chase Everyday Acc (*4921)
                  </div>
                </div>
              </div>
            </div>

            <button
              onClick={() => navigate('/applicant/applications')}
              className="w-full py-2 rounded-lg text-[#2563EB] font-medium text-xs hover:bg-surface-muted transition-colors border border-border-subtle hover:border-[#2563EB]/30"
            >
              View All Activity History
            </button>
          </div>
        </section>
      </div>
    </div>
  );
};
