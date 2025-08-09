# Используем Python 3.10
FROM python:3.10-slim-bookworm

# Установка зависимостей системы
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Рабочая директория приложения
WORKDIR /app

# Копирование requirements.txt первым для кэширования слоя
COPY requirements.txt .

RUN pip install --upgrade pip

# Установка Python зависимостей с указанием совместимости
RUN pip install --no-cache-dir -r requirements.txt

# Копирование всего проекта
COPY . .

# Команда запуска (будет переопределена в docker-compose)
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]