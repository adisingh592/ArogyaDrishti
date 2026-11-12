import { Link, useNavigate } from 'react-router-dom'
import { ArrowRight } from 'lucide-react'

const extractedParams = [
  { name: 'Fasting glucose', value: '142 mg/dL', reference: '70 – 99', status: 'HIGH' },
  { name: 'HbA1c', value: '6.9 %', reference: '4.0 – 5.6', status: 'HIGH' },
  { name: 'Total cholesterol', value: '214 mg/dL', reference: '< 200', status: 'HIGH' },
  { name: 'Hemoglobin', value: '13.1 g/dL', reference: '12.0 – 15.5', status: 'NORMAL' },
  { name: 'Serum creatinine', value: '0.9 mg/dL', reference: '0.6 – 1.2', status: 'NORMAL' },
]

const docRows = [
  { label: 'Fasting glucose', value: '142 mg/dL', isHigh: true },
  { label: 'HbA1c', value: '6.9 %', isHigh: true },
  { label: 'Total cholesterol', value: '214 mg/dL', isHigh: true },
  { label: 'Hemoglobin', value: '13.1 g/dL', isHigh: false },
  { label: 'Serum creatinine', value: '0.9 mg/dL', isHigh: false },
]

export default function AnalysisPage() {
  const navigate = useNavigate()

  return (
    <div className="max-w-6xl mx-auto px-6 py-12">
      <p className="step-label">Step 2 of 4</p>
      <h1 className="font-serif text-4xl font-bold text-gray-900 mb-3">What we found in your report</h1>
      <p className="text-gray-500 mb-10">
        Check the extracted values before screening. Anything misread can be corrected.
      </p>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {/* Document preview */}
        <div className="card p-5">
          <div className="flex items-center justify-between mb-4 pb-2 border-b border-gray-100">
            <span className="text-sm font-semibold text-gray-700">blood_test_report.pdf</span>
            <span className="text-xs text-gray-400">PAGE 1 / 2</span>
          </div>
          {/* Fake doc lines */}
          <div className="space-y-1 mb-3">
            <div className="h-2 bg-gray-200 rounded w-4/5" />
            <div className="h-2 bg-gray-200 rounded w-3/5" />
          </div>
          <div className="space-y-1.5">
            {docRows.map((r) => (
              <div
                key={r.label}
                className={`flex justify-between items-center px-3 py-2 rounded text-sm ${
                  r.isHigh ? 'bg-orange-50 border border-orange-200' : 'bg-teal-50 border border-teal-100'
                }`}
              >
                <span className="text-gray-700">{r.label}</span>
                <span className="font-medium text-gray-800">{r.value}</span>
              </div>
            ))}
          </div>
          <div className="mt-3 space-y-1">
            <div className="h-2 bg-gray-200 rounded w-full" />
            <div className="h-2 bg-gray-200 rounded w-2/3" />
          </div>
        </div>

        {/* Right panel */}
        <div className="space-y-5">
          {/* Extracted parameters table */}
          <div className="card p-5">
            <div className="flex items-center justify-between mb-4">
              <h3 className="font-serif font-bold text-gray-900">Extracted parameters</h3>
              <span className="text-xs text-gray-400">5 found · 0 unreadable</span>
            </div>
            <table className="w-full text-sm">
              <thead>
                <tr className="border-b border-gray-100">
                  <th className="text-left text-xs text-gray-400 font-semibold pb-2 uppercase tracking-wide">Parameter</th>
                  <th className="text-left text-xs text-gray-400 font-semibold pb-2 uppercase tracking-wide">Value</th>
                  <th className="text-left text-xs text-gray-400 font-semibold pb-2 uppercase tracking-wide">Reference</th>
                  <th className="text-left text-xs text-gray-400 font-semibold pb-2 uppercase tracking-wide">Status</th>
                </tr>
              </thead>
              <tbody>
                {extractedParams.map((p) => (
                  <tr key={p.name} className="border-b border-gray-50 last:border-0">
                    <td className="py-2.5 text-gray-700">{p.name}</td>
                    <td className="py-2.5 text-gray-800 font-medium">{p.value}</td>
                    <td className="py-2.5 text-gray-500">{p.reference}</td>
                    <td className="py-2.5">
                      <span className={p.status === 'HIGH' ? 'badge-high' : 'badge-normal'}>
                        {p.status}
                      </span>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>

          {/* Disease routing */}
          <div className="card p-5">
            <p className="text-xs font-semibold tracking-widest text-[#1a5e52] uppercase mb-4">Disease Routing</p>
            <div className="flex items-center gap-2 flex-wrap mb-4">
              <span className="border border-gray-300 rounded-md px-3 py-1.5 text-sm text-gray-700">Blood test report</span>
              <ArrowRight size={16} className="text-gray-400 flex-shrink-0" />
              <span className="border border-gray-300 rounded-md px-3 py-1.5 text-sm text-gray-700">Endocrine &amp; Metabolic</span>
              <ArrowRight size={16} className="text-gray-400 flex-shrink-0" />
              <button className="btn-primary text-sm py-1.5">Diabetes model (tabular)</button>
            </div>
            <p className="text-xs text-gray-500 leading-relaxed">
              The report contains glucose and HbA1c values, so it was routed to the diabetes screening
              model. Cholesterol, hemoglobin and creatinine are kept for context.
            </p>
          </div>
        </div>
      </div>

      {/* Actions */}
      <div className="flex items-center gap-3 mt-8">
        <button onClick={() => navigate('/results')} className="btn-primary">
          Run screening
        </button>
        <button onClick={() => navigate('/upload')} className="btn-outline">
          Upload a different report
        </button>
      </div>
    </div>
  )
}
