from pydantic import BaseModel

class AddressInfo(BaseModel):
    """Схема для представления информации о Tron-адресе"""
    address: str
    bandwidth: int
    energy: int
    trx_balance: int

    class Config:
        from_attributes = True