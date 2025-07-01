import datetime
from uuid import UUID
from pydantic import BaseModel, Field
from typing import Optional, Union

from src.core.enums import CompetitionStatus


class CompetitionBase(BaseModel):
    name: str = Field(..., max_length=255)
    location: Optional[str] = Field(None, max_length=255)
    start_date: Optional[datetime.datetime] = Field(None)
    end_date: Optional[datetime.datetime] = Field(None)
    fullname: Optional[str] = Field(None, max_length=255)
    age_from: Optional[str] = Field(None, max_length=10)
    age_to: Optional[str] = Field(None, max_length=10)
    organizer: Optional[str] = Field(None, max_length=255)
    judge: Optional[str] = Field(None, max_length=255)
    info: Optional[str] = Field(None, max_length=255)
    city: Optional[str] = Field(None, max_length=255)
    status: CompetitionStatus = CompetitionStatus.PLANNED
    # skip_pos: bool = False
    # check_ead: bool = False
    # art: bool = False
    # final: bool = False
    # key: Optional[str] = Field(None, max_length=255)
    # parent: Optional[str] = Field(None, max_length=255)
    # logo: Optional[Union[bytes, str]] = None
    # logo_print: bool = False
    # logo_dim: Optional[int] = None
    # team_type: bool = False
    # team_n: bool = False


class CompetitionCreate(CompetitionBase):
    pass


class CompetitionUpdate(CompetitionBase):
    pass


class CompetitionResponse(CompetitionBase):
    id: UUID
    created_at: datetime.datetime
    updated_at: datetime.datetime
    started_at: datetime.datetime | None = None
    completed_at: datetime.datetime | None = None
