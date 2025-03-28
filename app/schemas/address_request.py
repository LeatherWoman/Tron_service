from datetime import datetime
from pydantic import BaseModel
from typing import Optional, List

class AddressRequestBase(BaseModel):
    address: str

class AddressRequestCreate(AddressRequestBase):
    pass

class AddressRequest(AddressRequestBase):
    id: int
    bandwidth: Optional[int] = None
    energy: Optional[int] = None
    trx_balance: Optional[int] = None
    created_at: datetime

    class Config:
        from_attributes = True  # Обновлено для Pydantic v2

class AddressRequestPaginated(BaseModel):
    items: List[AddressRequest]
    total: int
    page: int
    size: int