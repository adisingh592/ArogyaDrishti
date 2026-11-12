import { useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import { Apple, Dumbbell, Moon, Info, AlertCircle, BookmarkCheck, ChevronLeft } from 'lucide-react'
import { useApp } from '../context/AppContext'

function BulletList({ items = [], color = 'text-gray-400' }) {
  if (!items.length) return <p className="text-sm text-gray-400 italic">No data available.</p>
  return (
    <ul className="space-y-1.5">
      {items.map((item, i) => (
        <li key={i} className="text-sm text-gray-600 flex gap-2">
          <span className={color}>•</span>
          <span>{item}</span>
        </li>
      ))}
    </ul>
  )
}

export default function GuidancePage() {
  const navigate = useNavigate()
  const { analysis, loading } = useApp()

  useEffect(() => {
    if (!loading && !analysis) navigate('/upload')
  }, [analysis, loading, navigate])

  if (!analysis) return null

  // Pick the first guidance block (top condition)
  const guidance = analysis.guidance?.[0]
  const conditions = analysis.conditions || []
  const topCondition = conditions.find(c => c.severity > 0) || conditions[0]
  const diseaseName = guidance?.for || topCondition?.condition || 'your condition'

  // Fallback if no guidance block returned
  const food_prefer      = guidance?.food_prefer      || []
  const food_limit       = guidance?.food_limit        || []
  const exercise         = guidance?.exercise          || []
  const lifestyle        = guidance?.lifestyle         || []
  const warning_signs    = guidance?.warning_signs     || []
  const when_to_seek     = guidance?.when_to_seek_help || []

  // Description from conditions evidence
  const conditionDesc = topCondition?.evidence?.join(' ') || null

  return (
    <div className="max-w-6xl mx-auto px-6 py-12">
      <p className="step-label">Step 4 of 4</p>
      <h1 className="font-serif text-4xl font-bold text-gray-900 mb-3">
        Health guidance for {diseaseName}
      </h1>
      <p className="text-gray-500 mb-10 max-w-xl">
        General education related to your screening result. It does not replace advice from your doctor or a dietitian.
      </p>

      <div className="space-y-5">

        {/* Row 1 — Food + Activity */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-5">

          {/* Food */}
          <div className="card p-6">
            <div className="flex items-center gap-2 mb-5">
              <Apple size={20} className="text-[#1a5e52]" />
              <h3 className="font-serif font-bold text-gray-900 text-lg">Food and nutrition</h3>
            </div>
            <p className="text-xs font-semibold text-[#1a5e52] uppercase tracking-wide mb-2">Favour</p>
            <BulletList items={food_prefer} color="text-[#1a5e52]" />
            {food_limit.length > 0 && (
              <>
                <p className="text-xs font-semibold text-orange-500 uppercase tracking-wide mt-4 mb-2">Limit</p>
                <BulletList items={food_limit} color="text-orange-400" />
              </>
            )}
          </div>

          {/* Activity */}
          <div className="card p-6">
            <div className="flex items-center gap-2 mb-5">
              <Dumbbell size={20} className="text-[#1a5e52]" />
              <h3 className="font-serif font-bold text-gray-900 text-lg">Activity and precautions</h3>
            </div>
            <p className="text-xs font-semibold text-[#1a5e52] uppercase tracking-wide mb-2">Recommended</p>
            <BulletList items={exercise} color="text-[#1a5e52]" />
          </div>
        </div>

        {/* Lifestyle — full width */}
        {lifestyle.length > 0 && (
          <div className="card p-6">
            <div className="flex items-center gap-2 mb-4">
              <Moon size={20} className="text-[#1a5e52]" />
              <h3 className="font-serif font-bold text-gray-900 text-lg">Lifestyle</h3>
            </div>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-x-10">
              <BulletList items={lifestyle} />
            </div>
            <p className="text-xs text-gray-400 italic mt-3">
              Small, steady habits matter more than quick fixes.
            </p>
          </div>
        )}

        {/* Row 3 — About + Warnings */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-5">

          {/* About the condition */}
          <div className="card p-6">
            <div className="flex items-center gap-2 mb-4">
              <Info size={20} className="text-[#1a5e52]" />
              <h3 className="font-serif font-bold text-gray-900 text-lg">About the condition</h3>
            </div>
            {conditionDesc ? (
              <p className="text-sm text-gray-600 leading-relaxed">{conditionDesc}</p>
            ) : (
              <p className="text-sm text-gray-500 leading-relaxed">
                {diseaseName} was flagged based on the values in your report. A diagnosis needs
                confirmation by a qualified doctor through clinical evaluation and repeat testing.
              </p>
            )}
            <p className="text-xs text-gray-400 mt-4 italic">
              A diagnosis needs confirmation by a doctor through clinical evaluation and repeat testing.
            </p>
          </div>

          {/* Warning signs */}
          <div className="bg-amber-50 border border-amber-200 rounded-lg p-6">
            <div className="flex items-center gap-2 mb-4">
              <AlertCircle size={20} className="text-amber-500" />
              <h3 className="font-serif font-bold text-gray-900 text-lg">Warning signs &amp; when to see a doctor</h3>
            </div>

            {warning_signs.length > 0 && (
              <>
                <p className="text-xs font-semibold text-orange-500 uppercase tracking-wide mb-2">
                  Book an appointment soon if you notice
                </p>
                <BulletList items={warning_signs} color="text-orange-400" />
              </>
            )}

            {when_to_seek.length > 0 && (
              <>
                <p className="text-xs font-semibold text-red-500 uppercase tracking-wide mt-4 mb-2">
                  Seek emergency care for
                </p>
                <BulletList items={when_to_seek} color="text-red-400" />
              </>
            )}

            {!warning_signs.length && !when_to_seek.length && (
              <p className="text-sm text-gray-500 italic">
                Consult your doctor if symptoms worsen or new symptoms appear.
              </p>
            )}
          </div>
        </div>

        {/* Multiple conditions */}
        {analysis.guidance?.length > 1 && (
          <div className="card p-5">
            <h3 className="font-serif font-bold text-gray-900 mb-3">Other conditions detected</h3>
            <div className="space-y-6">
              {analysis.guidance.slice(1).map((g, i) => (
                <div key={i} className="border-t border-gray-100 pt-4">
                  <p className="text-sm font-semibold text-[#1a5e52] mb-2">{g.for}</p>
                  {g.food_prefer?.length > 0 && (
                    <div className="mb-2">
                      <p className="text-xs text-gray-400 uppercase font-semibold mb-1">Favour</p>
                      <BulletList items={g.food_prefer.slice(0, 3)} />
                    </div>
                  )}
                  {g.warning_signs?.length > 0 && (
                    <div>
                      <p className="text-xs text-gray-400 uppercase font-semibold mb-1">Watch for</p>
                      <BulletList items={g.warning_signs.slice(0, 3)} color="text-orange-400" />
                    </div>
                  )}
                </div>
              ))}
            </div>
          </div>
        )}
      </div>

      {/* Footer */}
      <div className="flex items-center justify-between mt-10 pt-6 border-t border-gray-200">
        <p className="text-xs text-gray-400">
          Source: curated knowledge base, <code className="bg-gray-100 px-1 rounded">disease_information.json</code>
        </p>
        <div className="flex gap-3">
          <button onClick={() => navigate('/results')} className="btn-outline flex items-center gap-2">
            <ChevronLeft size={15} /> Back to result
          </button>
          <button className="btn-primary flex items-center gap-2">
            <BookmarkCheck size={15} /> Save to history
          </button>
        </div>
      </div>
    </div>
  )
}
