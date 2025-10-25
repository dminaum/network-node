FROM python:3.11-slim as base

# Установка переменных окружения
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    POETRY_VERSION=1.8.3 \
    POETRY_HOME="/opt/poetry" \
    POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_CREATE=false

# Добавление Poetry в PATH
ENV PATH="$POETRY_HOME/bin:$PATH"

# Установка системных зависимостей
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    postgresql-client \
    gcc \
    python3-dev \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Установка Poetry
RUN curl -sSL https://install.python-poetry.org | python3 - && \
    poetry --version

# Создание рабочей директории
WORKDIR /app

# Копирование файлов Poetry
COPY pyproject.toml poetry.lock* ./

# Установка зависимостей (без dev зависимостей для продакшена)
RUN poetry install --no-root --only main

# Копирование проекта
COPY . .

# Создание пользователя без root прав
RUN adduser --disabled-password --gecos '' appuser && \
    chown -R appuser:appuser /app
USER appuser

# Expose порт
EXPOSE 8000

# ===== Development stage =====
FROM base as development

USER root

# Установка dev зависимостей
RUN poetry install --no-root

USER appuser

# ===== Production stage =====
FROM base as production

CMD ["sh", "-c", "python manage.py wait_for_db && python manage.py migrate && python manage.py runserver 0.0.0.0:8000"]
