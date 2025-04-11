import React from 'react'
import { useAdvice } from '../context/AdviceContext'

const Dashboard = () => {
  const { advice, metrics, researchSources } = useAdvice()

  if (!advice) {
    return (
      <div className="text-center mt-8 text-gray-600">
        <p>Use the form above to get expert farming advice based on your crop and region.</p>
      </div>
    )
  }

  const renderMetrics = () => {
    if (!metrics) return null
    
    return (
      <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-8">
        {Object.entries(metrics).map(([key, value]) => {
          if (value === null) return null
          
          const formattedKey = key.split('_').map(word => 
            word.charAt(0).toUpperCase() + word.slice(1)
          ).join(' ')
          
          return (
            <div key={key} className="bg-white p-4 rounded-lg shadow-sm">
              <h3 className="text-sm text-gray-500">{formattedKey}</h3>
              <p className="text-xl font-semibold text-green-600">
                {typeof value === 'number' ? value.toFixed(1) : value}
              </p>
            </div>
          )
        })}
      </div>
    )
  }

  const renderResearchSources = () => {
    if (!researchSources || researchSources.length === 0) return null

    return (
      <div className="mb-6">
        <h2 className="text-xl font-semibold text-green-700 mb-3">Research Sources</h2>
        <ul className="list-disc list-inside space-y-2 text-gray-700">
          {researchSources.map((source, index) => (
            <li key={index} className="ml-4">
              <a href={source} target="_blank" rel="noopener noreferrer" className="text-blue-600 hover:underline">
                {source}
              </a>
            </li>
          ))}
        </ul>
      </div>
    )
  }

  const renderAdvice = () => {
    if (!advice) return null

    // Split the advice into sections
    const sections = advice.split('\n\n').filter(section => section.trim())
    
    return sections.map((section, index) => {
      const [title, ...content] = section.split('\n')
      return (
        <div key={index} className="mb-6">
          <h2 className="text-xl font-semibold text-green-700 mb-3">{title}</h2>
          <ul className="list-disc list-inside space-y-2 text-gray-700">
            {content.map((item, i) => (
              <li key={i} className="ml-4">{item.trim()}</li>
            ))}
          </ul>
        </div>
      )
    })
  }

  return (
    <div className="max-w-4xl mx-auto mt-8">
      {renderMetrics()}
      <div className="bg-white p-6 rounded-lg shadow-sm">
        {renderResearchSources()}
        {renderAdvice()}
      </div>
    </div>
  )
}

export default Dashboard
