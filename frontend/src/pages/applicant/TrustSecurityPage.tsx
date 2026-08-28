import React, { useState } from 'react';

export const TrustSecurityPage: React.FC = () => {
  const [bureauSync, setBureauSync] = useState(true);
  const [bankFeed, setBankFeed] = useState(true);
  const [thirdPartyShare, setThirdPartyShare] = useState(false);

  return (
    <div className="space-y-8">
      {/* Header */}
      <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4 border-b border-border-subtle pb-4">
        <div>
          <h1 className="text-3xl font-bold font-display text-on-surface tracking-tight">
            Trust & Security Controls
          </h1>
          <p className="text-sm text-on-surface-variant mt-1">
            Manage data privacy permissions, AI governance disclosures, and encryption settings.
          </p>
        </div>

        <div className="flex items-center gap-2 bg-emerald-50 text-emerald-700 border border-emerald-200 px-3 py-1.5 rounded-full text-xs font-semibold">
          <span className="w-2 h-2 rounded-full bg-emerald-500"></span>
          <span>AES-256 Encrypted Session</span>
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
        {/* Section 1: User Data Control & Permissions */}
        <div className="bg-surface rounded-xl border border-border-subtle p-6 space-y-6 shadow-xs">
          <div className="border-b border-border-subtle pb-3">
            <h3 className="font-bold text-base text-on-surface">Data Permissions & Sync Controls</h3>
            <p className="text-xs text-on-surface-variant mt-0.5">Control how your financial records are shared with credit evaluation engines.</p>
          </div>

          <div className="space-y-4">
            <div className="flex items-center justify-between p-3 bg-surface-bright rounded-lg border border-border-subtle">
              <div>
                <div className="font-semibold text-xs text-on-surface">Automated Credit Bureau Sync</div>
                <div className="text-[11px] text-on-surface-variant">Real-time credit score updates via Experian / Equifax.</div>
              </div>
              <button
                onClick={() => setBureauSync(!bureauSync)}
                className={`w-11 h-6 flex items-center rounded-full p-0.5 transition-colors ${bureauSync ? 'bg-[#2563EB] justify-end' : 'bg-slate-300 justify-start'}`}
              >
                <div className="w-4 h-4 rounded-full bg-white shadow-xs"></div>
              </button>
            </div>

            <div className="flex items-center justify-between p-3 bg-surface-bright rounded-lg border border-border-subtle">
              <div>
                <div className="font-semibold text-xs text-on-surface">Read-Only Bank Account Feed</div>
                <div className="text-[11px] text-on-surface-variant">Automated cashflow verification via Plaid / Finicity.</div>
              </div>
              <button
                onClick={() => setBankFeed(!bankFeed)}
                className={`w-11 h-6 flex items-center rounded-full p-0.5 transition-colors ${bankFeed ? 'bg-[#2563EB] justify-end' : 'bg-slate-300 justify-start'}`}
              >
                <div className="w-4 h-4 rounded-full bg-white shadow-xs"></div>
              </button>
            </div>

            <div className="flex items-center justify-between p-3 bg-surface-bright rounded-lg border border-border-subtle">
              <div>
                <div className="font-semibold text-xs text-on-surface">Third-Party Data Sharing</div>
                <div className="text-[11px] text-on-surface-variant">Share credit profile with non-affiliated underwriters.</div>
              </div>
              <button
                onClick={() => setThirdPartyShare(!thirdPartyShare)}
                className={`w-11 h-6 flex items-center rounded-full p-0.5 transition-colors ${thirdPartyShare ? 'bg-[#2563EB] justify-end' : 'bg-slate-300 justify-start'}`}
              >
                <div className="w-4 h-4 rounded-full bg-white shadow-xs"></div>
              </button>
            </div>
          </div>
        </div>

        {/* Section 2: AI Transparency & Audit Log Disclosures */}
        <div className="bg-surface rounded-xl border border-border-subtle p-6 space-y-6 shadow-xs flex flex-col justify-between">
          <div className="space-y-4">
            <div className="border-b border-border-subtle pb-3">
              <h3 className="font-bold text-base text-on-surface">AI Transparency & Rights</h3>
              <p className="text-xs text-on-surface-variant mt-0.5">AgentTrust OS institutional AI governance principles.</p>
            </div>

            <div className="space-y-3 text-xs text-on-surface-variant leading-relaxed">
              <div className="flex items-start gap-2 p-2.5 bg-surface-muted rounded-lg border border-border-subtle">
                <span className="material-symbols-outlined text-[#2563EB] text-base mt-0.5">verified_user</span>
                <div>
                  <strong className="text-on-surface block mb-0.5">Deterministic Credit Evaluation</strong>
                  AI models operate under strict deterministic rules. No protected demographic data is evaluated.
                </div>
              </div>

              <div className="flex items-start gap-2 p-2.5 bg-surface-muted rounded-lg border border-border-subtle">
                <span className="material-symbols-outlined text-[#2563EB] text-base mt-0.5">gavel</span>
                <div>
                  <strong className="text-on-surface block mb-0.5">Immutable Audit Trail</strong>
                  Every underwriting action, document scan, and policy check is recorded to an unalterable audit log.
                </div>
              </div>
            </div>
          </div>

          <div className="pt-4 border-t border-border-subtle flex items-center justify-between text-xs font-mono text-on-surface-variant">
            <span>FIPS 140-3 Cryptographic Core</span>
            <span className="text-emerald-600 font-bold">VERIFIED</span>
          </div>
        </div>
      </div>
    </div>
  );
};
