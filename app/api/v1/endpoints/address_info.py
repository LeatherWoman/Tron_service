from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.schemas.address_info import AddressInfo
from app.schemas.address_request import AddressRequestCreate
from app.services.tron_service import TronService
from app.repositories.address_request_repository import AddressRequestRepository
from app.utils.database import get_db

router = APIRouter(prefix="/api/v1/address", tags=["address"])

def get_tron_service():
    return TronService()

@router.post("/info", response_model=AddressInfo)
async def get_address_info(
    request: AddressRequestCreate,
    db: Session = Depends(get_db),
    tron_service: TronService = Depends(get_tron_service)
) -> AddressInfo:
    """Получение информации о Tron-адресе"""
    if not tron_service.is_valid_address(request.address):
        raise HTTPException(
            status_code=400,
            detail="Invalid Tron address format. Valid address must start with 'T' and contain exactly 34 alphanumeric characters"
        )

    address_info = tron_service.get_address_info(request.address)
    
    if not address_info:
        raise HTTPException(
            status_code=404,
            detail="Address not found or error occurred"
        )
    
    # Логируем запрос
    repo = AddressRequestRepository(db)
    repo.create(
        address=request.address,
        bandwidth=address_info["bandwidth"],
        energy=address_info["energy"],
        trx_balance=address_info["trx_balance"]
    )
    
    return AddressInfo(
        address=request.address,
        bandwidth=address_info["bandwidth"],
        energy=address_info["energy"],
        trx_balance=address_info["trx_balance"]
    )