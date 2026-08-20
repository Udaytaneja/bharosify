import { useQuery } from '@tanstack/react-query'
import { applicationApi, loanApi, repaymentApi, underwritingApi } from '@/api/financial'

export const useApplications = (skip = 0, limit = 20) => {
  return useQuery({
    queryKey: ['applications', skip, limit],
    queryFn: () => applicationApi.getAll(skip, limit),
    staleTime: 2 * 60 * 1000,
  })
}

export const useApplicationDetail = (applicationId: string) => {
  return useQuery({
    queryKey: ['applications', applicationId],
    queryFn: () => applicationApi.getDetail(applicationId),
    enabled: !!applicationId,
  })
}

export const useLoans = (skip = 0, limit = 20) => {
  return useQuery({
    queryKey: ['loans', skip, limit],
    queryFn: () => loanApi.getAll(skip, limit),
    staleTime: 3 * 60 * 1000,
  })
}

export const useLoanDetail = (loanId: string) => {
  return useQuery({
    queryKey: ['loans', loanId],
    queryFn: () => loanApi.getDetail(loanId),
    enabled: !!loanId,
  })
}

export const useRepaymentSchedule = (skip = 0, limit = 20) => {
  return useQuery({
    queryKey: ['repayments', 'schedule', skip, limit],
    queryFn: () => repaymentApi.getSchedule(skip, limit),
    staleTime: 2 * 60 * 1000,
  })
}

export const useLoanRepaymentSchedule = (loanId: string, skip = 0, limit = 20) => {
  return useQuery({
    queryKey: ['repayments', 'loan', loanId, skip, limit],
    queryFn: () => repaymentApi.getLoanSchedule(loanId, skip, limit),
    enabled: !!loanId,
  })
}

export const useUnderwriting = (applicationId: string) => {
  return useQuery({
    queryKey: ['underwriting', applicationId],
    queryFn: () => underwritingApi.getAnalysis(applicationId),
    enabled: !!applicationId,
  })
}
