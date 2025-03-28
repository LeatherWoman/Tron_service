# Tron Address Info Microservice

Микросервис для получения информации о кошельках в сети Tron (TRX), включая баланс, bandwidth и energy. Сервис сохраняет историю запросов в базу данных.

## Возможности

- Получение информации о Tron-адресе (баланс TRX, bandwidth, energy)
- Сохранение истории запросов в БД
- Просмотр истории запросов с пагинацией
- Полноценное API с документацией (Swagger/Redoc)

## Установка

1. Клонируйте репозиторий

2. Установите зависимости:
pip install -e .

3. Настройте окружение (при необходимости):
Создайте файл .env и укажите параметры подключения к БД и Tron API

Пример .env файла:
TRON_API_KEY=Your_key
DATABASE_URL=sqlite:///./tron_address_service.db
TRON_NETWORK=mainnet  # или nile для тестовой сети

Также создайте .env.test файл

Пример:

ENV=TEST
TRON_API_KEY=Your_key
TRON_NETWORK=nile

##  Запуск
Запустите сервис с помощью Uvicorn:

uvicorn app.main:app --reload

* Сервис будет доступен по адресу:
http://localhost:8000

* Если сервер не работает создайте на другом порте
uvicorn app.main:app --port 8002 --reload

## API Документация

После запуска сервиса доступны:

* Swagger UI: http://localhost:8000/api/docs

* ReDoc: http://localhost:8000/api/redoc

* Health check: http://localhost:8000/health

## Тестирование

Для запуска тестов используйте:

* pytest tests/ -v 
* pytest --cov=app tests/

## Проверка Эндпоинтов
Get запрос:

curl "http://localhost:8000/api/v1/requests/?page=1&size=5"

Post запросы:

curl -X POST "http://localhost:8000/api/v1/address/info"      -H "Content-Type: application/json"   
   -d '{"address": "TR7NHqjeKQxGTCi8q8ZY4pL8otSzgjLj6t"}'


curl -X POST "http://localhost:8002/api/v1/address/info"      -H "Content-Type: application/json"   
   -d '{"address": "TXLAQ63Xg1NAzckPwKHvzv7YFyZUDNvsTC"}'
