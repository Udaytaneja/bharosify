import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import { authApi, userApi } from '@/api/auth'
import { useNavigate } from 'react-router-dom'

export const useAuth = () => {
  const user = localStorage.getItem('user')
  const token = localStorage.getItem('access_token')

  return {
    user: user ? JSON.parse(user) : null,
    token,
    isAuthenticated: !!token,
  }
}

export const useLogin = () => {
  const _navigate = useNavigate()

  return useMutation({
    mutationFn: (data: { email: string; password: string }) =>
      authApi.login(data.email, data.password),
    onSuccess: (data) => {
      localStorage.setItem('access_token', data.access_token)
      localStorage.setItem('refresh_token', data.refresh_token)
      localStorage.setItem('user', JSON.stringify(data.user))
      _navigate(`/${data.user.role}`)
    },
  })
}

export const useRegister = () => {
  const _navigate = useNavigate()

  return useMutation({
    mutationFn: (data: any) => authApi.register(data),
    onSuccess: () => {
      _navigate('/login')
    },
  })
}

export const useLogout = () => {
  const _unused = useNavigate()
  const queryClient = useQueryClient()

  return useMutation({
    mutationFn: () => authApi.logout(),
    onSuccess: () => {
      localStorage.removeItem('access_token')
      localStorage.removeItem('refresh_token')
      localStorage.removeItem('user')
      queryClient.clear()
      _unused('/')
    },
  })
}

export const useCurrentUser = () => {
  return useQuery({
    queryKey: ['auth', 'me'],
    queryFn: () => authApi.getCurrentUser(),
    retry: 1,
  })
}

export const useUserProfile = () => {
  return useQuery({
    queryKey: ['user', 'profile'],
    queryFn: () => userApi.getProfile(),
  })
}

export const useUpdateProfile = () => {
  const queryClient = useQueryClient()

  return useMutation({
    mutationFn: (data: any) => userApi.updateProfile(data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['user', 'profile'] })
    },
  })
}
