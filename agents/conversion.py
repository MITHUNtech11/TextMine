import os
from pathlib import Path
from PIL import Image
from docx2pdf import convert
from agents.base import BaseAgent, AgentContext
from models.schemas import ProcessingStage


class ConversionAgent(BaseAgent):
    """Agent responsible for converting various formats to PDF"""
    
    def __init__(self):
        super().__init__("ConversionAgent")
    
    def execute(self, context: AgentContext) -> AgentContext:
        """Convert DOCX or images to PDF format"""
        print(f"🔄 [{self.name}] Converting file to PDF format")
        
        extension = Path(context.file_path).suffix.lower()
        base_name = Path(context.file_path).stem
        
        if extension == '.pdf':
            context.pdf_path = context.file_path
            print(f"✅ [{self.name}] File already in PDF format")
        
        elif extension in ['.docx', '.doc']:
            output_pdf_path = os.path.join(context.temp_dir, f"{base_name}_temp.pdf")
            try:
                convert(context.file_path, output_pdf_path)
                if os.path.exists(output_pdf_path):
                    context.pdf_path = output_pdf_path
                    print(f"✅ [{self.name}] DOCX converted to PDF")
                else:
                    raise Exception("PDF conversion produced no output")
            except Exception as e:
                raise Exception(f"DOCX conversion failed: {e}")
        
        elif extension in ['.png', '.jpg', '.jpeg', '.tiff', '.bmp']:
            try:
                temp_pdf_path = os.path.join(context.temp_dir, f"{base_name}_temp_img.pdf")
                img = Image.open(context.file_path).convert('RGB')
                img.save(temp_pdf_path, "PDF", resolution=300)
                context.pdf_path = temp_pdf_path
                print(f"✅ [{self.name}] Image converted to PDF")
            except Exception as e:
                raise Exception(f"Image conversion failed: {e}")
        
        if not context.pdf_path:
            context.current_stage = ProcessingStage.FAILED
            raise Exception("Conversion agent could not produce PDF")
        
        context.current_stage = ProcessingStage.OCR
        return context
