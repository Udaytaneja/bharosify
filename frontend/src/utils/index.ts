export const formatCurrency = (amount: number, currency = 'INR'): string => {
  return new Intl.NumberFormat('en-IN', {
    style: 'currency',
    currency,
    minimumFractionDigits: 2,
  }).format(amount)
}

export const formatDate = (date: string | Date): string => {
  return new Intl.DateTimeFormat('en-IN', {
    year: 'numeric',
    month: 'long',
    day: 'numeric',
  }).format(new Date(date))
}

export const formatDateShort = (date: string | Date): string => {
  return new Intl.DateTimeFormat('en-IN', {
    year: 'numeric',
    month: 'short',
    day: 'numeric',
  }).format(new Date(date))
}

export const formatDateTime = (date: string | Date): string => {
  return new Intl.DateTimeFormat('en-IN', {
    year: 'numeric',
    month: 'short',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit',
  }).format(new Date(date))
}

export const formatPhoneNumber = (phone: string): string => {
  const cleaned = phone.replace(/\D/g, '')
  if (cleaned.length === 10) {
    return `+91 ${cleaned.slice(0, 5)} ${cleaned.slice(5)}`
  }
  return phone
}

export const validateEmail = (email: string): boolean => {
  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/
  return emailRegex.test(email)
}

export const validatePhoneNumber = (phone: string): boolean => {
  const phoneRegex = /^[0-9]{10}$/
  const cleaned = phone.replace(/\D/g, '')
  return phoneRegex.test(cleaned)
}

export const getTrustLevelColor = (level: string): string => {
  switch (level) {
    case 'trusted':
      return 'text-status-success'
    case 'good':
      return 'text-brand-500'
    case 'needs_attention':
      return 'text-status-warning'
    case 'critical':
      return 'text-status-danger'
    default:
      return 'text-text-secondary'
  }
}

export const getRiskLevelColor = (level: string): string => {
  switch (level) {
    case 'low':
      return 'text-status-success'
    case 'medium':
      return 'text-status-warning'
    case 'high':
      return 'text-status-danger'
    case 'critical':
      return 'text-status-danger'
    default:
      return 'text-text-secondary'
  }
}

export const getStatusColor = (status: string): string => {
  if (['approved', 'active', 'completed', 'paid'].includes(status)) {
    return 'bg-status-success bg-opacity-10 text-status-success'
  }
  if (['pending', 'upcoming', 'submitted', 'under_review'].includes(status)) {
    return 'bg-status-info bg-opacity-10 text-status-info'
  }
  if (['rejected', 'failed', 'defaulted', 'overdue'].includes(status)) {
    return 'bg-status-danger bg-opacity-10 text-status-danger'
  }
  return 'bg-text-muted bg-opacity-10 text-text-muted'
}

export const debounce = <T extends (...args: any[]) => any>(
  func: T,
  delay: number
): ((...args: Parameters<T>) => void) => {
  let timeoutId: NodeJS.Timeout
  return (...args: Parameters<T>) => {
    clearTimeout(timeoutId)
    timeoutId = setTimeout(() => func(...args), delay)
  }
}

export const getInitials = (name: string): string => {
  return name
    .split(' ')
    .map((part) => part[0])
    .join('')
    .toUpperCase()
    .slice(0, 2)
}
