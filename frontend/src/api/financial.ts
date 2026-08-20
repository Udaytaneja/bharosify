import { apiClient } from './client'
import { 
  LoanApplication, 
  Loan, 
  Repayment,
  PaginatedResponse,
  Underwriting,
} from '@/types'

export const applicationApi = {
  create: async (data: any) => {
    const response = await apiClient.post<LoanApplication>('/applications', data)
    return response.data
  },

  getAll: async (skip = 0, limit = 20) => {
    const response = await apiClient.get<PaginatedResponse<LoanApplication>>(
      '/applications',
      { params: { skip, limit } }
    )
    return response.data
  },

  getDetail: async (applicationId: string) => {
    const response = await apiClient.get<LoanApplication>(
      `/applications/${applicationId}`
    )
    return response.data
  },

  update: async (applicationId: string, data: Partial<LoanApplication>) => {
    const response = await apiClient.put<LoanApplication>(
      `/applications/${applicationId}`,
      data
    )
    return response.data
  },
}

export const loanApi = {
  getAll: async (skip = 0, limit = 20) => {
    const response = await apiClient.get<PaginatedResponse<Loan>>(
      '/loans',
      { params: { skip, limit } }
    )
    return response.data
  },

  getDetail: async (loanId: string) => {
    const response = await apiClient.get<Loan>(`/loans/${loanId}`)
    return response.data
  },
}

export const repaymentApi = {
  getSchedule: async (skip = 0, limit = 20) => {
    const response = await apiClient.get<PaginatedResponse<Repayment>>(
      '/repayments',
      { params: { skip, limit } }
    )
    return response.data
  },

  getLoanSchedule: async (loanId: string, skip = 0, limit = 20) => {
    const response = await apiClient.get<PaginatedResponse<Repayment>>(
      `/repayments/${loanId}`,
      { params: { skip, limit } }
    )
    return response.data
  },
}

export const underwritingApi = {
  getAnalysis: async (applicationId: string) => {
    const response = await apiClient.get<Underwriting>(
      `/underwriting/${applicationId}`
    )
    return response.data
  },
}

export const aiApi = {
  chat: async (message: string, language = 'en') => {
    const response = await apiClient.post('/ai/chat', {
      message,
      language,
    })
    return response.data
  },

  scenario: async (data: any) => {
    const response = await apiClient.post('/ai/scenario', data)
    return response.data
  },

  riskAnalysis: async (data: any) => {
    const response = await apiClient.post('/ai/risk-analysis', data)
    return response.data
  },

  underwriting: async (data: any) => {
    const response = await apiClient.post('/ai/underwriting', data)
    return response.data
  },
}
