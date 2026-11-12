import { useNavigate } from 'react-router-dom'
import { Apple, Dumbbell, Moon, Info, AlertCircle, BookmarkCheck } from 'lucide-react'

const foodData = {
  favor: [
    'Vegetables and leafy greens',
    'Whole grains such as millets, oats and brown rice',
    'Lentils, beans and chickpeas',
    'Nuts, seeds and lean protein',
  ],
  limit: [
    'Sugary drinks and sweets',
    'Refined flour and white bread',
    'Deep-fried and processed snacks',
  ],
  tip: 'Eat at regular times and keep portions moderate.',
}

const activityData = {
  recommended: [
    'Brisk walking, cycling or swimming',
    'About 150 minutes of moderate activity a week',
    'Light strength exercises twice a week',
    'A short walk after meals',
  ],
  precautions: [
    'Ask your doctor before starting intense exercise',
    'Stay hydrated',
    'Stop and rest if you feel dizzy or unwell',
  ],
}

const lifestyle = [
  'Sleep 7 to 9 hours each night',
  'Make time to manage stress',
  'Avoid tobacco and limit alcohol',
  'Work toward a healthy body weight',
  'Repeat blood tests as your doctor advises',
]

const warningBook = [
  'Constant thirst or frequent urination',
  'Unexplained weight loss or tiredness',
  'Blurred vision or slow-healing wounds',
]

const warningEmergency = [
  'Confusion, drowsiness or fainting',
  'Persistent vomiting or fruity-smelling breath',
  'Severe weakness or trouble breathing',
]

export default function GuidancePage() {
  const navigate = useNavigate()

  return (
    <div className="max-w-6xl mx-auto px-6 py-12">
      <p className="step-label">Step 4 of 4</p>
      <h1 className="font-serif text-4xl font-bold text-gray-900 mb-3">Health guidance for diabetes</h1>
      <p className="text-gray-500 mb-10 max-w-xl">
        General education related to your screening result. It does not replace advice from your doctor or a dietitian.
      </p>

      <div className="space-y-5">
        {/* Row 1 */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-5">
          {/* Food */}
          <div className="card p-6">
            <div className="flex items-center gap-2 mb-4">
              <Apple size={20} className="text-[#1a5e52]" />
              <h3 className="font-serif font-bold text-gray-900 text-lg">Food and nutrition</h3>
            </div>
            <p className="text-xs font-semibold text-[#1a5e52] uppercase tracking-wide mb-2">Favor</p>
            <ul className="space-y-1 mb-4">
              {foodData.favor.map((f) => (
                <li key={f} className="text-sm text-gray-600 flex gap-2">
                  <span className="text-gray-400">•</span>{f}
                </li>
              ))}
            </ul>
            <p className="text-xs font-semibold text-orange-500 uppercase tracking-wide mb-2">Limit</p>
            <ul className="space-y-1 mb-4">
              {foodData.limit.map((f) => (
                <li key={f} className="text-sm text-gray-600 flex gap-2">
                  <span className="text-gray-400">•</span>{f}
                </li>
              ))}
            </ul>
            <p className="text-xs text-gray-400 italic">{foodData.tip}</p>
          </div>

          {/* Activity */}
          <div className="card p-6">
            <div className="flex items-center gap-2 mb-4">
              <Dumbbell size={20} className="text-[#1a5e52]" />
              <h3 className="font-serif font-bold text-gray-900 text-lg">Activity and precautions</h3>
            </div>
            <p className="text-xs font-semibold text-[#1a5e52] uppercase tracking-wide mb-2">Recommended</p>
            <ul className="space-y-1 mb-4">
              {activityData.recommended.map((f) => (
                <li key={f} className="text-sm text-gray-600 flex gap-2">
                  <span className="text-gray-400">•</span>{f}
                </li>
              ))}
            </ul>
            <p className="text-xs font-semibold text-orange-500 uppercase tracking-wide mb-2">Precautions</p>
            <ul className="space-y-1">
              {activityData.precautions.map((f) => (
                <li key={f} className="text-sm text-gray-600 flex gap-2">
                  <span className="text-gray-400">•</span>{f}
                </li>
              ))}
            </ul>
          </div>
        </div>

        {/* Lifestyle — full width */}
        <div className="card p-6">
          <div className="flex items-center gap-2 mb-4">
            <Moon size={20} className="text-[#1a5e52]" />
            <h3 className="font-serif font-bold text-gray-900 text-lg">Lifestyle</h3>
          </div>
          <ul className="grid grid-cols-1 md:grid-cols-2 gap-x-10 gap-y-1.5 mb-4">
            {lifestyle.map((f) => (
              <li key={f} className="text-sm text-gray-600 flex gap-2">
                <span className="text-gray-400">•</span>{f}
              </li>
            ))}
          </ul>
          <p className="text-xs text-gray-400 italic">Small, steady habits matter more than quick fixes.</p>
        </div>

        {/* Row 3 */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-5">
          {/* About the condition */}
          <div className="card p-6">
            <div className="flex items-center gap-2 mb-4">
              <Info size={20} className="text-[#1a5e52]" />
              <h3 className="font-serif font-bold text-gray-900 text-lg">About the condition</h3>
            </div>
            <p className="text-sm text-gray-600 leading-relaxed mb-3">
              Diabetes is a long-term condition in which the body cannot keep blood sugar in a healthy range.
              Two measures often used in reports are fasting glucose and HbA1c, which reflects average blood
              sugar over about three months.
            </p>
            <p className="text-sm text-gray-600 leading-relaxed">
              A diagnosis needs confirmation by a doctor through clinical evaluation and repeat testing.
            </p>
          </div>

          {/* Warning signs */}
          <div className="bg-amber-50 border border-amber-200 rounded-lg p-6">
            <div className="flex items-center gap-2 mb-4">
              <AlertCircle size={20} className="text-amber-500" />
              <h3 className="font-serif font-bold text-gray-900 text-lg">Warning signs and when to see a doctor</h3>
            </div>
            <p className="text-xs font-semibold text-orange-500 uppercase tracking-wide mb-2">
              Book an appointment soon if you notice
            </p>
            <ul className="space-y-1 mb-4">
              {warningBook.map((f) => (
                <li key={f} className="text-sm text-gray-700 flex gap-2">
                  <span className="text-orange-400">•</span>{f}
                </li>
              ))}
            </ul>
            <p className="text-xs font-semibold text-orange-500 uppercase tracking-wide mb-2">
              Seek emergency care for
            </p>
            <ul className="space-y-1">
              {warningEmergency.map((f) => (
                <li key={f} className="text-sm text-gray-700 flex gap-2">
                  <span className="text-orange-400">•</span>{f}
                </li>
              ))}
            </ul>
          </div>
        </div>
      </div>

      {/* Footer actions */}
      <div className="flex items-center justify-between mt-10 pt-6 border-t border-gray-200">
        <p className="text-xs text-gray-400">
          Source: curated knowledge base, <code className="bg-gray-100 px-1 rounded">diabetes.json</code>
        </p>
        <div className="flex gap-3">
          <button onClick={() => navigate('/results')} className="btn-outline flex items-center gap-2">
            Back to result
          </button>
          <button className="btn-primary flex items-center gap-2">
            <BookmarkCheck size={15} />
            Save to history
          </button>
        </div>
      </div>
    </div>
  )
}
