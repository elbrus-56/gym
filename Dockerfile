# Этап 1: Установка зависимостей
FROM python:3.12-slim as builder

WORKDIR /app

# Устанавливаем системные зависимости, если они нужны (например, для psycopg2)
# RUN apt-get update && apt-get install -y --no-install-recommends gcc libpq-dev && rm -rf /var/lib/apt/lists/*

# Создаем виртуальное окружение
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Копируем файл зависимостей и устанавливаем их
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# Этап 2: Сборка финального образа
FROM python:3.12-slim

WORKDIR /app

# Копируем виртуальное окружение из этапа сборки
COPY --from=builder /opt/venv /opt/venv

# Копируем код приложения
COPY . .

# Указываем Python использовать виртуальное окружение
ENV PATH="/opt/venv/bin:$PATH"

# Открываем порт, на котором работает FastAPI (по умолчанию 8000)
EXPOSE 8000

# Запускаем миграции Alembic при старте контейнера (опционально, но рекомендуется)
# И затем запускаем Uvicorn
# Важно: Используем shell form для CMD, чтобы переменные окружения из .env (если они монтируются) работали
CMD ["sh", "-c", "alembic upgrade head && uvicorn main:app --host 0.0.0.0 --port 8000"] 