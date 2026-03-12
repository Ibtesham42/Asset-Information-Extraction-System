"""
Environment Variables & Configuration
"""
from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    # API Keys
    GEMINI_API_KEY: Optional[str] = None
    OPENAI_API_KEY: Optional[str] = None
    SERPAPI_KEY: Optional[str] = None
    GOOGLE_SEARCH_API_KEY: Optional[str] = None
    GOOGLE_SEARCH_ENGINE_ID: Optional[str] = None
    
    # Model Configuration
    DEFAULT_LLM_MODEL: str = "gemini-pro"  # or "gpt-3.5-turbo"
    MAX_RETRIES: int = 5
    RETRY_DELAY_SECONDS: int = 2
    
    # Search Configuration
    MAX_SEARCH_RESULTS: int = 5
    SEARCH_TIMEOUT_SECONDS: int = 10
    
    # Server
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    DEBUG: bool = False
    
    class Config:
        env_file = ".env"

settings = Settings()
