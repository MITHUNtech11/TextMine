# 🚀 TextMine - Quick Setup Guide

Get TextMine up and running in 5 minutes!

## Prerequisites

- Python 3.10+
- Git
- Tesseract OCR
- Google Gemini API Key

## ⚡ Quick Start

### 1️⃣ Clone Repository
```bash
git clone https://github.com/yourusername/textmine.git
cd textmine
```

### 2️⃣ Setup Virtual Environment
```powershell
# Windows PowerShell
python -m venv venv
.\.venv\Scripts\Activate.ps1

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### 3️⃣ Install Dependencies
```bash
pip install -r requirements.txt
```

### 4️⃣ Get API Key
1. Visit: https://aistudio.google.com/apikey
2. Click "Create API Key"
3. Copy the key

### 5️⃣ Configure Environment
```bash
# Copy example config
copy .env.example .env

# Edit .env file
# Windows: notepad .env
# Mac/Linux: nano .env
```

Add your API key:
```env
GOOGLE_API_KEY=your_api_key_here
TESSERACT_PATH=C:\Program Files\Tesseract-OCR\tesseract.exe
```

### 6️⃣ Install Tesseract OCR

**Windows (Chocolatey):**
```powershell
choco install tesseract
```

**Windows (Manual):**
1. Download: https://github.com/UB-Mannheim/tesseract/wiki
2. Run installer
3. Update TESSERACT_PATH in .env

**macOS:**
```bash
brew install tesseract
```

**Linux (Ubuntu/Debian):**
```bash
sudo apt-get install tesseract-ocr poppler-utils
```

### 7️⃣ Run Server
```bash
uvicorn main:app --reload
```

Visit: **http://localhost:8000/docs**

## 📊 Test It

Upload a resume or document in the Swagger UI to see TextMine in action!

## 🆘 Troubleshooting

### "TESSERACT_PATH not set"
Update `.env` with correct path. On Windows:
```powershell
# Find Tesseract
Get-ChildItem -Path "C:\Program Files" -Filter "tesseract.exe" -Recurse
```

### "GOOGLE_API_KEY not set"
- Create .env from .env.example
- Add your API key from https://aistudio.google.com/apikey

### "Module not found"
```bash
# Reinstall dependencies
pip install --force-reinstall -r requirements.txt
```

## 📚 Next Steps

- Read [DEPLOYMENT.md](DEPLOYMENT.md) for production setup
- Check [CONTRIBUTING.md](CONTRIBUTING.md) to contribute
- Visit [Documentation](Documentation/) for detailed guides

## 🎯 Common Tasks

### Run tests (if available)
```bash
pytest
```

### Check API health
```bash
curl http://localhost:8000/health
```

### Parse a resume via CLI
```bash
curl -F "file=@resume.pdf" http://localhost:8000/parse_resume/online
```

## 📖 Documentation

- **API Docs**: http://localhost:8000/docs (when running)
- **Architecture**: See [DEPLOYMENT.md](DEPLOYMENT.md)
- **Contributing**: See [CONTRIBUTING.md](CONTRIBUTING.md)

---

**Questions?** Open an issue on GitHub! 🤝
