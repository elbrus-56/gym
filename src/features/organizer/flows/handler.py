from datetime import datetime, timezone
from typing import List, Optional
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from src.core.depends import get_db
from src.infrastructure.database.models import (
    Flow,
    Group,
)
from src.features.organizer.flows.schemas import (
    FlowCreate,
    FlowUpdate,
    FlowResponse,
)

router = APIRouter(
    prefix="/flows",
    tags=["Flows"],
    responses={404: {"description": "Not found"}},
)


async def _get_flow_or_404(db: Session, flow_id: UUID) -> Flow:
    """Получить поток по ID или вызвать 404 ошибку"""
    flow = await db.scalar(select(Flow).where(Flow.id == flow_id))
    if not flow:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Flow with ID {flow_id} not found",
        )
    return flow


async def _check_group_exists(db: Session, group_id: UUID) -> None:
    """Проверить существование группы"""
    if group_id and not await db.scalar(select(Group).where(Group.id == group_id)):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Group with ID {group_id} does not exist",
        )


@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    summary="Создать новый поток",
    response_model=FlowResponse,
)
async def create_flow(
    flow_data: FlowCreate,
    db: Session = Depends(get_db),
):
    """
    Создает новый поток с валидацией группы при наличии
    """
    if flow_data.group:
        await _check_group_exists(db, flow_data.group)

    new_flow = Flow(**flow_data.model_dump())
    db.add(new_flow)
    await db.commit()
    await db.refresh(new_flow)
    return new_flow


@router.get(
    "/",
    summary="Получить список потоков",
    response_model=List[FlowResponse],
)
async def read_flows(
    group_id: Optional[UUID] = None,
    name: Optional[str] = None,
    brake_type: Optional[int] = None,
    db: Session = Depends(get_db),
):
    """
    Получает список потоков с опциональной фильтрацией
    """
    stmt = select(Flow)

    if group_id:
        stmt = stmt.where(Flow.group == group_id)
    if name:
        stmt = stmt.where(Flow.name == name)
    if brake_type is not None:
        stmt = stmt.where(Flow.brake_type == brake_type)

    result = await db.scalars(stmt)
    return result.all()


@router.get(
    "/{flow_id}",
    summary="Получить поток по ID",
    response_model=FlowResponse,
)
async def read_flow(flow_id: UUID, db: Session = Depends(get_db)):
    """Получает детальную информацию о потоке по его ID"""
    return await _get_flow_or_404(db, flow_id)


@router.patch(
    "/{flow_id}", summary="Обновить данные потока", response_model=FlowResponse
)
async def update_flow(
    flow_id: UUID,
    update_data: FlowUpdate,
    db: Session = Depends(get_db),
):
    """
    Обновляет данные потока с проверками:
    - Существование потока
    - Существование группы (если она изменена)
    """
    flow = await _get_flow_or_404(db, flow_id)

    # Проверка существования группы (если указана)
    if update_data.group is not None:
        await _check_group_exists(db, update_data.group)

    update_values = update_data.model_dump(exclude_unset=True)

    for field, value in update_values.items():
        setattr(flow, field, value)

    flow.updated_at = datetime.now(timezone.utc)
    await db.refresh(flow)
    return flow


@router.delete(
    "/{flow_id}", status_code=status.HTTP_204_NO_CONTENT, summary="Удалить поток"
)
async def delete_flow(flow_id: UUID, db: Session = Depends(get_db)) -> None:
    """Удаляет поток по ID"""
    flow = await _get_flow_or_404(db, flow_id)
    await db.delete(flow)
