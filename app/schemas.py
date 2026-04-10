from datetime import datetime
from typing import Any

from pydantic import BaseModel, ConfigDict, Field


class CompanyPayload(BaseModel):
    id: int
    name: str = Field(min_length=1, max_length=255)
    data: dict[str, Any]


class CompanyResponse(CompanyPayload):
    created_at: datetime | None = None
    updated_at: datetime | None = None
    model_config = ConfigDict(from_attributes=True)


class CompanyListResponse(BaseModel):
    companies: list[CompanyResponse]


class CompanyBulkUpsert(BaseModel):
    companies: list[CompanyPayload]


class HealthResponse(BaseModel):
    status: str
