import React from 'react';

export const BankerPortfolioPage: React.FC = () => (
  <div className="space-y-4">
    <h1 className="text-2xl font-bold font-headline-lg text-on-surface border-b border-border-subtle pb-4">
      Commercial Portfolio Oversight
    </h1>
    <div className="bg-surface p-6 rounded-xl border border-border-subtle shadow-xs">
      <p className="text-sm text-on-surface-variant">Active portfolio metrics, asset distribution, and institutional risk exposures.</p>
    </div>
  </div>
);

export const BankerCustomersPage: React.FC = () => (
  <div className="space-y-4">
    <h1 className="text-2xl font-bold font-headline-lg text-on-surface border-b border-border-subtle pb-4">
      Customer Records & KYC Vault
    </h1>
    <div className="bg-surface p-6 rounded-xl border border-border-subtle shadow-xs">
      <p className="text-sm text-on-surface-variant">Institutional entity profiles, ultimate beneficial owner (UBO) records, and compliance files.</p>
    </div>
  </div>
);

export const BankerTransactionsPage: React.FC = () => (
  <div className="space-y-4">
    <h1 className="text-2xl font-bold font-headline-lg text-on-surface border-b border-border-subtle pb-4">
      Transaction Monitoring & Settlement Ledger
    </h1>
    <div className="bg-surface p-6 rounded-xl border border-border-subtle shadow-xs">
      <p className="text-sm text-on-surface-variant">Real-time wire monitoring, credit line drawdowns, and settlement verification.</p>
    </div>
  </div>
);

export const BankerLoanApprovalsPage: React.FC = () => (
  <div className="space-y-4">
    <h1 className="text-2xl font-bold font-headline-lg text-on-surface border-b border-border-subtle pb-4">
      Loan Approvals Queue
    </h1>
    <div className="bg-surface p-6 rounded-xl border border-border-subtle shadow-xs">
      <p className="text-sm text-on-surface-variant">Credit committee approval workflow and electronic signature binding.</p>
    </div>
  </div>
);

export const BankerRiskReportsPage: React.FC = () => (
  <div className="space-y-4">
    <h1 className="text-2xl font-bold font-headline-lg text-on-surface border-b border-border-subtle pb-4">
      Institutional Risk Reports
    </h1>
    <div className="bg-surface p-6 rounded-xl border border-border-subtle shadow-xs">
      <p className="text-sm text-on-surface-variant">Stress testing, concentration reports, and AI model risk performance audits.</p>
    </div>
  </div>
);
