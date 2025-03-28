from fastapi import APIRouter, Depends, Query
from app.schemas.address_request import AddressRequestPaginated
from app.repositories.address_request_repository import AddressRequestRepository
from app.utils.database import get_db
from sqlalchemy.orm import Session


router = APIRouter(prefix="/api/v1/requests", tags=["requests"])


@router.get("/", response_model=AddressRequestPaginated)
async def get_address_requests(
    page: int = Query(1, ge=1, description="Номер страницы (начиная с 1)"),
    size: int = Query(10, ge=1, le=100, description="Количество элементов на странице (1-100)"),
    db: Session = Depends(get_db)
) -> AddressRequestPaginated:
    """Получение списка последних запросов с пагинацией.
    
    Args:
        page (int): Номер страницы
        size (int): Количество элементов на странице
        db (Session): Сессия базы данных
        
    Returns:
        AddressRequestPaginated: Пагинированный список запросов
    """
    repo = AddressRequestRepository(db)
    return repo.get_latest_requests(page=page, size=size)