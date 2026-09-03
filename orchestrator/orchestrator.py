import time
import random
from typing import Dict, Any, Literal
from pydantic import BaseModel, Field

from agents.base import AgentContext
from agents import (
    FileValidationAgent,
    ConversionAgent,
    OCRAgent,
    LLMParsingAgent,
    QualityCheckAgent,
    RecoveryAgent,
)
from models.schemas import ProcessingStage
from config.settings import (
    SUPPORTED_EXTENSIONS,
    GENTLE_OCR_CONFIG,
    SCANNED_OCR_CONFIG,
    LOW_CONFIDENCE_THRESHOLD,
    GOOGLE_API_KEY,
    GEMINI_MODEL,
    DEFAULT_NUM_WORKERS,
)


# ============================================================
# RESPONSE MODELS
# ============================================================

class OfflineParseResponse(BaseModel):
    """Response model for offline OCR-only parsing"""
    extracted_text: str = Field(description="Raw extracted text from OCR")
    page_count: int = Field(description="Number of pages processed")
    confidence_score: float = Field(description="Average confidence of OCR extraction (0-100)")
    processing_mode: Literal["offline"] = "offline"


class OnlineParseResponse(BaseModel):
    """Response model for online parsing with Gemini"""
    parsed_json: Dict[str, Any] = Field(description="Structured resume data")
    extracted_text: str = Field(description="Raw extracted text from OCR")
    page_count: int = Field(description="Number of pages processed")
    processing_mode: Literal["online"] = "online"


# ============================================================
# ORCHESTRATORS
# ============================================================

class ResumeParsingOrchestrator:
    """Central orchestrator that coordinates all agents"""
    
    def __init__(self, mode: Literal["offline", "online"] = "online"):
        """Initialize all agents
        
        Args:
            mode: "offline" for OCR-only, "online" for OCR+Gemini parsing
        """
        self.mode = mode
        self.file_agent = FileValidationAgent(SUPPORTED_EXTENSIONS)
        self.conversion_agent = ConversionAgent()
        self.ocr_agent = OCRAgent(
            GENTLE_OCR_CONFIG,
            SCANNED_OCR_CONFIG,
            LOW_CONFIDENCE_THRESHOLD,
            num_workers=DEFAULT_NUM_WORKERS
        )
        
        # Only initialize LLM agent in online mode
        if self.mode == "online":
            self.llm_agent = LLMParsingAgent(GOOGLE_API_KEY, GEMINI_MODEL)
            self.quality_agent = QualityCheckAgent()
            self.recovery_agent = RecoveryAgent()
        
        mode_label = "🌐 ONLINE" if mode == "online" else "📴 OFFLINE"
        print(f"🚀 Orchestrator initialized with mode: {mode_label}")
    
    def process_offline(self, file_path: str, temp_dir: str) -> OfflineParseResponse:
        """OCR-only processing (no network required)"""
        context = AgentContext(file_path=file_path, temp_dir=temp_dir)
        
        print("\n" + "="*60)
        print("📴 OFFLINE RESUME PARSING PIPELINE STARTED (OCR ONLY)")
        print("="*60 + "\n")
        
        try:
            # Execute OCR agents only
            context = self.file_agent.execute(context)
            context = self.conversion_agent.execute(context)
            context = self.ocr_agent.execute(context)
            
            print("\n" + "="*60)
            print("✅ OFFLINE PIPELINE COMPLETED SUCCESSFULLY")
            print("="*60 + "\n")
            
            return OfflineParseResponse(
                extracted_text=context.extracted_text,
                page_count=context.page_count,
                confidence_score=context.confidence_score,
                processing_mode="offline"
            )
        
        except Exception as e:
            context.current_stage = ProcessingStage.FAILED
            print("\n" + "="*60)
            print(f"❌ OFFLINE PIPELINE FAILED AT STAGE: {context.current_stage}")
            print("="*60 + "\n")
            raise
    
    def process_online(self, file_path: str, temp_dir: str) -> OnlineParseResponse:
        """Full processing with OCR + Gemini parsing"""
        context = AgentContext(file_path=file_path, temp_dir=temp_dir)
        
        print("\n" + "="*60)
        print("🌐 ONLINE RESUME PARSING PIPELINE STARTED (OCR + GEMINI)")
        print("="*60 + "\n")
        
        try:
            # Execute agents
            context = self.file_agent.execute(context)
            context = self.conversion_agent.execute(context)
            context = self.ocr_agent.execute(context)
            
            # Parsing with retry logic and exponential backoff with jitter
            while context.current_stage == ProcessingStage.PARSING:
                try:
                    context = self.llm_agent.execute(context)
                    context = self.quality_agent.execute(context)
                    break
                except Exception as e:
                    if self.recovery_agent.can_recover(context, e):
                        context.error_count += 1
                        
                        # Calculate backoff with jitter: base * 2^attempt + random(0, base)
                        base_delay = 5
                        exponential_delay = base_delay * (2 ** context.error_count)
                        jitter = random.uniform(0, base_delay)
                        total_delay = exponential_delay + jitter
                        
                        if '429' in str(e) or 'resource_exhausted' in str(e).lower():
                            print(f"⏳ Rate limit hit. Waiting {total_delay:.1f}s before retry...")
                            time.sleep(total_delay)
                        else:
                            time.sleep(2)
                        
                        print(f"🔄 Retrying parsing (attempt {context.error_count + 1}/{context.max_retries + 1})...")
                        continue
                    else:
                        raise
            
            print("\n" + "="*60)
            print("✅ ONLINE PIPELINE COMPLETED SUCCESSFULLY")
            print("="*60 + "\n")
            
            return OnlineParseResponse(
                parsed_json=context.parsed_json,
                extracted_text=context.extracted_text,
                page_count=context.page_count,
                processing_mode="online"
            )
        
        except Exception as e:
            context.current_stage = ProcessingStage.FAILED
            print("\n" + "="*60)
            print(f"❌ ONLINE PIPELINE FAILED AT STAGE: {context.current_stage}")
            print("="*60 + "\n")
            raise
    
    def process(self, file_path: str, temp_dir: str) -> Dict[str, Any]:
        """Main process method - routes to offline or online based on mode"""
        if self.mode == "offline":
            result = self.process_offline(file_path, temp_dir)
            return result.model_dump()
        else:
            result = self.process_online(file_path, temp_dir)
            return result.model_dump()
