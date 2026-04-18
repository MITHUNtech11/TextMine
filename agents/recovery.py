from agents.base import BaseAgent, AgentContext


class RecoveryAgent(BaseAgent):
    """Enhanced agent with smart error classification"""
    
    def __init__(self):
        super().__init__("RecoveryAgent")
        self.transient_errors = ['timeout', 'connection', '429', 'resource_exhausted', 'quota']
        self.retriable_errors = ['quality check', 'parsing failed', 'confidence']
        self.fatal_errors = ['invalid api key', 'authentication', 'file not found', 'unsupported']
    
    def can_recover(self, context: AgentContext, error: Exception) -> bool:
        """Intelligent error recovery decision"""
        print(f"🔧 [{self.name}] Analyzing error: {str(error)[:100]}")
        
        if context.error_count >= context.max_retries:
            print(f"❌ [{self.name}] Max retries ({context.max_retries}) reached.")
            return False
        
        error_str = str(error).lower()
        
        if any(keyword in error_str for keyword in self.fatal_errors):
            print(f"❌ [{self.name}] Fatal error detected. Cannot recover.")
            return False
        
        if any(keyword in error_str for keyword in self.transient_errors):
            print(f"✓ [{self.name}] Transient error. Retry recommended.")
            return True
        
        if any(keyword in error_str for keyword in self.retriable_errors):
            print(f"✓ [{self.name}] Retriable error. Attempting recovery.")
            return True
        
        print(f"⚠️ [{self.name}] Unknown error type. Failing safely.")
        return False
    
    def get_wait_time(self, error: Exception) -> int:
        """Suggest wait time based on error type"""
        error_str = str(error).lower()
        
        if '429' in error_str or 'rate limit' in error_str:
            return 60
        elif 'timeout' in error_str:
            return 5
        else:
            return 2
