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
} from '@/types'

export const financialApi = {
  getProfile: async () => {
    const response = await apiClient.get<FinancialProfile>('/financial/profile')
    return response.data
  },

  getHealth: async () => {
    const response = await apiClient.get<FinancialHealth>('/financial/health')
    return response.data
  },

  getTransactions: async (skip = 0, limit = 20) => {
    const response = await apiClient.get<PaginatedResponse<Transaction>>(
      '/transactions',
      { params: { skip, limit } }
    )
    return response.data
  },

  searchTransactions: async (query: string, skip = 0, limit = 20) => {
    const response = await apiClient.get<PaginatedResponse<Transaction>>(
      '/transactions',
      { params: { q: query, skip, limit } }
    )
    return response.data
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
  getNotifications: async (skip = 0, limit = 20) => {
    const response = await apiClient.get<PaginatedResponse<Notification>>(
      '/notifications',
      { params: { skip, limit } }
    )
    return response.data
  },

  markAsRead: async (notificationId: string) => {
    await apiClient.put(`/notifications/${notificationId}/read`)
  },
}

export const auditApi = {
  getActivity: async (skip = 0, limit = 50) => {
    const response = await apiClient.get('/audit/me', {
      params: { skip, limit }
    })
    return response.data
  },
}

export const bankerApi = {
  getCustomers: async (skip = 0, limit = 20) => {
    const response = await apiClient.get('/bankers/customers', {
      params: { skip, limit }
    })
    return response.data
  },

  getCustomerDetail: async (customerId: string) => {
    const response = await apiClient.get(`/bankers/customers/${customerId}`)
    return response.data
  },

  getApplications: async (skip = 0, limit = 20) => {
    const response = await apiClient.get('/bankers/applications', {
      params: { skip, limit }
    })
    return response.data
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
