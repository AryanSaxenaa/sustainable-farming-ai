import React, { useState } from 'react'
import axios from 'axios'
import { useAdvice } from '../context/AdviceContext'

const InputForm = () => {
  const [location, setLocation] = useState('')
  const [crop, setCrop] = useState('')
  const [soilType, setSoilType] = useState('')
  const [season, setSeason] = useState('')
  const [waterAvailability, setWaterAvailability] = useState('')
  const [previousCrop, setPreviousCrop] = useState('')
  const [pestIssues, setPestIssues] = useState('')
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)
  const { updateAdvice } = useAdvice()

  const handleSubmit = async (e) => {
    e.preventDefault()
    setLoading(true)
    setError(null)
    
    try {
      const res = await axios.post('http://127.0.0.1:5000/query', {
        input: `Location: ${location}, Crop: ${crop}, Soil Type: ${soilType}, Season: ${season}, Water Availability: ${waterAvailability}, Previous Crop: ${previousCrop}, Pest Issues: ${pestIssues}`
      })
      
      if (res.data.error) {
        setError(res.data.error)
        return
      }

      console.log('Response data:', res.data) // Debug log
      
      updateAdvice(
        res.data.advice,
        res.data.metrics,
        res.data.research_sources || []
      )
    } catch (err) {
      console.error('Error fetching advice:', err)
      setError(err.response?.data?.error || 'Failed to get advice. Please try again.')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="bg-white shadow-md rounded p-6 max-w-xl mx-auto">
      <form onSubmit={handleSubmit} className="space-y-4">
        <div>
          <label className="block mb-2 font-semibold text-gray-700">
            Location:
          </label>
          <input
            type="text"
            value={location}
            onChange={(e) => setLocation(e.target.value)}
            className="w-full border rounded p-2 mb-4"
            placeholder="e.g., California"
            required
          />
        </div>

        <div>
          <label className="block mb-2 font-semibold text-gray-700">
            Crop:
          </label>
          <input
            type="text"
            value={crop}
            onChange={(e) => setCrop(e.target.value)}
            className="w-full border rounded p-2 mb-4"
            placeholder="e.g., Tomatoes"
            required
          />
        </div>

        <div>
          <label className="block mb-2 font-semibold text-gray-700">
            Soil Type:
          </label>
          <select
            value={soilType}
            onChange={(e) => setSoilType(e.target.value)}
            className="w-full border rounded p-2 mb-4"
            required
          >
            <option value="">Select Soil Type</option>
            <option value="Loamy">Loamy</option>
            <option value="Sandy">Sandy</option>
            <option value="Clay">Clay</option>
            <option value="Silty">Silty</option>
            <option value="Peaty">Peaty</option>
            <option value="Chalky">Chalky</option>
          </select>
        </div>

        <div>
          <label className="block mb-2 font-semibold text-gray-700">
            Season:
          </label>
          <select
            value={season}
            onChange={(e) => setSeason(e.target.value)}
            className="w-full border rounded p-2 mb-4"
            required
          >
            <option value="">Select Season</option>
            <option value="Spring">Spring</option>
            <option value="Summer">Summer</option>
            <option value="Autumn">Autumn</option>
            <option value="Winter">Winter</option>
          </select>
        </div>

        <div>
          <label className="block mb-2 font-semibold text-gray-700">
            Water Availability:
          </label>
          <select
            value={waterAvailability}
            onChange={(e) => setWaterAvailability(e.target.value)}
            className="w-full border rounded p-2 mb-4"
            required
          >
            <option value="">Select Water Availability</option>
            <option value="High">High (Regular rainfall/irrigation)</option>
            <option value="Medium">Medium (Seasonal rainfall)</option>
            <option value="Low">Low (Limited water access)</option>
          </select>
        </div>

        <div>
          <label className="block mb-2 font-semibold text-gray-700">
            Previous Crop (if any):
          </label>
          <input
            type="text"
            value={previousCrop}
            onChange={(e) => setPreviousCrop(e.target.value)}
            className="w-full border rounded p-2 mb-4"
            placeholder="e.g., Wheat, None"
          />
        </div>

        <div>
          <label className="block mb-2 font-semibold text-gray-700">
            Known Pest Issues:
          </label>
          <input
            type="text"
            value={pestIssues}
            onChange={(e) => setPestIssues(e.target.value)}
            className="w-full border rounded p-2 mb-4"
            placeholder="e.g., Aphids, None"
          />
        </div>

        <button
          type="submit"
          className="w-full bg-green-600 text-white px-4 py-2 rounded hover:bg-green-700 disabled:opacity-50"
          disabled={loading}
        >
          {loading ? 'Getting Advice...' : 'Get Farming Advice'}
        </button>
      </form>

      {loading && (
        <div className="mt-6 text-center">
          <div className="inline-block animate-spin rounded-full h-8 w-8 border-b-2 border-green-600"></div>
        </div>
      )}

      {error && (
        <div className="mt-6 bg-red-100 p-4 rounded">
          <h2 className="font-bold text-red-700">Error:</h2>
          <p>{error}</p>
        </div>
      )}
    </div>
  )
}

export default InputForm
