import json
import os
import sys
import time
from pathlib import Path
from json import JSONDecodeError

# Ensure project virtual environment site-packages are on sys.path if not running in .venv
_venv_site_packages = Path(__file__).resolve().parent.parent / ".venv" / "Lib" / "site-packages"
if _venv_site_packages.exists() and str(_venv_site_packages) not in sys.path:
    sys.path.insert(0, str(_venv_site_packages))

from google import genai
from google.genai import types
from pydantic import ValidationError

from agents.base import BaseAgent, AgentContext
from models.schemas import ProcessingStage, DocumentExtractionRoot
from config.settings import REQUEST_TIMEOUT, REQUEST_DELAY


class LLMParsingAgent(BaseAgent):
    """Agent responsible for reconstructing and maximizing readable text using Gemini"""
    
    def __init__(self, api_key: str, model_name: str | None = None):
        super().__init__("LLMParsingAgent")
        self.api_key = api_key
        env_model = os.getenv("GEMINI_MODEL")
        self.model_name = model_name or env_model or "gemini-2.5-flash"
        self.client = genai.Client(api_key=self.api_key)
        self.last_request_time = 0

    @staticmethod
    def _extract_json_text(raw_text: str) -> str:
        """Extract a JSON object from model output that may include markdown fences."""
        text = (raw_text or "").strip()

        if text.startswith("```"):
            lines = text.splitlines()
            if len(lines) >= 3 and lines[-1].strip() == "```":
                text = "\n".join(lines[1:-1]).strip()
                if text.lower().startswith("json"):
                    text = text[4:].strip()

        start = text.find("{")
        end = text.rfind("}")
        if start == -1 or end == -1 or end <= start:
            raise ValueError("No JSON object found in LLM response")

        return text[start:end + 1]
    
    @staticmethod
    def _build_visual_part(context: AgentContext) -> types.Part | None:
        """Attempt to load the original file as an image or PDF Part for visual grounding."""
        target_path = context.file_path or context.pdf_path
        if not target_path or not os.path.exists(target_path):
            return None
        
        try:
            file_size = os.path.getsize(target_path)
            # Limit direct visual upload to 15MB to ensure fast response
            if file_size > 15 * 1024 * 1024:
                return None
            
            ext = os.path.splitext(target_path)[1].lower()
            mime_map = {
                ".png": "image/png",
                ".jpg": "image/jpeg",
                ".jpeg": "image/jpeg",
                ".webp": "image/webp",
                ".bmp": "image/bmp",
                ".tiff": "image/tiff",
                ".pdf": "application/pdf"
            }
            mime_type = mime_map.get(ext)
            if not mime_type and context.pdf_path and os.path.exists(context.pdf_path):
                target_path = context.pdf_path
                mime_type = "application/pdf"
            
            if not mime_type:
                return None
            
            with open(target_path, "rb") as f:
                data = f.read()
            
            return types.Part.from_bytes(data=data, mime_type=mime_type)
        except Exception as e:
            print(f"⚠️ [LLMParsingAgent] Could not attach visual part: {e}")
            return None

    def execute(self, context: AgentContext) -> AgentContext:
        """Reconstruct degraded text and extract structured document content using Gemini"""
        print(f"🤖 [{self.name}] Reconstructing readable text with {self.model_name}")
        
        if not context.extracted_text and not context.file_path:
            raise ValueError("No extracted text or file available for parsing")
        
        # Request throttling: ensure minimum delay between requests
        time_since_last_request = time.time() - self.last_request_time
        if time_since_last_request < REQUEST_DELAY:
            sleep_time = REQUEST_DELAY - time_since_last_request
            print(f"⏱️  Throttling requests: waiting {sleep_time:.2f}s...")
            time.sleep(sleep_time)
        
        system_instruction = (
            "You are TextMine AI, a world-class Document Text Reconstruction, OCR Error-Correction, and Maximum Retrieval Engine.\n"
            "Your core objective is to analyze degraded, low-quality, blurry, or noisy documents and reconstruct the absolute MAXIMUM ACCURATE, READABLE TEXT possible.\n\n"
            "CORE DIRECTIVES:\n"
            "1. MAXIMUM TEXT RETRIEVAL: Extract and reconstruct every readable word, number, line, and detail. Do NOT omit or prematurely truncate text. If words are blurred or degraded, deduce and recover them accurately using context.\n"
            "2. CORRECT OCR ERRORS & NOISE: Fix character confusion (e.g. '0' vs 'O', '1' vs 'l' or '|', '5' vs 'S', 'rn' vs 'm'), reconnect broken or hyphenated words, fix irregular spacing, and repair punctuation.\n"
            "3. NATURAL FLOW & STRUCTURE: Present the restored text in clean, coherent, flowing paragraphs and sections in natural reading order. Ignore OCR diagnostic headers (e.g. '----- PAGE 1 (Method: ...) -----').\n"
            "4. HIGH FACTUAL FIDELITY: Strictly preserve genuine names, dates, numbers, contact info, and terminology without inventing unrelated content.\n"
            "5. OUTPUT FORMAT: Return ONLY a single valid JSON object adhering strictly to the schema provided."
        )
        
        config = types.GenerateContentConfig(
            system_instruction=system_instruction,
            response_mime_type="application/json",
            temperature=0.1
        )

        schema_hint = DocumentExtractionRoot.model_json_schema()
        prompt_text = (
            "Analyze the document and raw OCR text below. Reconstruct and retrieve the absolute maximum readable text, "
            "repairing OCR errors, blur, and noise.\n\n"
            f"Target JSON schema:\n{json.dumps(schema_hint, ensure_ascii=False)}\n\n"
            f"Raw OCR Candidate Text:\n---\n{context.extracted_text or 'No OCR text available.'}"
        )
        
        contents = []
        visual_part = self._build_visual_part(context)
        if visual_part:
            contents.append(visual_part)
        contents.append(prompt_text)

        try:
            self.last_request_time = time.time()
            response = self.client.models.generate_content(
                model=self.model_name,
                contents=contents,
                config=config
            )

            json_text = self._extract_json_text(response.text)
            parsed = json.loads(json_text)
            
            try:
                validated = DocumentExtractionRoot.model_validate(parsed)
                context.parsed_json = validated.model_dump(mode="json")
                context.readable_text = validated.readable_text
            except ValidationError:
                context.parsed_json = parsed
                context.readable_text = parsed.get("readable_text") or str(parsed.get("content") or context.extracted_text or "")
            
            if not context.readable_text:
                context.readable_text = context.extracted_text or ""

            print(f"✅ [{self.name}] Text reconstruction successful ({len(context.readable_text)} chars retrieved)")
            context.current_stage = ProcessingStage.COMPLETE
            return context
        except Exception as e:
            # If multimodal call failed, retry once with text-only
            if visual_part:
                print(f"⚠️ [{self.name}] Multimodal call failed ({e}), falling back to text-only reconstruction...")
                try:
                    self.last_request_time = time.time()
                    response = self.client.models.generate_content(
                        model=self.model_name,
                        contents=[prompt_text],
                        config=config
                    )
                    json_text = self._extract_json_text(response.text)
                    parsed = json.loads(json_text)
                    context.parsed_json = parsed
                    context.readable_text = parsed.get("readable_text") or context.extracted_text or ""
                    print(f"✅ [{self.name}] Text-only reconstruction successful ({len(context.readable_text)} chars)")
                    context.current_stage = ProcessingStage.COMPLETE
                    return context
                except Exception as fallback_err:
                    raise Exception(f"LLM reconstruction failed: {fallback_err}")
            raise Exception(f"LLM parsing failed: {e}")


