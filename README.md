# LMS Django REST API

Проект системы управления обучением (LMS) на основе Django REST Framework с полным CI/CD пайплайном.

## 🚀 Особенности

- **Django REST Framework** - мощный API для образовательной платформы
- **Docker & Docker Compose** - контейнеризация приложения
- **Nginx + Gunicorn** - продакшен-окружение
- **PostgreSQL** - надежная база данных
- **GitHub Actions** - автоматический CI/CD
- **Systemd** - управление сервисами на сервере

## 📋 Требования

- Docker 20.10+
- Docker Compose 2.0+
- Python 3.11+
- Ubuntu 22.04 LTS (для продакшена)

## 🏗️ Структура проекта
lms-django-rest/
├── .github/workflows/ # GitHub Actions workflows
├── lms_backend/ # Основное приложение Django
├── courses/ # Модуль курсов
├── users/ # Модуль пользователей
├── subscriptions/ # Модуль подписок
├── payments/ # Модуль платежей
├── docker-compose.prod.yml # Продакшен-конфигурация
├── Dockerfile # Docker образ приложения
├── nginx.conf # Конфигурация Nginx
└── requirements.txt # Зависимости Python


## 🚀 Быстрый старт

### Локальная разработка

```bash
# Клонирование репозитория
git clone -b develop https://github.com/st1lm4n/-LMS--Django-REST.git
cd -LMS--Django-REST

# Создание виртуального окружения
python -m venv venv
source venv/bin/activate # Linux/Mac
или
venv\Scripts\activate    # Windows

# Установка зависимостей
pip install -r requirements.txt

# Настройка окружения
cp .env_template .env
# Отредактируйте .env файл с вашими настройками

# Запуск миграций
python manage.py migrate

# Запуск сервера разработки
python manage.py runserver
```

### Продакшен-развертывание с Docker
```bash
# Клонирование на сервере
sudo mkdir -p /opt/lms
sudo chown -R $USER:$USER /opt/lms
cd /opt/lms
git clone -b develop https://github.com/st1lm4n/-LMS--Django-REST.git .

# Настройка окружения
cp .env_template .env
nano .env  # Заполните реальными значениями

# Запуск контейнеров
docker-compose -f docker-compose.prod.yml up -d --build

# Выполнение миграций
docker-compose -f docker-compose.prod.yml exec web python manage.py migrate

# Создание суперпользователя
docker-compose -f docker-compose.prod.yml exec web python manage.py createsuperuser

# Проверка статуса
docker-compose -f docker-compose.prod.yml ps
```

# 🔧 Настройка сервера
1. Обновление системы и установка базовых пакетов
```bash
sudo apt update && sudo apt upgrade -y
sudo apt install -y curl git ufw
```
2. Установка Docker и Docker Compose
```bash
# Установка Docker
curl -fsSL https://get.docker.com | sh
sudo usermod -aG docker $USER
sudo systemctl enable docker

# Установка Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/download/v2.23.3/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose
```
3. Настройка брандмауэра
```bash
sudo ufw allow OpenSSH
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp
sudo ufw --force enable
```
4. Настройка SSH доступа
```bash
# Генерация SSH ключа на локальной машине
ssh-keygen -t ed25519 -C "your_email@example.com"

# Копирование ключа на сервер
ssh-copy-id -i ~/.ssh/id_ed25519.pub user@your-server-ip

# Отключение парольной аутентификации (опционально)
sudo nano /etc/ssh/sshd_config
# Установите: PasswordAuthentication no
sudo systemctl restart sshd
```
# ⚙️ Настройка CI/CD
## GitHub Secrets
Добавьте в Secrets репозитория (Settings → Secrets → Actions):

- `SERVER_IP`: IP адрес вашего сервера

- `SERVER_USER`: SSH пользователь (например, `test`)

- `SSH_PRIVATE_KEY`: Приватный SSH ключ

- `TEST_SECRET_KEY`: Секретный ключ для тестов Django

## Workflow процесс
1. Push в ветку develop → запускает workflow

2. Тестирование → запуск pytest тестов

3. Деплой → автоматическое развертывание на сервер

4. Уведомления → статус сборки в Telegram/Slack

# 🐳 Docker Compose продекшен
Файл `docker-compose.prod.yml`
```yaml
version: '3.8'

services:
  db:
    image: postgres:15
    environment:
      POSTGRES_DB: ${POSTGRES_DB}
      POSTGRES_USER: ${POSTGRES_USER}
      POSTGRES_PASSWORD: ${POSTGRES_PASSWORD}
    volumes:
      - postgres_data:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U ${POSTGRES_USER} -d ${POSTGRES_DB}"]
      interval: 10s
      timeout: 5s
      retries: 5

  web:
    build: .
    command: gunicorn --bind 0.0.0.0:8000 lms_backend.wsgi:application
    env_file:
      - .env
    volumes:
      - static_volume:/app/staticfiles
    depends_on:
      db:
        condition: service_healthy
    restart: unless-stopped

  nginx:
    image: nginx:1.25-alpine
    ports:
      - "80:80"
    volumes:
      - ./nginx.conf:/etc/nginx/conf.d/default.conf
      - static_volume:/app/staticfiles
    depends_on:
      - web
    restart: unless-stopped

volumes:
  postgres_data:
  static_volume:
```

# 🔐 Переменные окружения
Создайте файл `.env` на основе `.env_template`:

```ini
# Django settings
DEBUG=0
SECRET_KEY=your-super-secret-key-here
ALLOWED_HOSTS=localhost,127.0.0.1,your-server-ip

# Database settings
DB_NAME=lms_db
DB_USER=db_user
DB_PASSWORD=strong-password-here
DB_HOST=db
DB_PORT=5432

# PostgreSQL settings
POSTGRES_DB=lms_db
POSTGRES_USER=db_user
POSTGRES_PASSWORD=strong-password-here
DATABASE_URL=postgres://db_user:strong-password-here@db:5432/lms_db

# Celery settings
CELERY_BROKER_URL=redis://redis:6379/0
CELERY_RESULT_BACKEND=redis://redis:6379/1
```

# 📊 Systemd сервис
## Создание сервисного файла
```bash
sudo nano /etc/systemd/system/lms.service
```
```ini
[Unit]
Description=LMS Docker Compose Application
After=docker.service
Requires=docker.service

[Service]
Type=oneshot
RemainAfterExit=yes
WorkingDirectory=/opt/lms
ExecStart=/usr/bin/docker compose -f docker-compose.prod.yml up -d
ExecStop=/usr/bin/docker compose -f docker-compose.prod.yml down
User=test
Group=docker
Restart=on-failure
RestartSec=30

[Install]
WantedBy=multi-user.target
```
## Активация сервиса
```bash
sudo systemctl daemon-reload
sudo systemctl enable lms.service
sudo systemctl start lms.service
sudo systemctl status lms.service
```

# 🧪 Тестирование
```bash
# Запуск тестов локально
python manage.py test

# Запуск тестов в CI
docker-compose -f docker-compose.prod.yml exec web python manage.py test

# Запуск с покрытием
coverage run manage.py test
coverage report
```

# 📞 Мониторинг и логи

```bash
# Просмотр логов приложения
docker-compose -f docker-compose.prod.yml logs -f web

# Просмотр логов базы данных
docker-compose -f docker-compose.prod.yml logs -f db

# Просмотр логов Nginx
docker-compose -f docker-compose.prod.yml logs -f nginx

# Systemd логи сервиса
sudo journalctl -u lms.service -f
```

# 🔧 Утилиты управления

```bash
# Сборка статических файлов
docker-compose -f docker-compose.prod.yml exec web python manage.py collectstatic --noinput

# Создание миграций
docker-compose -f docker-compose.prod.yml exec web python manage.py makemigrations

# Выполнение миграций
docker-compose -f docker-compose.prod.yml exec web python manage.py migrate

# Создание суперпользователя
docker-compose -f docker-compose.prod.yml exec web python manage.py createsuperuser

# Django shell
docker-compose -f docker-compose.prod.yml exec web python manage.py shell
```

# 🚨 Устранение неполадок
## Ошибка подключения к базе данных

```bash
# Проверка подключения к БД
docker-compose -f docker-compose.prod.yml exec web python -c "
import psycopg2
import os
try:
    conn = psycopg2.connect(
        dbname=os.environ.get('POSTGRES_DB'),
        user=os.environ.get('POSTGRES_USER'),
        password=os.environ.get('POSTGRES_PASSWORD'),
        host='db',
        port='5432'
    )
    print('✅ Подключение успешно')
    conn.close()
except Exception as e:
    print('❌ Ошибка:', e)
"
```

## Ошибка статических файлов
Проверьте правильность путей в `nginx.conf` и настройки `STATIC_ROOT` в Django.


# 🤝 Вклад в проект
1. Форкните репозиторий

2. Создайте feature ветку (`git checkout -b feature/amazing-feature`)

3. Закоммитьте изменения (`git commit -m 'Add some amazing feature'`)

4. Запушьте в ветку (`git push origin feature/amazing-feature`)

5. Откройте Pull Request

# 📧 Контакты
Сергей Скапинцев - [@st1lm4n](https://github.com/st1lm4n)

Ссылка на проект: https://github.com/st1lm4n/-LMS--Django-REST