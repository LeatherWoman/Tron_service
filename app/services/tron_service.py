from tronpy import Tron
from tronpy.exceptions import AddressNotFound
from tronpy.providers import HTTPProvider
from typing import Optional, Dict
import logging
import os

logger = logging.getLogger(__name__)

class TronService:
    def __init__(self):
        """Инициализация Tron клиента с резервными провайдерами"""
        self.client = self._init_client()

    def _init_client(self):
        """Инициализация клиента с резервными вариантами подключения"""
        providers = [
            {"url": "https://api.trongrid.io", "api_key": os.getenv("TRON_API_KEY")},
            {"url": "https://nile.trongrid.io", "api_key": os.getenv("TRON_API_KEY")},
            {"url": "https://api.shasta.trongrid.io", "api_key": None}  # Тестовая сеть Shasta
        ]
        
        for provider in providers:
            try:
                http_provider = HTTPProvider(
                    endpoint_uri=provider["url"],
                    api_key=provider["api_key"]
                )
                return Tron(provider=http_provider)
            except Exception as e:
                logger.warning(f"Failed to connect to {provider['url']}: {e}")
                continue
                
        raise ConnectionError("Could not connect to any Tron network provider")

    def get_address_info(self, address: str) -> Optional[Dict[str, int]]:
        """Получение информации о Tron-адресе"""
        try:
            if not self.is_valid_address(address):
                return None
                
            account = self.client.get_account(address)
            resources = self.client.get_account_resource(address)
            
            return {
                "bandwidth": resources.get("free_net_limit", 0),
                "energy": resources.get("energy_limit", 0),
                "trx_balance": account.get("balance", 0)
            }
        except AddressNotFound:
            logger.warning(f"Address not found: {address}")
            return None
        except Exception as e:
            logger.error(f"Error getting address info: {e}")
            return None

    @staticmethod
    def is_valid_address(address: str) -> bool:
        """Проверка валидности Tron адреса"""
        try:
            return (isinstance(address, str) 
                    and address.startswith('T') 
                    and len(address) == 34
                    and all(c in '123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz' 
                           for c in address))
        except Exception:
            return False