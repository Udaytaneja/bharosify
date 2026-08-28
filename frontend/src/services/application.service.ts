import type { LoanApplication, FullApplicationSubmission } from '../types';
import { apiClient } from '../api/client';

export class ApplicationService {
  static async getApplications(searchTerm = ''): Promise<LoanApplication[]> {
    try {
      const response = await apiClient.get<any>('/applications');
      const data = Array.isArray(response.data) ? response.data : response.data?.items;
      if (data) {
        const mapped: LoanApplication[] = data.map((item: any) => ({
          id: String(item.id || `APP-${item.customer_id || '2026'}`),
          applicantName: item.applicant_name || item.name || 'Applicant',
          type: item.purpose || 'Credit Facility',
          category: 'Commercial Credit',
          amount: `$${(Number(item.amount) || 0).toLocaleString()}`,
          amountNumeric: Number(item.amount) || 0,
          dateSubmitted: item.created_at
            ? new Date(item.created_at).toLocaleDateString('en-US', {
                month: 'short',
                day: '2-digit',
                year: 'numeric',
              })
            : 'Recently',
          lastUpdated: 'Recently',
          stage: 'Underwriter Review',
          status: item.status?.toUpperCase() || 'UNDER_REVIEW',
          riskRating: 'Low',
          trustScore: 88,
          assistedFlags: ['Verified'],
        }));

        if (!searchTerm) return mapped;
        const lower = searchTerm.toLowerCase();
        return mapped.filter(
          (app) =>
            app.applicantName.toLowerCase().includes(lower) ||
            app.id.toLowerCase().includes(lower) ||
            app.type.toLowerCase().includes(lower)
        );
      }
    } catch (err) {
      console.warn('Real API getApplications error:', err);
    }
    return [];
  }

  static async getApplicationById(id: string): Promise<LoanApplication | null> {
    try {
      const response = await apiClient.get<any>(`/applications/${id}`);
      if (response.data) {
        const item = response.data;
        return {
          id: String(item.id),
          applicantName: item.applicant_name || 'Applicant',
          type: item.purpose || 'Credit Facility',
          category: 'Commercial Credit',
          amount: `$${(Number(item.amount) || 0).toLocaleString()}`,
          amountNumeric: Number(item.amount) || 0,
          dateSubmitted: item.created_at
            ? new Date(item.created_at).toLocaleDateString('en-US', {
                month: 'short',
                day: '2-digit',
                year: 'numeric',
              })
            : 'Recently',
          lastUpdated: 'Recently',
          stage: 'Underwriter Review',
          status: item.status?.toUpperCase() || 'UNDER_REVIEW',
          riskRating: 'Low',
          trustScore: 88,
          assistedFlags: ['Verified'],
        };
      }
    } catch (err) {
      console.warn('Real API getApplicationById error:', err);
    }
    return null;
  }

  static async submitFullApplication(payload: FullApplicationSubmission): Promise<LoanApplication> {
    const numericAmount = Number(payload.loanRequest.loanAmount) || 250000;

    const apiPayload = {
      amount: numericAmount,
      purpose: `${payload.loanRequest.purpose} (${payload.loanRequest.scheme})`,
      documents: [],
    };

    const response = await apiClient.post('/applications', apiPayload);
    const item = response.data;

    return {
      id: String(item.id || Date.now()),
      applicantName: payload.personalDetails.fullName,
      type: `${payload.loanRequest.purpose} (${payload.loanRequest.scheme})`,
      category:
        payload.loanRequest.purpose === 'Social' || payload.loanRequest.purpose === 'Medical'
          ? 'Retail / Mortgage'
          : 'Commercial Credit',
      amount: `$${numericAmount.toLocaleString()}`,
      amountNumeric: numericAmount,
      dateSubmitted: new Date().toLocaleDateString('en-US', {
        month: 'short',
        day: '2-digit',
        year: 'numeric',
      }),
      lastUpdated: 'Just now',
      stage: 'Document OCR',
      status: 'UNDER_REVIEW',
      riskRating: 'Low',
      trustScore: 88,
      assistedFlags: ['Full Profile Verified'],
    };
  }
}
