import React, { useState, useEffect } from 'react'
import { useTranslation } from 'react-i18next'
import AppLayout from '@/layouts/AppLayout'
import { useUserProfile, useUpdateProfile } from '@/hooks'
import { PageHeader, Loading, Card, Input, Select, Button, Alert } from '@/components'

const UserSettings: React.FC = () => {
  const { t, i18n } = useTranslation()
  const { data: profile, isLoading } = useUserProfile()
  const { mutateAsync: updateProfile, isPending } = useUpdateProfile()
  const [formData, setFormData] = useState({
    name: '',
    phone: '',
    language: 'en',
  })
  const [feedback, setFeedback] = useState<{ type: 'success' | 'danger'; message: string } | null>(null)

  useEffect(() => {
    if (profile) {
      setFormData({
        name: profile.name || '',
        phone: profile.phone || '',
        language: profile.language || 'en',
      })
    }
  }, [profile])

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setFeedback(null)
    try {
      await updateProfile(formData)
      if (formData.language !== i18n.language) {
        i18n.changeLanguage(formData.language)
        localStorage.setItem('language', formData.language)
      }
      setFeedback({ type: 'success', message: 'Profile updated successfully!' })
    } catch (err: any) {
      setFeedback({ type: 'danger', message: err.message || 'Failed to update profile' })
    }
  }

  if (isLoading) {
    return (
      <AppLayout>
        <Loading />
      </AppLayout>
    )
  }

  return (
    <AppLayout>
      <PageHeader title={t('nav.settings')} subtitle="Manage your account details and preferences" />

      <Card className="max-w-2xl">
        <h2 className="text-lg font-semibold text-text-primary mb-6">{t('common.profile')}</h2>

        {feedback && (
          <div className="mb-4">
            <Alert type={feedback.type} message={feedback.message} />
          </div>
        )}

        <form onSubmit={handleSubmit} className="space-y-4">
          <Input
            label={t('auth.name')}
            value={formData.name}
            onChange={(e) => setFormData({ ...formData, name: e.target.value })}
            disabled={isPending}
          />

          <Input
            label={t('auth.phone')}
            value={formData.phone}
            onChange={(e) => setFormData({ ...formData, phone: e.target.value })}
            disabled={isPending}
          />

          <div>
            <label className="block text-sm font-medium text-text-primary mb-1">
              Language Preference
            </label>
            <Select
              value={formData.language}
              onChange={(e) => setFormData({ ...formData, language: e.target.value })}
              options={[
                { value: 'en', label: 'English' },
                { value: 'hi', label: 'हिन्दी (Hindi)' },
              ]}
              disabled={isPending}
            />
          </div>

          <div className="pt-4 border-t border-border flex justify-end">
            <Button type="submit" variant="primary" isLoading={isPending}>
              {t('common.save')}
            </Button>
          </div>
        </form>
      </Card>
    </AppLayout>
  )
}

export default UserSettings
