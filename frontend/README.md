# TextMine Frontend

A beautiful, modern React + Vite frontend for the TextMine AI-powered resume parser.

## 🎨 Design Features

- **Modern UI**: Unique color scheme with deep purple, cyan, and gold accents
- **Responsive Design**: Works seamlessly on desktop, tablet, and mobile
- **Smooth Animations**: Polished transitions and loading states
- **Dark Theme**: Easy on the eyes with professional gradient backgrounds

## 🚀 Features

- **Drag & Drop Upload**: Intuitive file upload with visual feedback
- **Dual Processing Modes**:
  - ⚡ Offline: Fast OCR extraction (no network required)
  - 🧠 AI-Enhanced: Intelligent parsing with Google Gemini
- **Real-time Results**: Beautiful collapsible sections for extracted data
- **JSON Export**: Download extracted data as JSON
- **File Validation**: Support for PDF, DOCX, DOC, PNG, JPG, JPEG, TIFF, BMP

## 📦 Installation

```bash
# Install dependencies
npm install

# Start development server
npm run dev

# Build for production
npm run build

# Preview production build
npm run preview
```

## 🌐 GitHub Pages Deployment

```bash
# Install gh-pages (if not already installed)
npm install --save-dev gh-pages

# Deploy to GitHub Pages
npm run deploy
```

The app will be available at: `https://yourusername.github.io/TextMine`

## ⚙️ Configuration

Update `vite.config.js` if your repository name is different:

```javascript
export default defineConfig({
  base: '/YourRepoName/',
  // ...
})
```

## 🔗 API Integration

The frontend communicates with the FastAPI backend at:
- Development: `http://localhost:8000`
- Production: Configure the API endpoint in your environment

## 🛠️ Tech Stack

- **React 18**: UI framework
- **Vite**: Build tool & dev server
- **Lucide React**: Beautiful icons
- **Axios**: HTTP client
- **CSS**: Modern, custom styling with gradients

## 📱 Browser Support

- Chrome/Edge (latest 2 versions)
- Firefox (latest 2 versions)
- Safari (latest 2 versions)

## 🎯 Color Scheme

- **Primary**: Deep Purple (#7c3aed)
- **Accent**: Bright Cyan (#00d9ff)
- **Secondary**: Warm Gold (#f59e0b)
- **Background**: Dark gradient (#0f0f1e to #1a0f2e)

## 📝 License

MIT License - See LICENSE file in the root repository for details.

---

Built with ❤️ for the TextMine community
