"""
API route handlers for extraction
"""
from fastapi import APIRouter, HTTPException, BackgroundTasks
from src.models.request_models import AssetRequest
from src.models.response_models import AssetResponse
from src.services.extraction_service import ExtractionService
from src.utils.logger import get_logger

router = APIRouter()
logger = get_logger(__name__)
extraction_service = ExtractionService()

@router.post("/extract", response_model=AssetResponse)
async def extract_asset_info(
    request: AssetRequest,
    background_tasks: BackgroundTasks
):
    """
    Extract asset information from model number and classification
    
    - **model_number**: Required. The product model number
    - **asset_classification_name**: Required. The asset classification
    - **manufacturer**: Optional. Manufacturer name
    - **asset_classification_guid2**: Optional. Asset classification GUID
    """
    try:
        logger.info(f"Received extraction request: {request.model_number}")
        
        # Process extraction
        result = await extraction_service.extract_asset_info(request)
        
        # Add background task for logging/metrics
        background_tasks.add_task(log_completion, request, result)
        
        return result
        
    except Exception as e:
        logger.error(f"Request failed: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

async def log_completion(request: AssetRequest, result: dict):
    """Background task to log completion"""
    logger.info(f"Completed extraction for {request.model_number}")
    # Add any additional logging or metrics here
