import React from 'react'
import InputForm from './components/InputForm'
import Dashboard from './components/Dashboard'
import { AdviceProvider } from './context/AdviceContext'

const App = () => {
  return (
    <AdviceProvider>
      <div className="min-h-screen bg-green-50 p-6">
        <h1 className="text-3xl font-bold text-center text-green-700 mb-6">
          🌿 Sustainable Farming Assistant
        </h1>
        <InputForm />
        <Dashboard />
      </div>
    </AdviceProvider>
  )
}

export default App
