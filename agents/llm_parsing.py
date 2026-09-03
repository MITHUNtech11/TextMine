import json
import os
import time
from json import JSONDecodeError
from google import genai
from google.genai import types
from pydantic import ValidationError

from agents.base import BaseAgent, AgentContext
from models.schemas import ProcessingStage, ResumeRoot
from config.settings import REQUEST_TIMEOUT, REQUEST_DELAY


class LLMParsingAgent(BaseAgent):
    """Agent responsible for structured parsing using Gemini"""
    
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
    
    def execute(self, context: AgentContext) -> AgentContext:
        """Parse extracted text into structured JSON"""
        print(f"🤖 [{self.name}] Parsing text with {self.model_name}")
        
        if not context.extracted_text:
            raise ValueError("No extracted text available for parsing")
        
        # Request throttling: ensure minimum delay between requests
        time_since_last_request = time.time() - self.last_request_time
        if time_since_last_request < REQUEST_DELAY:
            sleep_time = REQUEST_DELAY - time_since_last_request
            print(f"⏱️  Throttling requests: waiting {sleep_time:.2f}s...")
            time.sleep(sleep_time)
        
        system_instruction = (
            "You are an expert Resume Parsing and Data Extraction engine. "
            "Your task is to meticulously extract all relevant information from the provided "
            "resume text and map it precisely to the required JSON schema structure. "
            "The text may contain header information like '----- PAGE X -----' and 'Confidence: Y%'. "
            "IGNORE all such header/metadata information and focus ONLY on the raw resume content. "
            "Extract first_name and last_name separately from the full name field. "
            "You MUST return ONLY a single valid JSON object that adheres to the schema."
        )
        
        config = types.GenerateContentConfig(
            system_instruction=system_instruction,
            response_mime_type="application/json",
            temperature=0.1
        )

        schema_hint = ResumeRoot.model_json_schema()
        prompt = (
            "Parse the following resume text and return structured JSON. "
            "Return only a single JSON object with no extra text. "
            "If a value is unknown, use null for optional fields and [] for list fields.\n\n"
            f"Target JSON schema:\n{json.dumps(schema_hint, ensure_ascii=False)}\n\n"
            f"Resume text:\n---\n{context.extracted_text}"
        )
        
        try:
            self.last_request_time = time.time()
            response = self.client.models.generate_content(
                model=self.model_name,
                contents=[prompt],
                config=config
            )

            json_text = self._extract_json_text(response.text)
            parsed = json.loads(json_text)
            validated = ResumeRoot.model_validate(parsed)
            context.parsed_json = validated.model_dump(mode="json")
            print(f"✅ [{self.name}] Parsing successful")
            context.current_stage = ProcessingStage.COMPLETE
            return context
        except ValidationError as e:
            raise Exception(f"LLM output failed schema validation: {e}")
        except JSONDecodeError as e:
            raise Exception(f"LLM returned invalid JSON: {e}")
        except Exception as e:
            raise Exception(f"LLM parsing failed: {e}")

