import './Features.css'
import { Zap, Brain, Lock, Cpu } from 'lucide-react'

export default function Features() {
  const features = [
    {
      icon: <Zap size={32} />,
      title: 'Lightning Fast',
      description: 'Process multiple resumes in seconds with parallel OCR extraction'
    },
    {
      icon: <Brain size={32} />,
      title: 'AI-Powered',
      description: 'Google Gemini 2.0 Flash for intelligent structured extraction'
    },
    {
      icon: <Lock size={32} />,
      title: 'Secure & Private',
      description: 'Your data is processed securely and not permanently stored'
    },
    {
      icon: <Cpu size={32} />,
      title: 'Multi-Format',
      description: 'Support for PDF, DOCX, DOC, PNG, JPG, JPEG, TIFF, and BMP'
    }
  ]

  return (
    <section className="features-section">
      <div className="features-container">
        <h2 className="features-title">Why TextMine?</h2>
        <p className="features-subtitle">Powerful features for professional document parsing</p>

        <div className="features-grid-large">
          {features.map((feature, index) => (
            <div key={index} className="feature-card-large">
              <div className="feature-icon-large">{feature.icon}</div>
              <h3>{feature.title}</h3>
              <p>{feature.description}</p>
            </div>
          ))}
        </div>

        <div className="stats-grid">
          <div className="stat-card">
            <div className="stat-number">6+</div>
            <div className="stat-label">OCR Methods</div>
          </div>
          <div className="stat-card">
            <div className="stat-number">95%+</div>
            <div className="stat-label">Accuracy</div>
          </div>
          <div className="stat-card">
            <div className="stat-number">&lt;5s</div>
            <div className="stat-label">Processing Time</div>
          </div>
          <div className="stat-card">
            <div className="stat-number">8+</div>
            <div className="stat-label">File Formats</div>
          </div>
        </div>
      </div>
    </section>
  )
}
