# ⛏️ TextMine - AI-Powered Document Text Extraction

[![GitHub license](https://img.shields.io/github/license/yourusername/TextMine)](https://github.com/yourusername/TextMine/blob/main/LICENSE)
[![Python Version](https://img.shields.io/badge/Python-3.10%2B-blue)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104+-green)](https://fastapi.tiangolo.com/)
[![Contributions Welcome](https://img.shields.io/badge/contributions-welcome-brightgreen.svg?style=flat)](https://github.com/yourusername/TextMine/issues)

**Extract structured data from low-quality images and documents with AI-powered accuracy.**

TextMine is an intelligent, production-ready application for extracting and structuring text from scanned documents, poor-quality images, and multi-format files. Perfect for digitizing resumes, invoices, receipts, forms, and any text-heavy documents.

**Powered by**: FastAPI • Google Gemini AI • Tesseract OCR • Autonomous Agents

## ✨ Features

- 📄 **Multi-Format Support**: PDF, DOCX, DOC, PNG, JPG, JPEG, TIFF, BMP
- 🤖 **Agentic Architecture**: Autonomous agents for validation, conversion, OCR, and parsing
- 🧠 **AI-Powered Extraction**: Google Gemini 2.0 Flash for intelligent structured parsing
- 🔄 **Parallel OCR Processing**: 6 OCR methods running in parallel for optimal accuracy
- 🛡️ **Smart Error Recovery**: Automatic retry logic with exponential backoff
- ✓ **Quality Validation**: Comprehensive data completeness and format checks
- 📊 **Structured Output**: JSON schema-validated resume data
- ⚡ **Fast Processing**: Multi-core parallel extraction and processing

## 🏗️ Project Structure

\`\`\`
resume-parser/
├── config/              # Configuration and settings
│   ├── __init__.py
│   └── settings.py      # API keys, paths, OCR configs
├── models/              # Pydantic schemas
│   ├── __init__.py
│   └── schemas.py       # Resume data models
├── agents/              # AI agents (modular)
│   ├── __init__.py
│   ├── base.py          # Base agent class
│   ├── file_validation.py
│   ├── conversion.py
│   ├── ocr.py
│   ├── llm_parsing.py
│   ├── quality_check.py
│   └── recovery.py
├── utils/               # Helper functions
│   ├── __init__.py
│   ├── extraction_helpers.py  # OCR helpers
│   └── validators.py    # Validation utilities
├── orchestrator/        # Main orchestrator
│   ├── __init__.py
│   └── orchestrator.py  # Coordinates all agents
├── main.py              # FastAPI app entry point
├── requirements.txt     # Python dependencies
├── .env                 # Environment variables (create this)
└── README.md            # This file
\`\`\`

## 🚀 Quick Start

### Prerequisites

- Python 3.10+
- Tesseract OCR
- Google Gemini API Key

### 1. Clone & Setup

\`\`\`powershell
# Create virtual environment
python -m venv venv

# Activate (Windows PowerShell)
.\\venv\\Scripts\\Activate.ps1

# Install dependencies
pip install -r requirements.txt
\`\`\`

### 2. Install System Dependencies

**Windows (Tesseract):**
\`\`\`powershell
choco install tesseract
# Or download: https://github.com/UB-Mannheim/tesseract/wiki
\`\`\`

**macOS:**
\`\`\`bash
brew install tesseract
\`\`\`

**Linux (Ubuntu/Debian):**
\`\`\`bash
sudo apt-get install tesseract-ocr poppler-utils
\`\`\`

### 3. Configure Environment

Create \`.env\` file in project root:

\`\`\`env
GOOGLE_API_KEY=your_api_key_from_https://aistudio.google.com/apikey
TESSERACT_PATH=C:\\Program Files\\Tesseract-OCR\\tesseract.exe
\`\`\`

**Get your API Key:**
1. Go to https://aistudio.google.com/apikey
2. Click "Create API Key"
3. Copy and paste into .env

### 4. Run the Backend

Start the FastAPI backend from the project root:

\`\`\`powershell
uvicorn main:app --reload
# API runs on http://localhost:8000
\`\`\`

### 5. Run the Frontend

Open a second PowerShell window, change to the project root, and serve the
static frontend:

\`\`\`powershell
python -m http.server 5500 --bind 127.0.0.1 --directory site
\`\`\`

Open the frontend at [http://127.0.0.1:5500/](http://127.0.0.1:5500/).
The frontend is configured to send extraction requests to the backend at
`http://127.0.0.1:8000`.

## 📖 Usage

### Option 1: Swagger UI (Easiest)

1. Open: [**http://localhost:8000/docs**](http://localhost:8000/docs)
2. Click **\`/parse_resume\`** endpoint
3. Click **"Try it out"**
4. Upload your resume file
5. Click **"Execute"**

### Option 2: PowerShell

\`\`\`powershell
\$filePath = "C:\\Users\\YourName\\Desktop\\resume.pdf"
\$form = @{ file = Get-Item -Path \$filePath }
\$response = Invoke-WebRequest -Uri "http://localhost:8000/parse_resume" -Method Post -Form \$form
\$result = \$response.Content | ConvertFrom-Json
\$result | ConvertTo-Json -Depth 10
\`\`\`

### Option 3: Health Check

\`\`\`powershell
Invoke-WebRequest -Uri "http://localhost:8000/health" -Method Get
\`\`\`

## 📤 API Endpoints

### POST /parse_resume
Upload and parse a resume file.

**Request:**
- Form data: \`file\` (PDF, DOCX, PNG, JPG, etc.)

**Response:**
\`\`\`json
{
  "name": "John Doe",
  "first_name": "John",
  "last_name": "Doe",
  "email": "john@example.com",
  "phone": "+1234567890",
  "skills": ["Python", "JavaScript", "React"],
  "employment": [
    {
      "company_name": "Tech Corp",
      "designation": "Senior Developer",
      "startDate": "2020-01",
      "endDate": null
    }
  ],
  "qualifications": [
    {
      "qualification": "Bachelor's",
      "specialization": "Computer Science",
      "university_name": "State University"
    }
  ],
  "languages": [
    {
      "language": "English",
      "can_read": "yes",
      "can_speak": "yes",
      "can_write": "yes"
    }
  ]
}
\`\`\`

### GET /health
Health check endpoint.

**Response:**
\`\`\`json
{"status": "healthy"}
\`\`\`

## 🤖 Agent Architecture

| Agent | Responsibility |
|-------|-----------------|
| **FileValidationAgent** | Validates file format and accessibility |
| **ConversionAgent** | Converts DOCX/Images to PDF format |
| **OCRAgent** | Extracts text using 6 parallel OCR methods |
| **LLMParsingAgent** | Structures text into JSON using Gemini AI |
| **QualityCheckAgent** | Validates completeness and data quality |
| **RecoveryAgent** | Handles errors intelligently with retry logic |

## 🔍 Processing Pipeline

\`\`\`
Upload File
    ↓
[FileValidationAgent] - Validate format
    ↓
[ConversionAgent] - Convert to PDF
    ↓
[OCRAgent] - Extract text (6 methods in parallel)
    ↓
[LLMParsingAgent] - Parse to JSON structure
    ↓
[QualityCheckAgent] - Validate quality
    ↓
[RecoveryAgent] - Handle errors if needed
    ↓
Return Parsed Resume
\`\`\`

## 🔧 Configuration

Edit \`config/settings.py\` to customize:

\`\`\`python
# OCR Configuration
GENTLE_OCR_CONFIG = "--oem 3 --psm 3 -c textord_heavy_nr=1"
SCANNED_OCR_CONFIG = "--oem 3 --psm 1 -c tessedit_do_invert=0 --dpi 400"

# Supported file types
SUPPORTED_EXTENSIONS = ('.pdf', '.docx', '.png', '.jpg', '.jpeg')

# Processing
MAX_RETRIES = 3
DEFAULT_NUM_WORKERS = 4  # Parallel workers

# API
API_PORT = 8000
\`\`\`

## 🐛 Troubleshooting

### "TESSERACT_PATH not set"
\`\`\`powershell
# Find Tesseract
Get-ChildItem -Path "C:\\Program Files" -Filter "tesseract.exe" -Recurse
# Update .env with correct path
\`\`\`

### "GOOGLE_API_KEY not set"
\`\`\`powershell
# Update .env file
notepad .env
# Add: GOOGLE_API_KEY=your_actual_key
\`\`\`

### "Cannot import agents"
\`\`\`powershell
# Verify __init__.py files exist
Get-ChildItem -Recurse -Filter "__init__.py"
\`\`\`

### "0 characters extracted"
- Ensure Tesseract is installed correctly
- Check that TESSERACT_PATH in .env is accurate
- Try with a different resume file

## 📊 Example Output

\`\`\`
🎯 AGENTIC RESUME PARSING PIPELINE STARTED

🔍 [FileValidationAgent] Validating file: resume.pdf
✅ [FileValidationAgent] Validation successful

🔄 [ConversionAgent] Converting file to PDF format
✅ [ConversionAgent] File already in PDF format

📄 [OCRAgent] Starting multi-method extraction with 4 workers
   Processing page 1/2...
      Method (High Contrast): 773 chars ✓
      Method (Heavy OCR): 168 chars
      Method (Native PDF): 0 chars
   ✅ Best method: High Contrast with 773 characters

🤖 [LLMParsingAgent] Parsing text with gemini-2.0-flash-exp
✅ [LLMParsingAgent] Parsing successful

✓ [QualityCheckAgent] Checking parsing quality
✅ [QualityCheckAgent] Quality check passed

✅ AGENTIC PIPELINE COMPLETED SUCCESSFULLY
\`\`\`

## 📋 Supported Resume Formats

- **Documents**: PDF, DOCX, DOC
- **Images**: PNG, JPG, JPEG, TIFF, BMP
- **Languages**: English (configurable in Tesseract)

## 🔐 Environment Variables

| Variable | Description | Example |
|----------|-------------|---------|
| \`GOOGLE_API_KEY\` | Gemini API key | \`AIzaSyD...\` |
| \`TESSERACT_PATH\` | Tesseract executable path | \`C:\\Program Files\\Tesseract-OCR\\tesseract.exe\` |

## 📦 Dependencies

- fastapi - Web framework
- uvicorn - ASGI server
- pydantic - Data validation
- google-genai - Gemini AI integration
- pytesseract - OCR engine wrapper
- pillow - Image processing
- opencv-python - Computer vision
- pymupdf - PDF handling
- docx2pdf - Document conversion

## 🚀 Deployment

### Local Development

Start the backend in one terminal:

\`\`\`powershell
uvicorn main:app --reload
\`\`\`

Start the frontend in a second terminal:

\`\`\`powershell
python -m http.server 5500 --bind 127.0.0.1 --directory site
\`\`\`

- Frontend: [http://127.0.0.1:5500/](http://127.0.0.1:5500/)
- API: [http://127.0.0.1:8000/](http://127.0.0.1:8000/)
- API documentation: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

### Production (Windows)
\`\`\`powershell
uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4
\`\`\`

### Docker (Optional)
Create a \`Dockerfile\` for containerization if needed.

## 📝 License

This project is provided as-is for educational and commercial use.

## 🤝 Contributing

Feel free to fork, modify, and improve this project!

## 📞 Support

If you encounter issues:
1. Check the Troubleshooting section
2. Verify .env configuration
3. Ensure all system dependencies are installed
4. Check API rate limits on Google AI Studio

---

**Last Updated:** November 2025
**Version:** 1.0
