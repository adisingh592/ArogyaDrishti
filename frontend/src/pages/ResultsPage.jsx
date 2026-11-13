import React, { useEffect } from 'react'
import { useNavigate, Link } from 'react-router-dom'
import { useApp } from '../context/AppContext'

export default function ResultsPage() {
  const navigate = useNavigate()
  const { analysis, loading } = useApp()

  useEffect(() => {
    if (!loading && !analysis) navigate('/upload')
  }, [analysis, loading, navigate])

  if (!analysis) return null

  const findings = analysis.findings || []
  const conditions = analysis.conditions || []
  const modelResults = (analysis.model_results || []).filter(m => m.status === 'ran')

  // Count metrics
  const totalParams = findings.length || Object.keys(analysis.extracted_values || {}).length
  const aboveRange = findings.filter(f => f.status === 'ABNORMAL' || f.status === 'URGENT' || f.status === 'BORDERLINE').length
  const inRange = totalParams - aboveRange

  const primary = conditions.find(c => c.severity > 0) || conditions[0]
  const conditionName = primary?.condition || 'Multi-Disease'

  const flagged = findings.filter(f => f.status !== 'NORMAL')

  return (
    <div className="py-16 px-5 max-w-[1240px] mx-auto">
      <span className="badge-tag">Step 3 of 3</span>
      
      <h1 className="disp text-[clamp(3.4rem,9vw,6.5rem)] mt-6">
        Your <span className="hl">results</span>
      </h1>
      <p className="mt-4 text-lg opacity-70 max-w-xl">
        A quick summary of the clinical parameters and what the screening models detected.
      </p>

      {/* 3 Metric Tiles */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-5 mt-10">
        <div className="p-7 border border-[rgba(23,30,25,0.1)] rounded-2xl bg-white shadow-sm">
          <b className="disp text-[clamp(4rem,7vw,6rem)] block text-[#171e19]">{totalParams}</b>
          <span className="text-xs font-bold uppercase tracking-[0.16em] opacity-60">Parameters read</span>
        </div>
        <div className="p-7 border border-transparent rounded-2xl bg-[#ffe17c] text-[#171e19] shadow-sm">
          <b className="disp text-[clamp(4rem,7vw,6rem)] block">{aboveRange}</b>
          <span className="text-xs font-bold uppercase tracking-[0.16em] opacity-80">Above range</span>
        </div>
        <div className="p-7 border border-[rgba(23,30,25,0.1)] rounded-2xl bg-white shadow-sm">
          <b className="disp text-[clamp(4rem,7vw,6rem)] block text-[#171e19]">{Math.max(0, inRange)}</b>
          <span className="text-xs font-bold uppercase tracking-[0.16em] opacity-60">In range</span>
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mt-8">
        {/* Left Dark Outcome Panel */}
        <div className="bg-[#171e19] text-white border border-[rgba(183,198,194,0.1)] rounded-2xl p-8 flex flex-col justify-between">
          <div>
            <span className="badge-tag !bg-transparent !text-white !border-[rgba(183,198,194,0.2)]">
              Screening Outcome
            </span>

            <h3 className="disp text-3xl mt-5">
              {conditionName} screening: {aboveRange > 0 ? 'worth discussing with a doctor' : 'within normal baseline'}
            </h3>
            
            <p className="mt-4 text-sm text-[#b7c6c2] leading-relaxed">
              {analysis.recommended_action || 'Predictions are not a confirmed medical diagnosis. Please review these findings with a licensed healthcare professional.'}
            </p>

            {/* Model Breakdown */}
            {modelResults.length > 0 && (
              <div className="mt-6 pt-5 border-t border-[rgba(183,198,194,0.15)] space-y-2">
                <span className="text-xs uppercase tracking-wider text-[#b7c6c2]/80 font-bold block">
                  Model Inference:
                </span>
                {modelResults.map((m, idx) => (
                  <div key={idx} className="flex justify-between items-center text-xs bg-white/5 p-2 rounded">
                    <span className="text-white font-medium">{m.label}</span>
                    <span className="font-mono text-[#ffe17c]">{m.probability}% risk</span>
                  </div>
                ))}
              </div>
            )}
          </div>

          <div className="flex flex-wrap gap-3 mt-8 items-center">
            <Link to="/guidance" className="btn-y">
              See guidance
            </Link>
            <Link to="/upload" className="btn-ghost">
              Upload another
            </Link>
          </div>
        </div>

        {/* Right Flagged Values Panel */}
        <div className="bg-white border border-[rgba(23,30,25,0.1)] rounded-2xl p-8 shadow-sm">
          <div className="flex justify-between text-xs font-bold uppercase tracking-wider opacity-60 pb-3 border-b border-[rgba(23,30,25,0.1)]">
            <span>Flagged values</span>
            <span>Classification</span>
          </div>

          <div className="divide-y divide-[rgba(23,30,25,0.08)]">
            {flagged.length > 0 ? (
              flagged.map((f, i) => (
                <div key={i} className="flex justify-between items-center py-3.5 text-sm">
                  <span className="font-medium text-[#171e19]">{f.parameter}</span>
                  <span className="font-mono text-xs flex items-center gap-2">
                    {f.value} {f.unit}
                    <span className="chip-hi">{f.status}</span>
                  </span>
                </div>
              ))
            ) : (
              <p className="py-8 text-sm opacity-60 text-center italic">
                All extracted laboratory parameters are within normal reference ranges.
              </p>
            )}
          </div>
        </div>
      </div>
    </div>
  )
}
