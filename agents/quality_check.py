from agents.base import BaseAgent, AgentContext
from models.schemas import ProcessingStage
from utils.validators import is_valid_email, calculate_completeness


class QualityCheckAgent(BaseAgent):
    """Enhanced agent with comprehensive validation"""
    
    def __init__(self, min_completeness_score: float = 0.4):
        super().__init__("QualityCheckAgent")
        self.required_fields = ['name', 'first_name', 'last_name']
        self.recommended_fields = ['email', 'phone']
        self.min_completeness_score = min_completeness_score
    
    def execute(self, context: AgentContext) -> AgentContext:
        """Comprehensive quality validation"""
        print(f"✓ [{self.name}] Checking parsing quality")
        
        if not context.parsed_json:
            raise ValueError("No parsed data to validate")
        
        data = context.parsed_json
        issues = []
        
        # Check 1: Required fields
        missing_required = [field for field in self.required_fields if not data.get(field)]
        if missing_required:
            issues.append(f"Missing required fields: {', '.join(missing_required)}")
        
        # Check 2: Data completeness score
        completeness = calculate_completeness(data, self.required_fields, self.recommended_fields)
        if completeness < self.min_completeness_score:
            issues.append(f"Low completeness score: {completeness:.1%}")
        
        # Check 3: Field validation
        if data.get('email') and not is_valid_email(data['email']):
            issues.append("Invalid email format")
        
        if data.get('phone') and len(str(data['phone'])) < 10:
            issues.append("Phone number too short")
        
        # Check 4: Minimum text extraction
        text_length = len(context.extracted_text)
        if text_length < 100:
            issues.append(f"Very low text extraction: {text_length} chars")
        
        # Decision: Pass or retry?
        if issues:
            print(f"⚠️ [{self.name}] Quality issues found:")
            for issue in issues:
                print(f"     - {issue}")
            
            critical_issues = [i for i in issues if "required" in i.lower() or "completeness" in i.lower()]
            
            if critical_issues and context.error_count < context.max_retries:
                context.error_count += 1
                context.current_stage = ProcessingStage.PARSING
                raise ValueError(f"Quality check failed: {'; '.join(critical_issues)}")
            else:
                print(f"⚠️ [{self.name}] Non-critical issues detected, continuing...")
        
        print(f"✅ [{self.name}] Quality check passed")
        return context
