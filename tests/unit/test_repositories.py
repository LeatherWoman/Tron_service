from sqlalchemy.orm import Session
from datetime import datetime
from app.models.address_request import AddressRequest
from app.repositories.address_request_repository import AddressRequestRepository

VALID_TEST_ADDRESS = "TR7NHqjeKQxGTCi8q8ZY4pL8otSzgjLj6t"

def test_create_address_request(db_session: Session) -> None:
    """Тест создания запроса информации о Tron-адресе."""
    repo = AddressRequestRepository(db_session)
    
    request = repo.create(
        address=VALID_TEST_ADDRESS,
        bandwidth=1000,
        energy=500,
        trx_balance=100
    )
    
    assert request.id is not None
    assert request.address == VALID_TEST_ADDRESS
    assert request.bandwidth == 1000
    assert request.energy == 500
    assert request.trx_balance == 100
    assert isinstance(request.created_at, datetime)
    
    db_request = db_session.query(AddressRequest).filter(AddressRequest.id == request.id).first()
    assert db_request == request