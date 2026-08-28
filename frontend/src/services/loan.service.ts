import type { ActiveLoanFacility, PaymentScheduleItem } from '../types';
import { apiClient } from '../api/client';

export class LoanService {
  static async getActiveFacility(): Promise<ActiveLoanFacility | null> {
    try {
      const response = await apiClient.get<any>('/loans');
      const items = Array.isArray(response.data) ? response.data : response.data?.items;
      if (items && items.length > 0) {
        const item = items[0];

        // Fetch repayment schedule for this loan
        let scheduleItems: PaymentScheduleItem[] = [];
        try {
          const repRes = await apiClient.get<any>(`/repayments/${item.id}`);
          const repList = Array.isArray(repRes.data) ? repRes.data : repRes.data?.items;
          if (repList && repList.length > 0) {
            scheduleItems = repList.map((r: any, idx: number) => ({
              num: String(idx + 1).padStart(2, '0'),
              dueDate: r.due_date ? new Date(r.due_date).toLocaleDateString('en-US', { month: 'short', day: '2-digit', year: 'numeric' }) : 'Upcoming',
              principal: `$${(Number(r.amount) * 0.8 || 0).toFixed(2)}`,
              interest: `$${(Number(r.amount) * 0.2 || 0).toFixed(2)}`,
              total: `$${(Number(r.amount) || 0).toFixed(2)}`,
              status: r.status === 'paid' ? 'PAID' : r.status === 'upcoming' ? 'DUE SOON' : 'SCHEDULED',
            }));
          }
        } catch {
          // If no repayments returned, keep empty schedule
        }

        const orig = Number(item.principal) || 0;
        const out = Number(item.outstanding_amount) || 0;
        const percentPaid = orig > 0 ? Math.round(((orig - out) / orig) * 1000) / 10 : 0;

        return {
          facilityId: `L-FACILITY-${item.id}`,
          facilityName: 'Commercial Credit Facility',
          category: 'Commercial Term Loan',
          principalOutstanding: out,
          originalAmount: orig,
          percentPaid,
          interestRate: `${item.interest_rate || 8.5}%`,
          interestPaidYtd: 0,
          maturityDate: item.maturity_date ? new Date(item.maturity_date).toLocaleDateString('en-US', { month: 'short', day: '2-digit', year: 'numeric' }) : 'TBD',
          nextPaymentDueDate: scheduleItems[0]?.dueDate || 'TBD',
          nextPaymentAmount: scheduleItems[0] ? Number(scheduleItems[0].total.replace(/[^0-9.]/g, '')) || 0 : 0,
          schedule: scheduleItems,
        };
      }
    } catch (err) {
      console.warn('Real API getActiveFacility error:', err);
    }
    return null;
  }
}
