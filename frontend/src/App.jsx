import { useState } from 'react'
import './App.css'
import Header from './components/Header'
import UploadSection from './components/UploadSection'
import ResultsDisplay from './components/ResultsDisplay'
import Features from './components/Features'
import Footer from './components/Footer'

function App() {
  const [uploadedFile, setUploadedFile] = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)
  const [results, setResults] = useState(null)
  const [parseMode, setParseMode] = useState('offline')

  const handleFileUpload = async (file, mode) => {
    setUploadedFile(file)
    setError(null)
    setResults(null)
    setLoading(true)
    setParseMode(mode)

    try {
      const formData = new FormData()
      formData.append('file', file)

      const endpoint = mode === 'offline' 
        ? '/api/parse_resume/offline'
        : '/api/parse_resume/online'

      // For local development: adjust base URL
      const baseUrl = process.env.NODE_ENV === 'development' 
        ? 'http://localhost:8000'
        : ''

      const response = await fetch(`${baseUrl}${endpoint}`, {
        method: 'POST',
        body: formData,
        headers: {
          'Accept': 'application/json',
        }
      })

      if (!response.ok) {
        const errorData = await response.json()
        throw new Error(errorData.detail || `Upload failed: ${response.statusText}`)
      }

      const data = await response.json()
      setResults(data)
    } catch (err) {
      setError(err.message || 'Failed to process file')
      console.error('Upload error:', err)
    } finally {
      setLoading(false)
    }
  }

  const handleReset = () => {
    setUploadedFile(null)
    setResults(null)
    setError(null)
  }

  return (
    <div className="app">
      <Header />
      
      <main className="main-content">
        {!results ? (
          <>
            <UploadSection 
              onFileUpload={handleFileUpload}
              loading={loading}
              error={error}
              uploadedFile={uploadedFile}
            />
            <Features />
          </>
        ) : (
          <ResultsDisplay 
            results={results}
            file={uploadedFile}
            mode={parseMode}
            onReset={handleReset}
            loading={loading}
          />
        )}
      </main>

      <Footer />
    </div>
  )
}

export default App
