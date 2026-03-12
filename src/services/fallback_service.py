"""
Fallback handling service
"""
from typing import Dict
from src.models.response_models import FallbackResponse
from src.utils.logger import get_logger

logger = get_logger(__name__)

class FallbackService:
    def __init__(self):
        self.fallback_count = 0
        
    def get_fallback_response(self, model_number: str) -> Dict:
        """Return fallback response when extraction fails"""
        self.fallback_count += 1
        logger.warning(f"Returning fallback response (count: {self.fallback_count})")
        
        return FallbackResponse(
            model_number=model_number
        ).dict()
    
    def reset_count(self):
        """Reset fallback counter"""
        self.fallback_count = 0
        logger.info("Fallback counter reset")
