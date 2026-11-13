import { BrowserRouter, Routes, Route } from 'react-router-dom'
import { AppProvider } from './context/AppContext'
import DisclaimerBar from './components/DisclaimerBar'
import Navbar from './components/Navbar'
import Footer from './components/Footer'
import WorkflowDock from './components/WorkflowDock'
import HomePage from './pages/HomePage'
import UploadPage from './pages/UploadPage'
import AnalysisPage from './pages/AnalysisPage'
import ResultsPage from './pages/ResultsPage'
import GuidancePage from './pages/GuidancePage'
import Demo from './components/ui/demo'

export default function App() {
  return (
    <BrowserRouter>
      <AppProvider>
        <div className="min-h-screen bg-white text-[#171e19] flex flex-col font-body selection:bg-[#ffe17c] selection:text-[#171e19]">
          <DisclaimerBar />
          <Navbar />
          <main className="flex-1 pt-20 pb-20 sm:pb-28">
            <Routes>
              <Route path="/" element={<HomePage />} />
              <Route path="/upload" element={<UploadPage />} />
              <Route path="/analysis" element={<AnalysisPage />} />
              <Route path="/results" element={<ResultsPage />} />
              <Route path="/guidance" element={<GuidancePage />} />
              <Route path="/demo" element={<Demo />} />
            </Routes>
          </main>
          <WorkflowDock />
          <Footer />
        </div>
      </AppProvider>
    </BrowserRouter>
  )
}
