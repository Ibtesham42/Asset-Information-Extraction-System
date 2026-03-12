"""
Tests for LLM service
"""
import pytest
from src.services.llm_service import LLMService

@pytest.mark.asyncio
async def test_extract_info_with_mock():
    service = LLMService()
    
    search_results = [
        {
            "title": "Product Info",
            "snippet": "The MRN85HD is a marine generator from Cummins",
            "link": "https://example.com"
        }
    ]
    
    original_input = {
        "model_number": "MRN85HD",
        "asset_classification_name": "Marine Generator",
        "manufacturer": ""
    }
    
    result = await service.extract_info(search_results, original_input)
    
    assert result is not None
    assert "manufacturer" in result
    assert "model_number" in result

@pytest.mark.asyncio
async def test_parse_response():
    service = LLMService()
    
    response = '{"asset_classification": "Marine Generator", "manufacturer": "Cummins"}'
    parsed = service._parse_response(response)
    
    assert parsed["asset_classification"] == "Marine Generator"
    assert parsed["manufacturer"] == "Cummins"

if __name__ == "__main__":
    pytest.main([__file__])
