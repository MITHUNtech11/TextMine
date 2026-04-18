import './Header.css'
import { Gem, Github } from 'lucide-react'

export default function Header() {
  return (
    <header className="header">
      <div className="header-content">
        <div className="logo-section">
          <div className="logo-icon">
            <Gem size={32} />
          </div>
          <div className="logo-text">
            <h1>TextMine</h1>
            <p>AI-Powered Resume Parser</p>
          </div>
        </div>
        
        <a 
          href="https://github.com/MITHUNtech11/TextMine" 
          target="_blank" 
          rel="noopener noreferrer"
          className="github-link"
        >
          <Github size={24} />
          <span>GitHub</span>
        </a>
      </div>
      
      <div className="header-gradient"></div>
    </header>
  )
}
