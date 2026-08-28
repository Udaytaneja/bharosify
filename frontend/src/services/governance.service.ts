import type { GovernanceConfig } from '../types';

export class GovernanceService {
  private static mockConfig: GovernanceConfig = {
    dtiRatioMax: 43.5,
    trustIndexCutoffMin: 720,
    aiAutonomyLevel: 'medium',
    rules: [
      {
        id: 'R1',
        name: 'Income Verification Variance',
        condition: 'Stated vs Verified > 15%',
        action: 'Flag for Manual Review',
        active: true
      },
      {
        id: 'R2',
        name: 'High Risk Geography',
        condition: 'Property ZIP in Blocklist',
        action: 'Require Supervisor Audit',
        active: true
      }
    ]
  };

  static async getGovernanceConfig(): Promise<GovernanceConfig> {
    return this.mockConfig;
  }

  static async saveGovernanceConfig(config: Partial<GovernanceConfig>): Promise<{ success: boolean; timestamp: string }> {
    this.mockConfig = { ...this.mockConfig, ...config };
    return {
      success: true,
      timestamp: new Date().toISOString()
    };
  }
}
