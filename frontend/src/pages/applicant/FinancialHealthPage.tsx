import React from 'react';

export const FinancialHealthPage: React.FC = () => {
  return (
    <div className="space-y-8">
      {/* Top Hero Card: Trust Index & Profile Evaluation */}
      <div className="bg-surface shadow-xs p-6 sm:p-8 rounded-xl border border-border-subtle flex flex-col md:flex-row gap-8 items-center md:items-start relative overflow-hidden">
        {/* Trust Index Radial Gauge */}
        <div className="relative w-44 h-44 shrink-0 flex items-center justify-center">
          <svg className="absolute inset-0 w-full h-full transform -rotate-90" viewBox="0 0 100 100">
            <circle className="text-surface-container" cx="50" cy="50" fill="none" r="44" stroke="currentColor" strokeWidth="4"></circle>
            <circle
              className="text-[#2563EB] transition-all duration-800 ease-out"
              cx="50"
              cy="50"
              fill="none"
              r="44"
              stroke="currentColor"
              strokeWidth="5"
              strokeDasharray="276"
              strokeDashoffset="27.6"
              strokeLinecap="round"
            ></circle>
          </svg>

          <div className="text-center z-10">
            <span className="text-4xl font-bold font-display text-[#2563EB] block leading-none tracking-tight tnum">
              90<span className="text-lg font-normal">%</span>
            </span>
            <span className="text-[10px] font-semibold text-on-surface-variant uppercase tracking-[0.2em] block mt-2">
              Trust Index
            </span>
          </div>

          <div className="absolute top-2 right-2 bg-white text-emerald-600 w-6 h-6 rounded-full flex items-center justify-center shadow-xs border border-border-subtle">
            <span className="material-symbols-outlined text-base">verified</span>
          </div>
        </div>

        {/* Profile Copy */}
        <div className="flex-1 flex flex-col justify-center space-y-3">
          <div className="flex items-center gap-2">
            <span className="text-xs font-mono uppercase text-on-surface-variant tracking-wider">
              Institutional AI Profile Evaluation
            </span>
            <span className="text-emerald-700 bg-emerald-50 px-2 py-0.5 rounded text-[11px] font-bold border border-emerald-200 uppercase">
              Tier 1 Borrower
            </span>
          </div>

          <h1 className="text-2xl font-bold font-headline-md text-on-surface">
            How AgentTrust OS evaluates your profile
          </h1>

          <p className="text-sm text-on-surface-variant leading-relaxed">
            Sarah, your financial footprint indicates a highly responsible approach to credit. Your consistent on-time repayment history over the past 36 months, coupled with stable cashflow, classifies you as a <strong className="text-on-surface">Tier 1 Trusted Borrower</strong>. This unlocks preferred interest rates and accelerated underwriting.
          </p>

          <div className="flex flex-wrap gap-2 pt-2">
            <span className="inline-flex items-center gap-1.5 px-3 py-1 bg-emerald-50 border border-emerald-200 text-emerald-800 rounded-full text-xs font-semibold">
              <span className="w-2 h-2 rounded-full bg-emerald-500"></span> Premium Rates Active
            </span>
            <span className="inline-flex items-center gap-1.5 px-3 py-1 bg-blue-50 border border-blue-200 text-[#2563EB] rounded-full text-xs font-semibold">
              <span className="w-2 h-2 rounded-full bg-[#2563EB]"></span> Accelerated Underwriting Eligible
            </span>
          </div>
        </div>
      </div>

      {/* Grid of Financial Health Indicators */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {/* Indicator 1: Repayment Behavior */}
        <div className="bg-surface shadow-xs rounded-xl p-6 border border-border-subtle flex flex-col justify-between space-y-4">
          <div className="flex items-start justify-between">
            <div className="flex items-center gap-2">
              <span className="material-symbols-outlined text-[#2563EB] text-xl">event_available</span>
              <h2 className="font-semibold text-xs text-on-surface uppercase tracking-wider">Repayment Behavior</h2>
            </div>
            <span className="text-[11px] font-bold text-emerald-700 bg-emerald-50 px-2 py-0.5 rounded border border-emerald-200 uppercase">
              Excellent
            </span>
          </div>
          <p className="text-xs text-on-surface-variant">Consistent on-time performance across all commercial facilities.</p>
          <div>
            <div className="flex justify-between text-xs text-on-surface-variant font-mono mb-1">
              <span>ON-TIME RATE</span>
              <span className="font-bold text-on-surface tnum">100.00%</span>
            </div>
            <div className="h-2 w-full bg-surface-container rounded-full overflow-hidden">
              <div className="h-full bg-emerald-500 rounded-full w-full"></div>
            </div>
            <span className="text-[10px] text-on-surface-variant block mt-1 font-mono">VERIFIED: LAST 36 MONTHS</span>
          </div>
        </div>

        {/* Indicator 2: Income Stability */}
        <div className="bg-surface shadow-xs rounded-xl p-6 border border-border-subtle flex flex-col justify-between space-y-4">
          <div className="flex items-start justify-between">
            <div className="flex items-center gap-2">
              <span className="material-symbols-outlined text-[#2563EB] text-xl">trending_up</span>
              <h2 className="font-semibold text-xs text-on-surface uppercase tracking-wider">Income Stability</h2>
            </div>
            <span className="text-[11px] font-bold text-emerald-700 bg-emerald-50 px-2 py-0.5 rounded border border-emerald-200 uppercase">
              Consistent
            </span>
          </div>
          <p className="text-xs text-on-surface-variant">Reliable earnings pattern with low volatility index.</p>
          <div>
            <div className="flex items-end gap-1.5 h-10 mb-2">
              {[60, 65, 62, 70, 68, 75, 72, 80, 78, 85, 82, 90].map((h, i) => (
                <div key={i} className="flex-1 bg-[#2563EB]/20 rounded-t-xs" style={{ height: `${h}%` }}></div>
              ))}
            </div>
            <div className="flex justify-between text-xs text-on-surface-variant font-mono">
              <span>12M REVENUE TREND</span>
              <span className="font-bold text-emerald-600 tnum">+4.2% YoY</span>
            </div>
          </div>
        </div>

        {/* Indicator 3: Debt-to-Income */}
        <div className="bg-surface shadow-xs rounded-xl p-6 border border-border-subtle flex flex-col justify-between space-y-4">
          <div className="flex items-start justify-between">
            <div className="flex items-center gap-2">
              <span className="material-symbols-outlined text-[#2563EB] text-xl">balance</span>
              <h2 className="font-semibold text-xs text-on-surface uppercase tracking-wider">Debt-to-Income (DTI)</h2>
            </div>
            <span className="text-[11px] font-bold text-emerald-700 bg-emerald-50 px-2 py-0.5 rounded border border-emerald-200 uppercase">
              Healthy
            </span>
          </div>
          <p className="text-xs text-on-surface-variant">Total debt obligations are well within sustainable policy limits.</p>
          <div>
            <div className="flex justify-between text-xs text-on-surface-variant font-mono mb-1">
              <span>CURRENT DTI: <strong className="text-on-surface">28.0%</strong></span>
              <span>BENCHMARK FLOOR: <strong>36.0%</strong></span>
            </div>
            <div className="h-2 w-full bg-surface-container rounded-full overflow-hidden">
              <div className="h-full bg-emerald-500 rounded-full" style={{ width: '28%' }}></div>
            </div>
          </div>
        </div>

        {/* Indicator 4: Liquidity Ratio */}
        <div className="bg-surface shadow-xs rounded-xl p-6 border border-border-subtle flex flex-col justify-between space-y-4">
          <div className="flex items-start justify-between">
            <div className="flex items-center gap-2">
              <span className="material-symbols-outlined text-[#2563EB] text-xl">account_balance_wallet</span>
              <h2 className="font-semibold text-xs text-on-surface uppercase tracking-wider">Liquidity Coverage</h2>
            </div>
            <span className="text-[11px] font-bold text-emerald-700 bg-emerald-50 px-2 py-0.5 rounded border border-emerald-200 uppercase">
              Strong
            </span>
          </div>
          <p className="text-xs text-on-surface-variant">Liquid cash reserves cover short-term liabilities by 2.10x.</p>
          <div>
            <div className="flex justify-between text-xs text-on-surface-variant font-mono mb-1">
              <span>CURRENT LIQUIDITY RATIO</span>
              <span className="font-bold text-emerald-600 tnum">2.10x</span>
            </div>
            <div className="h-2 w-full bg-surface-container rounded-full overflow-hidden">
              <div className="h-full bg-emerald-500 rounded-full" style={{ width: '84%' }}></div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};
