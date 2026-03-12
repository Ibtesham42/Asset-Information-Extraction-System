import aiohttp
import asyncio
from typing import List, Dict, Any, Optional
from src.config.settings import settings
from src.utils.logger import get_logger

logger = get_logger(__name__)

class SearchService:
    def __init__(self):
        # Serper.dev key
        self.serper_key = settings.SERPAPI_KEY  # Variable name same rahega
        
    async def build_search_query(self, asset_info: Dict[str, Any]) -> str:
        """Build optimized search query"""
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
        """Serper.dev se search karo"""
        if not num_results:
            num_results = settings.MAX_SEARCH_RESULTS
            
        if not self.serper_key:
            logger.error("SERPER.DEV key not configured")
            return self._get_mock_results(query)
        
        try:
            # Serper.dev API endpoint
            url = "https://google.serper.dev/search"
            
            # Headers - Serper.dev uses Bearer token
            headers = {
                'X-API-KEY': self.serper_key,
                'Content-Type': 'application/json'
            }
            
            # Payload - Serper.dev ka format
            payload = {
                'q': query,
                'num': num_results,
                'gl': 'us',
                'hl': 'en'
            }
            
            logger.info(f"Calling Serper.dev with query: {query}")
            
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    url,
                    headers=headers,
                    json=payload,
                    timeout=settings.SEARCH_TIMEOUT_SECONDS
                ) as response:
                    
                    if response.status == 200:
                        data = await response.json()
                        results = []
                        
                        # Serper.dev response structure
                        organic = data.get('organic', [])
                        for item in organic[:num_results]:
                            results.append({
                                'title': item.get('title', ''),
                                'snippet': item.get('snippet', ''),
                                'link': item.get('link', '')
                            })
                        
                        logger.info(f"Found {len(results)} search results from Serper.dev")
                        return results
                    else:
                        error_text = await response.text()
                        logger.error(f"Serper.dev error: {response.status} - {error_text}")
                        return self._get_mock_results(query)
                        
        except asyncio.TimeoutError:
            logger.error("Serper.dev timeout")
            return self._get_mock_results(query)
        except Exception as e:
            logger.error(f"Serper.dev search error: {str(e)}")
            return self._get_mock_results(query)
    
    def _get_mock_results(self, query: str) -> List[Dict[str, str]]:
        """Mock results for testing"""
        logger.warning("Using mock search results")
        return [
            {
                'title': f'Product Information for {query}',
                'snippet': f'The {query} is industrial equipment designed for reliable performance.',
                'link': 'https://example.com/product'
            }
        ]