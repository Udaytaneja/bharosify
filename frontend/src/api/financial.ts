import { apiClient } from './client'
import { 
  LoanApplication, 
  Loan, 
  Repayment,
  PaginatedResponse,
  Underwriting,
  PaymentCreate,
  PaymentResponse,
  AIRequest,
  AIResponse,
} from '@/types'

function normalizeList<T>(data: any, skip = 0, limit = 20): PaginatedResponse<T> {
  if (Array.isArray(data)) {
    return {
      items: data,
      total: data.length,
      skip,
      limit,
    }
  }
  if (data && Array.isArray(data.items)) {
    return data
  }
  return {
    items: [],
    total: 0,
    skip,
    limit,
  }
}

export const applicationApi = {
  create: async (data: { amount: number; purpose: string; documents?: string[] }) => {
    const response = await apiClient.post<LoanApplication>('/applications', data)
    return response.data
  },

  getAll: async (skip = 0, limit = 20): Promise<PaginatedResponse<LoanApplication>> => {
    const response = await apiClient.get<any>('/applications', {
      params: { skip, limit },
    })
    return normalizeList<LoanApplication>(response.data, skip, limit)
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
  getAll: async (skip = 0, limit = 20): Promise<PaginatedResponse<Loan>> => {
    const response = await apiClient.get<any>('/loans', {
      params: { skip, limit },
    })
    return normalizeList<Loan>(response.data, skip, limit)
  },

  getDetail: async (loanId: string) => {
    const response = await apiClient.get<Loan>(`/loans/${loanId}`)
    return response.data
  },
}

export const repaymentApi = {
  getSchedule: async (skip = 0, limit = 20): Promise<PaginatedResponse<Repayment>> => {
    const response = await apiClient.get<any>('/repayments', {
      params: { skip, limit },
    })
    return normalizeList<Repayment>(response.data, skip, limit)
  },

  getLoanSchedule: async (loanId: string, skip = 0, limit = 20): Promise<PaginatedResponse<Repayment>> => {
    const response = await apiClient.get<any>(`/repayments/${loanId}`, {
      params: { skip, limit },
    })
    return normalizeList<Repayment>(response.data, skip, limit)
  },
}

export const paymentApi = {
  create: async (data: PaymentCreate): Promise<PaymentResponse> => {
    const response = await apiClient.post<PaymentResponse>('/payments', data)
    return response.data
  },

  confirm: async (paymentId: number): Promise<PaymentResponse> => {
    const response = await apiClient.post<PaymentResponse>(`/payments/${paymentId}/confirm`)
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
  chat: async (input: string, language = 'en', context: Record<string, any> = {}): Promise<AIResponse> => {
    const payload: AIRequest = {
      request_id: `req_${Date.now()}_${Math.random().toString(36).substring(2, 7)}`,
      task: 'chat',
      input,
      language,
      context,
    }
    const response = await apiClient.post<AIResponse>('/ai/chat', payload)
    return response.data
  },

  scenario: async (input: string, language = 'en', context: Record<string, any> = {}): Promise<AIResponse> => {
    const payload: AIRequest = {
      request_id: `req_${Date.now()}_${Math.random().toString(36).substring(2, 7)}`,
      task: 'scenario',
      input,
      language,
      context,
    }
    const response = await apiClient.post<AIResponse>('/ai/scenario', payload)
    return response.data
  },

  riskAnalysis: async (input: string, language = 'en', context: Record<string, any> = {}): Promise<AIResponse> => {
    const payload: AIRequest = {
      request_id: `req_${Date.now()}_${Math.random().toString(36).substring(2, 7)}`,
      task: 'risk_analysis',
      input,
      language,
      context,
    }
    const response = await apiClient.post<AIResponse>('/ai/risk-analysis', payload)
    return response.data
  },

  underwriting: async (input: string, language = 'en', context: Record<string, any> = {}): Promise<AIResponse> => {
    const payload: AIRequest = {
      request_id: `req_${Date.now()}_${Math.random().toString(36).substring(2, 7)}`,
      task: 'underwriting',
      input,
      language,
      context,
    }
    const response = await apiClient.post<AIResponse>('/ai/underwriting', payload)
    return response.data
  },
}
