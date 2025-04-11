import React, { createContext, useContext, useState } from 'react'

const AdviceContext = createContext()

export const AdviceProvider = ({ children }) => {
  const [advice, setAdvice] = useState(null)
  const [metrics, setMetrics] = useState(null)
  const [researchSources, setResearchSources] = useState([])

  const updateAdvice = (newAdvice, newMetrics, newResearchSources = []) => {
    setAdvice(newAdvice)
    setMetrics(newMetrics)
    setResearchSources(newResearchSources)
  }

  return (
    <AdviceContext.Provider value={{ advice, metrics, researchSources, updateAdvice }}>
      {children}
    </AdviceContext.Provider>
  )
}

export const useAdvice = () => {
  const context = useContext(AdviceContext)
  if (!context) {
    throw new Error('useAdvice must be used within an AdviceProvider')
  }
  return context
} 