import React from 'react'
import { Providers } from './providers'
import { router } from './router'

const App: React.FC = () => {
  return (
    <Providers>
      {router}
    </Providers>
  )
}

export default App
