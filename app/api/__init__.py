"""API package."""
from fastapi import FastAPI
from app.utils.database import engine, Base
from dotenv import load_dotenv

load_dotenv()

Base.metadata.create_all(bind=engine)

app = FastAPI()

# Импорт роутеров после создания app
from app.api.v1.endpoints import address_info, address_requests

app.include_router(address_info.router)
app.include_router(address_requests.router)
# Пустой файл, нужен только для обозначения пакета