from datetime import datetime, timezone
from typing import List, Optional
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from src.core.depends import get_db

from src.features.organizer.periods.schemas import (
    PeriodCreate,
    PeriodResponse,
    PeriodUpdate,
)
from src.infrastructure.database.models import Period

router = APIRouter(
    prefix="/periods",
    tags=["Periods"],
    responses={404: {"description": "Not found"}},
)


async def _get_period_or_404(db: Session, period_id: UUID) -> Period:
    """Вспомогательная функция для получения периода или выброса исключения"""
    period = await db.scalar(select(Period).where(Period.id == period_id))
    if not period:
        raise HTTPException(
            status_code=404,
            detail=f"Период с ID {period_id} не найден",
        )
    return period


@router.post(
    "/",
    response_model=PeriodResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Создать период для расписания соревнования",
)
async def create_period(
    period: PeriodCreate,
    db: Session = Depends(get_db),
):
    db_period = Period(**period.model_dump())
    db.add(db_period)
    await db.flush()
    await db.refresh(db_period)
    return db_period


@router.get(
    "/",
    response_model=List[PeriodResponse],
    summary="Получить расписание соревнования",
)
async def read_periods(
    period_id: UUID | None = None,
    db: Session = Depends(get_db),
):
    stmt = select(Period)

    if period_id:
        stmt = stmt.where(Period.competition == period_id)

    result = await db.scalars(stmt)
    return result.all()


@router.get(
    "/{period_id}",
    response_model=PeriodResponse,
    summary="Получить информацию о конкретном периоде в расписании соревнования",
)
async def read_period(
    period_id: UUID,
    db: Session = Depends(get_db),
):
    return await _get_period_or_404(db, period_id)


@router.patch(
    "/{period_id}",
    response_model=PeriodResponse,
    summary="Обновить данные периода в расписании соревнования",
)
async def update_period(
    period_id: UUID,
    period: PeriodUpdate,
    db: Session = Depends(get_db),
):
    db_period = await _get_period_or_404(db, period_id)
    update_data = period.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_period, field, value)

    db_period.updated_at = datetime.now(timezone.utc)
    return db_period


@router.delete(
    "/{period_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Удалить период из расписания",
)
async def delete_period(
    period_id: UUID,
    db: Session = Depends(get_db),
):
    """
    Удаляет период из расписания по ID
    """
    db_period = await _get_period_or_404(db, period_id)
    await db.delete(db_period)
    return None
