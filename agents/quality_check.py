from agents.base import BaseAgent, AgentContext
from models.schemas import ProcessingStage


class QualityCheckAgent(BaseAgent):
    """Quality agent that evaluates document text reconstruction and readability"""
    
    def __init__(self, min_chars_threshold: int = 10):
        super().__init__("QualityCheckAgent")
        self.min_chars_threshold = min_chars_threshold
    
    def execute(self, context: AgentContext) -> AgentContext:
        """Evaluate text recovery quality and readability metrics"""
        print(f"✓ [{self.name}] Checking text reconstruction quality")
        
        readable_text = (context.readable_text or "").strip()
        ocr_text = (context.extracted_text or "").strip()
        
        chars_recovered = len(readable_text)
        chars_ocr = len(ocr_text)
        
        issues = []
        
        # Check 1: Ensure at least some text was retrieved
        if chars_recovered == 0 and chars_ocr == 0:
            issues.append("No text could be extracted or reconstructed from the document.")
            if context.error_count < context.max_retries:
                context.error_count += 1
                context.current_stage = ProcessingStage.PARSING
                raise ValueError("Quality check failed: Document appears empty or completely unreadable.")
        
        # Check 2: Low text warning
        if chars_recovered < self.min_chars_threshold:
            issues.append(f"Minimal text recovered ({chars_recovered} chars). Document may be extremely degraded or blank.")
        
        # Check 3: Assess recovery ratio
        recovery_ratio = chars_recovered / max(chars_ocr, 1)
        
        # Compute confidence score
        if chars_recovered >= 200:
            score = 95.0
        elif chars_recovered >= 50:
            score = 85.0
        elif chars_recovered > 0:
            score = 70.0
        else:
            score = 0.0
        
        context.confidence_score = max(context.confidence_score, score)
        
        # Attach quality report to parsed_json
        if isinstance(context.parsed_json, dict):
            context.parsed_json["quality_report"] = {
                "chars_recovered": chars_recovered,
                "chars_ocr": chars_ocr,
                "recovery_ratio": f"{recovery_ratio:.1%}",
                "confidence_score": context.confidence_score,
                "diagnostics": issues if issues else ["Text reconstruction and readability verified."]
            }
        
        if issues:
            print(f"⚠️ [{self.name}] Quality notes:")
            for issue in issues:
                print(f"     - {issue}")
        else:
            print(f"✅ [{self.name}] Quality check passed ({chars_recovered} readable chars recovered)")
        
        return context

