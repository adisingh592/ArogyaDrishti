import { Link } from 'react-router-dom'
import { CheckCircle, AlertTriangle } from 'lucide-react'

const labRows = [
  { name: 'Fasting glucose', value: '142 mg/dL', status: 'HIGH' },
  { name: 'HbA1c', value: '6.9 %', status: 'HIGH' },
  { name: 'Total cholesterol', value: '214 mg/dL', status: 'HIGH' },
  { name: 'Hemoglobin', value: '13.1 g/dL', status: 'NORMAL' },
  { name: 'Serum creatinine', value: '0.9 mg/dL', status: 'NORMAL' },
]

const steps = [
  { n: '01', title: 'Upload', desc: 'Add a PDF or photo of your medical report.' },
  { n: '02', title: 'Extract', desc: 'PDF parsing and OCR pull out each parameter, value and unit.' },
  { n: '03', title: 'Screen', desc: 'The report is routed to the matching disease-specific ML or DL model.' },
  { n: '04', title: 'Guide', desc: 'Food, activity and lifestyle advice from a structured knowledge base.' },
]

const categories = [
  { name: 'Neurological', desc: "Parkinson's, Alzheimer's, Stroke" },
  { name: 'Cardiovascular', desc: 'Heart disease, Heart failure' },
  { name: 'Endocrine & Metabolic', desc: 'Diabetes, Obesity, Thyroid' },
  { name: 'Hematological', desc: 'Anemia, Leukemia' },
  { name: 'Renal', desc: 'Chronic kidney disease' },
  { name: 'Hepatic', desc: 'Liver disease' },
  { name: 'Respiratory', desc: 'Pneumonia, Tuberculosis, Asthma, COPD' },
  { name: 'Oncology', desc: 'Breast, Lung and Skin cancer' },
  { name: 'Infectious', desc: 'Malaria, Hepatitis' },
  { name: "Women's Health", desc: 'PCOS, Maternal health risk' },
]

const features = [
  { title: 'Many diseases, one platform', desc: 'Disease-specific models for tabular data, medical images, EEG and time-series sit behind a single upload.' },
  { title: 'Reports, not forms', desc: 'You provide the report you already have. The system finds the parameters it needs.' },
  { title: 'Guidance after the result', desc: 'Nutrition, activity, precautions and warning signs follow every prediction.' },
]

export default function HomePage() {
  return (
    <div>
      {/* Hero */}
      <section className="max-w-6xl mx-auto px-6 py-16 grid grid-cols-1 md:grid-cols-2 gap-12 items-center">
        {/* Left */}
        <div>
          <p className="text-xs font-semibold tracking-widest text-[#1a5e52] uppercase mb-4">
            AI-Assisted Report Screening
          </p>
          <h1 className="font-serif text-4xl md:text-5xl font-bold text-gray-900 leading-tight mb-6">
            Bring your medical report. Get a clearer picture.
          </h1>
          <p className="text-gray-500 text-base mb-8 leading-relaxed">
            Upload a lab report and ArogyaDrishti reads the values, runs the matching disease-screening model,
            and explains what to eat, how to move and when to see a doctor.
          </p>
          <div className="flex items-center gap-3 flex-wrap">
            <Link to="/upload" className="btn-primary text-sm">
              Upload a medical report
            </Link>
            <Link to="/analysis" className="btn-outline text-sm">
              See how it works
            </Link>
          </div>
          <p className="text-xs text-gray-400 mt-3">
            PDF or image of your report. No manual entry of dozens of values.
          </p>
        </div>

        {/* Right — Sample Lab Card */}
        <div className="card p-5 shadow-md">
          <div className="flex items-center justify-between mb-4 pb-3 border-b border-gray-100">
            <span className="text-xs font-semibold tracking-widest text-gray-400 uppercase">Laboratory Report</span>
            <span className="text-xs text-gray-400 uppercase tracking-wide">Sample</span>
          </div>
          <div className="space-y-2">
            {labRows.map((row) => (
              <div key={row.name} className="flex items-center justify-between py-1.5">
                <span className="text-sm text-gray-700">{row.name}</span>
                <div className="flex items-center gap-3">
                  <span className="text-sm text-gray-600 font-medium">{row.value}</span>
                  <span className={row.status === 'HIGH' ? 'badge-high' : 'badge-normal'}>
                    {row.status}
                  </span>
                </div>
              </div>
            ))}
          </div>
          <div className="mt-4 pt-3 border-t border-gray-100 flex items-center gap-2 bg-teal-50 rounded-md px-3 py-2">
            <CheckCircle size={15} className="text-[#1a5e52] flex-shrink-0" />
            <span className="text-xs text-[#1a5e52] font-medium">5 parameters extracted. Routed to the diabetes model.</span>
          </div>
        </div>
      </section>

      {/* 4 Steps */}
      <section className="max-w-6xl mx-auto px-6 py-16 border-t border-gray-200">
        <h2 className="font-serif text-2xl font-bold text-gray-900 mb-12">
          From report to guidance in four steps
        </h2>
        <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-4 gap-8">
          {steps.map((s) => (
            <div key={s.n}>
              <div className="border-t-2 border-gray-300 mb-4" />
              <p className="text-xs font-semibold text-gray-400 mb-2">{s.n}</p>
              <h3 className="font-serif font-bold text-lg text-gray-900 mb-2">{s.title}</h3>
              <p className="text-sm text-gray-500 leading-relaxed">{s.desc}</p>
            </div>
          ))}
        </div>
      </section>

      {/* Categories */}
      <section className="max-w-6xl mx-auto px-6 py-16 border-t border-gray-200">
        <div className="flex items-center justify-between mb-8">
          <h2 className="font-serif text-2xl font-bold text-gray-900">Ten medical categories, one place</h2>
          <a href="#" className="text-sm text-[#1a5e52] underline underline-offset-2 hover:text-[#154a40]">
            Dataset and model information
          </a>
        </div>
        <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-4 gap-4">
          {categories.map((cat) => (
            <div key={cat.name} className="card p-4 hover:shadow-md transition-shadow cursor-pointer">
              <h3 className="font-semibold text-gray-900 text-sm mb-1">{cat.name}</h3>
              <p className="text-xs text-gray-500">{cat.desc}</p>
            </div>
          ))}
        </div>
      </section>

      {/* Feature strip */}
      <section className="bg-[#1a5e52] py-16">
        <div className="max-w-6xl mx-auto px-6 grid grid-cols-1 md:grid-cols-3 gap-10">
          {features.map((f) => (
            <div key={f.title}>
              <h3 className="font-serif text-lg font-bold text-white mb-3">{f.title}</h3>
              <p className="text-teal-100 text-sm leading-relaxed">{f.desc}</p>
            </div>
          ))}
        </div>
      </section>

      {/* Disclaimer */}
      <section className="max-w-6xl mx-auto px-6 py-10">
        <div className="border border-amber-300 bg-amber-50 rounded-lg p-5 flex gap-3">
          <AlertTriangle size={18} className="text-amber-500 flex-shrink-0 mt-0.5" />
          <p className="text-sm text-gray-700">
            <strong>Important.</strong> ArogyaDrishti is an academic AI screening and educational project.
            Its predictions are not confirmed diagnoses. Consult a qualified healthcare professional
            for diagnosis and treatment.
          </p>
        </div>
      </section>
    </div>
  )
}
