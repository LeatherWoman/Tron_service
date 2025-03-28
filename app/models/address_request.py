from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime
from app.utils.database import Base


class AddressRequest(Base):
    """Модель базы данных для хранения запросов информации о Tron-адресах."""
    
    __tablename__ = "address_requests"

    id = Column(Integer, primary_key=True, index=True)
    address = Column(String, index=True)
    bandwidth = Column(Integer, nullable=True)
    energy = Column(Integer, nullable=True)
    trx_balance = Column(Integer, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    def __repr__(self) -> str:
        """Строковое представление объекта для отладки."""
        return f"<AddressRequest {self.address} at {self.created_at}>"