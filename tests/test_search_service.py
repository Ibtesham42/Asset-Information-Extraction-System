"""
Tests for search service
"""
import pytest
import asyncio
from src.services.search_service import SearchService

@pytest.mark.asyncio
async def test_build_search_query():
    service = SearchService()
    asset_info = {
        "model_number": "MRN85HD",
        "manufacturer": "Cummins",
        "asset_classification_name": "Marine Generator"
    }
    
    query = await service.build_search_query(asset_info)
    assert "MRN85HD" in query
    assert "Cummins" in query
    assert "Marine Generator" in query

@pytest.mark.asyncio
async def test_search_with_mock():
    service = SearchService()
    results = await service.search("test query", num_results=2)
    
    assert isinstance(results, list)
    assert len(results) > 0
    assert "title" in results[0]
    assert "snippet" in results[0]

if __name__ == "__main__":
    pytest.main([__file__])
