import React from 'react'
import { Providers } from './providers'
import { router } from './router'
import { ErrorBoundary } from '@/components'

const App: React.FC = () => {
  return (
    <ErrorBoundary>
      <Providers>
        {router}
      </Providers>
    </ErrorBoundary>
  )
}

export default App

