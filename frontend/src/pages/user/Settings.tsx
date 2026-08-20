import React from 'react'
import { useTranslation } from 'react-i18next'
import AppLayout from '@/layouts/AppLayout'
import { useUserProfile, useUpdateProfile } from '@/hooks'
import { PageHeader, Loading, Card, Input, Button } from '@/components'

const UserSettings: React.FC = () => {
  const { t } = useTranslation()
  const { data: profile, isLoading } = useUserProfile()
  const { mutate: updateProfile, isPending } = useUpdateProfile()
  const [formData, setFormData] = React.useState({
    name: '',
    phone: '',
    language: 'en',
  })

  React.useEffect(() => {
    if (profile) {
      setFormData({
        name: profile.name || '',
        phone: profile.phone || '',
        language: profile.language || 'en',
      })
    }
  }, [profile])

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault()
    updateProfile(formData)
  }

  const navItems = [
    { label: t('nav.home'), href: '/user', icon: '🏠' },
    { label: t('nav.settings'), href: '/user/settings', icon: '⚙️' },
  ]

  if (isLoading) return <AppLayout navItems={navItems}><Loading /></AppLayout>

  return (
    <AppLayout navItems={navItems}>
      <PageHeader title={t('nav.settings')} />

      <Card>
        <h2 className="text-lg font-semibold text-text-primary mb-6">{t('common.profile')}</h2>

        <form onSubmit={handleSubmit} className="space-y-4">
          <Input
            label={t('auth.name')}
            value={formData.name}
            onChange={(e) => setFormData({ ...formData, name: e.target.value })}
          />

          <Input
            label={t('auth.phone')}
            value={formData.phone}
            onChange={(e) => setFormData({ ...formData, phone: e.target.value })}
          />

          <div>
            <label className="block text-sm font-medium text-text-primary mb-2">
              {t('common.language')}
            </label>
            <select
              value={formData.language}
              onChange={(e) => setFormData({ ...formData, language: e.target.value })}
              className="w-full px-4 py-2 border border-border rounded-lg"
            >
              <option value="en">English</option>
              <option value="hi">हिन्दी</option>
            </select>
          </div>

          <Button type="submit" isLoading={isPending}>
            {t('common.save')}
          </Button>
        </form>
      </Card>
    </AppLayout>
  )
}

export default UserSettings
