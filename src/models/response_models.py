"""
Pydantic models for output validation
"""
from pydantic import BaseModel, Field
from typing import Optional

class AssetResponse(BaseModel):
    asset_classification: str = Field(..., description="Extracted asset classification")
    manufacturer: str = Field(..., description="Extracted manufacturer")
    model_number: str = Field(..., description="Model number (original or extracted)")
    product_line: str = Field("", description="Extracted product line")
    summary: str = Field(..., description="Product summary")
    
    class Config:
        protected_namespaces = ()
        json_schema_extra = {
            "example": {
                "asset_classification": "Marine Generator",
                "manufacturer": "Cummins",
                "model_number": "MRN85HD",
                "product_line": "Onan",
                "summary": "The Cummins MRN85HD is a Marine Generator..."
            }
        }

class FallbackResponse(BaseModel):
    asset_classification: str = "Generator Emissions/UREA/DPF Systems"
    manufacturer: str = ""
    model_number: str
    product_line: str = ""
    summary: str = "Information could not be retrieved at this time."
