import { useState } from 'react'
import './UploadSection.css'
import { Upload, Loader, AlertCircle } from 'lucide-react'

export default function UploadSection({ onFileUpload, loading, error, uploadedFile }) {
  const [dragActive, setDragActive] = useState(false)
  const [parseMode, setParseMode] = useState('offline')

  const handleDrag = (e) => {
    e.preventDefault()
    e.stopPropagation()
    if (e.type === 'dragenter' || e.type === 'dragover') {
      setDragActive(true)
    } else if (e.type === 'dragleave') {
      setDragActive(false)
    }
  }

  const handleDrop = (e) => {
    e.preventDefault()
    e.stopPropagation()
    setDragActive(false)

    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      const file = e.dataTransfer.files[0]
      if (isValidFile(file)) {
        onFileUpload(file, parseMode)
      }
    }
  }

  const handleChange = (e) => {
    if (e.target.files && e.target.files[0]) {
      const file = e.target.files[0]
      if (isValidFile(file)) {
        onFileUpload(file, parseMode)
      }
    }
  }

  const isValidFile = (file) => {
    const validTypes = ['application/pdf', 'image/jpeg', 'image/png', 'image/tiff', 'image/bmp', 'application/vnd.openxmlformats-officedocument.wordprocessingml.document', 'application/msword']
    const validExtensions = ['.pdf', '.jpg', '.jpeg', '.png', '.tiff', '.bmp', '.docx', '.doc']
    
    const hasValidType = validTypes.includes(file.type)
    const hasValidExtension = validExtensions.some(ext => file.name.toLowerCase().endsWith(ext))

    if (!hasValidType && !hasValidExtension) {
      alert('Invalid file type. Please upload: PDF, DOCX, DOC, PNG, JPG, JPEG, TIFF, BMP')
      return false
    }

    if (file.size > 50 * 1024 * 1024) {
      alert('File is too large. Maximum size is 50MB')
      return false
    }

    return true
  }

  return (
    <section className="upload-section">
      <div className="upload-container">
        <h2 className="section-title">Upload Your Resume</h2>
        <p className="section-subtitle">Powered by AI-driven OCR and intelligent parsing</p>

        {/* Mode Selection */}
        <div className="mode-selector">
          <label className={`mode-option ${parseMode === 'offline' ? 'active' : ''}`}>
            <input
              type="radio"
              value="offline"
              checked={parseMode === 'offline'}
              onChange={(e) => setParseMode(e.target.value)}
              disabled={loading}
            />
            <span className="mode-label">
              <span className="mode-title">⚡ Offline</span>
              <span className="mode-desc">Fast OCR extraction (no network)</span>
            </span>
          </label>

          <label className={`mode-option ${parseMode === 'online' ? 'active' : ''}`}>
            <input
              type="radio"
              value="online"
              checked={parseMode === 'online'}
              onChange={(e) => setParseMode(e.target.value)}
              disabled={loading}
            />
            <span className="mode-label">
              <span className="mode-title">🧠 AI-Enhanced</span>
              <span className="mode-desc">Intelligent parsing with Gemini AI</span>
            </span>
          </label>
        </div>

        {/* Drop Zone */}
        <div
          className={`drop-zone ${dragActive ? 'active' : ''} ${loading ? 'loading' : ''}`}
          onDragEnter={handleDrag}
          onDragLeave={handleDrag}
          onDragOver={handleDrag}
          onDrop={handleDrop}
        >
          <input
            type="file"
            id="file-input"
            onChange={handleChange}
            disabled={loading}
            accept=".pdf,.docx,.doc,.png,.jpg,.jpeg,.tiff,.bmp"
            className="file-input"
          />

          <label htmlFor="file-input" className="drop-label">
            {loading ? (
              <>
                <Loader className="spinner" />
                <p>Processing your resume...</p>
                <span className="loading-text">This may take a moment</span>
              </>
            ) : (
              <>
                <Upload size={48} />
                <p>Drag and drop your resume here</p>
                <span>or click to browse</span>
                <span className="file-types">PDF • DOCX • PNG • JPG • TIFF • BMP (Max 50MB)</span>
              </>
            )}
          </label>
        </div>

        {/* Error Message */}
        {error && (
          <div className="error-message">
            <AlertCircle size={20} />
            <div>
              <p className="error-title">Upload Failed</p>
              <p className="error-text">{error}</p>
            </div>
          </div>
        )}

        {/* Uploaded File Info */}
        {uploadedFile && !loading && (
          <div className="file-info">
            <div className="file-icon">📄</div>
            <div className="file-details">
              <p className="file-name">{uploadedFile.name}</p>
              <p className="file-size">{(uploadedFile.size / 1024).toFixed(2)} KB</p>
            </div>
          </div>
        )}

        {/* Features Grid */}
        <div className="features-grid">
          <div className="feature-card">
            <div className="feature-icon">📄</div>
            <h3>Multi-Format</h3>
            <p>Support for all major document formats</p>
          </div>
          <div className="feature-card">
            <div className="feature-icon">🤖</div>
            <h3>AI-Powered</h3>
            <p>Intelligent structured extraction</p>
          </div>
          <div className="feature-card">
            <div className="feature-icon">⚡</div>
            <h3>Lightning Fast</h3>
            <p>Process resumes in seconds</p>
          </div>
        </div>
      </div>
    </section>
  )
}
