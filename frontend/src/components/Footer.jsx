import { Link } from 'react-router-dom'

export default function Footer() {
  return (
    <footer className="bg-[#171e19] text-[#b7c6c2] py-12 text-sm border-t border-[rgba(183,198,194,0.14)]">
      <div className="max-w-[1240px] mx-auto px-5 flex flex-col md:flex-row justify-between items-start md:items-center gap-6">
        <div>
          <Link to="/" className="font-disp text-2xl uppercase text-white tracking-normal block mb-2">
            ArogyaDrishti<span className="text-[#ffe17c]">.</span>
          </Link>
          <p className="max-w-xl text-xs md:text-sm text-[#b7c6c2]/80 leading-relaxed">
            ArogyaDrishti (formerly SehatSetu) is an academic AI screening and educational tool.
            Predictions are not a confirmed medical diagnosis. Please consult a qualified doctor for any health concern.
          </p>
        </div>
        <div className="text-xs text-[#b7c6c2]/60">
          © {new Date().getFullYear()} ArogyaDrishti. Multi-Disease AI Pipeline.
        </div>
      </div>
    </footer>
  )
}
