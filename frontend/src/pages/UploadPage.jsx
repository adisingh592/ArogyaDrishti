import React, { useState, useRef } from 'react'
import { useNavigate, Link } from 'react-router-dom'
import { Loader2, FileText, X } from 'lucide-react'
import { useApp } from '../context/AppContext'

export default function UploadPage() {
  const navigate = useNavigate()
  const fileInputRef = useRef(null)
  const { uploadedFile, setUploadedFile, runAnalysis, setAnalysis, loading, error } = useApp()
  const [dragging, setDragging] = useState(false)

  const handleFile = (f) => {
    if (f) setUploadedFile(f)
  }

  const handleDrop = (e) => {
    e.preventDefault()
    setDragging(false)
    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      handleFile(e.dataTransfer.files[0])
    }
  }

  const handleAnalyze = async () => {
    if (!uploadedFile) return
    try {
      await runAnalysis(uploadedFile)
      navigate('/analysis')
    } catch {
      // error surfaced in UI
    }
  }

  // Fallback demo sample report
  const handleTrySample = () => {
    const samplePayload = {
      decision: "CONSULT A DOCTOR",
      overall_severity: "ABNORMAL",
      recommended_action: "Some results are outside the normal range and suggest a metabolic condition that needs evaluation.",
      extracted_values: {
        fasting_glucose: 142.0,
        hba1c: 6.9,
        total_cholesterol: 214.0,
        hemoglobin: 13.1,
        creatinine: 0.9,
      },
      findings: [
        { parameter: "Fasting glucose", value: 142.0, unit: "mg/dL", reference: "70 – 99", status: "ABNORMAL", severity_label: "ABNORMAL" },
        { parameter: "HbA1c", value: 6.9, unit: "%", reference: "4.0 – 5.6", status: "ABNORMAL", severity_label: "ABNORMAL" },
        { parameter: "Total cholesterol", value: 214.0, unit: "mg/dL", reference: "< 200", status: "BORDERLINE", severity_label: "BORDERLINE" },
        { parameter: "Hemoglobin", value: 13.1, unit: "g/dL", reference: "12.0 – 15.5", status: "NORMAL", severity_label: "NORMAL" },
        { parameter: "Serum creatinine", value: 0.9, unit: "mg/dL", reference: "0.6 – 1.2", status: "NORMAL", severity_label: "NORMAL" },
      ],
      model_results: [
        {
          model: "diabetes",
          label: "Diabetes Risk Model",
          status: "ran",
          probability: 78.4,
          positive: true,
          features_used: "5/21",
          coverage: 23.8,
          assumptions: ["BMI (default 24.2)", "Age (default 45)"],
        },
        {
          model: "kidney_disease",
          label: "Chronic Kidney Disease Model",
          status: "ran",
          probability: 14.2,
          positive: false,
          features_used: "6/24",
          coverage: 25.0,
          assumptions: ["Age (default 45)"],
        },
      ],
      conditions: [
        { condition: "Diabetes", status: "ABNORMAL", severity: 2, evidence: ["Fasting glucose 142 mg/dL - High blood sugar", "HbA1c 6.9% - High glycemic index"] },
        { condition: "Dyslipidemia", status: "BORDERLINE", severity: 1, evidence: ["Total cholesterol 214 mg/dL - Elevated"] },
      ],
      guidance: [
        {
          for: "Diabetes",
          food_prefer: ["Vegetables and leafy greens", "Whole grains such as millets, oats and brown rice", "Lentils, beans and chickpeas", "Nuts, seeds and lean protein"],
          food_limit: ["Sugary drinks and sweets", "Refined flour and white bread", "Deep-fried snacks"],
          exercise: ["Brisk walking 30 mins daily", "Light strength training twice a week"],
          lifestyle: ["Sleep 7 to 9 hours nightly", "Stress reduction routines", "Routine blood monitoring"],
          warning_signs: ["Constant thirst or frequent urination", "Unexplained weight loss or tiredness", "Blurred vision"],
          when_to_seek_help: ["Confusion or dizziness", "Persistent vomiting or fruity-smelling breath"],
        }
      ]
    }
    setUploadedFile({ name: "sample_clinical_report.pdf", size: 142 * 1024 })
    setAnalysis(samplePayload)
    navigate('/analysis')
  }

  return (
    <div className="py-16 px-5 max-w-[1240px] mx-auto">
      <span className="badge-tag">Step 1 of 3</span>
      
      <h1 className="disp text-[clamp(3.4rem,9vw,6.5rem)] mt-6">
        Upload your <span className="hl">report</span>
      </h1>
      <p className="mt-4 text-lg opacity-70 max-w-xl">
        Add a PDF or an image of your lab report. ArogyaDrishti reads the clinical values automatically.
      </p>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mt-12">
        {/* Dropzone panel */}
        <div className="bg-white border border-[rgba(23,30,25,0.1)] rounded-2xl p-8 flex flex-col justify-between shadow-sm">
          <div>
            <div
              onDragOver={(e) => { e.preventDefault(); setDragging(true) }}
              onDragLeave={() => setDragging(false)}
              onDrop={handleDrop}
              onClick={() => fileInputRef.current?.click()}
              className={`flex flex-col items-center justify-center text-center min-h-[240px] p-8 border-2 border-dashed rounded-xl cursor-pointer transition-all ${
                dragging
                  ? 'border-[#171e19] bg-[#ffe17c]/20'
                  : 'border-[rgba(23,30,25,0.25)] hover:border-[#171e19] hover:bg-[#ffe17c]/10'
              }`}
            >
              <FileText size={40} className="mb-3 text-[#171e19] opacity-75" />
              <b className="disp text-2xl font-normal">Drop your report here</b>
              <span className="text-sm opacity-70 mt-1">or click to choose a PDF or image (JPG/PNG)</span>
              <input
                ref={fileInputRef}
                type="file"
                accept=".pdf,image/*,.txt"
                className="hidden"
                onChange={(e) => handleFile(e.target.files?.[0])}
              />
            </div>

            {/* Picked file preview */}
            {uploadedFile && (
              <div className="flex items-center justify-between gap-3 mt-4 p-3 border border-[rgba(23,30,25,0.15)] rounded-lg bg-[#f8f9fa] text-sm">
                <span className="font-medium truncate">{uploadedFile.name}</span>
                <button
                  type="button"
                  onClick={() => setUploadedFile(null)}
                  className="font-bold text-xs underline cursor-pointer text-[#171e19]"
                >
                  Remove
                </button>
              </div>
            )}

            {error && (
              <div className="mt-4 p-3 bg-red-50 border border-red-200 text-red-700 text-xs rounded-lg">
                {error}
              </div>
            )}
          </div>

          <div className="flex flex-wrap gap-3 mt-8 items-center">
            {uploadedFile ? (
              <button
                type="button"
                onClick={handleAnalyze}
                disabled={loading}
                className="btn-y flex items-center gap-2"
              >
                {loading && <Loader2 size={18} className="animate-spin" />}
                {loading ? 'Analyzing…' : 'Analyze report'}
              </button>
            ) : (
              <button
                type="button"
                onClick={handleTrySample}
                className="btn-y"
              >
                Try with a sample report
              </button>
            )}
            <Link to="/" className="btn-ghost">
              Back to home
            </Link>
          </div>
          <p className="mt-4 text-xs opacity-60">
            Real-time multi-disease extraction, confidence evaluation &amp; guideline matching.
          </p>
        </div>

        {/* Right Info Panel */}
        <div className="bg-[#171e19] text-white border border-[rgba(183,198,194,0.1)] rounded-2xl p-8 flex flex-col justify-between">
          <div>
            <h3 className="disp text-3xl mb-4">Before you upload</h3>
            <ul className="space-y-3 text-sm text-[#b7c6c2]">
              <li className="flex gap-3 items-center border-t border-[rgba(183,198,194,0.15)] pt-3">
                <span className="w-4 h-4 rounded-full bg-[#ffe17c] inline-block flex-shrink-0" />
                <span>A PDF or image of your complete medical lab report</span>
              </li>
              <li className="flex gap-3 items-center border-t border-[rgba(183,198,194,0.15)] pt-3">
                <span className="w-4 h-4 rounded-full bg-[#ffe17c] inline-block flex-shrink-0" />
                <span>A clear, flat, well-lit photo or digital document reads best</span>
              </li>
              <li className="flex gap-3 items-center border-t border-[rgba(183,198,194,0.15)] pt-3">
                <span className="w-4 h-4 rounded-full bg-[#ffe17c] inline-block flex-shrink-0" />
                <span>No manual entry of dozens of lab values required</span>
              </li>
            </ul>
          </div>
          <p className="mt-8 text-xs text-[#b7c6c2]/70 leading-relaxed">
            ArogyaDrishti is an academic AI screening and educational tool. Predictions are not a confirmed medical diagnosis. Always share your results with a licensed doctor.
          </p>
        </div>
      </div>
    </div>
  )
}
