import { Component, ErrorInfo, ReactNode } from 'react'

interface Props {
  children: ReactNode
}

interface State {
  hasError: boolean
  error: Error | null
}

class ErrorBoundary extends Component<Props, State> {
  public state: State = {
    hasError: false,
    error: null,
  }

  public static getDerivedStateFromError(error: Error): State {
    return { hasError: true, error }
  }

  public componentDidCatch(error: Error, errorInfo: ErrorInfo) {
    console.error('Uncaught error:', error, errorInfo)
  }

  private handleReset = () => {
    this.setState({ hasError: false, error: null })
    window.location.href = '/'
  }

  public render() {
    if (this.state.hasError) {
      return (
        <div className="min-h-screen bg-bg-page flex items-center justify-center p-6">
          <div className="bg-bg-surface border border-border rounded-xl p-8 max-w-md w-full text-center shadow-lg">
            <div className="text-4xl mb-4">⚠️</div>
            <h1 className="text-2xl font-bold text-text-primary mb-2">Something went wrong</h1>
            <p className="text-text-secondary text-sm mb-6">
              An unexpected error occurred. Don't worry, your financial data is safe.
            </p>
            <div className="flex gap-3 justify-center">
              <button
                onClick={() => this.setState({ hasError: false, error: null })}
                className="px-4 py-2 text-sm font-medium bg-brand-100 text-brand-700 rounded-lg hover:bg-brand-50 transition-colors"
              >
                Try Again
              </button>
              <button
                onClick={this.handleReset}
                className="px-4 py-2 text-sm font-medium bg-brand-700 text-white rounded-lg hover:bg-brand-800 transition-colors"
              >
                Go to Home
              </button>
            </div>
          </div>
        </div>
      )
    }

    return this.props.children
  }
}

export default ErrorBoundary
