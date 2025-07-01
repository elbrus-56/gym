from contextlib import asynccontextmanager

from fastapi import FastAPI
from src.includes import router
from src.infrastructure.database.connection import close_db_connection
from loguru import logger


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Асинхронный контекстный менеджер для управления жизненным циклом FastAPI приложения."""
    logger.info("Запуск приложения...")
    yield
    await close_db_connection()
    logger.info("Приложение остановлено.")


app = FastAPI(lifespan=lifespan, title="GYM API")


app.include_router(router)


@app.get("/", tags=["Root"])
async def read_root():
    """Корневой эндпоинт для проверки работы API."""
    return {"message": "Welcome to Gym API"}
