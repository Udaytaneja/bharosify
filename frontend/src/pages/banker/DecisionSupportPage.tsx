import React from 'react';
import { AIInsight, Badge, Button } from '../../components/common/Primitives';

export const DecisionSupportPage: React.FC = () => {
  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 border-b border-border-subtle pb-4">
        <div>
          <div className="text-xs font-mono uppercase text-on-surface-variant tracking-wider">
            Automated Risk Evaluation & Policy Engine
          </div>
          <h1 className="text-2xl font-bold font-headline-lg text-on-surface">
            Underwriting Decision Support
          </h1>
        </div>

        <div className="flex items-center gap-3">
          <Badge variant="success" size="md">
            Model Active: AgentTrust-v4.8
          </Badge>
          <Button variant="secondary" size="sm" icon={<span className="material-symbols-outlined text-sm">tune</span>}>
            Configure Rules
          </Button>
        </div>
      </div>

      {/* Top AI Evaluation Banner */}
      <AIInsight
        title="AI Credit Recommendation"
        confidence={99.1}
        modelName="AgentTrust Risk Engine v4.8"
        auditTrailId="REC-2026-8819-US"
      >
        <div className="font-semibold text-base text-on-surface mb-1">
          RECOMMENDATION: CONDITIONAL APPROVAL ($450,000 CRE Credit Line)
        </div>
        <p className="text-xs text-on-surface-variant">
          Automated evaluation executed 14 underwriting policies across liquidity, debt-service coverage, collateral valuation, and historical repayment records. Zero policy violations detected.
        </p>
      </AIInsight>

      {/* 2-Column Risk Score Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {/* Risk Factor Decomposition */}
        <div className="bg-surface rounded-xl border border-border-subtle p-6 space-y-4 shadow-xs">
          <div className="flex items-center justify-between border-b border-border-subtle pb-3">
            <h3 className="font-semibold text-sm text-on-surface">Risk Factor Decomposition</h3>
            <span className="text-xs font-mono text-on-surface-variant">Weighted Index</span>
          </div>

          <div className="space-y-3 text-xs">
            <div>
              <div className="flex justify-between font-medium mb-1">
                <span>Credit Score & Payment History (35%)</span>
                <span className="text-emerald-600 font-mono">Low Risk (94/100)</span>
              </div>
              <div className="w-full h-[8px] bg-surface-container rounded-full overflow-hidden">
                <div className="h-full bg-emerald-500 rounded-full" style={{ width: '94%' }}></div>
              </div>
            </div>

            <div>
              <div className="flex justify-between font-medium mb-1">
                <span>Cash Flow & Debt Service Ratio (30%)</span>
                <span className="text-emerald-600 font-mono">Low Risk (88/100)</span>
              </div>
              <div className="w-full h-[8px] bg-surface-container rounded-full overflow-hidden">
                <div className="h-full bg-emerald-500 rounded-full" style={{ width: '88%' }}></div>
              </div>
            </div>

            <div>
              <div className="flex justify-between font-medium mb-1">
                <span>Collateral Coverage & LTV (20%)</span>
                <span className="text-emerald-600 font-mono">Low Risk (90/100)</span>
              </div>
              <div className="w-full h-[8px] bg-surface-container rounded-full overflow-hidden">
                <div className="h-full bg-emerald-500 rounded-full" style={{ width: '90%' }}></div>
              </div>
            </div>

            <div>
              <div className="flex justify-between font-medium mb-1">
                <span>Macro Industry Concentration (15%)</span>
                <span className="text-amber-600 font-mono">Moderate Risk (65/100)</span>
              </div>
              <div className="w-full h-[8px] bg-surface-container rounded-full overflow-hidden">
                <div className="h-full bg-amber-500 rounded-full" style={{ width: '65%' }}></div>
              </div>
            </div>
          </div>
        </div>

        {/* Human Override & Banker Action */}
        <div className="bg-surface rounded-xl border border-border-subtle p-6 space-y-4 shadow-xs flex flex-col justify-between">
          <div>
            <div className="flex items-center justify-between border-b border-border-subtle pb-3 mb-4">
              <h3 className="font-semibold text-sm text-on-surface">Underwriter Action & Sign-off</h3>
              <span className="text-xs text-on-surface-variant font-mono">Mandatory Human-in-the-Loop</span>
            </div>

            <p className="text-xs text-on-surface-variant leading-relaxed mb-4">
              As mandated by AgentTrust OS AI Governance Policy (FIPS 140-3), AI recommendations require explicit human underwriter endorsement before credit line binding.
            </p>

            <div className="space-y-3">
              <label className="block text-xs font-semibold text-on-surface uppercase tracking-wider">
                Underwriter Notes / Rationale
              </label>
              <textarea
                rows={3}
                defaultValue="Verified IRS tax transcript matches 1040 line items. DSCR 1.42x satisfies institutional commercial underwriting guidelines."
                className="w-full p-3 bg-surface-bright border border-border-subtle rounded-md text-xs text-on-surface focus:outline-none focus:border-[#2563EB]"
              />
            </div>
          </div>

          <div className="flex items-center gap-3 pt-4 border-t border-border-subtle">
            <Button variant="danger" size="sm" className="flex-1">
              Reject / Request Info
            </Button>
            <Button variant="primary" size="sm" className="flex-2 bg-[#2563EB]">
              Approve Credit Line ($450,000)
            </Button>
          </div>
        </div>
      </div>
    </div>
  );
};
