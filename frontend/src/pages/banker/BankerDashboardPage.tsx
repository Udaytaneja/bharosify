import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { ApplicationService } from '../../services/application.service';
import type { LoanApplication } from '../../types';

export const BankerDashboardPage: React.FC = () => {
  const navigate = useNavigate();
  const [viewVariant, setViewVariant] = useState<'refined' | 'institutional'>('refined');
  const [searchTerm, setSearchTerm] = useState('');
  const [applications, setApplications] = useState<LoanApplication[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    setLoading(true);
    ApplicationService.getApplications(searchTerm).then((data) => {
      setApplications(data);
      setLoading(false);
    });
  }, [searchTerm]);

  const pendingKycList = [
    {
      entity: 'Goliath National Bank',
      id: 'V-77291',
      priority: 'HIGH PRIORITY',
      issue: 'Beneficial ownership mismatch detected in Tier 2 subsidiary.'
    },
    {
      entity: 'LexCorp Holding',
      id: 'V-77284',
      priority: 'STANDARD',
      issue: 'Awaiting translated documents from Zurich branch.'
    }
  ];

  const filteredApps = applications.filter((a: any) =>
    (a.applicantName || a.name || '').toLowerCase().includes(searchTerm.toLowerCase()) ||
    (a.id || '').toLowerCase().includes(searchTerm.toLowerCase())
  );

  return (
    <div className="space-y-6">
      {/* Header & View Variant Switcher */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 border-b border-border-subtle pb-4">
        <div>
          <div className="text-xs font-mono uppercase text-on-surface-variant tracking-wider">
            Banker Command Center • Institutional Risk Oversight
          </div>
          <h1 className="text-2xl font-bold font-headline-lg text-on-surface">
            Good morning, Vikram
          </h1>
        </div>

        <div className="flex items-center gap-3">
          {/* View Toggle */}
          <div className="bg-surface-container-high p-1 rounded-md border border-border-subtle flex items-center gap-1 text-xs">
            <button
              onClick={() => setViewVariant('refined')}
              className={`px-3 py-1.5 rounded font-medium transition-all ${
                viewVariant === 'refined' ? 'bg-surface text-on-surface shadow-xs font-semibold' : 'text-on-surface-variant hover:text-on-surface'
              }`}
            >
              Refined Dashboard
            </button>
            <button
              onClick={() => setViewVariant('institutional')}
              className={`px-3 py-1.5 rounded font-medium transition-all ${
                viewVariant === 'institutional' ? 'bg-[#0F172A] text-white shadow-xs font-semibold' : 'text-on-surface-variant hover:text-on-surface'
              }`}
            >
              Institutional Precision
            </button>
          </div>

          <button
            onClick={() => navigate('/banker/underwriting')}
            className="bg-[#2563EB] hover:bg-blue-700 text-white px-4 py-2 rounded-md font-medium text-xs flex items-center gap-2 transition-colors shadow-xs"
          >
            <span className="material-symbols-outlined text-base">play_arrow</span>
            <span>Start Case Queue</span>
          </button>
        </div>
      </div>

      {viewVariant === 'institutional' ? (
        /* Institutional Precision Variant Layout */
        <div className="grid grid-cols-12 gap-6">
          <div className="col-span-12 xl:col-span-8 space-y-6">
            {/* 3 Metric Cards */}
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
              <div className="p-4 bg-surface rounded-xl border border-border-subtle shadow-xs relative overflow-hidden">
                <div className="absolute right-0 top-0 h-full w-1 bg-[#2563EB]"></div>
                <span className="text-[11px] font-semibold text-on-surface-variant uppercase tracking-wider block mb-1">
                  Total Managed Facility
                </span>
                <span className="text-3xl font-bold font-mono text-on-surface tnum">$2.4B</span>
                <div className="mt-2 w-full h-1 bg-surface-container rounded-full overflow-hidden">
                  <div className="h-full bg-[#2563EB] w-[75%] rounded-full"></div>
                </div>
                <span className="text-[11px] font-mono text-on-surface-variant mt-1 block">75% Capacity Utilized</span>
              </div>

              <div className="p-4 bg-surface rounded-xl border border-border-subtle shadow-xs relative overflow-hidden">
                <div className="absolute right-0 top-0 h-full w-1 bg-rose-500"></div>
                <span className="text-[11px] font-semibold text-on-surface-variant uppercase tracking-wider block mb-1">
                  High-Risk Exceptions
                </span>
                <span className="text-3xl font-bold font-mono text-rose-600 tnum">5</span>
                <span className="text-[11px] font-semibold text-rose-600 block mt-3">Immediate Sign-off Required</span>
              </div>

              <div className="p-4 bg-surface rounded-xl border border-border-subtle shadow-xs relative overflow-hidden">
                <div className="absolute right-0 top-0 h-full w-1 bg-emerald-500"></div>
                <span className="text-[11px] font-semibold text-on-surface-variant uppercase tracking-wider block mb-1">
                  Automated Clearances
                </span>
                <span className="text-3xl font-bold font-mono text-emerald-600 tnum">18</span>
                <span className="text-[11px] font-mono text-emerald-600 block mt-3">Zero Policy Exceptions</span>
              </div>
            </div>

            {/* Applications Queue Table */}
            <div className="bg-surface rounded-xl border border-border-subtle shadow-xs overflow-hidden">
              <div className="px-6 py-4 border-b border-border-subtle bg-surface-muted/40 flex items-center justify-between">
                <h2 className="text-sm font-bold font-headline-sm text-on-surface">
                  Institutional Credit Queue (FIPS 140-3 Monitored)
                </h2>
                <div className="relative">
                  <span className="material-symbols-outlined absolute left-2.5 top-1.5 text-on-surface-variant text-sm">search</span>
                  <input
                    type="text"
                    placeholder="Filter ID or Name..."
                    value={searchTerm}
                    onChange={(e) => setSearchTerm(e.target.value)}
                    className="pl-8 pr-3 py-1 bg-surface border border-border-subtle rounded text-xs w-[224px] focus:outline-none focus:border-[#2563EB]"
                  />
                </div>
              </div>

              <div className="overflow-x-auto">
                <table className="w-full text-left border-collapse">
                  <thead>
                    <tr className="bg-surface-muted border-b border-border-subtle text-[11px] font-semibold uppercase text-on-surface-variant tracking-wider">
                      <th className="py-3 px-6">Entity / Applicant</th>
                      <th className="py-3 px-4 font-mono">App ID</th>
                      <th className="py-3 px-4 font-mono text-right">Credit Amount</th>
                      <th className="py-3 px-4">Risk Rating</th>
                      <th className="py-3 px-4 text-center">Action</th>
                    </tr>
                  </thead>
                  <tbody className="divide-y divide-border-subtle text-sm">
                    {loading ? (
                      <tr>
                        <td colSpan={5} className="py-8 text-center text-xs text-on-surface-variant">
                          Loading applications from backend database...
                        </td>
                      </tr>
                    ) : applications.length === 0 ? (
                      <tr>
                        <td colSpan={5} className="py-8 text-center text-xs text-on-surface-variant">
                          No credit applications currently in review queue.
                        </td>
                      </tr>
                    ) : (
                      applications.map((app: any) => (
                        <tr key={app.id} className="hover:bg-surface-muted/40 transition-colors">
                          <td className="py-3.5 px-6">
                            <span className="font-bold text-on-surface block text-sm">{app.applicantName || app.name}</span>
                            <span className="text-xs text-on-surface-variant">{app.type}</span>
                          </td>
                          <td className="py-3.5 px-4 font-mono text-xs text-on-surface-variant">{app.id}</td>
                          <td className="py-3.5 px-4 font-mono text-right font-bold text-on-surface tnum">{app.amount}</td>
                          <td className="py-3.5 px-4">
                            <span className={`text-xs font-semibold px-2 py-0.5 rounded border ${
                              (app.riskRating || app.risk) === 'High' ? 'bg-rose-50 text-rose-700 border-rose-200' : 'bg-emerald-50 text-emerald-700 border-emerald-200'
                            }`}>
                              {app.riskRating || app.risk || 'Low'} Risk
                            </span>
                          </td>
                          <td className="py-3.5 px-4 text-center">
                            <button
                              onClick={() => navigate('/banker/underwriting')}
                              className="px-3 py-1 bg-surface border border-border-subtle hover:border-[#2563EB] text-xs font-medium rounded transition-colors text-[#2563EB]"
                            >
                              Inspect Case
                            </button>
                          </td>
                        </tr>
                      ))
                    )}
                  </tbody>
                </table>
              </div>
            </div>
          </div>

          {/* Right Column: Pending KYC/AML Queue & Operational Efficiency */}
          <div className="col-span-12 xl:col-span-4 space-y-6">
            <div className="bg-surface rounded-xl border border-border-subtle overflow-hidden shadow-xs">
              <div className="p-4 bg-surface-muted border-b border-border-subtle">
                <h3 className="font-bold text-sm text-on-surface">Pending KYC / AML Review</h3>
                <p className="text-xs text-on-surface-variant">Manual underwriting override required</p>
              </div>

              <div className="divide-y divide-border-subtle">
                {pendingKycList.map((item) => (
                  <div key={item.id} className="p-4 space-y-2 hover:bg-surface-muted/80 transition-colors cursor-pointer">
                    <div className="flex justify-between items-start">
                      <div>
                        <div className="font-bold text-xs text-on-surface">{item.entity}</div>
                        <div className="font-mono text-[11px] text-on-surface-variant">ID: {item.id}</div>
                      </div>
                      <span className={`text-[10px] font-bold px-2 py-0.5 rounded border ${
                        item.priority === 'HIGH PRIORITY' ? 'bg-amber-50 text-amber-700 border-amber-200' : 'bg-slate-100 text-slate-700 border-slate-200'
                      }`}>
                        {item.priority}
                      </span>
                    </div>

                    <div className="p-2 bg-surface-bright rounded border border-border-subtle text-xs text-on-surface flex items-center gap-2">
                      <span className="material-symbols-outlined text-amber-600 text-sm">warning</span>
                      <span className="text-[11px]">{item.issue}</span>
                    </div>
                  </div>
                ))}
              </div>
            </div>

            <div className="bg-surface rounded-xl border border-border-subtle p-5 shadow-xs space-y-4">
              <h3 className="font-bold text-sm text-on-surface">Operational Efficiency</h3>
              <div className="space-y-3 text-xs">
                <div>
                  <div className="flex justify-between mb-1">
                    <span className="text-on-surface-variant">Avg. Decision Time</span>
                    <span className="font-mono font-bold text-on-surface">4.2 Hrs</span>
                  </div>
                  <div className="w-full h-1.5 bg-surface-container rounded-full overflow-hidden">
                    <div className="h-full bg-emerald-500 w-[85%] rounded-full"></div>
                  </div>
                </div>

                <div>
                  <div className="flex justify-between mb-1">
                    <span className="text-on-surface-variant">AI Auto-Resolution Rate</span>
                    <span className="font-mono font-bold text-on-surface">62%</span>
                  </div>
                  <div className="w-full h-1.5 bg-surface-container rounded-full overflow-hidden">
                    <div className="h-full bg-[#2563EB] w-[62%] rounded-full"></div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      ) : (
        /* Refined Command Center Variant Layout */
        <div className="space-y-6">
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
            <div className="bg-surface p-4 rounded-xl border border-border-subtle shadow-xs flex flex-col justify-between h-24">
              <div className="flex justify-between items-start">
                <span className="text-[11px] font-semibold text-on-surface-variant uppercase tracking-wider">
                  Applications Awaiting
                </span>
                <span className="material-symbols-outlined text-on-surface-variant text-base">inbox</span>
              </div>
              <div className="flex items-end justify-between">
                <span className="text-2xl font-bold text-on-surface font-mono tnum">24</span>
                <span className="text-xs text-emerald-600 font-medium flex items-center">
                  <span className="material-symbols-outlined text-xs">arrow_upward</span> +4 today
                </span>
              </div>
            </div>

            <div className="bg-surface p-4 rounded-xl border border-border-subtle shadow-xs flex flex-col justify-between h-24">
              <div className="flex justify-between items-start">
                <span className="text-[11px] font-semibold text-on-surface-variant uppercase tracking-wider">
                  High-Risk Cases
                </span>
                <span className="material-symbols-outlined text-rose-500 text-base">warning</span>
              </div>
              <div className="flex items-end justify-between">
                <span className="text-2xl font-bold text-rose-600 font-mono tnum">5</span>
                <span className="text-xs text-rose-600 font-medium">Requires Action</span>
              </div>
            </div>

            <div className="bg-surface p-4 rounded-xl border border-border-subtle shadow-xs flex flex-col justify-between h-24">
              <div className="flex justify-between items-start">
                <span className="text-[11px] font-semibold text-on-surface-variant uppercase tracking-wider">
                  Docs Requiring Attention
                </span>
                <span className="material-symbols-outlined text-on-surface-variant text-base">description</span>
              </div>
              <div className="flex items-end justify-between">
                <span className="text-2xl font-bold text-on-surface font-mono tnum">12</span>
                <span className="text-xs text-on-surface-variant font-medium">Pending OCR</span>
              </div>
            </div>

            <div className="bg-surface p-4 rounded-xl border border-border-subtle shadow-xs flex flex-col justify-between h-24">
              <div className="flex justify-between items-start">
                <span className="text-[11px] font-semibold text-on-surface-variant uppercase tracking-wider">
                  Approvals Today
                </span>
                <span className="material-symbols-outlined text-emerald-600 text-base">check_circle</span>
              </div>
              <div className="flex items-end justify-between">
                <span className="text-2xl font-bold text-on-surface font-mono tnum">18</span>
                <span className="text-xs text-emerald-600 font-medium">Cleared</span>
              </div>
            </div>
          </div>

          <div className="bg-surface rounded-xl border border-border-subtle shadow-xs overflow-hidden">
            <div className="px-6 py-4 border-b border-border-subtle bg-surface-muted/40 flex flex-col sm:flex-row sm:items-center justify-between gap-4">
              <div>
                <h2 className="text-base font-semibold text-on-surface font-headline-sm">
                  Applications Requiring Attention
                </h2>
                <p className="text-xs text-on-surface-variant">
                  Active queue with AI trust scores and assisted analysis flags
                </p>
              </div>

              <div className="flex items-center gap-3">
                <div className="relative">
                  <span className="material-symbols-outlined absolute left-3 top-2 text-on-surface-variant text-sm">search</span>
                  <input
                    type="text"
                    placeholder="Search ID or Name..."
                    value={searchTerm}
                    onChange={(e) => setSearchTerm(e.target.value)}
                    className="pl-9 pr-3 py-1.5 bg-surface border border-border-subtle rounded-md text-xs w-56 focus:outline-none focus:border-[#2563EB]"
                  />
                </div>
              </div>
            </div>

            <div className="overflow-x-auto">
              <table className="w-full text-left border-collapse">
                <thead>
                  <tr className="bg-surface-muted border-b border-border-subtle text-[11px] font-semibold uppercase text-on-surface-variant tracking-wider">
                    <th className="py-3 px-6">Applicant</th>
                    <th className="py-3 px-4 font-mono">App ID</th>
                    <th className="py-3 px-4 text-right font-mono">Amount</th>
                    <th className="py-3 px-4">Risk</th>
                    <th className="py-3 px-4">Trust Score</th>
                    <th className="py-3 px-4">Assisted Analysis</th>
                    <th className="py-3 px-4">Last Updated</th>
                    <th className="py-3 px-4 text-center">Action</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-border-subtle text-sm">
                  {filteredApps.map((app: any) => (
                    <tr key={app.id} className="hover:bg-surface-muted/50 transition-colors group">
                      <td className="py-3.5 px-6">
                        <div className="font-semibold text-on-surface">{app.applicantName || app.name}</div>
                        <div className="text-xs text-on-surface-variant">{app.type}</div>
                      </td>
                      <td className="py-3.5 px-4 font-mono text-xs text-on-surface-variant">{app.id}</td>
                      <td className="py-3.5 px-4 font-mono text-right font-medium text-on-surface tnum">{app.amount}</td>
                      <td className="py-3.5 px-4">
                        <div className="flex items-center gap-1.5">
                          <span className={`w-2 h-2 rounded-full ${(app.riskRating || app.risk) === 'High' ? 'bg-rose-500' : (app.riskRating || app.risk) === 'Elevated' ? 'bg-amber-500' : 'bg-emerald-500'}`}></span>
                          <span className="text-xs font-medium">{app.riskRating || app.risk || 'Low'}</span>
                        </div>
                      </td>
                      <td className="py-3.5 px-4">
                        <div className="flex items-center gap-2">
                          <span className="font-mono text-xs font-semibold w-6 text-right tnum">{app.trustScore || app.score || 88}</span>
                          <div className="w-24 h-1.5 bg-surface-container rounded-full overflow-hidden">
                            <div
                              className={`h-full rounded-full ${(app.trustScore || app.score || 88) < 50 ? 'bg-rose-500' : (app.trustScore || app.score || 88) < 80 ? 'bg-amber-500' : 'bg-emerald-500'}`}
                              style={{ width: `${app.trustScore || app.score || 88}%` }}
                            ></div>
                          </div>
                        </div>
                      </td>
                      <td className="py-3.5 px-4">
                        <div className="flex flex-wrap gap-1">
                          {(app.assistedFlags || app.flags || ['Verified']).map((flag: string, i: number) => (
                            <span key={i} className="text-[10px] bg-surface-muted border border-border-subtle px-1.5 py-0.5 rounded text-on-surface-variant font-medium">
                              {flag}
                            </span>
                          ))}
                        </div>
                      </td>
                      <td className="py-3.5 px-4 text-xs text-on-surface-variant">{app.lastUpdated || app.updated || 'Recently'}</td>
                      <td className="py-3.5 px-4 text-center">
                        <button
                          onClick={() => navigate('/banker/underwriting')}
                          className="px-3 py-1 bg-surface border border-border-subtle hover:border-[#2563EB] text-xs font-medium rounded transition-colors text-[#2563EB]"
                        >
                          Inspect
                        </button>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};
