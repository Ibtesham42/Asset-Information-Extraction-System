"""
Tests for extraction service
"""
import pytest
from src.services.extraction_service import ExtractionService
from src.models.request_models import AssetRequest

@pytest.mark.asyncio
async def test_extract_asset_info():
    service = ExtractionService()
    
    request = AssetRequest(
        model_number="MRN85HD",
        asset_classification_name="Marine Generator",
        manufacturer=""
    )
    
    result = await service.extract_asset_info(request)
    
    assert result is not None
    assert "asset_classification" in result
    assert "manufacturer" in result
    assert "model_number" in result
    assert result["model_number"] == "MRN85HD"

@pytest.mark.asyncio
async def test_fallback_response():
    service = ExtractionService()
    
    # Test with invalid data to trigger fallback
    request = AssetRequest(
        model_number="INVALID123",
        asset_classification_name="Unknown",
        manufacturer=""
    )
    
    result = await service.extract_asset_info(request)
    
    assert result["asset_classification"] == "Generator Emissions/UREA/DPF Systems"
    assert result["model_number"] == "INVALID123"

if __name__ == "__main__":
    pytest.main([__file__])
