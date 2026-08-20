import React, { useState } from 'react'
import { useSearchParams, Link } from 'react-router-dom'
import { useTranslation } from 'react-i18next'
import AuthLayout from '@/layouts/AuthLayout'
import Input from '@/components/Input'
import Button from '@/components/Button'
import Alert from '@/components/Alert'
import { useLogin } from '@/hooks'
import { validateEmail } from '@/utils'

const LoginPage: React.FC = () => {
  const { t } = useTranslation()
  const [searchParams] = useSearchParams()
  const role = searchParams.get('role') || 'user'
  const { mutate: login, isPending, error } = useLogin()
  const [formData, setFormData] = useState({ email: '', password: '' })
  const [errors, setErrors] = useState<Record<string, string>>({})

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault()
    const newErrors: Record<string, string> = {}

    if (!formData.email) {
      newErrors.email = t('auth.email') + ' is required'
    } else if (!validateEmail(formData.email)) {
      newErrors.email = t('auth.invalidEmail')
    }

    if (!formData.password) {
      newErrors.password = t('auth.passwordRequired')
    }

    if (Object.keys(newErrors).length > 0) {
      setErrors(newErrors)
      return
    }

    login(formData)
  }

  return (
    <AuthLayout title={t('auth.login')} subtitle={`${t('auth.selectRole')} - ${role.toUpperCase()}`}>
      {error && (
        <Alert
          type="danger"
          title={t('auth.loginFailed')}
          message={(error as any)?.response?.data?.error?.message || 'Login failed. Please try again.'}
        />
      )}

      <form onSubmit={handleSubmit} className="space-y-4">
        <Input
          label={t('auth.email')}
          type="email"
          value={formData.email}
          onChange={(e) => {
            setFormData({ ...formData, email: e.target.value })
            if (errors.email) setErrors({ ...errors, email: '' })
          }}
          error={errors.email}
          placeholder="you@example.com"
        />

        <Input
          label={t('auth.password')}
          type="password"
          value={formData.password}
          onChange={(e) => {
            setFormData({ ...formData, password: e.target.value })
            if (errors.password) setErrors({ ...errors, password: '' })
          }}
          error={errors.password}
          placeholder="••••••••"
        />

        <div className="flex justify-between items-center text-sm">
          <label className="flex items-center gap-2">
            <input type="checkbox" className="w-4 h-4 rounded border-border" />
            <span className="text-text-secondary">{t('common.loading')} me</span>
          </label>
          <a href="#" className="text-brand-700 hover:underline">
            {t('auth.forgotPassword')}
          </a>
        </div>

        <Button fullWidth type="submit" isLoading={isPending}>
          {t('auth.login')}
        </Button>
      </form>

      <div className="mt-6 text-center text-text-muted text-sm">
        {t('auth.noAccount')}{' '}
        <Link to={`/register?role=${role}`} className="text-brand-700 hover:underline font-medium">
          {t('auth.createAccount')}
        </Link>
      </div>
    </AuthLayout>
  )
}

export default LoginPage
