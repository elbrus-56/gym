from datetime import datetime
from uuid import UUID
from pydantic import BaseModel, Field, condecimal
from typing import Optional


class GroupID(BaseModel):
    id: UUID


class GroupBase(BaseModel):
    age_from: Optional[str] = Field(None, max_length=10)
    age_to: Optional[str] = Field(None, max_length=10)
    period: Optional[UUID] = None
    category: Optional[str] = Field(None, max_length=50)
    vid: Optional[str] = Field(None, max_length=50)
    date: Optional[datetime] = None
    hour_from: Optional[str] = Field(None, max_length=10)
    min_from: Optional[str] = Field(None, max_length=10)
    hour_to: Optional[str] = Field(None, max_length=10)
    min_to: Optional[str] = Field(None, max_length=255)
    fullname: Optional[str] = Field(None, max_length=255)
    group: Optional[int] = None
    fullkey: Optional[str] = Field(None, max_length=255)
    wa: Optional[str] = Field(None, max_length=10)
    prog: Optional[str] = Field(None, max_length=255)
    brake_type: Optional[int] = None
    brake_name: Optional[str] = Field(None, max_length=255)
    ex: Optional[int] = None
    sec: Optional[int] = None
    letter: Optional[str] = Field(None, max_length=255)
    v1: Optional[int] = None
    v2: Optional[int] = None
    v3: Optional[int] = None
    v4: Optional[int] = None
    vert: Optional[int] = None
    num_sf: Optional[int] = None
    min_sf: Optional[int] = None
    team_k: Optional[condecimal(max_digits=100, decimal_places=7)] = None  # type: ignore
    max_d: Optional[int] = None
    ofp: bool = False
    ofp_n: int = 0
    ofp_ex1: Optional[str] = Field(None, max_length=255)
    ofp_ex2: Optional[str] = Field(None, max_length=255)
    ofp_ex3: Optional[str] = Field(None, max_length=255)
    ofp_ex4: Optional[str] = Field(None, max_length=255)
    ofp_ex5: Optional[str] = Field(None, max_length=255)
    ofp_ex6: Optional[str] = Field(None, max_length=255)
    ofp_ex7: Optional[str] = Field(None, max_length=255)
    ofp_ex8: Optional[str] = Field(None, max_length=255)
    ofp_ex9: Optional[str] = Field(None, max_length=255)
    ofp_ex10: Optional[str] = Field(None, max_length=255)
    ofp_ex11: Optional[str] = Field(None, max_length=255)
    ofp_ex12: Optional[str] = Field(None, max_length=255)
    ofp_ex13: Optional[str] = Field(None, max_length=255)
    ofp_ex14: Optional[str] = Field(None, max_length=255)
    ofp_ex15: Optional[str] = Field(None, max_length=255)
    est: bool = False
    est_gr: int = 0
    est_short: int = 0
    aer: bool = False
    aer_cat: int = 0
    aer_age: int = 0
    aer_sex: int = 0
    aer_dd_k: Optional[condecimal(max_digits=100, decimal_places=7)] = 0  # type: ignore
    aer_year: Optional[str] = Field(None, max_length=255)
    aer_final: bool = False
    man: bool = False
    man_cat: int = 0
    kat: bool = False
    kat_type: int = 0
    kat_age: int = 0
    kat_sex: int = 0
    kat_ex: int = 0
    kat_name: Optional[str] = Field(None, max_length=255)
    kat_kata_name1: Optional[str] = Field(None, max_length=255)
    kat_kata_name2: Optional[str] = Field(None, max_length=255)
    kat_kata_name3: Optional[str] = Field(None, max_length=255)
    kat_kata_ind1: int = 0
    kat_kata_ind2: int = 0
    kat_kata_ind3: int = 0
    art: bool = False
    art_man: bool = False
    art_age_number: int = 0
    art_age_name: Optional[str] = Field(None, max_length=255)
    art_type: bool = False
    art_grade_number: int = 0
    art_grade_name: Optional[str] = Field(None, max_length=255)
    art_fig: bool = False
    v5: Optional[int] = None
    v6: Optional[int] = None
    group_type: Optional[int] = None
    age_group_num: int = 0
    age_group_name: Optional[str] = Field(None, max_length=255)
    step_name: Optional[str] = Field(None, max_length=255)


class GroupCreate(GroupBase):
    pass


class GroupUpdate(GroupBase):
    pass


class GroupResponse(GroupBase, GroupID):
    created_at: datetime
    updated_at: datetime
