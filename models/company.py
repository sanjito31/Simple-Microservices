from __future__ import annotations

from typing import Optional
from uuid import UUID, uuid4
from datetime import datetime
from pydantic import BaseModel, Field



class CompanyBase(BaseModel):
    """Base model definition for a company."""
    id: UUID = Field(
        default_factory=uuid4,
        description="Persistent Company ID (server-generated)",
        json_schema_extra={"example": "550e8400-e29b-41d4-a716-446655440000"}
    )
    name: str = Field(
        ...,
        description="Name of the company.",
        json_schema_extra={"example": "Major Company Inc."}
    )
    industry: str = Field(
        ...,
        description="Industry that the company is a part of.",
        json_schema_extra={"example": "Aerospace"}
    )
    employees: int = Field(
        ...,
        description="Number of current employees.",
        json_schema_extra={"example": 400}
    )
    phone: str = Field(
        ...,
        description="The public phone number of the company.",
        json_schema_extra={"example": "555-555-5555"}
    )
    state: str = Field(
        ...,
        description="State where the company is headquarted or based.",
        json_schema_extra={"example": "New York"}
    )

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "id": "550e8400-e29b-41d4-a716-446655440000",
                    "name": "Major Company Inc.",
                    "industry": "Aerospace",
                    "employees": 400,
                    "phone": "555-555-5555",
                    "state": "New York"
                }
            ]
        }
    }

class CompanyCreate(CompanyBase):
    """Creation payload for company"""
    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "id": "550e8400-e29b-41d4-a716-446655440000",
                    "name": "Empire Taxi Company",
                    "industry": "Transportation",
                    "employees": 200,
                    "phone": "212-555-1000",
                    "state": "New York"
                }
            ]
        }
    }

class CompanyUpdate(BaseModel):
    """Partial update of company; ID is taken from path"""
    name: Optional[str] = Field(
        ...,
        description="Name of the company.",
        json_schema_extra={"example": "Major Company Inc."}
    )
    industry: Optional[str] = Field(
        ...,
        description="Industry that the company is a part of.",
        json_schema_extra={"example": "Aerospace"}
    )
    employees: Optional[int] = Field(
        ...,
        description="Number of current employees.",
        json_schema_extra={"example": 400}
    )
    phone: Optional[str] = Field(
        ...,
        description="The public phone number of the company.",
        json_schema_extra={"example": "555-555-5555"}
    )
    state: Optional[str] = Field(
        ...,
        description="State where the company is headquarted or based.",
        json_schema_extra={"example": "New York"}
    )

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "id": "550e8400-e29b-41d4-a716-446655440000",
                    "name": "Major Company Inc.",
                    "industry": "Aerospace",
                    "employees": 400,
                    "phone": "555-555-5555",
                    "state": "New York"
                },
                {"employees": 450},
            ]
        }
    }

class CompanyRead(CompanyBase):
    created_at: datetime = Field(
        default_factory=datetime.utcnow,
        description="Creation timestamp (UTC).",
        json_schema_extra={"example": "2025-01-15T10:20:30Z"},
    )
    updated_at: datetime = Field(
        default_factory=datetime.utcnow,
        description="Last update timestamp (UTC).",
        json_schema_extra={"example": "2025-01-16T12:00:00Z"},
    )
    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "id": "550e8400-e29b-41d4-a716-446655440000",
                    "name": "Major Company Inc.",
                    "industry": "Aerospace",
                    "employees": 400,
                    "phone": "555-555-5555",
                    "state": "New York",
                    "created_at": "2025-01-15T10:20:30Z",
                    "updated_at": "2025-01-16T12:00:00Z",
                }
            ]
        }
    }