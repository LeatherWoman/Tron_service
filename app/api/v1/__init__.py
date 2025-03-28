from fastapi import APIRouter

router = APIRouter()

# Импорт после создания router
from .endpoints import address_info, address_requests

router.include_router(address_info.router)
router.include_router(address_requests.router)