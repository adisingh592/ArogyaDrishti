import { NavLink, Link } from 'react-router-dom'

const navLinks = [
  { to: '/', label: 'Home' },
  { to: '/upload', label: 'Upload' },
  { to: '/analysis', label: 'Analysis' },
  { to: '/results', label: 'Results' },
  { to: '/guidance', label: 'Guidance' },
]

export default function Navbar() {
  return (
    <header className="fixed top-0 left-0 right-0 h-20 z-50 bg-white/90 backdrop-blur-md border-b border-[rgba(23,30,25,0.1)] text-[#171e19]">
      <div className="max-w-[1240px] mx-auto px-5 h-full flex items-center justify-between gap-4">
        {/* Logo */}
        <Link to="/" className="font-disp text-3xl uppercase tracking-normal flex items-baseline">
          ArogyaDrishti<span className="text-[#ffe17c] text-4xl leading-none">.</span>
        </Link>

        {/* Links */}
        <nav className="hidden md:flex items-center gap-7 text-sm font-medium">
          {navLinks.map(({ to, label }) => (
            <NavLink
              key={to}
              to={to}
              end={to === '/'}
              className={({ isActive }) =>
                `py-2 border-b-2 transition-colors ${
                  isActive
                    ? 'border-[#ffe17c] text-[#171e19] font-bold'
                    : 'border-transparent text-[#171e19]/70 hover:text-[#171e19]'
                }`
              }
            >
              {label}
            </NavLink>
          ))}
        </nav>

        {/* Action Button */}
        <Link to="/upload" className="btn-pill">
          Upload report
        </Link>
      </div>
    </header>
  )
}
