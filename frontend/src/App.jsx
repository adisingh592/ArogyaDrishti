import { BrowserRouter, Routes, Route } from 'react-router-dom'
import { AppProvider } from './context/AppContext'
import DisclaimerBar from './components/DisclaimerBar'
import Navbar from './components/Navbar'
import Footer from './components/Footer'
import HomePage from './pages/HomePage'
import UploadPage from './pages/UploadPage'
import AnalysisPage from './pages/AnalysisPage'
import ResultsPage from './pages/ResultsPage'
import GuidancePage from './pages/GuidancePage'

export default function App() {
  return (
    <BrowserRouter>
      <AppProvider>
        <div className="min-h-screen bg-white text-[#171e19] flex flex-col font-body selection:bg-[#ffe17c] selection:text-[#171e19]">
          <DisclaimerBar />
          <Navbar />
          <main className="flex-1 pt-20">
            <Routes>
              <Route path="/" element={<HomePage />} />
              <Route path="/upload" element={<UploadPage />} />
              <Route path="/analysis" element={<AnalysisPage />} />
              <Route path="/results" element={<ResultsPage />} />
              <Route path="/guidance" element={<GuidancePage />} />
            </Routes>
          </main>
          <Footer />
        </div>
      </AppProvider>
    </BrowserRouter>
  )
}
