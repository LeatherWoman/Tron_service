from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from unittest.mock import patch, MagicMock
from fastapi import status

VALID_TEST_ADDRESS = "TR7NHqjeKQxGTCi8q8ZY4pL8otSzgjLj6t"

def test_get_address_info_success(client: TestClient, db_session: Session) -> None:
    """Интеграционный тест успешного запроса информации о Tron-адресе."""
    # Создаем мок для TronService
    mock_service = MagicMock()
    mock_service.get_address_info.return_value = {
        "bandwidth": 5000,
        "energy": 2000,
        "trx_balance": 1000
    }

    # Патчим зависимость
    with patch("app.api.v1.endpoints.address_info.TronService") as mock_tron_service:
        mock_tron_service.return_value = mock_service
        
        # Выполняем запрос
        response = client.post(
            "/api/v1/address/info",
            json={"address": VALID_TEST_ADDRESS}
        )
        
        # Проверяем результаты
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["address"] == VALID_TEST_ADDRESS
        assert data["bandwidth"] == 5000
        assert data["energy"] == 2000
        assert data["trx_balance"] == 1000