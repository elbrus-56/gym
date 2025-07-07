from datetime import datetime, timezone
from typing import List, Optional
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from src.core.depends import get_db
from src.infrastructure.database.models import Group, Period
from src.features.organizer.groups.schemas import (
    GroupCreate,
    GroupUpdate,
    GroupResponse,
)

router = APIRouter(
    prefix="/groups",
    tags=["Groups"],
    responses={404: {"description": "Not found"}},
)


async def _get_group_or_404(db: Session, group_id: UUID) -> Group:
    """Получить группу по ID или вызвать 404 ошибку"""
    group = await db.scalar(select(Group).where(Group.id == group_id))
    if not group:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Group with ID {group_id} not found",
        )
    return group


async def _check_period_exists(db: Session, period_id: UUID) -> None:
    """Проверить существование периода"""
    if period_id and not await db.scalar(select(Period).where(Period.id == period_id)):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Period with ID {period_id} does not exist",
        )


@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    summary="Создать новую группу",
    response_model=GroupResponse,
)
async def create_group(
    group_data: GroupCreate,
    db: Session = Depends(get_db),
):
    """
    Создает новую группу с валидацией периода при наличии
    """
    # Проверка существования периода (если указан)
    if group_data.period:
        await _check_period_exists(db, group_data.period)

    new_group = Group(**group_data.model_dump())
    db.add(new_group)
    await db.flush()
    await db.refresh(new_group)
    return new_group


@router.get(
    "/",
    summary="Получить список групп",
    response_model=List[GroupResponse],
)
async def read_groups(
    period_id: Optional[UUID] = None,
    category: Optional[str] = None,
    group_type: Optional[int] = None,
    db: Session = Depends(get_db),
):
    """
    Получает список групп с опциональной фильтрацией
    """
    stmt = select(Group)

    if period_id:
        stmt = stmt.where(Group.period == period_id)
    if category:
        stmt = stmt.where(Group.category == category)
    if group_type is not None:
        stmt = stmt.where(Group.group_type == group_type)

    result = await db.scalars(stmt)
    return result.all()


@router.get(
    "/{group_id}",
    summary="Получить группу по ID",
    response_model=GroupResponse,
)
async def read_group(group_id: UUID, db: Session = Depends(get_db)):
    """Получает детальную информацию о группе по её ID"""
    return await _get_group_or_404(db, group_id)


@router.patch(
    "/{group_id}", summary="Обновить данные группы", response_model=GroupResponse
)
async def update_group(
    group_id: UUID,
    update_data: GroupUpdate,
    db: Session = Depends(get_db),
):
    """
    Обновляет данные группы с проверками:
    - Существование группы
    - Существование периода (если он изменен)
    """
    group = await _get_group_or_404(db, group_id)
    if update_data.period is not None:
        await _check_period_exists(db, update_data.period)

    update_values = update_data.model_dump(exclude_unset=True)

    for field, value in update_values.items():
        setattr(group, field, value)

    group.updated_at = datetime.now(timezone.utc)
    await db.refresh(group)
    return db


@router.delete(
    "/{group_id}", status_code=status.HTTP_204_NO_CONTENT, summary="Удалить группу"
)
async def delete_group(group_id: UUID, db: Session = Depends(get_db)) -> None:
    """Удаляет группу по ID"""
    group = await _get_group_or_404(db, group_id)
    await db.delete(group)
