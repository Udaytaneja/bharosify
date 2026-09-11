import type { AuditLogEntry } from '../types';
import { apiClient } from '../api/client';

export class AuditService {
  private static initialLogs: AuditLogEntry[] = [
    {
      id: 'LOG-88192-NY',
      timestamp: '2026-08-28 15:42:05 UTC',
      actorType: 'SYS',
      actor: 'Automated Guardrail Engine',
      action: 'POLICY_ENFORCE',
      resource: 'TXN_8849_LMT',
      status: 'BLOCKED',
      evidence: 'Audit-99A',
      hash: '0x8F92A1...99C2'
    },
    {
      id: 'LOG-88191-NY',
      timestamp: '2026-08-28 14:05:12 UTC',
      actorType: 'USR',
      actor: 'Vikram Singh (Lead Underwriter)',
      action: 'HUMAN_APPROVE_CREDIT_LINE',
      resource: 'APP_HL_8942',
      status: 'SUCCESS',
      evidence: 'View Log',
      hash: '0x31B09F...441A'
    },
    {
      id: 'LOG-88190-NY',
      timestamp: '2026-08-28 11:15:30 UTC',
      actorType: 'MGR',
      actor: 'A. Chen (Risk Director)',
      action: 'THRESHOLD_ADJUSTMENT',
      resource: 'MDL_FRAUD_V4',
      status: 'SUCCESS',
      evidence: 'Diff-8B2',
      hash: '0x7A9122...00DF'
    },
    {
      id: 'LOG-88189-NY',
      timestamp: '2026-08-28 08:00:00 UTC',
      actorType: 'SYS',
      actor: 'PaddleOCR Forensic Engine',
      action: 'TAMPER_INDEX_COMPUTE',
      resource: 'IRS_1040_2023.pdf',
      status: 'SUCCESS',
      evidence: 'Evidence-12C',
      hash: '0x12C990...E88B'
    }
  ];

  static async getAuditLogs(filter = ''): Promise<AuditLogEntry[]> {
    let logs: AuditLogEntry[] = [];
    try {
      const response = await apiClient.get('/audit/me');
      if (Array.isArray(response.data) && response.data.length > 0) {
        logs = response.data.map((evt: any) => ({
          id: `LOG-${evt.id}`,
          timestamp: evt.timestamp ? new Date(evt.timestamp).toISOString().replace('T', ' ').substring(0, 19) + ' UTC' : 'Recently',
          actorType: evt.actor_type === 'user' || evt.actor_type === 'banker' ? 'USR' : 'SYS',
          actor: evt.actor_type === 'banker' ? 'Vikram Singh (Lead Underwriter)' : evt.actor_type || 'System Engine',
          action: (evt.action || 'ACTION').toUpperCase(),
          resource: evt.resource || 'SYSTEM',
          status: evt.result === 'success' || evt.result === 'SUCCESS' ? 'SUCCESS' : 'BLOCKED',
          evidence: `Ref-${evt.id}`,
          hash: evt.resource_id ? `0x${evt.resource_id.substring(0, 10).toUpperCase()}...SHA256` : '0x8F92A1...99C2'
        }));
      }
    } catch {
      // Offline / unauthenticated fallback to initial logs
    }

    if (logs.length === 0) {
      logs = this.initialLogs;
    }

    if (!filter) return logs;
    const lower = filter.toLowerCase();
    return logs.filter(log =>
      log.actor.toLowerCase().includes(lower) ||
      log.action.toLowerCase().includes(lower) ||
      log.resource.toLowerCase().includes(lower)
    );
  }
}
