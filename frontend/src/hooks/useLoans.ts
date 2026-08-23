import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import { applicationApi, loanApi, repaymentApi, paymentApi, underwritingApi } from '@/api/financial'
import { PaymentCreate } from '@/types'

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

export const useCreateApplication = () => {
  const queryClient = useQueryClient()
  return useMutation({
    mutationFn: (data: { amount: number; purpose: string; documents?: string[] }) =>
      applicationApi.create(data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['applications'] })
    },
  })
}

export const useUpdateApplication = () => {
  const queryClient = useQueryClient()
  return useMutation({
    mutationFn: ({ id, data }: { id: string; data: any }) =>
      applicationApi.update(id, data),
    onSuccess: (_, variables) => {
      queryClient.invalidateQueries({ queryKey: ['applications'] })
      queryClient.invalidateQueries({ queryKey: ['applications', variables.id] })
    },
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

export const useCreatePayment = () => {
  const queryClient = useQueryClient()
  return useMutation({
    mutationFn: (data: PaymentCreate) => paymentApi.create(data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['repayments'] })
      queryClient.invalidateQueries({ queryKey: ['loans'] })
    },
  })
}

export const useConfirmPayment = () => {
  const queryClient = useQueryClient()
  return useMutation({
    mutationFn: (paymentId: number) => paymentApi.confirm(paymentId),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['repayments'] })
      queryClient.invalidateQueries({ queryKey: ['loans'] })
      queryClient.invalidateQueries({ queryKey: ['financial', 'health'] })
    },
  })
}

export const useUnderwriting = (applicationId: string) => {
  return useQuery({
    queryKey: ['underwriting', applicationId],
    queryFn: () => underwritingApi.getAnalysis(applicationId),
    enabled: !!applicationId,
  })
}
