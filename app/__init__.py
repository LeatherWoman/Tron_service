"""Основной модуль приложения FastAPI."""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.utils.database import engine, Base
from app.api.v1.endpoints import address_info, address_requests

# Создаем таблицы в базе данных
Base.metadata.create_all(bind=engine)

# Инициализация приложения FastAPI
app = FastAPI(
    title="Tron Address Info Service",
    description="Микросервис для получения информации о кошельках в сети Tron",
    version="1.0.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc"
)

# Настройка CORS (при необходимости)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Подключаем роутеры
app.include_router(address_info.router)
app.include_router(address_requests.router)