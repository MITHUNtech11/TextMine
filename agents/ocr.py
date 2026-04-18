from typing import List, Tuple
from PIL import Image
from concurrent.futures import ProcessPoolExecutor, as_completed
import io

from agents.base import BaseAgent, AgentContext
from models.schemas import ProcessingStage
from utils.extraction_helpers import (
    process_extraction_job,
    load_pdf_pages
)


class OCRAgent(BaseAgent):
    """Enhanced agent with parallel multi-method extraction"""
    
    def __init__(self, gentle_config: str, scanned_config: str, threshold: float, num_workers: int = 4):
        super().__init__("OCRAgent")
        self.gentle_config = gentle_config
        self.scanned_config = scanned_config
        self.threshold = threshold
        self.num_workers = num_workers
    
    def execute(self, context: AgentContext) -> AgentContext:
        """Extract text using parallel methods and select best result"""
        print(f"📄 [{self.name}] Starting multi-method extraction with {self.num_workers} workers")
        
        if not context.pdf_path:
            raise ValueError("No PDF path available for extraction")
        
        pages = load_pdf_pages(context.pdf_path)
        
        if not pages:
            raise ValueError("No pages loaded from PDF")
        
        full_text = ""
        total_chars = 0
        
        for i, page in enumerate(pages):
            print(f"   Processing page {i + 1}/{len(pages)}...")
            
            # Convert PIL Image to bytes for pickling
            img_byte_arr = io.BytesIO()
            page.save(img_byte_arr, format='PNG')
            img_bytes = img_byte_arr.getvalue()
            
            # Prepare extraction jobs
            extraction_jobs = [
                ("Native PDF", context.pdf_path, i, None),
                ("Gentle OCR", None, None, img_bytes, self.gentle_config, None),
                ("Heavy OCR", None, None, img_bytes, self.scanned_config, "heavy"),
                ("PSM 6", None, None, img_bytes, "--oem 3 --psm 6", None),
                ("PSM 4", None, None, img_bytes, "--oem 3 --psm 4", None),
                ("High Contrast", None, None, img_bytes, self.scanned_config, "high_contrast"),
            ]
            
            # Run all methods in parallel
            extraction_results = self._run_parallel_extraction(extraction_jobs)
            
            # Select best result
            if extraction_results:
                best_method, best_text, best_char_count = max(extraction_results, key=lambda x: x[2])
                
                if best_char_count < 50:
                    print(f"   ⚠️ Warning: Page {i + 1} appears blank or has minimal content ({best_char_count} chars)")
                
                print(f"   ✅ Best method: {best_method} with {best_char_count} characters")
                
                full_text += (
                    f"\n----- PAGE {i + 1} (Method: {best_method}) -----\n"
                    f"Characters: {best_char_count}\n"
                    f"{best_text.strip()}\n"
                )
                total_chars += best_char_count
            else:
                print(f"   ❌ All extraction methods failed for page {i + 1}")
        
        context.extracted_text = full_text.strip()
        context.page_count = len(pages)
        # Confidence score: percentage of text extracted (estimated)
        context.confidence_score = min(100.0, (total_chars / 1000) * 10) if total_chars > 0 else 0.0
        
        print(f"✅ [{self.name}] Extraction complete. Total: {len(context.extracted_text)} characters")
        context.current_stage = ProcessingStage.PARSING
        return context
    
    
    def _run_parallel_extraction(self, extraction_jobs: List[Tuple]) -> List[Tuple]:
        """Run extraction jobs in parallel"""
        from config.settings import TESSERACT_PATH
        extraction_results = []
        
        with ProcessPoolExecutor(max_workers=self.num_workers) as executor:
            futures = {}
            for job in extraction_jobs:
                method_name = job[0]
                job_with_path = job + (TESSERACT_PATH,)
                future = executor.submit(process_extraction_job, job_with_path)
                futures[future] = method_name
            
            for future in as_completed(futures):
                method_name = futures[future]
                try:
                    text, char_count = future.result()
                    extraction_results.append((method_name, text, char_count))
                    print(f"      Method ({method_name}): {char_count} chars")
                except Exception as e:
                    print(f"      Method ({method_name}): Failed - {str(e)[:50]}")
        
        return extraction_results
