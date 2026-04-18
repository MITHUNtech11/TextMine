# TextMine Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [2.0.0] - 2024-04-18

### Added
- Rebranded to **TextMine** with updated messaging for general document text extraction
- Dual-mode API: Offline (OCR-only) and Online (OCR + Gemini AI)
- 6 parallel OCR methods for improved accuracy
- Agentic architecture with autonomous processing agents
- Quality validation pipeline
- Error recovery with intelligent retry logic
- Comprehensive GitHub repository setup
- Contributing guidelines
- MIT License

### Features
- Multi-format document support (PDF, DOCX, DOC, PNG, JPG, JPEG, TIFF, BMP)
- Parallel OCR processing with 4 workers
- Google Gemini 2.0 Flash integration
- Pydantic-based data validation
- FastAPI with Swagger UI
- Production-ready error handling

### Changed
- API title from "Agentic Resume Parsing Service" to "TextMine"
- Enhanced documentation for general use cases
- Improved README with architecture diagrams

---

## [1.0.0] - Initial Release

### Added
- Basic resume parsing functionality
- OCR text extraction
- Resume data structuring
- API endpoints for parsing

---

For more information, see [GitHub Releases](https://github.com/yourusername/TextMine/releases)
