from datetime import datetime
from uuid import UUID
from pydantic import BaseModel, Field
from typing import Optional


class FlowID(BaseModel):
    id: UUID


class FlowBase(BaseModel):
    group: Optional[UUID] = None
    hour_from: Optional[str] = Field(None, max_length=10)
    min_from: Optional[str] = Field(None, max_length=10)
    hour_to: Optional[str] = Field(None, max_length=10)
    min_to: Optional[str] = Field(None, max_length=10)
    fullname: Optional[str] = Field(None, max_length=255)
    name: Optional[str] = Field(None, max_length=255)
    fullkey: Optional[str] = Field(None, max_length=255)
    brake_name: Optional[str] = Field(None, max_length=255)
    brake_type: Optional[int] = None


class FlowCreate(FlowBase):
    pass


class FlowUpdate(FlowBase):
    pass


class FlowResponse(FlowBase, FlowID):
    created_at: datetime
    updated_at: datetime
