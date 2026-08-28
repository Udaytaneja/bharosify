import React, { useState } from 'react';
import { Badge, Button } from '../../components/common/Primitives';

export const GovernancePage: React.FC = () => {
  const [activeTab, setActiveTab] = useState<'policy' | 'thresholds' | 'permissions' | 'gateways'>('policy');
  const [dtiRatio, setDtiRatio] = useState(43.5);
  const [trustIndexCutoff, setTrustIndexCutoff] = useState(720);
  const [rule1Active, setRule1Active] = useState(true);
  const [rule2Active, setRule2Active] = useState(true);
  const [saveStatus, setSaveStatus] = useState<string | null>(null);

  // Clean Service Abstraction for Config Persistence
  const handleSaveConfig = () => {
    setSaveStatus('Persisting governance policies to FIPS 140-3 Vault...');
    setTimeout(() => {
      setSaveStatus('Governance Configuration Saved & Signed by Vikram Singh (Lead Underwriter)');
      setTimeout(() => setSaveStatus(null), 4000);
    }, 1200);
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 border-b border-border-subtle pb-4">
        <div>
          <div className="text-xs font-mono uppercase text-on-surface-variant tracking-wider">
            Institutional Risk Policy & Decision Controls
          </div>
          <h1 className="text-2xl font-bold font-headline-lg text-on-surface">
            Governance & System Control
          </h1>
          <p className="text-xs text-on-surface-variant mt-1">
            Configure automated decision thresholds, access policies, and AI audit parameters.
          </p>
        </div>

        <div className="flex items-center gap-3">
          <Badge variant="success" size="md">
            Active Mode: Strict (Dual-Auth Enforced)
          </Badge>
          <Button variant="primary" size="sm" onClick={handleSaveConfig} className="bg-[#2563EB]">
            Save Configuration
          </Button>
        </div>
      </div>

      {saveStatus && (
        <div className="p-3 bg-emerald-50 text-emerald-800 border border-emerald-200 rounded-lg text-xs font-semibold font-mono animate-fade-in">
          ✓ {saveStatus}
        </div>
      )}

      {/* Grid Layout */}
      <div className="grid grid-cols-12 gap-6">
        {/* Left Sub-Nav Tabs (2 cols / ~16%) */}
        <div className="col-span-12 md:col-span-3 lg:col-span-2 space-y-1">
          <button
            onClick={() => setActiveTab('policy')}
            className={`w-full text-left px-4 py-2.5 text-xs font-semibold rounded-md transition-colors border-l-4 ${
              activeTab === 'policy' ? 'bg-[#2563EB]/10 text-[#2563EB] border-[#2563EB]' : 'text-on-surface-variant border-transparent hover:bg-surface-muted'
            }`}
          >
            Policy Rules
          </button>
          <button
            onClick={() => setActiveTab('thresholds')}
            className={`w-full text-left px-4 py-2.5 text-xs font-semibold rounded-md transition-colors border-l-4 ${
              activeTab === 'thresholds' ? 'bg-[#2563EB]/10 text-[#2563EB] border-[#2563EB]' : 'text-on-surface-variant border-transparent hover:bg-surface-muted'
            }`}
          >
            Risk Thresholds
          </button>
          <button
            onClick={() => setActiveTab('permissions')}
            className={`w-full text-left px-4 py-2.5 text-xs font-semibold rounded-md transition-colors border-l-4 ${
              activeTab === 'permissions' ? 'bg-[#2563EB]/10 text-[#2563EB] border-[#2563EB]' : 'text-on-surface-variant border-transparent hover:bg-surface-muted'
            }`}
          >
            User Permissions
          </button>
          <button
            onClick={() => setActiveTab('gateways')}
            className={`w-full text-left px-4 py-2.5 text-xs font-semibold rounded-md transition-colors border-l-4 flex items-center justify-between ${
              activeTab === 'gateways' ? 'bg-[#2563EB]/10 text-[#2563EB] border-[#2563EB]' : 'text-on-surface-variant border-transparent hover:bg-surface-muted'
            }`}
          >
            <span>AI Gateways</span>
            <span className="material-symbols-outlined text-sm">smart_toy</span>
          </button>
        </div>

        {/* Right Settings Panel (10 cols / ~84%) */}
        <div className="col-span-12 md:col-span-9 lg:col-span-10 space-y-6">
          {/* Global Risk Thresholds Card */}
          <div className="bg-surface border border-border-subtle rounded-xl overflow-hidden shadow-xs">
            <div className="px-6 py-4 border-b border-border-subtle bg-surface-muted/40 flex items-center justify-between">
              <h2 className="font-bold text-sm text-on-surface">Global Risk Thresholds</h2>
              <span className="px-2 py-0.5 bg-slate-100 text-slate-700 font-mono text-[11px] rounded border border-border-subtle uppercase">
                Active Mode: Strict
              </span>
            </div>

            <div className="p-6 grid grid-cols-1 lg:grid-cols-2 gap-6">
              {/* DTI Threshold */}
              <div className="space-y-2">
                <div className="flex justify-between items-center text-xs font-semibold">
                  <span>Maximum DTI Ratio</span>
                  <span className="font-mono text-[#2563EB] text-sm">{dtiRatio.toFixed(1)}%</span>
                </div>
                <p className="text-[11px] text-on-surface-variant">Applications exceeding this threshold require Level 2 Risk Officer sign-off.</p>
                <div className="flex items-center gap-4 pt-1">
                  <input
                    type="range"
                    min={30}
                    max={60}
                    step={0.5}
                    value={dtiRatio}
                    onChange={(e) => setDtiRatio(Number(e.target.value))}
                    className="w-full accent-[#2563EB] [&::-webkit-slider-thumb]:w-[18px] [&::-webkit-slider-thumb]:h-[18px]"
                  />
                  <input
                    type="text"
                    value={dtiRatio}
                    onChange={(e) => setDtiRatio(Number(e.target.value) || 40)}
                    className="w-20 px-2 py-1 font-mono text-xs text-right border border-border-subtle rounded focus:outline-none focus:border-[#2563EB]"
                  />
                </div>
              </div>

              {/* Trust Index Cutoff */}
              <div className="space-y-2">
                <div className="flex justify-between items-center text-xs font-semibold">
                  <span>Minimum Trust Index Cutoff</span>
                  <span className="font-mono text-[#2563EB] text-sm">{trustIndexCutoff}</span>
                </div>
                <p className="text-[11px] text-on-surface-variant">Base Trust Score required for automated fast-track routing.</p>
                <div className="flex items-center gap-4 pt-1">
                  <input
                    type="range"
                    min={500}
                    max={850}
                    step={10}
                    value={trustIndexCutoff}
                    onChange={(e) => setTrustIndexCutoff(Number(e.target.value))}
                    className="w-full accent-[#2563EB] [&::-webkit-slider-thumb]:w-[18px] [&::-webkit-slider-thumb]:h-[18px]"
                  />
                  <input
                    type="text"
                    value={trustIndexCutoff}
                    onChange={(e) => setTrustIndexCutoff(Number(e.target.value) || 700)}
                    className="w-20 px-2 py-1 font-mono text-xs text-right border border-border-subtle rounded focus:outline-none focus:border-[#2563EB]"
                  />
                </div>
              </div>
            </div>
          </div>

          {/* Decision Guard Rules Table */}
          <div className="bg-surface border border-border-subtle rounded-xl overflow-hidden shadow-xs">
            <div className="px-6 py-4 border-b border-border-subtle bg-surface-muted/40 flex items-center justify-between">
              <div className="flex items-center gap-2">
                <h2 className="font-bold text-sm text-on-surface">Decision Guard Rules</h2>
                <span className="material-symbols-outlined text-emerald-600 text-sm">verified</span>
              </div>
              <button className="px-3 py-1.5 bg-surface text-on-surface border border-border-subtle rounded text-xs font-medium hover:bg-surface-muted transition-colors flex items-center gap-1">
                <span className="material-symbols-outlined text-sm">add</span> + Add Guard Rule
              </button>
            </div>

            <div className="overflow-x-auto">
              <table className="w-full text-left border-collapse">
                <thead>
                  <tr className="bg-surface-muted border-b border-border-subtle text-[11px] font-semibold uppercase text-on-surface-variant tracking-wider">
                    <th className="py-3 px-6">Rule Name</th>
                    <th className="py-3 px-4 font-mono">Condition</th>
                    <th className="py-3 px-4">Action</th>
                    <th className="py-3 px-4 text-center">Status</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-border-subtle text-sm">
                  <tr className="hover:bg-surface-muted/40 transition-colors h-14">
                    <td className="px-6 py-3 font-semibold text-on-surface text-xs">Income Verification Variance</td>
                    <td className="px-4 py-3 font-mono text-xs text-on-surface-variant">Stated vs Verified &gt; 15%</td>
                    <td className="px-4 py-3">
                      <span className="px-2 py-0.5 bg-rose-50 text-rose-700 border border-rose-200 text-[11px] font-bold rounded uppercase">
                        Flag for Manual Review
                      </span>
                    </td>
                    <td className="px-4 py-3 text-center">
                      <button
                        onClick={() => setRule1Active(!rule1Active)}
                        className={`w-9 h-5 flex items-center rounded-full p-0.5 transition-colors mx-auto ${rule1Active ? 'bg-[#2563EB] justify-end' : 'bg-slate-300 justify-start'}`}
                      >
                        <div className="w-4 h-4 rounded-full bg-white shadow-xs"></div>
                      </button>
                    </td>
                  </tr>

                  <tr className="hover:bg-surface-muted/40 transition-colors h-14">
                    <td className="px-6 py-3 font-semibold text-on-surface text-xs">High Risk Geography</td>
                    <td className="px-4 py-3 font-mono text-xs text-on-surface-variant">Property ZIP in Blocklist</td>
                    <td className="px-4 py-3">
                      <span className="px-2 py-0.5 bg-amber-50 text-amber-700 border border-amber-200 text-[11px] font-bold rounded uppercase">
                        Require Supervisor Audit
                      </span>
                    </td>
                    <td className="px-4 py-3 text-center">
                      <button
                        onClick={() => setRule2Active(!rule2Active)}
                        className={`w-9 h-5 flex items-center rounded-full p-0.5 transition-colors mx-auto ${rule2Active ? 'bg-[#2563EB] justify-end' : 'bg-slate-300 justify-start'}`}
                      >
                        <div className="w-4 h-4 rounded-full bg-white shadow-xs"></div>
                      </button>
                    </td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>

          {/* AI Output Validation Callout Panel */}
          <div className="bg-surface-muted border border-border-subtle rounded-xl p-6 relative overflow-hidden space-y-3">
            <div className="flex items-start justify-between">
              <div>
                <div className="flex items-center gap-2 mb-1">
                  <h3 className="font-bold text-sm text-on-surface">AI Output Validation & Compliance Gateway</h3>
                  <span className="px-2 py-0.5 bg-[#2563EB] text-white rounded text-[10px] uppercase font-bold tracking-widest">Active</span>
                </div>
                <p className="text-xs text-on-surface-variant max-w-xl leading-relaxed">
                  All generative insights and predictive models are currently subjected to secondary deterministic checks. Audit trails are retained for 7 years per compliance mandates.
                </p>
              </div>

              <button
                onClick={handleSaveConfig}
                className="px-4 py-2 bg-[#2563EB] text-white rounded-md font-medium text-xs shadow-xs hover:bg-blue-700 transition-colors"
              >
                Save Configuration
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};
