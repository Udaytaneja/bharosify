import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { AIInsight, VerificationIndicator, AuditTrailLink } from '../../components/common/Primitives';

export const UnderwritingWorkspacePage: React.FC = () => {
  const navigate = useNavigate();
  const [activeTab, setActiveTab] = useState<'documents' | 'financials' | 'collateral'>('documents');
  const [zoomLevel, setZoomLevel] = useState(100);

  return (
    <div className="space-y-6">
      {/* Header Bar */}
      <div className="flex flex-col lg:flex-row lg:items-center justify-between gap-4 border-b border-border-subtle pb-4">
        <div className="flex items-center gap-4">
          <div className="w-12 h-12 rounded-xl bg-surface border border-border-subtle flex items-center justify-center text-secondary shadow-xs">
            <span className="material-symbols-outlined text-2xl">real_estate_agent</span>
          </div>
          <div>
            <div className="flex items-center gap-2">
              <h1 className="text-2xl font-bold font-headline-md text-on-surface">Sarah Connor</h1>
              <VerificationIndicator label="Identity Confirmed" />
            </div>
            <div className="flex items-center gap-3 text-xs text-on-surface-variant font-mono mt-0.5">
              <span>APP-2023-891A</span>
              <span>•</span>
              <span>Commercial Real Estate Purchase</span>
              <span>•</span>
              <span className="text-emerald-700 bg-emerald-50 px-2 py-0.5 rounded font-semibold border border-emerald-200 uppercase">
                In Active Underwriting
              </span>
            </div>
          </div>
        </div>

        <div className="flex items-center gap-3">
          <button
            onClick={() => navigate('/banker/underwriting/decision-support')}
            className="px-4 py-2 bg-surface hover:bg-surface-muted border border-border-subtle text-on-surface font-medium text-xs rounded-md flex items-center gap-2 transition-colors"
          >
            <span className="material-symbols-outlined text-sm text-secondary">psychology</span>
            <span>Open Decision Support AI</span>
          </button>
          <button
            onClick={() => navigate('/banker/audit-trail')}
            className="px-4 py-2 bg-[#2563EB] hover:bg-blue-700 text-white font-medium text-xs rounded-md flex items-center gap-2 transition-colors shadow-xs"
          >
            <span className="material-symbols-outlined text-sm">gavel</span>
            <span>Approve & Sign Audit Log</span>
          </button>
        </div>
      </div>

      {/* 3-Column Layout */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
        {/* Left Column (3 cols): Borrower Profile & Loan Details */}
        <div className="lg:col-span-3 space-y-4">
          {/* Applicant Card */}
          <div className="bg-surface rounded-xl border border-border-subtle p-5 space-y-4 shadow-xs">
            <div className="flex items-center justify-between border-b border-border-subtle pb-3">
              <span className="text-xs font-semibold uppercase text-on-surface-variant tracking-wider">
                Applicant Profile
              </span>
              <span className="material-symbols-outlined text-sm text-on-surface-variant">person</span>
            </div>

            <div className="flex items-center gap-3">
              <div className="w-12 h-12 rounded-lg bg-slate-800 text-white font-bold flex items-center justify-center text-lg">
                SC
              </div>
              <div>
                <div className="font-bold text-sm text-on-surface">Sarah Connor</div>
                <div className="text-xs text-on-surface-variant">Principal Borrower</div>
              </div>
            </div>

            <div className="space-y-2 text-xs divide-y divide-border-subtle">
              <div className="flex justify-between py-1.5">
                <span className="text-on-surface-variant">SSN Tax ID</span>
                <span className="font-mono font-medium">XXX-XX-1984</span>
              </div>
              <div className="flex justify-between py-1.5">
                <span className="text-on-surface-variant">FICO Credit Score</span>
                <span className="font-mono font-bold text-emerald-600 tnum">782 (Prime)</span>
              </div>
              <div className="flex justify-between py-1.5">
                <span className="text-on-surface-variant">Annual Revenue</span>
                <span className="font-mono font-medium tnum">$1,450,000</span>
              </div>
              <div className="flex justify-between py-1.5">
                <span className="text-on-surface-variant">Years in Business</span>
                <span className="font-mono font-medium tnum">12 Years</span>
              </div>
            </div>
          </div>

          {/* Requested Loan Details Card */}
          <div className="bg-surface rounded-xl border border-border-subtle p-5 space-y-4 shadow-xs">
            <div className="flex items-center justify-between border-b border-border-subtle pb-3">
              <span className="text-xs font-semibold uppercase text-on-surface-variant tracking-wider">
                Loan Request Metrics
              </span>
              <span className="material-symbols-outlined text-sm text-on-surface-variant">request_quote</span>
            </div>

            <div>
              <div className="text-3xl font-bold font-mono text-on-surface tnum">$450,000</div>
              <div className="text-xs text-on-surface-variant mt-1">Requested Commercial Credit</div>
            </div>

            <div className="grid grid-cols-2 gap-3 text-xs">
              <div className="bg-surface-bright p-2.5 rounded border border-border-subtle">
                <span className="text-[10px] text-on-surface-variant block uppercase">Term</span>
                <span className="font-mono font-semibold text-on-surface">180 Months</span>
              </div>
              <div className="bg-surface-bright p-2.5 rounded border border-border-subtle">
                <span className="text-[10px] text-on-surface-variant block uppercase">LTV Ratio</span>
                <span className="font-mono font-semibold text-on-surface">65.0%</span>
              </div>
              <div className="bg-surface-bright p-2.5 rounded border border-border-subtle">
                <span className="text-[10px] text-on-surface-variant block uppercase">Interest Rate</span>
                <span className="font-mono font-semibold text-on-surface">5.20% Fixed</span>
              </div>
              <div className="bg-surface-bright p-2.5 rounded border border-border-subtle">
                <span className="text-[10px] text-on-surface-variant block uppercase">DSCR Ratio</span>
                <span className="font-mono font-semibold text-emerald-600">1.42x</span>
              </div>
            </div>
          </div>
        </div>

        {/* Center Column (5 cols): Document Intelligence & OCR Preview */}
        <div className="lg:col-span-5 space-y-4">
          <div className="bg-surface rounded-xl border border-border-subtle overflow-hidden shadow-xs">
            {/* Tabs */}
            <div className="flex items-center justify-between border-b border-border-subtle bg-surface-muted/40 px-4 py-2">
              <div className="flex items-center gap-1">
                <button
                  onClick={() => setActiveTab('documents')}
                  className={`px-3 py-1.5 rounded-md text-xs font-semibold transition-colors ${
                    activeTab === 'documents' ? 'bg-surface text-on-surface border border-border-subtle shadow-2xs' : 'text-on-surface-variant hover:text-on-surface'
                  }`}
                >
                  2023 Tax Return (IRS 1040)
                </button>
                <button
                  onClick={() => setActiveTab('financials')}
                  className={`px-3 py-1.5 rounded-md text-xs font-semibold transition-colors ${
                    activeTab === 'financials' ? 'bg-surface text-on-surface border border-border-subtle shadow-2xs' : 'text-on-surface-variant hover:text-on-surface'
                  }`}
                >
                  Audited P&L
                </button>
              </div>

              {/* Viewer Controls */}
              <div className="flex items-center gap-1">
                <button onClick={() => setZoomLevel(prev => Math.max(70, prev - 10))} className="p-1 text-on-surface-variant hover:bg-surface-muted rounded">
                  <span className="material-symbols-outlined text-sm">remove</span>
                </button>
                <span className="text-[11px] font-mono w-10 text-center">{zoomLevel}%</span>
                <button onClick={() => setZoomLevel(prev => Math.min(150, prev + 10))} className="p-1 text-on-surface-variant hover:bg-surface-muted rounded">
                  <span className="material-symbols-outlined text-sm">add</span>
                </button>
              </div>
            </div>

            {/* Document Content Box */}
            <div className="p-6 bg-slate-900 text-slate-200 font-mono text-xs space-y-4 min-h-[420px] overflow-y-auto" style={{ transform: `scale(${zoomLevel / 100})`, transformOrigin: 'top left' }}>
              <div className="flex items-center justify-between border-b border-slate-700 pb-2">
                <span className="text-emerald-400 font-bold">IRS FORM 1040 - U.S. INDIVIDUAL INCOME TAX RETURN</span>
                <span className="bg-emerald-950 text-emerald-400 text-[10px] px-2 py-0.5 rounded border border-emerald-800">OCR VERIFIED 99.8%</span>
              </div>

              <div className="space-y-2">
                <div className="bg-slate-800/80 p-2.5 rounded border border-slate-700 flex justify-between items-center">
                  <span>Line 1z: Wages, salaries, tips:</span>
                  <span className="text-white font-bold tnum">$285,400.00</span>
                </div>
                <div className="bg-slate-800/80 p-2.5 rounded border border-slate-700 flex justify-between items-center">
                  <span>Line 8: Additional income (Schedule 1):</span>
                  <span className="text-white font-bold tnum">$164,200.00</span>
                </div>
                <div className="bg-[#2563EB]/12 p-2.5 rounded border border-[#2563EB] flex justify-between items-center">
                  <span className="text-[#2563EB] font-bold">Line 11: Adjusted Gross Income (AGI):</span>
                  <span className="text-emerald-400 font-bold text-sm tnum">$449,600.00</span>
                </div>
                <div className="bg-slate-800/80 p-2.5 rounded border border-slate-700 flex justify-between items-center">
                  <span>Line 24: Total Tax Owed:</span>
                  <span className="text-white font-bold tnum">$112,400.00</span>
                </div>
              </div>

              <div className="p-3 bg-slate-850 rounded border border-slate-700 text-[11px] text-slate-400">
                <div className="text-xs text-slate-200 font-semibold mb-1">Forensic Document Check</div>
                <div>• Digital Signature Hash Match: 0x8a994ff...3b9</div>
                <div>• IRS Tax Transcript Cross-Verification: MATCHED</div>
                <div>• Tampering Index: 0.00 (No pixel anomalies detected)</div>
              </div>
            </div>
          </div>
        </div>

        {/* Right Column (4 cols): AI Governance & Underwriting Decision Engine */}
        <div className="lg:col-span-4 space-y-4">
          <AIInsight
            title="Underwriting AI Analysis"
            confidence={98.6}
            auditTrailId="LOG-2026-9812-NY"
          >
            Applicant exhibits a strong cashflow profile with a 1.42x DSCR ratio exceeding the institutional 1.25x policy floor. Forensic document checks confirm authentic tax transcripts.
          </AIInsight>

          {/* Policy Checklist Card */}
          <div className="bg-surface rounded-xl border border-border-subtle p-5 space-y-4 shadow-xs">
            <div className="flex items-center justify-between border-b border-border-subtle pb-3">
              <span className="text-xs font-semibold uppercase text-on-surface-variant tracking-wider">
                Automated Policy Check Matrix
              </span>
              <span className="material-symbols-outlined text-sm text-emerald-600">fact_check</span>
            </div>

            <div className="space-y-2 text-xs">
              <div className="flex items-center justify-between py-[10px] px-2 rounded bg-emerald-50 border border-emerald-200 text-emerald-800">
                <div className="flex items-center gap-2">
                  <span className="material-symbols-outlined text-sm">check_circle</span>
                  <span>Minimum FICO Score (&ge; 680)</span>
                </div>
                <span className="font-mono font-bold">782 PASSED</span>
              </div>

              <div className="flex items-center justify-between py-[10px] px-2 rounded bg-emerald-50 border border-emerald-200 text-emerald-800">
                <div className="flex items-center gap-2">
                  <span className="material-symbols-outlined text-sm">check_circle</span>
                  <span>Minimum DSCR Coverage (&ge; 1.25x)</span>
                </div>
                <span className="font-mono font-bold">1.42x PASSED</span>
              </div>

              <div className="flex items-center justify-between py-[10px] px-2 rounded bg-emerald-50 border border-emerald-200 text-emerald-800">
                <div className="flex items-center gap-2">
                  <span className="material-symbols-outlined text-sm">check_circle</span>
                  <span>Maximum Loan-to-Value (&le; 75%)</span>
                </div>
                <span className="font-mono font-bold">65% PASSED</span>
              </div>

              <div className="flex items-center justify-between py-[10px] px-2 rounded bg-rose-50 border border-rose-200 text-rose-800">
                <div className="flex items-center gap-2">
                  <span className="material-symbols-outlined text-sm">warning</span>
                  <span>Entity Concentration Risk (&le; 10%)</span>
                </div>
                <span className="font-mono font-bold">FLAGGED 14%</span>
              </div>

              <div className="flex items-center justify-between p-2 rounded bg-emerald-50 border border-emerald-200 text-emerald-800">
                <div className="flex items-center gap-2">
                  <span className="material-symbols-outlined text-sm">check_circle</span>
                  <span>Minimum DSCR (&ge; 1.25x)</span>
                </div>
                <span className="font-mono font-bold">1.42x PASSED</span>
              </div>

              <div className="flex items-center justify-between p-2 rounded bg-emerald-50 border border-emerald-200 text-emerald-800">
                <div className="flex items-center gap-2">
                  <span className="material-symbols-outlined text-sm">check_circle</span>
                  <span>Max Loan-to-Value (&le; 75%)</span>
                </div>
                <span className="font-mono font-bold">65% PASSED</span>
              </div>

              <div className="flex items-center justify-between p-2 rounded bg-amber-50 border border-amber-200 text-amber-800">
                <div className="flex items-center gap-2">
                  <span className="material-symbols-outlined text-sm">warning</span>
                  <span>Entity Concentration Risk</span>
                </div>
                <span className="font-mono font-bold">FLAGGED 14%</span>
              </div>
            </div>
          </div>

          <AuditTrailLink hash="0x8F9...A3C" label="Underwriting State Commit" />
        </div>
      </div>
    </div>
  );
};
