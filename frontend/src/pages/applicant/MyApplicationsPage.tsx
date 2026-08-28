import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { ApplicationService } from '../../services/application.service';
import type { LoanApplication } from '../../types';

export const MyApplicationsPage: React.FC = () => {
  const navigate = useNavigate();
  const [filter, setFilter] = useState<'all' | 'under_review' | 'active' | 'closed'>('all');
  const [applications, setApplications] = useState<LoanApplication[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    ApplicationService.getApplications().then((data) => {
      setApplications(data);
      setLoading(false);
    });
  }, []);

  const filteredApps = applications.filter((app) => {
    if (filter === 'under_review') return app.status === 'UNDER_REVIEW';
    if (filter === 'active') return app.status === 'APPROVED_ACTIVE';
    if (filter === 'closed') return app.status === 'COMPLETED';
    return true;
  });

  return (
    <div className="space-y-8">
      {/* Header Section */}
      <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4 border-b border-border-subtle pb-4">
        <div>
          <h1 className="text-3xl font-bold font-display text-on-surface tracking-tight">
            My Applications
          </h1>
          <p className="text-sm text-on-surface-variant mt-1">
            Track and manage your current and past loan applications.
          </p>
        </div>

        <button
          onClick={() => navigate('/applicant/documents')}
          className="bg-[#2563EB] text-white font-medium text-xs px-4 py-2.5 rounded-lg shadow-xs hover:bg-blue-700 transition-all flex items-center gap-2"
        >
          <span className="material-symbols-outlined text-base">add</span>
          <span>Start New Application</span>
        </button>
      </div>

      {/* Summary Cards */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6 w-full">
        {/* Card 1 */}
        <div
          onClick={() => setFilter('all')}
          className={`bg-surface border rounded-xl p-5 shadow-xs transition-colors duration-100 cursor-pointer ${
            filter === 'all' ? 'border-[#2563EB] bg-[#2563EB]/5' : 'border-border-subtle hover:bg-surface-muted'
          }`}
        >
          <div className="flex flex-col gap-3">
            <div className="flex justify-between items-center">
              <div className="w-10 h-10 rounded-xl bg-blue-50 text-[#2563EB] flex items-center justify-center">
                <span className="material-symbols-outlined text-xl">description</span>
              </div>
              <span className="text-3xl font-bold font-mono text-on-surface tnum">{applications.length}</span>
            </div>
            <div>
              <p className="text-xs font-semibold text-on-surface-variant uppercase tracking-widest">Total Applications</p>
              <p className="text-xs text-on-surface-variant/80 mt-0.5">Across all credit categories</p>
            </div>
          </div>
        </div>

        {/* Card 2 */}
        <div
          onClick={() => setFilter('under_review')}
          className={`bg-surface border rounded-xl p-5 shadow-xs transition-colors duration-100 cursor-pointer ${
            filter === 'under_review' ? 'border-amber-500 bg-amber-50/50' : 'border-border-subtle hover:bg-surface-muted'
          }`}
        >
          <div className="flex flex-col gap-3">
            <div className="flex justify-between items-center">
              <div className="w-10 h-10 rounded-xl bg-amber-50 text-amber-700 flex items-center justify-center">
                <span className="material-symbols-outlined text-xl">pending_actions</span>
              </div>
              <span className="text-3xl font-bold font-mono text-on-surface tnum">
                {applications.filter(a => a.status === 'UNDER_REVIEW').length}
              </span>
            </div>
            <div>
              <p className="text-xs font-semibold text-on-surface-variant uppercase tracking-widest">Under Review</p>
              <p className="text-xs text-on-surface-variant/80 mt-0.5">Awaiting underwriting verification</p>
            </div>
          </div>
        </div>

        {/* Card 3 */}
        <div
          onClick={() => setFilter('active')}
          className={`bg-surface border rounded-xl p-5 shadow-xs transition-colors duration-100 cursor-pointer ${
            filter === 'active' ? 'border-emerald-500 bg-emerald-50/50' : 'border-border-subtle hover:bg-surface-muted'
          }`}
        >
          <div className="flex flex-col gap-3">
            <div className="flex justify-between items-center">
              <div className="w-10 h-10 rounded-xl bg-emerald-50 text-emerald-700 flex items-center justify-center">
                <span className="material-symbols-outlined text-xl">check_circle</span>
              </div>
              <span className="text-3xl font-bold font-mono text-on-surface tnum">
                {applications.filter(a => a.status === 'APPROVED_ACTIVE' || a.status === 'COMPLETED').length}
              </span>
            </div>
            <div>
              <p className="text-xs font-semibold text-on-surface-variant uppercase tracking-widest">Approved / Completed</p>
              <p className="text-xs text-on-surface-variant/80 mt-0.5">Successfully processed</p>
            </div>
          </div>
        </div>
      </div>

      {/* Applications Table */}
      <div className="bg-surface border border-border-subtle rounded-xl overflow-hidden shadow-xs">
        <div className="bg-surface-muted/40 border-b border-border-subtle px-6 py-4 flex items-center justify-between">
          <h2 className="font-bold text-base text-on-surface">Application History</h2>
          <div className="flex gap-2">
            <button
              onClick={() => setFilter('all')}
              className={`text-xs px-3 py-1 rounded-md border font-medium ${
                filter === 'all' ? 'bg-surface text-on-surface border-border-subtle shadow-2xs' : 'text-on-surface-variant border-transparent'
              }`}
            >
              Show All
            </button>
          </div>
        </div>

        <div className="w-full overflow-x-auto">
          {loading ? (
            <div className="p-8 text-center text-xs font-mono text-on-surface-variant">Loading application ledger...</div>
          ) : (
            <table className="w-full text-left border-collapse min-w-[700px]">
              <thead>
                <tr className="bg-surface-muted border-b border-border-subtle text-[11px] font-semibold uppercase text-on-surface-variant tracking-wider">
                  <th className="py-3 px-6">Application Type</th>
                  <th className="py-3 px-4 font-mono text-right">Amount</th>
                  <th className="py-3 px-4 font-mono">Date Submitted</th>
                  <th className="py-3 px-4">Current Stage</th>
                  <th className="py-3 px-4 text-center">Status</th>
                  <th className="py-3 px-6 text-right">Action</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-border-subtle text-sm">
                {filteredApps.map((app) => (
                  <tr key={app.id} className="hover:bg-surface-muted/40 transition-colors h-14">
                    <td className="px-6 py-3">
                      <div className="flex items-center gap-3">
                        <div className="w-8 h-8 rounded-lg bg-surface-muted flex items-center justify-center text-on-surface-variant border border-border-subtle">
                          <span className="material-symbols-outlined text-base">description</span>
                        </div>
                        <div>
                          <span className="font-bold text-on-surface block text-sm">{app.type}</span>
                          <span className="text-[11px] text-on-surface-variant font-mono">{app.id}</span>
                        </div>
                      </div>
                    </td>
                    <td className="px-4 py-3 font-mono font-bold text-right text-on-surface tnum">{app.amount}</td>
                    <td className="px-4 py-3 font-mono text-xs text-on-surface-variant">{app.dateSubmitted}</td>
                    <td className="px-4 py-3 text-xs text-on-surface-variant font-medium">{app.stage}</td>
                    <td className="px-4 py-3 text-center">
                      {app.status === 'UNDER_REVIEW' && (
                        <span className="px-2.5 py-1 rounded-full bg-amber-50 text-amber-700 border border-amber-200 text-[11px] font-semibold uppercase tracking-wider">
                          Under Review
                        </span>
                      )}
                      {app.status === 'APPROVED_ACTIVE' && (
                        <span className="px-2.5 py-1 rounded-full bg-emerald-50 text-emerald-700 border border-emerald-200 text-[11px] font-semibold uppercase tracking-wider">
                          Approved & Active
                        </span>
                      )}
                      {app.status === 'COMPLETED' && (
                        <span className="px-2.5 py-1 rounded-full bg-slate-100 text-slate-700 border border-slate-200 text-[11px] font-semibold uppercase tracking-wider">
                          Completed
                        </span>
                      )}
                    </td>
                    <td className="px-6 py-3 text-right">
                      <button
                        onClick={() => navigate('/applicant/loans')}
                        className="text-xs text-[#2563EB] hover:underline font-semibold uppercase tracking-wider"
                      >
                        Inspect
                      </button>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          )}
        </div>
      </div>
    </div>
  );
};
