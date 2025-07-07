from datetime import datetime, timezone
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session
from pydantic import ValidationError

from src.core.depends import get_db
from src.infrastructure.database.models import Event, Competition
from .schemas import (  # Импорт созданных ранее схем
    EventCreate,
    EventUpdate,
    EventResponse,
)

router = APIRouter(
    prefix="/events",
    tags=["Events"],
    responses={404: {"description": "Not found"}},
)


async def _get_event_or_404(db: Session, event_id: UUID) -> Event:
    """Получить событие по ID или вызвать 404"""
    event = await db.scalar(select(Event).where(Event.id == event_id))
    if not event:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Event with ID {event_id} not found",
        )
    return event


async def _check_competition_exists(db: Session, competition_id: UUID) -> None:
    """Проверить существование соревнования"""
    if not await db.scalar(select(Competition).where(Competition.id == competition_id)):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Competition with ID {competition_id} does not exist",
        )


@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    summary="Создать новое событие",
    response_model=EventResponse,
)
async def create_event(
    event_data: EventCreate,
    db: Session = Depends(get_db),
):
    """
    Создает новое событие с валидацией:
    - Проверка существования competition
    - Автоматическая валидация временных меток (completed_at > started_at)
    """
    await _check_competition_exists(db, event_data.competition)

    try:
        new_event = Event(**event_data.model_dump())
    except ValidationError as e:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=str(e),
        )

    db.add(new_event)
    await db.commit()
    await db.refresh(new_event)
    return new_event


@router.get(
    "/",
    summary="Получить список событий",
    response_model=list[EventResponse],
)
async def read_events(
    competition_id: UUID | None = None,
    event_type: str | None = None,
    start_from: datetime | None = None,
    start_to: datetime | None = None,
    db: Session = Depends(get_db),
):
    """
    Получает список событий с фильтрацией:
    - По соревнованию (competition_id)
    - По типу события (event_type)
    - По временному диапазону (start_from - start_to)
    """
    stmt = select(Event)

    if competition_id:
        stmt = stmt.where(Event.competition == competition_id)
    if event_type:
        stmt = stmt.where(Event.name == event_type)
    if start_from:
        stmt = stmt.where(Event.started_at >= start_from)
    if start_to:
        stmt = stmt.where(Event.started_at <= start_to)

    result = await db.scalars(stmt.order_by(Event.started_at))
    return result.all()


@router.get(
    "/{event_id}",
    summary="Получить событие по ID",
    response_model=EventResponse,
)
async def read_event(event_id: UUID, db: Session = Depends(get_db)):
    """Получает детальную информацию о событии по ID"""
    return await _get_event_or_404(db, event_id)


@router.patch(
    "/{event_id}",
    summary="Обновить данные события",
    response_model=EventResponse,
)
async def update_event(
    event_id: UUID,
    update_data: EventUpdate,
    db: Session = Depends(get_db),
):
    """
    Обновляет данные события с проверками:
    - Существование события
    - Существование competition (если обновляется)
    - Валидация временных меток
    """
    event = await _get_event_or_404(db, event_id)
    update_values = update_data.model_dump(exclude_unset=True)

    # Проверка существования competition (если обновляется)
    if "competition" in update_values:
        await _check_competition_exists(db, update_values["competition"])

    # Валидация временных меток
    if "started_at" in update_values or "completed_at" in update_values:
        started_at = update_values.get("started_at", event.started_at)
        completed_at = update_values.get("completed_at", event.completed_at)

        if completed_at <= started_at:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="completed_at must be after started_at",
            )

    # Применение обновлений
    for field, value in update_values.items():
        setattr(event, field, value)

    event.updated_at = datetime.now(timezone.utc)
    await db.commit()
    await db.refresh(event)
    return event


@router.delete(
    "/{event_id}", status_code=status.HTTP_204_NO_CONTENT, summary="Удалить событие"
)
async def delete_event(event_id: UUID, db: Session = Depends(get_db)) -> None:
    """Удаляет событие по ID"""
    event = await _get_event_or_404(db, event_id)
    await db.delete(event)
    await db.commit()
