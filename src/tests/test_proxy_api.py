import asyncio  # Добавляем импорт
import uuid
from typing import List, Optional  # Добавляем List
# Убираем импорт respx, если он больше не используется
# import respx
from unittest.mock import (AsyncMock,  # Добавляем импорты для мокирования
                           MagicMock, patch)

import httpx  # Добавляем импорт httpx для TimeoutException
import pytest
from fastapi import status
from httpx import AsyncClient, Response
# Добавляем импорт AsyncSession
from sqlalchemy.ext.asyncio import AsyncSession

# Импортируем DTO для проверок
from core.dto.proxy_dto import ProxyResponseDTO

# Убираем импорт доменной модели, если она больше не нужна напрямую в тестах
# from core.domain.proxy import ProxyServer

# Помечаем все тесты в этом файле как асинхронные
pytestmark = pytest.mark.asyncio

async def test_read_root(client: AsyncClient):
    response = await client.get("/")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"message": "Welcome to Proxy Manager API"}

# --- Тесты для POST /proxies --- #

async def test_add_proxy_object(client: AsyncClient):
    """Тестирует добавление прокси через JSON объект (AddProxyCommand)."""
    proxy_data = {
        "host": "192.168.1.1",
        "port": 8080,
        "username": "testuser",
        "password": "testpass",
        "protocol": "http"
    }
    response = await client.post("/proxies", json=proxy_data)
    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    assert data["host"] == proxy_data["host"]
    assert data["port"] == proxy_data["port"]
    assert data["username"] == proxy_data["username"]
    assert data["protocol"] == proxy_data["protocol"] # Проверяем protocol
    assert "id" in data
    assert data["is_alive"] is None
    assert data["last_checked_at"] is None
    assert "created_at" in data
    assert "password_hash" not in data

async def test_add_proxy_string_simple(client: AsyncClient):
    """Тестирует добавление прокси через строку в JSON - host:port."""
    proxy_string = "192.168.1.2:3128" # Этот формат все еще поддерживается
    payload = {"proxy_string": proxy_string}
    response = await client.post("/proxies", json=payload)
    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    assert data["host"] == "192.168.1.2"
    assert data["port"] == 3128
    assert data["username"] is None

async def test_add_proxy_string_with_auth(client: AsyncClient):
    """Тестирует добавление прокси через строку в JSON с аутентификацией - user:pass@host:port."""
    # Используем новый формат
    proxy_string = "user2:pass2@192.168.1.3:8888"
    payload = {"proxy_string": proxy_string}
    response = await client.post("/proxies", json=payload)
    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    assert data["host"] == "192.168.1.3"
    assert data["port"] == 8888
    assert data["username"] == "user2"
    assert "password_hash" not in data
    assert "id" in data

async def test_add_proxy_string_invalid_format(client: AsyncClient):
    """Тестирует неверный формат строки прокси."""
    invalid_strings = [
        "192.168.1.4", # Нет порта (и не user:pass@host:port)
        "user:pass@192.168.1.5", # Нет порта после @
        "user@192.168.1.5:8080", # Нет пароля перед @
        "user:@192.168.1.5:8080", # Нет пароля перед @ (пустой)
        "@192.168.1.6:8080", # Нет user:pass перед @
        "user:pass@", # Нет host:port после @
        "192.168.1.7:port", # Нечисловой порт
        "user:pass@host:port", # Нечисловой порт
        "", # Пустая строка
        "host:port:extra" # Лишняя часть для host:port
    ]
    for proxy_string in invalid_strings:
        payload = {"proxy_string": proxy_string}
        response = await client.post("/proxies", json=payload)
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
        detail = response.json()["detail"]
        # Проверяем, что сообщение об ошибке содержит одну из ожидаемых фраз
        assert "Invalid format" in detail or \
               "Invalid authentication format" in detail or \
               "Invalid host:port format" in detail or \
               "Invalid port number" in detail # Эта проверка осталась от предыдущего теста на порт

async def test_add_proxy_string_invalid_port_value(client: AsyncClient):
    """Тестирует неверное значение порта в строке прокси."""
    invalid_strings = [
        "192.168.1.7:0", # порт 0
        "192.168.1.8:65536", # порт > 65535
        "user:pass@192.168.1.9:0", # порт 0 с auth
        "user:pass@192.168.1.10:65536" # порт > 65535 с auth
    ]
    for proxy_string in invalid_strings:
        payload = {"proxy_string": proxy_string}
        response = await client.post("/proxies", json=payload)
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
        assert "Invalid port number" in response.json()["detail"]

async def test_add_proxy_duplicate_from_string(client: AsyncClient):
    """Тестирует добавление дубликата через строку (новый формат)."""
    # Используем новый формат
    proxy_string = "dupuser:duppass@10.0.10.1:5000"
    payload = {"proxy_string": proxy_string}
    # Первое добавление - успешно
    response1 = await client.post("/proxies", json=payload)
    assert response1.status_code == status.HTTP_201_CREATED
    # Второе добавление - ошибка 409 (хост и порт совпадают)
    response2 = await client.post("/proxies", json=payload)
    assert response2.status_code == status.HTTP_409_CONFLICT
    assert "already exists" in response2.json()["detail"]


# Переименовываем оригинальный тест для ясности
async def test_add_proxy_object_invalid_port(client: AsyncClient):
    proxy_data = {"host": "192.168.1.9", "port": 99999} # Невалидный порт
    response = await client.post("/proxies", json=proxy_data)
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

async def test_list_proxies_empty(client: AsyncClient):
    response = await client.get("/proxies")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == []

# Вспомогательная функция для создания прокси
async def create_proxy(client: AsyncClient, host: str, port: int) -> ProxyResponseDTO: # Возвращаем DTO
    proxy_data = {"host": host, "port": port}
    add_response = await client.post("/proxies", json=proxy_data)
    assert add_response.status_code == status.HTTP_201_CREATED
    # Парсим ответ в DTO
    created_proxy = ProxyResponseDTO(**add_response.json())
    # Убираем логику обновления is_alive, она тут не нужна и не работала
    return created_proxy

async def test_list_proxies_with_data(client: AsyncClient):
    proxy1 = await create_proxy(client, "10.0.0.1", 3128)
    proxy2 = await create_proxy(client, "10.0.0.2", 3129)

    response = await client.get("/proxies")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert len(data) == 2
    hosts = {item["host"] for item in data}
    assert hosts == {proxy1.host, proxy2.host}
    # Проверяем поля из ProxyResponseDTO
    assert all(item["is_alive"] is None for item in data) # Исправляем is_active -> is_alive
    assert all(item["last_checked_at"] is None for item in data) # Исправляем last_checked -> last_checked_at
    assert all("created_at" in item for item in data) # created_at

async def test_delete_proxy(client: AsyncClient):
    # create_proxy теперь возвращает ProxyResponseDTO, у которого есть id типа UUID
    proxy = await create_proxy(client, "delete.me", 1234)

    delete_response = await client.delete(f"/proxies/{proxy.id}")
    assert delete_response.status_code == status.HTTP_204_NO_CONTENT

    list_response = await client.get("/proxies")
    assert list_response.status_code == status.HTTP_200_OK
    proxies = list_response.json()
    # Сравниваем UUID из proxy.id с ID в ответе (которые теперь должны быть строками UUID)
    assert str(proxy.id) not in [p["id"] for p in proxies]

async def test_delete_proxy_not_found(client: AsyncClient):
    non_existent_id = uuid.uuid4()
    delete_response = await client.delete(f"/proxies/{non_existent_id}")
    assert delete_response.status_code == status.HTTP_404_NOT_FOUND

# --- Новые тесты --- #

# Убираем @respx.mock
# @respx.mock
@pytest.mark.asyncio # Используем стандартный маркер
async def test_check_proxy_status_alive(client: AsyncClient):
    proxy = await create_proxy(client, "alive.proxy", 8888)
    # check_url больше не нужен для respx
    # check_url = "http://httpbin.org/ip"

    # --- Мокирование httpx.AsyncClient ---
    # Создаем мок ответа
    mock_response = httpx.Response(200, json={"origin": proxy.host})
    # Мокируем raise_for_status(), чтобы он ничего не делал
    mock_response.raise_for_status = MagicMock()

    # Создаем мок экземпляра клиента с асинхронным методом get
    mock_http_client_instance = MagicMock()
    # Используем AsyncMock для асинхронного метода
    mock_http_client_instance.get = AsyncMock(return_value=mock_response)

    # Настраиваем мок для работы с 'async with'
    mock_http_client_instance.__aenter__.return_value = mock_http_client_instance
    mock_http_client_instance.__aexit__.return_value = None # Простое значение для __aexit__

    # Патчим класс AsyncClient в модуле use_case
    with patch("features.check_proxy_status.use_case.httpx.AsyncClient", return_value=mock_http_client_instance) as mock_async_client_class:
        # Вызываем эндпоинт API
        response = await client.get(f"/proxies/{proxy.id}/check")

        # --- Проверки ---
        # Проверяем, что AsyncClient был вызван (не обязательно, но полезно)
        # mock_async_client_class.assert_called_once()

        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        # Сравниваем строку UUID из ответа с str(proxy.id)
        assert data["proxy_id"] == str(proxy.id)
        assert data["is_alive"] is True
        assert data["error"] is None

# Убираем @respx.mock
# @respx.mock
@pytest.mark.asyncio
async def test_check_proxy_status_down(client: AsyncClient):
    proxy = await create_proxy(client, "down.proxy", 8889)
    # check_url больше не нужен
    # check_url = "http://httpbin.org/ip"

    # --- Мокирование httpx.AsyncClient ---
    # Создаем мок экземпляра клиента с асинхронным методом get, который выбрасывает исключение
    mock_http_client_instance = MagicMock()
    # Настраиваем AsyncMock на выброс TimeoutException
    mock_http_client_instance.get = AsyncMock(side_effect=httpx.TimeoutException("Timeout occurred"))

    # Настраиваем мок для работы с 'async with'
    mock_http_client_instance.__aenter__.return_value = mock_http_client_instance
    mock_http_client_instance.__aexit__.return_value = None

    # Патчим класс AsyncClient в модуле use_case
    with patch("features.check_proxy_status.use_case.httpx.AsyncClient", return_value=mock_http_client_instance) as mock_async_client_class:
        # Вызываем эндпоинт API
        response = await client.get(f"/proxies/{proxy.id}/check")

        # --- Проверки ---
        assert response.status_code == status.HTTP_200_OK # Ожидаем 200, но с is_active=False
        data = response.json()
        # Сравниваем строку UUID из ответа с str(proxy.id)
        assert data["proxy_id"] == str(proxy.id)
        assert data["is_alive"] is False
        assert "Тайм-аут" in data["error"] # Проверяем наличие русского слова "Тайм-аут" в ошибке

async def test_check_proxy_status_not_found(client: AsyncClient):
    non_existent_id = uuid.uuid4()
    response = await client.get(f"/proxies/{non_existent_id}/check")
    assert response.status_code == status.HTTP_404_NOT_FOUND

# Тесты для GET /proxies/random
# Важно: Эти тесты зависят от того, что база данных очищается между тестами (через rollback в db_session)

async def test_get_random_proxy_no_proxies(client: AsyncClient):
    response = await client.get("/proxies/random")
    # Если нет никаких прокси (даже не проверенных), репозиторий вернет None -> 404
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json()["detail"] == "No alive proxies found."

async def test_get_random_proxy_none_alive(client: AsyncClient, db_session: AsyncSession):
    # Добавляем прокси, но помечаем его как не живой (нужно обновление в БД)
    proxy = await create_proxy(client, "dead.proxy", 1111)
    # Обновляем статус в БД вручную для теста
    from sqlalchemy import update

    from infrastructure.database.models import ProxyServerDB
    stmt = update(ProxyServerDB).where(ProxyServerDB.id == proxy.id).values(is_alive=False)
    await db_session.execute(stmt)

    response = await client.get("/proxies/random")
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json()["detail"] == "No alive proxies found."

async def test_get_random_proxy_one_alive(client: AsyncClient, db_session: AsyncSession):
    # Добавляем один живой прокси
    # create_proxy возвращает DTO
    proxy_alive_dto = await create_proxy(client, "alive.proxy.random", 2222)
    from sqlalchemy import update

    from infrastructure.database.models import ProxyServerDB

    # Используем ID из DTO
    stmt = update(ProxyServerDB).where(ProxyServerDB.id == proxy_alive_dto.id).values(is_alive=True)
    await db_session.execute(stmt)

    # Добавляем один мертвый прокси
    proxy_dead_dto = await create_proxy(client, "dead.proxy.random", 3333)
    stmt_dead = update(ProxyServerDB).where(ProxyServerDB.id == proxy_dead_dto.id).values(is_alive=False)
    await db_session.execute(stmt_dead)

    response = await client.get("/proxies/random")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    # Сверяем с данными из DTO, конвертируя ID в строку для сравнения с JSON
    assert data["id"] == str(proxy_alive_dto.id)
    assert data["host"] == proxy_alive_dto.host
    assert data["port"] == proxy_alive_dto.port
    assert data["username"] == proxy_alive_dto.username
    assert data["is_alive"] is True # Теперь будет сверяться с полем is_alive в DTO
    assert "last_checked_at" in data # Исправляем last_checked -> last_checked_at
    assert "created_at" in data # Проверяем наличие created_at

# --- Тесты для фильтрации и сортировки GET /proxies ---

async def test_list_proxies_filter_by_is_active(client: AsyncClient, db_session: AsyncSession):
    """Проверяет фильтрацию по статусу is_alive."""
    from datetime import datetime, timedelta

    from sqlalchemy import update

    from infrastructure.database.models import ProxyServerDB

    # create_proxy возвращает DTO
    p1_dto = await create_proxy(client, "active.filter", 1001)
    p2_dto = await create_proxy(client, "inactive.filter", 1002)
    p3_dto = await create_proxy(client, "also.active", 1003)

    # Обновляем статусы в БД используя ID из DTO
    await db_session.execute(update(ProxyServerDB).where(ProxyServerDB.id == p1_dto.id).values(is_alive=True))
    await db_session.execute(update(ProxyServerDB).where(ProxyServerDB.id == p2_dto.id).values(is_alive=False))
    await db_session.execute(update(ProxyServerDB).where(ProxyServerDB.id == p3_dto.id).values(is_alive=True))

    # Запрос активных
    response_active = await client.get("/proxies?is_active=true")
    assert response_active.status_code == status.HTTP_200_OK
    data_active = response_active.json()
    assert len(data_active) == 2
    # Сверяем ID из DTO (как строки) с ID в JSON ответе
    assert {p["id"] for p in data_active} == {str(p1_dto.id), str(p3_dto.id)}
    # Проверяем поля DTO в ответе
    assert all(p["is_alive"] is True for p in data_active) # Теперь будет сверяться с полем is_alive в DTO

    # Запрос неактивных
    response_inactive = await client.get("/proxies?is_active=false")
    assert response_inactive.status_code == status.HTTP_200_OK
    data_inactive = response_inactive.json()
    assert len(data_inactive) == 1
    # Сверяем ID из DTO (как строку) с ID в JSON ответе
    assert data_inactive[0]["id"] == str(p2_dto.id)
    assert data_inactive[0]["is_alive"] is False # Проверяем поле is_alive

async def test_list_proxies_filter_by_protocol(client: AsyncClient, db_session: AsyncSession):
    """Проверяет фильтрацию по протоколу (без учета регистра)."""
    from sqlalchemy import update

    from infrastructure.database.models import ProxyServerDB

    p1 = await create_proxy(client, "proto.http", 2001)
    p2 = await create_proxy(client, "proto.https", 2002)
    p3 = await create_proxy(client, "proto.socks", 2003)

    # Обновляем протоколы в БД (по умолчанию они не задаются)
    # Используем pN.id (UUID) для запросов к БД
    await db_session.execute(update(ProxyServerDB).where(ProxyServerDB.id == p1.id).values({ProxyServerDB.protocol: 'HTTP'}))
    await db_session.execute(update(ProxyServerDB).where(ProxyServerDB.id == p2.id).values({ProxyServerDB.protocol: 'https'}))
    await db_session.execute(update(ProxyServerDB).where(ProxyServerDB.id == p3.id).values({ProxyServerDB.protocol: 'socks5'}))

    # Запрос HTTP (нижний регистр)
    response_http = await client.get("/proxies?protocol=http")
    assert response_http.status_code == status.HTTP_200_OK
    data_http = response_http.json()
    assert len(data_http) == 1
    # Сравниваем строковое представление ID
    assert data_http[0]["id"] == str(p1.id)

    # Запрос HTTPS (смешанный регистр)
    response_https = await client.get("/proxies?protocol=HtTpS")
    assert response_https.status_code == status.HTTP_200_OK
    data_https = response_https.json()
    assert len(data_https) == 1
    # Сравниваем строковое представление ID
    assert data_https[0]["id"] == str(p2.id)

async def test_list_proxies_filter_by_country(client: AsyncClient, db_session: AsyncSession):
    """Проверяет фильтрацию по стране (без учета регистра)."""
    from sqlalchemy import update

    from infrastructure.database.models import ProxyServerDB

    p1 = await create_proxy(client, "country.us", 3001)
    p2 = await create_proxy(client, "country.de", 3002)
    p3 = await create_proxy(client, "country.us.again", 3003)

    # Обновляем страны в БД
    # Используем pN.id (UUID)
    await db_session.execute(update(ProxyServerDB).where(ProxyServerDB.id == p1.id).values({ProxyServerDB.country: 'US'}))
    await db_session.execute(update(ProxyServerDB).where(ProxyServerDB.id == p2.id).values({ProxyServerDB.country: 'de'}))
    await db_session.execute(update(ProxyServerDB).where(ProxyServerDB.id == p3.id).values({ProxyServerDB.country: 'us'}))

    # Запрос US (верхний регистр)
    response_us = await client.get("/proxies?country=US")
    assert response_us.status_code == status.HTTP_200_OK
    data_us = response_us.json()
    assert len(data_us) == 2
    # Сравниваем строковые представления ID
    assert {p["id"] for p in data_us} == {str(p1.id), str(p3.id)}

    # Запрос de (нижний регистр)
    response_de = await client.get("/proxies?country=de")
    assert response_de.status_code == status.HTTP_200_OK
    data_de = response_de.json()
    assert len(data_de) == 1
    # Сравниваем строковое представление ID
    assert data_de[0]["id"] == str(p2.id)

async def test_list_proxies_sort_by_created_at(client: AsyncClient):
    """Проверяет сортировку по дате создания."""
    p1 = await create_proxy(client, "sort.created.1", 2001)
    await asyncio.sleep(0.01) # Небольшая пауза для гарантии разницы во времени
    p2 = await create_proxy(client, "sort.created.2", 2002)
    await asyncio.sleep(0.01)
    p3 = await create_proxy(client, "sort.created.3", 2003)

    # Сортировка по возрастанию (по умолчанию)
    response_asc = await client.get("/proxies?sort_by=created_at")
    assert response_asc.status_code == status.HTTP_200_OK
    data_asc = response_asc.json()
    # Сравниваем строковые представления ID
    assert [p["id"] for p in data_asc] == [str(p1.id), str(p2.id), str(p3.id)]
    # Проверяем, что created_at присутствует
    assert all("created_at" in p for p in data_asc)

    # Сортировка по убыванию
    response_desc = await client.get("/proxies?sort_by=created_at&sort_order=desc")
    assert response_desc.status_code == status.HTTP_200_OK
    data_desc = response_desc.json()
    # Сравниваем строковые представления ID
    assert [p["id"] for p in data_desc] == [str(p3.id), str(p2.id), str(p1.id)]
    assert all("created_at" in p for p in data_desc)

async def test_list_proxies_sort_by_last_checked_at(client: AsyncClient, db_session: AsyncSession):
    """Проверяет сортировку по дате последней проверки."""
    from datetime import datetime, timedelta, timezone  # Добавляем timezone

    from sqlalchemy import update

    from infrastructure.database.models import ProxyServerDB

    # Используем aware datetime
    now = datetime.now(timezone.utc)

    p1 = await create_proxy(client, "sort.checked.1", 3001)
    p2 = await create_proxy(client, "sort.checked.2", 3002)
    p3 = await create_proxy(client, "sort.checked.3", 3003)

    # Обновляем last_checked_at в БД, используя pN.id (UUID)
    await db_session.execute(update(ProxyServerDB).where(ProxyServerDB.id == p1.id).values(last_checked_at=now - timedelta(minutes=10)))
    await db_session.execute(update(ProxyServerDB).where(ProxyServerDB.id == p2.id).values(last_checked_at=now))
    await db_session.execute(update(ProxyServerDB).where(ProxyServerDB.id == p3.id).values(last_checked_at=now - timedelta(minutes=5)))

    # Сортировка по возрастанию (старые сначала)
    response_asc = await client.get("/proxies?sort_by=last_checked_at&sort_order=asc")
    assert response_asc.status_code == status.HTTP_200_OK
    data_asc = response_asc.json()
    assert len(data_asc) >= 3
    # Проверяем порядок тех, у кого есть дата, сравнивая строковые ID
    ids_with_date = [p["id"] for p in data_asc if p["last_checked_at"] is not None]
    expected_ids_asc = [str(p1.id), str(p3.id), str(p2.id)]
    assert ids_with_date[-3:] == expected_ids_asc
    # Проверяем, что last_checked присутствует в ответе
    assert all("last_checked_at" in p for p in data_asc if p["id"] in [str(p1.id), str(p2.id), str(p3.id)])

    # Сортировка по убыванию (новые сначала)
    response_desc = await client.get("/proxies?sort_by=last_checked_at&sort_order=desc")
    assert response_desc.status_code == status.HTTP_200_OK
    data_desc = response_desc.json()
    assert len(data_desc) >= 3
    ids_with_date_desc = [p["id"] for p in data_desc if p["last_checked_at"] is not None]
    expected_ids_desc = [str(p2.id), str(p3.id), str(p1.id)]
    assert ids_with_date_desc[:3] == expected_ids_desc
    assert all("last_checked_at" in p for p in data_desc if p["id"] in [str(p1.id), str(p2.id), str(p3.id)])

async def test_list_proxies_combined_filter_sort(client: AsyncClient, db_session: AsyncSession):
    """Проверяет комбинированную фильтрацию и сортировку."""
    from datetime import datetime, timedelta, timezone

    from sqlalchemy import update

    from infrastructure.database.models import ProxyServerDB

    # Создаем прокси
    p1 = await create_proxy(client, "combo.http.us.1", 6001)
    await asyncio.sleep(0.01)
    p2 = await create_proxy(client, "combo.https.de", 6002)
    await asyncio.sleep(0.01)
    p3 = await create_proxy(client, "combo.http.us.2", 6003)
    await asyncio.sleep(0.01)
    p4 = await create_proxy(client, "combo.socks.us", 6004)

    # Обновляем данные в БД
    now = datetime.now(timezone.utc)
    await db_session.execute(update(ProxyServerDB).where(ProxyServerDB.id == p1.id).values({
        ProxyServerDB.protocol: 'HTTP',
        ProxyServerDB.country: 'US',
        ProxyServerDB.is_alive: True,
        ProxyServerDB.last_checked_at: now - timedelta(minutes=10)
    }))
    await db_session.execute(update(ProxyServerDB).where(ProxyServerDB.id == p2.id).values({
        ProxyServerDB.protocol: 'HTTPS',
        ProxyServerDB.country: 'DE',
        ProxyServerDB.is_alive: True,
        ProxyServerDB.last_checked_at: now - timedelta(minutes=5)
    }))
    await db_session.execute(update(ProxyServerDB).where(ProxyServerDB.id == p3.id).values({
        ProxyServerDB.protocol: 'http',
        ProxyServerDB.country: 'us',
        ProxyServerDB.is_alive: False,
        ProxyServerDB.last_checked_at: now - timedelta(minutes=15)
    }))
    await db_session.execute(update(ProxyServerDB).where(ProxyServerDB.id == p4.id).values({
        ProxyServerDB.protocol: 'socks5',
        ProxyServerDB.country: 'US',
        ProxyServerDB.is_alive: True,
        ProxyServerDB.last_checked_at: now - timedelta(minutes=1)
    }))

    # Ищем активные HTTP прокси из US, сортируем по last_checked_at по убыванию
    query_params = "is_active=true&protocol=http&country=US&sort_by=last_checked_at&sort_order=desc"
    response = await client.get(f"/proxies?{query_params}")

    assert response.status_code == status.HTTP_200_OK
    data = response.json()

    # Ожидаем только p1
    assert len(data) == 1
    # Сравниваем строковое представление ID
    assert data[0]["id"] == str(p1.id)
    assert data[0]["protocol"].lower() == "http"
    assert data[0]["country"].lower() == "us"
    assert data[0]["is_alive"] is True

    # Ищем все прокси из US, сортируем по created_at по возрастанию
    query_params_us = "country=us&sort_by=created_at&sort_order=asc"
    response_us = await client.get(f"/proxies?{query_params_us}")
    assert response_us.status_code == status.HTTP_200_OK
    data_us = response_us.json()
    assert len(data_us) == 3
    ids_us = [p["id"] for p in data_us]
    # Сравниваем строковые представления ID
    assert ids_us == [str(p1.id), str(p3.id), str(p4.id)]

    # Убедиться, что все проверки в тестах фильтрации и сортировки используют поля DTO
    # Например, в test_list_proxies_combined_filter_sort проверить is_alive в ответе
