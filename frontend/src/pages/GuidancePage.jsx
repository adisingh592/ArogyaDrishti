import React, { useEffect } from 'react'
import { useNavigate, Link } from 'react-router-dom'
import { Check } from 'lucide-react'
import { useApp } from '../context/AppContext'

export default function GuidancePage() {
  const navigate = useNavigate()
  const { analysis, loading } = useApp()

  useEffect(() => {
    if (!loading && !analysis) navigate('/upload')
  }, [analysis, loading, navigate])

  if (!analysis) return null

  const guidance = analysis.guidance?.[0]
  const conditions = analysis.conditions || []
  const topCondition = conditions.find(c => c.severity > 0) || conditions[0]
  const conditionName = guidance?.for || topCondition?.condition || 'your health'

  const foodPrefer = guidance?.food_prefer?.length ? guidance.food_prefer : [
    'Favor fresh vegetables, leafy greens and whole grains',
    'Include fiber-rich lentils, chickpeas and beans',
    'Keep meals consistent with portion control',
  ]

  const warnings = (guidance?.warning_signs?.length || guidance?.when_to_seek_help?.length)
    ? [...(guidance?.warning_signs || []).slice(0, 2), ...(guidance?.when_to_seek_help || []).slice(0, 1)]
    : [
      'Share this screening summary with a certified doctor',
      'Ask if repeat blood assays are recommended',
      'Seek emergency care immediately if feeling faint or breathless',
    ]

  const exercise = guidance?.exercise?.length ? guidance.exercise : [
    'Start with a brisk daily walk you can maintain consistently',
    'Incorporate short movement breaks throughout the day',
    'Build up intensity gradually and stop if dizziness occurs',
  ]

  return (
    <div className="py-16 px-5 max-w-[1240px] mx-auto">
      <span className="badge-tag">After your results</span>

      <h1 className="disp text-[clamp(3.4rem,9vw,6.5rem)] mt-6">
        Guidance for {conditionName}, written <span className="hl">plainly</span>
      </h1>
      <p className="mt-4 text-lg opacity-70 max-w-xl">
        What to eat, how to move and when to see a healthcare professional.
      </p>

      {/* 3 Tier Cards */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mt-12 items-start">
        {/* Tier 1: Food */}
        <article className="p-8 border border-[rgba(23,30,25,0.1)] rounded-2xl bg-white shadow-sm hover:-translate-y-1 transition-transform">
          <span className="badge-tag text-xs">Food &amp; Nutrition</span>
          <h3 className="disp text-3xl my-6">What to eat</h3>
          <ul className="space-y-3.5 text-sm">
            {foodPrefer.map((item, idx) => (
              <li key={idx} className="flex gap-3 items-start border-t border-[rgba(23,30,25,0.1)] pt-3">
                <span className="w-4 h-4 rounded-full bg-[#ffe17c] flex items-center justify-center text-[#171e19] flex-shrink-0 mt-0.5">
                  <Check size={11} strokeWidth={3} />
                </span>
                <span className="opacity-80">{item}</span>
              </li>
            ))}
          </ul>
        </article>

        {/* Tier 2: Doctor (Mid card elevated in dark) */}
        <article className="p-8 border border-[rgba(183,198,194,0.15)] rounded-2xl bg-[#171e19] text-white shadow-xl md:translate-y-4 hover:md:translate-y-2 transition-transform">
          <span className="badge-tag !bg-transparent !text-white !border-[rgba(183,198,194,0.2)] text-xs">
            Most important
          </span>
          <h3 className="disp text-3xl my-6">When to see a doctor</h3>
          <ul className="space-y-3.5 text-sm text-[#b7c6c2]">
            {warnings.map((item, idx) => (
              <li key={idx} className="flex gap-3 items-start border-t border-[rgba(183,198,194,0.15)] pt-3">
                <span className="w-4 h-4 rounded-full bg-[#ffe17c] flex items-center justify-center text-[#171e19] flex-shrink-0 mt-0.5">
                  <Check size={11} strokeWidth={3} />
                </span>
                <span>{item}</span>
              </li>
            ))}
          </ul>
        </article>

        {/* Tier 3: Movement */}
        <article className="p-8 border border-[rgba(23,30,25,0.1)] rounded-2xl bg-white shadow-sm hover:-translate-y-1 transition-transform">
          <span className="badge-tag text-xs">Physical Activity</span>
          <h3 className="disp text-3xl my-6">How to move</h3>
          <ul className="space-y-3.5 text-sm">
            {exercise.map((item, idx) => (
              <li key={idx} className="flex gap-3 items-start border-t border-[rgba(23,30,25,0.1)] pt-3">
                <span className="w-4 h-4 rounded-full bg-[#ffe17c] flex items-center justify-center text-[#171e19] flex-shrink-0 mt-0.5">
                  <Check size={11} strokeWidth={3} />
                </span>
                <span className="opacity-80">{item}</span>
              </li>
            ))}
          </ul>
        </article>
      </div>

      <p className="mt-14 text-xs opacity-60 max-w-xl">
        General educational suggestions from clinical knowledge base (WHO, ADA, AHA). Not individual medical advice. Please consult a doctor for personalized evaluation.
      </p>

      <div className="flex flex-wrap gap-4 mt-8 items-center">
        <Link to="/upload" className="btn-y">
          Upload another report
        </Link>
        <Link to="/" className="btn-ghost">
          Back to home
        </Link>
      </div>
    </div>
  )
}
