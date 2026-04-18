import os
from pathlib import Path
from agents.base import BaseAgent, AgentContext
from models.schemas import ProcessingStage


class FileValidationAgent(BaseAgent):
    """Agent responsible for validating uploaded files"""
    
    def __init__(self, supported_extensions: tuple):
        super().__init__("FileValidationAgent")
        self.supported_extensions = supported_extensions
    
    def execute(self, context: AgentContext) -> AgentContext:
        """Validate file extension and accessibility"""
        print(f"🔍 [{self.name}] Validating file: {Path(context.file_path).name}")
        
        file_extension = Path(context.file_path).suffix.lower()
        
        if file_extension not in self.supported_extensions:
            context.current_stage = ProcessingStage.FAILED
            raise ValueError(
                f"Unsupported file type '{file_extension}'. "
                f"Supported: {', '.join(self.supported_extensions)}"
            )
        
        if not os.path.exists(context.file_path):
            context.current_stage = ProcessingStage.FAILED
            raise FileNotFoundError(f"File not found: {context.file_path}")
        
        print(f"✅ [{self.name}] Validation successful")
        context.current_stage = ProcessingStage.CONVERSION
        return context
