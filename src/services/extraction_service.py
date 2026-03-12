"""
Main orchestration logic
"""
from typing import Dict, Any
from src.services.search_service import SearchService
from src.services.llm_service import LLMService
from src.services.fallback_service import FallbackService
from src.models.request_models import AssetRequest
from src.models.response_models import AssetResponse
from src.utils.retry import async_retry
from src.utils.logger import get_logger
from src.config.settings import settings

logger = get_logger(__name__)

class ExtractionService:
    def __init__(self):
        self.search_service = SearchService()
        self.llm_service = LLMService()
        self.fallback_service = FallbackService()
        
    async def extract_asset_info(self, request: AssetRequest) -> Dict[str, Any]:
        """Main extraction orchestration"""
        logger.info(f"Processing request for model: {request.model_number}")
        
        # Convert request to dict
        asset_info = request.dict()
        
        try:
            # Build search query
            query = await self.search_service.build_search_query(asset_info)
            
            # Perform search with retry
            search_results = await self._search_with_retry(query)
            
            if not search_results:
                logger.warning("No search results found")
                return self.fallback_service.get_fallback_response(request.model_number)
            
            logger.info(f"Retrieved {len(search_results)} search results")
            
            # Extract information using LLM with retry
            extracted_data = await self._extract_with_retry(search_results, asset_info)
            
            if not extracted_data:
                logger.warning("Extraction failed after retries")
                return self.fallback_service.get_fallback_response(request.model_number)
            
            # Validate and build response
            response = self._build_response(extracted_data, request.model_number)
            logger.info(f"Successfully extracted data for {request.model_number}")
            return response
            
        except Exception as e:
            logger.error(f"Extraction failed: {str(e)}")
            return self.fallback_service.get_fallback_response(request.model_number)
            
    @async_retry(max_attempts=settings.MAX_RETRIES, delay=settings.RETRY_DELAY_SECONDS)
    async def _search_with_retry(self, query: str):
        """Search with retry logic"""
        return await self.search_service.search(query)
        
    @async_retry(max_attempts=settings.MAX_RETRIES, delay=settings.RETRY_DELAY_SECONDS)
    async def _extract_with_retry(self, search_results, asset_info):
        """Extract with retry logic"""
        return await self.llm_service.extract_info(search_results, asset_info)
        
    def _build_response(self, extracted_data: Dict, original_model_number: str) -> Dict:
        """Build standardized response"""
        return AssetResponse(
            asset_classification=extracted_data.get('asset_classification', ''),
            manufacturer=extracted_data.get('manufacturer', ''),
            model_number=extracted_data.get('model_number', original_model_number),
            product_line=extracted_data.get('product_line', ''),
            summary=extracted_data.get('summary', '')
        ).dict()
