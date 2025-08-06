# Food Delivery Service - Test Project

Этот проект был сформирован с помощью языковой модели (deepseek) для практики написания автотестов. 
Он представляет собой полноценный сервис доставки еды с бэкендом на FastAPI и фронтендом на Vue.js.

## Технологический стек
- **Backend**: Python + FastAPI + PostgreSQL + Redis + RabbitMQ
- **Frontend**: Vue 3 + TypeScript + Pinia
- **Инфраструктура**: Docker + Docker Compose

## Полная инструкция по запуску

### 1. Клонирование репозитория
```bash
git clone https://github.com/KoLeNnKo/food-delivery-test-project.git
cd food-delivery-test-project 
```

### 2. Запуск через Docker Compose
```bash
docker-compose up --build
```

После сборки сервисы будут доступны:

    Бэкенд API: http://localhost:8000
    Фронтенд: http://localhost:5173
    Админка RabbitMQ: http://localhost:15672 (guest/guest)
    PostgreSQL: порт 5432
    Redis: порт 6379
    Swagger: http://localhost:8000/docs
    RabbitMQ: http://localhost:15672


### 3. Инициализация базы данных
После запуска выполните миграции:
```bash
docker-compose exec backend alembic upgrade head
```

### 4. Тестовые данные
Для загрузки тестовых данных выполните:
```bash
docker-compose exec backend python -m app.db.seed
```

Доступные API endpoints

Основные эндпоинты (полная документация в Swagger UI):

    POST /auth/register - Регистрация
    POST /auth/login - Авторизация
    GET /restaurants - Список ресторанов
    POST /orders - Создание заказа
    GET /api/docs - Swagger документация

Структура проекта
```
food-delivery/
├── backend/          # FastAPI приложение
├── frontend/         # Vue.js приложение
├── docker-compose.yml # Конфигурация Docker
└── README.md         # Документация
```