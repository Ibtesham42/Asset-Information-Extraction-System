"""
Web search implementation
"""
import aiohttp
import asyncio
from typing import List, Dict, Any, Optional
from src.config.settings import settings
from src.config.constants import GOOGLE_SEARCH_URL, DEFAULT_TIMEOUT
from src.utils.logger import get_logger

logger = get_logger(__name__)

class SearchService:
    def __init__(self):
        self.api_key = settings.SERPAPI_KEY or settings.GOOGLE_SEARCH_API_KEY
        self.engine_id = settings.GOOGLE_SEARCH_ENGINE_ID
        
    async def build_search_query(self, asset_info: Dict[str, Any]) -> str:
        """Build optimized search query from asset information"""
        parts = [
            asset_info.get("model_number", ""),
            asset_info.get("manufacturer", ""),
            asset_info.get("asset_classification_name", ""),
            "specifications", "datasheet", "product details"
        ]
        query = " ".join(filter(None, parts))
        logger.info(f"Built search query: {query}")
        return query
    
    async def search(self, query: str, num_results: Optional[int] = None) -> List[Dict[str, str]]:
        """Perform web search and return relevant results"""
        if not num_results:
            num_results = settings.MAX_SEARCH_RESULTS
            
        if not self.api_key or not self.engine_id:
            logger.error("Search API credentials not configured")
            return self._get_mock_results(query)
            
        try:
            params = {
                'key': self.api_key,
                'cx': self.engine_id,
                'q': query,
                'num': min(num_results, 10)  # API limit
            }
            
            async with aiohttp.ClientSession() as session:
                async with session.get(
                    GOOGLE_SEARCH_URL,
                    params=params,
                    timeout=DEFAULT_TIMEOUT
                ) as response:
                    if response.status == 200:
                        data = await response.json()
                        results = []
                        for item in data.get('items', []):
                            results.append({
                                'title': item.get('title', ''),
                                'snippet': item.get('snippet', ''),
                                'link': item.get('link', '')
                            })
                        logger.info(f"Found {len(results)} search results")
                        return results
                    else:
                        logger.error(f"Search API error: {response.status}")
                        return self._get_mock_results(query)
                        
        except asyncio.TimeoutError:
            logger.error("Search timeout")
            return self._get_mock_results(query)
        except Exception as e:
            logger.error(f"Search error: {str(e)}")
            return self._get_mock_results(query)
    
    def _get_mock_results(self, query: str) -> List[Dict[str, str]]:
        """Return mock results for testing when API is not configured"""
        logger.warning("Using mock search results")
        return [
            {
                'title': f'Product Information for {query}',
                'snippet': f'The {query} is a high-quality marine generator designed for reliable performance...',
                'link': 'https://example.com/product1'
            },
            {
                'title': f'{query} Specifications and Datasheet',
                'snippet': f'Technical specifications for model {query} including power output, dimensions, and features...',
                'link': 'https://example.com/specs'
            }
        ]
