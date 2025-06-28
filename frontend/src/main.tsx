// src/main.tsx
import React from 'react'
import ReactDOM from 'react-dom/client'
import App from './App'
import './styles/globals.css'

import * as Sentry from '@sentry/react'

const FallbackComponent = () => (
  <div style={{ padding: '2rem', textAlign: 'center', color: '#fff' }}>
    <h1>Something went wrong.</h1>
    <p>We’re working on it!</p>
  </div>
)

ReactDOM.createRoot(document.getElementById('root')!).render(
  <React.StrictMode>
    <Sentry.ErrorBoundary fallback={FallbackComponent} showDialog>
      <App />
    </Sentry.ErrorBoundary>
  </React.StrictMode>
)
