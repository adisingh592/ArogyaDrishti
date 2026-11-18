import React from 'react'
import { useNavigate, useLocation } from 'react-router-dom'
import { Home, UploadCloud, Cpu, FileText, Sparkles } from 'lucide-react'
import { MagnificationDock, DockItemData } from '@/components/ui/magnification-dock'
import { useApp } from '@/context/AppContext'

export default function WorkflowDock() {
  const navigate = useNavigate()
  const location = useLocation()
  const { analysis } = useApp()

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
