// Domain Types & API Contracts for AgentTrust OS

export type UserRole = 'banker' | 'applicant' | null;

export interface UserProfile {
  id: string;
  name: string;
  role: UserRole;
  title: string;
  email: string;
  authLevel?: string;
  accountStatus?: 'VERIFIED' | 'PENDING' | 'SUSPENDED';
}

export type ApplicationStage =
  | 'Pre-Qualification'
  | 'Document OCR'
  | 'Underwriter Review'
  | 'Credit Committee'
  | 'Final Closing'
  | 'Disbursed';

export type ApplicationStatus =
  | 'UNDER_REVIEW'
  | 'APPROVED_ACTIVE'
  | 'COMPLETED'
  | 'REJECTED';

export interface LoanApplication {
  id: string;
  applicantName: string;
  type: string;
  category: 'Retail / Mortgage' | 'SME / Term Loan' | 'Retail / Auto' | 'Commercial Credit' | 'Project Finance';
  amount: string;
  amountNumeric: number;
  dateSubmitted: string;
  lastUpdated: string;
  stage: ApplicationStage;
  status: ApplicationStatus;
  riskRating: 'Low' | 'Elevated' | 'High';
  trustScore: number;
  assistedFlags: string[];
}

export interface PaymentScheduleItem {
  num: string;
  dueDate: string;
  principal: string;
  interest: string;
  total: string;
  status: 'PAID' | 'DUE SOON' | 'SCHEDULED';
}

export interface ActiveLoanFacility {
  facilityId: string;
  facilityName: string;
  category: string;
  principalOutstanding: number;
  originalAmount: number;
  percentPaid: number;
  interestRate: string;
  interestPaidYtd: number;
  maturityDate: string;
  nextPaymentDueDate: string;
  nextPaymentAmount: number;
  schedule: PaymentScheduleItem[];
}

export interface FinancialHealthProfile {
  trustIndexScore: number;
  borrowerTier: string;
  evaluationSummary: string;
  repaymentOnTimeRate: number;
  revenueTrendYoy: string;
  dtiRatioCurrent: number;
  dtiBenchmarkFloor: number;
  liquidityRatio: number;
  badges: string[];
}

export interface DocumentItem {
  id: string;
  name: string;
  type: string;
  requirement: 'REQUIRED' | 'RECOMMENDED' | 'OPTIONAL';
  dateUploaded: string;
  status: 'VERIFIED' | 'PROCESSING_OCR' | 'NOT UPLOADED';
  ocrScore?: number;
  tamperRisk?: 'NONE' | 'LOW_FLAG' | 'HIGH_FLAG';
}

export interface ExtractedField {
  fieldKey: string;
  label: string;
  extractedValue: string;
  confidenceScore: number;
  hasWarning?: boolean;
}

export interface UnderwritingCase {
  caseId: string;
  applicantName: string;
  ssnMasked: string;
  ficoScore: number;
  annualRevenue: number;
  requestedAmount: number;
  purpose: string;
  termMonths: number;
  ltvRatio: number;
  dscrRatio: number;
  activeDocument: string;
  aiRecommendation: string;
  aiConfidence: number;
  policyChecks: {
    ruleName: string;
    condition: string;
    passed: boolean;
    valString: string;
  }[];
  auditTrailId: string;
}

export interface AuditLogEntry {
  id: string;
  timestamp: string;
  actorType: 'SYS' | 'USR' | 'MGR';
  actor: string;
  action: string;
  resource: string;
  status: 'SUCCESS' | 'BLOCKED';
  evidence: string;
  hash: string;
}

export interface GovernanceConfig {
  dtiRatioMax: number;
  trustIndexCutoffMin: number;
  aiAutonomyLevel: 'low' | 'medium' | 'high';
  rules: {
    id: string;
    name: string;
    condition: string;
    action: string;
    active: boolean;
  }[];
}

// Extended Application Submission Domain Models
export interface PersonalDetails {
  fullName: string;
  fatherName: string;
  maritalStatus: 'Married' | 'Unmarried';
  spouseName?: string;
  dob: string;
}

export interface LegalHeir {
  id: string;
  name: string;
  relation: string;
  address: string;
  age: number | string;
}

export interface PersonalFinancialReport {
  assetsDescription: string;
  totalAssetsValue: number | string;
  liabilitiesDescription: string;
  totalLiabilitiesValue: number | string;
  otherNotes?: string;
}

export interface PreviousLoan {
  id: string;
  lenderName: string;
  originalAmount: number | string;
  outstandingAmount: number | string;
  status: 'Active' | 'Closed' | 'Default';
  notes?: string;
}

export interface GuarantorDetails {
  guarantorName: string;
  relation: string;
  netWorth: number | string;
  guaranteeAmount: number | string;
  liabilityDetails: string;
}

export interface QualificationDetails {
  highestEducation: 'Undergraduate' | 'Postgraduate' | 'Professional' | 'Doctorate' | 'Other';
  institutionName: string;
  graduationYear: string;
}

export interface IdentityDocuments {
  panDocument?: DocumentItem;
  aadhaarDocument?: DocumentItem;
}

export interface LoanRequestDetails {
  loanAmount: number | string;
  purpose: 'Social' | 'Medical' | 'Commercial Real Estate' | 'Working Capital' | 'Equipment Financing' | 'Refinance' | 'Other';
  scheme: string;
}

export interface FullApplicationSubmission {
  personalDetails: PersonalDetails;
  legalHeirs: LegalHeir[];
  financialReport: PersonalFinancialReport;
  previousLoans: PreviousLoan[];
  guaranteeDetails: GuarantorDetails;
  qualification: QualificationDetails;
  identityDocs: IdentityDocuments;
  loanRequest: LoanRequestDetails;
  otherInfoToBank?: string;
}
