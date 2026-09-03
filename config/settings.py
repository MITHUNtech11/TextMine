import os
from pathlib import Path
from dotenv import load_dotenv

# --- PATHS & ENVIRONMENT ---
BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(dotenv_path=BASE_DIR / ".env", override=True)

TESSERACT_PATH = os.getenv("TESSERACT_PATH")
# Some editors may save .env with UTF-8 BOM, which can prefix the first key.
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY") or os.getenv("\ufeffGOOGLE_API_KEY")
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")

if not GOOGLE_API_KEY:
    raise RuntimeError("GOOGLE_API_KEY environment variable not set.")

# --- CONFIGURE TESSERACT ---
if TESSERACT_PATH:
    import pytesseract
    pytesseract.pytesseract.tesseract_cmd = TESSERACT_PATH
else:
    print("⚠️ Warning: TESSERACT_PATH not set in .env. Assuming Tesseract is in system PATH.")

# --- OCR CONFIGURATION ---
GENTLE_OCR_CONFIG = "--oem 3 --psm 3 -c textord_heavy_nr=1"
SCANNED_OCR_CONFIG = "--oem 3 --psm 1 -c tessedit_do_invert=0 -c textord_heavy_nr=1 --dpi 400"
LOW_CONFIDENCE_THRESHOLD = 55.0

# --- FILE SUPPORT ---
SUPPORTED_EXTENSIONS = (
    '.pdf', '.docx', '.doc', '.png', '.jpg', '.jpeg', 
    '.jfif', '.tiff', '.bmp'
)

# --- PROCESSING ---
MAX_RETRIES = 5  # Increased for rate limit recovery
REQUEST_TIMEOUT = 60  # Timeout per request in seconds
REQUEST_DELAY = 1  # Delay between requests in seconds (throttling)
DEFAULT_ZOOM_FACTOR = 4
DEFAULT_NUM_WORKERS = 4

# --- API ---
API_TITLE = "TextMine - AI-Powered Document Text Extraction"
API_HOST = "0.0.0.0"
API_PORT = 8000
