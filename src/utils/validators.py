"""
Data validation helpers
"""
import re
from typing import Dict, Any, List
from src.utils.logger import get_logger

logger = get_logger(__name__)

def validate_model_number(model_number: str) -> bool:
    """Validate model number format"""
    if not model_number or len(model_number) < 3:
        return False
    
    # Common model number patterns
    patterns = [
        r'^[A-Z0-9\-]+$',  # Alphanumeric with hyphens
        r'^[A-Z]{2,}[0-9]+',  # Letters followed by numbers
        r'^[0-9]+[A-Z]+'  # Numbers followed by letters
    ]
    
    for pattern in patterns:
        if re.match(pattern, model_number):
            return True
    
    logger.warning(f"Model number {model_number} doesn't match common patterns")
    return True  # Return True even if no match, just log warning

def validate_extracted_data(data: Dict[str, Any]) -> List[str]:
    """Validate extracted data and return list of missing fields"""
    required_fields = ['asset_classification', 'manufacturer', 'summary']
    missing_fields = []
    
    for field in required_fields:
        if not data.get(field):
            missing_fields.append(field)
    
    if missing_fields:
        logger.warning(f"Missing required fields: {missing_fields}")
    
    return missing_fields

def sanitize_text(text: str) -> str:
    """Sanitize text for safe processing"""
    if not text:
        return ""
    
    # Remove control characters
    text = ''.join(char for char in text if ord(char) >= 32 or char == '\n')
    
    # Limit length
    if len(text) > 1000:
        text = text[:997] + "..."
    
    return text.strip()
