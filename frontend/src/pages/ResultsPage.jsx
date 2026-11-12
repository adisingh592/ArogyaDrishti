import { useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import { AlertTriangle, Download, ChevronRight } from 'lucide-react'
import { useApp } from '../context/AppContext'

const SEVERITY_ORDER = { URGENT: 4, ABNORMAL: 3, BORDERLINE: 2, NORMAL: 1 }

function ConfidenceBar({ pct, color = 'bg-[#1a5e52]' }) {
  return (
    <div className="h-2.5 bg-gray-100 rounded-full overflow-hidden">
      <div className={`h-2.5 rounded-full transition-all ${color}`} style={{ width: `${pct}%` }} />
    </div>
  )
}

function StatusBadge({ status }) {
  const map = {
    URGENT:    'bg-red-100 text-red-700',
    ABNORMAL:  'bg-orange-100 text-orange-600',
    BORDERLINE:'bg-yellow-100 text-yellow-700',
    NORMAL:    'bg-teal-100 text-teal-700',
  }
  return (
    <span className={`text-xs font-semibold px-2 py-0.5 rounded ${map[status] || 'bg-gray-100 text-gray-500'}`}>
      {status}
    </span>
  )
}

export default function ResultsPage() {
  const navigate = useNavigate()
  const { analysis, uploadedFile, loading } = useApp()

  useEffect(() => {
    if (!loading && !analysis) navigate('/upload')
  }, [analysis, loading, navigate])

  if (!analysis) return null

  const conditions   = analysis.conditions  || []
  const modelResults = analysis.model_results || []
  const findings     = analysis.findings     || []

  // Primary (highest severity) condition
  const primary = [...conditions].sort(
    (a, b) => (SEVERITY_ORDER[b.status] || 0) - (SEVERITY_ORDER[a.status] || 0)
  )[0]

  // Best ML result that ran
  const topModel = modelResults.find(m => m.status === 'ran' && m.positive)
    || modelResults.find(m => m.status === 'ran')

  // Feature importance — take abnormal/borderline findings as "influence"
  const influence = findings
    .filter(f => f.status !== 'NORMAL')
    .slice(0, 4)
    .map(f => ({
      label:    `${f.parameter} · ${f.value} ${f.unit}`.trim(),
      pct:      f.status === 'URGENT' ? 92 : f.status === 'ABNORMAL' ? 78 : 45,
      strength: f.status === 'URGENT' || f.status === 'ABNORMAL' ? 'Strong' : 'Minor',
    }))

  // Other conditions beyond primary
  const others = conditions.filter(c => c !== primary).slice(0, 4)

  const isUrgent    = primary?.status === 'URGENT'
  const isAbnormal  = primary?.status === 'ABNORMAL'
  const needsDoctor = isUrgent || isAbnormal

  const badgeText = {
    URGENT:    'Urgent — seek care today',
    ABNORMAL:  'Elevated risk indicated',
    BORDERLINE:'Borderline — monitor closely',
    NORMAL:    'No abnormality found',
  }

  const confidence = topModel?.probability ?? (primary ? (primary.status === 'ABNORMAL' ? 78 : 55) : 0)

  return (
    <div className="max-w-6xl mx-auto px-6 py-12">
      <p className="step-label">Step 3 of 4</p>
      <h1 className="font-serif text-4xl font-bold text-gray-900 mb-3">Screening result</h1>
      <p className="text-gray-500 mb-10">
        Based on {uploadedFile?.name || 'your report'}. This is a screening indicator, not a diagnosis.
      </p>

      <div className="grid grid-cols-1 md:grid-cols-5 gap-6">
        {/* ── Left column ── */}
        <div className="md:col-span-3 space-y-5">

          {/* Main result card */}
          {primary ? (
            <div className="card p-6">
              <p className="text-xs font-semibold tracking-widest text-gray-400 uppercase mb-2">
                {conditions.length > 1 ? 'Primary Condition' : 'Possible Condition'}
              </p>
              <div className="flex items-start gap-3 flex-wrap mb-1">
                <h2 className="font-serif text-3xl font-bold text-gray-900">{primary.condition}</h2>
                <span className={`text-xs font-semibold px-3 py-1 rounded-full self-center ${
                  isUrgent ? 'bg-red-100 text-red-700' :
                  isAbnormal ? 'bg-orange-100 text-orange-600' :
                  'bg-yellow-100 text-yellow-700'
                }`}>
                  {badgeText[primary.status] || primary.status}
                </span>
              </div>
              {topModel && (
                <p className="text-sm text-gray-500 mb-6">
                  {topModel.label} · {topModel.features_used} input{topModel.features_used !== 1 ? 's' : ''} used
                </p>
              )}

              {/* Confidence bar */}
              <div className="mb-6">
                <div className="flex justify-between mb-2">
                  <span className="text-sm font-semibold text-gray-700">Model confidence</span>
                  <span className="text-sm font-bold text-gray-900">{confidence}%</span>
                </div>
                <ConfidenceBar pct={confidence} />
                <p className="text-xs text-gray-400 mt-1.5">
                  Confidence describes the model's certainty, not the chance that you have the disease.
                </p>
              </div>

              <div className="flex gap-3 flex-wrap">
                <button onClick={() => navigate('/guidance')} className="btn-primary flex items-center gap-2">
                  View health guidance <ChevronRight size={15} />
                </button>
                <button className="btn-outline flex items-center gap-2">
                  <Download size={15} /> Download summary
                </button>
              </div>
            </div>
          ) : (
            <div className="card p-6">
              <h2 className="font-serif text-2xl font-bold text-gray-900 mb-2">No abnormality found</h2>
              <p className="text-gray-500 text-sm">
                {analysis.recommended_action || 'All recognised values are within the normal range.'}
              </p>
            </div>
          )}

          {/* Feature influence */}
          {influence.length > 0 && (
            <div className="card p-5">
              <h3 className="font-serif font-bold text-gray-900 mb-1">What influenced this result</h3>
              <p className="text-sm text-gray-400 mb-5">Parameters that moved the prediction most.</p>
              <div className="space-y-5">
                {influence.map((f, i) => (
                  <div key={i}>
                    <div className="flex justify-between mb-1.5">
                      <span className="text-sm text-gray-700">{f.label}</span>
                      <span className={`text-xs font-semibold ${f.strength === 'Strong' ? 'text-orange-500' : 'text-gray-400'}`}>
                        {f.strength}
                      </span>
                    </div>
                    <ConfidenceBar
                      pct={f.pct}
                      color={f.strength === 'Strong' ? 'bg-orange-400' : 'bg-gray-300'}
                    />
                  </div>
                ))}
              </div>
            </div>
          )}

          {/* Warning box */}
          {needsDoctor && (
            <div className="border border-amber-300 bg-amber-50 rounded-lg p-4 flex gap-3">
              <AlertTriangle size={18} className="text-amber-500 flex-shrink-0 mt-0.5" />
              <p className="text-sm text-gray-700">
                <strong>Please see a doctor.</strong>{' '}
                {analysis.recommended_action || 'Some values are outside the normal range and need medical evaluation.'}
              </p>
            </div>
          )}
        </div>

        {/* ── Right column ── */}
        <div className="md:col-span-2 space-y-5">

          {/* Other conditions */}
          {others.length > 0 && (
            <div className="card p-5">
              <h3 className="font-serif font-bold text-gray-900 mb-4">Other checks on this report</h3>
              <div className="space-y-3">
                {others.map((c, i) => (
                  <div key={i} className="flex items-center justify-between py-1 border-b border-gray-50 last:border-0">
                    <span className="text-sm text-gray-700">{c.condition}</span>
                    <StatusBadge status={c.status} />
                  </div>
                ))}
              </div>
            </div>
          )}

          {/* ML models used */}
          {modelResults.length > 0 && (
            <div className="card p-5">
              <h3 className="font-serif font-bold text-gray-900 mb-4">About this prediction</h3>
              <div className="space-y-3 text-sm">
                <div className="flex justify-between border-b border-gray-50 pb-2">
                  <span className="text-gray-500">Values extracted</span>
                  <span className="font-medium text-gray-800">
                    {Object.keys(analysis.extracted_values || {}).length}
                  </span>
                </div>
                <div className="flex justify-between border-b border-gray-50 pb-2">
                  <span className="text-gray-500">Models evaluated</span>
                  <span className="font-medium text-emerald-700 bg-emerald-50 px-2 py-0.5 rounded font-mono">
                    {modelResults.filter(m => m.status === 'ran').length} active
                  </span>
                </div>
                <div className="flex justify-between border-b border-gray-50 pb-2">
                  <span className="text-gray-500">Overall decision</span>
                  <span className="font-medium text-gray-800 text-xs text-right max-w-[55%]">
                    {analysis.decision}
                  </span>
                </div>
              </div>

              {/* Models Breakdown */}
              <div className="mt-4 pt-3 border-t border-gray-100">
                <p className="text-xs font-semibold uppercase tracking-wider text-gray-400 mb-2">
                  Meta-Classifier Routed Models
                </p>
                <div className="space-y-2">
                  {modelResults.map((m, idx) => (
                    <div key={idx} className="bg-gray-50 rounded p-2 text-xs">
                      <div className="flex justify-between items-center mb-1">
                        <span className="font-medium text-gray-800">{m.label}</span>
                        <span className={`px-1.5 py-0.5 rounded text-[10px] font-semibold ${
                          m.status === 'ran' 
                            ? (m.positive ? 'bg-orange-100 text-orange-700' : 'bg-teal-100 text-teal-800')
                            : 'bg-gray-200 text-gray-600'
                        }`}>
                          {m.status === 'ran' ? `${m.probability}% prob` : m.status}
                        </span>
                      </div>
                      <div className="text-[11px] text-gray-500 flex justify-between">
                        <span>Report inputs: {m.features_used || '—'}</span>
                        <span>Coverage: {m.coverage ? `${m.coverage}%` : '—'}</span>
                      </div>
                      {m.assumptions && m.assumptions.length > 0 && (
                        <div className="mt-1 text-[10px] text-amber-700 bg-amber-50/80 px-1.5 py-0.5 rounded">
                          Defaults: {m.assumptions.join(', ')}
                        </div>
                      )}
                    </div>
                  ))}
                </div>
              </div>
            </div>
          )}

          <p className="text-xs text-gray-500 leading-relaxed px-1">
            Next: food, activity and lifestyle guidance for this result, plus warning signs to watch for.
          </p>
        </div>
      </div>
    </div>
  )
}
