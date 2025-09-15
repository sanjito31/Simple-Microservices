from __future__ import annotations

from typing import Optional
from uuid import UUID, uuid4
from datetime import datetime
from pydantic import BaseModel, Field


class ProductBase(BaseModel):
    """Base model for a product to be used in an inventory system, for example"""
    id: UUID = Field(
        default_factory=uuid4,
        description="Persistent Address ID (server-generated).",
        json_schema_extra={"example": "550e8400-e29b-41d4-a716-446655440000"},
    )
    name: str = Field(
        ...,
        description="Name of the product",
        json_schema_extra={"example": "Toaster"},
    )
    description: Optional[str] = Field(
        None,
        description="A short description of the product.",
        json_schema_extra={"example": "A kitchen appliance used to toast bread."}
    )
    price: float = Field(
        ...,
        description="The price in US Dollars for the item.",
        json_schema_extra={"example": 24.99}
    )
    quantity: int = Field(
        ...,
        description="The number of items in stock.",
        json_schema_extra={"example": 35}
    )
    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "id": "550e8400-e29b-41d4-a716-446655440000",
                    "name": "Toaster",
                    "description": "A kitchen appliance used to toast bread.",
                    "price": 24.99,
                    "quantity": 35
                }
            ]
        }
    }
    
class ProductCreate(ProductBase):
    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "id": "550e8400-e29b-41d4-a716-446655440000",
                    "name": "Bag",
                    "description": None,
                    "price": 24.99,
                    "quantity": 1,
                }
            ]
        }
    }

class ProductUpdate(BaseModel):
    """Update the product."""
    name: Optional[str] = Field(
        None,
        description="Name of the product",
        json_schema_extra={"example": "Toaster"},
    )
    description: Optional[str] = Field(
        None,
        description="A short description of the product.",
        json_schema_extra={"example": "A kitchen appliance used to toast bread."}
    )
    price: Optional[float] = Field(
        None,
        description="The price in US Dollars for the item.",
        json_schema_extra={"example": "24.99"}
    )
    quantity: Optional[int] = Field(
        None,
        description="The number of items in stock.",
        json_schema_extra={"example": "35"}
    )
    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "name": "Toaster",
                    "description": "A kitchen appliance used to toast bread.",
                    "price": 24.99,
                    "quantity": 35,
                },
                {"price": 19.99},
            ]
        }
    }

class ProductRead(ProductBase):
    """Read the product and get updated and created at times."""
    created_at: datetime = Field(
        default_factory=datetime.utcnow,
        description="Creation timestamp (UTC).",
        json_schema_extra={"example": "2025-09-10T14:19:00Z"},
    )
    updated_at: datetime = Field(
        default_factory=datetime.utcnow,
        description="Last update timestamp (UTC).",
        json_schema_extra={"example": "2025-09-14T01:00:00Z"},
    )
    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "id": "550e8400-e29b-41d4-a716-446655440000",
                    "name": "Toaster",
                    "description": "A kitchen appliance used to toast bread.",
                    "price": 24.99,
                    "quantity": 35,
                    "created_at": "2025-09-10T14:19:00Z",
                    "updated_at": "2025-09-14T01:00:00Z",
                }
            ]
        }
    }