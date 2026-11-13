import React from 'react'
import { useNavigate, useLocation } from 'react-router-dom'
import { Home, UploadCloud, Cpu, FileText, Sparkles, Zap } from 'lucide-react'
import { MagnificationDock, DockItemData } from '@/components/ui/magnification-dock'
import { useApp } from '@/context/AppContext'

export default function WorkflowDock() {
  const navigate = useNavigate()
  const location = useLocation()
  const { setUploadedFile, setAnalysis, analysis } = useApp()

  const handleLoadSample = () => {
    const samplePayload = {
      filename: "sample_clinical_report.pdf",
      raw_text: "Fasting blood sugar: 142 mg/dL\nHbA1c: 6.9%\nTotal cholesterol: 214 mg/dL\nHemoglobin: 13.1 g/dL\nSerum creatinine: 0.9 mg/dL",
      parameters_found: 5,
      models_run: 2,
      tests: [
        { parameter: "Fasting blood sugar", value: 142.0, unit: "mg/dL", reference: "70 – 99", status: "HIGH", severity_label: "HIGH" },
        { parameter: "HbA1c", value: 6.9, unit: "%", reference: "< 5.7", status: "HIGH", severity_label: "HIGH" },
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

  const pathname = location.pathname

  const dockItems: DockItemData[] = [
    {
      icon: <Home size={19} className={pathname === '/' ? 'text-[#171e19]' : 'text-white'} />,
      label: 'Home',
      onClick: () => navigate('/'),
      active: pathname === '/',
      className: pathname === '/' ? 'bg-[#ffe17c] text-[#171e19]' : 'bg-[#272727] text-white hover:bg-[#ffe17c]/20',
    },
    {
      icon: <UploadCloud size={19} className={pathname === '/upload' ? 'text-[#171e19]' : 'text-white'} />,
      label: 'Upload Report',
      onClick: () => navigate('/upload'),
      active: pathname === '/upload',
      className: pathname === '/upload' ? 'bg-[#ffe17c] text-[#171e19]' : 'bg-[#272727] text-white hover:bg-[#ffe17c]/20',
    },
    {
      icon: <Cpu size={19} className={pathname === '/analysis' ? 'text-[#171e19]' : 'text-white'} />,
      label: 'Model Router',
      onClick: () => navigate('/analysis'),
      active: pathname === '/analysis',
      className: pathname === '/analysis' ? 'bg-[#ffe17c] text-[#171e19]' : 'bg-[#272727] text-white hover:bg-[#ffe17c]/20',
    },
    {
      icon: <FileText size={19} className={pathname === '/results' ? 'text-[#171e19]' : 'text-white'} />,
      label: analysis ? 'Predictions (Ready)' : 'Predictions',
      onClick: () => navigate('/results'),
      active: pathname === '/results',
      className: pathname === '/results' ? 'bg-[#ffe17c] text-[#171e19]' : 'bg-[#272727] text-white hover:bg-[#ffe17c]/20',
    },
    {
      icon: <Sparkles size={19} className={pathname === '/guidance' ? 'text-[#171e19]' : 'text-white'} />,
      label: 'Guidance',
      onClick: () => navigate('/guidance'),
      active: pathname === '/guidance',
      className: pathname === '/guidance' ? 'bg-[#ffe17c] text-[#171e19]' : 'bg-[#272727] text-white hover:bg-[#ffe17c]/20',
    },
    {
      icon: <Zap size={19} className="text-[#ffe17c]" />,
      label: 'Instant Sample Demo',
      onClick: handleLoadSample,
      className: 'bg-[#171e19] text-[#ffe17c] border-[#ffe17c]/40 hover:bg-[#ffe17c] hover:text-[#171e19]',
    },
  ]

  return (
    <aside
      aria-label="Screening navigation dock"
      className="fixed right-3 sm:right-6 top-1/2 -translate-y-1/2 z-40 pointer-events-none hidden sm:flex flex-col items-center"
    >
      <MagnificationDock
        items={dockItems}
        orientation="vertical"
        className="border border-white/10 shadow-[0_20px_50px_rgba(0,0,0,0.5)] backdrop-blur-xl"
        baseItemSize={44}
        magnification={66}
        distance={140}
      />
    </aside>
  )
}
