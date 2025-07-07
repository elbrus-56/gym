import datetime
from uuid import UUID
from pydantic import BaseModel, Field
from typing import Optional


from src.core.enums import TypeEvents


class EventID(BaseModel):
    id: UUID


class EventBase(BaseModel):
    name: TypeEvents = Field(..., description="Тип события")
    competition: UUID = Field(..., description="ID связанного соревнования")
    started_at: datetime.datetime = Field(..., description="Начало события (UTC)")
    completed_at: datetime.datetime = Field(..., description="Завершение события (UTC)")


class EventCreate(EventBase):
    pass


class EventUpdate(BaseModel):
    name: Optional[TypeEvents] = Field(None, description="Тип события")
    competition: Optional[UUID] = Field(None, description="ID связанного соревнования")
    started_at: Optional[datetime.datetime] = Field(
        None, description="Начало события (UTC)"
    )
    completed_at: Optional[datetime.datetime] = Field(
        None, description="Завершение события (UTC)"
    )


class EventResponse(EventBase, EventID):
    created_at: datetime.datetime = Field(..., description="Дата создания записи (UTC)")
    updated_at: datetime.datetime = Field(
        ..., description="Дата обновления записи (UTC)"
    )
