import { apiClient } from './client'
import { 
  FinancialProfile, 
  FinancialHealth, 
  Transaction, 
  TrustProfile,
  PaginatedResponse,
  Notification,
  RiskAssessment,
  FraudSignal,
  Customer,
  LoanApplication,
} from '@/types'

export * from './auth'
export * from './financial'

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

export const financialApi = {
  getProfile: async () => {
    const response = await apiClient.get<FinancialProfile>('/financial/profile')
    return response.data
  },

  getHealth: async () => {
    const response = await apiClient.get<FinancialHealth>('/financial/health')
    return response.data
  },

  getTransactions: async (skip = 0, limit = 20): Promise<PaginatedResponse<Transaction>> => {
    const response = await apiClient.get<any>('/transactions', {
      params: { offset: skip, limit },
    })
    return normalizeList<Transaction>(response.data, skip, limit)
  },

  searchTransactions: async (query: string, skip = 0, limit = 20): Promise<PaginatedResponse<Transaction>> => {
    const response = await apiClient.get<any>('/transactions', {
      params: { q: query, offset: skip, limit },
    })
    return normalizeList<Transaction>(response.data, skip, limit)
  },
}

export const trustApi = {
  getProfile: async () => {
    const response = await apiClient.get<TrustProfile>('/trust/me')
    return response.data
  },

  getFactors: async () => {
    const response = await apiClient.get('/trust/me/factors')
    return response.data
  },
}

export const notificationApi = {
  getNotifications: async (skip = 0, limit = 20): Promise<PaginatedResponse<Notification>> => {
    const response = await apiClient.get<any>('/notifications', {
      params: { skip, limit },
    })
    return normalizeList<Notification>(response.data, skip, limit)
  },

  markAsRead: async (notificationId: string) => {
    await apiClient.put(`/notifications/${notificationId}/read`)
  },
}

export const auditApi = {
  getActivity: async (skip = 0, limit = 50): Promise<PaginatedResponse<any>> => {
    const response = await apiClient.get<any>('/audit/me', {
      params: { skip, limit }
    })
    return normalizeList<any>(response.data, skip, limit)
  },
}

export const bankerApi = {
  getCustomers: async (skip = 0, limit = 20): Promise<PaginatedResponse<Customer>> => {
    const response = await apiClient.get<any>('/bankers/customers', {
      params: { skip, limit }
    })
    return normalizeList<Customer>(response.data, skip, limit)
  },

  getCustomerDetail: async (customerId: string): Promise<Customer> => {
    const response = await apiClient.get<Customer>(`/bankers/customers/${customerId}`)
    return response.data
  },

  getApplications: async (skip = 0, limit = 20): Promise<PaginatedResponse<LoanApplication>> => {
    const response = await apiClient.get<any>('/bankers/applications', {
      params: { skip, limit }
    })
    return normalizeList<LoanApplication>(response.data, skip, limit)
  },
}

export const riskApi = {
  getRiskAssessment: async (customerId: string) => {
    const response = await apiClient.get<RiskAssessment>(
      `/risk/${customerId}`
    )
    return response.data
  },

  getFraudSignals: async (customerId: string) => {
    const response = await apiClient.get<FraudSignal[]>(
      `/fraud/${customerId}`
    )
    return response.data
  },
}
