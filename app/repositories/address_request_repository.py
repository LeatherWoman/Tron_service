from typing import Optional, List
from sqlalchemy.orm import Session
from app.models.address_request import AddressRequest
from app.schemas.address_request import AddressRequestPaginated


class AddressRequestRepository:
    """Репозиторий для работы с запросами информации о Tron-адресах в базе данных."""
    
    def __init__(self, db: Session) -> None:
        """Инициализация репозитория с сессией базы данных.
        
        Args:
            db (Session): Сессия SQLAlchemy
        """
        self.db = db

    def create(
        self, 
        address: str, 
        bandwidth: Optional[int] = None, 
        energy: Optional[int] = None, 
        trx_balance: Optional[int] = None
    ) -> AddressRequest:
        """Создание нового запроса информации о Tron-адресе.
        
        Args:
            address (str): Tron-адрес
            bandwidth (Optional[int]): Пропускная способность
            energy (Optional[int]): Энергия
            trx_balance (Optional[int]): Баланс TRX
            
        Returns:
            AddressRequest: Созданный объект запроса
        """
        db_request = AddressRequest(
            address=address,
            bandwidth=bandwidth,
            energy=energy,
            trx_balance=trx_balance
        )
        self.db.add(db_request)
        self.db.commit()
        self.db.refresh(db_request)
        return db_request

    def get_latest_requests(
        self, 
        page: int = 1, 
        size: int = 10
    ) -> AddressRequestPaginated:
        """Получение последних запросов с пагинацией.
        
        Args:
            page (int): Номер страницы (начиная с 1)
            size (int): Количество элементов на странице
            
        Returns:
            AddressRequestPaginated: Пагинированный список запросов
        """
        query = self.db.query(AddressRequest).order_by(AddressRequest.created_at.desc())
        total = query.count()
        items = query.offset((page - 1) * size).limit(size).all()
        
        return AddressRequestPaginated(
            items=items,
            total=total,
            page=page,
            size=size
        )