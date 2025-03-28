from fastapi import FastAPI
from typing import Dict  # Добавлен импорт Dict
from app.api.v1.endpoints import address_info, address_requests
from app.utils.database import engine, Base

# Создание таблиц в базе данных
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Tron Address Info Service",
    description="Microservice for getting Tron address information",
    version="1.0.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc"
)

# Подключение роутеров
app.include_router(address_info.router)
app.include_router(address_requests.router)

@app.get("/health", tags=["healthcheck"])
async def health_check() -> Dict[str, str]:
    """Проверка работоспособности сервиса.
    
    Returns:
        Dict[str, str]: Статус сервиса
    """
    return {"status": "healthy"}