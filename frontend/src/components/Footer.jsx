import './Footer.css'
import { Github, ExternalLink } from 'lucide-react'

export default function Footer() {
  const currentYear = new Date().getFullYear()

  return (
    <footer className="footer">
      <div className="footer-content">
        <div className="footer-section">
          <h3>TextMine</h3>
          <p>AI-powered document text extraction for the modern world.</p>
          <div className="footer-links">
            <a href="https://github.com/MITHUNtech11/TextMine" target="_blank" rel="noopener noreferrer">
              <Github size={20} />
              GitHub
            </a>
            <a href="https://github.com/MITHUNtech11" target="_blank" rel="noopener noreferrer">
              <ExternalLink size={20} />
              Creator
            </a>
          </div>
        </div>

        <div className="footer-section">
          <h4>Features</h4>
          <ul>
            <li><a href="#upload">Resume Upload</a></li>
            <li><a href="#features">AI Processing</a></li>
            <li><a href="#features">Structured Output</a></li>
          </ul>
        </div>

        <div className="footer-section">
          <h4>Tech Stack</h4>
          <ul>
            <li>FastAPI</li>
            <li>React + Vite</li>
            <li>Google Gemini 2.0</li>
            <li>Tesseract OCR</li>
          </ul>
        </div>
      </div>

      <div className="footer-divider"></div>

      <div className="footer-bottom">
        <p>&copy; {currentYear} TextMine. All rights reserved.</p>
        <p>Built with ❤️ for the community</p>
      </div>
    </footer>
  )
}
