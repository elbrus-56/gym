from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from src.config import settings

engine = create_async_engine(
    settings.DATABASE_URL,
    echo=settings.DB.ECHO,
)


AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False,
)


async def close_db_connection():
    """Закрывает соединение с базой данных."""
    await engine.dispose()
