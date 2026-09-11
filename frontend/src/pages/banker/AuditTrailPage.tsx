import React, { useState, useEffect } from 'react';
import { AuditTrailLink, Badge } from '../../components/common/Primitives';
import { AuditService } from '../../services/audit.service';
import type { AuditLogEntry } from '../../types';

export const AuditTrailPage: React.FC = () => {
  const [searchTerm, setSearchTerm] = useState('');
  const [timeframe, setTimeframe] = useState('7d');
  const [logs, setLogs] = useState<AuditLogEntry[]>([]);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    setIsLoading(true);
    AuditService.getAuditLogs(searchTerm).then((res) => {
      setLogs(res);
      setIsLoading(false);
    });
  }, [searchTerm]);

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 border-b border-border-subtle pb-4">
        <div>
          <div className="text-xs font-mono uppercase text-on-surface-variant tracking-wider">
            Institutional Governance & Accountability Console
          </div>
          <h1 className="text-2xl font-bold font-headline-lg text-on-surface">
            Immutable Audit Ledger
          </h1>
        </div>

        <div className="flex items-center gap-3">
          <Badge variant="success" size="md">
            SHA-256 Merkle Proof Verified
          </Badge>
          <button className="bg-surface hover:bg-surface-muted border border-border-subtle text-xs font-semibold px-3 py-1.5 rounded-md text-on-surface transition-colors flex items-center gap-1.5">
            <span className="material-symbols-outlined text-sm">download</span>
            <span>Export Audit Pack</span>
          </button>
        </div>
      </div>

      {/* System Metrics Banner */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <div className="bg-surface p-4 rounded-xl border border-border-subtle shadow-xs">
          <span className="text-[11px] font-semibold text-on-surface-variant uppercase tracking-wider block mb-1">
            Governance Node Status
          </span>
          <div className="text-2xl font-bold font-mono text-emerald-600 tnum">99.98% Uptime</div>
          <span className="text-xs text-on-surface-variant">Zero consensus desync events</span>
        </div>

        <div className="bg-surface p-4 rounded-xl border border-border-subtle shadow-xs">
          <span className="text-[11px] font-semibold text-on-surface-variant uppercase tracking-wider block mb-1">
            Avg Processing Latency
          </span>
          <div className="text-2xl font-bold font-mono text-on-surface tnum">142 ms</div>
          <span className="text-xs text-emerald-600">Sub-200ms Target Met</span>
        </div>

        <div className="bg-surface p-4 rounded-xl border border-border-subtle shadow-xs">
          <span className="text-[11px] font-semibold text-on-surface-variant uppercase tracking-wider block mb-1">
            Unresolved Exceptions
          </span>
          <div className="text-2xl font-bold font-mono text-emerald-600 tnum">0</div>
          <span className="text-xs text-on-surface-variant">All critical overrides resolved</span>
        </div>
      </div>

      {/* Audit Log Table */}
      <div className="bg-surface rounded-xl border border-border-subtle overflow-hidden shadow-xs">
        <div className="px-6 py-4 border-b border-border-subtle bg-surface-muted/40 flex flex-col sm:flex-row items-center justify-between gap-4">
          <div className="relative w-full sm:w-72">
            <span className="material-symbols-outlined absolute left-3 top-2 text-on-surface-variant text-sm">search</span>
            <input
              type="text"
              placeholder="Search entity, action, or actor..."
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              className="w-full pl-9 pr-3 py-1.5 bg-surface border border-border-subtle rounded-md text-xs focus:outline-none focus:border-[#2563EB]"
            />
          </div>

          <div className="flex items-center gap-2 text-xs">
            <span className="font-semibold text-on-surface-variant uppercase">Timeframe:</span>
            <select
              value={timeframe}
              onChange={(e) => setTimeframe(e.target.value)}
              className="bg-surface border border-border-subtle rounded px-2 pr-6 py-1 text-xs text-on-surface focus:outline-none"
            >
              <option value="7d">Last 7 Days</option>
              <option value="30d">Last 30 Days</option>
              <option value="all">All Time</option>
            </select>
          </div>
        </div>

        <div className="overflow-x-auto">
          <table className="w-full text-left border-collapse">
            <thead>
              <tr className="bg-surface-muted border-b border-border-subtle text-[11px] font-semibold uppercase text-on-surface-variant tracking-wider">
                <th className="py-3 px-6 font-mono">Timestamp (UTC)</th>
                <th className="py-3 px-4">Actor</th>
                <th className="py-3 px-4 font-mono">Action</th>
                <th className="py-3 px-4 font-mono">Resource / Entity</th>
                <th className="py-3 px-4 text-center">Status</th>
                <th className="py-3 px-6 text-right">Evidence Hash</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-border-subtle text-sm">
              {isLoading ? (
                <tr>
                  <td colSpan={6} className="py-8 text-center text-xs text-on-surface-variant">
                    Loading audit ledger entries...
                  </td>
                </tr>
              ) : logs.map((log) => (
                <tr key={log.id} className="hover:bg-surface-muted/40 transition-colors h-14">
                  <td className="px-6 py-3 font-mono text-xs text-on-surface-variant">{log.timestamp}</td>
                  <td className="px-4 py-3">
                    <div className="flex items-center gap-2">
                      <span className={`px-1.5 py-0.5 rounded text-[10px] font-mono font-bold ${
                        log.actorType === 'SYS' ? 'bg-slate-200 text-slate-800' : log.actorType === 'MGR' ? 'bg-amber-100 text-amber-900' : 'bg-blue-100 text-blue-900'
                      }`}>
                        {log.actorType}
                      </span>
                      <span className="font-medium text-on-surface text-xs">{log.actor}</span>
                    </div>
                  </td>
                  <td className="px-4 py-3 font-mono text-xs font-semibold text-on-surface">{log.action}</td>
                  <td className="px-4 py-3 font-mono text-xs text-on-surface-variant">{log.resource}</td>
                  <td className="px-4 py-3 text-center">
                    {log.status === 'SUCCESS' && (
                      <span className="w-6 h-6 rounded-full bg-emerald-50 text-emerald-600 inline-flex items-center justify-center border border-emerald-200" title="Success">
                        <span className="material-symbols-outlined text-xs">check</span>
                      </span>
                    )}
                    {log.status === 'BLOCKED' && (
                      <span className="w-6 h-6 rounded-full bg-rose-50 text-rose-600 inline-flex items-center justify-center border border-rose-200" title="Blocked">
                        <span className="material-symbols-outlined text-xs">block</span>
                      </span>
                    )}
                  </td>
                  <td className="px-6 py-3 text-right">
                    <AuditTrailLink hash={log.hash} label={log.evidence} />
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
};
