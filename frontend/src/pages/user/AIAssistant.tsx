import React, { useState, useRef, useEffect } from 'react'
import { useTranslation } from 'react-i18next'
import AppLayout from '@/layouts/AppLayout'
import { aiApi } from '@/api/financial'
import { PageHeader, Card, Input, Button, Badge } from '@/components'
import { AIResponse } from '@/types'

interface Message {
  id: string
  role: 'user' | 'assistant'
  content: string
  confidence?: number
  reasoningSummary?: string
  evidence?: any[]
  requiresHumanReview?: boolean
  timestamp: Date
}

const UserAI: React.FC = () => {
  const { t, i18n } = useTranslation()
  const [messages, setMessages] = useState<Message[]>([])
  const [input, setInput] = useState('')
  const [isLoading, setIsLoading] = useState(false)
  const chatContainerRef = useRef<HTMLDivElement>(null)

  const suggestions = i18n.language === 'hi'
    ? [
        'मेरी वित्तीय स्थिति का विश्लेषण करें',
        'क्या मैं ₹50,000 के ऋण के लिए योग्य हूँ?',
        'मेरा पुनर्भुगतान बोझ कैसे कम करें?',
      ]
    : [
        'Analyze my current financial stability',
        'Am I eligible for a ₹50,000 personal loan?',
        'How can I improve my trust score?',
      ]

  useEffect(() => {
    if (chatContainerRef.current) {
      chatContainerRef.current.scrollTop = chatContainerRef.current.scrollHeight
    }
  }, [messages, isLoading])

  const sendQuery = async (queryText: string) => {
    if (!queryText.trim() || isLoading) return

    const userMessage: Message = {
      id: `user_${Date.now()}`,
      role: 'user',
      content: queryText,
      timestamp: new Date(),
    }

    setMessages((prev) => [...prev, userMessage])
    setInput('')
    setIsLoading(true)

    try {
      const response: AIResponse = await aiApi.chat(queryText, i18n.language)
      
      const assistantMessage: Message = {
        id: `ai_${Date.now()}`,
        role: 'assistant',
        content: response.response || 'I have analyzed your request based on your financial records.',
        confidence: response.confidence,
        reasoningSummary: response.reasoning_summary,
        evidence: response.evidence,
        requiresHumanReview: response.requires_human_review,
        timestamp: new Date(),
      }
      setMessages((prev) => [...prev, assistantMessage])
    } catch (error: any) {
      const errorMessage: Message = {
        id: `err_${Date.now()}`,
        role: 'assistant',
        content: error.response?.data?.detail || 'Sorry, I encountered an error accessing the AI service. Please try again.',
        timestamp: new Date(),
      }
      setMessages((prev) => [...prev, errorMessage])
    } finally {
      setIsLoading(false)
    }
  }

  const handleSendMessage = (e: React.FormEvent) => {
    e.preventDefault()
    sendQuery(input)
  }

  return (
    <AppLayout>
      <PageHeader
        title={t('ai.assistant')}
        subtitle="AI-powered financial advisor & decision analysis"
      />

      <Card className="flex flex-col h-[520px] max-w-4xl mx-auto overflow-hidden">
        {/* Chat Messages */}
        <div ref={chatContainerRef} className="flex-1 overflow-y-auto p-4 space-y-4">
          {messages.length === 0 ? (
            <div className="flex flex-col items-center justify-center h-full text-center p-6">
              <div className="w-12 h-12 rounded-full bg-brand-100 text-brand-700 flex items-center justify-center text-2xl mb-3">
                🤖
              </div>
              <h3 className="font-semibold text-text-primary mb-1">AgentTrust AI Assistant</h3>
              <p className="text-text-muted text-sm max-w-md mb-6">
                Ask about your financial health, loan eligibility, trust score analysis, or budget guidance.
              </p>

              <div className="w-full max-w-md">
                <p className="text-xs font-semibold text-text-muted uppercase tracking-wider mb-2 text-left">
                  {t('ai.suggestions')}
                </p>
                <div className="space-y-2">
                  {suggestions.map((suggestion, idx) => (
                    <button
                      key={idx}
                      onClick={() => sendQuery(suggestion)}
                      className="w-full text-left p-2.5 text-xs font-medium bg-bg-page hover:bg-brand-50 hover:text-brand-700 border border-border rounded-lg transition-colors"
                    >
                      💡 {suggestion}
                    </button>
                  ))}
                </div>
              </div>
            </div>
          ) : (
            messages.map((msg) => (
              <div
                key={msg.id}
                className={`flex ${msg.role === 'user' ? 'justify-end' : 'justify-start'}`}
              >
                <div
                  className={`max-w-lg rounded-xl p-4 text-sm ${
                    msg.role === 'user'
                      ? 'bg-brand-700 text-white shadow-xs'
                      : 'bg-bg-page border border-border text-text-primary shadow-xs'
                  }`}
                >
                  <div className="flex items-center justify-between gap-2 mb-1.5">
                    <span className="font-bold text-xs">
                      {msg.role === 'user' ? 'You' : 'AgentTrust AI'}
                    </span>
                    {msg.confidence !== undefined && (
                      <Badge variant="info">
                        Confidence: {(msg.confidence * 100).toFixed(0)}%
                      </Badge>
                    )}
                  </div>

                  <p className="whitespace-pre-wrap leading-relaxed">{msg.content}</p>

                  {msg.reasoningSummary && (
                    <div className="mt-3 pt-2.5 border-t border-border/60 text-xs text-text-secondary">
                      <span className="font-semibold block mb-0.5">Summary:</span>
                      {msg.reasoningSummary}
                    </div>
                  )}

                  {msg.requiresHumanReview && (
                    <div className="mt-2 text-xs text-status-warning font-semibold flex items-center gap-1">
                      ⚠️ Requires Banker Review
                    </div>
                  )}
                </div>
              </div>
            ))
          )}

          {isLoading && (
            <div className="flex justify-start">
              <div className="bg-bg-page border border-border text-text-secondary px-4 py-3 rounded-xl text-sm flex items-center gap-2">
                <span className="animate-spin text-brand-700">⏳</span>
                <span>{t('ai.typing')}</span>
              </div>
            </div>
          )}
        </div>

        {/* Input Bar */}
        <form onSubmit={handleSendMessage} className="border-t border-border p-3 flex gap-2 bg-bg-surface">
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
