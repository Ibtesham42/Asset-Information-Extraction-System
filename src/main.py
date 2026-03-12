"""
FastAPI Application Entry Point
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.api.endpoints import extract
from src.config.settings import settings
from src.utils.logger import setup_logging

# Setup logging
setup_logging()

# Create FastAPI app
app = FastAPI(
    title="Asset Information Extraction System",
    description="AI-powered system for extracting product information from web search",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # Kisi bhi origin se request allow
    allow_credentials=True,
    allow_methods=["*"], # Sab HTTP methods allow
    allow_headers=["*"], # Sab headers allow
)

# Include routers
app.include_router(extract.router, prefix="/api/v1", tags=["extraction"])

@app.get("/")
async def root():
    return {
        "message": "Asset Information Extraction System",
        "version": "1.0.0",
        "docs": "/docs"
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "src.main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG
    )
