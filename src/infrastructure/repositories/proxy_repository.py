import uuid
from abc import ABC, abstractmethod
from typing import List, Literal, Optional

from sqlalchemy import asc, delete, desc, func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from core.domain.models import ProxyServer
from infrastructure.database.models import ProxyServerDB


class AbstractProxyRepository(ABC):
    @abstractmethod
    async def add(self, proxy: ProxyServer) -> ProxyServer:
        """Добавляет новый прокси-сервер в хранилище."""
        raise NotImplementedError

    @abstractmethod
    async def get_by_id(self, proxy_id: uuid.UUID) -> Optional[ProxyServer]:
        """Получает прокси-сервер по его ID."""
        raise NotImplementedError

    @abstractmethod
    async def exists_by_host_port(self, host: str, port: int) -> bool:
        """Проверяет, существует ли прокси с указанными host и port."""
        raise NotImplementedError

    @abstractmethod
    async def list_all(
        self,
        is_active: Optional[bool] = None,
        protocol: Optional[str] = None,
        country: Optional[str] = None,
        sort_by: Optional[Literal["created_at", "last_checked_at"]] = None,
        sort_order: Literal["asc", "desc"] = "asc",
    ) -> List[ProxyServer]:
        """Возвращает список всех прокси-серверов с возможностью фильтрации и сортировки."""
        raise NotImplementedError

    @abstractmethod
    async def delete(self, proxy_id: uuid.UUID) -> bool:
        """Удаляет прокси-сервер по его ID. Возвращает True, если удаление успешно."""
        raise NotImplementedError

    @abstractmethod
    async def get_random_alive(self) -> Optional[ProxyServer]:
        """Возвращает случайный 'живой' прокси-сервер."""
        raise NotImplementedError


class SQLAlchemyProxyRepository(AbstractProxyRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def add(self, proxy: ProxyServer) -> ProxyServer:
        """Добавляет новый прокси-сервер в БД."""
        db_proxy = ProxyServerDB(**proxy.model_dump(exclude_unset=True))
        self.session.add(db_proxy)
        await self.session.flush()  # Получаем ID до коммита
        await self.session.refresh(db_proxy)  # Обновляем объект данными из БД
        return ProxyServer.model_validate(db_proxy)

    async def get_by_id(self, proxy_id: uuid.UUID) -> Optional[ProxyServer]:
        """Получает прокси-сервер из БД по его ID."""
        result = await self.session.execute(
            select(ProxyServerDB).where(ProxyServerDB.id == str(proxy_id))
        )
        db_proxy = result.scalars().first()
        return ProxyServer.model_validate(db_proxy) if db_proxy else None

    async def exists_by_host_port(self, host: str, port: int) -> bool:
        """Проверяет существование прокси в БД по host и port."""
        stmt = select(func.count(ProxyServerDB.id)).where(
            ProxyServerDB.host == host, ProxyServerDB.port == port
        )
        result = await self.session.execute(stmt)
        count = result.scalar_one_or_none()
        return count is not None and count > 0

    async def list_all(
        self,
        is_active: Optional[bool] = None,
        protocol: Optional[str] = None,
        country: Optional[str] = None,
        sort_by: Optional[Literal["created_at", "last_checked_at"]] = None,
        sort_order: Literal["asc", "desc"] = "asc",
    ) -> List[ProxyServer]:
        """Возвращает список прокси из БД с фильтрацией и сортировкой."""
        stmt = select(ProxyServerDB)

        # Фильтрация
        if is_active is not None:
            stmt = stmt.where(ProxyServerDB.is_alive == is_active)
        if protocol:
            stmt = stmt.where(
                func.lower(ProxyServerDB.protocol) == func.lower(protocol)
            )
        if country:
            stmt = stmt.where(func.lower(ProxyServerDB.country) == func.lower(country))

        # Сортировка
        order_applied = False
        if sort_by:
            column_to_sort = getattr(ProxyServerDB, sort_by, None)
            if column_to_sort:
                order_func = asc if sort_order == "asc" else desc
                stmt = stmt.order_by(order_func(column_to_sort))
                order_applied = True

        # Сортировка по умолчанию, если другая не применялась
        if not order_applied:
            stmt = stmt.order_by(asc(ProxyServerDB.created_at))

        result = await self.session.execute(stmt)
        db_proxies = result.scalars().all()
        return [ProxyServer.model_validate(p) for p in db_proxies]

    async def delete(self, proxy_id: uuid.UUID) -> bool:
        """Удаляет прокси-сервер из БД по ID."""
        result = await self.session.execute(
            delete(ProxyServerDB).where(ProxyServerDB.id == str(proxy_id))
        )
        await self.session.flush()  # Применяем удаление
        return result.rowcount > 0

    async def get_random_alive(self) -> Optional[ProxyServer]:
        """Возвращает случайный 'живой' прокси-сервер из БД."""
        stmt = (
            select(ProxyServerDB)
            .where(ProxyServerDB.is_alive == True)  # Ищем только живые прокси
            .order_by(
                func.random()
            )  # Используем func.random() для случайной сортировки (работает в SQLite/PostgreSQL)
            .limit(1)  # Берем только один
        )
        result = await self.session.execute(stmt)
        db_proxy = result.scalars().first()
        return ProxyServer.model_validate(db_proxy) if db_proxy else None
