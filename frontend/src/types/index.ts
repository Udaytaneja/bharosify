// Shared types matching contracts/schemas.md

export interface User {
  id: string
  name: string
  email: string
  phone: string
  role: 'user' | 'banker'
  language: 'en' | 'hi'
  created_at: string
  updated_at: string
}

export interface AuthTokens {
  access_token: string
  refresh_token: string
  token_type: string
  user: User
}

export interface UserProfile {
  user_id: string
  name: string
  email: string
  phone: string
  language: 'en' | 'hi'
  profile_status: string
}

export interface FinancialProfile {
  user_id: string
  income: number
  expenses: number
  savings: number
  assets: number
  liabilities: number
  existing_loans: number
}

export interface FinancialHealth {
  user_id: string
  score: number
  income: number
  expenses: number
  savings: number
  debt: number
  repayment_burden: number
  status: string
  updated_at: string
}

export interface Transaction {
  id: string
  user_id: string
  amount: number
  type: 'income' | 'expense' | 'transfer'
  category: string
  merchant: string
  description: string
  date: string
  status: 'pending' | 'completed' | 'failed' | 'reversed'
}

export interface TrustProfile {
  user_id: string
  score: number
  level: 'critical' | 'needs_attention' | 'good' | 'trusted'
  change: number
  factors: TrustFactor[]
  updated_at: string
}

export interface TrustFactor {
  name: string
  impact: number
  value: string
  description: string
}

export interface LoanApplication {
  id: string
  customer_id: string
  amount: number
  purpose: string
  status: 'draft' | 'submitted' | 'under_review' | 'documents_required' | 'underwriting' | 'approved' | 'rejected' | 'withdrawn' | 'completed'
  documents: string[]
  created_at: string
  updated_at: string
}

export interface Loan {
  id: string
  application_id: string
  customer_id: string
  principal: number
  interest_rate: number
  duration: number
  outstanding_amount: number
  status: 'pending' | 'active' | 'completed' | 'defaulted' | 'cancelled'
  start_date: string
  maturity_date: string
}

export interface Repayment {
  id: string
  loan_id: string
  amount: number
  due_date: string
  paid_date: string | null
  status: 'upcoming' | 'pending' | 'paid' | 'partially_paid' | 'failed' | 'overdue'
  payment_reference: string
}

export interface Notification {
  id: string
  user_id: string
  type: 'info' | 'success' | 'warning' | 'action_required'
  title: string
  message: string
  status: 'unread' | 'read'
  created_at: string
}

export interface Customer {
  id: string
  name: string
  email: string
  phone: string
  trust_profile: TrustProfile
  financial_health: FinancialHealth
  account_status: 'active' | 'inactive' | 'suspended' | 'blocked'
}

export interface RiskAssessment {
  id: string
  customer_id: string
  score: number
  level: 'low' | 'medium' | 'high' | 'critical'
  factors: string[]
  evidence: string
  recommendation: string
  confidence: number
  created_at: string
}

export interface FraudSignal {
  id: string
  customer_id: string
  transaction_id: string
  type: string
  severity: 'low' | 'medium' | 'high' | 'critical'
  score: number
  evidence: string
  status: 'open' | 'under_review' | 'resolved' | 'false_positive'
  created_at: string
}

export interface Underwriting {
  application_id: string
  risk_score: number
  risk_level: 'low' | 'medium' | 'high' | 'critical'
  factors: string[]
  evidence: string
  recommendation: string
  confidence: number
  human_review_required: boolean
  decision: 'approve' | 'review' | 'reject' | 'escalate'
}

export interface PaymentCreate {
  amount: number
  payment_reference: string
  idempotency_key: string
  transaction_id?: number | null
  repayment_id?: number | null
}

export interface PaymentResponse {
  id: number
  user_id: number
  amount: number
  payment_reference: string
  idempotency_key: string
  status: string
  reconciled: boolean
  created_at: string
}

export interface AIRequest {
  request_id: string
  task: 'chat' | 'scenario' | 'risk_analysis' | 'underwriting'
  input: string
  language?: string
  context?: Record<string, any>
}

export interface AIResponse {
  request_id: string
  response: string
  confidence: number
  reasoning_summary: string
  evidence: any[]
  recommendation: string
  requires_human_review: boolean
}

export interface PaginatedResponse<T> {
  items: T[]
  total: number
  skip: number
  limit: number
}

export interface ApiError {
  error: {
    code: string
    message: string
    details: any
  }
}

