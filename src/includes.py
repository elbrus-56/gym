from fastapi import APIRouter
from src.features.organizer.competitions.handler import router as competitions_router
from src.features.organizer.periods.handler import router as periods_router
from src.features.organizer.groups.handler import router as groups_router
from src.features.organizer.flows.handler import router as flows_router
from src.features.organizer.events.handler import router as events_router

router = APIRouter()

router.include_router(competitions_router)
router.include_router(periods_router)
router.include_router(groups_router)
router.include_router(flows_router)
router.include_router(events_router)
