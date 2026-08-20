import React, { useState } from 'react'
import { useSearchParams, Link } from 'react-router-dom'
import { useTranslation } from 'react-i18next'
import AuthLayout from '@/layouts/AuthLayout'
import Input from '@/components/Input'
import Button from '@/components/Button'
import Alert from '@/components/Alert'
import { useRegister } from '@/hooks'
import { validateEmail, validatePhoneNumber } from '@/utils'

const RegisterPage: React.FC = () => {
  const { t } = useTranslation()
  const [searchParams] = useSearchParams()
  const role = searchParams.get('role') || 'user'
  const { mutate: register, isPending, error } = useRegister()
  const [formData, setFormData] = useState({
    name: '',
    email: '',
    phone: '',
    password: '',
    language: t('common.language') === 'English' ? 'en' : 'hi',
  })
  const [errors, setErrors] = useState<Record<string, string>>({})

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault()
    const newErrors: Record<string, string> = {}

    if (!formData.name) {
      newErrors.name = t('auth.name') + ' is required'
    }

    if (!formData.email) {
      newErrors.email = t('auth.email') + ' is required'
    } else if (!validateEmail(formData.email)) {
      newErrors.email = t('auth.invalidEmail')
    }

    if (!formData.phone) {
      newErrors.phone = t('auth.phone') + ' is required'
    } else if (!validatePhoneNumber(formData.phone)) {
      newErrors.phone = 'Phone number must be 10 digits'
    }

    if (!formData.password || formData.password.length < 6) {
      newErrors.password = 'Password must be at least 6 characters'
    }

    if (Object.keys(newErrors).length > 0) {
      setErrors(newErrors)
      return
    }

    register({ ...formData, role })
  }

  return (
    <AuthLayout title={t('auth.register')} subtitle={`${t('auth.selectRole')} - ${role.toUpperCase()}`}>
      {error && (
        <Alert
          type="danger"
          title={t('auth.registerFailed')}
          message={(error as any)?.response?.data?.error?.message || 'Registration failed. Please try again.'}
        />
      )}

      <form onSubmit={handleSubmit} className="space-y-4">
        <Input
          label={t('auth.name')}
          value={formData.name}
          onChange={(e) => {
            setFormData({ ...formData, name: e.target.value })
            if (errors.name) setErrors({ ...errors, name: '' })
          }}
          error={errors.name}
          placeholder="John Doe"
        />

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
          label={t('auth.phone')}
          value={formData.phone}
          onChange={(e) => {
            setFormData({ ...formData, phone: e.target.value })
            if (errors.phone) setErrors({ ...errors, phone: '' })
          }}
          error={errors.phone}
          placeholder="9876543210"
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

        <Button fullWidth type="submit" isLoading={isPending}>
          {t('auth.createAccount')}
        </Button>
      </form>

      <div className="mt-6 text-center text-text-muted text-sm">
        {t('auth.haveAccount')}{' '}
        <Link to={`/login?role=${role}`} className="text-brand-700 hover:underline font-medium">
          {t('auth.login')}
        </Link>
      </div>
    </AuthLayout>
  )
}

export default RegisterPage
