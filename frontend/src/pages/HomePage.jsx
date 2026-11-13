import React, { useState } from 'react'
import { Link } from 'react-router-dom'
import { Check, X } from 'lucide-react'

export default function HomePage() {
  const [openFaq, setOpenFaq] = useState(0)

  const faqs = [
    {
      q: 'Is this a diagnosis?',
      a: 'No. ArogyaDrishti is an academic AI screening and educational tool. Predictions are not a confirmed medical diagnosis, so please talk to a doctor about any result.',
    },
    {
      q: 'What can I upload?',
      a: 'A PDF or an image of your lab report. ArogyaDrishti parses and extracts test values automatically, so you do not have to type them in.',
    },
    {
      q: 'What happens after my report is read?',
      a: 'The values go to our Meta-Classifier which selects matching disease-screening models. You then see the results along with personalized guidance on food, activity and precautions.',
    },
  ]

  return (
    <div>
      {/* ── Hero Section with Grid Background ── */}
      <section className="bg-white grid-bg text-center py-24 px-5">
        <div className="max-w-[1240px] mx-auto">
          <span className="badge-tag">AI-assisted report screening</span>
          
          <h1 className="disp text-[clamp(3.6rem,11vw,8.5rem)] mt-8 mx-auto max-w-[1100px] leading-[0.9]">
            Your lab report, finally <span className="hl">explained</span>
          </h1>
          
          <p className="text-lg opacity-75 max-w-[36rem] mx-auto mt-7 leading-relaxed font-normal">
            Upload a PDF or photo. ArogyaDrishti reads the values, routes to matching screening models,
            and provides plain-language guidance on food, movement, and medical consults.
          </p>

          {/* Quick Upload CTA Form */}
          <div className="flex flex-col sm:flex-row gap-3 max-w-[640px] mx-auto mt-10">
            <Link
              to="/upload"
              className="flex-1 flex items-center px-6 border border-[rgba(23,30,25,0.2)] rounded-lg bg-white text-left text-sm opacity-90 min-h-[60px] hover:border-[#171e19] transition-colors"
            >
              Choose a PDF or image of your report
            </Link>
            <Link to="/upload" className="btn-y">
              Upload report
            </Link>
          </div>
          <p className="mt-4 text-xs opacity-60">
            No manual entry needed. Real-time OCR &amp; Multi-model classification.
          </p>

          {/* Mock Interactive Report Window */}
          <div className="max-w-[1000px] mx-auto mt-16 border border-[rgba(23,30,25,0.1)] bg-white shadow-2xl rounded-xl overflow-hidden text-left">
            <div className="flex items-center gap-2 px-4 py-3 border-b border-[rgba(23,30,25,0.1)] bg-[#f8f9fa]">
              <i className="w-2.5 h-2.5 rounded-full bg-[#b7c6c2]" />
              <i className="w-2.5 h-2.5 rounded-full bg-[#b7c6c2]" />
              <i className="w-2.5 h-2.5 rounded-full bg-[#b7c6c2]" />
              <b className="mx-auto text-xs font-medium opacity-60 pr-10">arogyadrishti / sample-report.pdf</b>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-[180px_1fr_220px] min-h-[300px]">
              {/* Left pane */}
              <div className="border-r border-[rgba(23,30,25,0.1)] p-5 text-xs space-y-1 hidden md:block">
                <p className="bg-[#ffe17c] font-bold p-2 rounded">sample-report.pdf</p>
                <p className="p-2 opacity-70">Values read</p>
                <p className="p-2 opacity-70">Model chosen</p>
                <p className="p-2 opacity-70">Guidance</p>
              </div>

              {/* Middle preview card */}
              <div className="bg-[#f8f9fa] p-6 relative flex items-center justify-center">
                <div className="bg-white text-[#171e19] w-full max-w-[340px] p-5 rounded-lg shadow-md border border-gray-100">
                  <div className="flex justify-between items-center pb-2 border-b border-gray-100 text-sm">
                    <span>Fasting glucose</span>
                    <span className="font-mono text-xs flex items-center gap-1.5">
                      142 mg/dL <span className="chip-hi">HIGH</span>
                    </span>
                  </div>
                  <div className="flex justify-between items-center py-2 border-b border-gray-100 text-sm">
                    <span>HbA1c</span>
                    <span className="font-mono text-xs flex items-center gap-1.5">
                      6.9 % <span className="chip-hi">HIGH</span>
                    </span>
                  </div>
                  <div className="flex justify-between items-center pt-2 text-sm">
                    <span>Hemoglobin</span>
                    <span className="font-mono text-xs flex items-center gap-1.5">
                      13.1 g/dL <span className="chip-ok">NORMAL</span>
                    </span>
                  </div>
                </div>

                <div className="absolute right-[8%] bottom-[12%] flex gap-1 items-start">
                  <svg width="22" height="22" viewBox="0 0 24 24" fill="#171e19" stroke="#fff" strokeWidth="1.5">
                    <path d="M4 3l16 7-7 2-2 7z" />
                  </svg>
                  <span className="bg-[#171e19] text-white text-[11px] font-bold px-2 py-0.5 rounded mt-3">
                    Diabetes model
                  </span>
                </div>
              </div>

              {/* Right pane */}
              <div className="border-l border-[rgba(23,30,25,0.1)] p-5 text-xs hidden md:block">
                <h4 className="disp text-lg mb-3">Flag</h4>
                <p className="opacity-75">Above range</p>
                <div className="flex items-center gap-2 mt-3 font-mono text-xs">
                  <i className="w-5 h-5 rounded bg-[#ffe17c] border border-[rgba(23,30,25,0.1)]" />
                  #FFE17C
                </div>
                <div className="flex gap-1 mt-3">
                  <i className="w-5 h-4 border border-[rgba(23,30,25,0.1)] rounded bg-gradient-to-r from-[#171e19] to-[#171e19] bg-no-repeat bg-center" />
                  <i className="w-5 h-4 border border-[rgba(23,30,25,0.1)] rounded" />
                  <i className="w-5 h-4 border border-[rgba(23,30,25,0.1)] rounded" />
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* ── Test Parameters Strip ── */}
      <section className="border-y border-[rgba(23,30,25,0.1)] py-5 bg-[#f8f9fa]">
        <div className="max-w-[1240px] mx-auto px-5 flex flex-wrap gap-x-10 gap-y-3 justify-center items-center text-xs font-bold uppercase tracking-[0.16em]">
          <span className="opacity-50">Reads</span>
          <span>Glucose</span>
          <span>HbA1c</span>
          <span>Cholesterol</span>
          <span>Hemoglobin</span>
          <span>Creatinine</span>
          <span>TSH</span>
          <span>ALT / AST</span>
        </div>
      </section>

      {/* ── Split Comparison: The Old Way vs The ArogyaDrishti Way ── */}
      <section className="grid grid-cols-1 md:grid-cols-2">
        <div className="bg-[#171e19] text-white p-12 lg:p-24 flex flex-col justify-center">
          <h2 className="disp text-[clamp(2.6rem,5vw,4.5rem)] text-[#b7c6c2] mb-6">
            The old way
          </h2>
          <ul className="space-y-4 text-base md:text-lg text-[#b7c6c2]">
            <li className="flex gap-3.5 items-start">
              <span className="p-1 rounded bg-red-500/20 text-red-400 mt-1">
                <X size={16} strokeWidth={3} />
              </span>
              <span>Retype dozens of laboratory values by hand</span>
            </li>
            <li className="flex gap-3.5 items-start">
              <span className="p-1 rounded bg-red-500/20 text-red-400 mt-1">
                <X size={16} strokeWidth={3} />
              </span>
              <span>Search medical terms online and guess what they mean</span>
            </li>
            <li className="flex gap-3.5 items-start">
              <span className="p-1 rounded bg-red-500/20 text-red-400 mt-1">
                <X size={16} strokeWidth={3} />
              </span>
              <span>Wait days to learn if an elevated number matters</span>
            </li>
          </ul>
        </div>

        <div className="bg-[#272727] text-white p-12 lg:p-24 flex flex-col justify-center border-l-0 md:border-l-4 border-[#ffe17c]">
          <h2 className="disp text-[clamp(2.6rem,5vw,4.5rem)] mb-6">
            The <span className="text-[#ffe17c]">ArogyaDrishti</span> way
          </h2>
          <ul className="space-y-4 text-base md:text-lg">
            <li className="flex gap-3.5 items-start">
              <span className="p-1 rounded bg-[#ffe17c]/20 text-[#ffe17c] mt-1">
                <Check size={16} strokeWidth={3} />
              </span>
              <span>Upload the PDF or photo as it is</span>
            </li>
            <li className="flex gap-3.5 items-start">
              <span className="p-1 rounded bg-[#ffe17c]/20 text-[#ffe17c] mt-1">
                <Check size={16} strokeWidth={3} />
              </span>
              <span>See each value flagged high, borderline, or normal</span>
            </li>
            <li className="flex gap-3.5 items-start">
              <span className="p-1 rounded bg-[#ffe17c]/20 text-[#ffe17c] mt-1">
                <Check size={16} strokeWidth={3} />
              </span>
              <span>Get structured food, movement, and medical guidance</span>
            </li>
          </ul>
        </div>
      </section>

      {/* ── Bento Grid: One Bridge, Four Jobs ── */}
      <section className="py-24 px-5">
        <div className="max-w-[1240px] mx-auto">
          <div className="max-w-[720px] mb-14">
            <h2 className="disp text-[clamp(2.8rem,6vw,5rem)]">
              One bridge, <span className="hl">four</span> jobs
            </h2>
            <p className="mt-5 text-lg opacity-70">
              Setu means bridge. ArogyaDrishti connects the raw clinical measurements on your report to structured actionable health advice.
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-5">
            {/* Bento Card 1 (Span 2) */}
            <div className="md:col-span-2 p-8 border border-[rgba(23,30,25,0.1)] rounded-2xl bg-[#f8f9fa] flex flex-col justify-between hover:-translate-y-1 transition-all">
              <div>
                <h3 className="disp text-3xl">Reads your report</h3>
                <p className="mt-2 text-sm opacity-70 max-w-sm">PDF or photo. Parameters, units and reference ranges extracted automatically.</p>
              </div>
              <div className="mt-8 space-y-2">
                <div className="flex justify-between items-center p-3 bg-white text-[#171e19] rounded-lg text-sm border border-gray-100">
                  <span>Fasting glucose</span>
                  <b className="font-mono text-xs">142 mg/dL</b>
                </div>
                <div className="flex justify-between items-center p-3 bg-white text-[#171e19] rounded-lg text-sm border border-gray-100">
                  <span>Total cholesterol</span>
                  <b className="font-mono text-xs">214 mg/dL</b>
                </div>
              </div>
            </div>

            {/* Bento Card 2 */}
            <div className="p-8 border border-[rgba(183,198,194,0.1)] rounded-2xl bg-[#171e19] text-white flex flex-col justify-between hover:-translate-y-1 transition-all">
              <div>
                <h3 className="disp text-3xl">Picks the model</h3>
                <p className="mt-2 text-sm opacity-70">Meta-classifier selects matching disease-screening models.</p>
              </div>
              <div className="mt-8 space-y-2">
                <div className="h-3.5 rounded-full bg-[#ffe17c] w-3/4 animate-pulse-soft" />
                <div className="h-3.5 rounded-full bg-[#b7c6c2]/20 w-full animate-pulse-soft" />
                <div className="h-3.5 rounded-full bg-[#b7c6c2]/20 w-1/2 animate-pulse-soft" />
              </div>
            </div>

            {/* Bento Card 3 */}
            <div className="p-8 border border-[rgba(23,30,25,0.1)] rounded-2xl bg-[#f8f9fa] flex flex-col justify-between hover:-translate-y-1 transition-all">
              <div>
                <h3 className="disp text-3xl">Plain guidance</h3>
                <p className="mt-2 text-sm opacity-70">Written to be understood, not decoded.</p>
              </div>
              <div className="mt-8 flex flex-wrap gap-2">
                <span className="inline-block px-3 py-1.5 rounded-full bg-white text-xs font-bold border border-[rgba(23,30,25,0.1)]">What to eat</span>
                <span className="inline-block px-3 py-1.5 rounded-full bg-white text-xs font-bold border border-[rgba(23,30,25,0.1)]">How to move</span>
                <span className="inline-block px-3 py-1.5 rounded-full bg-white text-xs font-bold border border-[rgba(23,30,25,0.1)]">When to see doctor</span>
              </div>
            </div>

            {/* Bento Card 4 (Span 2) */}
            <div className="md:col-span-2 p-8 border border-[rgba(183,198,194,0.1)] rounded-2xl bg-[#171e19] text-white flex flex-col justify-between hover:-translate-y-1 transition-all">
              <div>
                <h3 className="disp text-3xl">Flags every value</h3>
                <p className="mt-2 text-sm opacity-70">Above range or in range, clearly identified with clinical rules.</p>
              </div>
              <div className="mt-8 bg-[#0c110e] border border-[rgba(183,198,194,0.15)] rounded-lg p-4 font-mono text-xs text-[#b7c6c2] leading-relaxed">
                <div>glucose &nbsp;&nbsp;142 mg/dL &nbsp;<span className="text-[#ffe17c] font-bold">HIGH</span></div>
                <div>hba1c &nbsp;&nbsp;&nbsp;&nbsp;6.9 % &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span className="text-[#ffe17c] font-bold">HIGH</span></div>
                <div>hemoglobin 13.1 g/dL &nbsp;normal</div>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* ── How It Works (Sticky Section) ── */}
      <section className="py-24 px-5 bg-[#171e19] text-white">
        <div className="max-w-[1240px] mx-auto grid grid-cols-1 md:grid-cols-[1fr_2fr] gap-12">
          <div className="md:sticky md:top-28 self-start">
            <h2 className="disp text-[clamp(3.5rem,8vw,6.5rem)]">
              How it <span className="hl">works</span>
            </h2>
          </div>

          <div className="space-y-12">
            <div className="flex gap-8 items-start pt-8 border-t border-[rgba(183,198,194,0.15)] group">
              <span className="font-disp text-7xl md:text-8xl text-[#ffe17c] opacity-25 group-hover:opacity-100 transition-opacity leading-none">
                1
              </span>
              <div>
                <h3 className="disp text-3xl">Upload your report</h3>
                <p className="mt-3 text-[#b7c6c2] text-sm md:text-base leading-relaxed">
                  Add a PDF or a photo of your medical report. The OCR engine reads parameters and test measurements automatically.
                </p>
              </div>
            </div>

            <div className="flex gap-8 items-start pt-8 border-t border-[rgba(183,198,194,0.15)] group">
              <span className="font-disp text-7xl md:text-8xl text-[#ffe17c] opacity-25 group-hover:opacity-100 transition-opacity leading-none">
                2
              </span>
              <div>
                <h3 className="disp text-3xl">The matching models run</h3>
                <p className="mt-3 text-[#b7c6c2] text-sm md:text-base leading-relaxed">
                  The Meta-Classifier selects relevant disease models and adaptive median imputation runs to estimate clinical risk.
                </p>
              </div>
            </div>

            <div className="flex gap-8 items-start pt-8 border-y border-[rgba(183,198,194,0.15)] pb-8 group">
              <span className="font-disp text-7xl md:text-8xl text-[#ffe17c] opacity-25 group-hover:opacity-100 transition-opacity leading-none">
                3
              </span>
              <div>
                <h3 className="disp text-3xl">Act on the guidance</h3>
                <p className="mt-3 text-[#b7c6c2] text-sm md:text-base leading-relaxed">
                  Structured evidence-based dietary modifications, exercise guidelines, red flags, and next clinical steps.
                </p>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* ── FAQ (Good to Know) ── */}
      <section className="py-24 px-5 bg-[#f8f9fa]">
        <div className="max-w-[1240px] mx-auto">
          <div className="max-w-[720px] mb-12">
            <h2 className="disp text-[clamp(2.8rem,6vw,4.5rem)]">
              Good to <span className="hl">know</span>
            </h2>
          </div>

          <div className="max-w-[820px] space-y-2">
            {faqs.map((faq, idx) => (
              <div key={idx} className="border-t border-[rgba(23,30,25,0.1)] last:border-b">
                <button
                  type="button"
                  onClick={() => setOpenFaq(openFaq === idx ? -1 : idx)}
                  className="w-full py-6 flex justify-between items-center text-left text-lg md:text-xl font-medium"
                >
                  <span>{faq.q}</span>
                  <span
                    className={`w-8 h-8 rounded-full bg-[#ffe17c] text-[#171e19] flex items-center justify-center text-xl transition-transform ${
                      openFaq === idx ? 'rotate-45' : ''
                    }`}
                  >
                    +
                  </span>
                </button>
                {openFaq === idx && (
                  <p className="pb-6 text-sm md:text-base opacity-75 max-w-2xl leading-relaxed">
                    {faq.a}
                  </p>
                )}
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* ── Giant Yellow CTA Section ── */}
      <section className="bg-[#ffe17c] text-[#171e19] py-28 px-5 text-center relative overflow-hidden">
        <div className="absolute left-1/2 top-1/2 -translate-x-1/2 -translate-y-1/2 font-disp uppercase text-[clamp(8rem,28vw,24rem)] opacity-10 select-none pointer-events-none leading-none">
          Report
        </div>
        <div className="max-w-[1240px] mx-auto relative z-10">
          <h2 className="disp text-[clamp(3.2rem,8vw,6.5rem)]">
            Ready when your report is
          </h2>
          <p className="text-lg md:text-2xl max-w-xl mx-auto mt-6 opacity-90">
            Upload your document and get values, multi-model screening, and evidence-based guidance in one place.
          </p>
          <div className="mt-10 flex flex-col sm:flex-row gap-3 max-w-[560px] mx-auto bg-[#171e19] p-3 rounded-xl shadow-2xl">
            <Link
              to="/upload"
              className="flex-1 flex items-center px-5 rounded-lg bg-transparent text-white/80 text-sm border border-white/20 min-h-[54px]"
            >
              Choose a PDF or image
            </Link>
            <Link to="/upload" className="btn-y !bg-[#ffe17c] !text-[#171e19]">
              Upload report
            </Link>
          </div>
        </div>
      </section>
    </div>
  )
}
