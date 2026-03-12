"""
Pydantic models for input validation
"""
from pydantic import BaseModel, Field
from typing import Optional

class AssetRequest(BaseModel):
    model_number: str = Field(..., description="Product model number")
    asset_classification_name: str = Field(..., description="Asset classification name")
    manufacturer: Optional[str] = Field("", description="Manufacturer name")
    asset_classification_guid2: Optional[str] = Field("", description="Asset classification GUID")
    
    class Config:
        json_schema_extra = {
            "example": {
                "model_number": "MRN85HD",
                "asset_classification_name": "Generator (Marine)",
                "manufacturer": "",
                "asset_classification_guid2": ""
            }
        }
