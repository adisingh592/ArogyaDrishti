import { useNavigate } from 'react-router-dom'
import { AlertTriangle, Download } from 'lucide-react'

const featureImportance = [
  { label: 'HbA1c · 6.9 %', strength: 'Strong', pct: 88 },
  { label: 'Fasting glucose · 142 mg/dL', strength: 'Strong', pct: 76 },
  { label: 'Total cholesterol · 214 mg/dL', strength: 'Minor', pct: 25 },
]

const otherChecks = [
  { name: 'Chronic kidney disease', status: 'NO FLAG', variant: 'normal' },
  { name: 'Anemia', status: 'NO FLAG', variant: 'normal' },
  { name: 'Heart disease', status: 'NEEDS MORE DATA', variant: 'gray' },
]

export default function ResultsPage() {
  const navigate = useNavigate()

  return (
    <div className="max-w-6xl mx-auto px-6 py-12">
      <p className="step-label">Step 3 of 4</p>
      <h1 className="font-serif text-4xl font-bold text-gray-900 mb-3">Screening result</h1>
      <p className="text-gray-500 mb-10">
        Based on blood_test_report.pdf. This is a screening indicator, not a diagnosis.
      </p>

      <div className="grid grid-cols-1 md:grid-cols-5 gap-6">
        {/* Left */}
        <div className="md:col-span-3 space-y-5">
          {/* Main result card */}
          <div className="card p-6">
            <p className="text-xs font-semibold tracking-widest text-gray-400 uppercase mb-2">Possible Condition</p>
            <div className="flex items-center gap-3 mb-1">
              <h2 className="font-serif text-3xl font-bold text-gray-900">Diabetes</h2>
              <span className="bg-orange-100 text-orange-600 text-xs font-semibold px-3 py-1 rounded-full">
                Elevated risk indicated
              </span>
            </div>
            <p className="text-sm text-gray-500 mb-6">Endocrine &amp; Metabolic · Diabetes model</p>

            {/* Confidence */}
            <div className="mb-5">
              <div className="flex items-center justify-between mb-2">
                <span className="text-sm font-semibold text-gray-700">Model confidence</span>
                <span className="text-sm font-bold text-gray-900">78%</span>
              </div>
              <div className="h-2.5 bg-gray-100 rounded-full">
                <div className="h-2.5 bg-[#1a5e52] rounded-full" style={{ width: '78%' }} />
              </div>
              <p className="text-xs text-gray-400 mt-1.5">
                Confidence describes the model's certainty, not the chance that you have the disease.
              </p>
            </div>

            <div className="flex gap-3 flex-wrap">
              <button onClick={() => navigate('/guidance')} className="btn-primary flex items-center gap-2">
                View health guidance
              </button>
              <button className="btn-outline flex items-center gap-2">
                <Download size={15} />
                Download report summary
              </button>
            </div>
          </div>

          {/* Feature importance */}
          <div className="card p-5">
            <h3 className="font-serif font-bold text-gray-900 mb-1">What influenced this result</h3>
            <p className="text-sm text-gray-400 mb-5">Parameters that moved the prediction most.</p>
            <div className="space-y-5">
              {featureImportance.map((f) => (
                <div key={f.label}>
                  <div className="flex items-center justify-between mb-1.5">
                    <span className="text-sm text-gray-700">{f.label}</span>
                    <span className={`text-xs font-semibold ${f.strength === 'Strong' ? 'text-orange-500' : 'text-gray-400'}`}>
                      {f.strength}
                    </span>
                  </div>
                  <div className="h-2 bg-gray-100 rounded-full">
                    <div
                      className={`h-2 rounded-full ${f.strength === 'Strong' ? 'bg-orange-400' : 'bg-gray-300'}`}
                      style={{ width: `${f.pct}%` }}
                    />
                  </div>
                </div>
              ))}
            </div>
          </div>

          {/* Warning */}
          <div className="border border-amber-300 bg-amber-50 rounded-lg p-4 flex gap-3">
            <AlertTriangle size={18} className="text-amber-500 flex-shrink-0 mt-0.5" />
            <p className="text-sm text-gray-700">
              <strong>Please see a doctor.</strong> Elevated glucose and HbA1c values should be reviewed
              by a qualified healthcare professional who can confirm or rule out a diagnosis.
            </p>
          </div>
        </div>

        {/* Right */}
        <div className="md:col-span-2 space-y-5">
          {/* Other checks */}
          <div className="card p-5">
            <h3 className="font-serif font-bold text-gray-900 mb-4">Other checks on this report</h3>
            <div className="space-y-3">
              {otherChecks.map((c) => (
                <div key={c.name} className="flex items-center justify-between py-1 border-b border-gray-50 last:border-0">
                  <span className="text-sm text-gray-700">{c.name}</span>
                  <span className={`text-xs font-semibold px-2 py-0.5 rounded ${
                    c.variant === 'normal' ? 'bg-teal-100 text-teal-700' : 'bg-gray-100 text-gray-500'
                  }`}>
                    {c.status}
                  </span>
                </div>
              ))}
            </div>
          </div>

          {/* About prediction */}
          <div className="card p-5">
            <h3 className="font-serif font-bold text-gray-900 mb-4">About this prediction</h3>
            <div className="space-y-3 text-sm">
              <div className="flex justify-between border-b border-gray-50 pb-2">
                <span className="text-gray-500">Data type</span>
                <span className="font-medium text-gray-800">Tabular</span>
              </div>
              <div className="flex justify-between border-b border-gray-50 pb-2">
                <span className="text-gray-500">Parameters used</span>
                <span className="font-medium text-gray-800">5</span>
              </div>
              <div className="flex justify-between">
                <span className="text-gray-500">Model details</span>
                <a href="#" className="text-[#1a5e52] font-medium hover:underline">View</a>
              </div>
            </div>
          </div>

          <p className="text-xs text-gray-500 leading-relaxed px-1">
            Next: food, activity and lifestyle guidance for this result, plus warning signs to watch for.
          </p>
        </div>
      </div>
    </div>
  )
}
