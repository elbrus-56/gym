import os
import sys

# Добавляем корневую папку проекта в sys.path
# Это нужно, чтобы тесты могли импортировать модули из core, features, infrastructure
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, project_root)

import asyncio
from typing import AsyncGenerator, Generator

import pytest
import pytest_asyncio
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

# Используем отдельную БД для тестов
TEST_DATABASE_URL = "sqlite+aiosqlite:///./test_proxy_manager.db"

# Переопределяем engine и SessionLocal для тестов
engine = create_async_engine(TEST_DATABASE_URL, echo=False) # echo=False в тестах
TestingSessionLocal = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
)

from infrastructure.database.connection import get_db
# Импортируем Base из основной модели и основное приложение
from infrastructure.database.models import Base
from main import app

# Фикстура для создания таблиц перед тестами и удаления после
# УДАЛЕНО: pytest-asyncio предоставляет свою фикстуру event_loop
# @pytest.fixture(scope="session", autouse=True)
# def event_loop():
#     loop = asyncio.get_event_loop_policy().new_event_loop()
#     yield loop
#     loop.close()

@pytest_asyncio.fixture(scope="function", autouse=True)
async def setup_database():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all) # Удаляем старые таблицы
        await conn.run_sync(Base.metadata.create_all) # Создаем новые
    yield
    # Очистка после тестов (опционально, т.к. создаем заново)
    # async with engine.begin() as conn:
    #     await conn.run_sync(Base.metadata.drop_all)
    await engine.dispose()


# Фикстура для переопределения зависимости get_db
@pytest_asyncio.fixture(scope="function")
async def db_session() -> AsyncGenerator[AsyncSession, None]:
    async with TestingSessionLocal() as session:
        yield session
        await session.rollback() # Откатываем изменения после каждого теста

# Фикстура для тестового HTTP клиента
@pytest_asyncio.fixture(scope="function")
async def client(db_session: AsyncSession):
    # Переопределяем зависимость get_db для использования тестовой сессии
    def override_get_db() -> Generator[AsyncSession, None, None]:
        yield db_session

    app.dependency_overrides[get_db] = override_get_db

    # Используем ASGITransport для передачи FastAPI app в AsyncClient
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        yield ac

    # Удаляем переопределение после теста
    del app.dependency_overrides[get_db]
