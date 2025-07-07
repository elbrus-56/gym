from datetime import datetime, timezone
from typing import List, Optional
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from src.core.depends import get_db
from src.features.organizer.competitions.schemas import CompetitionStatus
from src.core.enums import CompetitionStatus
from src.infrastructure.database.models import Competition
from src.features.organizer.competitions.schemas import (
    CompetitionCreate,
    CompetitionResponse,
    CompetitionUpdate,
)

router = APIRouter(
    prefix="/competitions",
    tags=["Competitions"],
    responses={404: {"description": "Not found"}},
)


async def _get_competition_or_404(db: Session, competition_id: UUID) -> Competition:
    """Вспомогательная функция для получения соревнования или выброса исключения"""
    competition = await db.scalar(
        select(Competition).where(Competition.id == competition_id)
    )
    if not competition:
        raise HTTPException(
            status_code=404,
            detail=f"Соревнование с ID {competition_id} не найдено",
        )
    return competition


@router.post(
    "/",
    response_model=CompetitionResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Создать новое соревнование",
    description="Создает новое соревнование с указанными параметрами",
)
async def create_competition(
    competition: CompetitionCreate,
    db: Session = Depends(get_db),
):
    """
    Создает новое соревнование

    - **name**: Название соревнования (обязательно)
    - **description**: Описание соревнования
    - **discipline**: Дисциплина (например, "Художественная гимнастика")
    - **start_date**: Дата начала (YYYY-MM-DD)
    - **end_date**: Дата окончания (YYYY-MM-DD)
    - **location**: Место проведения
    """
    db_competition = Competition(**competition.model_dump())
    db.add(db_competition)
    await db.flush()
    await db.refresh(db_competition)
    return db_competition


@router.get(
    "/",
    response_model=List[CompetitionResponse],
    summary="Получить список соревнований",
    description="Возвращает список всех соревнований с возможностью фильтрации",
)
async def read_competitions(
    status_filter: Optional[CompetitionStatus] = None,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
):
    """
    Получает список соревнований

    Параметры запроса:
    - **status_filter**: Фильтр по статусу (planned, active, completed)
    - **skip**: Количество записей для пропуска (пагинация)
    - **limit**: Максимальное количество возвращаемых записей
    """
    stmt = select(Competition)

    if status_filter:
        stmt = stmt.filter(Competition.status == status_filter)

    result = await db.execute(stmt.offset(skip).limit(limit))
    return result.scalars().all()


@router.get(
    "/{competition_id}",
    response_model=CompetitionResponse,
    summary="Получить детали соревнования",
    description="Возвращает полную информацию о конкретном соревновании",
)
async def read_competition(
    competition_id: UUID,
    db: Session = Depends(get_db),
):
    """
    Получает детальную информацию о соревновании по ID
    """
    return await _get_competition_or_404(db, competition_id)


@router.put(
    "/{competition_id}",
    response_model=CompetitionResponse,
    summary="Обновить данные соревнования",
    description="Обновляет информацию о соревновании",
)
async def update_competition(
    competition_id: UUID,
    competition: CompetitionUpdate,
    db: Session = Depends(get_db),
):
    db_competition = await _get_competition_or_404(db, competition_id)

    update_data = competition.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_competition, field, value)

    db_competition.updated_at = datetime.now(timezone.utc)
    return db_competition


@router.patch(
    "/{competition_id}/status",
    response_model=CompetitionResponse,
    summary="Изменить статус соревнования",
    description="Обновляет статус соревнования (planned, active, completed)",
)
async def update_competition_status(
    competition_id: UUID,
    status_update: CompetitionStatus,
    db: Session = Depends(get_db),
):
    """
    Изменяет статус соревнования
    """
    db_competition = await _get_competition_or_404(db, competition_id)

    db_competition.status = status_update

    if status_update == CompetitionStatus.ACTIVE:
        db_competition.started_at = datetime.now(timezone.utc)
    elif status_update == CompetitionStatus.COMPLETED:
        db_competition.completed_at = datetime.now(timezone.utc)

    db_competition.updated_at = datetime.now(timezone.utc)
    return db_competition


@router.delete(
    "/{competition_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Удалить соревнование",
    description="Удаляет соревнование и все связанные данные",
)
async def delete_competition(
    competition_id: UUID,
    db: Session = Depends(get_db),
):
    """
    Удаляет соревнование по ID
    """
    db_competition = await _get_competition_or_404(db, competition_id)

    if db_competition.status == CompetitionStatus.ACTIVE:
        raise HTTPException(
            status_code=400, detail="Нельзя удалить активное соревнование"
        )

    await db.delete(db_competition)
    return None
