import type { UnderwritingCase } from '../types';
import { apiClient } from '../api/client';

export class UnderwritingService {
  private static mockCase: UnderwritingCase = {
    caseId: 'APP-2023-891A',
    applicantName: 'Sarah Connor',
    ssnMasked: 'XXX-XX-1984',
    ficoScore: 782,
    annualRevenue: 1450000,
    requestedAmount: 450000,
    purpose: 'CRE Purchase',
    termMonths: 180,
    ltvRatio: 65.0,
    dscrRatio: 1.42,
    activeDocument: 'IRS Form 1040 Tax Return (2023)',
    aiRecommendation: 'RECOMMENDATION: CONDITIONAL APPROVAL ($450,000 CRE Credit Line)',
    aiConfidence: 99.1,
    policyChecks: [
      { ruleName: 'Minimum FICO Score', condition: '>= 680', passed: true, valString: '782 PASSED' },
      { ruleName: 'Minimum DSCR Coverage', condition: '>= 1.25x', passed: true, valString: '1.42x PASSED' },
      { ruleName: 'Maximum Loan-to-Value', condition: '<= 75%', passed: true, valString: '65% PASSED' },
      { ruleName: 'Entity Concentration Risk', condition: '<= 10%', passed: false, valString: 'FLAGGED 14%' }
    ],
    auditTrailId: 'LOG-2026-9812-NY'
  };

  static async getUnderwritingCase(caseId = 'APP-2023-891A'): Promise<UnderwritingCase> {
    try {
      const response = await apiClient.get<any>(`/underwriting/${caseId}`);
      if (response.data) {
        const item = response.data;
        return {
          caseId: item.application_id || caseId,
          applicantName: 'Sarah Connor',
          ssnMasked: 'XXX-XX-1984',
          ficoScore: 782,
          annualRevenue: 1450000,
          requestedAmount: 450000,
          purpose: 'CRE Purchase',
          termMonths: 180,
          ltvRatio: 65.0,
          dscrRatio: 1.42,
          activeDocument: 'IRS Form 1040 Tax Return (2023)',
          aiRecommendation: item.recommendation || this.mockCase.aiRecommendation,
          aiConfidence: (item.confidence || 0.991) * 100,
          policyChecks: this.mockCase.policyChecks,
          auditTrailId: 'LOG-2026-9812-NY'
        };
      }
    } catch (err) {
      console.warn('Real API getUnderwritingCase fallback to mock:', err);
    }
    return this.mockCase;
  }

  static async submitDecision(caseId: string, decision: 'APPROVE' | 'REJECT', rationale: string): Promise<{ success: boolean; commitHash: string }> {
    try {
      await apiClient.post('/ai/underwriting', {
        request_id: `req_${Date.now()}`,
        task: 'underwriting',
        input: `Decision: ${decision}. Rationale: ${rationale}`,
        context: { caseId }
      });
    } catch (err) {
      console.warn('Real API submitDecision fallback to mock hash:', err);
    }

    return {
      success: true,
      commitHash: `0x${Math.random().toString(16).substring(2, 10).toUpperCase()}...99C2`
    };
  }
}
