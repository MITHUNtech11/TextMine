import { useState } from 'react'
import './ResultsDisplay.css'
import { Download, RotateCcw, ChevronDown } from 'lucide-react'

export default function ResultsDisplay({ results, file, mode, onReset }) {
  const [expandedSections, setExpandedSections] = useState({})

  const toggleSection = (section) => {
    setExpandedSections(prev => ({
      ...prev,
      [section]: !prev[section]
    }))
  }

  const downloadJSON = () => {
    const element = document.createElement('a')
    const file_name = file.name.split('.')[0]
    element.setAttribute('href', 'data:text/plain;charset=utf-8,' + encodeURIComponent(JSON.stringify(results, null, 2)))
    element.setAttribute('download', `${file_name}_extracted.json`)
    element.style.display = 'none'
    document.body.appendChild(element)
    element.click()
    document.body.removeChild(element)
  }

  const sections = [
    { 
      title: 'Personal Information', 
      key: 'personal_info',
      icon: '👤'
    },
    { 
      title: 'Professional Summary', 
      key: 'professional_summary',
      icon: '📝'
    },
    { 
      title: 'Experience', 
      key: 'experience',
      icon: '💼'
    },
    { 
      title: 'Education', 
      key: 'education',
      icon: '🎓'
    },
    { 
      title: 'Skills', 
      key: 'skills',
      icon: '🛠️'
    },
    { 
      title: 'Certifications', 
      key: 'certifications',
      icon: '📜'
    },
    { 
      title: 'Raw Text', 
      key: 'raw_text',
      icon: '📄'
    },
  ]

  return (
    <div className="results-container">
      <div className="results-header">
        <div className="result-title">
          <h2>✨ Extraction Complete</h2>
          <p className="mode-badge">{mode === 'offline' ? '⚡ Offline Processing' : '🧠 AI-Enhanced'}</p>
        </div>

        <div className="results-actions">
          <button className="btn-download" onClick={downloadJSON}>
            <Download size={20} />
            <span>Download JSON</span>
          </button>
          <button className="btn-reset" onClick={onReset}>
            <RotateCcw size={20} />
            <span>New Resume</span>
          </button>
        </div>
      </div>

      <div className="file-metadata">
        <div className="metadata-item">
          <span className="metadata-label">File:</span>
          <span className="metadata-value">{file.name}</span>
        </div>
        <div className="metadata-item">
          <span className="metadata-label">Size:</span>
          <span className="metadata-value">{(file.size / 1024).toFixed(2)} KB</span>
        </div>
        <div className="metadata-item">
          <span className="metadata-label">Processing Mode:</span>
          <span className="metadata-value">{mode === 'offline' ? 'Offline' : 'AI-Enhanced'}</span>
        </div>
      </div>

      <div className="results-sections">
        {sections.map(section => {
          const data = results[section.key]
          if (!data) return null

          const isExpanded = expandedSections[section.key]

          return (
            <div key={section.key} className="result-section">
              <button 
                className={`section-header ${isExpanded ? 'expanded' : ''}`}
                onClick={() => toggleSection(section.key)}
              >
                <span className="section-icon">{section.icon}</span>
                <span className="section-title">{section.title}</span>
                <ChevronDown className={`chevron ${isExpanded ? 'open' : ''}`} size={20} />
              </button>

              {isExpanded && (
                <div className="section-content">
                  {section.key === 'raw_text' ? (
                    <div className="raw-text-content">
                      <p>{data}</p>
                    </div>
                  ) : section.key === 'skills' && Array.isArray(data) ? (
                    <div className="skills-grid">
                      {data.map((skill, idx) => (
                        <span key={idx} className="skill-tag">{skill}</span>
                      ))}
                    </div>
                  ) : section.key === 'experience' && Array.isArray(data) ? (
                    <div className="experience-list">
                      {data.map((item, idx) => (
                        <div key={idx} className="experience-item">
                          {Object.entries(item).map(([key, value]) => (
                            <div key={key} className="detail-row">
                              <span className="detail-label">{key.replace(/_/g, ' ').toUpperCase()}</span>
                              <span className="detail-value">{typeof value === 'object' ? JSON.stringify(value) : String(value)}</span>
                            </div>
                          ))}
                        </div>
                      ))}
                    </div>
                  ) : section.key === 'education' && Array.isArray(data) ? (
                    <div className="education-list">
                      {data.map((item, idx) => (
                        <div key={idx} className="education-item">
                          {Object.entries(item).map(([key, value]) => (
                            <div key={key} className="detail-row">
                              <span className="detail-label">{key.replace(/_/g, ' ').toUpperCase()}</span>
                              <span className="detail-value">{typeof value === 'object' ? JSON.stringify(value) : String(value)}</span>
                            </div>
                          ))}
                        </div>
                      ))}
                    </div>
                  ) : typeof data === 'object' ? (
                    <div className="object-content">
                      {Object.entries(data).map(([key, value]) => (
                        <div key={key} className="detail-row">
                          <span className="detail-label">{key.replace(/_/g, ' ').toUpperCase()}</span>
                          <span className="detail-value">{typeof value === 'object' ? JSON.stringify(value, null, 2) : String(value)}</span>
                        </div>
                      ))}
                    </div>
                  ) : (
                    <p className="plain-text">{String(data)}</p>
                  )}
                </div>
              )}
            </div>
          )
        })}
      </div>

      <div className="results-footer">
        <p className="footer-text">
          💡 All data extracted and processed on our secure servers. Your data is not stored permanently.
        </p>
      </div>
    </div>
  )
}
