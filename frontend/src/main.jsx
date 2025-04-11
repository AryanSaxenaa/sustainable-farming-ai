import React from 'react'
import ReactDOM from 'react-dom/client'
import App from './App'
import './index.css'

console.log('Starting React application...')

try {
  const root = ReactDOM.createRoot(document.getElementById('root'))
  console.log('Root element found:', document.getElementById('root'))
  
  root.render(
    <React.StrictMode>
      <App />
    </React.StrictMode>
  )
  console.log('React application rendered successfully')
} catch (error) {
  console.error('Error rendering React application:', error)
}
