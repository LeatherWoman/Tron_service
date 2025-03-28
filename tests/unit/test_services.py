from unittest.mock import MagicMock, patch
from tronpy.exceptions import AddressNotFound
from app.services.tron_service import TronService

VALID_TEST_ADDRESS = "TR7NHqjeKQxGTCi8q8ZY4pL8otSzgjLj6t"

@patch("app.services.tron_service.Tron")
def test_get_address_info_success(mock_tron: MagicMock) -> None:
    """Тест успешного получения информации о Tron-адресе."""
    # Настройка моков
    mock_client = MagicMock()
    mock_tron.return_value = mock_client
    
    # Мокируем ответы API
    mock_client.get_account.return_value = {"balance": 1000}
    mock_client.get_account_resource.return_value = {
        "free_net_limit": 5000,
        "energy_limit": 2000
    }
    
    service = TronService()
    # Переопределяем клиент для теста
    service.client = mock_client
    
    result = service.get_address_info(VALID_TEST_ADDRESS)
    
    assert result == {
        "bandwidth": 5000,
        "energy": 2000,
        "trx_balance": 1000
    }

@patch("app.services.tron_service.Tron")
def test_get_address_info_not_found(mock_tron: MagicMock) -> None:
    """Тест случая, когда Tron-адрес не найден."""
    mock_client = MagicMock()
    mock_tron.return_value = mock_client
    
    mock_client.get_account.side_effect = AddressNotFound("Address not found")
    
    service = TronService()
    # Переопределяем клиент для теста
    service.client = mock_client
    
    result = service.get_address_info(VALID_TEST_ADDRESS)
    
    assert result is None