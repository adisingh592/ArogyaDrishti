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
      const res = await fetch(`${API_BASE}/api/analyze`, { method: 'POST', body: form })
      const data = await res.json()
      if (!res.ok) throw new Error(data.error || 'Server error')
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
