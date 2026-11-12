import { useState, useRef } from 'react'
import { Link, useNavigate } from 'react-router-dom'
import { FileText, Upload, X, CheckCircle } from 'lucide-react'

const reportTypes = ['Auto-detect', 'Blood test', 'Urine / kidney', 'Medical image', 'EEG / signal']

const nextSteps = [
  { n: 1, title: 'Report processing', desc: 'Text is read from the PDF or by OCR.' },
  { n: 2, title: 'Extract medical data', desc: 'Parameters, values and units are identified.' },
  { n: 3, title: 'Identify relevant disease', desc: 'The report is routed to the matching model.' },
  { n: 4, title: 'Prediction and guidance', desc: 'You get a result with confidence and lifestyle advice.' },
]


export default function UploadPage() {
  const navigate = useNavigate()
  const fileInputRef = useRef(null)
  const [file, setFile] = useState(null)
  const [dragging, setDragging] = useState(false)
  const [reportType, setReportType] = useState('Auto-detect')

  const handleFile = (f) => {
    if (f) setFile(f)
  }

  const onDrop = (e) => {
    e.preventDefault()
    setDragging(false)
    const f = e.dataTransfer.files[0]
    if (f) handleFile(f)
  }

  const formatSize = (bytes) => {
    if (bytes < 1024 * 1024) return `${(bytes / 1024).toFixed(0)} KB`
    return `${(bytes / (1024 * 1024)).toFixed(1)} MB`
  }

  return (
    <div className="max-w-6xl mx-auto px-6 py-12">
      <p className="step-label">Step 1 of 4</p>
      <h1 className="font-serif text-4xl font-bold text-gray-900 mb-3">Upload your medical report</h1>
      <p className="text-gray-500 mb-10 max-w-xl">
        Add the report you already have. SehatSetu reads the values and decides which disease-screening model fits.
      </p>

      <div className="grid grid-cols-1 md:grid-cols-5 gap-8">
        {/* Left col */}
        <div className="md:col-span-3 space-y-5">
          {/* Drop zone */}
          <div
            onDragOver={(e) => { e.preventDefault(); setDragging(true) }}
            onDragLeave={() => setDragging(false)}
            onDrop={onDrop}
            onClick={() => !file && fileInputRef.current.click()}
            className={`border-2 border-dashed rounded-xl p-12 text-center cursor-pointer transition-colors ${
              dragging ? 'border-[#1a5e52] bg-[#1a5e52]/5' : 'border-gray-300 hover:border-[#1a5e52] bg-white'
            }`}
          >
            <FileText size={40} className="text-[#1a5e52] mx-auto mb-4" />
            <p className="font-semibold text-gray-800 text-lg mb-1">Drag your report here</p>
            <p className="text-sm text-gray-400 mb-5">PDF, JPG or PNG</p>
            <button
              type="button"
              onClick={(e) => { e.stopPropagation(); fileInputRef.current.click() }}
              className="btn-primary"
            >
              Choose a file
            </button>
            <input
              ref={fileInputRef}
              type="file"
              accept=".pdf,.jpg,.jpeg,.png"
              className="hidden"
              onChange={(e) => handleFile(e.target.files[0])}
            />
          </div>

          {/* File preview */}
          {file && (
            <div className="card p-4">
              <div className="flex items-center gap-3 mb-3">
                <div className="w-10 h-12 bg-gray-100 border border-gray-300 rounded flex items-center justify-center">
                  <span className="text-[9px] font-bold text-gray-500 uppercase">
                    {file.name.split('.').pop()}
                  </span>
                </div>
                <div className="flex-1 min-w-0">
                  <p className="text-sm font-semibold text-gray-800 truncate">{file.name}</p>
                  <p className="text-xs text-gray-400">{formatSize(file.size)} · Uploaded</p>
                </div>
                <span className="text-xs font-semibold text-[#1a5e52] bg-teal-50 px-2 py-1 rounded flex items-center gap-1">
                  <CheckCircle size={12} /> READY TO ANALYZE
                </span>
                <button onClick={() => setFile(null)} className="text-gray-400 hover:text-gray-600">
                  <X size={16} />
                </button>
              </div>
              <div className="h-1.5 bg-gray-100 rounded-full">
                <div className="h-1.5 bg-[#1a5e52] rounded-full w-full transition-all" />
              </div>
            </div>
          )}

          {/* Report type */}
          <div>
            <p className="text-sm font-semibold text-gray-700 mb-3">Report type</p>
            <div className="flex flex-wrap gap-2">
              {reportTypes.map((t) => (
                <button
                  key={t}
                  onClick={() => setReportType(t)}
                  className={`px-4 py-1.5 rounded-full text-sm border transition-colors ${
                    reportType === t
                      ? 'bg-[#1a5e52] text-white border-[#1a5e52]'
                      : 'bg-white text-gray-600 border-gray-300 hover:border-[#1a5e52]'
                  }`}
                >
                  {t}
                </button>
              ))}
            </div>
          </div>

          {/* Actions */}
          <div className="flex items-center gap-3 pt-2">
            <button
              onClick={() => navigate('/analysis')}
              className="btn-primary"
            >
              Analyze report
            </button>
            <button onClick={() => { setFile(null) }} className="text-sm text-gray-500 hover:text-gray-700">
              Cancel
            </button>
          </div>
        </div>

        {/* Right col */}
        <div className="md:col-span-2 space-y-5">
          <div className="card p-5">
            <h3 className="font-serif font-bold text-gray-900 mb-5">What happens next</h3>
            <div className="space-y-5">
              {nextSteps.map((s) => (
                <div key={s.n} className="flex gap-3">
                  <div className="w-7 h-7 rounded-full bg-[#1a5e52] text-white text-xs font-bold flex items-center justify-center flex-shrink-0">
                    {s.n}
                  </div>
                  <div>
                    <p className="text-sm font-semibold text-gray-800">{s.title}</p>
                    <p className="text-xs text-gray-500 mt-0.5">{s.desc}</p>
                  </div>
                </div>
              ))}
            </div>
          </div>

          <div className="card p-5">
            <p className="text-sm font-semibold text-gray-700 mb-3">For the best reading</p>
            <ul className="space-y-2 text-sm text-gray-500">
              <li className="flex gap-2"><span className="text-[#1a5e52]">•</span>Use the original PDF when you can.</li>
              <li className="flex gap-2"><span className="text-[#1a5e52]">•</span>Photos should be flat, bright and in focus.</li>
              <li className="flex gap-2"><span className="text-[#1a5e52]">•</span>Keep reference ranges visible in the report.</li>
            </ul>
          </div>
        </div>
      </div>
    </div>
  )
}
