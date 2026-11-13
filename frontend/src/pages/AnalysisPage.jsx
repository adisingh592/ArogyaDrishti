import React, { useEffect } from 'react'
import { useNavigate, Link } from 'react-router-dom'
import { useApp } from '../context/AppContext'

export default function AnalysisPage() {
  const navigate = useNavigate()
  const { analysis, uploadedFile, loading } = useApp()

  useEffect(() => {
    if (!loading && !analysis) navigate('/upload')
  }, [analysis, loading, navigate])

  if (!analysis) return null

  const findings = analysis.findings || []
  const conditions = analysis.conditions || []
  const modelResults = (analysis.model_results || []).filter(m => m.status === 'ran')
  const topCondition = conditions.find(c => c.severity > 0) || conditions[0]
  const valuesCount = Object.keys(analysis.extracted_values || {}).length

  return (
    <div className="py-16 px-5 max-w-[1240px] mx-auto">
      <span className="badge-tag">Step 2 of 3</span>
      
      <h1 className="disp text-[clamp(3.4rem,9vw,6.5rem)] mt-6">
        Your report, <span className="hl">read</span>
      </h1>
      <p className="mt-4 text-lg opacity-70 max-w-xl">
        Here is what ArogyaDrishti found in the report and where the clinical parameters were routed.
      </p>

      {/* Stepper */}
      <ol className="grid grid-cols-1 md:grid-cols-3 gap-5 mt-10">
        <li className="p-5 border border-[rgba(23,30,25,0.1)] rounded-xl bg-white flex gap-3.5 items-center shadow-sm">
          <div className="w-3 h-3 rounded-full bg-[#ffe17c] ring-2 ring-[#171e19] flex-shrink-0" />
          <div>
            <b className="block text-sm font-bold">Report received</b>
            <small className="text-xs opacity-60 truncate block max-w-[200px]">{uploadedFile?.name || 'Uploaded document'}</small>
          </div>
        </li>
        <li className="p-5 border border-[rgba(23,30,25,0.1)] rounded-xl bg-white flex gap-3.5 items-center shadow-sm">
          <div className="w-3 h-3 rounded-full bg-[#ffe17c] ring-2 ring-[#171e19] flex-shrink-0" />
          <div>
            <b className="block text-sm font-bold">Values read</b>
            <small className="text-xs opacity-60">{findings.length || valuesCount} parameters extracted</small>
          </div>
        </li>
        <li className="p-5 border border-[rgba(23,30,25,0.1)] rounded-xl bg-white flex gap-3.5 items-center shadow-sm">
          <div className="w-3 h-3 rounded-full bg-[#ffe17c] ring-2 ring-[#171e19] flex-shrink-0" />
          <div>
            <b className="block text-sm font-bold">Model chosen</b>
            <small className="text-xs opacity-60">
              {topCondition ? `${topCondition.condition} model` : 'General screening'}
            </small>
          </div>
        </li>
      </ol>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mt-8">
        {/* Left: Extracted Parameters Table */}
        <div className="bg-white border border-[rgba(23,30,25,0.1)] rounded-2xl p-8 shadow-sm">
          <div className="flex justify-between text-xs font-bold uppercase tracking-wider opacity-60 pb-3 border-b border-[rgba(23,30,25,0.1)]">
            <span>Extracted parameters</span>
            <span>Status</span>
          </div>

          <div className="divide-y divide-[rgba(23,30,25,0.08)]">
            {findings.length > 0 ? (
              findings.map((f, i) => {
                const isHigh = f.status === 'ABNORMAL' || f.status === 'URGENT' || f.status === 'BORDERLINE'
                return (
                  <div key={i} className="flex justify-between items-center py-3.5 text-sm">
                    <span className="font-medium text-[#171e19]">{f.parameter}</span>
                    <span className="font-mono text-xs flex items-center gap-2">
                      {f.value} {f.unit}
                      <span className={isHigh ? 'chip-hi' : 'chip-ok'}>
                        {f.status}
                      </span>
                    </span>
                  </div>
                )
              })
            ) : (
              Object.entries(analysis.extracted_values || {}).map(([key, val], i) => (
                <div key={i} className="flex justify-between items-center py-3.5 text-sm">
                  <span className="font-medium text-[#171e19] capitalize">{key.replace(/_/g, ' ')}</span>
                  <span className="font-mono text-xs flex items-center gap-2">
                    {val}
                    <span className="chip-ok">MEASURED</span>
                  </span>
                </div>
              ))
            )}
          </div>
        </div>

        {/* Right: Dark Routing Panel */}
        <div className="bg-[#171e19] text-white border border-[rgba(183,198,194,0.1)] rounded-2xl p-8 flex flex-col justify-between">
          <div>
            <h3 className="disp text-3xl mb-3">
              Routed to {topCondition ? topCondition.condition : 'Clinical'} Model
            </h3>
            <p className="text-sm text-[#b7c6c2] leading-relaxed">
              Your values match specific organ markers. The Meta-Classifier selects the disease-screening model matching these biomarkers and infers risk certainty.
            </p>

            {modelResults.length > 0 && (
              <div className="mt-6 space-y-2">
                <span className="text-xs uppercase tracking-wider text-[#b7c6c2]/70 font-semibold block">
                  Active Models Evaluated:
                </span>
                <div className="flex flex-wrap gap-2">
                  {modelResults.map((m, idx) => (
                    <span key={idx} className="bg-white/10 text-[#ffe17c] text-xs font-mono px-2.5 py-1 rounded">
                      {m.label} ({m.probability}%)
                    </span>
                  ))}
                </div>
              </div>
            )}
          </div>

          <div className="flex flex-wrap gap-3 mt-8 items-center">
            <Link to="/results" className="btn-y">
              View results
            </Link>
            <Link to="/upload" className="btn-ghost">
              Upload another
            </Link>
          </div>
        </div>
      </div>
    </div>
  )
}
