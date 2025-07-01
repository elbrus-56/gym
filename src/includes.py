from fastapi import APIRouter
from src.features.organizer.competitions.handler import router as competitions_router

router = APIRouter()

router.include_router(competitions_router)
