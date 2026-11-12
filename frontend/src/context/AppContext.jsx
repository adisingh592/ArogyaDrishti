/**
 * Global app state — flows between Upload → Analysis → Results → Guidance
 * Stored in React context so every page can read/write it.
 */
import { createContext, useContext, useState } from 'react'

const AppContext = createContext(null)

export function AppProvider({ children }) {
  const [uploadedFile, setUploadedFile] = useState(null)      // File object
  const [reportType, setReportType]     = useState('Auto-detect')
  const [analysis, setAnalysis]         = useState(null)      // raw API response
  const [loading, setLoading]           = useState(false)
  const [error, setError]               = useState(null)

  // ── call the Flask API ──────────────────────────────────────────────────
  const API_BASE = import.meta.env.VITE_API_URL || 'http://localhost:8000'

  async function runAnalysis(file) {
    setLoading(true)
    setError(null)
    setAnalysis(null)
    try {
      const form = new FormData()
      form.append('file', file)

      let res
      try {
        res = await fetch(`${API_BASE}/api/analyze`, { method: 'POST', body: form })
      } catch (networkErr) {
        throw new Error(
          `Cannot reach the API at ${API_BASE}. ` +
          `Check that VITE_API_URL is set correctly on Vercel and the Railway service is online.`
        )
      }

      // Safe JSON parse — handle empty or non-JSON responses
      const text = await res.text()
      if (!text || text.trim() === '') {
        throw new Error(`Server returned an empty response (HTTP ${res.status}). Check Railway logs.`)
      }

      let data
      try {
        data = JSON.parse(text)
      } catch {
        throw new Error(`Server returned non-JSON response (HTTP ${res.status}): ${text.slice(0, 200)}`)
      }

      if (!res.ok) throw new Error(data.error || `Server error ${res.status}`)
      setAnalysis(data)
      return data
    } catch (err) {
      setError(err.message)
      throw err
    } finally {
      setLoading(false)
    }
  }

  return (
    <AppContext.Provider value={{
      uploadedFile, setUploadedFile,
      reportType, setReportType,
      analysis, setAnalysis,
      loading, error,
      runAnalysis,
    }}>
      {children}
    </AppContext.Provider>
  )
}

export const useApp = () => useContext(AppContext)
