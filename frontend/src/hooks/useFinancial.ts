import { useQuery } from '@tanstack/react-query'
import { financialApi, trustApi, notificationApi, auditApi } from '@/api'

export const useFinancialHealth = () => {
  return useQuery({
    queryKey: ['financial', 'health'],
    queryFn: () => financialApi.getHealth(),
    staleTime: 5 * 60 * 1000,
  })
}

export const useFinancialProfile = () => {
  return useQuery({
    queryKey: ['financial', 'profile'],
    queryFn: () => financialApi.getProfile(),
    staleTime: 5 * 60 * 1000,
  })
}

export const useTransactions = (skip = 0, limit = 20) => {
  return useQuery({
    queryKey: ['transactions', skip, limit],
    queryFn: () => financialApi.getTransactions(skip, limit),
    staleTime: 2 * 60 * 1000,
  })
}

export const useTrustProfile = () => {
  return useQuery({
    queryKey: ['trust', 'profile'],
    queryFn: () => trustApi.getProfile(),
    staleTime: 5 * 60 * 1000,
  })
}

export const useTrustFactors = () => {
  return useQuery({
    queryKey: ['trust', 'factors'],
    queryFn: () => trustApi.getFactors(),
    staleTime: 5 * 60 * 1000,
  })
}

export const useNotifications = (skip = 0, limit = 20) => {
  return useQuery({
    queryKey: ['notifications', skip, limit],
    queryFn: () => notificationApi.getNotifications(skip, limit),
    staleTime: 1 * 60 * 1000,
    refetchInterval: 2 * 60 * 1000,
  })
}

export const useAuditActivity = (skip = 0, limit = 50) => {
  return useQuery({
    queryKey: ['audit', 'activity', skip, limit],
    queryFn: () => auditApi.getActivity(skip, limit),
    staleTime: 5 * 60 * 1000,
  })
}
