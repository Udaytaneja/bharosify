import React, { useState } from 'react'
import { useTranslation } from 'react-i18next'
import AppLayout from '@/layouts/AppLayout'
import { aiApi } from '@/api/financial'
import { PageHeader, Card, Input, Button } from '@/components'

interface Message {
  id: string
  role: 'user' | 'assistant'
  content: string
  timestamp: Date
}

const UserAI: React.FC = () => {
  const { t, i18n } = useTranslation()
  const [messages, setMessages] = useState<Message[]>([])
  const [input, setInput] = useState('')
  const [isLoading, setIsLoading] = useState(false)

  const navItems = [
    { label: t('nav.home'), href: '/user', icon: '🏠' },
    { label: t('nav.aiAssistant'), href: '/user/ai-assistant', icon: '🤖' },
  ]

  const handleSendMessage = async (e: React.FormEvent) => {
    e.preventDefault()
    if (!input.trim() || isLoading) return

    const userMessage: Message = {
      id: Date.now().toString(),
      role: 'user',
      content: input,
      timestamp: new Date(),
    }

    setMessages((prev) => [...prev, userMessage])
    setInput('')
    setIsLoading(true)

    try {
      const response = await aiApi.chat(input, i18n.language)
      const assistantMessage: Message = {
        id: (Date.now() + 1).toString(),
        role: 'assistant',
        content: response.message || response,
        timestamp: new Date(),
      }
      setMessages((prev) => [...prev, assistantMessage])
    } catch (error) {
      const errorMessage: Message = {
        id: (Date.now() + 2).toString(),
        role: 'assistant',
        content: 'Sorry, I encountered an error. Please try again.',
        timestamp: new Date(),
      }
      setMessages((prev) => [...prev, errorMessage])
    } finally {
      setIsLoading(false)
    }
  }

  return (
    <AppLayout navItems={navItems}>
      <PageHeader title={t('ai.assistant')} />

      <Card className="flex flex-col h-96">
        <div className="flex-1 overflow-y-auto p-4 space-y-4">
          {messages.length === 0 ? (
            <div className="flex items-center justify-center h-full text-text-muted">
              {t('ai.noConversation')}
            </div>
          ) : (
            messages.map((msg) => (
              <div
                key={msg.id}
                className={`flex ${msg.role === 'user' ? 'justify-end' : 'justify-start'}`}
              >
                <div
                  className={`max-w-xs px-4 py-2 rounded-lg ${
                    msg.role === 'user'
                      ? 'bg-brand-700 text-white'
                      : 'bg-bg-page text-text-primary'
                  }`}
                >
                  {msg.content}
                </div>
              </div>
            ))
          )}
          {isLoading && (
            <div className="flex justify-start">
              <div className="bg-bg-page text-text-secondary px-4 py-2 rounded-lg">
                {t('ai.typing')}
              </div>
            </div>
          )}
        </div>

        <form onSubmit={handleSendMessage} className="border-t border-border p-4 flex gap-2">
          <Input
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder={t('ai.askQuestion')}
            disabled={isLoading}
          />
          <Button type="submit" variant="primary" isLoading={isLoading}>
            {t('ai.send')}
          </Button>
        </form>
      </Card>
    </AppLayout>
  )
}

export default UserAI
