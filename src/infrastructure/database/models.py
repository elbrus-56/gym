from datetime import datetime
from typing import Optional
import uuid

from sqlalchemy import (
    CHAR,
    UUID,
    Boolean,
    Column,
    DateTime,
    Enum,
    Float,
    ForeignKey,
    Integer,
    String,
)
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.orm import DeclarativeBase

from src.core.enums import CompetitionStatus, SessionStatus
from sqlalchemy import Column, String, DateTime, Enum, func
from sqlalchemy.dialects.postgresql import UUID as PostgresUUID
from datetime import datetime, timezone
import uuid
from sqlalchemy import (
    Integer,
    String,
    SmallInteger,
    Numeric,
    Boolean,
    DateTime,
    ForeignKey,
    Index,
)
from sqlalchemy.orm import DeclarativeBase, mapped_column, Mapped, relationship


class Base(AsyncAttrs, DeclarativeBase):
    pass


class Competition(Base):
    __tablename__ = "competitions"

    id: Mapped[UUID] = mapped_column(PostgresUUID, primary_key=True, default=uuid.uuid4)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    location: Mapped[Optional[str]] = mapped_column(String(255))
    start_date: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True))
    end_date: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True))
    full_name: Mapped[Optional[str]] = mapped_column(String(255))
    age_from: Mapped[Optional[str]] = mapped_column(String(10))
    age_to: Mapped[Optional[str]] = mapped_column(String(10))
    organizer: Mapped[Optional[str]] = mapped_column(String(255))
    judge: Mapped[Optional[str]] = mapped_column(String(255))
    info: Mapped[Optional[str]] = mapped_column(String(255))
    city: Mapped[Optional[str]] = mapped_column(String(255))
    status: Mapped[CompetitionStatus] = mapped_column(
        Enum(CompetitionStatus), default=CompetitionStatus.PLANNED
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc)
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )
    started_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True))
    completed_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True))
    skip_pos = Column(Boolean, default=False)
    check_ead = Column(Boolean, default=False)
    art = Column(Boolean, default=False)
    final = Column(Boolean, default=False)
    team_type = Column(Boolean, default=False)
    team_n = Column(Boolean, default=False)


class Period(Base):
    __tablename__ = "periods"

    id: Mapped[UUID] = mapped_column(PostgresUUID, primary_key=True, default=uuid.uuid4)
    value: Mapped[Optional[str]] = mapped_column(String(20))
    competition: Mapped[Optional[UUID]] = mapped_column(
        PostgresUUID,
        ForeignKey("competitions.id", ondelete="CASCADE", onupdate="CASCADE"),
    )
    name: Mapped[Optional[str]] = mapped_column(String(255))
    hour_from: Mapped[Optional[str]] = mapped_column(String(10))
    min_from: Mapped[Optional[str]] = mapped_column(String(10))
    hour_to: Mapped[Optional[str]] = mapped_column(String(10))
    min_to: Mapped[Optional[str]] = mapped_column(String(10))
    age_from: Mapped[Optional[str]] = mapped_column(String(10))
    age_to: Mapped[Optional[str]] = mapped_column(String(10))
    fullkey: Mapped[Optional[str]] = mapped_column(String(255))
    n: Mapped[Optional[int]] = mapped_column(SmallInteger)
    art: Mapped[bool] = mapped_column(Boolean, default=False)


class Group(Base):
    __tablename__ = "groups"

    id: Mapped[uuid.UUID] = mapped_column(
        PostgresUUID, primary_key=True, default=uuid.uuid4
    )
    age_from: Mapped[Optional[str]] = mapped_column(String(10))
    age_to: Mapped[Optional[str]] = mapped_column(String(10))
    period: Mapped[Optional[UUID]] = mapped_column(
        PostgresUUID,
        ForeignKey("periods.id", ondelete="CASCADE", onupdate="CASCADE"),
    )
    category: Mapped[Optional[str]] = mapped_column(String(50))
    vid: Mapped[Optional[str]] = mapped_column(String(50))
    date: Mapped[Optional[DateTime]] = mapped_column(DateTime(timezone=True))
    hour_from: Mapped[Optional[str]] = mapped_column(String(10))
    min_from: Mapped[Optional[str]] = mapped_column(String(10))
    hour_to: Mapped[Optional[str]] = mapped_column(String(10))
    min_to: Mapped[Optional[str]] = mapped_column(String(255))
    fullname: Mapped[Optional[str]] = mapped_column(String(255))
    group: Mapped[Optional[int]] = mapped_column(SmallInteger)
    fullkey: Mapped[Optional[str]] = mapped_column(String(255))
    wa: Mapped[Optional[str]] = mapped_column(String(10))
    prog: Mapped[Optional[str]] = mapped_column(String(255))
    brake_type: Mapped[Optional[int]] = mapped_column(SmallInteger)
    brake_name: Mapped[Optional[str]] = mapped_column(String(255))
    ex: Mapped[Optional[int]] = mapped_column(Integer)
    sec: Mapped[Optional[int]] = mapped_column(Integer)
    letter: Mapped[Optional[str]] = mapped_column(String(255))
    v1: Mapped[Optional[int]] = mapped_column(SmallInteger)
    v2: Mapped[Optional[int]] = mapped_column(SmallInteger)
    v3: Mapped[Optional[int]] = mapped_column(SmallInteger)
    v4: Mapped[Optional[int]] = mapped_column(SmallInteger)
    vert: Mapped[Optional[int]] = mapped_column(SmallInteger)
    num_sf: Mapped[Optional[int]] = mapped_column(SmallInteger)
    min_sf: Mapped[Optional[int]] = mapped_column(SmallInteger)
    team_k: Mapped[Optional[Numeric]] = mapped_column(Numeric(precision=100, scale=7))
    max_d: Mapped[Optional[int]] = mapped_column(Integer)
    ofp: Mapped[Optional[bool]] = mapped_column(Boolean, default=False)
    ofp_n: Mapped[Optional[int]] = mapped_column(SmallInteger, default=0)
    ofp_ex1: Mapped[Optional[str]] = mapped_column(String(255))
    ofp_ex2: Mapped[Optional[str]] = mapped_column(String(255))
    ofp_ex3: Mapped[Optional[str]] = mapped_column(String(255))
    ofp_ex4: Mapped[Optional[str]] = mapped_column(String(255))
    ofp_ex5: Mapped[Optional[str]] = mapped_column(String(255))
    ofp_ex6: Mapped[Optional[str]] = mapped_column(String(255))
    ofp_ex7: Mapped[Optional[str]] = mapped_column(String(255))
    ofp_ex8: Mapped[Optional[str]] = mapped_column(String(255))
    ofp_ex9: Mapped[Optional[str]] = mapped_column(String(255))
    ofp_ex10: Mapped[Optional[str]] = mapped_column(String(255))
    ofp_ex11: Mapped[Optional[str]] = mapped_column(String(255))
    ofp_ex12: Mapped[Optional[str]] = mapped_column(String(255))
    ofp_ex13: Mapped[Optional[str]] = mapped_column(String(255))
    ofp_ex14: Mapped[Optional[str]] = mapped_column(String(255))
    ofp_ex15: Mapped[Optional[str]] = mapped_column(String(255))
    est: Mapped[Optional[bool]] = mapped_column(Boolean, default=False)
    est_gr: Mapped[Optional[int]] = mapped_column(SmallInteger, default=0)
    est_short: Mapped[Optional[int]] = mapped_column(SmallInteger, default=0)
    aer: Mapped[Optional[bool]] = mapped_column(Boolean, default=False)
    aer_cat: Mapped[Optional[int]] = mapped_column(SmallInteger, default=0)
    aer_age: Mapped[Optional[int]] = mapped_column(SmallInteger, default=0)
    aer_sex: Mapped[Optional[int]] = mapped_column(SmallInteger, default=0)
    aer_dd_k: Mapped[Optional[Numeric]] = mapped_column(
        Numeric(precision=100, scale=7), default=0
    )
    aer_year: Mapped[Optional[str]] = mapped_column(String(255))
    aer_final: Mapped[Optional[bool]] = mapped_column(Boolean, default=False)
    man: Mapped[Optional[bool]] = mapped_column(Boolean, default=False)
    man_cat: Mapped[Optional[int]] = mapped_column(SmallInteger, default=0)
    kat: Mapped[Optional[bool]] = mapped_column(Boolean, default=False)
    kat_type: Mapped[Optional[int]] = mapped_column(SmallInteger, default=0)
    kat_age: Mapped[Optional[int]] = mapped_column(SmallInteger, default=0)
    kat_sex: Mapped[Optional[int]] = mapped_column(SmallInteger, default=0)
    kat_ex: Mapped[Optional[int]] = mapped_column(SmallInteger, default=0)
    kat_name: Mapped[Optional[str]] = mapped_column(String(255))
    kat_kata_name1: Mapped[Optional[str]] = mapped_column(String(255))
    kat_kata_name2: Mapped[Optional[str]] = mapped_column(String(255))
    kat_kata_name3: Mapped[Optional[str]] = mapped_column(String(255))
    kat_kata_ind1: Mapped[Optional[int]] = mapped_column(SmallInteger, default=0)
    kat_kata_ind2: Mapped[Optional[int]] = mapped_column(SmallInteger, default=0)
    kat_kata_ind3: Mapped[Optional[int]] = mapped_column(SmallInteger, default=0)
    art: Mapped[Optional[bool]] = mapped_column(Boolean, default=False)
    art_man: Mapped[Optional[bool]] = mapped_column(Boolean, default=False)
    art_age_number: Mapped[Optional[int]] = mapped_column(Integer, default=0)
    art_age_name: Mapped[Optional[str]] = mapped_column(String(255))
    art_type: Mapped[Optional[bool]] = mapped_column(Boolean, default=False)
    art_grade_number: Mapped[Optional[int]] = mapped_column(Integer, default=0)
    art_grade_name: Mapped[Optional[str]] = mapped_column(String(255))
    art_fig: Mapped[Optional[bool]] = mapped_column(Boolean, default=False)
    v5: Mapped[Optional[int]] = mapped_column(SmallInteger)
    v6: Mapped[Optional[int]] = mapped_column(SmallInteger)
    group_type: Mapped[Optional[int]] = mapped_column(SmallInteger)
    age_group_num: Mapped[Optional[int]] = mapped_column(SmallInteger, default=0)
    age_group_name: Mapped[Optional[str]] = mapped_column(String(255))
    step_name: Mapped[Optional[str]] = mapped_column(String(255))


class Flow(Base):
    __tablename__ = "flows"

    id: Mapped[UUID] = mapped_column(PostgresUUID, primary_key=True, default=uuid.uuid4)
    group: Mapped[Optional[UUID]] = mapped_column(
        PostgresUUID,
        ForeignKey("groups.id", ondelete="CASCADE", onupdate="CASCADE"),
    )
    hour_from: Mapped[Optional[str]] = mapped_column(String(10))
    min_from: Mapped[Optional[str]] = mapped_column(String(10))
    hour_to: Mapped[Optional[str]] = mapped_column(String(10))
    min_to: Mapped[Optional[str]] = mapped_column(String(10))
    fullname: Mapped[Optional[str]] = mapped_column(String(255))
    name: Mapped[Optional[str]] = mapped_column(String(255))
    fullkey: Mapped[Optional[str]] = mapped_column(String(255))
    brake_name: Mapped[Optional[str]] = mapped_column(String(255))
    brake_type: Mapped[Optional[int]] = mapped_column(SmallInteger)


class Judge(Base):
    __tablename__ = "judges"

    id: Mapped[UUID] = mapped_column(PostgresUUID, primary_key=True, default=uuid.uuid4)
    competition: Mapped[Optional[UUID]] = mapped_column(
        PostgresUUID,
        ForeignKey("competitions.id", ondelete="CASCADE", onupdate="CASCADE"),
    )
    name: Mapped[Optional[str]] = mapped_column(String(255))
    grade: Mapped[Optional[str]] = mapped_column(String(255))
    category: Mapped[Optional[str]] = mapped_column(String(255))
    city: Mapped[Optional[str]] = mapped_column(String(255))
    sign: Mapped[bool] = mapped_column(Boolean, default=False)
    region: Mapped[Optional[str]] = mapped_column(String(255))
    pos: Mapped[int] = mapped_column(SmallInteger, default=0)
    rank: Mapped[Optional[str]] = mapped_column(String(255))


class Athlete(Base):
    __tablename__ = "athletes"

    id: Mapped[UUID] = mapped_column(PostgresUUID, primary_key=True, default=uuid.uuid4)
    flow: Mapped[Optional[UUID]] = mapped_column(
        PostgresUUID,
        ForeignKey("flows.id", ondelete="CASCADE"),
    )
    name: Mapped[Optional[str]] = mapped_column(String(255))
    dob: Mapped[Optional[str]] = mapped_column(String(255))
    category: Mapped[Optional[str]] = mapped_column(String(255))
    city: Mapped[Optional[str]] = mapped_column(String(255))
    team: Mapped[Optional[str]] = mapped_column(String(255))
    coach: Mapped[Optional[str]] = mapped_column(String(255))
    is_group: Mapped[Optional[int]] = mapped_column(Integer)
    fullkey: Mapped[Optional[str]] = mapped_column(String(255))
    start_n: Mapped[Optional[int]] = mapped_column(Integer)
    pos: Mapped[Optional[int]] = mapped_column(Integer)
    result: Mapped[Optional[Numeric]] = mapped_column(Numeric(100, 7), default=0.0)
    result_v1: Mapped[Optional[Numeric]] = mapped_column(Numeric(100, 7), default=0.0)
    result_v2: Mapped[Optional[Numeric]] = mapped_column(Numeric(100, 7), default=0.0)
    result_v3: Mapped[Optional[Numeric]] = mapped_column(Numeric(100, 7), default=0.0)
    result_v4: Mapped[Optional[Numeric]] = mapped_column(Numeric(100, 7), default=0.0)
    result_v5: Mapped[Optional[Numeric]] = mapped_column(Numeric(100, 7), default=0.0)
    result_v6: Mapped[Optional[Numeric]] = mapped_column(Numeric(100, 7), default=0.0)
    result_v7: Mapped[Optional[Numeric]] = mapped_column(Numeric(100, 7), default=0.0)
    pos_v1: Mapped[Optional[int]] = mapped_column(Integer)
    pos_v2: Mapped[Optional[int]] = mapped_column(Integer)
    pos_v3: Mapped[Optional[int]] = mapped_column(Integer)
    pos_v4: Mapped[Optional[int]] = mapped_column(Integer)
    pos_v5: Mapped[Optional[int]] = mapped_column(Integer)
    pos_v6: Mapped[Optional[int]] = mapped_column(Integer)
    pos_v7: Mapped[Optional[int]] = mapped_column(Integer)
    subresult: Mapped[Optional[Numeric]] = mapped_column(Numeric(100, 7), default=0.0)
    penalty: Mapped[Optional[Numeric]] = mapped_column(Numeric(100, 7), default=0.0)
    post: Mapped[Optional[str]] = mapped_column(String(255))
    v1: Mapped[Optional[int]] = mapped_column(Integer)
    v2: Mapped[Optional[int]] = mapped_column(Integer)
    v3: Mapped[Optional[int]] = mapped_column(Integer)
    v4: Mapped[Optional[int]] = mapped_column(Integer)
    checked: Mapped[bool] = mapped_column(Boolean, default=False)
    music_1: Mapped[Optional[str]] = mapped_column(String(255))
    music_2: Mapped[Optional[str]] = mapped_column(String(255))
    music_3: Mapped[Optional[str]] = mapped_column(String(255))
    music_4: Mapped[Optional[str]] = mapped_column(String(255))
    music_5: Mapped[Optional[str]] = mapped_column(String(255))
    music_6: Mapped[Optional[str]] = mapped_column(String(255))
    music_7: Mapped[Optional[str]] = mapped_column(String(255))
    performed: Mapped[bool] = mapped_column(Boolean, default=True)
    ofp: Mapped[bool] = mapped_column(Boolean, default=False)
    result_ofp1: Mapped[Optional[Numeric]] = mapped_column(Numeric(100, 7), default=0.0)
    result_ofp2: Mapped[Optional[Numeric]] = mapped_column(Numeric(100, 7), default=0.0)
    result_ofp3: Mapped[Optional[Numeric]] = mapped_column(Numeric(100, 7), default=0.0)
    result_ofp4: Mapped[Optional[Numeric]] = mapped_column(Numeric(100, 7), default=0.0)
    result_ofp5: Mapped[Optional[Numeric]] = mapped_column(Numeric(100, 7), default=0.0)
    result_ofp6: Mapped[Optional[Numeric]] = mapped_column(Numeric(100, 7), default=0.0)
    result_ofp7: Mapped[Optional[Numeric]] = mapped_column(Numeric(100, 7), default=0.0)
    result_ofp8: Mapped[Optional[Numeric]] = mapped_column(Numeric(100, 7), default=0.0)
    result_ofp9: Mapped[Optional[Numeric]] = mapped_column(Numeric(100, 7), default=0.0)
    result_ofp10: Mapped[Optional[Numeric]] = mapped_column(
        Numeric(100, 7), default=0.0
    )
    result_ofp11: Mapped[Optional[Numeric]] = mapped_column(
        Numeric(100, 7), default=0.0
    )
    result_ofp12: Mapped[Optional[Numeric]] = mapped_column(
        Numeric(100, 7), default=0.0
    )
    result_ofp13: Mapped[Optional[Numeric]] = mapped_column(
        Numeric(100, 7), default=0.0
    )
    result_ofp14: Mapped[Optional[Numeric]] = mapped_column(
        Numeric(100, 7), default=0.0
    )
    result_ofp15: Mapped[Optional[Numeric]] = mapped_column(
        Numeric(100, 7), default=0.0
    )
    result_est_tv: Mapped[Optional[Numeric]] = mapped_column(
        Numeric(100, 7), default=0.0
    )
    result_est_av: Mapped[Optional[Numeric]] = mapped_column(
        Numeric(100, 7), default=0.0
    )
    result_est_ex: Mapped[Optional[Numeric]] = mapped_column(
        Numeric(100, 7), default=0.0
    )
    result_est_pred: Mapped[Optional[Numeric]] = mapped_column(
        Numeric(100, 7), default=0.0
    )
    result_est_pred_pos: Mapped[Optional[Numeric]] = mapped_column(
        Numeric(100, 7), default=0.0
    )
    result_est_tv_f: Mapped[Optional[Numeric]] = mapped_column(
        Numeric(100, 7), default=0.0
    )
    result_est_av_f: Mapped[Optional[Numeric]] = mapped_column(
        Numeric(100, 7), default=0.0
    )
    result_est_ex_f: Mapped[Optional[Numeric]] = mapped_column(
        Numeric(100, 7), default=0.0
    )
    result_est_final: Mapped[Optional[Numeric]] = mapped_column(
        Numeric(100, 7), default=0.0
    )
    result_est_final_pos: Mapped[Optional[Numeric]] = mapped_column(
        Numeric(100, 7), default=0.0
    )
    est: Mapped[bool] = mapped_column(Boolean, default=False)
    aer: Mapped[bool] = mapped_column(Boolean, default=False)
    result_aer_e1: Mapped[Optional[Numeric]] = mapped_column(
        Numeric(100, 7), default=0.0
    )
    result_aer_e2: Mapped[Optional[Numeric]] = mapped_column(
        Numeric(100, 7), default=0.0
    )
    result_aer_e3: Mapped[Optional[Numeric]] = mapped_column(
        Numeric(100, 7), default=0.0
    )
    result_aer_e4: Mapped[Optional[Numeric]] = mapped_column(
        Numeric(100, 7), default=0.0
    )
    result_aer_e5: Mapped[Optional[Numeric]] = mapped_column(
        Numeric(100, 7), default=0.0
    )
    result_aer_e6: Mapped[Optional[Numeric]] = mapped_column(
        Numeric(100, 7), default=0.0
    )
    result_aer_a1: Mapped[Optional[Numeric]] = mapped_column(
        Numeric(100, 7), default=0.0
    )
    result_aer_a2: Mapped[Optional[Numeric]] = mapped_column(
        Numeric(100, 7), default=0.0
    )
    result_aer_a3: Mapped[Optional[Numeric]] = mapped_column(
        Numeric(100, 7), default=0.0
    )
    result_aer_a4: Mapped[Optional[Numeric]] = mapped_column(
        Numeric(100, 7), default=0.0
    )
    result_aer_a5: Mapped[Optional[Numeric]] = mapped_column(
        Numeric(100, 7), default=0.0
    )
    result_aer_a6: Mapped[Optional[Numeric]] = mapped_column(
        Numeric(100, 7), default=0.0
    )
    result_aer_d1d2: Mapped[Optional[Numeric]] = mapped_column(
        Numeric(100, 7), default=0.0
    )
    penalty_aer_dd: Mapped[Optional[Numeric]] = mapped_column(
        Numeric(100, 7), default=0.0
    )
    penalty_aer_cjp: Mapped[Optional[Numeric]] = mapped_column(
        Numeric(100, 7), default=0.0
    )
    penalty_aer_l: Mapped[Optional[Numeric]] = mapped_column(
        Numeric(100, 7), default=0.0
    )
    result_aer_e: Mapped[Optional[Numeric]] = mapped_column(
        Numeric(100, 7), default=0.0
    )
    result_aer_a: Mapped[Optional[Numeric]] = mapped_column(
        Numeric(100, 7), default=0.0
    )
    result_aer_d: Mapped[Optional[Numeric]] = mapped_column(
        Numeric(100, 7), default=0.0
    )
    penalty_aer: Mapped[Optional[Numeric]] = mapped_column(Numeric(100, 7), default=0.0)
    result_aer: Mapped[Optional[Numeric]] = mapped_column(Numeric(100, 7), default=0.0)
    total_d: Mapped[Optional[Numeric]] = mapped_column(Numeric(100, 7), default=0.0)
    total_a: Mapped[Optional[Numeric]] = mapped_column(Numeric(100, 7), default=0.0)
    total_e: Mapped[Optional[Numeric]] = mapped_column(Numeric(100, 7), default=0.0)
    total_d_v1: Mapped[Optional[Numeric]] = mapped_column(Numeric(100, 7), default=0.0)
    total_d_v2: Mapped[Optional[Numeric]] = mapped_column(Numeric(100, 7), default=0.0)
    total_d_v3: Mapped[Optional[Numeric]] = mapped_column(Numeric(100, 7), default=0.0)
    total_d_v4: Mapped[Optional[Numeric]] = mapped_column(Numeric(100, 7), default=0.0)
    total_d_v5: Mapped[Optional[Numeric]] = mapped_column(Numeric(100, 7), default=0.0)
    total_d_v6: Mapped[Optional[Numeric]] = mapped_column(Numeric(100, 7), default=0.0)
    total_d_v7: Mapped[Optional[Numeric]] = mapped_column(Numeric(100, 7), default=0.0)
    total_a_v1: Mapped[Optional[Numeric]] = mapped_column(Numeric(100, 7), default=0.0)
    total_a_v2: Mapped[Optional[Numeric]] = mapped_column(Numeric(100, 7), default=0.0)
    total_a_v3: Mapped[Optional[Numeric]] = mapped_column(Numeric(100, 7), default=0.0)
    total_a_v4: Mapped[Optional[Numeric]] = mapped_column(Numeric(100, 7), default=0.0)
    total_a_v5: Mapped[Optional[Numeric]] = mapped_column(Numeric(100, 7), default=0.0)
    total_a_v6: Mapped[Optional[Numeric]] = mapped_column(Numeric(100, 7), default=0.0)
    total_a_v7: Mapped[Optional[Numeric]] = mapped_column(Numeric(100, 7), default=0.0)
    total_e_v1: Mapped[Optional[Numeric]] = mapped_column(Numeric(100, 7), default=0.0)
    total_e_v2: Mapped[Optional[Numeric]] = mapped_column(Numeric(100, 7), default=0.0)
    total_e_v3: Mapped[Optional[Numeric]] = mapped_column(Numeric(100, 7), default=0.0)
    total_e_v4: Mapped[Optional[Numeric]] = mapped_column(Numeric(100, 7), default=0.0)
    total_e_v5: Mapped[Optional[Numeric]] = mapped_column(Numeric(100, 7), default=0.0)
    total_e_v6: Mapped[Optional[Numeric]] = mapped_column(Numeric(100, 7), default=0.0)
    total_e_v7: Mapped[Optional[Numeric]] = mapped_column(Numeric(100, 7), default=0.0)
    man: Mapped[bool] = mapped_column(Boolean, default=False)
    kat: Mapped[bool] = mapped_column(Boolean, default=False)
    kat_1_res_0: Mapped[Optional[Numeric]] = mapped_column(Numeric(100, 2), default=0.0)
    kat_1_res_1: Mapped[Optional[Numeric]] = mapped_column(Numeric(100, 2), default=0.0)
    kat_1_res_2: Mapped[Optional[Numeric]] = mapped_column(Numeric(100, 2), default=0.0)
    kat_1_res_3: Mapped[Optional[Numeric]] = mapped_column(Numeric(100, 2), default=0.0)
    kat_1_res_4: Mapped[Optional[Numeric]] = mapped_column(Numeric(100, 2), default=0.0)
    kat_2_res_0: Mapped[Optional[Numeric]] = mapped_column(Numeric(100, 2), default=0.0)
    kat_2_res_1: Mapped[Optional[Numeric]] = mapped_column(Numeric(100, 2), default=0.0)
    kat_2_res_2: Mapped[Optional[Numeric]] = mapped_column(Numeric(100, 2), default=0.0)
    kat_2_res_3: Mapped[Optional[Numeric]] = mapped_column(Numeric(100, 2), default=0.0)
    kat_2_res_4: Mapped[Optional[Numeric]] = mapped_column(Numeric(100, 2), default=0.0)
    kat_f_res_0: Mapped[Optional[Numeric]] = mapped_column(Numeric(100, 2), default=0.0)
    kat_f_res_1: Mapped[Optional[Numeric]] = mapped_column(Numeric(100, 2), default=0.0)
    kat_f_res_2: Mapped[Optional[Numeric]] = mapped_column(Numeric(100, 2), default=0.0)
    kat_f_res_3: Mapped[Optional[Numeric]] = mapped_column(Numeric(100, 2), default=0.0)
    kat_f_res_4: Mapped[Optional[Numeric]] = mapped_column(Numeric(100, 2), default=0.0)
    kat_1_res: Mapped[Optional[Numeric]] = mapped_column(Numeric(100, 2), default=0.0)
    kat_2_res: Mapped[Optional[Numeric]] = mapped_column(Numeric(100, 2), default=0.0)
    kat_f_res: Mapped[Optional[Numeric]] = mapped_column(Numeric(100, 2), default=0.0)
    kat_1_2_res: Mapped[Optional[Numeric]] = mapped_column(Numeric(100, 2), default=0.0)
    kat_1_2_pos: Mapped[Optional[int]] = mapped_column(Integer, default=0)
    kat_f_pos: Mapped[Optional[int]] = mapped_column(Integer, default=0)
    kat_1_min: Mapped[Optional[Numeric]] = mapped_column(Numeric(100, 2), default=0.0)
    kat_1_max: Mapped[Optional[Numeric]] = mapped_column(Numeric(100, 2), default=0.0)
    kat_2_min: Mapped[Optional[Numeric]] = mapped_column(Numeric(100, 2), default=0.0)
    kat_2_max: Mapped[Optional[Numeric]] = mapped_column(Numeric(100, 2), default=0.0)
    kat_f_min: Mapped[Optional[Numeric]] = mapped_column(Numeric(100, 2), default=0.0)
    kat_f_max: Mapped[Optional[Numeric]] = mapped_column(Numeric(100, 2), default=0.0)
    kat_type: Mapped[Optional[int]] = mapped_column(Integer, default=0)
    kat_flag1: Mapped[Optional[int]] = mapped_column(Integer, default=0)
    kat_flag2: Mapped[Optional[int]] = mapped_column(Integer, default=0)
    kat_1_min_n: Mapped[Optional[int]] = mapped_column(Integer, default=0)
    kat_1_max_n: Mapped[Optional[int]] = mapped_column(Integer, default=0)
    kat_2_min_n: Mapped[Optional[int]] = mapped_column(Integer, default=0)
    kat_2_max_n: Mapped[Optional[int]] = mapped_column(Integer, default=0)
    kat_f_min_n: Mapped[Optional[int]] = mapped_column(Integer, default=0)
    kat_f_max_n: Mapped[Optional[int]] = mapped_column(Integer, default=0)
    art: Mapped[bool] = mapped_column(Boolean, default=False)
    art_boy: Mapped[bool] = mapped_column(Boolean, default=False)
    art_vk: Mapped[bool] = mapped_column(Boolean, default=False)
    medal: Mapped[bool] = mapped_column(Boolean, default=False)
    v5: Mapped[Optional[int]] = mapped_column(Integer)
    v6: Mapped[Optional[int]] = mapped_column(Integer)
    is_group_type: Mapped[Optional[int]] = mapped_column(Integer)
