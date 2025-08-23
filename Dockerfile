FROM python:3.11

# Установка системных зависимостей
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    gcc \
    libpq-dev \
    libpq5 \
    && rm -rf /var/lib/apt/lists/*

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV SECRET_KEY=temp_secret_key_for_build

WORKDIR /app

# Создаем директорию для статических файлов
RUN mkdir -p /app/staticfiles
&& pip install --upgrade pip
COPY requirements.txt .
RUN pip install -r requirements.txt
&& pip install gunicorn==21.2.0

COPY . .

# Запускаем collectstatic
RUN python manage.py collectstatic --noinput