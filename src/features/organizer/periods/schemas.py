from datetime import datetime, date as _date
from uuid import UUID
from pydantic import BaseModel, Field
from typing import Optional


class PeriodID(BaseModel):
    id: UUID


class PeriodBase(BaseModel):
    date: Optional[_date] = None
    competition: Optional[UUID] = None
    name: Optional[str] = Field(None, max_length=255)
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    age_from: Optional[str] = Field(None, max_length=10)
    age_to: Optional[str] = Field(None, max_length=10)
    n: Optional[int] = None
    art: bool = False


class PeriodCreate(PeriodBase):
    pass


class PeriodUpdate(PeriodBase):
    pass


class PeriodResponse(PeriodBase, PeriodID):
    created_at: datetime
    updated_at: datetime
