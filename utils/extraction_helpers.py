"""Module-level functions for multiprocessing (must be at module level for pickling)"""

import io
import pytesseract
import cv2
import numpy as np
from PIL import Image
import fitz


def process_extraction_job(job_data):
    """Process a single extraction job (module-level for pickling)"""
    method_name, pdf_path, page_num, img_bytes, *extra = job_data
    
    try:
        if method_name == "Native PDF":
            text = extract_native_pdf(pdf_path, page_num)
        else:
            img = Image.open(io.BytesIO(img_bytes))
            config = extra[0] if extra else "--oem 3 --psm 3"
            preprocess_type = extra[1] if len(extra) > 1 else None
            tesseract_path = extra[2] if len(extra) > 2 else None
            text = run_ocr_on_image(img, config, preprocess_type, tesseract_path)
        
        return text, len(text)
    except Exception as e:
        return "", 0



def extract_native_pdf(pdf_path: str, page_num: int) -> str:
    """Extract text from PDF without OCR"""
    try:
        doc = fitz.open(pdf_path)
        page = doc.load_page(page_num)
        text = page.get_text()
        doc.close()
        return text
    except Exception:
        return ""


def run_ocr_on_image(img: Image.Image, config: str, preprocess_type: str = None, tesseract_path: str = None) -> str:
    """Run OCR with optional preprocessing"""
    try:
        import pytesseract
        import cv2
        import numpy as np
        from PIL import Image
        
        # Set Tesseract path in worker process
        if tesseract_path:
            pytesseract.pytesseract.tesseract_cmd = tesseract_path
        
        # Apply preprocessing if specified
        if preprocess_type == "heavy":
            img = _apply_heavy_preprocessing(img)
        elif preprocess_type == "high_contrast":
            img = _apply_high_contrast(img)
        
        # Run Tesseract
        text = pytesseract.image_to_string(img, lang="eng", config=config)
        return text
    except Exception as e:
        print(f"OCR Error: {str(e)}")
        return ""



def _apply_heavy_preprocessing(img: Image.Image) -> Image.Image:
    """Apply heavy preprocessing to image"""
    img_cv = np.array(img)
    if len(img_cv.shape) == 3:
        img_cv = cv2.cvtColor(img_cv, cv2.COLOR_RGB2GRAY)
    
    clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8, 8))
    img_cv = clahe.apply(img_cv)
    gaussian = cv2.GaussianBlur(img_cv, (0, 0), 3.0)
    img_cv = cv2.addWeighted(img_cv, 2.0, gaussian, -1.0, 0)
    binary = cv2.adaptiveThreshold(
        img_cv, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 21, 10
    )
    return Image.fromarray(binary)


def _apply_high_contrast(img: Image.Image) -> Image.Image:
    """Apply high contrast preprocessing to image"""
    img_cv = np.array(img)
    if len(img_cv.shape) == 3:
        img_cv = cv2.cvtColor(img_cv, cv2.COLOR_RGB2GRAY)
    
    alpha = 2.0
    adjusted = cv2.convertScaleAbs(img_cv, alpha=alpha, beta=0)
    binary = cv2.adaptiveThreshold(
        adjusted, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 15, 10
    )
    return Image.fromarray(binary)


def load_pdf_pages(pdf_path: str, zoom_factor: int = 4):
    """Load PDF pages as high-resolution images"""
    pages = []
    try:
        doc = fitz.open(pdf_path)
        for page_num in range(doc.page_count):
            page = doc.load_page(page_num)
            matrix = fitz.Matrix(zoom_factor, zoom_factor)
            pix = page.get_pixmap(matrix=matrix, alpha=False)
            img_data = pix.tobytes("ppm")
            img = Image.frombytes("RGB", [pix.width, pix.height], img_data)
            pages.append(img)
        doc.close()
        return pages
    except Exception as e:
        raise Exception(f"PDF page loading failed: {e}")
