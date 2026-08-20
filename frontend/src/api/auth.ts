import { apiClient } from './client'
import { AuthTokens, User, UserProfile } from '@/types'

export const authApi = {
  register: async (data: {
    email: string
    password: string
    name: string
    phone: string
    language: 'en' | 'hi'
  }) => {
    const response = await apiClient.post<User>('/auth/register', data)
    return response.data
  },

  login: async (email: string, password: string) => {
    const response = await apiClient.post<AuthTokens>('/auth/login', {
      email,
      password,
    })
    return response.data
  },

  refresh: async (refreshToken: string) => {
    const response = await apiClient.post<AuthTokens>('/auth/refresh', {
      refresh_token: refreshToken,
    })
    return response.data
  },

  logout: async () => {
    await apiClient.post('/auth/logout')
  },

  getCurrentUser: async () => {
    const response = await apiClient.get<User>('/auth/me')
    return response.data
  },
}

export const userApi = {
  getProfile: async () => {
    const response = await apiClient.get<UserProfile>('/users/me')
    return response.data
  },

  updateProfile: async (data: Partial<UserProfile>) => {
    const response = await apiClient.put<UserProfile>('/users/me', data)
    return response.data
  },
}
