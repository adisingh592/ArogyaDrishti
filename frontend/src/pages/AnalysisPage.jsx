import { useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import { ArrowRight, AlertCircle } from 'lucide-react'
import { useApp } from '../context/AppContext'

const SEVERITY_COLOR = {
  'URGENT':     'badge-high',
  'ABNORMAL':   'badge-high',
  'BORDERLINE': 'bg-yellow-100 text-yellow-700 text-xs font-semibold px-2 py-0.5 rounded',
  'NORMAL':     'badge-normal',
}

const STATUS_DOC_COLOR = {
  'URGENT':     'bg-red-50 border border-red-200',
  'ABNORMAL':   'bg-orange-50 border border-orange-200',
  'BORDERLINE': 'bg-yellow-50 border border-yellow-200',
  'NORMAL':     'bg-teal-50 border border-teal-100',
}

export default function AnalysisPage() {
  const navigate = useNavigate()
  const { analysis, uploadedFile, loading } = useApp()

  // redirect to upload if no data
  useEffect(() => {
    if (!loading && !analysis) navigate('/upload')
  }, [analysis, loading, navigate])

  if (!analysis) return null

  const findings    = analysis.findings || []
  const conditions  = analysis.conditions || []
  const values      = analysis.extracted_values || {}
  const modelResults = (analysis.model_results || []).filter(m => m.status === 'ran')

  // Top condition for routing display
  const topCondition = conditions.find(c => c.severity > 0) || conditions[0]

  return (
    <div className="max-w-6xl mx-auto px-6 py-12">
      <p className="step-label">Step 2 of 4</p>
      <h1 className="font-serif text-4xl font-bold text-gray-900 mb-3">What we found in your report</h1>
      <p className="text-gray-500 mb-10">
        Check the extracted values before screening. Anything misread can be corrected.
      </p>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {/* Document preview — extracted values */}
        <div className="card p-5">
          <div className="flex items-center justify-between mb-4 pb-2 border-b border-gray-100">
            <span className="text-sm font-semibold text-gray-700 truncate">
              {uploadedFile?.name || 'report'}
            </span>
            <span className="text-xs text-gray-400 ml-2 flex-shrink-0">EXTRACTED VALUES</span>
          </div>

          {Object.keys(values).length === 0 ? (
            <div className="flex items-center gap-2 text-amber-600 bg-amber-50 rounded p-3">
              <AlertCircle size={16} />
              <p className="text-sm">No standard values were recognised in this report.</p>
            </div>
          ) : (
            <div className="space-y-1.5">
              {Object.entries(values).map(([key, val]) => {
                const finding = findings.find(f =>
                  f.parameter?.toLowerCase().includes(key.toLowerCase()) ||
                  key.toLowerCase().includes(f.parameter?.toLowerCase())
                )
                const sev = finding?.severity_label || finding?.status || 'NORMAL'
                return (
                  <div
                    key={key}
                    className={`flex justify-between items-center px-3 py-2 rounded text-sm ${STATUS_DOC_COLOR[sev] || STATUS_DOC_COLOR['NORMAL']}`}
                  >
                    <span className="text-gray-700 capitalize">{key.replace(/_/g, ' ')}</span>
                    <span className="font-medium text-gray-800">{typeof val === 'number' ? val.toFixed(1) : val}</span>
                  </div>
                )
              })}
            </div>
          )}

          {/* Model info */}
          {modelResults.length > 0 && (
            <div className="mt-4 pt-3 border-t border-gray-100 space-y-1">
              {modelResults.map(m => (
                <p key={m.model} className="text-xs text-gray-500">
                  🤖 <span className="font-medium">{m.label}</span> — {m.probability}% probability
                </p>
              ))}
            </div>
          )}
        </div>

        {/* Right panel */}
        <div className="space-y-5">
          {/* Findings table */}
          <div className="card p-5">
            <div className="flex items-center justify-between mb-4">
              <h3 className="font-serif font-bold text-gray-900">Extracted parameters</h3>
              <span className="text-xs text-gray-400">
                {findings.length} found · {findings.filter(f => f.status === 'URGENT' || f.status === 'ABNORMAL').length} flagged
              </span>
            </div>
            {findings.length === 0 ? (
              <p className="text-sm text-gray-400 italic">No flags raised for supported tests.</p>
            ) : (
              <table className="w-full text-sm">
                <thead>
                  <tr className="border-b border-gray-100">
                    {['Parameter', 'Value', 'Reference', 'Status'].map(h => (
                      <th key={h} className="text-left text-xs text-gray-400 font-semibold pb-2 uppercase tracking-wide">{h}</th>
                    ))}
                  </tr>
                </thead>
                <tbody>
                  {findings.map((f, i) => (
                    <tr key={i} className="border-b border-gray-50 last:border-0">
                      <td className="py-2.5 text-gray-700 pr-2">{f.parameter}</td>
                      <td className="py-2.5 text-gray-800 font-medium pr-2">{f.value} {f.unit}</td>
                      <td className="py-2.5 text-gray-500 pr-2 text-xs">{f.reference || '—'}</td>
                      <td className="py-2.5">
                        <span className={SEVERITY_COLOR[f.status] || SEVERITY_COLOR['NORMAL']}>
                          {f.status}
                        </span>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            )}
          </div>

          {/* Disease routing */}
          {topCondition && (
            <div className="card p-5">
              <p className="text-xs font-semibold tracking-widest text-[#1a5e52] uppercase mb-4">Disease Routing</p>
              <div className="flex items-center gap-2 flex-wrap mb-4">
                <span className="border border-gray-300 rounded-md px-3 py-1.5 text-sm text-gray-700">
                  {uploadedFile?.name?.endsWith('.pdf') ? 'PDF report' : 'Medical report'}
                </span>
                <ArrowRight size={16} className="text-gray-400 flex-shrink-0" />
                <span className="border border-gray-300 rounded-md px-3 py-1.5 text-sm text-gray-700">
                  {conditions.length} condition{conditions.length !== 1 ? 's' : ''} evaluated
                </span>
                <ArrowRight size={16} className="text-gray-400 flex-shrink-0" />
                <span className="btn-primary text-sm py-1.5 cursor-default">
                  {topCondition.condition}
                </span>
              </div>
              <p className="text-xs text-gray-500 leading-relaxed">
                {analysis.recommended_action || 'Review the findings above with your healthcare provider.'}
              </p>
            </div>
          )}
        </div>
      </div>

      {/* Actions */}
      <div className="flex items-center gap-3 mt-8">
        <button onClick={() => navigate('/results')} className="btn-primary">
          View screening result
        </button>
        <button onClick={() => navigate('/upload')} className="btn-outline">
          Upload a different report
        </button>
      </div>
    </div>
  )
}
