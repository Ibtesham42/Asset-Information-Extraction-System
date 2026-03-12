"""
Retry decorator/logic
"""
import asyncio
from functools import wraps
from src.utils.logger import get_logger

logger = get_logger(__name__)

def async_retry(max_attempts=3, delay=1):
    """Decorator for async retry logic with exponential backoff"""
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            last_exception = None
            for attempt in range(1, max_attempts + 1):
                try:
                    result = await func(*args, **kwargs)
                    if result:  # Success condition
                        if attempt > 1:
                            logger.info(f"Success after {attempt} attempts")
                        return result
                    
                    if attempt == max_attempts:
                        logger.warning(f"All {max_attempts} attempts exhausted, no result returned")
                        return None
                        
                except Exception as e:
                    last_exception = e
                    logger.warning(f"Attempt {attempt}/{max_attempts} failed: {str(e)}")
                
                # Exponential backoff
                wait_time = delay * (2 ** (attempt - 1))
                logger.info(f"Waiting {wait_time} seconds before retry {attempt + 1}")
                await asyncio.sleep(wait_time)
            
            if last_exception:
                logger.error(f"All retry attempts failed: {str(last_exception)}")
            return None
        return wrapper
    return decorator

def retry(max_attempts=3, delay=1):
    """Decorator for sync retry logic"""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            import time
            last_exception = None
            for attempt in range(1, max_attempts + 1):
                try:
                    result = func(*args, **kwargs)
                    if result:
                        if attempt > 1:
                            logger.info(f"Success after {attempt} attempts")
                        return result
                    
                    if attempt == max_attempts:
                        logger.warning(f"All {max_attempts} attempts exhausted")
                        return None
                        
                except Exception as e:
                    last_exception = e
                    logger.warning(f"Attempt {attempt} failed: {str(e)}")
                
                time.sleep(delay * attempt)
            
            if last_exception:
                raise last_exception
            return None
        return wrapper
    return decorator
