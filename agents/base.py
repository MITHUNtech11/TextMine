from dataclasses import dataclass, field
from models.schemas import ProcessingStage
from typing import Optional, Dict, Any


@dataclass
class AgentContext:
    """Shared context passed between agents"""
    file_path: str
    temp_dir: str
    pdf_path: Optional[str] = None
    extracted_text: Optional[str] = None
    parsed_json: Optional[Dict[str, Any]] = None
    current_stage: ProcessingStage = ProcessingStage.VALIDATION
    error_count: int = 0
    max_retries: int = 3
    page_count: int = 0
    confidence_score: float = 0.0


class BaseAgent:
    """Base class for all agents"""
    
    def __init__(self, name: str):
        self.name = name
    
    def execute(self, context: AgentContext) -> AgentContext:
        """Execute agent logic - to be overridden by subclasses"""
        raise NotImplementedError("Subclasses must implement execute()")
