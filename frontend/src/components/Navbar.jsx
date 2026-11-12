import { NavLink } from 'react-router-dom'
import { Activity } from 'lucide-react'

const navLinks = [
  { to: '/', label: 'Home' },
  { to: '/upload', label: 'Upload report' },
  { to: '/analysis', label: 'Analysis' },
  { to: '/results', label: 'Results' },
  { to: '/guidance', label: 'Guidance' },
]

export default function Navbar() {
  return (
    <nav className="bg-white border-b border-gray-200 sticky top-0 z-50">
      <div className="max-w-6xl mx-auto px-6 h-16 flex items-center justify-between">
        {/* Logo */}
        <NavLink to="/" className="flex items-center gap-2 font-serif font-semibold text-[#1a5e52] text-lg">
          <div className="w-8 h-8 rounded-md bg-[#1a5e52] flex items-center justify-center">
            <Activity size={16} className="text-white" />
          </div>
          SehatSetu
        </NavLink>

        {/* Links */}
        <div className="hidden md:flex items-center gap-6">
          {navLinks.map(({ to, label }) => (
            <NavLink
              key={to}
              to={to}
              end={to === '/'}
              className={({ isActive }) =>
                `text-sm pb-1 border-b-2 transition-colors ${
                  isActive
                    ? 'text-[#1a5e52] border-[#1a5e52] font-semibold'
                    : 'text-gray-500 border-transparent hover:text-[#1a5e52]'
                }`
              }
            >
              {label}
            </NavLink>
          ))}
        </div>
      </div>
    </nav>
  )
}
